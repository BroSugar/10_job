import requests
import datetime

import Util as util

# 西南大学就业网数据收集
title_name = '西南大学就业网数据收集'

json_default_list = []
second_url = 'http://bkjyw.swu.edu.cn/#/wanted/preach-detail/${id}'
json_default_title = ['ID', '单位名称', '领域', '岗位性质', '招聘日期', '招聘地点', '关注度', '岗位详情']


def write_excel(json_list, title):
    today = datetime.date.today()
    str_today = today.strftime("%Y%m%d")
    file_name = title_name + str_today + '.xlsx'
    util.create_excel(file_name)
    util.write_excel_title(file_name, title)
    util.write_excel_batch(file_name, json_list, 'A2')


def get_list_page(url, params):
    response = requests.get(url, data=params)
    # 当前页数
    p = params['page']
    if response.status_code == 200:
        result = response.json()['data']
        # 共total页
        total = result['totalPage']
        # 数据列表
        rows = result['list']
        for record in rows:
            # ['ID', '单位名称', '领域', '岗位性质', '招聘日期', '招聘地点', '关注度', '岗位详情']
            r = [record['id'], record['unitName'], record['industry'],
                 record['nature'], record['startTime'], record['placeName'], record['viewCount'],
                 second_url.replace('${id}', str(record['id']))]
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
    url = util.read_json('config.json')['job_infos'][1]['data_url']
    params = util.read_json('config.json')['job_infos'][1]['param']
    get_list(url, params)
