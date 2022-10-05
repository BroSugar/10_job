
import datetime

import Util as util

# 成都本地本地宝教师招聘数据收集
title_name = '成都本地本地宝教师招聘数据收集'

json_default_list = []
json_default_title = ['ID', '单位名称', '招聘简介', '发布日期', '招聘明细', '岗位详情']


def write_excel(json_list, title):
    today = datetime.date.today()
    str_today = today.strftime("%Y%m%d")
    file_name = title_name + str_today + '.xlsx'
    util.create_excel(file_name)
    util.write_excel_title(file_name, title)
    util.write_excel_batch(file_name, json_list, 'A2')



def get_data():
    url = util.read_json('config.json')['job_infos'][2]['page_url']

