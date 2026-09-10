"""Exit request endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.core.database import get_db
from app.models.entities import ExitRequest, User
from app.schemas.schemas import ExitRequestCreate, ExitRequestResponse
from app.services.exit_service import create_exit_request, list_employee_requests

router = APIRouter(prefix="/api/exit-requests", tags=["Exit Requests"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_request(
    payload: ExitRequestCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("employee")),
) -> dict:
    """Create an exit request for the signed-in employee."""
    request = create_exit_request(db, user.id, payload.reason, payload.last_working_day)
    data = ExitRequestResponse.model_validate(request).model_dump()
    return {"success": True, "data": data, "message": "Exit request submitted"}


@router.get("/mine")
def get_my_requests(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    """List exit requests belonging to the signed-in user."""
    requests = list_employee_requests(db, user.id)
    data = [ExitRequestResponse.model_validate(item).model_dump() for item in requests]
    return {"success": True, "data": data, "message": "Exit requests retrieved"}


@router.get("/all")
def get_all_requests(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """List all exit requests for HR users."""
    requests = list(db.query(ExitRequest).order_by(ExitRequest.id.desc()).all())
    data = [ExitRequestResponse.model_validate(item).model_dump() for item in requests]
    return {"success": True, "data": data, "message": "Exit requests retrieved"}
