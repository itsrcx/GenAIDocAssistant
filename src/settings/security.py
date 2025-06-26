from fastapi import Depends
from fastapi.security import APIKeyHeader, HTTPBearer

bearer_auth = HTTPBearer()

api_key_header = APIKeyHeader(name="Authorization")

def verify_jwt(token: str = Depends(api_key_header)):
    return token
