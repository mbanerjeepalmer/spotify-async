import subprocess
import shutil
import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_openapi_client():
    """
    Generates a Python client using openapi-python-client from unofficial 'fixed' OpenAPI specification.
    """
    try:
        command = [
            "uv",
            "run",
            "openapi-python-client",
            "generate",
            "--url",
            "https://raw.githubusercontent.com/APIs-guru/openapi-directory/main/APIs/spotify.com/1.0.0/openapi.yaml",
            "--meta",
            "uv",
            "--config",
            "openapi_config.yaml",
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)

        logger.debug(result.stdout)
        logger.info("Generated client")
        if result.stderr:
            logger.debug(result.stderr)
            logger.warning("Encountered errors during generation")

    except subprocess.CalledProcessError as e:
        print(f"Error generating client: {e}", file=sys.stderr)
        print("Command output:", e.stdout, file=sys.stderr)
        print("Command error:", e.stderr, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(
            "Error: 'uv' or 'openapi-python-client' not found. Make sure you have them installed.",
            file=sys.stderr,
        )
        sys.exit(1)


def copy_client():
    source = "generated-client/generated_client"
    target = "spotify_async"

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
