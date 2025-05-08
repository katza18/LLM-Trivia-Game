from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from backend.quiz import generate_quiz, QuizRequest
from backend.crud import question
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from backend.db.database import SessionLocal

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/previous")
async def get_previous_questions(quantity: int = 10, session: SessionContainer = Depends(verify_session())):
    """
    Endpoint to get previously generated questions for a specific topic.

    Parameters:
    - number: The number of previous questions to fetch.
    """
    # Check that the user is logged in
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Get the user ID from the session
    user_id = session.get_user_id()

    try:
        db = SessionLocal()
        previous_questions = await question.get_user_previous_questions(db, user_id, quantity)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"previous_questions": previous_questions}


@router.post("/generate")
async def generate(quiz_params: QuizRequest, openai_client: AsyncOpenAI = Depends(), session: SessionContainer = Depends(verify_session())):
    """
    Endpoint to generate a quiz.
    TODO: Add SQL injection prevention and input validation.
    """
    # Check that this user has enough quota left
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        quiz_data = await generate_quiz(quiz_params, openai_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"quiz": quiz_data}


@router.get("/{qid}/answer")
async def get_answer(qid: int):
    """
    Endpoint to check the answer of a quiz question.
    """
    try:
        db = SessionLocal()
        correct_answer = await question.get_answer(db, qid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"correct_answer": correct_answer}
