# Scrapy 
- - - 
一款简单易懂的异步IO爬虫框架！

## 国内镜像
- 通过python3 pip3 从国内镜像(https://pypi.douban.com/simple)中安装scrapy
pip3 install -i https://pypi.douban.com/simple scrapy
## 官方文档
- https://docs.scrapy.org/en/latest/

## 简介Scrapy
自身含有命令 scrapy，可创建工程，自动生成爬虫代码；

- 创建项目 articlespider
```shell
scrapy startproject articlespider
```
- 生成爬取 news.cnblos.com的爬虫文件
```shell
scrapy genspider jobbole news.cnblogs.com
```
- 启动爬虫
```shell
# 启动 python-action-frank/articlespider/articlespider/spiders/jobbole.py
scrapy crawl jbobbole
```