import asyncio
from typing import Optional

import grpc
from grpc import aio

from bot.logger import logger
from bot.protos.predict import predict_pb2, predict_pb2_grpc


class PredictClient:
    """A gRPC client for making predictions.

    This class provides methods to connect to a gRPC server, make predictions,
    and handle connection errors.
    """

    _instance: Optional["PredictClient"] = None
    _lock = asyncio.Lock()

    def __init__(
        self, host: str, port: str, channel: Optional[aio.Channel] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.channel = channel or aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = predict_pb2_grpc.PredictorStub(self.channel)
        self._connect_timeout = 10.0

    @classmethod
    async def get_instance(cls, host: str, port: str) -> "PredictClient":
        async with cls._lock:
            if cls._instance is None:
                cls._instance = cls(host, port)
                await cls._instance.connect()
            return cls._instance

    async def connect(self) -> None:
        if self.connected:
            return

        try:
            self.channel = aio.insecure_channel(f"{self.host}:{self.port}")
            self.stub = predict_pb2_grpc.PredictorStub(self.channel)

            # Wait for the connection to be established.
            # If the connection is not established within _connect_timeout second, raise an exception.
            await asyncio.wait_for(
                self.channel.channel_ready(),
                timeout=self._connect_timeout,
            )
            logger.info(f"Connected to gRPC server at {self.host}:{self.port}")
        except asyncio.TimeoutError:
            raise ConnectionError(f"Connection timeout to {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Connection error: {e!s}", exc_info=True)
            raise ConnectionError(f"Failed to connect: {e}")

    @property
    def connected(self) -> bool:
        return (
            self.channel is not None
            and self.channel.get_state() == grpc.ChannelConnectivity.READY
        )

    async def close(self) -> None:
        """Close the gRPC channel."""
        if self.channel:
            await self.channel.close()
            self.channel = None
            self.stub = None
            logger.info("Connection to gRPC server closed.")

    async def predict(
        self,
        images_data: list[bytes],
        plant_type: predict_pb2.Plant,
    ) -> predict_pb2.PredictorReply:
        """Make a prediction using the gRPC client.

        Args:
            images_data (list[bytes]): List of image data in bytes.
            plant_type (predict_pb2.Plant): The type of plant to predict.

        Returns:
            predict_pb2.PredictorReply: The prediction result from the gRPC server.

        Raises:
            ConnectionError: If there is a connection error.

        """
        if not self.connected:
            await self.connect()

        try:
            request = predict_pb2.PredictorRequest(
                image_data=images_data,
                plant=plant_type,
            )

            return await asyncio.wait_for(
                self.stub.Predict(request),
                timeout=self._connect_timeout,
            )
        except grpc.RpcError as e:
            error_mapping = {
                grpc.StatusCode.INVALID_ARGUMENT: "Invalid argument",
                grpc.StatusCode.DEADLINE_EXCEEDED: "Request timeout",
                grpc.StatusCode.UNAVAILABLE: "Service unavailable",
                grpc.StatusCode.INTERNAL: "Internal server error",
            }

            error_type = error_mapping.get(e.code(), "Unknown error")
            logger.error(f"{error_type}: {e.details()}")

            raise ConnectionError(f"gRPC error: {error_type}") from e

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()
