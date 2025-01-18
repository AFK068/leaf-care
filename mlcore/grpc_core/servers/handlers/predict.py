from PIL import Image
import io
import os
from grpc_core.protos.predict import predict_pb2
from PIL import Image
from ultralytics import YOLO

class PredictHandler:
    """ 
    PredictHandler class is a handler for the prediction requests.
    """
    
    _models = {}

    @classmethod
    def get_or_create_model(cls, plant_type):
        if plant_type not in cls._models:
            path = cls.get_model_path(plant_type)
            cls._models[plant_type] = YOLO(path)

        return cls._models[plant_type]
    
    @staticmethod
    def bytes_to_image(image_data):
        return Image.open(io.BytesIO(image_data))
    
    @staticmethod
    def run_model(model, image):
        model_result = model.predict(image)
        return str(model_result[0].masks)
    
    @staticmethod
    def get_model_path(plant_type):
        BASE_MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, 'models'))

        model_paths = {
            predict_pb2.PLANT_CUCUMBER: 'cucumber_cls_model.pt',
            predict_pb2.PLANT_MELON: 'melons_cls_model.pt',
            predict_pb2.PLANT_PEPPER: 'pepper_cls_model.pt',
            predict_pb2.PLANT_SALAD: 'salad_cls_model.pt',
            predict_pb2.PLANT_STRAWBERRY: 'strawberrie_cls_model.pt',
            predict_pb2.PLANT_TOMATO: 'tomatoe_cls_model.pt',
            predict_pb2.PLANT_WATERMELON: 'watermelon_cls_model.pt',
        }

        return os.path.join(BASE_MODEL_PATH, model_paths[plant_type])