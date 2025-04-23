from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.crud import question as question_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/quiz/generate")
def generate_quiz(db: Session = Depends(get_db)):
    return question_crud.generate_quiz(db=db)


