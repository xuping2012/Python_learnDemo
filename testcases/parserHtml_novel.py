'''
Created on 2020年7月24日

@author: qguan
'''
import re
import requests

url = 'https://k.yqhy.org/chapters_46215_{}/'

for num in range(30, 60):
    r_url = url.format(num)
    res = requests.get(r_url, verify=False).text
    reg_x = '[0-9]{8}.html'
    res_url = re.findall(reg_x, res)
#     print(res_url)
#     for i in range(0, 20):
#         print(res_url.groups())
    for i in range(len(res_url)):
        print(res_url[i])
