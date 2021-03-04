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


# 初始化图片保存地址
class ArticleImagePipeline(ImagesPipeline):
    # 重载item_completed方法
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item
