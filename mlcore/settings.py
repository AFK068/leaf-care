from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class manages configuration settings for the application.
    """
    GRPC_HOST_LOCAL: str = '0.0.0.0'
    GRPC_PORT: int = 50052

# Create an instance of the Settings class.
settings = Settings()