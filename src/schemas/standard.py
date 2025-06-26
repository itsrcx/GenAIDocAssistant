from typing import Any, Optional

from pydantic import BaseModel

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: Optional[Any] = None
    metadata: Optional[dict] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    error: Optional[str] = None
    details: Optional[Any] = None
    metadata: Optional[dict] = None
