from pydantic import BaseModel
import datetime

class IndicatorBase(BaseModel):
    type: str        
    value: str
    severity: str
    source: str

class IndicatorCreate(IndicatorBase):
    pass

class IndicatorResponse(IndicatorBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True