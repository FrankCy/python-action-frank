import logging

import redis
import requests
from scrapy.utils.project import get_project_settings

from items import CommonItem

logger = logging.getLogger(__name__)


def call_back(url):
    '''执行完成回调函数'''
    if url == 'FFF0':
        logger.info('callback url is FFF0, return callback')
        return
    if url is None:
        logger.error('callback_url is None!')
        return
    # 回调控制系统，表示爬虫执行结束
    try:
        result = requests.get(url)
        # 接口有正确的数据才读入，否则为空
        if result.status_code == 200:
            logger.info('callback success,url:'+url)
        else:
            logger.error('callback fail,url'+url)
    except Exception as e:
        logger.error(e)


def get_conn_redis():
    '''连接redis'''
    settings = get_project_settings()
    pool = redis.ConnectionPool(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'),
                                db=settings.get('REDIS_DB'), password='123456', decode_responses=True)
    conn = redis.StrictRedis(connection_pool=pool)
    return conn


def from_redis_get_data(url):
    '''处理从redis中取出的参数信息'''
    logger.info("spider running, %s", url)
    spval = url.split(",")
    flg = int(spval[0])
    common_item = CommonItem()
    common_item['taskId'] = spval[1]
    common_item['skuId'] = spval[2]
    common_item['websiteId'] = spval[3]
    common_item['siteId'] = spval[4]
    common_item['countries'] = spval[5]
    common_item['row'] = spval[6]
    common_item['callbackUrl'] = spval[7]
    common_item['dataType'] = spval[8]
    common_item['fatherId'] = spval[9]
    goods_detail_url = spval[10]
    return flg, goods_detail_url, common_item


def final_callback(response, common_item):
    '''解析成功后最后回调的函数'''
    flg = int(response.meta.get('flg'))
    if flg:
        callback_item = {"callback_type": "detail", "callbackUrl": common_item.get('callbackUrl')}
        return callback_item
    else:
        uuid_key = response.meta.get('uuid_key')
        goods_num = response.meta.get('goods_num')
        callback_item = {"callback_type": "search", "uuid_key": uuid_key, "goods_num": goods_num,
                         "callbackUrl": common_item.get('callbackUrl')}
        return callback_item


