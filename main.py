import datetime
import logging

import requests

import Util

file_url = "./config.json"

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '69',
    'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

cookies = {
    'JSESSIONID': '20d51a18-2ea2-4d47-baed-1ebf3ec8aeff'
}

fmt = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s"


def log_config():
    today = datetime.date.today()
    str_today = today.strftime("%Y%m%d")
    logging.basicConfig(
        level=logging.DEBUG,
        format=fmt,
        filename="./log-" + str_today + ".log",
        filemode="w",
        datefmt="%a, %d %b %Y %H:%M:%S"
    )


if __name__ == '__main__':
    config = Util.read_json(file_url)
    job_infos = config.get("job_infos")
    log_config()
    for job in job_infos:
        is_valid = job.get("is_valid")
        if is_valid and len(job.get("data_url")) > 0 and job.get("type") == 'json':
            method = job.get("method")
            url = job.get("data_url")
            param = job.get("param")
            if method == 'post':
                response = requests.post(url, data=param)
                res_code = response.status_code
                if res_code == 200:
                    logging.info(job.get("name") + "：请求成功")
                    logging.info(response.json())
                else:
                    logging.error(job.get("name") + "：请求失败")
            if method == 'get':
                response = requests.get(url, params=param, timeout=3)
                res_code = response.status_code
                if res_code == 200:
                    logging.info(job.get("name") + "：请求成功")
                    logging.info(response.json())
                else:
                    logging.error(job.get("name") + "：请求失败")
