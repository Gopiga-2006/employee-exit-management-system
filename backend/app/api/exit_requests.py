from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user, require_hr
from app.core.database import get_db
from app.models.exit_request import ExitRequest
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.exit_request import ApprovalRequest, ExitRequestCreate
from app.services.exit_service import approve_or_reject, create_exit_request, dashboard_counts, to_response

router = APIRouter(prefix="/api/v1/exit-requests", tags=["Exit Requests"])


@router.post("", status_code=status.HTTP_201_CREATED)
def submit_exit_request(payload: ExitRequestCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        item = create_exit_request(db, current_user, payload.reason, payload.requested_last_working_date, payload.comments)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return MessageResponse(success=True, data=to_response(item), message="Exit request submitted")


@router.get("/mine")
def get_my_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.scalars(select(ExitRequest).where(ExitRequest.employee_id == current_user.id).options(joinedload(ExitRequest.employee)).order_by(ExitRequest.id.desc())).unique().all()
    return MessageResponse(success=True, data=[to_response(item) for item in items], message="Requests loaded")


@router.get("")
def get_all_requests(_: User = Depends(require_hr), db: Session = Depends(get_db)):
    items = db.scalars(select(ExitRequest).options(joinedload(ExitRequest.employee)).order_by(ExitRequest.id.desc())).unique().all()
    return MessageResponse(success=True, data=[to_response(item) for item in items], message="Requests loaded")


@router.patch("/{request_id}/decision")
def decide_request(request_id: int, payload: ApprovalRequest, current_user: User = Depends(require_hr), db: Session = Depends(get_db)):
    item = db.scalar(select(ExitRequest).where(ExitRequest.id == request_id).options(joinedload(ExitRequest.employee)))
    if not item:
        raise HTTPException(status_code=404, detail="Exit request not found")
    try:
        item = approve_or_reject(db, item, current_user, payload.decision, payload.comment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return MessageResponse(success=True, data=to_response(item), message=f"Request {payload.decision}")


@router.get("/dashboard")
def dashboard(_: User = Depends(require_hr), db: Session = Depends(get_db)):
    return MessageResponse(success=True, data=dashboard_counts(db), message="Dashboard loaded")
