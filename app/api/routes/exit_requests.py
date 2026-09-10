"""Exit request endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import User
from app.schemas.schemas import ExitRequestCreate, ExitRequestResponse
from app.services.exit_service import create_exit_request, list_employee_requests

router = APIRouter(prefix="/api/exit-requests", tags=["Exit Requests"])


def get_demo_employee(db: Session) -> User:
    """Use the first employee for the initial MVP flow."""
    user = db.query(User).filter(User.role == "employee").order_by(User.id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Create an employee account first")
    return user


@router.post("", response_model=ExitRequestResponse)
def create_request(payload: ExitRequestCreate, db: Session = Depends(get_db)) -> ExitRequestResponse:
    """Create an exit request for the first employee account during the MVP stage."""
    user = get_demo_employee(db)
    return create_exit_request(db, user.id, payload.reason, payload.last_working_day)


@router.get("/mine", response_model=list[ExitRequestResponse])
def get_my_requests(db: Session = Depends(get_db)) -> list[ExitRequestResponse]:
    """List exit requests for the first employee account during the MVP stage."""
    user = get_demo_employee(db)
    return list_employee_requests(db, user.id)
