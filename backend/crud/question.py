from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from backend.models.question import Question as QuestionModel
from backend.models.view import View as ViewModel

class QuestionSchema(BaseModel):
    id: int = None
    question: str
    answer: str
    type: str
    topic: str
    choices: list = None

class QuizSchema(BaseModel):
    questions: list[QuestionSchema]


def get_answer(db: Session, question_id: int) -> str:
    # Check the answer in the database and return
    statement = select(QuestionModel.answer).where(QuestionModel.id == question_id)
    answer = db.execute(statement).scalars().one()
    return answer


def get_previous_questions(db: Session, topic: str) -> list[str]:
    # Get previous questions from the database
    statement = select(QuestionModel.question).where(QuestionModel.topic == topic)
    questions = db.execute(statement).scalars().all()
    return questions

def get_user_previous_questions(db: Session, user_id: str, quantity: int):
    # Get previous questions for a specific user from the database sorted by created_at
    recent_views_statement = (
        select(ViewModel)
        .where(ViewModel.user_id == user_id)
        .order_by(ViewModel.last_viewed.desc())
        .limit(quantity))
    statement = (
        select(QuestionModel)
        .join(recent_views_statement.subquery(), QuestionModel.id == recent_views_statement.c.question_id)
    )
    questions = db.execute(statement).scalars().all()
    return questions

def save_quiz(db: Session, quiz_data: QuizSchema) -> list[QuestionSchema]:
    # Convert the questions to Question objects
    questions = [QuestionSchema(**q.dict()) for q in quiz_data]

    # Add the questions to the session and commit
    db.add_all(questions)
    db.commit()

    # Refresh the session to get the IDs of the new questions
    db.refresh(question for question in questions)

    # Return the list of questions with their IDs
    return questions
