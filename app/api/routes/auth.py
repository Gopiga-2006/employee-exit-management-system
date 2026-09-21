"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.entities import User
from app.schemas.schemas import (
    OtpVerify,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_user,
    request_signup_otp,
    verify_signup_otp,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup/request-otp")
def signup_request_otp(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> dict:
    """Send an OTP for new-user registration."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    request_signup_otp(db, payload.name, payload.email, payload.password, "employee")
    return {
        "success": True,
        "data": {"email": payload.email},
        "message": "OTP sent. Enter the OTP to complete registration.",
    }


@router.post("/signup/verify-otp", status_code=status.HTTP_201_CREATED)
def signup_verify_otp(
    payload: OtpVerify,
    db: Session = Depends(get_db),
) -> dict:
    """Verify the registration OTP and create the user account."""
    user = verify_signup_otp(db, payload.email, payload.otp)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    return {
        "success": True,
        "data": UserResponse.model_validate(user).model_dump(),
        "message": "User registered",
    }


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)) -> dict:
    """Register a new user after OTP verification."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    request_signup_otp(db, payload.name, payload.email, payload.password, payload.role)
    return {
        "success": True,
        "data": {"email": payload.email},
        "message": "OTP sent. Use the OTP verification endpoint to complete registration.",
    }


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)) -> dict:
    """Authenticate a user and issue a signed access token."""
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user.id, user.role)
    data = TokenResponse(access_token=token, user=user).model_dump()
    return {"success": True, "data": data, "message": "Login successful"}


@router.get("/me")
def get_profile(user: User = Depends(get_current_user)) -> dict:
    """Return the profile represented by the current access token."""
    data = UserResponse.model_validate(user).model_dump()
    return {"success": True, "data": data, "message": "Profile retrieved"}
