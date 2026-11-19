"""Single place where environment variables are read."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent

# Real environment variables win; the file only fills in what is missing.
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _required(name: str) -> str:
    value = (os.environ.get(name) or "").strip()
    if not value:
        raise RuntimeError(f"{name} is not set; add it to .env or the environment")
    return value


TRIMET_ID = _required("TRIMET_ID")