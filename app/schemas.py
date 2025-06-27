from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime


class RoleEnum(str, Enum):
    manager = "manager"
    employee = "employee"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum
    manager_id: Optional[int] = None  # NEW


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: RoleEnum


class TokenData(BaseModel):
    id: Optional[int] = None


class SentimentEnum(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class FeedbackCreate(BaseModel):
    employee_id: int
    strengths: str
    areas_to_improve: str
    sentiment: SentimentEnum

class FeedbackUpdate(BaseModel):
    strengths: Optional[str] = None
    areas_to_improve: Optional[str] = None
    sentiment: Optional[SentimentEnum] = None

class FeedbackResponse(BaseModel):
    id: int
    manager_id: int
    employee_id: int
    strengths: str
    areas_to_improve: str
    sentiment: SentimentEnum
    acknowledged: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
