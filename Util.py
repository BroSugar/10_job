import json

import requests
import xlwings as xw
import urllib
from urllib import parse


def read_json(file_url):
    return json.load(open(file_url, 'r', encoding="utf-8"))


def create_excel(filename):
    app = xw.App(visible=True, add_book=False)
    wb = app.books.add()
    wb.save(filename)
    wb.close()
    app.quit()


def write_excel_title(filename, title_json_list, sheetname='Sheet1', first_cell='A1'):
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    wb = app.books.open(filename)
    sheet = wb.sheets[sheetname]
    sheet.range(first_cell).value = title_json_list
    wb.save()
    wb.close()
    app.quit()


def write_excel(filename, json, first_cell, sheetname='Sheet1'):
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    wb = app.books.open(filename)
    sheet = wb.sheets[sheetname]
    sheet.range(first_cell).value = json
    wb.save()
    wb.close()
    app.quit()


def write_excel_batch(filename, json_list, first_cell, sheetname='Sheet1'):
    app = xw.App(visible=True, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    wb = app.books.open(filename)
    sheet = wb.sheets[sheetname]
    sheet.range(first_cell).options(expand='table').value = json_list
    wb.save()
    wb.close()
    app.quit()


def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        return response.text
    else:
        return


def get_data_url_encode(url, params):
    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = response.json()
        recuit_files = result.get('RecuitFiles')
        return urllib.parse.unquote(recuit_files)
    else:
        return


if __name__ == '__main__':
    # write_excel_title('test.xlsx',  read_json('config.json').get("excel").get("title_name"), 'Sheet1','A1')
    params = {
        "page": 1,
        "rows": 50,
        "sidx": "Id",
        "sord": "asc",
        "id": 10138
    }
    text = get_data_url_encode('https://jy.sicnu.edu.cn/home/queryZwPro', params)
    print(text)
