"""
Source Loader

WHY THIS FILE EXISTS:
---------------------
Source configuration is maintained in Excel by non-technical users.
This loader:
- Reads the Excel file
- Converts each row into a validated Source model
- Skips invalid rows safely
- Logs clear validation errors
- Produces a clean list of trusted Source objects

This ensures only valid, predictable data enters the scraping pipeline.
"""

from pathlib import Path
from typing import List

import pandas as pd
from pydantic import ValidationError

from models.source import Source
from utils.logger import get_logger

logger = get_logger(__name__)


def load_sources_from_excel(excel_path: str | Path) -> List[Source]:
    """
    Load and validate sources from an Excel file.

    Parameters
    ----------
    excel_path : str | Path
        Path to the Excel configuration file.

    Returns
    -------
    List[Source]
        List of validated and enabled Source objects.
    """

    excel_path = Path(excel_path)

    if not excel_path.exists():
        logger.error(f"Source Excel file not found: {excel_path}")
        raise FileNotFoundError(f"Source Excel file not found: {excel_path}")

    logger.info(f"Loading sources from Excel: {excel_path}")

    df = pd.read_excel(excel_path)

    if df.empty:
        logger.warning("Source Excel file is empty.")
        return []

    sources: List[Source] = []
    total_rows = len(df)

    for idx, row in df.iterrows():
        row_number = idx + 2  # Excel header offset

        try:
            source = Source(**row.to_dict())

            if not source.enabled:
                logger.info(
                    f"Skipping disabled source (row {row_number}): {source.source_name}"
                )
                continue

            sources.append(source)

        except ValidationError as ve:
            logger.error(
                f"Validation error in Excel row {row_number}: {ve.errors()}"
            )
        except Exception as ex:
            logger.exception(
                f"Unexpected error while processing Excel row {row_number}: {ex}"
            )

    logger.info(
        f"Loaded {len(sources)} valid sources out of {total_rows} rows."
    )

    return sources
