'''
# -*- encoding=utf-8 -*-
Created on 2020年6月1日上午11:07:24
@author: qguan
@file:utils.HandleMySQL.py

'''
import pymysql
from utils.HandleConfig import INIParser
import path_config

# mysql_info = {"host": '47.107.254.16',
#               "port": 3306,
#               "user": 'root',
#               "passwd": 'Hcp_dev_0326',
#               "db": 'hcp_study_abroad_data',
#               "charset": 'utf8'}


class HandleMySQL(object):
    '''
    classdocs
    '''

    conf = INIParser(path=path_config.prop_path + "mysql.ini")

    def __init__(self):
        '''
        初始化mysql数据库信息，创建连接游标
        '''

#         self.db_info = mysql_info
        try:
            self.conn = pymysql.connect(host=self.conf.get_string('mysql', 'host'),
                                        port=self.conf.get_int(
                                            'mysql', 'port'),
                                        user=self.conf.get_string(
                                            'mysql', 'user'),
                                        passwd=self.conf.get_string(
                                            'mysql', 'password'),
                                        db=self.conf.get_string('mysql', 'db'),
                                        charset=self.conf.get_string(
                                            'mysql', 'charset'),
                                        cursorclass=pymysql.cursors.DictCursor)
#             self.logger.info("success!")
        except Exception as a:
            #             self.logger.info("failture:%s" % a)
            raise a
        else:
            #             self.logger.info("create cursor!")
            self.cursor = self.conn.cursor()

    def __call__(self, sql, arg=None, is_more=False):
        '''
                        调用数据库执行方法
        :param sql:执行的sql语句，str类型
        :param arg:参数必须是序列类型：list、str、tuple
        :param is_more:是否查询显示更多数据，通常根据sql的limit来确定
        :return:
        '''
        self.mysql_execute(sql, arg)
        if is_more:
            result = self.cursor.fetchall()

        else:
            result = self.cursor.fetchone()
#         不合适，如果还有sql在循环执行，在这里关闭，会造成sql执行失败
#         self.mysql_close()
        return result

    def mysql_execute(self, sql, arg=None):
        '''
                       封装自己执行sql语句的方法
        '''
        try:
            self.cursor.execute(sql)
        except Exception as a:
            self.conn.rollback()  # sql回滚处理
#             self.logger.info("回滚sql,异常如下：{}".format(a))
            raise a
        else:
            self.conn.commit()  # sql提交

    def mysql_getrows(self, sql):
        '''
                      返回查询结果集
        :return: 返回的是一个嵌套字典的元组      
        '''
        try:
            self.cursor.execute(sql)  # arg必须是序列类型
        except Exception as a:
            #             self.logger.info("执行SQL语句出现异常：%s" % a)
            raise a  # 直接抛出异常，不在执行后面的语句
        else:
            rows = self.cursor.fetchall()
            return rows

    def mysql_getrow(self, sql):
        '''
                    返回查询结果集
        return:结果是个字典
        '''
        try:
            self.cursor.execute(sql)  # arg必须是序列类型
        except Exception as a:
            #             self.logger.info("执行SQL语句出现异常：%s" % a)
            raise a
        else:
            row = self.cursor.fetchone()
            return row

    def mysql_close(self):
        '''
        关闭数据库连接，关闭游标
        '''
        try:
            self.conn.close()
            self.cursor.close()
#             self.logger.info("正常关闭mysql连接！")
        except Exception as a:
            #             self.logger.info("关闭mysql连接池失败，异常如下：{}".format(a))
            raise a

if __name__ == '__main__':
    do_mysql = HandleMySQL()
    sql = "select user_id from user_info where mobile='13266515340'"
    res = do_mysql(sql)
    print(res.get('user_id'))
    pass
