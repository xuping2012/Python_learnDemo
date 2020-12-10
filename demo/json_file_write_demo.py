#-*- coding:utf-8 -*-

import json

import path_config


if __name__ == "__main__":
    print("python 写json串实例")

    data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]

    fp = open(path_config.data_path + 'json_write.json', 'w')

    # 以可读性格式写入json_write.json文件中
    json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))

    fp.close()
