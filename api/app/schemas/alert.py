from pydantic import BaseModel
from datetime import datetime

class AlertBase(BaseModel):
    ioc_id: int
    rule_name: str
    description: str
    severity: str
    timestamp: datetime

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True