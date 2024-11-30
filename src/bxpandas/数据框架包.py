import pandas
from typing import Literal, Union
from bxpandas.配置 import 枚举_字典结构


class 数据框架类:
    @staticmethod
    def 行标签列表获取(x):
        return x.index

    @staticmethod
    def 行标签列表设置(x, 值):
        x.index = 值
        return x

    @staticmethod
    def 列标签列表获取(x):
        return x.columns

    @staticmethod
    def 列标签列表设置(x, 值):
        x.columns = 值
        return x

    @staticmethod
    def 所有元素值获取(x):
        return x.values

    @staticmethod
    def 所有元素值设置(x, 值):
        x.values = 值
        return x

    @staticmethod
    def 形状获取(x):
        return x.shape

    @staticmethod
    def 维度获取(x):
        return x.ndim

    @staticmethod
    def 数据框架创建_通过列表(数据, 行标签列表=None, 列标签列表=None, 元素类型=None, 复制=False):
        temp = pandas.DataFrame(data=数据, index=行标签列表, columns=列标签列表, dtype=元素类型, copy=复制)
        return temp

    @staticmethod
    def 数据框架创建_通过字典列表(数据):
        temp = pandas.DataFrame(data=数据)
        return temp

    @staticmethod
    def 数据框架创建_通过字典(数据):
        """

        >>> 数据框架创建_通过字典({'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]})
        """
        temp = pandas.DataFrame(数据)
        return temp

    @staticmethod
    def 运算_相加(x1, x2, 填充值=0):
        aax = x1.add(x2, fill_value=填充值)
        return aax

    @staticmethod
    def 运算_相减(x1, x2, 填充值=0):
        aax = x1.sub(x2, fill_value=填充值)
        return aax

    @staticmethod
    def 运算_相乘(x1, x2, 填充值=0):
        aax = x1.mul(x2, fill_value=填充值)
        return aax

    @staticmethod
    def 切片_前N行(x, n=5):
        aax = x.head(n=n)
        return aax

    # @staticmethod
    # def 切片_按元素值(self, 字符串表达式, 函数作用域=None):
    #     """
    #     例子：对象.切片按元素值_字符串表达式('x > 1.0 & x <1.25 & y >2.5 & y < 2.75')

    #     :param 字符串表达式:
    #     :param 函数作用域:
    #     :return:
    #     """
    #     if " isin " in 字符串表达式:
    #         dx = 字符串表达式.split(" isin ")
    #         dxq = eval(dx[0], 函数作用域)
    #         dxh = eval(dx[1], 函数作用域)
    #         brx = dxq.isin(dxh)
    #         aax = self[brx]
    #         # aax = self
    #         # for n in va:
    #         #     if ' isin ' in n:
    #         #         n = n.replace(' isin ', '.isin(')
    #         #         n = n + ')'
    #         #         print(n)
    #         #     st = 'self[' + n + ']'
    #         #     aax = eval(st)
    #         return _类型转换(aax)
    #     elif " isin " not in 字符串表达式:
    #         aax = self.嵌入对象DataFrame.query(字符串表达式)
    #         return _类型转换(aax)

    # @staticmethod
    # def 切片_按行列(self, *va):
    #     """
    #     将数据框架在各个维度进行切片。
    #     输入数据应该是多个列表，每个列表代表该维度上的切片。第一个维度是列，然后是行。

    #     输入：*va（多个列表）每个列表中可输入索引、标题、元祖等。空的列表代表保留全部数据。
    #     输出：（数据框架or数据序列）根据切片后结果范围数据序列或者数据框架。
    #     范例：
    #         >>> axxx = 数据框架.生成数据框架_通过列表([['a', 'b', 'c'],['e', 'f', 'g']])
    #         >>> axxxx = axxx.切片_按行列([],[0, 2])
    #         >>> axxxx.属性_形状
    #         (2, 2)
    #     """
    #     dalt = []
    #     sy = [self.嵌入对象DataFrame.index, self.嵌入对象DataFrame.columns]
    #     js = -1
    #     for m in va:
    #         js += 1
    #         lst = []
    #         if m:
    #             for n in m:
    #                 if type(n) == tuple:
    #                     if type(n[0]) == int:
    #                         lst.extend(list(range(*n)))
    #                     if type(n[0]) == str:
    #                         nn0 = list(sy[js]).index(n[0])
    #                         nn1 = list(sy[js]).index(n[1]) + 1
    #                         if len(n) == 3:
    #                             nn3 = n[2]
    #                         else:
    #                             nn3 = 1
    #                         lst.extend(list(range(nn0, nn1, nn3)))
    #                 else:
    #                     if type(n) == int:
    #                         lst.append(n)
    #                     if type(n) == str:
    #                         n = list(sy[js]).index(n)
    #                         lst.append(n)
    #         else:
    #             vb = len(sy[js])
    #             lst.extend(list(range(0, vb, 1)))
    #         dalt.append(lst)
    #     aaxx = self.嵌入对象DataFrame.iloc[dalt[0], dalt[1]]
    #     if len(aaxx.columns) == 1:  # 转换为数据系列
    #         aaxx = aaxx[aaxx.columns[0]]
    #     return _类型转换(aaxx)

    @staticmethod
    def 组合(对象, 轴=0, 排序=None, 组合方式="并集"):
        _组合方式映射 = {"并集": "outer", "交集": "inner"}
        组合方式 = _组合方式映射[组合方式]

        aax = pandas.concat(对象, axis=轴, sort=排序, join=组合方式)  # type: ignore
        return aax

    @staticmethod
    def 组合_垂直方向(x1: pandas.DataFrame, x2, 忽略索引=True, 排序=None):
        aax = x1.append(x2, ignore_index=忽略索引, sort=排序)  # type: ignore
        return aax

    @staticmethod
    def 组合_水平方向(x左, x右, 连接标题=None, 左连接标题=None, 右连接标题=None, 包含左索引=False, 包含右索引=False, 联合方式="交集", 标题后缀=("_x", "_y")):
        _联合方式映射 = {"并集": "outer", "交集": "inner", "左并集": "left", "右并集": "right"}
        联合方式raw = _联合方式映射[联合方式]
        aax = pandas.merge(x左, x右, on=连接标题, left_on=左连接标题, right_on=右连接标题, left_index=包含左索引, right_index=包含右索引, how=联合方式raw, suffixes=标题后缀)  # type: ignore
        return aax

    @staticmethod
    def 组合_水平方向_按索引(x1, x2, 连接标题=None):
        aax = x1.join(x2, on=连接标题)
        return aax

    # @staticmethod
    # def 元素_增加_按行列(x, 元素值, 轴=0, 插入位置=0, 字段或索引=None):
    #     aaxc = None
    #     if 轴 == 0:
    #         bbx = pandas.DataFrame(元素值).T
    #         bbx.columns = x.嵌入对象DataFrame.columns
    #         bbx.index = [字段或索引]
    #         # if 标题或索引 is None:
    #         #     aaxc = self.嵌入对象DataFrame.append(bbx, ignore_index=True)
    #         aaxc = x.嵌入对象DataFrame.append(bbx, ignore_index=False)
    #     elif 轴 == 1:
    #         if 字段或索引 is None:
    #             字段或索引 = "New"
    #         x.insert(插入位置, 字段或索引, 元素值)
    #         aaxc = x.嵌入对象DataFrame
    #     return aaxc

    # @staticmethod
    # def 元素_删除_按行列(self, 标题或索引, 轴=0, 修改源=False):
    #     aax = self.嵌入对象DataFrame.drop(标题或索引, axis=轴, inplace=修改源)
    #     return _类型转换(aax)

    # @staticmethod
    # def 元素_批量操作(self):
    #     return _元素批量操作(self.嵌入对象DataFrame.str)

    # @staticmethod
    # def 元素_替换元素值(self, 旧值=None, 新值=None):
    #     aax = self.嵌入对象DataFrame.replace(to_replace=旧值, value=新值)
    #     return _类型转换(aax)

    @staticmethod
    def 元素_删除_带有空值的行或列(x, 轴="行", 删除条件: Literal["全为空值才删", "阈值及以上为空值才删"] = "阈值及以上为空值才删", 阈值: Union[int, None] = None, 列名称过滤=None, 修改源=False):
        _轴映射 = {"行": 0, "列": 1}
        if type(轴) is str:
            轴raw = _轴映射[轴]
        else:
            轴raw = 轴

        if 删除条件 == "阈值及以上为空值才删" and type(阈值) is int:
            删除条件raw = "any"
            非空值数量raw = len(x.columns) - 阈值 + 1
        elif 删除条件 == "全为空值才删":
            删除条件raw = "all"
            非空值数量raw = None

        aax = x.dropna(axis=轴raw, inplace=修改源, how=删除条件raw, thresh=非空值数量raw, subset=列名称过滤)
        return aax

    # @staticmethod
    # def 元素_空值_填充(self, 值, 修改源=False, 填充方式=None):
    #     轴 = None
    #     if 填充方式 == "左值填充":
    #         填充方式 = "ffill"
    #         轴 = 1
    #     elif 填充方式 == "右值填充":
    #         填充方式 = "bfill"
    #         轴 = 1
    #     elif 填充方式 == "上值填充":
    #         填充方式 = "ffill"
    #         轴 = 0
    #     elif 填充方式 == "下值填充":
    #         填充方式 = "bfill"
    #         轴 = 0
    #     aax = self.嵌入对象DataFrame.fillna(值, axis=轴, inplace=修改源, method=填充方式)
    #     return _类型转换(aax)

    # @staticmethod
    # def 元素_是否为空(self, 取反=False):
    #     aax = self.嵌入对象DataFrame.isnull()
    #     if 取反:
    #         aax = self.嵌入对象DataFrame.notnull()
    #     return _类型转换(aax)

    # @staticmethod
    # def 标签_索引重生成(self, 丢弃现有索引=False):
    #     aax = self.嵌入对象DataFrame.reset_index(drop=丢弃现有索引)
    #     return _类型转换(aax)

    # @staticmethod
    # def 分组(self, key1):
    #     return _元素分组操作(self.嵌入对象DataFrame.groupby(key1))

    # @staticmethod
    # def 透视表(self, 聚合的内容=None, 分组的索引=None, 分组的标题=None, 聚合的方式="mean", 汇总=False):
    #     """
    #     将列分别作为行索引和列索引，然后对指定的列应用聚集函数。

    #     """
    #     aax = self.嵌入对象DataFrame.pivot_table(values=聚合的内容, index=分组的索引, columns=分组的标题, aggfunc=聚合的方式, margins=汇总)
    #     return _类型转换(aax)

    # @staticmethod
    # def 透视表_交叉表(列标题, 行标题):
    #     """专门用于统计分组频率的特殊透视表"""
    #     aax = pandas.crosstab(index=列标题, columns=行标题)
    #     return _类型转换(aax)
    @staticmethod
    def 转换_到excel文件(x: pandas.DataFrame, excel路径, excel表名称="Sheet1", 是否保留数据框架索引=False, 起始行索引=0, 起始列索引=0, **参):
        return x.to_excel(excel路径, sheet_name=excel表名称, index=是否保留数据框架索引, startrow=起始行索引, startcol=起始列索引, **参)

    @staticmethod
    def 转换_到json字符串(x: pandas.DataFrame, 数据结构=枚举_字典结构.JSON, 缩进=0, 日期格式="iso", **参):
        return x.to_json(orient=数据结构, indent=缩进, date_format=日期格式, **参)  # type: ignore

    @staticmethod
    def 转换_到json文件(x: pandas.DataFrame, 文件路径, 数据结构=枚举_字典结构.JSON, 缩进=0, 日期格式="iso", **参):
        return x.to_json(文件路径, orient=数据结构, indent=缩进, date_format=日期格式, **参)  # type: ignore

    @staticmethod
    def 转换_到字典(x: pandas.DataFrame, 数据结构=枚举_字典结构.JSON):
        aax = x.to_dict(orient=数据结构)  # type: ignore
        return aax

    @staticmethod
    def 转换_到csv文件(x: pandas.DataFrame, csv路径, 列名称列表=None, 行名称列表=True, 标题=True, 写入模式: Literal["追加", "覆盖"] = "覆盖", 编码="utf-8"):
        _写入和读取模式映射 = {"追加": "a", "a": "a", "覆盖": "w", "w": "w"}
        写入模式raw = _写入和读取模式映射[写入模式]
        return x.to_csv(csv路径, columns=列名称列表, header=标题, index=行名称列表, mode=写入模式raw, encoding=编码)  # type: ignore

    # def 转换_数据框架到mssql(self, 表名, 重名处理='追加', 用户名x='', 密码x='', 数据库实例=r'.\SQLEXPRESS', 数据库名称='beixiao'):
    #     engine = create_engine(
    #         'mssql+pyodbc://' + 用户名x + ':' + 密码x + '@' + 数据库实例 + '/' + 数据库名称 +
    #         '?driver=SQL server')
    #     with engine.connect() as conn, conn.begin():
    #         if 重名处理 == '追加':
    #             重名处理 = 'append'
    #         self.嵌入对象DataFrame.to_sql(表名, engine, if_exists=重名处理)
    #     return

    @staticmethod
    def 转换_从csv文件(csv路径, 列名称列表=None, 标题行索引=0):
        aa = pandas.read_csv(csv路径, names=列名称列表, header=标题行索引)
        return aa

    @staticmethod
    def 转换_从json文件(json路径):
        aa = pandas.read_json(json路径)
        return aa

    @staticmethod
    def 转换_从excel文件(excel路径, excel表名称="Sheet1", 指定行标签所在行的索引=0, 指定列标签所在列的索引=None, 要读取的列: Union[list, tuple, None] = None, 要读取的行: Union[list, tuple, None] = None, 要跳过的行: Union[list, None] = None, 指定数据类型=None, 被视为缺失值的值=None):
        from bxpandas.数据框架包 import 数据框架类

        aa = pandas.read_excel(excel路径, sheet_name=excel表名称, header=指定行标签所在行的索引, index_col=指定列标签所在列的索引, usecols=要读取的列, nrows=要读取的行, skiprows=要跳过的行, dtype=指定数据类型, na_values=被视为缺失值的值)  # type: ignore
        bb = 数据框架类.元素_删除_带有空值的行或列(aa, 删除条件="全为空值才删")
        return bb
