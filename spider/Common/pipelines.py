import pymongo
from twisted.internet import defer, reactor


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_set):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.col = mongo_set

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_set=crawler.settings.get('MONGO_SET'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.mongodb = self.client[self.mongo_db]

    def spider_closed(self, spider, reason):
        self.client.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        out = defer.Deferred()
        reactor.callInThread(self._insert, item, out)
        yield out
        defer.returnValue(item)

    def _insert(self, item, out):
        if item.get("title", ""):
            fid = str(self.mongodb[self.col].find_one({"title": item.get("title", "")}))
            if not fid or fid == 'None':
                self.mongodb[self.col].insert(dict(item))
        reactor.callFromThread(out.callback, item)




