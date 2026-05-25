from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QUESTIONS = {
    "junior": [
        "Explain REST API design principles.",
        "What is database indexing?"
    ],
    "mid": [
        "Explain async programming in Python.",
        "How does connection pooling work?"
    ],
    "senior": [
        "How would you design scalable microservices?",
        "Explain eventual consistency."
    ]
}

current_level = "junior"

history = []

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

    questions = QUESTIONS[current_level]

    current = len(history) % len(questions)
    return {
        "question": questions[current]
    }


@app.post("/score")
def score(data: Answer):

    answer = data.answer.lower()

    

    keywords = [
        "api", "html", "stateless", "resource", "await", "async", "index", "database"
    ]

    points = 0

    for k in keywords:
        if k in answer:
            points += 15
    
    if points >= 75:
        feedback = "Strong technical understanding"

    elif points >= 50:
        feedback = "Good answer, but lacks depth"

    else:
        feedback = "Needs improvement"

    
    history.append({
        "answer": data.answer,
        "score": points        
    })
    
    return {
        "score": points,
        "feedback": feedback
    }

@app.get("/history")
def get_history():
    return history

@app.get("/level/{level}")
def set_level(level: str):

    global current_level

    current_level = level

    history.clear()

    return {
        "level": current_level
    }

@app.get("/report")
def generate_report():

    pdf = "report.pdf"

    doc = SimpleDocTemplate(pdf)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            f"Interview Level: {current_level}",
            styles["Title"]
        )
    )

    total = 0

    for i,h in enumerate(history):
        total += h["score"]

        story.append(
            Paragraph(
                f"Attempt {i+1}: {h['score']}%",
                styles["Normal"]
            )
        )

    avg = 0 

    if history:
        avg = total / len(history)
    
    story.append(
        Paragraph(
            f"Average Score: {avg:.2f}%",
            styles["Heading2"]
        )
    )

    doc.build(story)

    return FileResponse(
        pdf,
        filename="interview_report.pdf"
    )
