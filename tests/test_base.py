import http.server
import os
import pathlib
import unittest
import urllib.request

import httptest

_stubhome = os.path.join(pathlib.Path(__file__).parent.path, "stubdata")


class HTTPTestBase(unittest.TestCase):
    @httptest.Server(
        lambda *args: http.server.SimpleHTTPRequestHandler(*args, directory=_stubhome)
    )
    def get(self, filename, ts=httptest.NoServer()):
        with urllib.request.urlopen(ts.url() + filename) as f:
            yield f.read().decode("utf-8")


if __name__ == "__main__":
    unittest.main()
