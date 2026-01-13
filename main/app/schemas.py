from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4


class RequestBase(BaseModel):
    customer_id: str
    items: List[dict]
    total_amount: float
    status: str = "pending"


class RequestCreate(RequestBase):
    pass


class RequestUpdate(BaseModel):
    status: Optional[str] = None
    items: Optional[List[dict]] = None
    total_amount: Optional[float] = None


class RequestResponse(RequestBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    status: str = "healthy"
    timestamp: datetime