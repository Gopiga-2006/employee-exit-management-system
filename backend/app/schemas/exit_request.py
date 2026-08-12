from datetime import date, datetime

from pydantic import BaseModel, Field


class ExitRequestCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=200)
    requested_last_working_date: date
    comments: str | None = Field(default=None, max_length=1000)


class ExitRequestResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    reason: str
    requested_last_working_date: date
    comments: str | None
    status: str
    created_at: datetime


class ApprovalRequest(BaseModel):
    decision: str = Field(pattern="^(approved|rejected)$")
    comment: str | None = Field(default=None, max_length=1000)
