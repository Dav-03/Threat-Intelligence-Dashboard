from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="stats", tags=["stats"])

@router.get("/summary")
def stat_counter():
    return True