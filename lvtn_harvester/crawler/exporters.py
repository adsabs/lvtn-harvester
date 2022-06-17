from scrapy.exporters import BaseItemExporter


class DatabaseExporter(BaseItemExporter):
    """
    Example of the data storage layer; I'll likely abandon it
    when switching over to kafka and gRPC. It is here just to
    temporarily fill gaps

    """

    def __init__(self, file, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.worker = file
        self._session = None

    def start_exporting(self):
        self._session = self.worker._session()

    def finish_exporting(self):
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise (e)
        finally:
            self._session.close()

    def export_item(self, pipeline_item):
        self._session.execute(self.worker.add(self.worker.create_model(pipeline_item)))
