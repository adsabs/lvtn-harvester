from lvtn1_utils import ProjectWorker
from scrapy.exporters import BaseItemExporter

from lvtn_harvester import models
from lvtn_harvester.crawler.items import ItemFruit, ItemSeed


class DatabaseExporter(BaseItemExporter):
    """
    Example of the data storage layer; I'll likely abandon it
    when switching over to kafka and gRPC. It is here just to
    temporarily fill gaps

    """

    def __init__(self, file, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.file = file
        self.buffer = []

    def start_exporting(self):
        self.db = DatabaseWorker(
            "lvtn_harvester.exporters.DatabaseExporter",
            local_config={"SQLALCHEMY_URL": self.file},
        )

    def finish_exporting(self):
        if self.buffer:
            self._push()
        self.db.close_app()

    def export_item(self, item):
        self._add(item)

    def _add(self, item):
        self.buffer.append(self.db.create_item(item))

    def _push(self):
        with self.db.db_session() as session:
            for o in self._buffer:
                session.add(o)
            session.commit()
            self._buffer.clear()


class DatabaseWorker(ProjectWorker):
    def create_item(self, item):
        if isinstance(item, ItemFruit):
            return models.Fruit(**item)
        elif isinstance(item, ItemSeed):
            return models.Seed(**item)
        else:
            raise Exception("Incompatible type passed")
