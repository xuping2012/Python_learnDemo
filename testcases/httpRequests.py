'''
Created on 2020年4月22日

@author: qguan
'''
# 导包
import requests

# 构造参数：请求参数、请求头、headers
header = {"User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

# 发送请求
do_http = requests.request("GET", "http://www.baidu.com")
res = requests.get("http://www.baidu.com")
# 接收响应结果
print(res.headers)
print(do_http.status_code)
print(res.text)
print(res.content.decode('utf-8'))

# print(res.json())
# 1、字典的形式定义请求参数
dic1 = {
    "curPage": 1,
    "limit": 10,
    "order": "desc",
    "orderFields": "id",
    "regionId": 0,
    "sortType": 0,
    "topicId": 100026
}
header = {"conTent-Type": "application/json"}
res1 = requests.post(
    "http://47.107.254.16:9500/hcp/studyAbroad/question/listByTopic", json=dic1, headers=header)
print(res1.content.decode('utf-8'))
print(res1.headers)
