from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    department_id: int | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
    full_name: str
