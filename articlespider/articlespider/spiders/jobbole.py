
from urllib import parse
import scrapy

# 反爬的处理工具
import requests
# 动态获取ID，解决反爬使用
import re
import json

# line 4的代码应用在23、24、25行
# from scrapy import Selector

from scrapy import Request


class JobboleSpider(scrapy.Spider):

    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        # response：通过response获取到也看信息
        # 通过full xpath获取
        url = response.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/h2/a/@href').extract_first()
        # 通过不变ID结合xpath获取（集合）
        #url2 = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract()
        # CSS selector获取节点信息
        #url3 = response.css('#news_list h2 a::attr(href)')

        # 通过scrapy selector执行选择器
        # sel = Selector(text=response.text)
        # url4 = sel.css('#news_list h2 a::attr(href)')
        # url5 = sel.xpath('/html/body/div[2]/div[2]/div[4]/div[1]/div[2]/h2/a/@href').extract_first()

        """
        目标：
        1.获取新闻列表页的新闻url，交给scrapy进行下载后调用相应的解析方法
        2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse继续跟进
        """
        post_nodes = response.css('#news_list .news_block')[:1]
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(href)').extract_first("")
            print("图片地址：" + image_url)
            post_url = post_node.css('h2 a::attr(href)').extract_first("")

            print("详细地址：" + post_url)
            # 重定向到详情信息
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载（翻页） 46和47含义相同，一个是css一个是xpath
        """
        # 方法1：
        next_url = response.css('div.pager a:last-child::text').extract_first("")
        if next_url == "Next >":
            next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
            yield Request(url = parse.urljoin(response.url, next_url), callback=self.parse)
        """
        # --------------------------------------------------------
        """
        # 方法2：
        next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first("")
        yield Request(url = parse.urljoin(response.url, next_url), callback=self.parse)
        """

        pass

    def parse_detail(self, response):

        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            # 标题
            title = response.css('#news_title a::text').extract_first('')
            # 时间
            create_date = response.css('#news_info > span.time::text').extract_first('')
            # 内容
            content = response.css('#news_content').extract_first('')
            # 标签
            tag_list = response.css('.news_tags a::text').extract()
            tags = ",".join(tag_list)
            # 评论（JS获取）
            comment = response.css('#news_info > span.comment > a').extract()
            # 点赞数（JS获取）
            agree = response.css('#news_otherinfo > div:nth-child(1) > div.diggit > span::text').extract()

            post_id = match_re.group(1)
            # source_url 应该是动态的
            source_url = 'https://news.cnblogs.com';
            html = requests.get(parse.urljoin(source_url, "NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            j_data = json.loads(html.text)
            # 点赞数
            praise_nums = j_data["DiggCount"]
            # 兴趣数
            fav_nums = j_data["TotalView"]
            # 评论数
            comment_nums = j_data["CommentCount"]
        pass
