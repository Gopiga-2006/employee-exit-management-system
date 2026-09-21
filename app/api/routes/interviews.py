"""Exit interview endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.entities import ExitInterview, ExitRequest, User
from app.schemas.activity_schemas import (
    InterviewCreate,
    InterviewResponse,
    InterviewUpdate,
)
from app.services.activity_service import create_interview as create_interview_service, update_interview as update_interview_service

router = APIRouter(prefix="/api/interviews", tags=["Exit Interviews"])


@router.post("/{request_id}", status_code=status.HTTP_201_CREATED)
def create_interview(
    request_id: int,
    payload: InterviewCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Record an exit interview for a request."""
    request = db.get(ExitRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Exit request not found")
    if request.interview:
        raise HTTPException(status_code=400, detail="Interview already recorded")
    interview = create_interview_service(
        db, request_id, payload.interview_date, payload.feedback, user.id
    )
    data = InterviewResponse.model_validate(interview).model_dump()
    return {"success": True, "data": data, "message": "Exit interview recorded"}


@router.get("/{request_id}")
def get_interview(
    request_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Return the interview recorded for an exit request."""
    interview = db.query(ExitInterview).filter(ExitInterview.request_id == request_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Exit interview not found")
    data = InterviewResponse.model_validate(interview).model_dump()
    return {"success": True, "data": data, "message": "Exit interview retrieved"}


@router.put("/{request_id}")
def update_interview(
    request_id: int,
    payload: InterviewUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Update the interview recorded for an exit request."""
    interview = db.query(ExitInterview).filter(ExitInterview.request_id == request_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Exit interview not found")
    interview = update_interview_service(
        db, interview, payload.interview_date, payload.feedback, user.id
    )
    data = InterviewResponse.model_validate(interview).model_dump()
    return {"success": True, "data": data, "message": "Exit interview updated"}
