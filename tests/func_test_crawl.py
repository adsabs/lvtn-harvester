import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import ENVVAR, get_project_settings


def run():
    os.environ[ENVVAR] = "lvtn_harvester.crawler.settings"
    process = CrawlerProcess(get_project_settings())

    # 'followall' is the name of one of the spiders of the project.
    process.crawl("seeds", domain="localhost")
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    run()
