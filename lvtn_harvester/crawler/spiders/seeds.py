import json
import os
from urllib.parse import urlparse

import scrapy


class SeedsSpider(scrapy.Spider):
    name = "seeds"
    allowed_domains = ["localhost"]
    start_urls = ["ftptree://localhost:9921"]

    def start_requests(self):
        return [
            scrapy.Request(
                "ftptree://localhost:9921/",
                meta={"ftp_user": "test", "ftp_password": "test", "dont_obey_robotstxt": True},
            )
        ]

    def parse(self, response):
        url = urlparse(response.url)

        if url.scheme == "ftptree":
            basepath = response.url
            files = json.loads(response.body)
            for f in files:
                if f["filetype"] == "d":
                    path = os.path.join(response.url, f["filename"])
                    request = scrapy.Request(path, meta=response.request.meta)
                    yield request
                if f["filetype"] == "-":
                    path = os.path.join(basepath, f["filename"])
                    path = path.replace("ftptree:", "ftp:")
                    request = scrapy.Request(path, meta=response.request.meta)
                    yield request
        elif url.scheme == "ftp":
            print(response.body)
