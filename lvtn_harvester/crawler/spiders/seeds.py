import scrapy


class SeedsSpider(scrapy.Spider):
    name = "seeds"
    allowed_domains = ["example.com"]
    start_urls = ["http://example.com/"]

    def parse(self, response):
        pass
