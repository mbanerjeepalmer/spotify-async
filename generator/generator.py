from pathlib import Path
import shutil
import os
import logging
from openapi_python_client import generate
from openapi_python_client.cli import _process_config
from openapi_python_client.config import MetaType

logger = logging.getLogger(__name__)


def generate_openapi_client():
    """
    Generates a Python client using openapi-python-client from unofficial 'fixed' OpenAPI specification.
    """

    open_api_config = _process_config(
        path=Path("./generator/spotify-web-api.yaml"),
        config_path=Path("./openapi_config.yaml"),
        meta_type=MetaType.UV,
        overwrite=True,
        file_encoding="utf-8",
        output_path=None,
        url=None,
    )
    generate(config=open_api_config)
    logger.info("Generated client successfully.")


def copy_client():
    source = "generated-client/generated_client"
    target = "spotipython"

    if not os.path.exists(source):
        raise FileNotFoundError(f"Source directory not found: {source}")

    for item in os.listdir(source):
        if item == "__init__.py":
            logger.debug("Skipping __init__.py")
        source_item = os.path.join(source, item)
        target_item = os.path.join(target, item)

        if os.path.exists(target_item):
            if os.path.isdir(target_item):
                shutil.rmtree(target_item)
            else:
                os.remove(target_item)
            logger.debug(f"Removed {item}")

        if os.path.isdir(source_item):
            shutil.copytree(source_item, target_item)
            logger.debug(f"Copied {item}")
        else:
            shutil.copy2(source_item, target_item)
            logger.debug(f"Copied {item}")

    logger.info("Copied client")


if __name__ == "__main__":
    generate_openapi_client()
    copy_client()
