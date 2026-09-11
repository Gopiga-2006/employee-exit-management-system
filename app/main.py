"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.approvals import router as approvals_router
from app.api.routes.auth import router as auth_router
from app.api.routes.clearance import router as clearance_router
from app.api.routes.exit_requests import router as exit_requests_router
from app.api.routes.interviews import router as interviews_router
from app.core.database import Base, engine
from app.models.entities import AuditLog, ClearanceTask, ExitApproval, ExitInterview, ExitRequest, User

app = FastAPI(title="Employee Exit Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(exit_requests_router)
app.include_router(approvals_router)
app.include_router(interviews_router)
app.include_router(clearance_router)


@app.get("/api/health")
def health_check() -> dict[str, object]:
    """Return the current service status."""
    return {"success": True, "data": {"status": "ok"}, "message": "Service is running"}
