import os
import unittest

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import ENVVAR, get_project_settings

from lvtn_harvester import models
from lvtn_harvester.crawler.items import ItemFruit, ItemSeed  # noqa
from tests import TestCaseDatabase


class TestFullCycle(TestCaseDatabase):
    def crawl(self, **kwargs):
        os.environ[ENVVAR] = "lvtn_harvester.crawler.settings"
        settings = get_project_settings()
        settings.setdict(
            {
                "FEEDS": {
                    self.app.config["SQLALCHEMY_URL"]: {"format": "database"},
                    # "item_classes": [ItemSeed, ItemFruit],
                }
            }
        )
        process = CrawlerProcess(settings)

        process.crawl("adscrawler", **kwargs)
        process.start()  # will block here until the crawling is finished

    def test(self):

        # initial run: collect first level seeds
        self.crawl(start_urls=["ftptree://localhost:9921"], allowed_domains=["localhost"])

        # verify stuff was harvested
        with self.app.db_session() as sess:
            sess.query(models.Seed).all()


if __name__ == "__main__":
    unittest.main()
