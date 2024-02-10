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
    "GPValueTable": "GPValueTable",
    "值表": "GPValueTable",
    "DEFile": "DEFile",
    "文件": "DEFile",
    "DEFolder": "DEFolder",
    "文件夹": "DEFolder",
    "GPDataFile": "GPDataFile",
    "数据文件": "GPDataFile",
    "DECadDrawingDataset": "DECadDrawingDataset",
    "CAD数据集": "DECadDrawingDataset",
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
        self._内嵌对象: arcpy.Parameter = 内嵌对象

    @staticmethod
    def 参数创建(名称, 描述, 数据类型: Literal["要素图层", "要素类", "布尔值", "双精度", "字段", "长整型", "字符串", "表", "工作空间", "值表", "文件", "文件夹", "数据文件", "CAD数据集"], 参数必要性: Literal["必填", "选填", "隐藏的返回值"] = "选填", 参数类型: Literal["输入参数", "输出参数"] = "输入参数", 是否多个值=False, 是否可用=True, 默认值=None):
        数据类型raw = _数据类型映射[数据类型]
        参数必要性raw = _数据必要性映射[参数必要性]
        参数类型raw = _参数类型映射[参数类型]
        ret = 参数类(
            arcpy.Parameter(
                name=名称,
                displayName=描述,
                direction=参数类型raw,
                datatype=数据类型raw,
                parameterType=参数必要性raw,
                enabled=是否可用,
                multiValue=是否多个值,
            )
        )
        if 默认值:
            参数类.值设置(ret._内嵌对象, 默认值)
        return ret

    def 值读取(self: Union["参数类", arcpy.Parameter]):
        内嵌对象: arcpy.Parameter
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类 else (False, self)  # type: ignore
        return 内嵌对象.value

    def 值读取_作为字符串(self: Union["参数类", arcpy.Parameter]):
        内嵌对象: arcpy.Parameter
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类 else (False, self)  # type: ignore
        return 内嵌对象.valueAsText

    def 值设置(self: Union["参数类", arcpy.Parameter], 值):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类 else (False, self)
        内嵌对象.value = 值  # type: ignore

    def 名称读取(self: Union["参数类", arcpy.Parameter]):
        内嵌对象: arcpy.Parameter
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类 else (False, self)  # type: ignore
        return 内嵌对象.name

    def 可用性设置(self: Union["参数类", arcpy.Parameter], 布尔值):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类 else (False, self)
        内嵌对象.enabled = 布尔值  # type: ignore

    def 过滤器读取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类 else (False, self)
        return 参数类.过滤器类(内嵌对象.filter)  # type: ignore

    class 过滤器类:
        _类型映射 = {"值列表": "ValueList", "值区间": "Range"}

        def __init__(self, 内嵌对象) -> None:
            self._内嵌对象 = 内嵌对象

        def 类型设置(self, 类型: Literal["值列表", "值区间"]):
            self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类.过滤器类 else (False, self)
            类型raw = 参数类.过滤器类._类型映射[类型]
            内嵌对象.type = 类型raw  # type: ignore

        def 值设置(self, 值: list):
            self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 参数类.过滤器类 else (False, self)
            from . import 常量

            listTemp = []
            for x in 值:
                if x in 常量._要素类型映射.keys():
                    ret = 常量._要素类型映射[x]
                else:
                    ret = x
            listTemp.append(ret)
            值raw = listTemp
            内嵌对象.list = 值raw  # type: ignore


if __name__ == "__main__":
    a = 参数类.参数创建("输入要素", "输入要素", "要素图层")._内嵌对象
    参数类.值设置(a, 123)
    print(参数类.值读取(a))
