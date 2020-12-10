'''
Created on 2020年6月5日

@author: qguan
'''


def bubblue(list_num, n):
    for i in range(1, len(list_num)):  # 外层循环控制当前list长度的次数
        isPer = False
        for j in range(len(list_num) - i):  # 内循环是控制前面的元素和剩余的元素进行比较
            if list_num[j] > list_num[j + 1]:  # 如果前面的值比后面的大，就往后移动
                list_num[j], list_num[j + 1] = list_num[j + 1], list_num[j]
                isPer = True
        if not isPer:
            return list_num[len(list_num) - n]
        print("第{}次选择排序最后list结果:{}".format(i, list_num))


print(bubblue([1, 9, 5, 4, 3, 6, 7], 4))