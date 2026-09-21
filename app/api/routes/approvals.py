"""Exit approval endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.entities import ExitApproval, ExitRequest, User
from app.schemas.schemas import ApprovalCreate, ApprovalResponse, ApprovalUpdate
from app.services.activity_service import create_approval as create_approval_service, update_approval as update_approval_service

router = APIRouter(prefix="/api/approvals", tags=["Exit Approvals"])


@router.post("/{request_id}", status_code=status.HTTP_201_CREATED)
def create_approval(
    request_id: int,
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Record an HR decision for an exit request."""
    request = db.get(ExitRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Exit request not found")
    if payload.decision not in {"Approved", "Rejected"}:
        raise HTTPException(status_code=400, detail="Decision must be Approved or Rejected")
    approval = create_approval_service(
        db, request_id, user.id, payload.decision, payload.remarks
    )
    data = ApprovalResponse.model_validate(approval).model_dump()
    return {"success": True, "data": data, "message": "Exit request processed"}


@router.get("/{request_id}")
def list_approvals(
    request_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """List approval decisions recorded for an exit request."""
    if not db.get(ExitRequest, request_id):
        raise HTTPException(status_code=404, detail="Exit request not found")
    approvals = (
        db.query(ExitApproval)
        .filter(ExitApproval.request_id == request_id)
        .order_by(ExitApproval.id.desc())
        .all()
    )
    data = [ApprovalResponse.model_validate(item).model_dump() for item in approvals]
    return {"success": True, "data": data, "message": "Approvals retrieved"}


@router.put("/{approval_id}")
def update_approval(
    approval_id: int,
    payload: ApprovalUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Update an existing approval decision."""
    approval = db.get(ExitApproval, approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    if payload.decision not in {"Approved", "Rejected"}:
        raise HTTPException(status_code=400, detail="Decision must be Approved or Rejected")
    approval = update_approval_service(
        db, approval, payload.decision, payload.remarks, user.id
    )
    data = ApprovalResponse.model_validate(approval).model_dump()
    return {"success": True, "data": data, "message": "Approval updated"}
