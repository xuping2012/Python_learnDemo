'''
Created on 2020年6月4日

@author: qguan
'''
import unittest
from utils.HandleRedis import HandleRedis
from utils.HandleRequests import HandleRequests
from utils.HandleConfig import INIParser
from utils.HandleMySQL import HandleMySQL
import path_config


class Test(unittest.TestCase):
    red = HandleRedis(9)
    do_http = HandleRequests()
    conf = INIParser(path_config.prop_path + 'mysql.ini')
    do_mysql = HandleMySQL()

    @classmethod
    def setUpClass(cls):
        """oral:practice:should:write:both 为2同时写旧表和分表，不设置写旧表"""

        cls.g_v = cls.red.get_value_by_key('oral:practice:should:write:both')
        if not cls.g_v:
            cls.s_v = cls.red.set_key_value(
                'oral:practice:should:write:both', '2')
        cls.oral_topic_id = 443
        cls.question_id = 8982
        # 登录接口及请求参数
        login_url = '{}/hcp/apiLogin/passwordLogin'.format(
            cls.conf.get_string('mysql', 'addr'))
        login_data = {
            "verifyCode": "",
            "zone": "86",
                    "loginType": 0,
                    "password": '111111',
                    "deviceType": "ios",
                    "pushToken": "dea9b867c475831cf55d3e1318d478b9",
                    "channel": 0,
                    "deviceName": "iPhone 8 Plus",
                    "deviceid": "4F673A5F-BA15-47B9-B9A0-AF43F1DBF990",
                    "mobile": '13266515340'
        }
        # 发送http请求，封装的请求已经返回json格式
        cls.res = cls.do_http("post", login_url, data=login_data, is_json=True)
        # 没有使用jsonpath提取dict参数，已知接口返回json，使用dict的get方法
        try:  # 这里处理登录用户信息有时登录失败，可能区号不正确
            cls.token = cls.res.get('content').get('token')
            cls.userId = cls.res.get('content').get('userId')
        except:
            print(login_data)
            raise
        else:
            # 用户联系记录分表，%64取模分64张表
            cls.db_no = int(cls.userId) % 64
            # 构造下一个接口的请求头：加入token认证信息
            cls.headers = {
                "source": "0", "Authorization": "Bearer {}".format(cls.token)}
#
#         o_prac_sql = "SELECT count(1) as old_count FROM user_oral_practice_dup WHERE user_id={}".format(
#             cls.userId)
#         o_pres = cls.do_mysql(o_prac_sql)
#         cls.o_prac_count = o_pres.get('old_count')
#
#         p_no = int(cls.userId) % 64
#         f_prac_sql = "SELECT count(1) as fen_count FROM user_oral_practice_{} WHERE user_id={}".format(
#             p_no, cls.userId)
#         f_pres = cls.do_mysql(f_prac_sql)
#         cls.f_prac_count = f_pres.get('fen_count')

    def testName(self):

        # 查看范文 保存用户练习记录数据:硬编码，上面的一系列接口都不需要请求
        save_url = "{}/hcp/studyCenter/oralPractice/save".format(
            self.conf.get_string('mysql', 'addr'))
        save_data = {
            "oralTopCatalog": 4,
            "oralQuestion": "Do you prefer natural parks or amusement parks?",
            "ifPrivate": 1,
            "oralQuestionId": self.question_id,
            "oralPart": 1,
            "oralUrl": "1591155416556.mp3",
            "seconds": 11,
            "oralTopicId": self.oral_topic_id,
            "topic": "Park",
            "source": 0
        }
        self.do_http(
            'post', save_url, data=save_data, headers=self.headers, is_json=True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #     print(1592533156822153753 % 64)
    unittest.main()
#     print(443 % 64)
