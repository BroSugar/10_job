import json

def read_json(file_url):
    return json.load(open(file_url, 'r', encoding="utf-8"))
