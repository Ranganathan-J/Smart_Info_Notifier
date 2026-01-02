"""
Pydantic model defining the schema for a regulatory source.

WHY THIS FILE EXISTS:
---------------------
Source configuration is managed via Excel by non-technical users.
This model validates and normalizes that input before it enters
the scraping and analysis pipeline.

Benefits:
- Prevents invalid URLs and enums from crashing the system
- Enforces a strict contract between business config and code
- Enables early, clear error reporting
- Makes the pipeline predictable and auditable
"""

from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class SourceType(str, Enum):
    """
    Defines the high-level type of source.

    REGULATOR:
        Official regulatory authority (RBI, SEBI)
    NEWS:
        Media or news source reporting on regulations
    """
    REGULATOR = "REGULATOR"
    NEWS = "NEWS"


class SourceCategory(str, Enum):
    """
    Defines the content category of the source.
    Used for filtering and analysis prioritization.
    """
    CIRCULAR = "CIRCULAR"
    PRESS = "PRESS"
    NEWS = "NEWS"


class SourcePriority(str, Enum):
    """
    Defines how important this source is.
    Priority is later used to decide:
    - Crawl frequency
    - Depth of analysis
    """
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Source(BaseModel):
    """
    Canonical representation of a single monitoring source.

    This object is created AFTER reading Excel and BEFORE
    any scraping or LLM processing begins.
    """

    model_config = ConfigDict(extra="forbid")

    source_id: int = Field(..., description="Unique identifier from Excel")
    source_name: str = Field(..., min_length=3)
    url: HttpUrl = Field(..., description="Target URL to scrape")
    source_type: SourceType
    category: SourceCategory
    frequency: str = Field(..., description="Execution frequency (DAILY/WEEKLY)")
    priority: SourcePriority
    enabled: bool = Field(default=True)
    notes: str | None = None

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, value: str) -> str:
        """
        Ensure frequency is within supported values.

        This prevents silent misconfigurations such as:
        'DALIY', 'EVERDAY', etc.
        """
        allowed = {"DAILY", "WEEKLY"}
        value = value.upper()

        if value not in allowed:
            raise ValueError(f"Invalid frequency '{value}'. Allowed: {allowed}")

        return value

    @field_validator("source_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        """
        Normalize source names for consistent directory and log usage.
        """
        return value.strip()

