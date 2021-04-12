import scrapy

class KrNewsInformation(scrapy.Item):
    # 标题
    titile = scrapy.Field()
    # 创建时间（xx分钟前）
    create_time_key = scrapy.Field()
    # 简要
    brief = scrapy.Field()
    # 正文链接
    text_link = scrapy.Field()
