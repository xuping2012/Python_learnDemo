'''
Created on 2020年6月1日

@author: qguan
'''
import random
import unittest

import path_config
from utils.HandleConfig import INIParser
from utils.HandleMySQL import HandleMySQL
from utils.HandleRequests import HandleRequests


def test():
    return False


class Test(unittest.TestCase):

    # 初始化http请求、mysql操作对象
    do_http = HandleRequests()
    do_mysql = HandleMySQL()
    conf = INIParser(path=path_config.prop_path + 'mysql.ini')

    @classmethod
    def setUpClass(cls):
        # 查询正常可登录的普通用户，rand()数据库随机函数，返回一个limit 1
        sql = "select mobile,raw_password,c.subtask_id from user_info a,(select user_id FROM user_oral_practice  GROUP BY user_id HAVING count(user_id)>2 limit 1000) b,(SELECT  subtask_id from hcp_question_bank_data.question_bank_subtask  WHERE  task_id IN (SELECT DISTINCT task_id from user_exercises where create_date > '2020-02-01 00:00:00') LIMIT 500) c where vip_status=1 and allow_login=1 and status=0  and zone=86 and a.user_id=b.user_id ORDER BY RAND() LIMIT 1"
        cls.db_res = cls.do_mysql(sql)
        # 登录接口及请求参数
        login_url = '{}/hcp/apiLogin/passwordLogin'.format(
            cls.conf.get_string('mysql', 'addr'))
        login_data = {
            "verifyCode": "",
            "zone": "86",
                    "loginType": 0,
                    "password": cls.db_res.get('raw_password'),
                    "deviceType": "ios",
                    "pushToken": "dea9b867c475831cf55d3e1318d478b9",
                    "channel": 0,
                    "deviceName": "iPhone 8 Plus",
                    "deviceid": "4F673A5F-BA15-47B9-B9A0-AF43F1DBF990",
                    "mobile": cls.db_res.get('mobile')
        }
        # 发送http请求，封装的请求已经返回json格式
        cls.res = cls.do_http("post", login_url, data=login_data, is_json=True)
        # 没有使用jsonpath提取dict参数，已知接口返回json，使用dict的get方法
        try:  # 这里处理登录用户信息有时登录失败，可能区号不正确
            cls.token = cls.res.get('content').get('token')
            cls.userId = cls.res.get('content').get('userId')
            cls.sub_tasks_id = cls.db_res.get('subtask_id')

        except:
            print(login_data)
            raise
        else:
            # 用户联系记录分表，%64取模分64张表
            cls.db_no = int(cls.userId) % 64
            # 构造下一个接口的请求头：加入token认证信息
            cls.headers = {
                "source": "0", "Authorization": "Bearer {}".format(cls.token)}
        cls.host = cls.conf.get_string('mysql', 'addr')

    @unittest.skipIf(test(), "test")
    def test_study_hard(self):
        # 学勤排行榜接口地址
        url = "{}/hcp/studyCenter/oralPractice/getStudyHardRankingList?rankingType=2".format(
            self.host)
        # 发起http请求
        res = self.do_http("get", url, headers=self.headers)
        # 提取该登录用户联系stars信息：获赞星星总数
        res_stars = res.get('content').get('studyRankingVO').get('stars')

        # 先查一次分表前的数据
        o_sql = "select sum(show_stars) as stars FROM user_oral_practice  WHERE create_date > '2020-03-01 00:00:00' AND create_date < '2020-06-01 00:00:00' AND status = 0 AND user_id = {}".format(
            self.userId)
        # 执行sql
        db_o_res = self.do_mysql(o_sql)
        # 提取数据库查询结果
        db_o_stars = db_o_res.get('stars')

        # 再根据用户id%64取模后查库，统计用户获赞星星总数
        n_sql = "select sum(show_stars) as stars FROM user_oral_practice_{}  WHERE create_date > '2020-03-01 00:00:00' AND create_date < '2020-06-01 00:00:00' AND status = 0 AND user_id = {}".format(
            self.db_no, self.userId)
        # 执行sql
        db_n_res = self.do_mysql(n_sql)
        # 提取数据库查询结果
        db_n_stars = db_n_res.get('stars')
        # mysql查询结果为空null,不处理:<class 'decimal.Decimal'>
        if db_n_stars == None:  # and not isinstance(db_stars, int)
            db_stars = 0

        # 先断言接口返回的数据是否与数据库一致
        self.assertEqual(res_stars, db_stars, "接口响应数据与数据库断言失败!!!")
        # 再断言分表前后数据是否一致
        self.assertEqual(db_o_stars, db_n_stars, "练习分表前后数据不一致!!!")

    @unittest.skipIf(test(), "test")
    def test_study_overlord(self):
        # 学霸排行榜接口地址
        url = "{}/hcp/studyCenter/oralPractice/getStudyOverlordRankingList?rankingType=2".format(
            self.host)
        # 发起http请求
        res = self.do_http("get", url, headers=self.headers)
        # 提取该登录用户联系stars信息：获赞星星总数
        res_stars = res.get('content').get('studyRankingVO').get('stars')

        # 先查一次分表前的数据
        o_sql = "select sum(show_stars) as stars FROM user_oral_practice  WHERE create_date > '2020-03-01 00:00:00' AND create_date < '2020-06-01 00:00:00' AND status = 0 AND user_id = {}".format(
            self.userId)
        # 执行sql
        db_o_res = self.do_mysql(o_sql)
        # 提取数据库查询结果
        db_o_stars = db_o_res.get('stars')

        # 再根据用户id%64取模后查库，统计用户获赞星星总数
        n_sql = "select sum(show_stars) as stars FROM user_oral_practice_{}  WHERE create_date > '2020-03-01 00:00:00' AND create_date < '2020-06-01 00:00:00' AND status = 0 AND user_id = {}".format(
            self.db_no, self.userId)
        # 执行sql
        db_n_res = self.do_mysql(n_sql)
        # 提取数据库查询结果
        db_n_stars = db_n_res.get('stars')
        # mysql查询结果为空null,不处理:<class 'decimal.Decimal'>
        if db_n_stars == None:  # and not isinstance(db_stars, int)
            db_stars = 0

        # 先断言接口返回的数据是否与数据库一致
        self.assertEqual(res_stars, db_stars, "接口响应数据与数据库断言失败!!!")
        # 再断言分表前后数据是否一致
        self.assertEqual(db_o_stars, db_n_stars, "练习分表前后数据不一致!!!")

#     @unittest.skip("执行效率太低，不利于调试")
    def test_practice_home(self):
        # 练习：四大模块的已练习数据接口
        url = '{}/hcp/qsBank/practiceHome/newHome?Listening=0&Oral=0&Reading=0&Writing=0'.format(
            self.host)

        res = self.do_http('get', url, headers=self.headers)
        module = res.get('content')

        lis_ele = []
        for ele in module:
            dic_ele = {}
            if ele.get('count'):
                dic_ele['exercise_part'] = ele.get('type')
                dic_ele['count'] = ele.get('count')
                lis_ele.append(dic_ele)

        o_sql = "select exercise_part, count(distinct(subject_id)) as count  from user_exercises  where user_id = {} and exercise_module = 0  GROUP BY exercise_part".format(
            self.userId)
        o_res = self.do_mysql(o_sql, is_more=True)

        n_sql = "select exercise_part, count(distinct(subject_id)) as count  from user_exercises_{}  where user_id = {} and exercise_module = 0  GROUP BY exercise_part".format(
            self.db_no, self.userId)
        n_res = self.do_mysql(n_sql, is_more=True)

        pracites_type = {1: "listening", 2: "Oral", 3: "reading", 4: "writing"}

        for i in range(len(o_res)):
            exc_part1 = o_res[i].get('exercise_part')
            exc_part2 = n_res[i].get('exercise_part')
            if exc_part1 == exc_part2:
                count = lis_ele[i].get('count')
                count1 = o_res[i].get('count')
                count2 = n_res[i].get('count')
                self.assertEqual(count, count2, "接口返回数据不一致!!!")
                self.assertEqual(
                    count1, count2, "练习类型：{},分表前后数据不一致!!!".format(pracites_type.get(exc_part1)))

    @unittest.skipIf(test(), "test")
    def test_task_words(self):
        # 测试会员列表:单词，前提是有效期的会员，在前置条件中setup筛选
        url = "{}/hcp/studyCenter/studyLog/wordTaskDetailList".format(
            self.host)
        task_data = {"taskId": self.sub_tasks_id, "taskType": 5}
        res = self.do_http('get', url, data=task_data, headers=self.headers)
        print("单词结果：{}".format(res))
#         o_sql = ""
#         单词练习分掌握/生词
#         n_sql = "select count(1) from user_words_33 where user_id= 1535505 and status=0 and task_id=1052"
#         n_sql = "select count(1) from user_words_33 where user_id= 1535505 and status=1 and task_id=1052"
#         o_res = self.do_mysql(o_sql)
#         n_res = self.do_mysql(n_sql)

    @unittest.skipIf(test(), "test")
    def test_task_passages(self):
        # 测试会员列表:单词，前提是有效期的会员，在前置条件中setup筛选
        url = "{}/hcp/studyCenter/studyLog/passagesTaskDetailList?taskId={}&taskType=3".format(
            self.host, self.sub_tasks_id)
        task_data = {"taskId": self.sub_tasks_id, "taskType": 5}
        res = self.do_http('get', url, data=task_data, headers=self.headers)
        print("阅读结果：{}".format(res))
#         o_sql = ""
#         n_sql = "select exer_id as exerId,  catalog as catalog, exercise_module as exerciseModule, exercise_part as exercisePart, subject_id as subjectId, question_id as questionId, score as score, score_detail as scoreDetail, status as status, time_spend as timeSpend, question_number as questionNumber, correct_anwser_number as correctAnwserNumber, started_date as startedDate, finished_date as finishedDate, user_id as userId, user_name as userName, update_id as updateId, update_name as updateName, create_date as createDate, update_date as updateDate,  task_id as taskId, part as part, paper_id as paperId, paper_type as paperType, paper_name as paperName, topic_id as topicId, question_type as questionType, channel_from as channelFrom  from user_exercises_33 where task_id = 1052 and subject_id in (  206   ) and user_id = 1513505 and catalog = 0 and exercise_module = 1 and exercise_part = 3"
#         o_res = self.do_mysql(o_sql)
#         n_res = self.do_mysql(n_sql)

    @unittest.skipIf(test(), "test")
    def test_task_listening(self):
        # 测试会员列表:单词，前提是有效期的会员，在前置条件中setup筛选
        url = "{}/hcp/studyCenter/studyLog/listeningTaskDetailList?taskId={}&taskType=1".format(
            self.host, self.sub_tasks_id)
        task_data = {"taskId": self.sub_tasks_id, "taskType": 5}
        res = self.do_http('get', url, data=task_data, headers=self.headers)
        print("听力结果：{}".format(res))
#         o_sql = ""
#         n_sql = "select exer_id as exerId,  catalog as catalog, exercise_module as exerciseModule, exercise_part as exercisePart, subject_id as subjectId, question_id as questionId, score as score, score_detail as scoreDetail, status as status, time_spend as timeSpend, question_number as questionNumber, correct_anwser_number as correctAnwserNumber, started_date as startedDate, finished_date as finishedDate, user_id as userId, user_name as userName, update_id as updateId, update_name as updateName, create_date as createDate, update_date as updateDate,  task_id as taskId, part as part, paper_id as paperId, paper_type as paperType, paper_name as paperName, topic_id as topicId, question_type as questionType, channel_from as channelFrom  from user_exercises_33 where task_id = 1052 and subject_id in (  206   ) and user_id = 1513505 and catalog = 0 and exercise_module = 1 and exercise_part = 1"
#         o_res = self.do_mysql(o_sql)
#         n_res = self.do_mysql(n_sql)

    @unittest.skipIf(test(), "test")
    def test_task_oral_task_detail(self):
        # 测试会员列表:单词，前提是有效期的会员，在前置条件中setup筛选
        url = "{}/hcp/studyCenter/studyLog/oralTaskDetailList?taskId={}&taskType=2".format(
            self.host, self.sub_tasks_id)
        task_data = {"taskId": self.sub_tasks_id, "taskType": 5}
        res = self.do_http('get', url, data=task_data, headers=self.headers)
        print("口语结果：{}".format(res))
#         o_sql = ""
#         n_sql = "select count(1) from user_practice_topic_{}  WHERE  oral_topic_id = ?".format(db_no)
#         o_res = self.do_mysql(o_sql)
#         n_res = self.do_mysql(n_sql)

    @unittest.skipIf(test(), "test")
    def test_oral_memory_detail(self):
        list_url = "{}/hcp/base/oralMemory/oralMemoryList".format(self.host)
        list_data = {"curPage": 1}
        lis_res = self.do_http(
            'post', list_url, data=list_data, headers=self.headers, is_json=True)
        oralMemoryId = lis_res.get('content').get(
            'list')[0].get('oralMemoryId')

        detail_url = "{}/hcp/base/oralMemory/{}".format(
            self.host, oralMemoryId)
        detail_res = self.do_http('get', detail_url, headers=self.headers)

        part1_list = detail_res.get('content').get('part1Orals')
#         part23_list = detail_res.get('content').get('part23Orals')
        if part1_list:
            for part1 in part1_list:
                topic_id = part1.get('topId')
                orals = part1.get('orals')
                if orals:
                    oral_list = []
                    for oral in orals:
                        oral_list.append(oral)
                    db_no = int(topic_id) % 64
                    n_sql = "select   oral_practice_id as oralPracticeId from user_practice_topic_{} where oral_topic_id = {}    and oral_part = 1 and if_private = 1 order by show_stars desc limit 3".format(
                        db_no, topic_id)
                    n_res = self.do_mysql(n_sql)
                    print(n_res)
#                     self.assertEqual(bool(orals), bool(n_res), "话题推荐录音数据有误")
                else:
                    db_no = int(topic_id) % 64
                    n_sql = "select   oral_practice_id as oralPracticeId from user_practice_topic_{} where oral_topic_id = {}    and oral_part = 1 and if_private = 1 order by show_stars desc limit 3".format(
                        db_no, topic_id)
                    n_res = self.do_mysql(n_sql)
#                     print("orals结果都是[]:{},{},比较两个值的bool类型".format(orals, n_res))
                    self.assertEqual(bool(orals), bool(n_res), "话题推荐录音数据有误")

    @unittest.skipIf(test(), "test")
    def test_practice_write_page(self):
        '''练习tab-写作，查看范文'''
        # 获取写作主题字典
#         write_topic_url = "{}/hcp/base/base/dict/WritingTopic2".format(
#             self.host)
#         topic_res = self.do_http('get', write_topic_url, headers=self.headers)
#
#         # 获取主题范文列表:如果硬编码，那么上面的接口就不必请求
#         url = "{}/hcp/qsBank/writings/list?topicId=77&writingPart=2".format(
#             self.host)
#         lis_res = self.do_http('get', url, headers=self.headers)
#         # 提取范文id
#         subject_id = lis_res.get('content').get(
#             'data')[1].get('subjectId')
#
#         # 查看范文：还是硬编码，上面也不要请求
#         detail_url = "{}/hcp/qsBank/writings/174".format(
#             self.host, subject_id)
#         detail_res = self.do_http('get', detail_url, headers=self.headers)

        # 接口请求前 写入旧表总数
        oo_sql = "SELECT COUNT(1) as sum from user_dup_exercises  WHERE user_id={} AND subject_id=174".format(
            self.userId)
        oo_res = self.do_mysql(oo_sql)
        oo_sum = oo_res.get('sum')

        # 接口请求前 写入分表总数
        o_sql = "SELECT COUNT(1) as sum from user_exercises_{}  WHERE user_id={} AND subject_id=174".format(
            self.db_no, self.userId)
        o_res = self.do_mysql(o_sql)
        o_sum = o_res.get('sum')

        # 查看范文 保存用户练习记录数据:如果硬编码，上面的一系列接口都不需要请求
        save_url = "{}/hcp/studyCenter/exercises/save".format(self.host)
        save_data = {
            "subjectId": "174",
            "exerciseModule": 0,
            "exercisePart": 4
        }

        self.do_http(
            'post', save_url, data=save_data, headers=self.headers, is_json=True)

        # 接口请求后 写入旧表总数
        nn_sql = "SELECT COUNT(1) as sum from user_dup_exercises  WHERE user_id={} AND subject_id=174".format(
            self.userId)
        nn_res = self.do_mysql(nn_sql)
        nn_sum = nn_res.get('sum')

        # 接口请求后 写入分表总数
        n_sql = "SELECT COUNT(1) as sum from user_exercises_{}  WHERE user_id={} AND subject_id=174".format(
            self.db_no, self.userId)
        n_res = self.do_mysql(n_sql)
        n_sum = n_res.get('sum')

        # 保存数据后，count总数会加①
        oo_sum += 1
        o_sum += 1
        self.assertEqual(n_sum, nn_sum, "新旧表同时写入数据+1")
        self.assertEqual(oo_sum, nn_sum, "旧表前后写入数据对比错误")
        self.assertEqual(o_sum, n_sum, "分表前后写入数据对比错误")

    @unittest.skipIf(test(), "test")
    def test_practice_oral(self):
        '''练习tab-口语，发布语音'''
        # 获取口语话题id
        oral_lis_url = "{}/hcp/qsBank/oralTopic/list?oralTopCatalog=4&part=0".format(
            self.host)
        oral_res = self.do_http('get', oral_lis_url, headers=self.headers)
        oral_topic_id = oral_res.get(
            'content')[random.randint(0, len(oral_res.get('content')) - 1)].get('oralTopicId')

        # 获取口语话题id下的问题
        question_url = "{}/hcp/qsBank/oralTopic/show?oralTopicId={}&part=0&type=all".format(
            self.host, oral_topic_id)
        q_res = self.do_http('get', question_url, headers=self.headers)
        question_id = q_res.get(
            'content')[random.randint(0, len(q_res.get('content')) - 1)].get('oralQuestionId')

#         print(self.userId, question_id, oral_topic_id)
        # 接口请求前 写入旧表总数
        oo_sql = "SELECT COUNT(1) as  sum from user_oral_practice_dup WHERE user_id={} AND oral_topic_id={} AND oral_question_id={}".format(
            self.userId, oral_topic_id, question_id)
        oo_res = self.do_mysql(oo_sql)
        oo_sum = oo_res.get('sum')

        if not oo_sum:
            oo_sum = 0
        # 接口请求前 写入分表总数
        o_sql = "SELECT COUNT(1) as sum from user_oral_practice_{} WHERE user_id={} AND oral_topic_id={} AND oral_question_id={}".format(
            self.db_no, self.userId, oral_topic_id, question_id)
        o_res = self.do_mysql(o_sql)
        o_sum = o_res.get('sum')

        if not o_sum:
            o_sum = 0
        # 查看范文 保存用户练习记录数据:硬编码，上面的一系列接口都不需要请求
        save_url = "{}/hcp/studyCenter/oralPractice/save".format(self.host)
        save_data = {
            "oralTopCatalog": 4,
            "oralQuestion": "Do you prefer natural parks or amusement parks?",
            "ifPrivate": 1,
            "oralQuestionId": question_id,
            "oralPart": 1,
            "oralUrl": "1591155416556.mp3",
            "seconds": 11,
            "oralTopicId": oral_topic_id,
            "topic": "Park",
            "source": 0
        }
        self.do_http(
            'post', save_url, data=save_data, headers=self.headers, is_json=True)

        # 接口请求后 写入旧表总数
        nn_sql = "SELECT COUNT(1) as sum from user_oral_practice_dup WHERE user_id={} AND oral_topic_id={} AND oral_question_id={}".format(
            self.userId, oral_topic_id, question_id)
        nn_res = self.do_mysql(nn_sql)
        nn_sum = nn_res.get('sum')

        # 接口请求后 写入分表总数
        n_sql = "SELECT COUNT(1) as sum from user_oral_practice_{} WHERE user_id={} AND oral_topic_id={} AND oral_question_id={}".format(
            self.db_no, self.userId, oral_topic_id, question_id)
        n_res = self.do_mysql(n_sql)
        n_sum = n_res.get('sum')

        # 保存数据成功后，count总数会加①
        oo_sum += 1
        o_sum += 1

        # 断言新旧表写入数据前后
        self.assertEqual(n_sum, nn_sum, "新旧表同时写入数据+1")
        self.assertEqual(oo_sum, nn_sum, "旧表前后写入数据对比错误")
        self.assertEqual(o_sum, n_sum, "分表前后写入数据对比错误")

    def test_listening_topic_list(self):
        """这是检查/hcp/qsBank/listening/list?topicId=93&type=topic接口获取话题：讨论列表的数据"""
        o_sql = "select sum(question_number) as count from user_exercises  where exercise_module = 0 AND subject_id in (66, 131, 135, 7, 74, 11, 78, 15, 82, 147, 86, 24, 155, 28, 159, 95, 32, 99, 163, 36, 103, 40, 171, 107, 44, 111, 48, 115, 52, 119, 58, 62)            and user_id ={}  and exercise_part =1 and exer_id in (62826218, 62318038, 62911303, 62826325, 62826338, 62826308, 62826139, 62826165, 62761809, 62826314, 62430948, 62761873, 474897558503141376, 62761968, 62430973, 62911304, 62431771, 62318048, 62761402, 62761404, 62430994, 62760903, 62431775, 62437732, 62762240, 62431046, 62318021, 62911307, 62830826, 62761023, 62431772, 62317983, 62801202, 62430916, 62766062, 40075359, 41147404, 41147398, 62911294, 38832519, 62437785, 62437797, 62437809, 51825280, 62437793, 62437789, 40075361, 62437774, 62761203, 62437773, 62437799, 62437701, 51519167, 62437720, 57763539, 53996519, 474890560822816768, 62431439, 62431367, 62431436, 62431417, 474903707285696513, 62437765, 62431138, 62431221, 62431253, 62431290, 62431327)".format(
            self.userId)
        n_sql = "select sum(question_number) as count from user_exercises_{}  where exercise_module = 0 AND subject_id in (66, 131, 135, 7, 74, 11, 78, 15, 82, 147, 86, 24, 155, 28, 159, 95, 32, 99, 163, 36, 103, 40, 171, 107, 44, 111, 48, 115, 52, 119, 58, 62)            and user_id ={}  and exercise_part =1 and exer_id in (62826218, 62318038, 62911303, 62826325, 62826338, 62826308, 62826139, 62826165, 62761809, 62826314, 62430948, 62761873, 474897558503141376, 62761968, 62430973, 62911304, 62431771, 62318048, 62761402, 62761404, 62430994, 62760903, 62431775, 62437732, 62762240, 62431046, 62318021, 62911307, 62830826, 62761023, 62431772, 62317983, 62801202, 62430916, 62766062, 40075359, 41147404, 41147398, 62911294, 38832519, 62437785, 62437797, 62437809, 51825280, 62437793, 62437789, 40075361, 62437774, 62761203, 62437773, 62437799, 62437701, 51519167, 62437720, 57763539, 53996519, 474890560822816768, 62431439, 62431367, 62431436, 62431417, 474903707285696513, 62437765, 62431138, 62431221, 62431253, 62431290, 62431327)".format(
            self.db_no, self.userId)

        o_res = self.do_mysql(o_sql)
        n_res = self.do_mysql(n_sql)

        o_count = o_res.get('count')
        n_count = n_res.get('count')

        self.assertEqual(o_count, n_count, "msg")

    @classmethod
    def tearDownClass(cls):
        #         cls.do_http.close()
        # 关闭数据库操作
        cls.do_mysql.mysql_close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
#     msg_data = {"msgtype": "text", "text": {
#         "content": "emergency: <测试一下>Java后台接口异常，@宁立远，查看后台服务<已发邮件通知>error!!!"}}
#     headers = {"content-type": "application/json;charset=utf-8"}
#     dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=7302a79374a1bb507e011f03d1c683adcadcd4a6bdc3a3485f8dd24c8c981a49"
#     requests.post(url=dingding_url, json=msg_data, headers=headers)
