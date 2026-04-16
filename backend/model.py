from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from backend.parser import get_parser
from backend.prompts import get_prompt

load_dotenv()


def generate_questions(resume_text: str, jd: str):

    parser = get_parser()

    prompt_template = PromptTemplate(
    template=get_prompt(),
    input_variables=["resume", "jd"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # LCEL chain
    chain = prompt_template | llm 

    raw_output = chain.invoke({
        "resume": resume_text,
        "jd": jd
    })

    try:
        # Handle both AIMessage and string
        if hasattr(raw_output, "content"):
            text = raw_output.content
        else:
            text = raw_output

        parsed = parser.parse(text)

        return parsed.dict()

    except Exception as e:
        return {
            "error": str(e),
            "raw_output": str(raw_output)
        }