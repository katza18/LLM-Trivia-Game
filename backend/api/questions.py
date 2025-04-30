from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from backend.quiz import generate_quiz, QuizRequest
from backend.crud import question
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/generate")
async def generate(quiz_params: QuizRequest, openai_client: AsyncOpenAI = Depends(), session: SessionContainer = Depends(verify_session())):
    """
    Endpoint to generate a quiz.
    TODO: Add SQL injection prevention and input validation.
    """
    # Check that this user has enough quota left

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
        correct_answer = await question.get_answer(session, qid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"correct_answer": correct_answer}
