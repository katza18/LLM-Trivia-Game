from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from backend.models.question import Question as QuestionModel

class QuestionSchema(BaseModel):
    id: int = None
    question: str
    answer: str
    type: str
    topic: str
    choices: list = None

class QuizSchema(BaseModel):
    questions: list[QuestionSchema]


def get_answer(session: Session, question_id: int) -> str:
    # Check the answer in the database and return
    statement = select(QuestionModel.answer).where(QuestionModel.id == question_id)
    answer = session.execute(statement).scalars().one()
    return answer


def get_previous_questions(session: Session, topic: str) -> list[str]:
    # Get previous questions from the database
    statement = select(QuestionModel.question).where(QuestionModel.topic == topic)
    questions = session.execute(statement).scalars().all()
    return questions


def save_quiz(session: Session, quiz_data: QuizSchema) -> list[QuestionSchema]:
    # Convert the questions to Question objects
    questions = [QuestionSchema(**q.dict()) for q in quiz_data]

    # Add the questions to the session and commit
    session.add_all(questions)
    session.commit()

    # Refresh the session to get the IDs of the new questions
    session.refresh(question for question in questions)

    # Return the list of questions with their IDs
    return questions
