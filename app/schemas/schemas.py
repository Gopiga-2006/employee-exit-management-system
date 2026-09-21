"""Request and response models for the REST API."""

from datetime import date

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.security import validate_password


class UserCreate(BaseModel):
    """Request body for user registration."""
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "employee"

    @field_validator("password")
    @classmethod
    def validate_password_policy(cls, value: str) -> str:
        """Enforce the application password security policy."""
        return validate_password(value)


class AdminUserCreate(BaseModel):
    """Request body for administrator-managed user creation."""
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: Literal["employee", "hr", "admin"]

    @field_validator("password")
    @classmethod
    def validate_password_policy(cls, value: str) -> str:
        """Enforce the application password security policy."""
        return validate_password(value)


class UserLogin(BaseModel):
    """Request body for user login."""
    email: EmailStr
    password: str


class OtpVerify(BaseModel):
    """Request body for registration OTP verification."""
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class PasswordResetRequest(BaseModel):
    """Request body for starting password reset verification."""
    email: EmailStr


class PasswordResetVerify(BaseModel):
    """Request body for completing a password reset."""
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")
    new_password: str = Field(min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password_policy(cls, value: str) -> str:
        """Enforce the application password security policy."""
        return validate_password(value)


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


class ApprovalCreate(BaseModel):
    """Request body for an HR approval decision."""
    decision: str
    remarks: str | None = None


class ApprovalUpdate(BaseModel):
    """Request body for updating an HR approval decision."""
    decision: str
    remarks: str | None = None


class ApprovalResponse(BaseModel):
    """Approval data returned by the API."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    request_id: int
    approver_id: int
    decision: str
    remarks: str | None
