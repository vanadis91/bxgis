import pandas
from bxpandas.配置 import 配置
from typing import Literal


class 序列类:
    # 继承Series。创建pandas中的Series类的实例，即带有索引的一维数组。
    @staticmethod
    def 数据序列创建_通过列表(数据, 索引=None, 元素类型=None, 名称=None, 复制=False, fastpath=False):
        temp = pandas.Series(data=数据, index=索引, dtype=元素类型, name=名称, copy=复制, fastpath=fastpath)  # type: ignore
        return temp

    @staticmethod
    def 数据序列创建_通过复制(x):
        return x.copy()

    @staticmethod
    def 标签列表获取(x):
        # 和self.嵌入对象Series.keys()作用一样
        return x.index

    @staticmethod
    def 标签列表设置(x, 索引列表):
        x.index = 索引列表
        return x

    @staticmethod
    def 标签获取_通过元素值(x: pandas.Series, 标签):
        return x.index[标签]

    @staticmethod
    def 所有元素值获取(x):
        return x.values

    @staticmethod
    def 所有元素值设置(x, 值):
        x.values = 值
        return x

    @staticmethod
    def 元素类型获取(x):
        return x.dtype

    @staticmethod
    def 统计_中位数(x):
        return x.median()

    @staticmethod
    def 统计_最大值(x):
        return x.max()

    @staticmethod
    def 统计_平均值(x):
        return x.mean()

    @staticmethod
    def 元素_删除(x, 标签列表, 轴=0, 索引=None, 标题=None, 修改源=False):
        ret = x.drop(labels=标签列表, axis=轴, index=索引, columns=标题, inplace=修改源)
        return ret

    @staticmethod
    def 元素_删除_空值(x, 修改源=False):
        ret = x.dropna(inplace=修改源)
        return ret

    @staticmethod
    def 元素_填充_空值(x, 值, 修改源=False, 填充方式="上值填充"):
        填充方式 = 配置.空值填充映射[填充方式]
        ret = x.fillna(值, inplace=修改源, method=填充方式)
        return ret

    @staticmethod
    def 元素_是否为空(x, 取反=False):
        if 取反:
            ret = x.notnull()
        else:
            ret = x.isnull()
        return ret

    # def 元素_批量操作(self):
    #     return _元素批量操作(self.嵌入对象Series.str)

    @staticmethod
    def 切片_按标签(x: pandas.Series, va):
        lst = []
        for n in va:
            if type(n) == tuple:
                if type(n[0]) == int:
                    lst.extend(list(range(*n)))
                if type(n[0]) == str:
                    nn0 = list(序列类.标签列表获取(x)).index(n[0])
                    nn1 = list(序列类.标签列表获取(x)).index(n[1]) + 1
                    if len(n) == 3:
                        nn3 = n[2]
                    else:
                        nn3 = 1
                    lst.extend(list(range(nn0, nn1, nn3)))
            else:
                if type(n[0]) == int:
                    lst.append(n)
                if type(n[0]) == str:
                    n = list(序列类.标签列表获取(x)).index(n)
                    lst.append(n)
        ret = x[lst]
        return ret

    @staticmethod
    def 切片_按元素值(x: pandas.Series, va):
        aaxxx = x[va]
        return aaxxx


if __name__ == "__main__":
    se = 序列类.数据序列创建_通过列表(["aa", "bb", "cc"])
    序列类.标签列表设置(se, [3, 4, 5])
    print(list(序列类.标签列表获取(se)))
