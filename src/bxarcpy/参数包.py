import arcpy
from typing import Union, Literal

_数据类型映射 = {
    "要素图层": "GPFeatureLayer",
    "要素类": "DEFeatureClass",
    "布尔值": "GPBoolean",
    "双精度": "GPDouble",
    "字段": "Field",
    "长整型": "GPLong",
    "字符串": "GPString",
    "表": "DETable",
    "工作空间": "DEWorkspace",
    "值表": "GPValueTable",
    "文件": "DEFile",
    "文件夹": "DEFolder",
    "数据文件": "GPDataFile",
    "CAD数据集": "DECadDrawingDataset",
}
_数据必要性映射 = {
    "必填": "Required",
    "选填": "Optional",
    "隐藏的输出参数": "Derived",
}
_参数类型映射 = {
    "输入参数": "Input",
    "输出参数": "Output",
}


class 参数类:
    @staticmethod
    def 参数创建(
        名称,
        数据类型: Literal["要素图层", "要素类", "布尔值", "双精度", "字段", "长整型", "字符串", "表", "工作空间", "值表", "文件", "文件夹", "数据文件", "CAD数据集"],
        描述=None,
        参数必要性: Literal["必填", "选填", "隐藏的返回值"] = "选填",
        参数类型: Literal["输入参数", "输出参数"] = "输入参数",
        是否多个值=False,
        是否可用=True,
        默认值=None,
        所依赖参数名称列表=None,
        参数预设类型: Literal["值列表", "值区间", None] = None,
        参数预设列表: Union[list, None] = None,
    ):
        数据类型raw = _数据类型映射.get(数据类型, 数据类型)
        参数必要性raw = _数据必要性映射.get(参数必要性, 参数必要性)
        参数类型raw = _参数类型映射.get(参数类型, 参数类型)
        描述 = 名称 if 描述 is None else 描述
        ret = arcpy.Parameter(
            name=名称,
            displayName=描述,
            direction=参数类型raw,
            datatype=数据类型raw,
            parameterType=参数必要性raw,
            enabled=是否可用,
            multiValue=是否多个值,
        )

        if 默认值:
            参数类.属性设置_值(ret, 默认值)

        if 所依赖参数名称列表:
            参数类.属性设置_依赖关系(ret, 所依赖参数名称列表)
            # ret._内嵌对象.schema.clone = True

        if 参数预设类型 == "值列表":
            ret.filter.type = "ValueList"
        elif 参数预设类型 == "值区间":
            ret.filter.type = "Range"
        if 参数预设类型 and 参数预设列表:
            from bxarcpy.基本对象包 import 枚举类

            值raw = [枚举类.要素类型.值获取(x) for x in 参数预设列表]
            ret.filter.list = 值raw
        return ret

    @staticmethod
    def 属性获取_值(参数对象: arcpy.Parameter):
        return 参数对象.value

    @staticmethod
    def 属性设置_值(参数对象: arcpy.Parameter, 值):
        参数对象.value = 值  # type: ignore

    @staticmethod
    def 属性获取_值_字符串形式(参数对象: arcpy.Parameter):
        return 参数对象.valueAsText

    @staticmethod
    def 属性获取_名称(参数对象: arcpy.Parameter):
        return 参数对象.name

    @staticmethod
    def 属性设置_可用性(参数对象: arcpy.Parameter, 布尔值):
        参数对象.enabled = 布尔值  # type: ignore

    @staticmethod
    def 属性设置_依赖关系(参数对象: arcpy.Parameter, 参数名称列表):
        参数对象.parameterDependencies = 参数名称列表  # type: ignore

    @staticmethod
    def 属性获取_过滤器(参数对象: arcpy.Parameter):
        return 参数对象.filter  # type: ignore

    class 过滤器类:
        _类型映射 = {"值列表": "ValueList", "值区间": "Range"}

        @staticmethod
        def 属性设置_类型(过滤器对象, 类型: Literal["值列表", "值区间"]):
            类型raw = 参数类.过滤器类._类型映射[类型]
            过滤器对象.type = 类型raw  # type: ignore

        @staticmethod
        def 属性设置_值(过滤器对象, 值: list):
            from bxarcpy.基本对象包 import 枚举类

            值raw = [枚举类.要素类型.值获取(x) for x in 值]
            过滤器对象.list = 值raw  # type: ignore


if __name__ == "__main__":
    a = 参数类.参数创建("输入要素", "要素图层")
    参数类.属性设置_值(a, 123)
    print(参数类.属性获取_值(a))
