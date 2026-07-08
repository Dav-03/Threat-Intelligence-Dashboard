from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.models.models import IoC
from app.schemas.indicator import IndicatorResponse
from app.database import get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/indicators", tags=["indicators"])

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", response_model=list[IndicatorResponse])
def get_all_indicators(user: user_dependency, severity:str = None, type: str = None, db: Session = Depends(get_db)):
    
    query = db.query(IoC)
    if severity:
        query = query.filter(IoC.severity == severity)
    if type:
        query = query.filter(IoC.type == type)
    
    return query.all()


@router.get("/{id}", response_model=IndicatorResponse)
def get_single_indicator(user: user_dependency, id:int, db: Session = Depends(get_db)):
    indicator = (db.query(IoC)
                 .filter(IoC.id == id)
                 .first()
                 )
    if indicator is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    else:
        return indicator