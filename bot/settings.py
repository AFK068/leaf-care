import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GRPC_HOST_LOCAL: str = "nginx"
    GRPC_PORT: int = 443

    BOT_TOKEN: str = os.getenv("BOT_TOKEN")


load_dotenv()
settings = Settings()
