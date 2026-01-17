"""
Data models for Authentication Service
"""
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User model"""
    user_id: str
    email: EmailStr
    password: str  # In production: Store hashed passwords only
    name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_001",
                "email": "demo@example.com",
                "password": "demo123",
                "name": "Demo User"
            }
        }


class LoginRequest(BaseModel):
    """Login request payload"""
    email: EmailStr
    password: str = Field(min_length=6)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "demo@example.com",
                "password": "demo123"
            }
        }


class LoginResponse(BaseModel):
    """Login response with JWT token"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    name: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "user_001",
                "email": "demo@example.com",
                "name": "Demo User"
            }
        }