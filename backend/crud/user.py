from sqlalchemy.orm import Session
from sqlalchemy import select, DateTime, timedelta
from pydantic import BaseModel
from backend.models.user import User
from datetime import datetime, timedelta
from typing import Optional
from backend.db.utils import safe_commit
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

class UserSchema(BaseModel):
    id: int
    email: str

class UserUpdateSchema(BaseModel):
    email: Optional[str]
    username: Optional[str]
    token_used: Optional[int]
    quota_expiry: Optional[DateTime]


async def create_user(db: Session, user_data: UserSchema) -> User:
    # Get the current time
    now = datetime.now(datetime.timezone.utc)

    # Convert the user data to a User object
    user = User(
        id = user_data.id,
        email=user_data.email,
        username=user_data.username,
        created_at=now,
        quota_expiry=now + timedelta(days=30),  # Assuming a 30-day quota expiry
    )

    try:
        db.add(user)
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create user due to database error.'
        )
    return user


def get_user(db: Session, user_id: int) -> User:
    # Query the database for the user's information excluding created_at and id
    stmt = select(User.username, User.email, User.quota, User.quota_expiration, User.tokens_used).where(User.id == user_id)
    user = db.execute(stmt).scalars().first()
    if not user:
        raise Exception("User not found")

    return user


async def update_user(db: Session, user: User, user_update: UserUpdateSchema) -> User:
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    try:
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update user due to database error.'
        )
    return user


async def delete_user(db: Session, user_id: int) -> User:
    # Query the database for the user
    try:
        user = get_user(db, user_id)
        db.delete(user)
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete user due to database error.'
        )
    return user
