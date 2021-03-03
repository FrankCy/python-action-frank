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
***ctrl+z 退出终端scrapy命令***

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
- 终端中通过命令测试爬虫逻辑
```shell
scrapy shell https://news.cnblogs.com/n/689294/
# 返回：response   <200 https://news.cnblogs.com/n/689294/> 代表成功了
# 然后直接执行选择器
response.css('#news_title a::text').extract_first('')
# 返回数据：'Google Workspace迎来远程办公新体验'
```
- 反爬方案1（解决js加载的问题）
```shell
# 添加requests库（用于解析js加载的数据）
pip3 install -i https://pypi.douban.com/simple requests
# 切换到python3
python3
# 引入requests
import requests
# 使用requests
reponse = requests.get("https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=689285")
# 检查是否获取到
reponse
# 显示<Response [200]>则获取到
# 查看ajax返回值
reponse.text
# 转换为json
import json
json.loads(reponse.text)
# 放入对象中，并获取某对象
j_data = json.loads(reponse.text)
j_data["TotalView"]
```