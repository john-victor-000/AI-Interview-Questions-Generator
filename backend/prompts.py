def get_prompt():

    return """
You are an expert interviewer.

Generate interview questions based on resume and job description.

STRICT RULES:
- Output ONLY valid JSON
- No explanation
- No extra text

Resume:
{resume}

Job Description:
{jd}

{format_instructions}
"""