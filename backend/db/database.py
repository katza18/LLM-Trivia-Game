from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = f'postgresql://{os.getenv('QUIZGEN_DB_USER')}:{os.getenv('QUIZGEN_DB_PASSWORD')}@{os.getenv('QUIZGEN_DB_URI')}'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
