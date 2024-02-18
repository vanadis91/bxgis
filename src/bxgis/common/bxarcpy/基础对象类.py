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
