from pydantic import BaseModel


class MessageResponse(BaseModel):
    success: bool
    data: object | None = None
    message: str
