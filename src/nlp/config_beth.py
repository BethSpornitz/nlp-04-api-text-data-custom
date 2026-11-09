"""config_beth.py.

Modified by: Beth Spornitz
Date: 2026-11

Purpose

  Store configuration values for the custom JSONPlaceholder
  comments EVTL pipeline.

Analytical Questions

- What API endpoint provides the comments data?
- What HTTP request headers identify this application?
- Where should raw and processed comments data be stored?
"""

from pathlib import Path

# ============================================================
# API CONFIGURATION
# ============================================================

# Retrieve comments instead of posts.
API_URL: str = "https://jsonplaceholder.typicode.com/comments"

# Identify the custom application in the HTTP request.
HTTP_REQUEST_HEADERS: dict[str, str] = {
    "User-Agent": "nlp-module-4-beth-comments/1.0",
    "Accept": "application/json",
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

# Store custom outputs separately from the original example.
RAW_JSON_PATH: Path = RAW_PATH / "beth_comments_raw.json"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "beth_comments_processed.csv"
