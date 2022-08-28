import time

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import JobInfo

@login_required(login_url='/login/')
def index(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    city = request.GET.get('city')
    jobs = JobInfo.objects.all().order_by("id")
    cityss = jobs.values("city")
    city_cnt = {}
    for citys in cityss:
        city_cnt[citys['city']] = city_cnt.get(citys['city'],0)+1
    city_cnt = dict(sorted(city_cnt.items(), key=lambda x:x[1], reverse=True)[:20])
    if search:
        jobs = jobs.filter(Q(job_name__icontains=search))
    else:
        search = ""
    if order == "new_views":
        jobs = jobs.order_by("-crawling_time")
    if city != "None" and city:
        jobs = jobs.filter(city=city)
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    context = {'jobs':jobs, 'search':search, 'page':page, 'city_cnt':city_cnt, 'city':city}
    return render(request, 'system/index.html', context)

@login_required(login_url='/login/')
def show(request):
    jobs = JobInfo.objects.all()
    date = time.strftime("%Y-%m-%d", time.localtime())
    count_today = len(jobs.filter(crawling_time__gt=date))
    count_sum = len(jobs)
    context = {'count_sum': count_sum, 'count_today': count_today}
    return render(request, 'system/show.html', context)

@login_required(login_url='/login/')
def show_number(request):
    jobs = JobInfo.objects.all()
    date = time.strftime("%Y-%m-%d", time.localtime())
    count_today = len(jobs.filter(crawling_time__gt=date))
    count_sum = len(jobs)
    context = {'count_sum':count_sum, 'count_today':count_today}
    return render(request, 'system/show_number.html', context)

def get_echart_data(request):
    jobs = JobInfo.objects.all()
    returnData = {}
    returnData['echart_1'] = {'x_name':[],'data':[]}
    returnData['echart_2'] = {'x_name': [], 'data': []}
    returnData['echart_3'] = {'data':[]}
    returnData['echart_4'] = {'data': []}
    returnData['echart_5'] = {'x_name': [], 'data': []}
    returnData['echart_6'] = {'data': []}
    returnData['map'] = {'data':[]}
    job_name_list = list(jobs.values('job_name'))
    job_name_cnt = {}
    for job_name in job_name_list:
        job_name = job_name['job_name']
        job_name_cnt[job_name] = job_name_cnt.get(job_name,0)+1
    job_name_cnt = sorted(job_name_cnt.items(), key=lambda x:x[1], reverse=True)
    for x_name,data in job_name_cnt[:10]:
        returnData['echart_1']['x_name'].append(x_name)
        returnData['echart_1']['data'].append(data)

    salary_section_list = list(jobs.filter(~Q(salary_section="")).values('salary_section'))
    salary_section_cnt = {}
    for salary_section in salary_section_list:
        salary_section = salary_section['salary_section']
        salary_section_cnt[salary_section] = salary_section_cnt.get(salary_section, 0) + 1
    salary_section_cnt = sorted(salary_section_cnt.items(), key=lambda x: x[0])
    salary_section_cnt.insert(1, salary_section_cnt[6])
    salary_section_cnt.insert(1, salary_section_cnt[7])
    salary_section_cnt.pop(8)
    salary_section_cnt.pop(12)
    for x_name,data in salary_section_cnt:
        returnData['echart_2']['x_name'].append(x_name)
        returnData['echart_2']['data'].append(data)

    company_direction_list = list(jobs.values('company_direction'))
    company_direction_cnt = {}
    for company_direction in company_direction_list:
        company_directions = company_direction['company_direction']
        for company_direction in company_directions.split('/'):
            company_direction_cnt[company_direction] = company_direction_cnt.get(company_direction,0)+1
    for name in company_direction_cnt:
        returnData['echart_3']['data'].append({'name':name,'value':company_direction_cnt[name]})

    company_size_list = list(jobs.values('company_size'))
    company_size_cnt = {}
    for company_size in company_size_list:
        company_size = company_size['company_size']
        company_size_cnt[company_size] = company_size_cnt.get(company_size, 0) + 1
    for name in company_size_cnt:
        returnData['echart_4']['data'].append({'name': name, 'value': company_size_cnt[name]})

    educational_list = list(jobs.values('educational'))
    educational_cnt = {}
    for educational in educational_list:
        educational = educational['educational']
        educational_cnt[educational] = educational_cnt.get(educational, 0) + 1
    educational_cnt = sorted(educational_cnt.items(), key=lambda x: x[1], reverse=True)
    for x_name, data in educational_cnt[:5]:
        returnData['echart_5']['x_name'].append(x_name)
        returnData['echart_5']['data'].append(data)

    experience_list = list(jobs.values('experience'))
    experience_cnt = {}
    for experience in experience_list:
        experience = experience['experience']
        experience_cnt[experience] = experience_cnt.get(experience,0)+1
    experience_cnt = sorted(experience_cnt.items(), key=lambda x: x[1], reverse=True)
    for name,value in experience_cnt[:4]:
        returnData['echart_6']['data'].append({'name': name, 'value': value})

    city_list = list(jobs.values('city'))
    city_cnt = {}
    for city in city_list:
        city = city['city']
        city_cnt[city] = city_cnt.get(city, 0) + 1
    for name in city_cnt:
        returnData['map']['data'].append({'name': name, 'value': city_cnt[name]})
    return JsonResponse(returnData,safe=False, json_dumps_params={'ensure_ascii': False})