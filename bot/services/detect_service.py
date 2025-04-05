import asyncio
from typing import Optional

import cv2
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
        """Initialize the DetectHandler with the model path.

        Args:
            model_path (str): Path to the model file.

        """
        self.model_path = model_path
        self._load_model()

    @classmethod
    async def get_instance(cls, model_path: str) -> "DetectHandler":
        """Get an instance of DetectHandler.

        If the instance does not exist, it will be created.
        If the model is not loaded, it will be loaded.

        Args:
            model_path (str): Path to the model file.

        Returns:
            DetectHandler: An instance of DetectHandler.

        """
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

    async def detect(self, image_path: str) -> list[bytes]:
        """Detect objects in the image at the given path.

        Args:
            image_path (str): Path to the image file.

        Returns:
            list[bytes]: List of cropped images as byte arrays.

        """
        if self._model is None:
            logger.error("Model is not loaded.")

            error_message = "Model not loaded."
            raise ValueError(error_message)

        try:
            result = self._model.predict(
                image_path,
                task="detect",
                save=False,
                conf=0.5,
            )

            image = cv2.imread(image_path)
            return await self._process_results(result[0], image)

        except Exception as e:
            logger.error(f"Detect error: {e!s}", exc_info=True)

            error_message = ("Error while processing the image")
            raise RuntimeError(error_message) from e
