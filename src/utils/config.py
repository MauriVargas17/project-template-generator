from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings


class GPTModel(str, Enum):
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"

class SentimentModel(str, Enum):
    sentiment = "ProsusAI/finbert"


class AnalysisModel(str, Enum):
    spacy = "en_core_web_sm"


class Settings(BaseSettings):
    api_name: str = "Mauricio's Financial Sentiment Analysis"
    log_level: str = "DEBUG"
    api_version: str = "0.0.1"
    openai_key: str
    models: dict[str, str] = {
        "GPT-3.5": GPTModel.gpt_3_5_turbo.value,
        "GPT-4": GPTModel.gpt_4.value,
        "Sentiment": SentimentModel.sentiment.value,
        "Analysis": AnalysisModel.spacy.value
    } 
    sentiment_categories: list[str] = ['very negative', 'negative', 'barely negative','neutral', 'barely positive', 'positive', 'very positive']
    sentiment_scale_length: int = 1
    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
