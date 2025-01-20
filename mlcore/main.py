from grpc_core.servers import manager

if __name__ == '__main__':
    server = manager.Server()
    server.run()