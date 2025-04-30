from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.token_log import TokenLog
from backend.db.utils import safe_commit
from typing import Optional

class TokenLogSchema(BaseModel):
    id: Optional[int]
    user_id: int
    tokens_used: int
    created_at: datetime

async def create_token_log(db: Session, token_log_data: TokenLogSchema) -> TokenLog:
    # Get the current time
    now = datetime.now(datetime.timezone.utc)

    # Convert the user data to a User object
    token_log = TokenLog(
        user_id=token_log_data.user_id,
        tokens_used=token_log_data.tokens_used,
        created_at=now,
    )

    try:
        db.add(token_log)
        await safe_commit(db, token_log)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create token log due to database error.'
        )
    return token_log


async def get_token_log(db: Session, token_id: int) -> TokenLog:
    # Query the database for the token log
    stmt = select(TokenLog).where(TokenLog.id == token_id)
    token_log = db.execute(stmt).scalars().first()
    if not token_log:
        raise Exception("Token log not found")
    return token_log


async def delete_token_log(db: Session, token_id: int) -> TokenLog:
    # Query the database for the token log
    try:
        token_log = await get_token_log(db, token_id)
        db.delete(token_log)
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete token log due to database error.'
        )
    return token_log
