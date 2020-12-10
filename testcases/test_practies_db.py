'''
Created on 2020年6月1日

@author: qguan
'''
import threading
import unittest

from utils.HandleMySQL import HandleMySQL


class Test(unittest.TestCase, threading.Thread):

    # 初始化http请求、mysql操作对象
    do_mysql = HandleMySQL()

    @classmethod
    def setUpClass(cls):
        # 用户练习表
        exc_sql = "SELECT user_id FROM user_dup_exercises AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(exer_id) FROM user_exercises)-(SELECT MIN(exer_id) FROM user_exercises))+(SELECT MIN(exer_id) FROM user_exercises)) AS exer_id) AS t2 WHERE t1.exer_id >= t2.exer_id ORDER BY t1.exer_id LIMIT 1"
        cls.exc_res = cls.do_mysql(exc_sql)

        # 用户口语练习表
        oral_sql = "SELECT user_id FROM user_oral_practice_dup AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM user_oral_practice)-(SELECT MIN(id) FROM user_oral_practice))+(SELECT MIN(id) FROM user_oral_practice)) AS id) AS t2 WHERE t1.id < t2.id ORDER BY t1.id LIMIT 1"
        cls.oral_res = cls.do_mysql(oral_sql)

        # 用户单词记录表
        wd_sql = "SELECT user_id FROM user_dup_words AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(word_id) FROM user_words)-(SELECT MIN(word_id) FROM user_words))+(SELECT MIN(word_id) FROM user_words)) AS word_id) AS t2 WHERE t1.word_id >= t2.word_id ORDER BY t1.word_id LIMIT 1"
        cls.wd_res = cls.do_mysql(wd_sql)

        # 用户练习口语主题表
        topic_sql = "SELECT oral_topic_id,user_id FROM user_oral_practice_dup AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM user_oral_practice_dup)-(SELECT MIN(id) FROM user_oral_practice_dup))+(SELECT MIN(id) FROM user_oral_practice_dup)) AS id) AS t2 WHERE t1.id >= t2.id ORDER BY t1.id LIMIT 1"
        cls.topic_res = cls.do_mysql(topic_sql)

    @unittest.skipIf(False, "用户练习表数据 分表尚未同步完数据!")
    def test_user_exercises(self):
        '''用户练习表:user_exercises'''
        # 校验每次随机的userId，分表后的该userId所拥有的数据是否一致
        user_id = self.exc_res.get('user_id')
        # int转换user_id%64取模
        db_no = int(user_id) % 64
        # 查询分表前用户数据count总数
        o_sql = "select count(1) as o_count from user_dup_exercises where user_id={}".format(
            user_id)
        o_res = self.do_mysql(o_sql)
        o_count = o_res.get('o_count')

        # 查询分表后用户数据count总数
        n_sql = "select count(1) as n_count from user_exercises_{} where user_id={}".format(
            db_no, user_id)
        n_res = self.do_mysql(n_sql)
        n_count = n_res.get('n_count')

#         print("分表前后数据对比：{},{}".format(o_count, n_count))
        # 断言分表前后count总数是否一致
        try:
            self.assertEqual(
                o_count, n_count, "user_dup_exercises分表{}前后user_id:{}数据有丢失!!!".format(db_no, user_id))
        except:
            with open("error_data.txt", 'a+') as pf:
                pf.write("用户：{},user_dup_exercises原数据：{},分表后user_exercises_{},数据：{} ".format(
                    user_id, o_count, db_no, n_count))
            raise

    def test_user_oral_practice(self):
        '''用户口语练习表:user_oral_practice:在这里分表时，需要将用户oral_topic_id为空的数据抛弃即可'''
        # 校验每次随机的userId，分表后的该userId所拥有的数据是否一致
        user_id = self.oral_res.get('user_id')
        # int转换user_id%64取模
        db_no = int(user_id) % 64
        # 查询分表前用户数据count总数
        o_sql = "select count(1) as o_count from user_oral_practice_dup where user_id={}".format(
            user_id)
        o_res = self.do_mysql(o_sql)
        o_count = o_res.get('o_count')

        # 查询分表后用户数据count总数
        n_sql = "select count(1) as n_count from user_oral_practice_{} where user_id={}".format(
            db_no, user_id)
        n_res = self.do_mysql(n_sql)
        n_count = n_res.get('n_count')

#         print("分表前后数据对比：{},{}".format(o_count, n_count))
        try:
            # 断言分表前后count总数是否一致
            self.assertEqual(
                o_count, n_count, "user_oral_practice_dup分表{}前后user_id:{}数据有丢失!!!".format(db_no, user_id))
        except:
            with open("error_data.txt", 'a+') as pf:
                pf.write("\n用户：{},user_oral_practice_dup原数据：{},分表后user_oral_practice_{},数据：{}  \n".format(
                    user_id, o_count, db_no, n_count))
                is_empty = self.do_mysql(
                    "select count(1) as o_count from user_oral_practice_dup where user_id={} and oral_topic_id !=''".format(user_id))
                pf.write(
                    "排除原数据是否有空oral_topic_id后的总数：{} \n".format(is_empty.get('o_count')))
            raise

    def test_user_words(self):
        '''用户练习表:user_words'''
        # 校验每次随机的userId，分表后的该userId所拥有的数据是否一致
        user_id = self.wd_res.get('user_id')
        # int转换user_id%64取模
        db_no = int(user_id) % 64
        # 查询分表前用户数据count总数
        o_sql = "select count(1) as o_count from user_dup_words where user_id={}".format(
            user_id)
        o_res = self.do_mysql(o_sql)
        o_count = o_res.get('o_count')

        # 查询分表后用户数据count总数
        n_sql = "select count(1) as n_count from user_words_{} where user_id={}".format(
            db_no, user_id)
        n_res = self.do_mysql(n_sql)
        n_count = n_res.get('n_count')

#         print("分表前后数据对比：{},{}".format(o_count, n_count))
        # 断言分表前后count总数是否一致
        try:
            self.assertEqual(
                o_count, n_count, "user_words分表{}前后user_id:{}数据有丢失!!!".format(db_no, user_id))
        except:
            with open("error_data.txt", 'a+') as pf:
                pf.write("用户：{},user_dup_words原数据：{},分表后user_words_{},数据：{}".format(
                    user_id, o_count, db_no, n_count))
            raise

    def test_user_oral_practice_dup(self):
        '''用户练习表:user_oral_practice_dup'''
        # 校验每次随机的userId，分表后的该userId所拥有的数据是否一致
        oral_topic_id = self.topic_res.get('oral_topic_id')
#         user_id = self.topic_res.get('user_id')
        # int转换user_id%64取模
        db_no = int(oral_topic_id) % 64
        # 查询分表前用户数据count总数
        o_sql = "select count(1) as o_count from user_oral_practice_dup where oral_topic_id={}".format(
            oral_topic_id)
        o_res = self.do_mysql(o_sql)
        o_count = o_res.get('o_count')

        # 查询分表后用户数据count总数
        n_sql = "select count(1) as n_count from user_practice_topic_{} where oral_topic_id={}".format(
            db_no, oral_topic_id,)
        n_res = self.do_mysql(n_sql)
        n_count = n_res.get('n_count')

#         print("分表前后数据对比：{},{}".format(o_count, n_count))
        # 断言分表前后count总数是否一致
        try:
            self.assertEqual(o_count, n_count, "user_oral_practice_dup分表{}前后:oral_topic_id:{},数据有丢失!!!".format(
                db_no, oral_topic_id))
        except:
            with open("error_data.txt", 'a+') as pf:
                pf.write("topic_id:{} ,user_practice_topic_dup原数据：{},分表后user_practice_topic_{},数据：{}\n".format(
                    oral_topic_id, o_count, db_no, n_count))
            raise

    @classmethod
    def tearDownClass(cls):
        #         cls.do_http.close()
        # 关闭数据库操作
        cls.do_mysql.mysql_close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
