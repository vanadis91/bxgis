import arcpy
from typing import Union, Literal

_数据类型映射 = {
    "GPFeatureLayer": "GPFeatureLayer",
    "要素图层": "GPFeatureLayer",
    "DEFeatureClass": "DEFeatureClass",
    "要素类": "DEFeatureClass",
    "GPBoolean": "GPBoolean",
    "布尔值": "GPBoolean",
    "GPDouble": "GPDouble",
    "双精度": "GPDouble",
    "Field": "Field",
    "字段": "Field",
    "GPLong": "GPLong",
    "长整型": "GPLong",
    "GPString": "GPString",
    "字符串": "GPString",
    "DETable": "DETable",
    "表": "DETable",
    "DEWorkspace": "DEWorkspace",
    "工作空间": "DEWorkspace",
}
_数据必要性映射 = {
    "必填": "Required",
    "Required": "Required",
    "选填": "Optional",
    "Optional": "Optional",
    "隐藏的返回值": "Derived",
    "Derived": "Derived",
}
_参数类型映射 = {
    "输入参数": "Input",
    "Input": "Input",
    "输出参数": "Output",
    "Output": "Output",
}


class 参数类:
    def __init__(self, 内嵌对象) -> None:
        self._内嵌对象 = 内嵌对象

    @staticmethod
    def 参数创建(名称, 描述, 数据类型, 参数必要性: Literal["必填"], 参数类型: Literal["输入参数"]):
        数据类型raw = _数据类型映射[数据类型]
        参数必要性raw = _数据必要性映射[参数必要性]
        参数类型raw = _参数类型映射[参数类型]
        ret = arcpy.Parameter(
            displayName=名称,
            name=描述,
            datatype=数据类型raw,
            parameterType=参数必要性raw,
            direction=参数类型raw,
        )
        return 参数类(ret)
