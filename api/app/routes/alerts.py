from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.models import Alerts
from app.schemas.alert import AlertResponse, AlertCreate
from app.database import get_db

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[AlertResponse])
def get_all_feeds(country: str, city: str, db: Session = Depends(get_db)):
    
    query = db.query(Alerts)
    if country:
        query = query.filter(Alerts.country == country)
    if city:
        query = query.filter(Alerts.city == city)
    
    return query.all()

@router.post("/", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session=Depends(get_db)):
    new_alert = Alerts(
        ioc_id = alert.ioc_id,
        rule_name = alert.rule_name,
        description = alert.description,
        severity = alert.severity,
        timestamp = alert.timestamp
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert