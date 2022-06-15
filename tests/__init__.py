import unittest

import testing.postgresql
from lvtn1_utils import ProjectWorker

from lvtn_harvester.models import Base


class TestBaseDatabase(unittest.TestCase):
    """
    Base test class for when databases are being used.
    """

    postgresql_url_dict = {
        "port": 1234,
        "host": "127.0.0.1",
        "user": "postgres",
        "database": "test",
    }
    postgresql_url = "postgresql://{user}@{host}:{port}/{database}".format(
        user=postgresql_url_dict["user"],
        host=postgresql_url_dict["host"],
        port=postgresql_url_dict["port"],
        database=postgresql_url_dict["database"],
    )

    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql(**cls.postgresql_url_dict)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()


class TestCaseDatabase(TestBaseDatabase):
    def create_app(self):
        """Start the wsgi application"""

        a = ProjectWorker(
            "test",
            local_config={
                "SQLALCHEMY_URL": self.postgresql_url,
                "SQLALCHEMY_ECHO": False,
            },
        )
        return a

    def setUp(self):
        super().setUp()
        self.app = self.create_app()
        Base.metadata.bind = self.app._session.get_bind()
        Base.metadata.create_all()

    def tearDown(self):
        super().tearDown()
        Base.metadata.bind = self.app._session.get_bind()
        Base.metadata.drop_all(bind=self.app._engine)
