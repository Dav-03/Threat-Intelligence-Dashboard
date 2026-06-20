from pydantic import BaseModel
from datetime import datetime

class FeedBase(BaseModel):
    ip: str
    port: list[int]
    org: str
    country: str
    city: str
    hostname: list[str]
    data: str
    timestamp: datetime

class FeedCreate(FeedBase):
    pass

class FeedResponse(FeedBase):
    timestamp: datetime


    class Config:
        from_attributes = True
