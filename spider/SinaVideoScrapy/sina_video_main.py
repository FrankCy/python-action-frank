import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scrapy.cmdline import execute
execute('scrapy crawl sinaVideo'.split())