from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.quiz import Quiz
from backend.core.database import initialize_database, get_answer, get_favorites, add_to_favorites, remove_from_favorites, get_all_lists, get_user_statistics, authenticate_user, register_user, logout_user, reset_user_password
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

# Initialize the FastAPI app
app = FastAPI()

# Enable CORS for all routes
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class QuizRequest(BaseModel):
    topic: str
    qtype: str
    numq: int


class AuthRequest(BaseModel):
    username: str
    password: str


class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str


@app.post("/quiz/generate")
async def create_quiz(data: QuizRequest):
    """
    Endpoint to generate a quiz.
    TODO: Add SQL injection prevention and input validation.
    """
    quiz = Quiz(data.topic, data.qtype)

    try:
        quiz_data = await quiz.generate_quiz(data.numq, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"quiz": quiz_data}


@app.get("/questions/{qid}/answer")
def get_answer(qid:int):
    """
    Endpoint to check the answer of a quiz question.
    """
    try:
        correct_answer = get_answer(qid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"correct_answer": correct_answer}


@app.get("/questions/favorites")
def get_favorite_questions(type: str = "all", page: int = 1, size: int = 10):
    """
    Endpoint to get all favorite questions from the database.
    """
    try:
        favorite_questions = get_favorites()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"favorite_questions": favorite_questions}


@app.post("/questions/{qid}/favorite")
@app.delete("/questions/{qid}/favorite")
def favorite_question(qid: int, request: Request):
    """
    Endpoint to favorite or unfavorite a question.
    """
    action = request.method

    try:
        if action == "POST":
            add_to_favorites(qid)
        elif action == "DELETE":
            remove_from_favorites(qid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": f"Question {action.lower()}d successfully"}


@app.get("/lists")
def get_lists(user: str, page: int, page_size: int):
    """
    Endpoint to get all lists from the database.
    """
    try:
        lists = get_all_lists()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"lists": lists}


@app.get("/user/usage")
def get_user_usage(user: str):
    """
    Endpoint to get user usage statistics.
    """
    try:
        usage = get_user_statistics(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"usage": usage}


@app.post("/auth/login")
def login(data: AuthRequest):
    """
    Endpoint to log in a user.
    """
    try:
        user = authenticate_user(data.username, data.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"user": user}


@app.post("/auth/signup")
def signup(data: AuthRequest):
    """
    Endpoint to register a new user.
    """
    try:
        user = register_user(data.username, data.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"user": user}


@app.post("/auth/logout")
def logout(user: str):
    """
    Endpoint to log out a user.
    """
    try:
        logout_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User logged out successfully"}


@app.post("/auth/reset-password")
def reset_password(data: ResetPasswordRequest):
    """
    Endpoint to reset a user's password.
    """
    try:
        reset_user_password(data.username, data.new_password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Password reset successfully"}
