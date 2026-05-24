from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

add.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

QUESTIONS = [
    {
        "question": "Explain REST API design principles.",
        "level": "junior"
    },
    {
        "question": "What is database indexing?",
        "level": "junior"
    },
    {
        "question": "Explain async programming in Python.",
        "level": "mid"
    }
]

@app.get("/")
def home():
    return {"status": "AI Interview Copilot running"}

@app.get("/questions")
def get_question():
    return QUESTIONS[0]