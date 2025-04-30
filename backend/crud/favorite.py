from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.favorite import Favorite
from backend.db.utils import safe_commit


async def create_favorite(db: Session, user_id: int) -> Favorite:
    # Get the current time
    now = datetime.now(datetime.timezone.utc)

    # Convert the user data to a User object
    favorite = Favorite(
        user_id=user_id,
        created_at=now,
    )

    try:
        db.add(favorite)
        await safe_commit(db, favorite)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create token log due to database error.'
        )
    return favorite


async def get_favorite(db: Session, favorite_id: int) -> Favorite:
    # Query the database for the favorite
    stmt = select(Favorite).where(Favorite.id == favorite_id)
    favorite = db.execute(stmt).scalars().first()
    if not favorite:
        raise Exception("Favorite not found")
    return favorite


async def delete_favorite(db: Session, favorite_id: int) -> Favorite:
    # Query the database for the token log
    try:
        favorite = await get_favorite(db, favorite_id)
        db.delete(favorite)
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete favorite due to database error.'
        )
