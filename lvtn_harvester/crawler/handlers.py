import json

from scrapy.core.downloader.handlers.ftp import FTPDownloadHandler
from scrapy.http import TextResponse
from twisted.protocols.ftp import FTPFileListProtocol


class FtpListingHandler(FTPDownloadHandler):
    """
    Handler that can fetch FTP listing - inspiration
    from: https://github.com/laserson/ftptree/blob/master/ftptree_crawler/handlers.py

    The handler must be activated in the settings

    DOWNLOAD_HANDLERS = {"ftptree": "crawler.handlers.FtpListingHandler"}
    """

    def gotClient(self, client, request, filepath):
        self.client = client
        protocol = FTPFileListProtocol()
        return client.list(filepath, protocol).addCallbacks(
            callback=self._build_response,
            callbackArgs=(request, protocol),
            errback=self._failed,
            errbackArgs=(request,),
        )

    def _build_response(self, result, request, protocol):
        self.result = result
        body = json.dumps(protocol.files)
        return TextResponse(url=request.url, status=200, body=body)
