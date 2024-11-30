import numpy
from .配置 import 配置
from typing import Literal


class 数组类:
    @staticmethod
    def 数组创建_通过列表(数据, 元素类型=None, **参):
        """

        :param 数据:
        :param 值:
        :param 元素类型:
        :param 参:
        :return:
        >>> aa = 数组.生成数组_通过列表或元祖([1111, 21, 31, 5151, 515])
        >>> aa.属性_元素个数
        5
        """
        temp = numpy.array(数据, dtype=元素类型, **参)
        return temp

    @staticmethod
    def 数组创建_全0(形状, 元素类型=None, 读取顺序="先行后列"):
        """

        :param 形状:
        :param 元素类型:
        :param 读取顺序:
        :return:
        >>> aa = 数组.生成数组_全0([2, 3])
        >>> aa.属性_元素个数
        6
        """
        读取顺序 = 配置.数据读取顺序映射[读取顺序]
        return numpy.zeros(shape=形状, dtype=元素类型, order=读取顺序)  # type: ignore

    @staticmethod
    def 数组创建_全1(形状, 元素类型=None, 读取顺序="先行后列"):
        """

        :param 形状:
        :param 元素类型:
        :param 读取顺序:
        :return:
        >>> bb = 数组.生成数组_全1([2, 3])
        >>> bb.属性_元素个数
        6
        """
        读取顺序 = 配置.数据读取顺序映射[读取顺序]
        return numpy.ones(shape=形状, dtype=元素类型, order=读取顺序)  # type: ignore

    @staticmethod
    def 数组创建_序列(起点, 终点, 步数, **参):
        """
        生成序列数组。1值则生成0到值1的序列数组，3值则生成从值1到值2步数为值3的序列数组

        :return:
        """
        return numpy.arange(起点, 终点, 步数, **参)

    @staticmethod
    def 数组创建_等分(起点, 终点, 等分数量=50, 包括终止数=True, 输出间距=False, 元素类型=None, 轴=0):
        start = 起点
        stop = 终点
        return numpy.linspace(start, stop, num=等分数量, endpoint=包括终止数, retstep=输出间距, dtype=元素类型, axis=轴)  # type: ignore

    @staticmethod
    def 数组创建_随机(数组形状=(10, 10), 数据分布: Literal["随机", "正态分布"] = "随机", 数据范围=(0, 1), 数据类型=Literal["整数", "浮点"], 平均值=None, 标准差=None):
        数组形状_元组 = 数组形状
        if type(数组形状) is int:
            数组形状_元组 = (数组形状,)
        aaxc = []
        if 数据分布 == "随机":
            return numpy.random.random([*数组形状_元组])
        if 数据分布 == "随机" and 数据范围 == (0, 1):
            return numpy.random.rand(*数组形状_元组)
        if 数据分布 == "随机" and 数据类型 == "整数":
            return numpy.random.randint(*数据范围, 数组形状_元组)  # type: ignore
        if 数据分布 == "正态分布" and 标准差 is None:
            return numpy.random.randn(*数组形状_元组)
        if 数据分布 == "正态分布" and 平均值 is not None and 标准差 is not None and 数组形状.__class__.__name__ == "int":
            return numpy.random.normal(平均值, 标准差, 数组形状)

    @staticmethod
    def 维度获取(x):
        return x.ndim

    @staticmethod
    def 形状获取(x):
        return x.shape

    @staticmethod
    def 元素个数获取(x):
        return x.size

    @staticmethod
    def 元素类型获取(x):
        return x.dtype

    @staticmethod
    def 元素的字节大小获取(x):
        return x.itemsize

    @staticmethod
    def 变形(x, 数组形状, 读取顺序="先行后列"):
        """

        :param 数组形状:
        :param 读取顺序:
        :return:
        >>> a = 数组.生成数组_通过列表或元祖([[1, 2], [3, 4]])
        >>> a.变形(1, 4).属性_形状
        (1, 4)
        >>> a = 数组.生成数组_通过列表或元祖([[1, 2], [3, 4]])
        >>> b = a.变形(4, 读取顺序='先列后行')
        >>> print(b[1])
        3
        """
        读取顺序 = 配置.数据读取顺序映射[读取顺序]
        return x.reshape(*数组形状, order=读取顺序)

    @staticmethod
    def 变形_一维化(x, 读取顺序="先行后列"):
        读取顺序 = 配置.数据读取顺序映射[读取顺序]
        x.flatten(order=读取顺序)
        return x

    @staticmethod
    def 组合(数组列表, 轴=0, **参):
        """
        输入一个列表，列表中每个元素代表要组合的数组。

        :param 数组列表: 轴=0|1|...(代表在哪个轴上进行合并，对于1维数组轴的设置无效。)
        :param 轴: 列表(对列表中的元素进行组合。1维是水平组合，2维是垂直组合。)
        :return:
        """
        return numpy.concatenate(数组列表, axis=轴, **参)

    @staticmethod
    def 组合_垂直方向(数组列表):
        """
        输入一个列表，列表中每个元素代表要组合的数组。

        :param 数组列表:
        :return:
        """
        return numpy.vstack(数组列表)

    @staticmethod
    def 组合_水平方向(数组列表):
        """
        输入一个列表，列表中每个元素代表要组合的数组。

        :param 数组列表:
        :return:
        """
        """
        说明：对数组进行水平组合。参数：采用列表形式的参数([X, Y])
        """
        return numpy.hstack(数组列表)

    @staticmethod
    def 拆分_垂直方向(x, 切片):
        """
        输入一个数组和一个切片，按照切片进行数组的拆分，切片是数组时，在数组中数字位置切开。

        :return: 返回一个列表，元素为切分后的各个数组。
        """
        return numpy.vsplit(x, 切片)

    @staticmethod
    def 拆分_水平方向(x, 切片):
        """
        输入一个数组和一个切片，按照切片进行数组的拆分。切片是数组时，在数组中数字位置切开。

        :return: 返回一个列表，元素为切分后的各个数组。
        """
        return numpy.hsplit(x, 切片)

    @staticmethod
    def 运算_相加(x1, x2, *值, **参):
        return numpy.add(x1, x2, *值, **参)

    @staticmethod
    def 运算_相减(x1, x2, *值, **参):
        return numpy.subtract(x1, x2, *值, **参)

    @staticmethod
    def 运算_取负(x, *值, **参):
        return numpy.negative(x, *值, **参)

    @staticmethod
    def 运算_相乘(x1, x2, *值, **参):
        return numpy.multiply(x1, x2, *值, **参)

    @staticmethod
    def 运算_相除(x1, x2, *值, **参):
        return numpy.divide(x1, x2, *值, **参)

    @staticmethod
    def 运算_相除取整(x1, x2, *值, **参):
        return numpy.floor_divide(x1, x2, *值, **参)

    @staticmethod
    def 运算_相除取余(x1, x2, *值, **参):
        return numpy.mod(x1, x2, *值, **参)

    @staticmethod
    def 运算_幂(x底数, x指数, *值, **参):
        return numpy.power(x底数, x指数, *值, **参)

    @staticmethod
    def 运算_矩阵相乘(x1, x2, *值, **参):
        return numpy.dot(x1, x2, *值, **参)

    @staticmethod
    def 运算_绝对值(x, *值, **参):
        return numpy.absolute(x, *值, **参)

    @staticmethod
    def 运算_sin(x, *值, **参):
        return numpy.sin(x, *值, **参)

    @staticmethod
    def 运算_cos(x, *值, **参):
        return numpy.cos(x, *值, **参)

    @staticmethod
    def 运算_tan(x, *值, **参):
        return numpy.tan(x, *值, **参)

    @staticmethod
    def 运算_指数_e为底(x, *值, **参):
        return numpy.exp(x, *值, **参)

    @staticmethod
    def 运算_指数_2为底(x, *值, **参):
        return numpy.exp2(x, *值, **参)

    @staticmethod
    def 运算_对数_e为底(x, *值, **参):
        return numpy.log(x, *值, **参)

    @staticmethod
    def 运算_对数_2为底(x, *值, **参):
        return numpy.log2(x, *值, **参)

    @staticmethod
    def 运算_对数_10为底(x, *值, **参):
        return numpy.log10(x, *值, **参)

    @staticmethod
    def 统计_求和(x, 轴=None, 元素类型=None, 空值安全=True, **参):
        if 空值安全:
            return numpy.nansum(x, axis=轴, dtype=元素类型, **参)
        else:
            return numpy.sum(x, axis=轴, dtype=元素类型, **参)

    @staticmethod
    def 统计_最大值(x, 轴=None, 空值安全=True, 元素类型=None, **参):
        if 空值安全:
            return numpy.max(x, axis=轴, **参)
        else:
            return numpy.nanmax(x, axis=轴, dtype=元素类型, **参)  # type: ignore

    @staticmethod
    def 统计_最小值(x, 轴=None, 空值安全=True, **参):
        if 空值安全:
            return numpy.min(x, axis=轴, **参)
        else:
            return numpy.nanmin(x, axis=轴, **参)

    @staticmethod
    def 统计_平均值(x, 轴=None, 空值安全=True, **参):
        if 空值安全:
            return numpy.mean(x, axis=轴, **参)
        else:
            return numpy.nanmean(x, axis=轴, **参)

    @staticmethod
    def 统计_标准差(x, 轴=None, 元素类型=None, 空值安全=True, **参):
        if 空值安全:
            return numpy.std(x, axis=轴, dtype=元素类型, **参)
        else:
            return numpy.nanstd(x, axis=轴, dtype=元素类型, **参)
