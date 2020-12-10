'''
Created on 2020年6月3日

@author: qguan
'''
import unittest
from utils.HandleMySQL import HandleMySQL


class Test(unittest.TestCase):

    do_mysql = HandleMySQL()

    def setUp(self):
        sql = "select DISTINCT oral_topic_id from user_oral_practice_dup where oral_topic_id != ''"
# ;
# ;
        self.res = self.do_mysql(sql, is_more=True)
#         self.topic_id=self.res.get('oral_topic_id')
        self.topic_list = []
        for topic_id in self.res:
            self.topic_list.append(topic_id.get('oral_topic_id'))

    @unittest.skipIf(False, "test")
    def testName(self):
        i = 0
        for topic_id in self.topic_list:
            o_sql = "SELECT COUNT(1) AS o_count FROM user_oral_practice_dup where oral_topic_id={}".format(
                topic_id)
            o_res = self.do_mysql(o_sql)
            o_count = o_res.get('o_count')
            db_no = int(topic_id) % 64
            n_sql = "SELECT COUNT(1) as n_count FROM user_practice_topic_{} where oral_topic_id={}".format(
                db_no, topic_id)
            n_res = self.do_mysql(n_sql)
            n_count = n_res.get('n_count')
            i += 1
            print("执行第{}次".format(i))
            if o_count != n_count:
                with open("oral_topic_id.txt", "a+") as pf:
                    pf.write("话题id：{},分表user_practice_topic_{}后数据不一致:{}，user_oral_practice_dup原数据：{}\n".format(
                        topic_id, db_no, n_count, o_count))

    def tearDown(self):
        self.do_mysql.mysql_close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
