"""pipeline_api_json_beth.py - Module 4 Custom Application.

Modified by: Beth Spornitz
Date: 2026-11

Purpose

  Orchestrate the custom JSONPlaceholder comments EVTL pipeline.
  Extract comments, validate their structure and field types,
  transform them into a Polars DataFrame, and save a CSV file.

Analytical Questions

- Can comments be retrieved from the JSONPlaceholder API?
- Do the comments contain the expected fields and data types?
- How can comment lengths be measured in characters and words?

Run from the root project folder with:

  uv run python -m nlp.pipeline_api_json_beth
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from datafun_toolkit.logger import get_logger, log_header, log_path

from nlp.config_beth import (
    API_URL,
    DATA_PATH,
    HTTP_REQUEST_HEADERS,
    PROCESSED_CSV_PATH,
    PROCESSED_PATH,
    RAW_JSON_PATH,
    RAW_PATH,
    ROOT_PATH,
)
from nlp.stage01_extract import run_extract
from nlp.stage02_validate_beth import run_validate
from nlp.stage03_transform_beth import run_transform
from nlp.stage04_load import run_load

# ============================================================
# Section 2. Configure Logging
# ============================================================

LOG: logging.Logger = get_logger("BethComments", level="DEBUG")

# ============================================================
# Section 3. Define Main Pipeline Function
# ============================================================


def main() -> None:
    """Run the custom JSONPlaceholder comments EVTL pipeline."""
    log_header(LOG, "MODULE 4: CUSTOM COMMENTS EVTL PIPELINE")
    LOG.info("START PIPELINE")

    RAW_PATH.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    log_path(LOG, "ROOT_PATH", ROOT_PATH)
    log_path(LOG, "DATA_PATH", DATA_PATH)
    log_path(LOG, "RAW_PATH", RAW_PATH)
    log_path(LOG, "PROCESSED_PATH", PROCESSED_PATH)

    # EXTRACT
    json_data = run_extract(
        source_api_url=API_URL,
        http_request_headers=HTTP_REQUEST_HEADERS,
        raw_json_path=RAW_JSON_PATH,
        LOG=LOG,
    )

    # VALIDATE
    validated_data = run_validate(
        json_data=json_data,
        LOG=LOG,
    )

    # TRANSFORM
    df = run_transform(
        json_data=validated_data,
        LOG=LOG,
    )

    # LOAD
    run_load(
        df=df,
        processed_csv_path=PROCESSED_CSV_PATH,
        LOG=LOG,
    )

    LOG.info("========================")
    LOG.info("Custom comments pipeline executed successfully!")
    LOG.info("========================")


# ============================================================
# Section 4. Run Main Function
# ============================================================

if __name__ == "__main__":
    main()
