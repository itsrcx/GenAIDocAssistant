import logging

from mangum import Mangum

from src.config import RESOURCE_PATH
from src.main import app


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

if not root_logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


handler = Mangum(app, api_gateway_base_path=f"/{RESOURCE_PATH}")
