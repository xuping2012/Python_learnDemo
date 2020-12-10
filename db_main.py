'''
Created on 2020年6月2日

@author: qguan
'''
import unittest

import path_config


def load_db_test():

    suite = unittest.defaultTestLoader.discover(
        path_config.basepath + '\\testcases', pattern="test_practies_db.py")
    lastall = unittest.TestSuite()
    lastall.addTest(suite)
    return lastall

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #     unittest.main()
    #     unittest.TextTestRunner().run(load_db_test())
    #     print(1513505 % 64)

    print(10 % 64)
