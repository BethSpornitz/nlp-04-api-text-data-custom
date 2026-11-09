"""stage02_validate_beth.py.

Modified by: Beth Spornitz
Date: 2026-11

Source: raw JSON object
Sink: validated JSON object

Purpose

  Inspect and validate JSONPlaceholder comments data.

Analytical Questions

- Is the JSON data a nonempty list of records?
- Does each comment contain the required fields?
- Do the fields have the expected data types?
- Is the data usable for transformation and analysis?
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
from typing import Any

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    json_data: Any,
    LOG: logging.Logger,
) -> list[dict]:
    """Inspect and validate JSONPlaceholder comments data."""
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT JSON STRUCTURE
    # ============================================================

    LOG.info("JSON STRUCTURE INSPECTION:")
    LOG.info(f"Top-level type: {type(json_data).__name__}")

    # Confirm the top-level JSON structure is usable.
    if not isinstance(json_data, list):
        raise TypeError("Expected JSON data to be a list of records.")

    if len(json_data) == 0:
        raise ValueError("Expected at least one comment record.")

    if not all(isinstance(record, dict) for record in json_data):
        raise TypeError("Expected each comment to be a dictionary.")

    first_record = json_data[0]

    LOG.info(f"Keys in first record: {list(first_record.keys())}")

    LOG.info("Field types:")
    for key, value in first_record.items():
        LOG.info(f"{key}: {type(value).__name__}")

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    # Expected fields and types for JSONPlaceholder comments.
    required_fields = {
        "postId": int,
        "id": int,
        "name": str,
        "email": str,
        "body": str,
    }

    for index, record in enumerate(json_data):
        for field, expected_type in required_fields.items():
            if field not in record:
                raise ValueError(f"Comment {index} is missing required field: {field}")

            if type(record[field]) is not expected_type:
                raise TypeError(
                    f"Comment {index}: {field} must be {expected_type.__name__}."
                )

    LOG.info(f"Validated {len(json_data)} comment records.")
    LOG.info("Validation passed.")
    LOG.info("Sink: validated JSON object")

    return json_data
