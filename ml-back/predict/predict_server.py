import io
import os
import logging
from concurrent import futures

import grpc
from PIL import Image
from ultralytics import YOLO

import proto

class Predictor(proto.predict_pb2_grpc.PredictorServicer):
    _model = {}

    @classmethod
    def get_or_create_model(cls, plant_type):
        if plant_type not in cls._model:
            path = cls.get_model_path(plant_type)
            cls._model[plant_type] = YOLO(path)

        return cls._model[plant_type]
    
    @staticmethod
    def get_model_path(plant_type):
        model_paths = {
            proto.predict_pb2.PLANT_CUCUMBER: os.path.join(os.path.dirname(__file__), 'models', 'cucumber_cls_model.pt'),
            proto.predict_pb2.PLANT_MELON: os.path.join(os.path.dirname(__file__), 'models', 'melons_cls_model.pt'),
            proto.predict_pb2.PLANT_PEPPER: os.path.join(os.path.dirname(__file__), 'models', 'pepper_cls_model.pt'),
            proto.predict_pb2.PLANT_SALAD: os.path.join(os.path.dirname(__file__), 'models', 'salad_cls_model.pt'),
            proto.predict_pb2.PLANT_STRAWBERRY: os.path.join(os.path.dirname(__file__), 'models', 'strawberrie_cls_model.pt'),
            proto.predict_pb2.PLANT_TOMATO: os.path.join(os.path.dirname(__file__), 'models', 'tomatoe_cls_model.pt'),
            proto.predict_pb2.PLANT_WATERMELON: os.path.join(os.path.dirname(__file__), 'models', 'watermelon_cls_model.pt'),
        }

        return model_paths[plant_type]
    
    @staticmethod
    def bytes_to_image(image_data):
        return Image.open(io.BytesIO(image_data))
    
    @staticmethod
    def run_model(model, image):
        model_result = model.predict(image)
        return str(model_result[0].masks)

    def Predict(self, request, context):
        plant_type = request.plant

        try:
            model = self.__class__.get_or_create_model(plant_type)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return proto.predict_pb2.PredictorReply(result="Error")

        results = []
        for image_data in request.image_data:
            try:
                image = self.bytes_to_image(image_data)
                model_result = self.run_model(model, image)
                results.append(model_result)
                
            except Exception:
                logging.error(f"Prediction error: {image}")
                return proto.predict_pb2.PredictorReply(result="Error")
        
        return proto.predict_pb2.PredictorReply(result=results)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto.predict_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()