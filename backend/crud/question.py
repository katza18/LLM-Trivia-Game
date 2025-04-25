from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from backend.models.question import Question

class Question(BaseModel):
    id: int = None
    question: str
    answer: str
    type: str
    topic: str
    choices: list = None

class Quiz(BaseModel):
    questions: list[Question]


def get_answer(session: Session, question_id: int) -> str:
    # Check the answer in the database and return
    statement = select(Question.answer).where(Question.id == question_id)
    answer = session.execute(statement).scalars().one()
    return answer


def get_previous_questions(session: Session, topic: str) -> list[str]:
    # Get previous questions from the database
    statement = select(Question.question).where(Question.topic == topic)
    questions = session.execute(statement).scalars().all()
    return questions


def save_quiz(session: Session, quiz_data: Quiz) -> list[Question]:
    # Convert the questions to Question objects
    questions = [Question(**q.dict()) for q in quiz_data]

    # Add the questions to the session and commit
    session.add_all(questions)
    session.commit()

    # Refresh the session to get the IDs of the new questions
    session.refresh(question for question in questions)

    # Return the list of questions with their IDs
    return questions
