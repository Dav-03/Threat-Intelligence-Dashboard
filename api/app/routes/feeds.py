from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.models import Feeds
from app.schemas.feed import FeedResponse
from app.database import get_db

router = APIRouter(prefix="/feeds", tags=["feeds"])

@router.get("/", response_model=list[FeedResponse])
def get_all_feeds(country:str = None, city: str = None, db: Session = Depends(get_db)):
    
    query = db.query(Feeds)
    if country:
        query = query.filter(Feeds.country == country)
    if city:
        query = query.filter(Feeds.city == city)
    
    return query.all()


@router.get("/{ip}", response_model=FeedResponse)
def get_single_feed(ip:str, db: Session = Depends(get_db)):
    feed = (db.query(Feeds)
                 .filter(Feeds.ip == ip)
                 .first()
                 )
    
    if feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")
    
    else:
        return feed