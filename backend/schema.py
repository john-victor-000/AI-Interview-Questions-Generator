from pydantic import BaseModel
from typing import List

class InterviewQuestions(BaseModel):
    technical_questions: List[str]
    hr_questions: List[str]
    project_questions: List[str]