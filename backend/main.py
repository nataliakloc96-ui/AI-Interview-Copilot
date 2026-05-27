from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import bcrypt
from db import get_conn
import init_db
from jose import jwt
from datetime import datetime, timedelta
from ai_feedback import generate_feedback

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

class User(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str


SECRET_KEY = "super-secret-key-change-me"
ALGORITHM = "HS256"

def create_token(email: str):

    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(auth_header):

    token = auth_header.replace("Bearer ", "")

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload["sub"]


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
def score(data: Answer, authorization: str = Header(None)):

    try:

        email = decode_token(authorization)

        answer = data.answer.lower()

        ai = generate_feedback(points)

        keywords = [
            "api", "html", "stateless", "resource", "await", "async", "index", "database"
     ]

        

        points = 0

        for k in keywords:
            if k in answer:
                points += 15
    
        if points >= 75:
            ai = "Strong technical understanding"

        elif points >= 50:
            ai = "Good answer, but lacks depth"

        else:
            ai = "Needs improvement"

    
        history.append({
            "answer": data.answer,
            "score": points        
        })
    

        conn = get_conn()

        cur = conn.cursor()

        cur.execute("""
            INSERT INTO interview_history (email, score)
            VALUES (%s, %s)
        """, (email, points))
        conn.commit()
        cur.close()
        conn.close()

   
        return {
            "score": points,
            "ai_level": ai["level"],
            "feedback": ai["feedback"]
        }
    
    except Exception as e:
        return {"error": str(e)}


@app.post("/register")
def register(user: User):

    conn = get_conn()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(
        user.password[:72].encode(),
        bcrypt.gensalt()
    ).decode()

    cur.execute("""
        INSERT INTO users
        (email, password_hash)
        VALUES (%s, %s)
    """, (
        user.email,
        hashed
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "registered"}


@app.get("/history")
def get_history(authorization: str = Header(None)):

    try:
        if not authorization:
            return {"error": "missing token"}

        email = decode_token(authorization)
    
    except Exception as e:
        return {"error": str(e)}

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT score
        FROM interview_history
        WHERE email = %s
    """, (email,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "email": email,
        "history": rows
    }
    


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

@app.post("/login")
def login(data: Login):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM users WHERE email = %s",
        (data.email,)
    )

    user = cur.fetchone()

    if not user:
        return {"error": "invalid credentials"}
    
    stored_hash = user[0]

    if not bcrypt.checkpw(
        data.password.encode(),
        stored_hash.encode()
    ):
        return {"error": "invalid credentials"}
    
    token = create_token(data.email)

    return {"token": token}

@app.get("/leaderboard")
def leaderboard():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            email,
            ROUND(AVG(score),2) as avg_score,
            COUNT(*) as interviews
            FROM interview_history
            GROUP BY email
            ORDER BY avg_score DESC
            LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for r in rows:

        avg_score = 0

        if r[1] is not None:
            avg_score = round(float(r[1]), 2)
            
        result.append({
            "email": r[0],
            "avg_score": avg_score,
            "interviews": r[2]
        })

    return {
        "leaderboard": result
    }

