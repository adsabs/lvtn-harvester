# Design Notes

Initial notes from 05/04/22


Harvester District will be an inverted tree.

The central storage (either RDBMS or NOSQL - I'm leaning towards Yugabyte because we can easily shift to Postgres; actually - take that back, I lean towards PG with the option of switching to YB)

First phase:

    - table: providers
        - attrs:
            - id
            - URL
            - name
            - class
            - timestamps (created, updated, lastrun)
            - status

    - periodically cron (k8s) or scheduler (Spark/YARN) wakes up
        - and runs **harvesting**

            - harvester's task is to collect everything from a given domain (URL)
                - URL types:
                    - fs (filesystem)
                    - ftp
                    - http/https
                    - s3
                - class corresponds to rules that will be applied to harvesting:
                    - IOP, arxiv ... (those are known publishers)
                    - DFS (depth-first search)
                    - BFS (breath-first search)
                    - other types
            - harvester will be implemented with Python Scrapy
                - because it has a nice set of api/extensions
                - and it is simple (compared to Apache Nutch, js Apify SDK, and others)

            - results of the harvesting are saved into another table **records**
                - this table will grow to be **massive**
                - at first, the harvester will insert basic information:
                    - URL
                    - id
                    - basic metadata (if identified)
                        - title
                    - payload (a bytestream, package of data that later on will be read and processed - html page, section of XML record/batch, citation etc)


Second phase:

    - gradual enrichment occurs later on
    - different workers will wake up to try to get (download, extract) extra information
        - fulltext
        - images (thumbnails)
        - citations
        - etc....
    - they will save the results into the same table with appropriate prefix, e.g.
        - fulltext_payload
        - fulltext_status
        - fulltext_first_visit
        - fulltext_last_visit


Third Phase:

    - after we have implemented first two phases, we'll be learning to use Kafka
    - exposing results of enrichment through protobufs (to districts down the stream)


Technical Objectives:

- learn to use gRPC
    - every operation has to be envokable via simple call
    - and also we want API to update state of the storage (from outside)
- learn to use Scrapy
    - at least for https and filesystem
- plugin existing (or create a basic scaffolding) extractors
    - we can expect need for refactoring
    - our goal is to make it **simple** to modify/update/plug new/old extractors (this is for providers as well as for extractors; i.e. phases 1 and 2)


- use fingerprint to identify unique resource: https://github.com/scrapy/scrapy/blob/06f3d12c1208c380f9f1a16cb36ba2dfa3c244c5/scrapy/utils/request.py#L23

request.request_fingerprint(Request('https://www.google.com?q=fooz'))
Out[36]: '18c233a7ecb15e92f694db0954079aacd03a8217'

In [37]: request.request_fingerprint(Request('ftp://www.google.com?q=fooz'))
Out[37]: '51c41bf1f5fd118917cb3988b4ea3ee04729d96c'


- use this to test seeds (different versions of a publisher - but only few of those, becusa IngestParser should do the rest)

https://github.com/scrapy/scrapy/blob/06f3d12c1208c380f9f1a16cb36ba2dfa3c244c5/tests/test_linkextractors.py
