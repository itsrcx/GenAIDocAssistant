import httpx

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from src.config import (
    API_STAGE_NAME,
    RESOURCE_PATH,
    COGNITO_DOMAIN,
    CLIENT_ID,
    CLIENT_SECRET,
    API_STAGE_URL
)
from src.routers.s3upload import router as s3upload

api_key_header = APIKeyHeader(name="Authorization")

def verify_jwt(token: str = Depends(api_key_header)):
    return token 

app = FastAPI(
    title=f"Python Apis",
    description="S3 presigned URL generator",
    version="0.1",
    root_path=f"/{API_STAGE_NAME}/{RESOURCE_PATH}",
    default_response_class=JSONResponse
)

v1_router = APIRouter(dependencies=[Depends(api_key_header)])
v1_router.include_router(s3upload)


app.include_router(v1_router)


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "Ok!"}

@app.get("/callback", include_in_schema=False)
async def cognito_callback(request: Request):
    code = request.query_params.get("code")
    REDIRECT_URI = f"{API_STAGE_URL}/{RESOURCE_PATH}/callback"

    if not code:
        return {"error": "Missing code"}

    token_url = f"{COGNITO_DOMAIN}/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    auth = (CLIENT_ID, CLIENT_SECRET)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers, auth=auth)
        tokens = response.json()

    return tokens
