import scrapy


class RawPageItem(scrapy.Item):
    """
    Represents raw scraped content from a source.

    This item is intentionally simple:
    - No analysis
    - No transformation
    - Just raw, normalized text
    """

    source_id = scrapy.Field()
    source_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    fetched_at = scrapy.Field()
