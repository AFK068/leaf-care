import logging
import grpc
from ultralytics import YOLO

from grpc_core.protos.predict import predict_pb2
from grpc_core.protos.predict import predict_pb2_grpc
from grpc_core.servers.handlers.predict import PredictHandler

class PredictService(predict_pb2_grpc.PredictorServicer):
    """
    PredictService class is a gRPC service that handles the prediction requests.
    """
    def Predict(self, request, context):
        plant_type = request.plant

        try:
            model = PredictHandler.get_or_create_model(plant_type)
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return predict_pb2.PredictorReply(result="Error")

        results = []
        for image_data in request.image_data:
            try:
                image = PredictHandler.bytes_to_image(image_data)
                model_result = PredictHandler.run_model(model, image)
                results.append(model_result)
                
            except Exception:
                logging.error(f"Prediction error: {image}")
                return predict_pb2.PredictorReply(result="Error")
        
        return predict_pb2.PredictorReply(result=results)