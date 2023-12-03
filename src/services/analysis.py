from functools import cache
import time
import spacy
from src.utils.config import get_settings
from src.utils.models import Analysis
from src.services.sentiment import TemplateSentiment

SETTINGS = get_settings()

@cache
def get_analysis_service():
    return TemplateSentiment()

class TemplateAnalysis:
    def __init__(self):
        self.nlp = spacy.load(SETTINGS.models["Analysis"])

    def analyze(self, text: str) -> Analysis:
        initial_time = time.time()
        doc = self.nlp(text)
        pos_tagging = [(token.text, token.pos_)  for token in doc]
        ner = [(ent.text, ent.label_) for ent in doc.ents]
        embedding = doc.vector
        sentiment = get_analysis_service().analyze(text)
        final_time = time.time()
        return Analysis(
            pos_tagging=pos_tagging,
            ner=ner,
            embedding=embedding,
            sentiment=sentiment,
            total_time_ms=round((final_time - initial_time) * 1000, 2)
        )