from bxpy import 日志
import arcpy
from .地图类 import 地图类


class 布局类:
    class 地图视图类:
        def __init__(self, 内嵌对象=None) -> None:
            self._内嵌对象 = 内嵌对象

        def __repr__(self) -> str:
            return self._内嵌对象.__repr__()

        @property
        def 地图对象(self):
            return 地图类(self._内嵌对象.map)

        @地图对象.setter
        def 地图对象(self, 地图对象):
            self._内嵌对象.map = 地图对象._内嵌对象
            return self

        def 视图缩放到书签(self, 书签对象: 地图类.书签类):
            return self.zoomToBookmark(书签对象._内嵌对象)

    def __init__(self, 内嵌对象=None) -> None:
        self._内嵌对象 = 内嵌对象

    def __repr__(self) -> str:
        return self._内嵌对象.__repr__()

    def 子元素列表读取(self, 筛选通配符="MAPFRAME_ELEMENT"):
        _子元素类型映射表 = {"MAPFRAME_ELEMENT": "MAPFRAME_ELEMENT", "地图视图列表": "MAPFRAME_ELEMENT"}
        子元素列表 = self._内嵌对象.listElements(筛选通配符)
        return [布局类.地图视图类(x) for x in 子元素列表]

    def 导出到PDF(self, 路径):
        return self._内嵌对象.exportToPDF(路径)
