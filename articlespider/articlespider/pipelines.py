# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# 处理文件和编码类
import codecs
import json

from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
# 异步数据库链接使用
from twisted.enterprise import adbapi

import MySQLdb

# 默认的pipeline
class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item

# 保存爬取的信息
class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        # 打开json
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    # 处理文件
    def process_item(self, item, spider):
        # 将数据转换成字符串
        # ensure_ascii:False
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入json文件内
        self.file.write(lines)
        return item

    # 文件关闭
    def spider_closed(self, spider):
        self.file.close()

# JSON解析器
class JsonExporterPipeline(object):
    def __init__(self):
        # 打开json
        self.file = open("articleexport.json", "wb")
        self.exporter =JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    # 处理文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        # 关闭exporter
        self.exporter.finish_exporting()
        # 关闭文件
        self.file.close()

# 保存数据至mysql
class MysqlPipeline(object):
    def __int__(self):
        # 初始化链接
        self.conn = MySQLdb.connect("127.0.0.1", "root", "root", "article_spider", charset="utf8mb4", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id, front_image_path, front_image_url, parise_nums, comment_nums, fav_nums, tags, content, create_date) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("front_image_path", ""))
        # 空列表转换字符串
        front_image = ",".join(item.get("front_image_url", []))
        params.append(front_image)
        params.append(item.get("parise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("create_date", "1970-07-01"))
        # 执行sql
        self.cursor.execute(insert_sql, tuple(params))
        # 提交
        self.conn.commit()

        return item

class MysqlTwistedPipeline(object):

    # 执行步骤2（通过重载方法初始化了dbpool
    def __int__(self, dbpool):
        self.dbpool = dbpool

    # 重载方法（执行步骤1）
    @classmethod
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        dbparms = dict(
            # 从settings文件中读取配置，不需要在上面写死
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    # 定义函数
    def process_item(self, item, spider):
        # 定义执行逻辑，逻辑为do_insert，传递参数item
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 定义异常回调，回调为handle_error
        query.addErrback(self.handle_error, item, spider)

    # 持久化出错后的错误处理
    def handle_error(self, failure, item, spider):
        print(failure)

    # 持久化数据
    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into jobbole_article(title, url, url_object_id, front_image_path, front_image_url, parise_nums, comment_nums, fav_nums, tags, content, create_date) 
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("front_image_path", ""))
        # 空列表转换字符串
        front_image = ",".join(item.get("front_image_url", []))
        params.append(front_image)
        params.append(item.get("parise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("create_date", "1970-07-01"))

        # 执行
        cursor.execute(insert_sql, tuple(params))


# 初始化图片保存地址
class ArticleImagePipeline(ImagesPipeline):
    # 重载item_completed方法
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item
