from ast import Is
from bxpy import 日志
try:
    import arcpy
except Exception as e:
    pass
from .要素类 import 要素类


class 图层类(要素类):
    class 符号系统类:
        def __init__(self, 内嵌对象, 内嵌图层对象):
            self._内嵌对象 = 内嵌对象
            self._内嵌图层对象 = 内嵌图层对象

        # def 符号系统设置_通过stylx样式文件(self, 样式文件路径):
        #     self._内嵌对象.applySymbologyFromLayer(样式文件路径)
        #     self._内嵌图层对象.refresh()

    def __init__(self, 内嵌对象=None):
        if 内嵌对象:
            self._内嵌对象 = 内嵌对象
            self.名称 = self._内嵌对象.name

    def __repr__(self) -> str:
        return f"<bxarcpy.图层类 对象 {{名称:{self.名称}}}>"

    @property
    def 符号系统(self):
        return 图层类.符号系统类(self._内嵌对象.symbology, self._内嵌对象)

    @符号系统.setter
    def 符号系统(self, 符号系统):
        if type(符号系统) is 图层类.符号系统类:
            符号系统 = 符号系统._内嵌对象
        self._内嵌对象.symbology = 符号系统

    def 类型是否为要素图层(self):
        return self._内嵌对象.isFeatureLayer

    def 类型是否为网络图层(self):
        return self._内嵌对象.isWebLayer

    def 操作是否被支持(self, 操作名称="DEFINITIONQUERY"):
        _操作映射表 = {"DEFINITIONQUERY": "DEFINITIONQUERY", "查询语句设置": "DEFINITIONQUERY", "minThreshold": "minThreshold", "最小视图比例设置": "minThreshold"}
        return self._内嵌对象.supports(操作名称)

    def 查询语句设置(self, 查询语句="Acres > 5.0"):
        self._内嵌对象.definitionQuery = 查询语句
        return self

    def 最小视图比例设置(self, 视图比例: int):
        self._内嵌对象.minThreshold = 视图比例
        return self

    def 符号系统设置_通过图层文件(self, 符号系统图层, 符号系统字段=[["值字段", "符号系统图层的字段", "输入图层的字段"]], 按数据更新符号系统范围="默认"):
        _符号系统字段类型映射表 = {"值字段": "VALUE_FIELD", "VALUE_FIELD": "VALUE_FIELD"}
        符号系统字段temp = []
        for x in 符号系统字段:
            if x[0] in _符号系统字段类型映射表:
                符号系统字段temp.append([_符号系统字段类型映射表[x[0]], x[1], x[2]])
            else:
                符号系统字段temp.append(x)
        符号系统字段 = 符号系统字段temp

        _按数据更新符号系统范围映射表 = {"默认": "DEFAULT", "DEFAULT": "DEFAULT", "更新范围": "UPDATE", "UPDATE": "UPDATE", "保留范围": "MAINTAIN", "MAINTAIN": "MAINTAIN"}
        按数据更新符号系统范围 = _按数据更新符号系统范围映射表[按数据更新符号系统范围]

        if type(符号系统图层) is 图层类:
            符号系统图层 = 符号系统图层._内嵌对象

        新建图层 = arcpy.management.ApplySymbologyFromLayer(in_layer=self._内嵌对象, in_symbology_layer=符号系统图层, symbology_fields=符号系统字段, update_symbology=按数据更新符号系统范围)[0]
        符号系统 = 图层类(新建图层).符号系统
        self.符号系统 = 符号系统
        return self

    def 符号系统设置_通过stylx样式文件(self, 匹配字段="地类编号", 样式文件路径=r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx"):
        新建图层 = arcpy.management.MatchLayerSymbologyToAStyle(in_layer=self._内嵌对象, match_values=匹配字段, in_style=样式文件路径)[0]
        符号系统 = 图层类(新建图层).符号系统
        self.符号系统 = 符号系统
        return self


class 图层类_10版本:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    @staticmethod
    def 图层创建(图层路径=None):
        return 图层类_10版本(内嵌对象=arcpy.mapping.Layer(图层路径))
