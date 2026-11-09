from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class random_question (BaseModel):
    question: str = Field(description="the question to be generated")
    correct_answer: str = Field(description="the correct answer from the question generated")

class SetQuestions (BaseModel):
    questions: list[random_question]

client = genai.Client()

uploaded_file = client.files.upload(file="Intro-Principles-in-Creating-a-Mobile-App-Design.pdf")

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=[
        {"type": "document", "uri": uploaded_file.uri, "mime_type": uploaded_file.mime_type},
        {"type": "text", "text": "generate 10 questions based on the file, then provide the correct answer"}
    ],
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": SetQuestions.model_json_schema()
    }
)

question = SetQuestions.model_validate_json(interaction.output_text)

for i in question.questions:
    print(i.question)
    print(i.correct_answer)
    print()