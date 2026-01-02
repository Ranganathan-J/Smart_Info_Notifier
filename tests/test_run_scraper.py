import pytest
from unittest.mock import patch, MagicMock

import run_scraper
from models.source import Source


def mock_source():
    """
    Create a fake Source object without touching Excel.
    """
    return Source(
        source_id=1,
        source_name="RBI Circulars",
        url="https://www.rbi.org.in",
        source_type="REGULATOR",
        category="CIRCULAR",
        frequency="DAILY",
        priority="HIGH",
        enabled=True,
    )


@patch("run_scraper.CrawlerProcess")
@patch("run_scraper.load_sources_from_excel")
def test_run_scraper_happy_path(mock_load_sources, mock_crawler_process):
    """
    GIVEN valid sources from Excel
    WHEN run() is executed
    THEN Scrapy crawler should be started with correct arguments
    """

    # Arrange
    mock_load_sources.return_value = [mock_source()]

    mock_process = MagicMock()
    mock_crawler_process.return_value = mock_process

    # Act
    run_scraper.run()

    # Assert
    mock_load_sources.assert_called_once_with("config/sources.xlsx")

    mock_crawler_process.assert_called_once()

    mock_process.crawl.assert_called_once()
    args, kwargs = mock_process.crawl.call_args

    # Ensure spider is passed
    assert args[0].__name__ == "GenericSourceSpider"

    # Ensure sources are passed as list of dicts
    assert "sources" in kwargs
    assert isinstance(kwargs["sources"], list)
    assert isinstance(kwargs["sources"][0], dict)

    mock_process.start.assert_called_once()
