from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, exit_requests, health
from app.core.database import Base, engine
from app.models import Approval, ClearanceTask, Department, ExitRequest, User


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Exit Management System API",
    version="0.1.0",
    description="Review-I MVP API for employee exit request and HR approval workflows.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(exit_requests.router)


@app.get("/")
def root():
    return {"success": True, "data": {"docs": "/docs", "health": "/api/health"}, "message": "Employee Exit Management System API"}
