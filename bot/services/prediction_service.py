from typing import Any

import grpc

from bot.logger import logger
from bot.protos.predict import predict_pb2
from bot.services.model_mapper import ModelMapper
from bot.services.predict_client import PredictClient
from bot.settings import settings


class PredictionService:
    """PredictionService class is responsible for handling predictions.

    It manages the interaction with the gRPC server for making predictions
    based on the detected objects in the images.
    """

    @staticmethod
    async def predict(
        data: dict[str, Any],
        detection_boxes: list[bytes],
    ) -> predict_pb2.PredictorReply:
        """Make a prediction based on the detected objects.

        Args:
            data (dict[str, Any]): Data containing the plant type.
            detection_boxes (list[bytes]): List of detected objects in bytes.

        Returns:
            predict_pb2.PredictorReply: The prediction result from the gRPC server.

        Raises:
            ValueError: If the plant type is invalid.
            RuntimeError: If there is an error during prediction.

        """
        def _raise_error(
            exception: Exception,
            message: str,
            error_type: type[Exception],
        ) -> None:
            logger.error(f"{message}. Original exception: {exception}")
            raise error_type(message) from exception

        try:
            plant_type = ModelMapper.get_plant_type(data["predict"])

            async with PredictClient(
                host=settings.GRPC_HOST_LOCAL,
                port=settings.GRPC_PORT,
            ) as client:
                result = await client.predict(
                    images_data=detection_boxes,
                    plant_type=plant_type,
                )

                if not result:
                    logger.warning("Empty response from gRPC server")
                    _raise_error(
                        None,
                        "Empty response from gRPC server",
                        RuntimeError,
                    )

                return result
        except ValueError as e:
            _raise_error(e, f"Invalid plant type: {e}", ValueError)
        except ConnectionError as e:
            _raise_error(e, f"Connection error: {e}", ConnectionError)
        except grpc.RpcError as e:
            _raise_error(e, f"gRPC error: {e.code()} - {e.details()}",grpc.RpcError)
        except Exception as e:
            _raise_error(e, f"Error during prediction: {e}", RuntimeError)
