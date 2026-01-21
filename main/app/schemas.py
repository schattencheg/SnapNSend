from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Literal, Optional, List
from uuid import UUID


class RegisterRequest(BaseModel):
    user_name: str
    user_mail: EmailStr


class RegisterResponse(BaseModel):
    user_id: UUID
    status: Literal["pending", "done", "error"]
    error: Optional[str] = None


class SearchRequest(BaseModel):
    user: Optional[UUID] = None  # Optional user ID, None means no user specified
    n: int = Field(..., ge=1, le=50)
    mode: Literal["async", "sync"] = "async"  # async = return immediately,
    # sync = wait
    prompt: str = Field(..., min_length=1)


class SearchResponse(BaseModel):
    request_id: UUID
    status: Literal["pending", "done", "error"]
    images: Optional[List[str]] = None
    error: Optional[str] = None


class HealthCheck(BaseModel):
    status: str = "healthy"
    timestamp: datetime
