from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.models import IoC
from app.schemas.indicator import IndicatorResponse
from app.database import get_db

router = APIRouter(prefix="/indicators", tags=["indicators"])

@router.get("/", response_model=list[IndicatorResponse])
def get_all_indicators(severity:str = None, type: str = None, db: Session = Depends(get_db)):
    
    query = db.query(IoC)
    if severity:
        query = query.filter(IoC.severity == severity)
    if type:
        query = query.filter(IoC.type == type)
    
    return query.all()


@router.get("/{id}", response_model=IndicatorResponse)
def get_single_indicator(id:int, db: Session = Depends(get_db)):
    indicator = (db.query(IoC)
                 .filter(IoC.id == id)
                 .first()
                 )
    
    if len(indicator) is None:
        raise HTTPException(status_code=404, detail="Indicator not found")
    
    else:
        return indicator