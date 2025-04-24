from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from backend.models import question as question_model

class Question(BaseModel):
    question: str
    answer: str
    type: str
    topic: str
    choices: list = None

def get_answer(session: Session, question_id: int) -> str:
    # Check the answer in the database and return
    statement = select(question_model.Question.answer).where(question_model.Question.id == question_id)
    answer = session.execute(statement).scalars().all()
    return answer[0] if answer else None 

def get_previous_questions(db: Session, topic: str) -> list:
    # Get previous questions from the database
    questions = db.query(question_model.Question.question).filter(question_model.Question.topic == topic).all()
    return [question[0] for question in questions]

def save_question(session: Session, question_data: Question) -> None:
    # Save the question to the database
    question = question_model.Question(**question_data)
    session.add(question)
    session.commit()
    session.refresh(question)