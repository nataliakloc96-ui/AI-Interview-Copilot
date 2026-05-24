from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

QUESTIONS = [
    {
        "question":
        "Explain REST API design principles.",
        "level":
        "junior"
    }
]


@app.get("/")
def home():
    return {
        "status":
        "AI Interview Copilot running"
    }


@app.get("/question")
def get_question():
    return QUESTIONS[0]