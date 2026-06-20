from pydantic import Basemodel
from datetime import datetime

class AlertBase(Basemodel):
    ioc_id: int
    rule_name: str
    description: str
    severity: str
    timestamp: str

class AlertCreate(AlertBase):
    pass

class FeedResponse(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True