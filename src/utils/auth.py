from typing import Callable
from functools import wraps

from fastapi import status
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
import hmac, hashlib, base64

from src.settings.config import CLIENT_ID, CLIENT_SECRET
from src.docs.cognito import COGNITO_ERROR_MAP

def get_secret_hash(username: str) -> str:
    message = username + CLIENT_ID
    digest = hmac.new(
        key=CLIENT_SECRET.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode()

def handle_client_error(default_message: str, http_status: int = status.HTTP_400_BAD_REQUEST):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                mapped_status, mapped_message = COGNITO_ERROR_MAP.get(
                    error_code, 
                    (http_status, default_message)
                )

                return JSONResponse(
                    status_code=mapped_status,
                    content={
                        "status": "failed",
                        "message": mapped_message,
                        "error": error_code,
                        "details": e.response["Error"].get("Message", str(e)),
                    },
                )
        return wrapper
    return decorator
