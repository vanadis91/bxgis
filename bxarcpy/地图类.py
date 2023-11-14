from bxpy import 日志
import arcpy
from .图层类 import 图层类


class 地图类:
    def __init__(self, 内嵌对象=None) -> None:
        self._内嵌对象 = 内嵌对象

    def __repr__(self) -> str:
        return f"<bxarcpy.地图类 对象 {{内嵌对象:{self._内嵌对象}}}>"

    class 书签类:
        def __init__(self, 内嵌对象=None):
            self._内嵌对象 = 内嵌对象

        def __repr__(self) -> str:
            return self._内嵌对象.__repr__()

    def 图层列表读取(self, 筛选通配符="") -> list["图层类"]:
        图层列表 = self._内嵌对象.listLayers(筛选通配符)
        return [图层类(x) for x in 图层列表]

    def 书签列表读取(self, 筛选通配符=""):
        书签列表 = self._内嵌对象.listBookmarks(筛选通配符)
        return [地图类.书签类(x) for x in 书签列表]

    def 图层添加_底图格式(self, 名称="中国地图彩色版"):
        self._内嵌对象.addBasemap(名称)
        return self

    def 图层添加_shp格式(self, 路径):
        self._内嵌对象.addDataFromPath(路径)
        return self

    def 图层添加_lyrx格式(self, 路径):
        图层对象 = arcpy.mp.LayerFile(路径)
        self._内嵌对象.addLayer(图层对象)
        return self

    def 图层添加_图层对象(self, 作为参照的图层对象, 准备插入的图层对象, 关系):
        _关系映射表 = {"上层": "BEFORE", "BEFORE": "BEFORE"}
        关系 = _关系映射表[关系]
        self._内嵌对象.insertLayer(作为参照的图层对象._内嵌对象, 准备插入的图层对象._内嵌对象, 关系)
        return self

    def 图层移除(self, 图层对象):
        self._内嵌对象.removeLayer(图层对象._内嵌对象)

    def 图层顺序调整(self, 作为参照的图层对象, 准备移动的图层对象, 关系):
        _关系映射表 = {"上层": "BEFORE", "BEFORE": "BEFORE"}
        关系 = _关系映射表[关系]
        self._内嵌对象.moveLayer(作为参照的图层对象._内嵌对象, 准备移动的图层对象._内嵌对象, 关系)
        return self


class 地图类_10版本:
    def __init__(self, 内嵌对象=None) -> None:
        self.内嵌对象 = 内嵌对象
        self.比例 = self.内嵌对象.scale
        self.界限 = self.内嵌对象.extent
        self.类型 = self.内嵌对象.type

    def 数据框读取_第一个数据框(文档对象=None):
        return 地图类_10版本(内嵌对象=arcpy.mapping.ListDataFrames(文档对象)[0])
