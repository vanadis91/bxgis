from shapely.geometry import LineString, Point
from shapely.geometry import MultiPoint
from typing import Union, Literal
from bxshapely import 通用对象包

# from _通用 import _点线面通用, _点集线集面集通用
from typing import Union, Literal


class 点类(通用对象包._点线面通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 点创建_通过xy坐标(x, y):
        return Point(x, y)

    @staticmethod
    def 点创建_通过坐标元祖(x: Union[tuple, list]):
        return Point(x)

    @staticmethod
    def x坐标获取(点实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if isinstance(self, 点类) else (False, self)
        return 点实例.x  # type: ignore

    @staticmethod
    def y坐标获取(点实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if isinstance(self, 点类) else (False, self)
        return 点实例.y  # type: ignore


# class 点cls:
#     def __init__(self) -> None:
#         super().__init__()


# def __init__(self, 内嵌对象):
#     if type(内嵌对象) is 点类:
#         self._内嵌对象 = 内嵌对象._内嵌对象
#     elif type(内嵌对象) is Point:
#         self._内嵌对象 = 内嵌对象


# 点类构造字典 = {
#     "__init__": __init__,
#     "x坐标获取": 点.x坐标获取,
# }
# 点类 = type("点类", (), 点类构造字典)


class 点集类(通用对象包._点集线集面集通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 点集创建_通过元祖列表(x):
        return MultiPoint(x)


if __name__ == "__main__":
    pass
    # 点类(Point()).x坐标获取()
