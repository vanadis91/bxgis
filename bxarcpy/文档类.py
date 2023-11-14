from bxpy import 日志
import arcpy
from .地图类 import 地图类
from .布局类 import 布局类


class 文档类:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    def __repr__(self) -> str:
        return f"<bxarcpy.文档类 对象 {{内嵌对象:{self._内嵌对象}}}>"

    @property
    def 默认数据库(self):
        return self.内嵌对象.defaultGeodatabase

    @默认数据库.setter
    def 默认数据库(self, 默认数据库路径):
        self.内嵌对象.defaultGeodatabase = 默认数据库路径

    @property
    def 默认工具箱(self):
        return self.内嵌对象.defaultToolbox

    @默认工具箱.setter
    def 默认工具箱(self, 默认工具箱路径):
        self.内嵌对象.defaultToolbox = 默认工具箱路径

    @property
    def 默认项目文件夹(self):
        return self.内嵌对象.homeFolder

    @默认项目文件夹.setter
    def 默认项目文件夹(self, 默认项目文件夹路径):
        self.内嵌对象.homeFolder = 默认项目文件夹路径

    @staticmethod
    def 文档读取_通过名称(文档路径="CURRENT"):
        return 文档类(内嵌对象=arcpy.mp.ArcGISProject(文档路径))

    def 文档另存为(self, 另存为路径):
        return self._内嵌对象.saveACopy(另存为路径)

    def 文档保存(self):
        return self._内嵌对象.save()

    def 地图列表读取(self, 筛选通配符="") -> list["地图类"]:
        地图列表 = self._内嵌对象.listMaps(筛选通配符)
        return [地图类(x) for x in 地图列表]

    def 布局列表读取(self, 筛选通配符="") -> list:
        布局列表 = self._内嵌对象.listLayouts(筛选通配符)
        return [布局类(x) for x in 布局列表]

    def 地图导入_mxd格式(self, 路径):
        self._内嵌对象.importDocument(路径)
        return self


class 文档类_10版本:
    def __init__(self, 内嵌对象=None):
        self.内嵌对象 = 内嵌对象

    @staticmethod
    def 文档读取(文档路径="CURRENT"):
        return 文档类_10版本(内嵌对象=arcpy.mapping.MapDocument(文档路径))

    def 文档另存为(self, 另存为路径, 版本="10.1"):
        return self.内嵌对象.saveACopy(另存为路径, version=版本)

    def 图层添加(self, 图层对象):
        return arcpy.mapping.AddLayer(self.内嵌对象, 图层对象)
