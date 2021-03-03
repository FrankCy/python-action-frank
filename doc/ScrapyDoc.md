# Scrapy 
- - - 
一款简单易懂的异步IO爬虫框架！

## 国内镜像
- 通过python3 pip3 从国内镜像(https://pypi.douban.com/simple)中安装scrapy
pip3 install -i https://pypi.douban.com/simple scrapy
## 官方文档
- https://docs.scrapy.org/en/latest/
 
## 简介Scrapy
自身含有命令 scrapy，可创建工程，自动生成爬虫代码；</br>
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
## 实战
### 反爬方案1（解决js加载的问题）
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
### 增加爬虫命中率
```python
ROBOTSTXT_OBEY 改为 False
ROBOTSTXT_OBEY：模式是True，意思是遵循ROBOTSTXT_OBEY规则，部分链接不允许爬取
```
- Pipeliens的意思
```python
# 300：优先级，数字越小越先执行，设置管道ITEM_PIPELINES内容，可以做爬取过程编排使用
ITEM_PIPELINES = {
   'articlespider.pipelines.ArticlespiderPipeline': 300,
}
```
### 爬图片
```python
# 官方文档：https://docs.scrapy.org/en/latest/topics/media-pipeline.html
# pipelines中添加：
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
# 设置IMAGES_STORE = '/path/to/valid/dir'
IMAGES_STORE = '/path/to/valid/dir'
# 下载保存图片的工具包（图片处理包）
pip3 install -i https://pypi.douban.com/simple pillow   
# 异常排查问题:代表目标对象第一个字符有问题
ValueError: Missing scheme in request url: /
```
### 将item保存在文件内
```python
import codecs
import json

# 保存爬取的信息
class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        # 打开json(w代表爬取，如果有相同内容，不保存，a代表为追加）
        self.file = codecs.open("article.json", "w", encoding="utf-8")

    # 处理文件
    def process_item(self, item, spider):
        # 将数据转换成字符串
        # ensure_ascii:False
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入json文件内
        self.file.write(lines)
        return item

    # 文件关闭
    def spider_closed(self, spider):
        self.file.close()
```
### 定义表结构，并入库
```shell

```