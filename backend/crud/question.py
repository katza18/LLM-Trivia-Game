from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.models import question as question_model

class Question(BaseModel):
    question: str
    answer: str
    type: str
    topic: str
    choices: list = None

def get_answer(db: Session, question_id: int) -> str:
    # Check the answer in the database and return
    question = db.query(question_model.Question).filter(question_model.Question.id == question_id).first()
    return question.answer if question else None

def save_question(db: Session, question_data: Question) -> None:
    # Save the question to the database
    question = question_model.Question(**question_data)
    db.add(question)
    db.commit()
    db.refresh(question)