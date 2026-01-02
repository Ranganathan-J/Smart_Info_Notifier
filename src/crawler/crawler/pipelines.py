from pathlib import Path
import re

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class RawTextStoragePipeline:
    """
    Stores raw scraped content into text files.

    Organizes files as: data/raw/<source_name>/<timestamp>.txt
    """

    def open_spider(self, spider):
        self.base_path = Path(settings.paths.raw_data)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        # Slugify source name for folder
        folder_name = re.sub(r'[^\w\s-]', '', item["source_name"]).strip().replace(" ", "_")
        source_dir = self.base_path / folder_name
        source_dir.mkdir(parents=True, exist_ok=True)

        # Windows doesn't allow ':' in filenames. Replace with '-' or similar.
        # Original: 2023-12-31T15:00:00.000000
        # New: 2023-12-31_15-00-00.txt
        timestamp = item['fetched_at'].replace(':', '-').replace('T', '_').split('.')[0]
        filename = f"{timestamp}.txt"
        file_path = source_dir / filename

        content = (
            f"URL: {item['url']}\n"
            f"TITLE: {item['title']}\n"
            f"FETCHED_AT: {item['fetched_at']}\n\n"
            f"{item['text']}"
        )

        file_path.write_text(content, encoding="utf-8")

        logger.info(f"Stored raw content: {file_path}")

        return item
