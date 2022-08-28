import scrapy
from bs4 import BeautifulSoup
from jobsSpider.items import JobsItem
from datetime import datetime, timedelta
from jobsSpider.Util.KEY_WORD_LIST import Get_Key_Word

class JobLiepinSpider(scrapy.Spider):
    name = 'job_liepin'
    baseUrl = 'https://www.liepin.com/zhaopin/?key={}&currentPage={}'
    start_urls = [baseUrl.format(Get_Key_Word(),0)]

    def parse(self, response):
        text = response.text
        soup = BeautifulSoup(text,'lxml')  
        li_list = soup.select('section.content-left-section div.left-list-box ul li div.job-list-item')
        for li in li_list:
            try:
                item = JobsItem()
                item['job_name'] = li.select('div.job-title-box div.ellipsis-1')[0].text.split()[0]
                item['crawling_time'] = (datetime.now()+timedelta(-2)).strftime('%Y-%m-%d %H:%M:%S')
                item['company_name'] = li.select('div.job-company-info-box span.company-name.ellipsis-1')[0].text.split()[0]
                item['salary'] = li.select('span.job-salary')[0].text.split()[0]
                item['salary_detail'],item['salary_section'] = self.salary_clean(item['salary'])
                item['city'],item['area'] = self.station_clean(li.select('div.job-dq-box span.ellipsis-1')[0].text.split()[0])
                item['experience'] = li.select('div.job-labels-box span.labels-tag')[1].text.split()[0]
                item['educational'] = li.select('div.job-labels-box span.labels-tag')[0].text.split()[0]
                item['skills'] = "|".join([skill.text.split()[0] for skill in li.select('div.job-labels-box span.labels-tag')[2:]])
                spans = li.select('div.company-tags-box.ellipsis-1 span')
                item['company_direction'] = spans[0].text
                if len(spans) >= 3:
                    item['company_size'] = spans[2].text
                else:
                    item['company_size'] = spans[1].text
                item['job_url'] = li.select('div.job-detail-box a')[0].get('href')
                try:
                    item['company_url'] = li.select('div.job-detail-box a')[1].get('href')
                except:
                    item['company_url'] = ""
                if item['salary'] == "":
                    continue
                yield item
            except:
                continue
        for i in range(1,21):
            next_url = self.baseUrl.format(Get_Key_Word(),i)
            yield scrapy.Request(next_url)

    def salary_clean(self, salary_detail):
        if '薪' in salary_detail:
            salary_detail = salary_detail.replace('薪','')
            salary_detail = (eval(salary_detail.split('k')[0].split('-')[0]) + eval(salary_detail.split('k')[0].split('-')[1])) * 1000 * eval(salary_detail.split('·')[1]) // 24
        elif '面议' in salary_detail:
            return "",""
        else:
            if '-' in salary_detail:
                salary_detail = salary_detail.replace('k','')
                salary_detail = (eval(salary_detail.split('-')[0]) + eval(salary_detail.split('-')[1])) * 1000 // 2
            else:
                salary_detail = eval(salary_detail) * 1000
        salary_section = ""
        if salary_detail <= 3000:
            salary_section = "0-3k"
        elif salary_detail <= 6000:
            salary_section = "3-6k"
        elif salary_detail <= 10000:
            salary_section = "6-10k"
        elif salary_detail <= 14000:
            salary_section = "10-14k"
        elif salary_detail <= 18000:
            salary_section = "14-18k"
        elif salary_detail <= 22000:
            salary_section = "18-22k"
        elif salary_detail <= 26000:
            salary_section = "22-26k"
        elif salary_detail <= 30000:
            salary_section = "26-30k"
        elif salary_detail <= 35000:
            salary_section = "30-35k"
        elif salary_detail <= 40000:
            salary_section = "35-40k"
        elif salary_detail <= 50000:
            salary_section = "40-50k"
        else:
            salary_section = "50k+"
        return str(salary_detail),salary_section

    def station_clean(self,station):
        try:
            return station.split("-")[0],station.split("-")[1]
        except:
            return station.split("-")[0],""