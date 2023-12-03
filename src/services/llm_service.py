from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from src.utils.config import get_settings
from src.utils.prompts import SENTIMENT_TEMPLATE, TextParams
from src.utils.parsers import get_analysis_parser
from src.utils.models import Analysis

_SETTINGS = get_settings()


class TemplateLLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=_SETTINGS.models["GPT-4"], openai_api_key=_SETTINGS.openai_key
        )
        self.parser = get_analysis_parser()
        self.prompt_template = PromptTemplate(
            template=SENTIMENT_TEMPLATE,
            input_variables=["language", "text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def generate(self, params: TextParams) -> Analysis:
        _input = self.prompt_template.format(**params.dict())
        output = self.llm.predict(_input)
        return self.parser.parse(output)

    def generate_and_save(self, params: TextParams, out_file: str):
        output_obj = self.generate(params)
        with open(out_file, "w") as f:
            f.write(output_obj.json(ensure_ascii=False))
