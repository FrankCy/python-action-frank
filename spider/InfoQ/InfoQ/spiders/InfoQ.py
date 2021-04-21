import datetime
import logging
import random
import time

from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
        # 使用模拟浏览器方式爬取
        default_target_url = 'http://www.baidu.com'
        return Request(default_target_url, callback=self.spider_news_chrome, headers=self.headers, dont_filter=True)

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

    def spider_news_chrome(self, response):
        try:

            # 处理从Redis获取
            spider_url = 'https://www.infoq.cn/'
            # 创建持久化对象
            info_q_news_information = InfoQNewsInformation()
            browser = webdriver.Chrome(chrome_options=chrome_pars())
            browser.get(spider_url)
            while True:
                if len(browser.page_source) > 10000:
                    break
                else:
                    print(len(browser.page_source))
                    browser.get(spider_url)
                    time.sleep(10)
                    browser.implicitly_wait(10)
            browser.implicitly_wait(5)
            # time.sleep(5)
            browser.maximize_window()
            browser.implicitly_wait(3)
            # time.sleep(5)

            # 创建匹配表达式
            xpath_list = ['//*[@id="layout"]/div[2]/div[2]/div[1]/div[3]/div[3]/div/div[1]/div']
            # spider集合
            news_list = []
            for xpath in xpath_list:
                news_list = browser.find_elements_by_xpath(xpath)
                if news_list:
                    break
            if not news_list:
                logger.error("url:" + response.url + "，检索无数据")
                logger.info(len(browser.page_source))
                browser.quit()
                return
            else:
                print('len(news_list)')
                print(len(news_list))
                # 遍历集合插入数据
                for index, news in enumerate(news_list):
                    # 标题
                    title = ''
                    try:
                        title = news.find_element_by_xpath('div/div[2]/h6').text
                    except Exception as e:
                        logger.error('title获取失败')
                    if not title:
                        title = ''
                    else:
                        info_q_news_information['title'] = news.find_element_by_xpath('div/div[2]/h6').text

                    # 创建时间（xx分钟前）
                    create_time = ''
                    try:
                        create_time = news.find_element_by_xpath('div/div[2]/div[1]/div').text
                    except Exception as e:
                        logger.error('时间获取失败')
                    if not create_time:
                        create_time = ''
                    else:
                        info_q_news_information['create_time_key'] = create_time

                    # 简要
                    brief = ''
                    try:
                        brief = news.find_element_by_xpath('div/div[2]/p').text
                    except Exception as e:
                        logger.error('简要获取失败')
                    if not brief:
                        brief = ''
                    else:
                        info_q_news_information['brief'] = brief

                    # 正文链接
                    text_link = ''
                    try:
                        text_link = news.find_element_by_xpath('div/div[2]/h6/a').get_attribute('href')
                    except Exception as e:
                        logger.error("正文链接获取失败")
                    if not text_link:
                        text_link = ''
                    else:
                        info_q_news_information['text_link'] = text_link

                    # 爬取时间
                    info_q_news_information['spider_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # 持久化数据
                    yield info_q_news_information
        except Exception as e:
            logger.error('爬取发生错误')
            logger.error(e)
            browser.quit()
        finally:
            browser.quit()



def chrome_pars():
    chrome_options = Options()
    # 无窗口模式
    chrome_options.add_argument('--headless')
    # 禁止硬件加速，避免严重占用cpu
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 关闭安全策略
    chrome_options.add_argument("disable-web-security")
    # 禁止图片加载
    chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    # 隐藏"Chrome正在受到自动软件的控制
    chrome_options.add_argument('disable-infobars')
    # 设置开发者模式启动，该模式下webdriver属性为正常值
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('User-Agent=' + random.choice(UserAgent_List))

    return chrome_options


UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"
]