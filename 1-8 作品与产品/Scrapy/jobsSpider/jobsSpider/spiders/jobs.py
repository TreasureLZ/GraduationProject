import scrapy
from bs4 import BeautifulSoup
import json
from jobsSpider.items import JobsItem
from datetime import datetime
from jobsSpider.Util.KEY_WORD_LIST import Get_Key_Word

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    baseUrl = "https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html"
    start_urls = [baseUrl.format(Get_Key_Word(),1)]

    def parse(self, response):
        text = response.text
        soup = BeautifulSoup(text,'lxml')
        print(soup)
        scripts = soup.select('script')
        old_json = str(scripts[7])
        print(old_json)
        new_json = old_json[old_json.find("{"):len(old_json)-old_json[::-1].find("}")]
        print(new_json)
        infos = json.loads(new_json)
        for info in infos['engine_jds']:
            item = JobsItem()
            item['job_name'] = info['job_name']
            item['release_time'] = info['issuedate']
            item['crawling_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['company_name'] = info['company_name']
            item['salary'] = info['providesalary_text']
            item['duty_station'] = info['workarea_text']
            item['experience'] = info['attribute_text'][1]
            if len(info['attribute_text']) == 4:
                item['educational'] = info['attribute_text'][2]
            else:
                item['educational'] = "不限"
            item['company_size'] = info['companysize_text']
            item['company_direction'] = info['companyind_text']
            item['job_url'] = info['job_href']
            item['company_url'] = info['company_href']
            yield item
        

        # for i in range(2,10):
        #     next_url = self.baseUrl.format(Get_Key_Word(),i)
        #     yield scrapy.Request(next_url)
