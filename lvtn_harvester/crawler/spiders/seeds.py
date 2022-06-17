import json
import os
from urllib.parse import urlparse

import scrapy

from lvtn_harvester.crawler.items import ItemFruit, ItemSeed


class SeedsSpider(scrapy.Spider):
    name = "adscrawler"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                "ftptree://localhost:9921/",
                meta={"ftp_user": "test", "ftp_password": "test", "dont_obey_robotstxt": True},
            )

    def parse(self, response):
        url = urlparse(response.url)

        if url.scheme == "ftptree":
            basepath = response.url
            files = json.loads(response.body)
            for f in files:
                if f["filetype"] == "d":
                    path = os.path.join(response.url, f["filename"])
                    request = scrapy.Request(path, meta=response.request.meta)
                    yield ItemSeed(request=request)
                if f["filetype"] == "-":
                    path = os.path.join(basepath, f["filename"])
                    path = path.replace("ftptree:", "ftp:")
                    request = scrapy.Request(path, meta=response.request.meta)
                    yield ItemFruit(request=request)

        else:
            # normally, this branch should not happen inside 'seed' parser
            # it means the spider has harvested contents from https/ftp/oai...
            # we'll return the appropriate Item
            yield ItemFruit(request=response.request, payload=response.body, response=response)
