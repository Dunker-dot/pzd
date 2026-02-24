from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "esl_demo.db"

SECRET_KEY = os.getenv("ESL_SECRET_KEY", "change-this-in-production")
SESSION_COOKIE = "esl_session"
