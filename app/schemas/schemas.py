"""Request and response models for the REST API."""

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Request body for user registration."""
    name: str
    email: EmailStr
    password: str
    role: str = "employee"


class UserLogin(BaseModel):
    """Request body for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public user information returned by the API."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    """Successful login response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ExitRequestCreate(BaseModel):
    """Request body for creating an exit request."""
    reason: str
    last_working_day: date


class ExitRequestResponse(BaseModel):
    """Exit request data returned by the API."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    reason: str
    last_working_day: date
    status: str
