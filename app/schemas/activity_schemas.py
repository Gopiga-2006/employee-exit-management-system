"""Interview and clearance request models."""

from datetime import date

from pydantic import BaseModel, ConfigDict


class InterviewCreate(BaseModel):
    """Request body for an exit interview record."""
    interview_date: date
    feedback: str


class InterviewResponse(BaseModel):
    """Exit interview data returned by the API."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    request_id: int
    interview_date: date
    feedback: str


class ClearanceTaskCreate(BaseModel):
    """Request body for a clearance task."""
    assigned_to: int
    task: str


class ClearanceTaskUpdate(BaseModel):
    """Request body for updating a clearance task."""
    status: str


class ClearanceTaskResponse(BaseModel):
    """Clearance task data returned by the API."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    request_id: int
    assigned_to: int
    task: str
    status: str
