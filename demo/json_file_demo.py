#-*- coding:utf-8 -*-
import path_config

import json

if __name__ == "__main__":
    print("python 读取json内容文件转化python对象实例")

    fp = open(path_config.data_path + 'json_data.json', 'r')

    json_data = json.load(fp)
    print(type(json_data))
    print(json_data)

    fp.close()
