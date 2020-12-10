'''
# -*- encoding=utf-8 -*-
Created on 2020年6月1日上午10:58:37
@author: qguan
@file:utils.HandleRequests.py

'''
import json
import requests


class HandleRequests(object):
    '''
    封装一个公共http请求工具类
    '''

    def __init__(self):
        '''
        构造方法
        '''
        self.session = requests.Session()

    def __call__(self, method, url, data=None, is_json=False, **kwargs):
        '''
        封装一个可以被直接调用的方法
        :param method: 请求方法
        :param url: 请求地址
        :param data: 请求参数
        :param is_json: 是否json格式
        :param kwargs: 占位，可自定义headers
        :return: 返回一个请求结果
        '''

        # 请求方法的参数转成小写，也可以是大写upper()
        method = method.lower()
        # 判断请求参数是否是str类型的json格式
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                self.logger.info("str字符串json数据处理异常:{}".format(e))
                if len(data) > 0:
                    data = eval(data)

        # 请求方法
        if method == 'get':
            res = self.session.request(
                method=method, url=url, params=data, **kwargs)
        elif method == 'post':
            if is_json:
                res = self.session.request(
                    method=method, url=url, json=data, **kwargs)
            else:
                res = self.session.request(
                    method=method, url=url, data=data, **kwargs)
        else:
            self.logger.info("[{}]该请求方法暂不支持。".format(method))

        # session需要关闭资源
        self.session.close()

        return res.json()

    def http_requst(self, method, url, data=None, json=None, **kwargs):
        '''
        封装一个可以被直接调用的方法
        :param method: 请求方法
        :param url: 请求地址
        :param data: 请求参数
        :param is_json: 是否json格式
        :param kwargs: 占位，可自定义headers
        :return: 返回一个请求结果
        '''

        # 请求方法的参数转成小写，也可以是大写upper()
        method = method.lower()
        # 判断请求参数是否是str类型的json格式
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                self.logger.info("str字符串json数据处理异常:{}".format(e))
                if len(data) > 0:
                    data = eval(data)

        # 请求方法
        if method == 'get':
            res = self.session.request(
                method=method, url=url, params=data, **kwargs)
        elif method == 'post':
            res = self.session.request(
                method=method, url=url, data=data, json=data, **kwargs)
        else:
            self.logger.info("[{}]该请求方法暂不支持。".format(method))

        # session需要关闭资源
        self.session.close()

        return res


if __name__ == '__main__':
    pass
