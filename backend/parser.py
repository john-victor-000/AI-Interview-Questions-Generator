from langchain_core.output_parsers import PydanticOutputParser
from backend.schema import InterviewQuestions

def get_parser():
    return PydanticOutputParser(
        pydantic_object=InterviewQuestions
    )