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
```sql
- 定义一张表
CREATE TABLE `jobbole_article`  (
  `title` varchar(255) NOT NULL COMMENT '标题',
  `url` varchar(500) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_path` varchar(255) NULL,
  `front_image_url` varchar(255) NULL,
  `parise_nums` int(255) NOT NULL,
  `comment_nums` int(255) NULL,
  `fav_nums` int(255) NULL,
  `tags` varchar(255) NULL,
  `content` longtext NULL,
  `create_date` datetime(0) NULL,
  PRIMARY KEY (`url_object_id`)
);
```
- 安装mysql
```shell
pip3 install -i https://pypi.douban.com/simple mysqlclient
# 如果碰到以下错误
ERROR: Command errored out with exit status 1:
 command: /usr/local/opt/python@3.8/bin/python3.8 -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-install-rxftxc00/mysqlclient_b15417b1f5c24e84a0145fa2228c6009/setup.py'"'"'; __file__='"'"'/private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-install-rxftxc00/mysqlclient_b15417b1f5c24e84a0145fa2228c6009/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-pip-egg-info-nj3ln6ft
     cwd: /private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-install-rxftxc00/mysqlclient_b15417b1f5c24e84a0145fa2228c6009/
Complete output (10 lines):
/bin/sh: mysql_config: command not found
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-install-rxftxc00/mysqlclient_b15417b1f5c24e84a0145fa2228c6009/setup.py", line 17, in <module>
    metadata, options = get_config()
  File "/private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-install-rxftxc00/mysqlclient_b15417b1f5c24e84a0145fa2228c6009/setup_posix.py", line 47, in get_config
    libs = mysql_config("libs_r")
  File "/private/var/folders/40/xfwrqjw5483cwh43vjdcj9_40000gn/T/pip-install-rxftxc00/mysqlclient_b15417b1f5c24e84a0145fa2228c6009/setup_posix.py", line 29, in mysql_config
    raise EnvironmentError("%s not found" % (mysql_config.path,))
OSError: mysql_config not found
# 软链以下mysql_config，可以找到它（这个方法可以使安装mysqlclient顺利进行，但是在实际使用mysql又会出现别的问题，建议重新装mysql）
sudo ln -s /usr/local/mysql/bin/mysql_config /usr/local/bin/mysql_config
# 然后再执行
pip3 install -i https://pypi.douban.com/simple mysqlclient
```

- 将数据存入mysql
```python
# 保存数据至mysql
class MysqlPipeline(object):
    def __int__(self):
        # 初始化链接（定义全局常量）
        self.conn = MySQLdb.connect("127.0.0.1", "root", "root", "article_spider", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id, front_image_path, front_image_url, parise_nums, comment_nums, fav_nums, tags, content, create_date) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("front_image_path", ""))
        # 空列表转换字符串
        front_image = ",".join(item.get("front_image_url", []))
        params.append(front_image)
        params.append(item.get("parise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("create_date", "1970-07-01"))
        # 执行sql
        self.cursor.execute(insert_sql, tuple(params))
        # 提交
        self.conn.commit()

        return item
```