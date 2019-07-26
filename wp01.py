import requests
import json

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user_id = config['wordpress']['user_id']
password = config['wordpress']['password']
end_point_url = config['wordpress']['end_point_url']

title = "Pythonから投稿するサンプル"
 
content = """<h2>サンプルだよ</h2>
 
あいうえお
かきくけこ
"""
 
status = "draft"
 
data = {
        'title': title, 
        'content' : content,
        'status' : status
        }
 
headers = {'content-type': "Application/json"}
 
r = requests.post(end_point_url, json=data, headers=headers, auth=(user_id, password))
print(r.text)
print(r.content)
