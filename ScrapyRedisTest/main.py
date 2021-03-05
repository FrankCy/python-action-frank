# -*- coding: utf-8 -*-
__author__ = 'bobby'

# 主程序
from scrapy.cmdline import execute

import sys
import os

# 获取需执行的python目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 执行命令 scrapy crawl jobbole（jobbole是爬虫主文件）
execute(["scrapy", "crawl", "jobbole"])