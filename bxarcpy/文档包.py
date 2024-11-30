from bxpy.日志包 import 日志生成器
import arcpy
from bxpy.日志包 import 日志生成器
from bxarcpy.要素包 import 要素类
from typing import Union, Literal, Any


class 文档类:
    # def __init__(self, 内嵌对象=None):
    #     self._内嵌对象 = 内嵌对象

    # def __repr__(self) -> str:
    #     return f"<bxarcpy.文档类 对象 {{内嵌对象:{self._内嵌对象}}}>"
    @staticmethod
    def 文档读取_通过名称(文档路径="CURRENT"):
        return arcpy.mp.ArcGISProject(文档路径)

    @staticmethod
    def 文档另存为(文档对象: arcpy.mp.ArcGISProject, 另存为路径):
        return 文档对象.saveACopy(另存为路径)

    @staticmethod
    def 文档保存(文档对象: arcpy.mp.ArcGISProject):
        return 文档对象.save()

    @staticmethod
    def 属性获取_默认数据库(文档对象: arcpy.mp.ArcGISProject):
        return 文档对象.defaultGeodatabase

    @staticmethod
    def 属性设置_默认数据库(文档对象: arcpy.mp.ArcGISProject, 默认数据库路径):
        文档对象.defaultGeodatabase = 默认数据库路径

    @staticmethod
    def 属性获取_默认工具箱(文档对象: arcpy.mp.ArcGISProject):
        return 文档对象.defaultToolbox

    @staticmethod
    def 属性设置_默认工具箱(文档对象: arcpy.mp.ArcGISProject, 默认工具箱路径):
        文档对象.defaultToolbox = 默认工具箱路径

    @staticmethod
    def 属性获取_默认项目文件夹(文档对象: arcpy.mp.ArcGISProject):
        return 文档对象.homeFolder

    @staticmethod
    def 属性设置_默认项目文件夹(文档对象: arcpy.mp.ArcGISProject, 默认项目文件夹路径):
        文档对象.homeFolder = 默认项目文件夹路径

    @staticmethod
    def 属性获取_地图列表(文档对象: arcpy.mp.ArcGISProject, 筛选通配符="") -> list:
        地图列表 = 文档对象.listMaps(筛选通配符)
        return 地图列表  # type: ignore

    @staticmethod
    def 属性获取_布局列表(文档对象: arcpy.mp.ArcGISProject, 筛选通配符="") -> list:
        布局列表 = 文档对象.listLayouts(筛选通配符)
        return 布局列表  # type: ignore

    @staticmethod
    def 转换_从mxd格式(文档对象: arcpy.mp.ArcGISProject, 路径):
        文档对象.importDocument(路径)
        return 文档对象

    class 布局类:
        class 地图视图类:
            @staticmethod
            def 属性获取_视图中地图对象(视图对象):
                return 视图对象.map

            @staticmethod
            def 属性设置_视图中地图对象(视图对象, 地图对象):
                视图对象.map = 地图对象

            @staticmethod
            def 视图缩放到书签(视图对象, 书签对象):
                return 视图对象.zoomToBookmark(书签对象)

        @staticmethod
        def 属性获取_子元素列表(布局对象, 筛选通配符="MAPFRAME_ELEMENT"):
            _子元素类型映射表 = {"地图视图列表": "MAPFRAME_ELEMENT"}
            筛选通配符 = _子元素类型映射表.get(筛选通配符, 筛选通配符)
            子元素列表 = 布局对象.listElements(筛选通配符)
            return 子元素列表

        @staticmethod
        def 转换_到pdf(布局对象, 路径):
            return 布局对象.exportToPDF(路径)

    class 地图类:
        # def __init__(self, 内嵌对象=None) -> None:
        #     self._内嵌对象 = 内嵌对象

        # def __repr__(self) -> str:
        #     return f"<bxarcpy.地图类 对象 {{内嵌对象:{self._内嵌对象}}}>"

        @staticmethod
        def 属性获取_图层列表(地图对象, 筛选通配符="") -> list:
            图层列表 = 地图对象.listLayers(筛选通配符)
            return 图层列表

        @staticmethod
        def 属性获取_书签列表(地图对象, 筛选通配符="") -> list:
            书签列表 = 地图对象.listBookmarks(筛选通配符)
            return 书签列表

        @staticmethod
        def 图层添加_底图格式(地图对象, 名称="中国地图彩色版"):
            地图对象.addBasemap(名称)
            return 地图对象

        @staticmethod
        def 图层添加_shp格式(地图对象, 路径):
            地图对象.addDataFromPath(路径)
            return 地图对象

        @staticmethod
        def 图层添加_lyrx格式(地图对象, 路径):
            图层对象 = arcpy.mp.LayerFile(路径)
            地图对象.addLayer(图层对象)
            return 地图对象

        @staticmethod
        def 图层添加_图层对象(地图对象, 准备插入的图层对象, 作为插入位置参照的图层对象, 关系):
            _关系映射表 = {"上层": "BEFORE", "BEFORE": "BEFORE"}
            关系 = _关系映射表[关系]
            地图对象.insertLayer(作为插入位置参照的图层对象, 准备插入的图层对象, 关系)
            return 地图对象

        @staticmethod
        def 图层移除(地图对象, 图层对象):
            地图对象.removeLayer(图层对象)

        @staticmethod
        def 图层顺序调整(地图对象, 准备移动的图层对象, 作为移动位置参照的图层对象, 关系):
            _关系映射表 = {"上层": "BEFORE", "BEFORE": "BEFORE"}
            关系 = _关系映射表[关系]
            地图对象.moveLayer(作为移动位置参照的图层对象, 准备移动的图层对象, 关系)
            return 地图对象

        class 图层类(要素类):
            class 符号系统类:
                pass

            #     def __init__(self, 内嵌对象, 内嵌图层对象):
            #         self._内嵌对象 = 内嵌对象
            #         self._内嵌图层对象 = 内嵌图层对象

            # def 符号系统设置_通过stylx样式文件(self, 样式文件路径):
            #     self._内嵌对象.applySymbologyFromLayer(样式文件路径)
            #     self._内嵌图层对象.refresh()

            # def __init__(self, 内嵌对象=None):
            #     if 内嵌对象:
            #         self._内嵌对象 = 内嵌对象
            #         self.名称 = self._内嵌对象.name

            # def __repr__(self) -> str:
            #     return f"<bxarcpy.图层类 对象 {{名称:{self.名称}}}>"

            @staticmethod
            def 属性获取_符号系统对象(图层对象):
                return 图层对象.symbology

            # @property
            # def 符号系统(self):
            #     return 图层类.符号系统类(self._内嵌对象.symbology, self._内嵌对象)

            @staticmethod
            def 属性设置_符号系统对象(图层对象, 符号系统对象):
                图层对象.symbology = 符号系统对象

            # @符号系统.setter
            # def 符号系统(self, 符号系统):
            #     if type(符号系统) is 图层类.符号系统类:
            #         符号系统 = 符号系统._内嵌对象
            #     self._内嵌对象.symbology = 符号系统

            @staticmethod
            def 类型是否为要素图层(图层对象):
                return 图层对象.isFeatureLayer

            @staticmethod
            def 类型是否为网络图层(图层对象):
                return 图层对象.isWebLayer

            @staticmethod
            def 操作是否被支持(图层对象, 操作名称: Literal["查询语句设置", "最小视图比例设置"] = "查询语句设置"):
                _操作映射表 = {"查询语句设置": "DEFINITIONQUERY", "最小视图比例设置": "minThreshold"}
                操作名称raw = _操作映射表[操作名称] if 操作名称 in _操作映射表 else 操作名称
                return 图层对象.supports(操作名称raw)

            @staticmethod
            def 属性设置_全局查询语句(图层对象, 查询语句="Acres > 5.0"):
                图层对象.definitionQuery = 查询语句
                return 图层对象

            @staticmethod
            def 属性设置_最小视图比例(图层对象, 视图比例: int):
                图层对象.minThreshold = 视图比例
                return 图层对象

            @staticmethod
            def 属性设置_符号系统_通过图层文件(图层对象, 符号系统图层对象, 符号系统字段=[["值字段", "符号系统图层的字段", "输入图层的字段"]], 按数据更新符号系统范围="默认"):
                _符号系统字段类型映射表 = {"值字段": "VALUE_FIELD"}
                符号系统字段temp = []
                for x in 符号系统字段:
                    if x[0] in _符号系统字段类型映射表:
                        符号系统字段temp.append([_符号系统字段类型映射表[x[0]], x[1], x[2]])
                    else:
                        符号系统字段temp.append(x)
                符号系统字段 = 符号系统字段temp

                _按数据更新符号系统范围映射表 = {"默认": "DEFAULT", "更新范围": "UPDATE", "保留范围": "MAINTAIN"}
                按数据更新符号系统范围 = _按数据更新符号系统范围映射表[按数据更新符号系统范围] if 按数据更新符号系统范围 in _按数据更新符号系统范围映射表 else 按数据更新符号系统范围

                新建图层 = arcpy.management.ApplySymbologyFromLayer(in_layer=图层对象, in_symbology_layer=符号系统图层对象, symbology_fields=符号系统字段, update_symbology=按数据更新符号系统范围)[0]  # type: ignore
                文档类.地图类.图层类.属性设置_符号系统对象(图层对象, 文档类.地图类.图层类.属性获取_符号系统对象(新建图层))
                return 图层对象

            @staticmethod
            def 属性设置_符号系统_通过STYLX样式文件(图层对象, 匹配字段="地类编号", 样式文件路径=r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx"):
                新建图层 = arcpy.management.MatchLayerSymbologyToAStyle(in_layer=图层对象, match_values=匹配字段, in_style=样式文件路径)[0]  # type: ignore
                文档类.地图类.图层类.属性设置_符号系统对象(图层对象, 文档类.地图类.图层类.属性获取_符号系统对象(新建图层))
                return 图层对象

        class 书签类:
            pass


class 图层文件类:
    # def __init__(self, 内嵌对象=None):
    #     self._内嵌对象 = 内嵌对象

    @staticmethod
    def 图层文件读取(文件路径):
        return arcpy.mp.LayerFile(文件路径)

    @staticmethod
    def 属性获取_图层列表(图层文件: arcpy.mp.LayerFile, 筛选通配符="*"):
        图层列表 = 图层文件.listLayers(筛选通配符)
        return 图层列表


class 文档类_10版本:
    # def __init__(self, 内嵌对象=None):
    #     self.内嵌对象 = 内嵌对象

    @staticmethod
    def 文档读取_通过名称(文档路径="CURRENT"):
        return arcpy.mapping.MapDocument(文档路径)  # type: ignore

    @staticmethod
    def 文档另存为(文档对象, 另存为路径, 版本="10.1"):
        return 文档对象.saveACopy(另存为路径, version=版本)

    @staticmethod
    def 图层添加(文档对象, 图层对象):
        return 文档对象.AddLayer(文档对象, 图层对象)

    class 地图类:
        @staticmethod
        def 属性获取_比例(地图对象):
            return 地图对象.scale

        @staticmethod
        def 属性获取_界限(地图对象):
            return 地图对象.extent

        @staticmethod
        def 属性获取_类型(地图对象):
            return 地图对象.type

        @staticmethod
        def 数据框读取_第一个数据框(文档对象):
            return arcpy.mapping.ListDataFrames(文档对象)[0]  # type: ignore

        class 图层类:
            # def __init__(self, 内嵌对象=None):
            #     self._内嵌对象 = 内嵌对象

            @staticmethod
            def 图层创建(图层路径=None):
                return arcpy.mapping.Layer(图层路径)  # type: ignore
