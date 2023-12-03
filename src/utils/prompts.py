from enum import Enum
from pydantic import BaseModel

SENTIMENT_TEMPLATE = """
    You are a financial sentiment analyzer.
    You need to analyze a financial text in {language} language.
    The text you need to analyze is: {text}
    I want you to respond with the following points after analyzing the text:
    - POS tagging (Part of speech tagging for each token)
    - NER (Name entity recognition for each token)
    - Embedding: Even though in the format an embedding is required, provide an empty list instead.
    - Sentiment, including confidence and how positive or negative it is in a scale of
    'very negative', 'negative', 'barely negative','neutral', 'barely positive', 'positive', 'very positive'. Also
    provide a numerical value between -1 and 1 to reflect how positive or negative it is, with 1 being very positive and -1 being very negative.
    - Total time it took to analyze the text
    Also provide the name of the model used.
    Generate the response with the given format using the {format_instructions}.

"""


class Language(str, Enum):
    spanish = "spanish"
    english = "english"

class TextParams(BaseModel):
    text: str = "The market shows a bad trend as Martin showed in Alaska last week"
    language: Language = Language.english
