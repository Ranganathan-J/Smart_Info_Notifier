import scrapy
from datetime import datetime

from crawler.items import RawPageItem


class GenericSourceSpider(scrapy.Spider):
    """
    Generic spider that scrapes content from a list of sources
    provided at runtime.

    WHY:
    ----
    - Excel controls what to crawl
    - Code stays stable
    - Easy to add/remove sources
    """

    name = "generic_source"

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "ROBOTSTXT_OBEY": True,
    }

    def __init__(self, sources: list[dict], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sources = sources

    def start_requests(self):
        for source in self.sources:
            yield scrapy.Request(
                url=source["url"],
                callback=self.parse,
                meta={"source": source},
            )

    def parse(self, response):
        source = response.meta["source"]

        # Basic extraction (robust for regulatory pages)
        title = response.xpath("//title/text()").get(default="").strip()

        paragraphs = response.xpath("//p//text()").getall()
        text = "\n".join(t.strip() for t in paragraphs if t.strip())

        yield RawPageItem(
            source_id=source["source_id"],
            source_name=source["source_name"],
            url=source["url"],
            title=title,
            text=text,
            fetched_at=datetime.utcnow().isoformat(),
        )
