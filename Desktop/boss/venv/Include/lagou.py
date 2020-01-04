# -*- coding: UTF-8 -*-

import requests
import pymysql
import random
import time
import json

# 直接在浏览器查看请求网址及请求头参数
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    'Cookie': 'user_trace_token=20180716091904-3a769091-8896-11e8-9a9b-525400f775ce; LGUID=20180716091904-3a7693db-8896-11e8-9a9b-525400f775ce; LG_LOGIN_USER_ID=85e6b36b294cf09b2a82093124adf51c41ff7364f82534e5; _ga=GA1.2.1393599455.1531703944; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221674ae853633e2-019d5fa93b9c51-3c604504-1049088-1674ae85364331%22%2C%22%24device_id%22%3A%221674ae853633e2-019d5fa93b9c51-3c604504-1049088-1674ae85364331%22%7D; WEBTJ-ID=20181204162515-16778523ed3109-0a5052acbff0a7-3c604504-1049088-16778523ed41c5; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543149992,1543911916; X_HTTP_TOKEN=9ff347da4ea369a0edd5701b5e619fc5; Hm_lvt_dde6ba2851f3db0ddc415ce0f895822e=1543149999,1543911923; _putrc=47050A59BD8A0BB5; JSESSIONID=ABAAABAAADEAAFIDC2DF4242ED8AC49BD143B87A88AAE1E; login=true; unick=%E5%BB%96%E5%9F%B9%E7%82%8E; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=31; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.970223374.1544061772; gate_login_token=ed085e50425284435c14fe4f8f181b01bd377453efc0258f; LGSID=20181206104428-d9e63fa3-f900-11e8-8cd0-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FlabelWords%3Dlabel; TG-TRACK-CODE=search_code; _gat=1; LGRID=20181206110812-2ad567bb-f904-11e8-8ce6-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544065694; Hm_lpvt_dde6ba2851f3db0ddc415ce0f895822e=1544065701; SEARCH_ID=da3215be183e441faa0840706b828476',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Connection': 'keep-alive',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_java?oquery=Python&fromSearch=true&labelWords=relative'
}

# 连接数据库
db = pymysql.connect(host='192.168.75.129', user='root', password='123456', port=3306, db='lagou')


def add_Mysql(id, name, salary, city, experience, education, company_name, company_status, company_people, ):
    # 将数据写入数据库中
    try:
        cursor = db.cursor()
        sql = 'insert into lagou_job(id, name, salary, city, experience, education, company_name,company_status, company_people) values ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (
        id, name, salary, city, experience, education, company_name, company_status, company_people)
        print(sql)
        cursor.execute(sql)
        print(cursor.lastrowid)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def get_message():
    for i in range(1, 10):
        print('第' + str(i) + '页')
        time.sleep(random.randint(10, 20))
        data = {
            'first': 'false',
            'pn': i,
            'kd': '数据分析'
        }
        response = requests.post(url, data=data, headers=headers)
        result = json.loads(response.text)
        # 打印获取结果
        print(result)
        job_messages = result['content']['positionResult']['result']
        for job in job_messages:
            global count
            count += 1
            # 岗位名称
            name = job['positionName']
            print(job_title)
            # 岗位薪水
            salary = job['salary']
            print(job_salary)
            # 岗位地点
            city = job['city']
            print(job_city)
            # 岗位经验
            experience = job['workYear']
            print(job_experience)
            # 岗位学历
            education = job['education']
            print(job_education)
            # 公司名称
            company_name = job['companyShortName']
            print(company_name)
            # 公司状态
            company_status = job['financeStage']
            print(company_status)
            # 公司规模
            company_people = job['companySize']
            print(company_people)
            # 写入数据库
            add_Mysql(id, name, salary, city, experience, education, company_name, company_status, company_people)


if __name__ == '__main__':
    get_message()
    span = round(random.random() * 6, 1)
    time.sleep(span)