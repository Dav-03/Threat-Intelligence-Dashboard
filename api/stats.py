from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import IoC
from app.schemas.indicator import IndicatorResponse
from app.database import get_db

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/summary")
def get_all_indicators(db: Session = Depends(get_db)):
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
    



    





