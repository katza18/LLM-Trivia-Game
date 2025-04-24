from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.crud import question as question_crud
from pydantic import BaseModel
from backend.quiz import Quiz
from openai import AsyncOpenAI

router = APIRouter(prefix="/quiz", tags=["quiz"])

class QuizRequest(BaseModel):
    topic: str
    qtype: str
    numq: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate")
async def generate_quiz(quiz_params: QuizRequest, client: AsyncOpenAI = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to generate a quiz.
    TODO: Add SQL injection prevention and input validation.
    """
    quiz = Quiz(quiz_params.topic, quiz_params.qtype)

    try:
        quiz_data = await quiz.generate_quiz(quiz_params.numq, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"quiz": quiz_data}


