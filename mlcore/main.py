import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mlcore.grpc_core.servers import manager

if __name__ == '__main__':
    server = manager.Server()
    server.run()