"""stage03_transform_beth.py.

Modified by: Beth Spornitz
Date: 2026-11

Source: validated JSON object
Sink: Polars DataFrame

Purpose

  Transform validated JSONPlaceholder comments into a
  structured DataFrame for text analysis.

Analytical Questions

- Which fields describe each comment?
- How can comments be organized into tabular data?
- How long are comments in characters and words?
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
from typing import Any

import polars as pl

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    json_data: list[dict[str, Any]],
    LOG: logging.Logger,
) -> pl.DataFrame:
    """Transform validated comments into a Polars DataFrame.

    Args:
        json_data (list[dict[str, Any]]): Validated comments data.
        LOG (logging.Logger): The logger instance.

    Returns:
        pl.DataFrame: The transformed comments dataset.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    records: list[dict[str, Any]] = []

    for record in json_data:
        records.append(
            {
                "post_id": record["postId"],
                "comment_id": record["id"],
                "name": record["name"],
                "email": record["email"],
                "body": record["body"],
            }
        )

    df: pl.DataFrame = pl.DataFrame(records)

    # ============================================================
    # DERIVED FIELDS
    # ============================================================

    # Calculate comment length in characters and words.
    df = df.with_columns(
        [
            pl.col("body").str.len_chars().alias("body_length"),
            pl.col("body")
            .str.split(" ")
            .list.eval(pl.element().filter(pl.element() != ""))
            .list.len()
            .alias("body_word_count"),
        ]
    )

    LOG.info("Transformation complete.")
    LOG.info(f"DataFrame preview:\n{df.head()}")
    LOG.info("Sink: Polars DataFrame created")

    return df
