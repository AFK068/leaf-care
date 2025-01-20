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
    
    @staticmethod
    def convert_to_class_probabilities(model_result):
        image_results = predict_pb2.ImageResults()

        for item in model_result:
            class_prob = predict_pb2.ClassProbability(
                class_name=item["class_name"],
                probability=item["probability"]
            )
            image_results.results.append(class_prob)

        return image_results
        
    @staticmethod
    def run_model(model, image):
        model_result = model.predict(image, verbose=False)

        if model_result[0].probs is None:
            return []
        
        probs = model_result[0].probs.data
        class_names = model.names 
        
        result = [{"class_name": class_names[i], "probability": float(probs[i])} for i in range(len(probs))]

        return result