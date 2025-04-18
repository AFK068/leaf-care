import os
import sys

# Add the root directory to the Python path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mlcore.grpc_core.servers import manager
from mlcore.logger import logger

if __name__ == "__main__":
    # Create an instance of the Server class.
    logger.info("Initializing gRPC server...")

    server = manager.Server()
    logger.info("gRPC server instance created successfully.")

    # Start the server.
    logger.info("Starting gRPC server...")
    server.run()
