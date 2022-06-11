import unittest

from scrapy import Request

from lvtn_harvester.crawler import items


class TestItems(unittest.TestCase):
    def test_assign(self):
        fruit = items.ItemFruit(
            request=Request("https://foo.com/query?foo=bar&hey=ho"), payload="foo bar"
        )
        self.assertEqual(
            {
                "fingerprint": "3aec26ce197dc0e9ea0d5f15cfc243098c181f51",
                "meta": {},
                "payload": "foo bar",
                "url": "https://foo.com/query?foo=bar&hey=ho",
            },
            fruit,
        )

        fruit = items.ItemFruit(
            request=Request("https://foo.com/query?hey=ho&foo=bar"), payload="foo bar"
        )
        self.assertEqual(
            {
                "fingerprint": "3aec26ce197dc0e9ea0d5f15cfc243098c181f51",
                "meta": {},
                "payload": "foo bar",
                "url": "https://foo.com/query?hey=ho&foo=bar",
            },
            fruit,
        )


if __name__ == "__main__":
    unittest.main()
