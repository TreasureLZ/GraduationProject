from itemadapter import ItemAdapter
import pymysql


class JobsMySQLPipeline:
    def __init__(self):
        self.connect = pymysql.connect(host="localhost", user="root", passwd="Llb011223", db="GraduationProject")
        self.cursor = self.connect.cursor()
        print("连接数据库成功！")

    def process_item(self, item, spider):
        insert_sql = '''
        insert into system_jobinfo(
            job_name,crawling_time,company_name,salary,salary_detail,salary_section,city,area,experience,educational,company_size,company_direction,skills,job_url,company_url
            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(insert_sql,
                            [item['job_name'], item['crawling_time'], item['company_name'], item['salary'],
                             item['salary_detail'],
                             item['salary_section']
                                , item['city'], item['area'], item['experience'], item['educational'],
                             item['company_size'], item['company_direction'],
                             item['skills'], item['job_url'], item['company_url']
                             ])
        self.connect.commit()
        return item

    def close_spider(self, spider):
        print("数据存储完成！")
        self.cursor.close()
        self.connect.close()


class JobsFilePipeline:
    def open_spider(self, spider):
        self.fp = open('infos.csv', 'w+')
        self.fp.write(
            'job_name,crawling_time,company_name,salary,salary_section,city,area,experience,educational,company_size,company_direction,skills,job_url,company_url\n')

    def process_item(self, item, spider):
        self.fp.write(",".join(
            [item['job_name'], item['crawling_time'], item['company_name'], item['salary'], item['salary_section']
                , item['city'], item['area'], item['experience'], item['educational'],
             item['company_size'], item['company_direction'],
             item['skills'], item['job_url'], item['company_url']
             ]) + "\n")

    def close_spider(self, spider):
        self.fp.close()
