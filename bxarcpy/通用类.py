import arcpy
from typing import Union, Literal


class bxArcpy数组:
    class 类:
        def __init__(self, 内嵌对象):
            if type(内嵌对象) is bxArcpy数组.类:
                self._内嵌对象 = 内嵌对象._内嵌对象
            elif type(内嵌对象) is arcpy.Array:
                self._内嵌对象 = 内嵌对象

        @staticmethod
        def 实例创建(内容=None) -> "bxArcpy数组.类":
            return bxArcpy数组.类(arcpy.Array(内容))

        def 项插入(self: Union[arcpy.Array, "bxArcpy数组.类", "bxArcpy数组"], 项) -> Union[arcpy.Array, "bxArcpy数组.类"]:
            self为bxArcpyArray = True if type(self) is bxArcpy数组.类 else False
            self = bxArcpy数组.类(self)

            self._内嵌对象.add(项)

            return self if self为bxArcpyArray else self._内嵌对象

    @staticmethod
    def bxArcpy数组创建(内容=None) -> arcpy.Array:
        return arcpy.Array(内容)

    项插入 = 类.项插入


class bxArcpy点:
    class 类:
        def __init__(self, 内嵌对象):
            if type(内嵌对象) is bxArcpy点.类:
                self._内嵌对象 = 内嵌对象._内嵌对象
            elif type(内嵌对象) is arcpy.Point:
                self._内嵌对象 = 内嵌对象

        @staticmethod
        def 实例创建(X, Y, Z=None, M=None, ID=None) -> "bxArcpy点.类":
            return bxArcpy点.类(arcpy.Point(X, Y, Z, M, ID))

        def X坐标获取(self: Union[arcpy.Point, "bxArcpy点.类", "bxArcpy点"]):
            self = bxArcpy点.类(self)
            return self._内嵌对象.X

        def Y坐标获取(self: Union[arcpy.Point, "bxArcpy点.类", "bxArcpy点"]):
            self = bxArcpy点.类(self)
            return self._内嵌对象.Y

    @staticmethod
    def bxArcpy点创建(X, Y, Z=None, M=None, ID=None) -> arcpy.Point:
        return arcpy.Point(X, Y, Z, M, ID)

    X坐标获取 = 类.X坐标获取
    Y坐标获取 = 类.Y坐标获取


class bxArcpy线:
    class 类:
        def __init__(self, 内嵌对象):
            if type(内嵌对象) is bxArcpy线.类:
                self._内嵌对象 = 内嵌对象._内嵌对象
            elif type(内嵌对象) is arcpy.Polyline:
                self._内嵌对象 = 内嵌对象

        @staticmethod
        def 实例创建(数组) -> "bxArcpy线.类":
            return bxArcpy线.类(arcpy.Polyline(数组))

    @staticmethod
    def bxArcpy线创建(数组) -> arcpy.Polyline:
        return arcpy.Polyline(数组)
