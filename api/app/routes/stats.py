from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Annotated

from app.models.models import IoC
from app.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/summary")
def get_all_indicators(user: user_dependency, db: Session = Depends(get_db)):
    total_IoCs = db.query(IoC).count()

    severity_rows = (
        db.query(IoC.severity, func.count(IoC.id))
        .group_by(IoC.severity)
        .all()
    )

    type_rows = (
        db.query(IoC.type, func.count(IoC.id))
        .group_by(IoC.type)
        .all()
    )

    severity_breakdown = {
        severity: count
        for severity, count in severity_rows
    }

    type_breakdown = {
        type: count
        for type, count in type_rows
    }

    return {
        "total_iocs": total_IoCs,
        "severity_breakdown": severity_breakdown,
        "type_breakdown": type_breakdown
    }
    



    





