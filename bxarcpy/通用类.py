import arcpy
from typing import Union, Literal


class 数组:
    def __init__(self, 内嵌对象) -> None:
        if hasattr(内嵌对象, "_内嵌对象"):
            self._内嵌对象 = 内嵌对象._内嵌对象
        else:
            self._内嵌对象 = 内嵌对象

    @staticmethod
    def 数组创建(内容=None):
        return 数组(arcpy.Array(内容))

    def 项插入(self, 项):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)

        内嵌对象.add(项)  # type: ignore

        return self


class 点:
    def __init__(self, 内嵌对象) -> None:
        if hasattr(内嵌对象, "_内嵌对象"):
            self._内嵌对象 = 内嵌对象._内嵌对象
        else:
            self._内嵌对象 = 内嵌对象

    @staticmethod
    def 点创建(X, Y, Z=None, M=None, ID=None):
        return 点(arcpy.Point(X, Y, Z, M, ID))

    def X坐标获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 内嵌对象.X  # type: ignore

    def Y坐标获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 内嵌对象.Y  # type: ignore


class 线:
    def __init__(self, 内嵌对象):
        if hasattr(内嵌对象, "_内嵌对象"):
            self._内嵌对象 = 内嵌对象._内嵌对象
        else:
            self._内嵌对象 = 内嵌对象

    @staticmethod
    def 线创建(数组):
        return 线(arcpy.Polyline(数组))
