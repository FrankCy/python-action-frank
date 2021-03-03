# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 处理文件和编码类
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline

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

# 初始化图片保存地址
class ArticleImagePipeline(ImagesPipeline):
    # 重载item_completed方法
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item
