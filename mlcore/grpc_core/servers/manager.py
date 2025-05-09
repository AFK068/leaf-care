import os
from concurrent import futures

import grpc

from mlcore.grpc_core.protos.predict import predict_pb2_grpc
from mlcore.grpc_core.servers.services.predict import PredictService
from mlcore.logger import logger


class Server:
    """Server class is a gRPC server manager.

    It initializes the gRPC server, registers services, and provides methods
    to start and stop the server.
    """

    def __init__(self) -> None:
        # Set the server address using settings.
        self.server_address = f"{os.getenv("GRPC_HOST_LOCAL")}:{os.getenv("GRPC_PORT")}"

        # Create a gRPC server with a thread pool executor.
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # Bind the server to the specified address.
        self.server.add_insecure_port(self.server_address)

        logger.info(f"gRPC server initialized and bound to {self.server_address}")

    def register(self) -> None:
        # Register the PredictService with the server.
        predict_pb2_grpc.add_PredictorServicer_to_server(PredictService(), self.server)

        logger.info("PredictService registered with the gRPC server")

    def run(self) -> None:
        # Register services before starting the server.
        self.register()

        # Start the server.
        self.server.start()

        logger.info("gRPC server started and is running...")

        # Keep the server running until termination.
        self.server.wait_for_termination()

        logger.info("gRPC server has been terminated")

    def stop(self) -> None:
        # Stop the server without waiting for ongoing requests to complete
        self.server.stop(grace=False)

        logger.info("gRPC server stopped")
