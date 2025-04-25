from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from backend.quiz import generate_quiz, QuizRequest
from backend.crud import question

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/generate")
async def generate_quiz(quiz_params: QuizRequest, client: AsyncOpenAI = Depends()):
    """
    Endpoint to generate a quiz.
    TODO: Add SQL injection prevention and input validation.
    """
    try:
        quiz_data = await generate_quiz(quiz_params, client)
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
