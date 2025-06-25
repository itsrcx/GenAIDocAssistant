import os

from dotenv import load_dotenv
import boto3.session

boto3_session = boto3.session.Session()

load_dotenv()

API_STAGE_NAME = os.getenv("API_STAGE_NAME", "dev")
RESOURCE_PATH = os.getenv("RESOURCE_PATH", "python-api")
API_STAGE_URL = os.getenv("API_STAGE_URL", f"https://l186m80th2.execute-api.ap-south-1.amazonaws.com/dev")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "ai-vanguard-poc3")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN", "https://ap-south-1m5znvnhtc.auth.ap-south-1.amazoncognito.com")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
