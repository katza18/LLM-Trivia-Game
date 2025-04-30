from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.list_item import ListItem
from backend.db.utils import safe_commit
