from sqlalchemy.orm import Session
from backend.models import question as question_model

def get_answer(db: Session, question_id: int) -> str:
    # Check the answer in the database and return
    question = db.query(question_model.Question).filter(question_model.Question.id == question_id).first()
    return question.answer if question else None
