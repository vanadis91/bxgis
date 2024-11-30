import shapely
from shapely.geometry import LineString, Point, Polygon, MultiPolygon
from typing import Union, Literal
from .通用对象包 import _点线面通用类, _点集线集面集通用类


class 面类(_点线面通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 面创建_通过点表(点表, 内环列表=None):
        # interiors
        return Polygon(点表, holes=内环列表)

    @staticmethod
    def 外环获取(x):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return x.exterior  # type: ignore

    @staticmethod
    def 坐标获取_外环(x):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return list(x.exterior.coords)  # type: ignore

    @staticmethod
    def 折点获取_外环(x):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return [Point(z) for z in x.exterior.coords]  # type: ignore

    @staticmethod
    def 内环列表获取(x):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return list(x.interiors)  # type: ignore

    @staticmethod
    def 坐标获取_内环列表(x):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return [list(z.coords) for z in x.interiors]  # type: ignore

    @staticmethod
    def 折点获取_内环列表(x):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        temp = []
        for z in x.interiors:  # type: ignore
            temp.append([Point(y) for y in z.coords])
        return temp


class 面集类(_点集线集面集通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 面集创建_通过外内环元祖列表(x):
        return MultiPolygon(x)


if __name__ == "__main__":
    pass
