from bxpy.日志包 import 日志类

try:
    import arcpy
except Exception as e:
    pass
from .图层类 import 图层类


class 图层文件类:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    @staticmethod
    def 图层文件读取(文件路径):
        return 图层文件类(arcpy.mp.LayerFile(文件路径))

    def 图层列表读取(self, 筛选通配符="*"):
        图层列表 = self._内嵌对象.listLayers(筛选通配符)
        return [图层类(x) for x in 图层列表]
