from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

QUESTIONS = [
    "Explain REST API design principles.",
    "What is database indexing?",
    "Explain async programming in Python."
]

class Answer(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "status":
        "AI Interview Copilot running"
    }


@app.get("/question")
def get_question():
    return {"question": QUESTIONS[0]}

@app.post("/score")
def score(data: Answer):

    answer = data.answer.lower()

    score = 0
    feedback = []

    keywords = [
        "api", "html", "stateless", "resource"
    ]

    for k in keywords:
        if k in answer:
            score += 25
    
    if score >= 75:
        feedback.append("Strong technical understanding")

    elif score >= 50:
        feedback.append("Good answer, but lacks depth")

    else:
        feedback.append("Needs improvement")
    
    return {
        "score": score,
        "feedback": feedback
    }
