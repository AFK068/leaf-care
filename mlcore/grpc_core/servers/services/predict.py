import logging
import grpc

from mlcore.grpc_core.protos.predict import predict_pb2, predict_pb2_grpc
from mlcore.grpc_core.servers.handlers.predict import PredictHandler

class PredictService(predict_pb2_grpc.PredictorServicer):
    """
    PredictService class is a gRPC service that handles prediction requests.

    It uses the PredictHandler to load models, process images, and return results.
    """
    def Predict(self, request, context):
        """
        Handles the Predict RPC call. 

        It processes the request, runs the model, and returns the prediction results.

        :param request: The gRPC request containing image data and plant type.
        :param context: The gRPC context for handling errors and metadata.
        :return: A PredictorReply message containing the prediction results.
        """
        plant_type = request.plant

        try:
            model = PredictHandler.get_or_create_model(plant_type)
        except ValueError as e:
            # Log the error and set gRPC status code and details.
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid plant type: {e}")

            return predict_pb2.PredictorReply(result=[])

        results = []
        for image_data in request.image_data:
            try:
                # Convert raw image data to a PIL Image.
                image = PredictHandler.bytes_to_image(image_data)

                # Run the model on the image.
                model_result = PredictHandler.run_model(model, image)

                # Convert the model results to a protobuf message.
                image_results = PredictHandler.convert_to_class_probabilities(model_result)

                results.append(image_results)
                
            except Exception:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Error processing image: {e}")
                return predict_pb2.PredictorReply(result=[])
        
        return predict_pb2.PredictorReply(result=results)