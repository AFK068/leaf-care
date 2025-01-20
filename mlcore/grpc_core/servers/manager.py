import os
from concurrent import futures

import grpc
from dotenv import load_dotenv

from settings import settings
from grpc_core.protos.predict import predict_pb2_grpc
from grpc_core.servers.services.predict import PredictService

class Server:
    """
    Server class is a gRPC server manager.

    The `register` method is responsible for registering the gRPC services with the server.
    """
    def __init__(self) -> None:
        # Load the environment variables.
        load_dotenv()
        self.server_address = f"{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}"

        # Create the gRPC server.
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.server.add_insecure_port(self.server_address)
    
    def register(self) -> None:
        # Register the services.
        predict_pb2_grpc.add_PredictorServicer_to_server(
            PredictService(), self.server
        )
    
    def run(self) -> None:
        # Start the server.
        self.register()
        
        self.server.start()
        self.server.wait_for_termination()


    def stop(self) -> None:
        # Stop the server.
        self.server.stop(grace=False)
    