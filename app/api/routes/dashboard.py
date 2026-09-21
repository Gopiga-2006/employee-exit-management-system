"""HR dashboard endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.entities import User
from app.services.dashboard_service import get_exit_dashboard_poc

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("hr")),
) -> dict[str, object]:
    """Return exit workflow summary information for HR users."""
    data = get_exit_dashboard_poc(db)
    return {"success": True, "data": data, "message": "Dashboard data retrieved"}
