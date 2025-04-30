from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.list import List
from backend.db.utils import safe_commit


async def create_list(db: Session, user_id: int, name: str) -> List:
    # Get the current time
    now = datetime.now(datetime.timezone.utc)

    # Convert the user data to a User object
    list = List(
        name=name,
        creator_id=user_id,
        created_at=now,
    )

    try:
        db.add(list)
        await safe_commit(db, list)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to create list due to database error.'
        )
    return list


async def get_list(db: Session, list_id: int) -> List:
    # Query the database for the token log
    stmt = select(List).where(List.id == list_id)
    list = db.execute(stmt).scalars().first()
    if not list:
        raise Exception("List not found")
    return list

async def update_list(db: Session, list: List, name: str) -> List:
    setattr(list, 'name', name)
    try:
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to update list due to database error.'
        )
    return list

async def delete_list(db: Session, list_id: int) -> List:
    # Query the database for the token log
    try:
        list = await get_list(db, list_id)
        db.delete(list)
        await safe_commit(db)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to delete list due to database error.'
        )
