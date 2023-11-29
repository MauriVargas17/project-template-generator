from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings


class GPTModel(str, Enum):
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"


class Settings(BaseSettings):
    service_name: str = "Projects Generator Service"
    service_version: str = "0.9.2"
    k_revision: str = "1.0.0"
    log_level: str = "DEBUG"
    openai_key: str = "123"
    model: GPTModel = GPTModel.gpt_3_5_turbo
    img_model: str = './models/efficientdet.tflite'

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
