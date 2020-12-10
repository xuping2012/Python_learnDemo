'''
Created on 2020年4月17日

@author: qguan
'''
# 读取文件
import unittest

import jsonpath
import requests

from BeautifulReport.BeautifulReport import BeautifulReport
from library.HTMLTestRunnerNew import HTMLTestRunner


class TestLoginMessage(unittest.TestCase):
    # aciia

    def test_01(self):
        "在这里描述"
        # 构造请求参数
        url = "http://test.user-center.ieltsbro.com/hcp/apiLogin/passwordLogin"
        data = {
            "appVersion": "9.0.0",
            "channel": 0,
            "deviceName": "HUAWEI EML-AL00",
            "deviceType": "android",
            "deviceid": "0795cd72-3e05-40ba-9733-5df1c1fa0970",
            "loginType": 0,
            "mobile": "13266515340",
            "password": "111111",
            "pushToken": "25b9b066dc939b9863fe9feb3fca654d",
            "systemVersion": "8.1.0",
            "zone": 86
        }
        header = {"content-type": "application/json"}
        global token
        # 发送请求并接收响应
        res = requests.post(url, json=data, headers=header)
        message = jsonpath.jsonpath(res.json(), "message")[0]
        token = jsonpath.jsonpath(res.json(), "$.content.token")[0]
        self.assertEqual(message, "success", "请求响应失败")

    def test_02(self):
        url = "http://test.user-center.ieltsbro.com/hcp/user/collectRecord/collectionAllPageList"
        data = {"curPage": 1, "limit": 20}
        header = {"source": "0", "content-type": "application/json",
                  "Authorization": "Bearer {}".format(token)}
        res = requests.get(url, params=data, headers=header)
        message = jsonpath.jsonpath(res.json(), "message")[0]
        self.assertEqual(message, "success1", "请求响应失败")

    @unittest.skip("希望失败")
    def test_sub(self):
        "在这里是否也支持"
        a = 1
        b = 2
        c = a - b

        url = "http://47.107.254.16:9300/hcp/user/collectRecord/collectionAllPageList"
        data = {"curPage": 1, "limit": 20}
        # .format(token)
        header = {"source": "0", "content-type": "application/json",
                  "Authorization": "Bearer {}".format(token)}
        res = requests.get(url, params=data, headers=header)
        message = jsonpath.jsonpath(res.json(), "message")[0]
        self.assertEqual(message, "success", "请求响应失败")
        self.assertEqual(c, -1, "msg")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoginMessage)
    with open(file="../reports/report.html", mode="wb+") as bf:
        run = HTMLTestRunner(
            stream=bf, verbosity=2, title="我是测试报告标题", description="描述一下测试报告", tester="是我完成的")
        run.run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoginMessage)
    run = BeautifulReport(suite)
    run.report(description="测试报告2020", filename="reportNew.html",
               report_dir="../reports", theme="theme_default")
