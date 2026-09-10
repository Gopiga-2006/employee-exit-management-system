"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.routes.approvals import router as approvals_router
from app.api.routes.auth import router as auth_router
from app.api.routes.exit_requests import router as exit_requests_router
from app.core.database import Base, engine
from app.models.entities import AuditLog, ClearanceTask, ExitApproval, ExitInterview, ExitRequest, User

app = FastAPI(title="Employee Exit Management System", version="1.0.0")

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(exit_requests_router)
app.include_router(approvals_router)


@app.get("/api/health")
def health_check() -> dict[str, object]:
    """Return the current service status."""
    return {"success": True, "data": {"status": "ok"}, "message": "Service is running"}
