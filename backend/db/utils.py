from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

async def safe_commit(db: Session):
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Commit failed: {e}")
        raise
