import sys
import os
from pathlib import Path

# Ensure 'src' and 'src/crawler' are in the path so imports work correctly
# when running this script directly from the project root.
root_dir = Path(__file__).resolve().parent.parent
src_dir = root_dir / "src"
crawler_dir = src_dir / "crawler"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(crawler_dir) not in sys.path:
    sys.path.insert(0, str(crawler_dir))

from scrapy.crawler import CrawlerProcess

from core.loader import load_sources_from_excel
from crawler.spiders.generic_spider import GenericSourceSpider


def run():
    sources = load_sources_from_excel("config/sources.xlsx")

    # Convert Pydantic models to JSON-compatible dicts for Scrapy (converts HttpUrl to str)
    source_dicts = [s.model_dump(mode="json") for s in sources]

    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            "crawler.pipelines.RawTextStoragePipeline": 300,
        },
        "LOG_LEVEL": "INFO",
        "USER_AGENT": "RegulatoryMonitorBot/1.0",
        "DOWNLOAD_TIMEOUT": 20,
    })
    process.crawl(GenericSourceSpider, sources=source_dicts)
    process.start()


if __name__ == "__main__":
    run()
