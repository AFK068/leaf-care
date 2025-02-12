import io
import os

from PIL import Image
from ultralytics import YOLO

from mlcore.logger import logger
from mlcore.grpc_core.protos.predict import predict_pb2


class PredictHandler:
    """
    PredictHandler class is a handler for processing prediction requests.

    It manages loading models, running predictions, and converting results.
    """

    _models = {}  # Dictionary to store loaded models for each plant type.

    @classmethod
    def get_or_create_model(cls, plant_type):
        """
        Retrieves or creates a YOLO model for the specified plant type.

        :param plant_type: The type of plant.
        :return: A YOLO model instance for the specified plant type.
        """
        if plant_type not in cls._models:
            path = cls.get_model_path(plant_type)
            cls._models[plant_type] = YOLO(path)
            logger.info(f"Model loaded successfully for plant type: {plant_type}")

        return cls._models[plant_type]

    @staticmethod
    def bytes_to_image(image_data):
        """
        Converts raw image bytes into a PIL Image object.

        :param image_data: Raw image data in bytes.
        :return: A PIL Image object.
        """
        logger.debug("Converting raw image data to PIL Image")
        return Image.open(io.BytesIO(image_data))

    @staticmethod
    def get_model_path(plant_type):
        """
        Returns the file path to the model for the specified plant type.

        :param plant_type: The type of plant.
        :return: The absolute path to the model file.
        """
        BASE_MODEL_PATH = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                os.path.pardir,
                "models",
            )
        )

        model_paths = {
            predict_pb2.PLANT_CUCUMBER: "cucumber_cls_model.pt",
            predict_pb2.PLANT_MELON: "melons_cls_model.pt",
            predict_pb2.PLANT_PEPPER: "pepper_cls_model.pt",
            predict_pb2.PLANT_SALAD: "salad_cls_model.pt",
            predict_pb2.PLANT_STRAWBERRY: "strawberrie_cls_model.pt",
            predict_pb2.PLANT_TOMATO: "tomatoe_cls_model.pt",
            predict_pb2.PLANT_WATERMELON: "watermelon_cls_model.pt",
        }

        model_path = os.path.join(BASE_MODEL_PATH, model_paths[plant_type])
        logger.debug(f"Resolved model path for plant type {plant_type}: {model_path}")

        return model_path

    @staticmethod
    def convert_to_class_probabilities(model_result):
        """
        Converts the raw model results into a structured format (protobuf message).

        :param model_result: A list of dictionaries containing class names and probabilities.
        :return: A protobuf message (predict_pb2.ImageResults) with the results.
        """
        logger.debug("Converting model results to protobuf message")
        image_results = predict_pb2.ImageResults()

        # Iterate over the model results and populate the protobuf message.
        for item in model_result:
            class_prob = predict_pb2.ClassProbability(
                class_name=item["class_name"], probability=item["probability"]
            )

            image_results.results.append(class_prob)

        logger.debug("Successfully converted model results to protobuf message")

        return image_results

    @staticmethod
    def run_model(model, image):
        """
        Runs the YOLO model on the provided image and returns the results.

        :param model: A YOLO model instance.
        :param image: A PIL Image object to run predictions on.
        :return: A list of dictionaries containing class names and probabilities.
        """
        logger.debug("Running model on the image")
        model_result = model.predict(image, verbose=False)

        # If no probabilities are found, return an empty list.
        if model_result[0].probs is None:
            logger.warning("No probabilities found in model result")
            return []

        # Extract probabilities and class names from the model result.
        probs = model_result[0].probs.data
        class_names = model.names

        # Format the results into a list of dictionaries.
        result = [
            {"class_name": class_names[i], "probability": float(probs[i])}
            for i in range(len(probs))
        ]

        logger.debug("Model prediction completed successfully")

        return result
