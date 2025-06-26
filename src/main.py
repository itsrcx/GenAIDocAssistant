from mangum import Mangum
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from src.settings.config import (
    API_STAGE_NAME,
    RESOURCE_PATH,
    COGNITO_DOMAIN,
    CLIENT_ID,
    CLIENT_SECRET,
    API_STAGE_URL
)
from src.settings.security import api_key_header
from src.api.auth import router as auth_router


root_path = f"/{API_STAGE_NAME}/{RESOURCE_PATH}" if RESOURCE_PATH else f"/{API_STAGE_NAME}"

app = FastAPI(
    title="Gen AI Document Assistant",
    description="These are the endpoints for the Gen AI Document Assistant.",
    version="0.1",
    root_path=root_path,
    default_response_class=JSONResponse
)

app.include_router(auth_router, prefix=f"/api/auth")

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Gen AI Document Assistant API!"}

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "Ok!"}

# @app.get("/callback", include_in_schema=False)
# async def cognito_callback(request: Request):
#     code = request.query_params.get("code")
#     REDIRECT_URI = f"{API_STAGE_URL}/{RESOURCE_PATH}/callback"

#     if not code:
#         return {"error": "Missing code"}

#     token_url = f"{COGNITO_DOMAIN}/oauth2/token"
#     data = {
#         "grant_type": "authorization_code",
#         "client_id": CLIENT_ID,
#         "code": code,
#         "redirect_uri": REDIRECT_URI
#     }
#     auth = (CLIENT_ID, CLIENT_SECRET)
# headers = {"Content-Type": "application/x-www-form-urlencoded"}

# async with httpx.AsyncClient() as client:
#     response = await client.post(token_url, data=data, headers=headers, auth=auth)
#     tokens = response.json()

# return tokens

if RESOURCE_PATH:
    handler = Mangum(app, api_gateway_base_path=f"/{RESOURCE_PATH}")
else:
    handler = Mangum(app)
