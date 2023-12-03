from typing import List
from pydantic import BaseModel

class Status(BaseModel):
    status: str
    version: str
    models_hosted: List[str]

class Sentiment(BaseModel):
    confidence: str
    category: str
    value_in_range: float
    time_ms: float

class Analysis(BaseModel):
    pos_tagging: List[tuple[str, str]]
    ner: List[tuple[str, str]]
    embedding: List[float]
    sentiment: Sentiment
    total_time_ms: float
