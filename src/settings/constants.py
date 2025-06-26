from enum import Enum, member

from src.schemas.standard import ErrorResponse

class Document(str, Enum):
    TXT = "txt"
    CSV = "csv"
    MD = "md"
    JSON = "json"
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    XLS = "xls"
    XLSX = "xlsx"
class Image(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"

class SupportedFileType(Enum):
    DOCUMENT = member(Document)
    IMAGE = member(Image)

BAD_REQUEST = {"model": ErrorResponse, "description": "Bad Request"}
UNAUTHORIZED = {"model": ErrorResponse, "description": "Unauthorized"}
