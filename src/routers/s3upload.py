from botocore.exceptions import ClientError

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from src.settings.config import AWS_REGION, S3_BUCKET, UPLOAD_DIR, boto3_session
from src.settings.constants import SupportedFileType

router = APIRouter(
    tags=["S3 Upload"],
)

SUPPORTED_FILE_TYPES = {
    ext.value
    for enum_cls in (
        SupportedFileType.DOCUMENT.value,
        SupportedFileType.IMAGE.value,
    )
    for ext in enum_cls
}


@router.get("/s3/presigned-url")
def get_presigned_url(
    filename: str = Query(..., description="Name of the file to upload"),
):
    # Validate filename length (without extension)
    if "." not in filename:
        raise HTTPException(status_code=400, detail="Filename must have an extension.")
    name_part, ext = filename.rsplit(".", 1)
    print(f"Filename: {filename}, Name part: {name_part}, Extension: {ext}")
    if len(name_part) < 3:
        raise HTTPException(status_code=400, detail="Filename must be more than three characters (excluding extension).")
    if ext.lower() not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}")

    s3_client = boto3_session.client(
        "s3", region_name=AWS_REGION,
    )
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": S3_BUCKET,
                "Key": f"{UPLOAD_DIR}/{filename}"
            },
            ExpiresIn=1100,
        )
        response = {"url": url, "filename": filename}
        return JSONResponse(
            status_code=200,
            content=response
        )

    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating presigned URL: {e.response['Error']['Message']}"
        )
