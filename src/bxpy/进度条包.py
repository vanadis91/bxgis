# -*- coding: utf-8 -*-

# import inspect
# import random
# import re
# import time
from bxpy.基本对象包 import 模块加载

模块加载("tqdm")
from tqdm import tqdm


class 进度条类:
    @staticmethod
    def 进度条创建(*args, 总进度=None, 前置信息="", 后置信息={}, 格式设置="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining},{rate_fmt}{postfix}]", 初始进度=0, 步长=None, 进度条结束后保留=True, 位置固定=None, 单位="it", **kwargs):
        # 在异步环境下，当多个进度条同时进行更新时，可能会导致进度条的显示出现多行的情况。这是因为异步任务的执行是并行的，多个任务同时更新进度条可能会导致输出混乱。position 参数可以指定进度条在终端中的位置。你可以在创建进度条时指定不同的 position 值，以确保进度条在终端中的固定位置显示。
        return tqdm(*args, total=总进度, desc=前置信息, postfix=后置信息, bar_format=格式设置, initial=初始进度, miniters=步长, leave=进度条结束后保留, position=位置固定, unit=单位, **kwargs)

    @staticmethod
    def 更新(进度条: tqdm, value):
        进度条.update(value)

    @staticmethod
    def 清除(进度条: tqdm):
        进度条.clear()

    @staticmethod
    def 关闭(进度条: tqdm):
        进度条.close()

    @staticmethod
    def 前置信息设置(进度条: tqdm, str):
        进度条.set_description(str)

    @staticmethod
    def 后置信息设置(进度条: tqdm, dict):
        进度条.set_postfix(dict)


if __name__ == "__main__":
    import time

    a = 进度条类.进度条创建(range(10), 前置信息="开始测算地块信息", 后置信息={"1": "1"}, 进度条结束后保留=True)
    for i in a:
        # a.close()
        time.sleep(1)

        # pbar.更新(10)

    # 啊啊啊 = "123"
    # print(变量名(啊啊啊))
    # print(time.time())
    # aa = [[[1, 2], [2, 3]], [[2, 3], [3, 4]]]
    # bb = 递归操作列表(lambda x1: x1 + 1, aa)
    # 打印详情(bb)
    # 啊啊 = ["啊啊啊", "不不不"]
    # 变量值替换(啊啊, ["啊啊啊", "不不不"], ["aaa", "bbb"])
    # # aa = open(r"C:\Users\Beixiao\Desktop\temp1.txt", "w")
    # 打印详情(啊啊)
    # print(type(aa))
    # aa.close()
    # print('a')
    # aa = r'anastassia,bandannas'
    # aa.分割成表(',')
    # a = [1, 2, 3]
    # b = [4, 5, 6]
    # c = 打包(a, b)
    # print(*c)
    # 输出.打印详情([])
    # print('Hello, world!')
    pass
