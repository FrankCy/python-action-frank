import logging
import random
import re
import time
import urllib.parse

import requests
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

class SinaVideoSpider(RedisSpider):
    name = 'sinaVideo'
    allowed_domains = ['sinavideo.cn']
    redis_key = 'sinavideo:start_urls-par'
    start_urls = ['https://weibo.com/']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    }

    def make_requests_from_url(self, url):
        # 使用模拟浏览器方式爬取
        default_target_url = 'http://www.baidu.com'
        return Request(default_target_url, callback=self.spider_chrome, headers=self.headers, dont_filter=True)

    def spider_chrome(self, response):
        try:
            video_key = '1301440200'
            # 处理从Redis获取
            spider_url = 'https://weibo.com/u/'+video_key+'?profile_type=1&is_video=1#_0/'
            # 创建持久化对象
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
            xpath_list = ['/html/body/div/div/div/div/div/div/div[2]/div/div/div[1]/div[4]/div/div/ul/li',
                          '/html/body/div[1]/div/div[4]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[3]/div[6]/div/ul/li']
            video_list = []
            for xpath in xpath_list:
                video_list = browser.find_elements_by_xpath(xpath)
                if video_list:
                    break

            if len(video_list) == 0:
                logger.error('video is null')
            else:
                print('视频总数：')
                print(len(video_list))
                for index, video in enumerate(video_list):
                    # 视频原地址
                    video_url_source = video.get_attribute('video-sources')
                    logger.info('video_url_source -----> ')
                    logger.info(video_url_source)
                    # 转码（两次）
                    video_source_decode_1 = urllib.parse.unquote(video_url_source)
                    video_source = urllib.parse.unquote(video_source_decode_1)
                    logger.info('video_source -----> ')
                    logger.info(video_source)

                    # 字符串处理
                    result = re.findall(".*http://(.*)http://.*", video_source)
                    # for x in result:
                    #     print('+++++++++++++++++++++++++')
                    #     print(x)
                    #     print('-------------------------')
                    if len(result) > 0:
                        target_url = result[0]
                        print('begin download!'+str(index))
                        # 下载视频
                        r = requests.get('http://'+target_url, stream=True)
                        with open(video_key+"_"+str(index)+'_video.mp4', "wb") as mp4:
                            for chunk in r.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    mp4.write(chunk)

            # spider集合
            logger.info('end spider sina video')

        except Exception as e:
            logger.error('爬取发生错误')
            logger.error(e)
            browser.quit()
        finally:
            browser.quit()

def get_proxy_url_one():
    proxy = requests.get(
        'http://tiensjtmm.v4.dailiyun.com/query.txt?key=NPAC507D5E&word=&count=1&rand=false&ltime=0&norepeat=true&detail=false').text
    logger.info('proxy one ---> ' + proxy)
    if proxy:
        return proxy.strip()

def chrome_pars():
    chrome_options = Options()
    # 无窗口模式
    # chrome_options.add_argument('--headless')
    # 禁止硬件加速，避免严重占用cpu
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 关闭安全策略
    chrome_options.add_argument("disable-web-security")
    # 禁止图片加载
    # chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    # 隐藏"Chrome正在受到自动软件的控制
    chrome_options.add_argument('disable-infobars')
    # 设置开发者模式启动，该模式下webdriver属性为正常值
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('User-Agent=' + random.choice(UserAgent_List))
    # proxy = '--proxy-server=http://' + get_proxy_url_one().replace('\n', '').replace('\r', '').replace(' ', '')
    # logger.info('chrome_pars proxy------------>' + proxy)
    # chrome_options.add_argument(proxy)
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