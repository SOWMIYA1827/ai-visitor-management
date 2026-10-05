from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from ..models.user import UserType


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    user_type: UserType = UserType.farmer
    organization: Optional[str] = None
    phone_number: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    user_type: UserType
    organization: Optional[str] = None
    is_admin: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
