from lvtn1_utils import ProjectWorker
from scrapy.extensions.feedexport import IFeedStorage
from zope.interface import implementer

from lvtn_harvester import models
from lvtn_harvester.crawler.items import ItemFruit, ItemSeed


class DatabaseWorker(ProjectWorker):
    def create_model(self, pipeline_item):
        if isinstance(pipeline_item, ItemFruit):
            return models.Fruit(**pipeline_item)
        elif isinstance(pipeline_item, ItemSeed):
            return models.Seed(**pipeline_item)
        else:
            raise Exception("Incompatible type passed")

    def add(self, orm_obj):
        return self.upsert_stmt(orm_obj)


@implementer(IFeedStorage)
class DBFeedStorage:
    def __init__(self, uri, *, feed_options=None):
        self.uri = uri
        self.db = None

    def open(self, spider):
        self.db = DatabaseWorker(
            "lvtn_harvester.crawler.storages.DBFeedStorage",
            local_config={"SQLALCHEMY_URL": self.uri},
        )
        return self.db

    def store(self, file):
        self.db.close_app()
        self.db = None
