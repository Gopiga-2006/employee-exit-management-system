"""Clearance task endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.entities import ClearanceTask, ExitRequest, User
from app.schemas.activity_schemas import ClearanceTaskCreate, ClearanceTaskResponse, ClearanceTaskUpdate

router = APIRouter(prefix="/api/clearance-tasks", tags=["Clearance Tasks"])


@router.post("/{request_id}", status_code=status.HTTP_201_CREATED)
def create_task(
    request_id: int,
    payload: ClearanceTaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Create a clearance task for an exit request."""
    if not db.get(ExitRequest, request_id):
        raise HTTPException(status_code=404, detail="Exit request not found")
    if not db.get(User, payload.assigned_to):
        raise HTTPException(status_code=404, detail="Assigned user not found")
    task = ClearanceTask(request_id=request_id, assigned_to=payload.assigned_to, task=payload.task)
    db.add(task)
    db.commit()
    db.refresh(task)
    data = ClearanceTaskResponse.model_validate(task).model_dump()
    return {"success": True, "data": data, "message": "Clearance task created"}


@router.get("/{request_id}")
def list_tasks(
    request_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """List clearance tasks for an exit request."""
    tasks = db.query(ClearanceTask).filter(ClearanceTask.request_id == request_id).order_by(ClearanceTask.id).all()
    data = [ClearanceTaskResponse.model_validate(item).model_dump() for item in tasks]
    return {"success": True, "data": data, "message": "Clearance tasks retrieved"}


@router.put("/{task_id}")
def update_task(
    task_id: int,
    payload: ClearanceTaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> dict:
    """Update the status of a clearance task."""
    task = db.get(ClearanceTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Clearance task not found")
    if payload.status not in {"Pending", "Completed"}:
        raise HTTPException(status_code=400, detail="Invalid clearance status")
    task.status = payload.status
    db.commit()
    db.refresh(task)
    data = ClearanceTaskResponse.model_validate(task).model_dump()
    return {"success": True, "data": data, "message": "Clearance task updated"}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr", "admin")),
) -> None:
    """Delete a clearance task from an exit request."""
    task = db.get(ClearanceTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Clearance task not found")
    db.delete(task)
    db.commit()
