from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: ClassVar[str] = "redis://127.0.0.1:6379/0"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
