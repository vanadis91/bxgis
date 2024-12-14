# *-* coding:utf8 *-*
import arcpy
from typing import Union, Literal
from enum import Enum


class 数组类:
    # def __init__(self, 内嵌对象) -> None:
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 数组创建(内容=[]):
        return arcpy.Array(内容)

    @staticmethod
    def 项插入(数组对象, 项):
        数组对象.add(项)  # type: ignore

        return 数组对象


class 枚举类:
    class 字段类型(Enum):
        @staticmethod
        def 值获取(x):
            try:
                return 枚举类.字段类型[x].value
            except Exception as e:
                try:
                    return 枚举类.字段类型(x).value
                except Exception as e:
                    return x

        @staticmethod
        def 名称获取(x):
            try:
                return 枚举类.字段类型((x.upper())).name
            except Exception as e:
                try:
                    return 枚举类.字段类型[x.upper()].name
                except Exception as e:
                    return x

        字符串 = "TEXT"
        双精度 = "DOUBLE"
        整型 = "INTEGER"
        长整型 = "LONG"
        短整型 = "SHORT"
        日期 = "DATE"
        单精度 = "FLOAT"
        对象ID = "OID"
        GUID = "GUID"
        定长字符串 = "STRING"

    class 要素类型(Enum):
        @staticmethod
        def 值获取(x):
            try:
                return 枚举类.要素类型[x].value
            except Exception as e:
                try:
                    return 枚举类.要素类型(x).value
                except Exception as e:
                    return x

        @staticmethod
        def 名称获取(x):
            try:
                return 枚举类.要素类型((x.upper())).name
            except Exception as e:
                try:
                    return 枚举类.要素类型[x.upper()].name
                except Exception as e:
                    return x

        点 = "POINT"
        多点 = "MULTIPOINT"
        面 = "POLYGON"
        线 = "POLYLINE"
        多面体 = "MULTIPATCH"


# 枚举_字段类型映射 = {"字符串": "TEXT", "TEXT": "TEXT", "双精度": "DOUBLE", "DOUBLE": "DOUBLE", "长整型": "LONG", "LONG": "LONG", "短整型": "SHORT", "SHORT": "SHORT", "日期": "DATE", "DATE": "DATE", "单精度": "FLOAT", "FLOAT": "FLOAT", "对象ID": "OID", "OID": "OID", "定长字符串": "定长字符串", "String": "String"}

# 枚举_要素类型映射 = {"点": "POINT", "POINT": "POINT", "多点": "MULTIPOINT", "MULTIPOINT": "MULTIPOINT", "面": "POLYGON", "POLYGON": "POLYGON", "线": "POLYLINE", "POLYLINE": "POLYLINE", "多面体": "MULTIPATCH", "MULTIPATCH": "MULTIPATCH"}

# 枚举_要素类型反映射 = {"点": "点", "POINT": "点", "多点": "多点", "MULTIPOINT": "多点", "面": "面", "POLYGON": "面", "线": "线", "POLYLINE": "线", "多面体": "多面体", "MULTIPATCH": "多面体"}
