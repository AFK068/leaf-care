import io
import os
import logging
from concurrent import futures

import grpc
from PIL import Image
from ultralytics import YOLO

import proto

class Predictor(proto.predict_pb2_grpc.PredictorServicer):
    _model = None

    @classmethod
    def get_or_create_model(cls):
        if cls._model is None:
            path = os.path.join(os.path.dirname(__file__), 'models', 'model.pt')
            cls._model = YOLO(path)

        return cls._model

    def Predict(self, request, context):
        model = self.__class__.get_or_create_model()

        # Convert bytes to image.
        bytes = request.image_data
        image = Image.open(io.BytesIO(bytes))

        # Run model.
        try:
            model_result = model.predict(image)
        except Exception:
            return proto.predict_pb2.PredictorReply(result="Error")
        
        result = model_result[0].masks

        return proto.predict_pb2.PredictorReply(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proto.predict_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()