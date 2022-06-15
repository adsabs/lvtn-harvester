import unittest

from lvtn_harvester import models
from tests import TestCaseDatabase


class TestName(TestCaseDatabase):
    def test_models(self):

        with self.app.db_session() as session:
            provider = models.Provider(name="arxiv", meta={"user": "test", "password": "test"})
            session.add(provider)
            session.add(models.Seed(url="foo", fingerprint="bar", provider=provider))

        with self.app.db_session() as session:
            provider = session.query(models.Provider).filter_by(name="arxiv").one()
            assert provider.name == "arxiv"
            assert len(provider.seeds) == 1
            assert provider.id == 1
            assert provider.seeds[0].url == "foo"

            seed = session.query(models.Seed).filter_by(fingerprint="bar").one()
            assert seed.id == provider.seeds[0].id
            assert seed == provider.seeds[0]

        with self.app.db_session() as session:
            seed = session.query(models.Seed).filter_by(fingerprint="bar").one()
            fruit = models.Fruit(url="https://foo.bar", seed=seed, fingerprint="foobaz")
            session.add(fruit)

        with self.app.db_session() as session:
            fruit = session.query(models.Fruit).filter_by(fingerprint="foobaz").one()
            assert fruit.id == 1
            assert fruit.seed.fingerprint == "bar"
            self.assertEqual(
                fruit.seed.provider.meta, '{"user": "test", "password": "test"}', "not there"
            )


if __name__ == "__main__":
    unittest.main()
