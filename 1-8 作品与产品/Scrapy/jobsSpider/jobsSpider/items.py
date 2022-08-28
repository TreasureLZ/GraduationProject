# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobsItem(scrapy.Item):
    # 岗位名称
    job_name = scrapy.Field()
    # 爬取时间
    crawling_time = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 薪资细分
    salary_detail = scrapy.Field()
    # 薪资区间
    salary_section= scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 区县
    area = scrapy.Field()
    # 工作经验
    experience = scrapy.Field()
    # 学历
    educational = scrapy.Field()
    # 公司规模
    company_size = scrapy.Field()
    # 公司方向
    company_direction = scrapy.Field()
    # 技能
    skills = scrapy.Field()
    # 岗位url
    job_url = scrapy.Field()
    # 公司url
    company_url = scrapy.Field()