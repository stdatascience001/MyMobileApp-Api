import re
from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator
from uuid import UUID

class UserCreate(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", v):
            raise ValueError('Password must contain at least 1 uppercase letter')
        if not re.search(r"[a-z]", v):
            raise ValueError('Password must contain at least 1 lowercase letter')
        if not re.search(r"\d", v):
            raise ValueError('Password must contain at least 1 number')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError('Password must contain at least 1 special character')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    uuid: UUID
    name: str | None
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefresh(BaseModel):
    refresh_token: str

from datetime import date

class TripBase(BaseModel):
    title: str
    destination: str
    start_date: date
    end_date: date
    preferences: list | dict | None = None

class TripCreate(TripBase):
    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v: date, info: ValidationInfo) -> date:
        # In Pydantic V2 we can access other fields from info.data
        start_date = info.data.get('start_date')
        if start_date and v < start_date:
            raise ValueError('End date must be after start date')
        return v
        
    @field_validator('destination')
    @classmethod
    def validate_destination(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Destination cannot be empty')
        return v

class TripUpdate(BaseModel):
    title: str | None = None
    destination: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    preferences: dict | None = None

class TripResponse(TripBase):
    uuid: UUID
    user_uuid: UUID
    itinerary_json: dict | None = None
    is_generated: bool | None = False

    class Config:
        from_attributes = True
