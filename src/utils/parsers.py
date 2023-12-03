from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.utils.models import Analysis

def get_analysis_parser():
    return PydanticOutputParser(pydantic_object=Analysis)
