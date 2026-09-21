"""Administrator user-management endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.entities import User
from app.schemas.schemas import AdminUserCreate, UserResponse
from app.services.auth_service import create_user

router = APIRouter(prefix="/api/admin", tags=["Administration"])


@router.post("/users", status_code=201)
def create_managed_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles("admin")),
) -> dict:
    """Create an employee, HR or administrator account for an admin user."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, payload.name, payload.email, payload.password, payload.role)
    return {
        "success": True,
        "data": UserResponse.model_validate(user).model_dump(),
        "message": f"{payload.role.title()} account created",
    }
