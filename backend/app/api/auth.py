from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenData
from app.schemas.common import MessageResponse
from app.services.auth_service import authenticate_user, issue_token, register_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload.full_name, payload.email, payload.password, payload.department_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    data = TokenData(access_token=issue_token(user), user_id=user.id, role=user.role, full_name=user.full_name)
    return MessageResponse(success=True, data=data.model_dump(), message="Registration successful")


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    data = TokenData(access_token=issue_token(user), user_id=user.id, role=user.role, full_name=user.full_name)
    return MessageResponse(success=True, data=data.model_dump(), message="Login successful")
