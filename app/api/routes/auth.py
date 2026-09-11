"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.entities import User
from app.schemas.schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import authenticate_user, create_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)) -> dict:
    """Register a new user."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload.name, payload.email, payload.password, payload.role)
    return {"success": True, "data": UserResponse.model_validate(user).model_dump(), "message": "User registered"}


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
