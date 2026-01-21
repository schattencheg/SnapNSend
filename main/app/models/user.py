from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    user_name: str
    user_mail: EmailStr
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
