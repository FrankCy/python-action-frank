#!usr/bin/env python3
#-*- coding: UTF-8 -*-
# 爬取微博短视频
__auth__='lz'
import logging
import os
import re
import time
from urllib.parse import quote

import requests

logger = logging.getLogger(__name__)

base_url = 'https://m.weibo.cn/api/container/getIndex?'

header = {
    "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36",
    "X - Requested - With": "XMLHttpRequest",
    "Accept": "application/json, text/plain, */*",
}

def get_homeInfo(name):
    hurl = base_url + 'containerid=100103type%3D1%26q%3D'+ quote(name) +'&page_type=searchall'
    logger.info('hurl>' + hurl)
    try:
        hresp = requests.get(hurl, header)
        if(hresp.status_code==200):
            return hresp.json()
    except requests.ConnectionError as e:
        print("连接错误：" + e.args)

# 请求页面
def get_page(uid, luicode, lfid, q, containerid, sinceid):
    # 如果不是非常清楚字典和确定 url 编码，不要使用字典方式构造 url 参数，
    # 建议直接用字符串构造
    # 构造好后，一步步删去非必要参数
    # 确定好后，在把一些变化的参数，换成变量
    params = 'uid=2674747062&t=0&luicode=' + str(luicode) + '&lfid=' + str(lfid) + 'type=3&q='+ str(q) +'&t=0&type=uid&value=' + str(uid) + '&containerid=' + str(containerid)
    if(sinceid != 1):
        params += '&since_id=' + str(sinceid)
# 构建请求头，不然会被禁

    # 注意 quote 不要对 (= & 等) url编码，不然和原来的请求 url 不一致，会返回没有内容
    url = base_url + quote(params, "\/\:\=\&\?\#\+\!\$\,\;\'\@\(\)\*\[\]")
    try:
        resp = requests.get(url, header)
        if(resp.status_code==200):
            # 获取到的是 json 格式数据，直接用 json 方法解析并返回 json 对象
            return resp.json()
    except requests.ConnectionError as e:
        print("连接错误：" + e.args)

# 解析json数据
def parse_page_get_name2url(resp_json_obj):
    # 对着所在 key 右键，选择 copy property path
    # data.cards[""0""].card_group[""0""].mblog.page_info.media_info.stream_url
    name2url = []
    length = len(resp_json_obj['data']['cards'])
    for index in range(0, length):
        # 推荐这种取值方式，json 对象在 python 中其实是字典（dict）类型。
        # 此中方式取值方便，但假如键有误，则会抛异常
        try:
            page_info = resp_json_obj['data']['cards'][index]['mblog']['page_info']
        # 此中方式取值繁琐，但能避免抛异常
        # data = obj_json.get('data', None)
        # cards = data.get('cards', None)
        # card_groups = cards[0].get('card_group', None)
        # mblog = card_groups[0].get('mblog', None)
        # page_info = mblog['page_info']
            media_name = page_info['content2']
            media_url = page_info['media_info']['stream_url_hd']
        # 追加到数组中
            name2url.append({media_name: media_url})
        except:
            pass
            continue
    return name2url

# 新建文件保存目录
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

# 下载视频
def download_video(path, filename, url):
    resp = requests.get(url)
    time.sleep(3)
    with open(path + filename + '.mp4', 'wb') as file:
        file.write(resp.content)
        print(filename, '下载完成')

# 获取栏目containerid
def getContained(url):
    res = requests.get(url, header)
    res_json = res.json()
    # 处理个别博主无‘视频’栏目的情况，从‘微博’栏目获取
    try:
        container = res_json['data']['tabsInfo']['tabs'][2]['containerid']
    except:
        container = res_json['data']['tabsInfo']['tabs'][1]['containerid']
    return container

def last_files(file_dir):
    file_names = []
    for root, dirs, files in os.walk(file_dir):
        # print('root_dir:', root)  # 当前目录路径
        # print('sub_dirs:', dirs)  # 当前路径下所有子目录
        # print('files:', files)  # 当前路径下所有非目录子文件
        file_names.extend(files)
    return set(file_names)

def recursiveGetPage(uid, back, lfid, q, containerid, since_id, pageNo, count):
    obj_json = get_page(uid, back, lfid, q, containerid, since_id)
    since_id = obj_json['data']['cardlistInfo']['since_id']
    total = obj_json['data']['cardlistInfo']['total']
    pageSize = len(obj_json['data']['cards'])
    name2urls = parse_page_get_name2url(obj_json)
    if(len(name2urls) != pageSize):
        count += pageSize - len(name2urls)
    print('正在下载第 %d 页,当前页共 %d 条记录 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' %(pageNo, pageSize))
    for name2url in name2urls:
        for (name, url) in name2url.items():
            try:
                # 去掉特殊符号
                filename_temp = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", name)
                # # 从文件中读取上次下载的记录
                # with open(lastRecordPath, 'r') as f:
                #     data = f.read()
                # if(filename_temp == data):
                #     print('下载终止！')
                #     return;
                if filename_temp + '.mp4' in allfile:
                    print(filename_temp + '.mp4 文件已存在，下载终止！')
                    return
                download_video(path, filename_temp, url)
                count += 1
                if(count > total):
                    print('===================== %s 的全部微博视频已下载完成！保存目录： %s=====================' %(q, path))
                    return 'Done'

                print('已下载 {:.2f} %    第{}页 | {}/{}'.format(count/total * 100, pageNo, count, total))
                print('---------------------------------------------------------------')
            except:
                print('%s 下载失败！' %(name))
                pass
                continue
    print('第 %d 页下载完成 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' %(pageNo))
    pageNo += 1

    return recursiveGetPage(uid, back, lfid, q, containerid, since_id, pageNo, count)

if __name__ =='__main__':
    q = '澳大利亚'
    rootPath = '/Users/cy/Downloads/' + q + '/'
    path = rootPath + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '\\'
    mkdir(path)
    # 获取已下载文件的文件名并去重
    allfile = last_files(rootPath)

    hres = get_homeInfo(q)
    lfid = hres['data']['scheme'].split('lfid=')[1].split('_-_')[0]
    uid = hres['data']['cards'][0]['card_group'][0]['user']['id']
    profile_url = hres['data']['cards'][0]['card_group'][0]['user']['profile_url']
    back = profile_url.split('&luicode=')[1]

    url2 = base_url + 'uid={0}&luicode={1}&type=uid&value={2}'.format(uid, back, uid)
    containerid = getContained(url2)
    # 递归函数
    recursiveGetPage(uid, back, lfid, q, containerid, 1, 1, 0)

