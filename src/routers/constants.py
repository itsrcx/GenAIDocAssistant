from enum import Enum, member

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
