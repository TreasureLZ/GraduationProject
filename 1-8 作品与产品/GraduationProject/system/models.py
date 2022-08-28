from django.db import models

class JobInfo(models.Model):
    job_name = models.CharField(max_length=255, null=True, blank=True)
    crawling_time = models.DateTimeField(max_length=255)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    salary = models.CharField(max_length=255, null=True, blank=True)
    salary_detail = models.CharField(max_length=255, null=True, blank=True)
    salary_section = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    educational = models.CharField(max_length=255, null=True, blank=True)
    company_size = models.CharField(max_length=255, null=True, blank=True)
    company_direction = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    job_url = models.TextField(null=True, blank=True)
    company_url = models.TextField(null=True, blank=True)