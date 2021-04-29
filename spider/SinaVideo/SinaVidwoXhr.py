# coding:utf-8
from bs4 import BeautifulSoup
import requests
import json
import pymongo
import logging
logger = logging.getLogger(__name__)

url = 'https://weibo.com/u/6926156236?profile_ftype=18&is_video=1#_0'


def dealData(url):
    web_data = requests.get(url)
    datas = json.loads(web_data.text)
    datas.keys()
    for data in datas['result']:
        logger.info('data >> ')
        logger.info(data)


def start():
    urls = [
        'http://www.guokr.com/apis/minisite/article.json?retrieve_type=by_subject&limit=20&offset={}&_=1508843461033'.format(
            str(i)) for i in range(20, 100, 20)]
    for url in urls:
        dealData(url)


def get_proxy_url_one():
    proxy = requests.get(
        'http://tiensjtmm.v4.dailiyun.com/query.txt?key=NPAC507D5E&word=&count=1&rand=false&ltime=0&norepeat=true&detail=false').text
    logger.info('proxy one ---> ' + proxy)
    if proxy:
        return proxy.strip()


if __name__ == '__main__':
    print(get_proxy_url_one())

