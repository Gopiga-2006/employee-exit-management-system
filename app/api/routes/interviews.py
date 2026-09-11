"""Exit interview endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.entities import ExitInterview, ExitRequest, User
from app.schemas.activity_schemas import InterviewCreate, InterviewResponse, InterviewUpdate

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
    interview = ExitInterview(
        request_id=request_id,
        interview_date=payload.interview_date,
        feedback=payload.feedback,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
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
    interview.interview_date = payload.interview_date
    interview.feedback = payload.feedback
    db.commit()
    db.refresh(interview)
    data = InterviewResponse.model_validate(interview).model_dump()
    return {"success": True, "data": data, "message": "Exit interview updated"}
