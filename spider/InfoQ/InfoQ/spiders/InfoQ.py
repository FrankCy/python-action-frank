import logging
import datetime

from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from spider.Common.items import InfoQNewsInformation

logger = logging.getLogger(__name__)

class InfoQSpider(RedisSpider):
    name = 'infoQ'
    allowed_domains = ['infoq.cn']
    redis_key = 'infoq:start_urls-par'
    start_urls = ['http://infoq.cn/']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    # 首页：https://www.infoq.cn/
    def make_requests_from_url(self, url):
        # 处理从Redis获取
        spider_url = 'https://www.infoq.cn/'
        return Request(spider_url, callback=self.spider_news, headers=self.headers, dont_filter=True)

    def spider_news(self, response):
        if len(response.text) < 10000:
            logger.error('response < 10000, return')
        # 创建持久化对象
        info_q_news_information = InfoQNewsInformation()
        # 创建匹配表达式
        xpath_list = ['//*[@id="layout"]/div[2]/div[2]/div[1]/div[3]/div[3]/div/div[1]/div/div']
        # spider集合
        news_list = []
        for xpath in xpath_list:
            news_list = response.xpath(xpath)
            if news_list:
                break
        if not news_list:
            logger.error("url:" + response.url + "，检索无数据")
        else:
            print('len(news_list)')
            print(len(news_list))
            # 遍历集合插入数据
            for index, news in enumerate(news_list):
                # 标题
                info_q_news_information['title'] = news.xpath('div/div[2]/h6/a/text()').get()
                # 创建时间（xx分钟前）
                info_q_news_information['create_time_key'] = news.xpath('div/div[2]/div[1]/div/text()').get()
                # 简要
                info_q_news_information['brief'] = news.xpath('div/div[2]/p/text()').get()
                # 正文链接
                info_q_news_information['text_link'] = news.xpath('div/div[2]/h6/a/@href').get()
                # 爬取时间
                info_q_news_information['text_link'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 持久化数据
                yield info_q_news_information
