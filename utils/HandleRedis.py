'''
# -*- encoding=utf-8 -*-
Created on 2020年6月4日上午11:37:49
@author: qguan
@file:utils.HandleRedis.py

'''
import redis
from utils.HandleConfig import INIParser
import path_config


class HandleRedis(object):
    '''
    classdocs
    '''
    conf = INIParser(path_config.prop_path + 'mysql.ini')

    def __init__(self, db_no):
        '''
        Constructor
        '''
        self.r = redis.StrictRedis(
            host=self.conf.get_string('redis', 'host'), port=self.conf.get_int('redis', 'port'), db=9, password=self.conf.get_string('redis', 'passwd'), decode_responses=True)

    def get_value_by_key(self, key):
        return self.r.get(key)

    def set_key_value(self, key, value):
        self.r.set(key, value)

    def del_key(self, key):
        self.r.delete(key)

if __name__ == '__main__':

    pass
