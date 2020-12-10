'''
Created on 2020年4月17日

@author: qguan
'''
from testcases import test_unittest

if __name__ == '__main__':
    # 测试加载器  loader
    import unittest
    loader = unittest.TestLoader()
    loader.loadTestsFromModule(test_unittest)
    suite = unittest.TestSuite()
    suite.addTest(loader)

    with open("./reports/test.html", "w") as pf:
        pass

    # 测试套件 suite
    # 测试环境管理：fixtrue
    pass

# import pytest
# import time
# tisrt = str(int(time.time()))
# print(tisrt)
# pytest.main(
#     ['-s', './testcases/', '--html=./reports/report_{}.html'.format(tisrt)])
