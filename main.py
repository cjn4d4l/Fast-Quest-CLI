from google import genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json, os

load_dotenv()

class random_question (BaseModel):
    question: str = Field(description="the question to be generated")
    correct_answer: str = Field(description="the correct answer from the question generated")


client = genai.Client()

def add_question ():
    topic = input("Enter a Topic: ")
    print("Generating...")

    prompt = f"""
    Please generate a question about {topic}, and provide the correct answer to that question
    """

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": random_question.model_json_schema()
            },
        )
    except Exception:
        print("Something Went Wrong. Try Again Later")
        return None
    
    question = random_question.model_validate_json(interaction.output_text)
    return {
        "topic": topic,
        "question": question.question,
        "correct_answer": question.correct_answer
    }

question_file = "questions.json"

def display_questions ():

    with open(question_file, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except Exception:
            return []

def save_questions (question):
    with open(question_file, "w", encoding="utf-8") as file:
        json.dump(question, file, indent=4)

# def simulate_quiz (question):

questions = display_questions()

while True:
    print("=====AI-Powered CLI Question Generator=====")
    print("Options:")
    print("[1] Generate Question")
    print("[2] View Saved Questions")
    print("[3] Exit")
    try:
        user = int(input("> "))
    except Exception:
        os.system("cls")
        print("Invalid Input. Try Again")
        continue

    if user == 1:
        os.system("cls")
        response = add_question()
        if response is None:
            continue

        print("=====Generated Question=====")
        print(f"Question: {response['question']}")
        print(f"Correct Answer: {response['correct_answer']}")
        input("Enter to Continue...")

        questions.append({
            "topic": response['topic'],
            "question": response['question'],
            "correct_answer": response['correct_answer']
        })
        os.system("cls")
    elif user == 2:
        os.system("cls")
        if not questions:
            print("No Available Questions Saved Yet...")
        else:
            print("=====Saved Generated Questions=====")
            n = 1
            for item in questions:
                print(f"[{n}] Topic: {item['topic']}")
                print(f"\tQuestion: {item['question']}")
                print(f"\tAnswer: {item['correct_answer']}")
                n += 1
        input("Enter to Continue...")
        os.system("cls")
    elif user == 3:
        save_questions(questions)
        print("=====Exiting Application=====")
        break
    else:
        print("Invalid Option")