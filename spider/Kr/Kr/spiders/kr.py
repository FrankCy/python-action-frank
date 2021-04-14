import logging
import datetime

from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from spider.Common.items import KrNewsInformation

logger = logging.getLogger(__name__)

class KrSpider(RedisSpider):

    name = 'kr'
    allowed_domains = ['36kr.com']
    redis_key = '36k:start_urls-par'
    main_url = 'https://36kr.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    # 新闻列表（最新咨询）：https://36kr.com/newsflashes
    def make_requests_from_url(self, url):
        # 处理从Redis获取
        spider_url = 'https://36kr.com/newsflashes'
        return Request(spider_url, callback=self.spider_news, headers=self.headers, dont_filter=True)

    def spider_news(self, response):
        # 创建持久化对象
        kr_news_information = KrNewsInformation()
        # 创建匹配表达式
        xpath_list = ['//*[@id="app"]/div/div[1]/div[3]/div/div/div[1]/div[2]/div/div[1]/div']
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
                kr_news_information['title'] = news.xpath('div[2]/div/a/text()').get()
                # 创建时间（xx分钟前）
                kr_news_information['create_time_key'] = news.xpath('div[2]/div/div[1]/span[1]/text()').get()
                # 简要
                kr_news_information['brief'] = news.xpath('div[2]/div/div[2]/span/text()').get()
                # 正文链接
                kr_news_information['text_link'] = news.xpath('div[2]/div/div[1]/a/@href').get()
                # 爬取时间
                kr_news_information['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 持久化数据
                yield kr_news_information
