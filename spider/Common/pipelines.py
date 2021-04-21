import logging

import pymongo
from pymysql import cursors
from twisted.enterprise import adbapi
from twisted.internet import defer, reactor

logger = logging.getLogger(__name__)


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



class MySqlPipeline(object):
    #函数初始化
    def __init__(self,db_pool):
        self.db_pool=db_pool

    @classmethod
    def from_settings(cls, crawler):
        """类方法，只加载一次，数据库初始化"""
        db_params = dict(
            host=crawler.settings['MYSQL_HOST'],
            user=crawler.settings['MYSQL_USER'],
            password=crawler.settings['MYSQL_PASSWORD'],
            port=crawler.settings['MYSQL_PORT'],
            database=crawler.settings['MYSQL_DBNAME'],
            charset=crawler.settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        # 返回一个pipeline对象
        return cls(db_pool)

    def process_item(self, item, spider):
        """
        数据处理
        :param item:
        :param spider:
        :return:
        """
        myItem = {}
        myItem["postId"] = item["PostId"]
        myItem["recruitPostId"] = item["RecruitPostId"]
        myItem["recruitPostName"] = item["RecruitPostName"]
        myItem["countryName"] = item["CountryName"]
        myItem["locationName"] = item["LocationName"]
        myItem["categoryName"] = item["CategoryName"]
        myItem["lastUpdateTime"] = item["LastUpdateTime"]
        logging.warning(myItem)
        # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
        asynItem = copy.deepcopy(myItem)

        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, asynItem)

        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, myItem, spider)
        return myItem

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO tencent (postId,recruitPostId,recruitPostName,countryName,locationName,categoryName,lastUpdateTime) " \
              "VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(
            item['postId'], item['recruitPostId'], item['recruitPostName'], item['countryName'], item['locationName'],
            item['categoryName'], item['lastUpdateTime'])
        # 执行sql语句
        cursor.execute(sql)
        # 错误函数

    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print("failure", failure)