from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GRPC_HOST_LOCAL: str = '0.0.0.0'
    GRPC_PORT: int = 50052

settings = Settings()