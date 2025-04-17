import asyncio
import tempfile
from typing import Optional

import cv2
import numpy as np
from aiogram.types import FSInputFile
from cv2.typing import MatLike
from ultralytics import YOLO
from ultralytics.engine.results import Results

from bot.logger import logger


class DetectHandler:
    """DetectHandler class is a handler for processing detection requests.

    It manages loading models, running detections, and converting results.
    """

    _model: Optional["YOLO"] = None
    _instance: Optional["DetectHandler"] = None
    _lock = asyncio.Lock()

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path
        self._load_model()

    @classmethod
    async def get_instance(cls, model_path: str) -> "DetectHandler":
        async with cls._lock:
            if cls._model is None:
                cls._instance = cls(model_path)
            return cls._instance

    def _load_model(self) -> None:
        try:
            self._model = YOLO(self.model_path)
            logger.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    async def _process_results(self, results: Results, image: MatLike) -> list[bytes]:
        if not results:
            return []

        return [
            await self._crop_and_convert_to_bytes(box, image) for box in results.boxes
        ]

    async def _crop_and_convert_to_bytes(self, box: Results, image: MatLike) -> bytes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cropped_image = image[y1:y2, x1:x2]

        _, buffer = cv2.imencode(".jpg", cropped_image)
        return buffer.tobytes()

    def _draw_boxes(self, image: np.ndarray, results: Results) -> np.ndarray:
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

            confidence = None
            if hasattr(box, "conf") and box.conf is not None:
                try:
                    confidence = float(box.conf[0])
                except Exception as e:
                    logger.error(f"Error extracting confidence: {e}", exc_info=True)

            if confidence is not None:
                label = f"leaf {confidence * 100:.1f}%"
            else:
                label = "leaf"

            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 0, 0), 1, cv2.LINE_AA)
        return image


    async def detect(self, image_path: str) -> tuple[list[bytes], FSInputFile]:
        """Detect objects in the image.

        Args:
            image_path (str): Path to the image file.

        Returns:
            tuple: A tuple containing a list of cropped images and a photo file.

        """
        if self._model is None:
            logger.error("Model is not loaded.")
            raise ValueError("Model not loaded.")

        try:
            result = self._model.predict(
                image_path,
                task="detect",
                save=False,
                conf=0.5,
            )

            image = cv2.imread(image_path)
            if image is None:
                raise RuntimeError(f"Failed to load image from path: {image_path}")

            image_with_boxes = self._draw_boxes(image, result[0])

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                cv2.imwrite(temp_file.name, image_with_boxes)
                logger.info(f"Annotated image saved to temporary file: {temp_file.name}")

                photo = FSInputFile(temp_file.name)

            cropped_boxes = await self._process_results(result[0], image)
            logger.info(f"Processed {len(cropped_boxes)} cropped objects.")

            cropped_boxes = await self._process_results(result[0], image)
        except Exception as e:
            logger.error(f"Error during detection: {e}", exc_info=True)
            raise RuntimeError("Error processing the image") from e
        else:
            return cropped_boxes, photo
