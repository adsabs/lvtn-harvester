# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.utils.request import request_fingerprint


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# TODO: turn those classes into protobufs


class ItemSeed(scrapy.Item):
    fingerprint = Field()
    url = Field()
    meta = Field()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", {})
        kwargs["fingerprint"] = request_fingerprint(request)
        kwargs["url"] = kwargs.get("url", request.url)
        kwargs["meta"] = kwargs.get("meta", request.meta)
        super().__init__(*args, **kwargs)


class ItemFruit(scrapy.Item):
    fingerprint = Field()
    url = Field()
    payload = Field()
    meta = Field()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        if request:
            kwargs["fingerprint"] = request_fingerprint(request)
            kwargs["url"] = kwargs.get("url", request.url)
            kwargs["meta"] = kwargs.get("meta", request.meta)
        _ = kwargs.pop("response", None)
        super().__init__(*args, **kwargs)
