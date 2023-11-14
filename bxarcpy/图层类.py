from bxpy import 日志
import arcpy
from .要素类 import 要素类


class 图层类(要素类):
    class 符号系统类:
        def __init__(self, 内嵌对象, 内嵌图层对象):
            self._内嵌对象 = 内嵌对象
            self._内嵌图层对象 = 内嵌图层对象

        def 符号系统设置_通过stylx样式文件(self, 样式文件路径):
            self._内嵌对象.applySymbologyFromLayer(样式文件路径)
            self._内嵌图层对象.refresh()

    def __init__(self, 内嵌对象=None, 名称=None):
        if 内嵌对象:
            self._内嵌对象 = 内嵌对象
            self.名称 = self._内嵌对象.name
        if 名称:
            self.名称 = 名称

    def __repr__(self) -> str:
        return f"<bxarcpy.图层类 对象 {{名称:{self.名称}}}>"

    @property
    def 符号系统(self):
        return 图层类.符号系统类(self._内嵌对象.symbology, self._内嵌对象)

    @符号系统.setter
    def 符号系统(self, 符号系统):
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

    def 刷新(self):
        self._内嵌对象.refresh()
        return self

    def 最小视图比例设置(self, 视图比例: int):
        self._内嵌对象.minThreshold = 视图比例
        return self

    def 符号系统设置_通过lyr图层文件(self, 图层文件路径, 映射关系=[["VALUE_FIELD", "", "JQYDDM"]]):
        return arcpy.management.ApplySymbologyFromLayer(
            in_layer=self._内嵌对象,
            in_symbology_layer=图层文件路径,
            symbology_fields=映射关系,
            update_symbology="DEFAULT",
        )[0]

    def 符号系统设置_通过stylx样式文件(self, 样式文件路径, 映射关系="地类编号"):
        # 映射关系="$feature.JQYDDM"
        # return arcpy.management.MatchLayerSymbologyToAStyle(in_layer=self._内嵌对象, match_values=映射关系, in_style=样式文件路径)[0]
        return arcpy.MatchLayerSymbologyToAStyle_management(in_layer=self._内嵌对象, match_values=映射关系, in_style=样式文件路径)[0]


class 图层类_10版本:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    @staticmethod
    def 图层创建(图层路径=None):
        return 图层类_10版本(内嵌对象=arcpy.mapping.Layer(图层路径))
