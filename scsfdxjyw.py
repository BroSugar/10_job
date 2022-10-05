import requests
import datetime

import Util as util

# 四川师范大学就业网数据收集
title_name = '四川师范大学就业网数据收集'

json_default_list = []
second_url = 'https://jy.sicnu.edu.cn/home/zwPro/${id}?code=1'
json_default_title = ['ID', '单位名称', '发布日期', '招聘日期', '招聘地点', '岗位详情']


def write_excel(json_list, title):
    today = datetime.date.today()
    str_today = today.strftime("%Y%m%d")
    file_name = title_name + str_today + '.xlsx'
    util.create_excel(file_name)
    util.write_excel_title(file_name, title)
    util.write_excel_batch(file_name, json_list, 'A2')


def get_list_page(url, params):
    response = requests.post(url, data=params)
    # 当前页数
    p = params['page']
    if response.status_code == 200:
        result = response.json()
        # 当前页
        page = result['page']
        # 总记录数
        records = result['records']
        # 共total页
        total = result['total']
        # 数据列表
        rows = result['rows']
        for record in rows:
            # ['ID', '单位名称', '发布日期', '招聘日期', '招聘地点', '岗位详情']
            r = [record['Id'], record['CorpName'], record['CreateDate'],
                 record['OpenDate'] + ' ' + record['StartHour'], record['Title'],
                 second_url.replace('${id}', str(record['Id']))]
            json_default_list.append(r)
        if p == total:
            return 0
    else:
        return 0


def get_list(url, params):
    while 1:
        r = get_list_page(url, params)
        if r == 0:
            break
        params['page'] = params['page'] + 1
    write_excel(json_default_list, json_default_title)


def get_data():
    url = util.read_json('config.json')['job_infos'][0]['data_url']
    params = util.read_json('config.json')['job_infos'][0]['param']
    get_list(url, params)
