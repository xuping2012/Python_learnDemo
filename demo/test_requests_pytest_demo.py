#-*- coding:utf-8 -*-

__author__ = "苦叶子"

import pytest

# 测试加减法


class TestDemo:
    # 加法

    @pytest.mark.parametrize("a, b, expected",
                             [(1, 2, 3), (2, 3, 5), (3, 4, 8)])
    def test_add(self, a, b, expected):
        # 求和
        s = a + b

        # 断言
        assert s == expected

    # 减法
    @pytest.mark.parametrize("a, b, expected",
                             [(1, 2, -1), (8, 3, 5), (3, 4, 8)])
    def test_sub(self, a, b, expected):
        # 减法
        s = a - b

        # 断言
        assert s == expected

if __name__ == '__main__':
    pytest.main()
