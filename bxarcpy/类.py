import arcpy
import time

_字段类型映射 = {"字符串": "TEXT", "TEXT": "TEXT", "双精度": "DOUBLE", "DOUBLE": "DOUBLE", "长整型": "LONG", "LONG": "LONG", "短整型": "SHORT", "SHORT": "SHORT", "日期": "DATE", "DATE": "DATE", "单精度": "FLOAT", "FLOAT": "FLOAT"}


class _配置类:
    _单例对象 = None

    def __new__(cls, *args, **kwargs):
        if cls._单例对象 is None:
            cls._单例对象 = super().__new__(cls)
        return cls._单例对象

    def __init__(self) -> None:
        pass

    @property
    def 是否覆盖输出要素(self):
        return arcpy.env.overwriteOutput

    @是否覆盖输出要素.setter
    def 是否覆盖输出要素(self, boolen):
        arcpy.env.overwriteOutput = boolen

    @property
    def 当前工作空间(self):
        return arcpy.env.workspace

    @当前工作空间.setter
    def 当前工作空间(self, 工作空间路径=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"):
        arcpy.env.workspace = 工作空间路径


配置 = _配置类()


class 环境:
    class 环境管理器(object):
        def __init__(self, 输出包含M值="Disabled", 输出包含Z值="Disabled", **kwargs):
            _参数映射 = {"临时工作空间": "scratchWorkspace", "scratchWorkspace": "scratchWorkspace", "工作空间": "workspace", "workspace": "workspace", "输出包含M值": "outputMFlag", "outputMFlag": "outputMFlag", "输出包含Z值": "outputZFlag", "outputZFlag": "outputZFlag"}
            kwargsTemp = {}
            for key, value in kwargs.items():
                kwargsTemp[_参数映射[key]] = value
            kwargs = kwargsTemp
            kwargs["outputMFlag"] = 输出包含M值
            kwargs["outputZFlag"] = 输出包含Z值

            self._original_envs = {}
            self._environments = kwargs

        def __enter__(self):
            envs = list(arcpy.env._environments) + ["autoCancelling", "overwriteOutput"]

            # Handle invalid keys and read-only environments
            for k in self._environments.keys():
                if k not in envs:
                    msg = arcpy.GetIDMessage(87059).replace("%1", "%s") % k
                    raise AttributeError(msg)
                elif k in ["scratchGDB", "scratchFolder"]:
                    msg = arcpy.GetIDMessage(87064).replace("%1", "%s") % k
                    raise AttributeError(msg)

            for k, v in self._environments.items():
                if k in envs:
                    self._original_envs[k] = getattr(arcpy.env, k)
                    setattr(arcpy.env, k, v)

        def __exit__(self, exc_type, exc_value, traceback):
            self.reset()

        def reset(self):
            for k, v in self._original_envs.items():
                setattr(arcpy.env, k, v)

    @staticmethod
    def 输入参数获取_以字符串形式(索引):
        return arcpy.GetParameterAsText(索引)


class 文档类:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    def __repr__(self) -> str:
        return self._内嵌对象.__repr__()

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
    def 文档读取(文档路径="CURRENT"):
        return 文档类(内嵌对象=arcpy.mp.ArcGISProject(文档路径))

    def 文档另存为(self, 另存为路径):
        return self._内嵌对象.saveACopy(另存为路径)

    def 文档保存(self):
        return self._内嵌对象.save()

    def 地图列表读取(self, 筛选通配符="") -> list:
        地图列表 = self._内嵌对象.listMaps(筛选通配符)
        return [地图类(x) for x in 地图列表]

    def 布局列表读取(self, 筛选通配符="") -> list:
        布局列表 = self._内嵌对象.listLayouts(筛选通配符)
        return [布局类(x) for x in 布局列表]

    def 地图导入_mxd格式(self, 路径):
        self._内嵌对象.importDocument(路径)
        return self


class 地图类:
    def __init__(self, 内嵌对象=None) -> None:
        self._内嵌对象 = 内嵌对象

    def __repr__(self) -> str:
        return self._内嵌对象.__repr__()

    class 书签类:
        def __init__(self, 内嵌对象=None):
            self._内嵌对象 = 内嵌对象

        def __repr__(self) -> str:
            return self._内嵌对象.__repr__()

    def 图层列表读取(self, 筛选通配符=""):
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


class 图层文件类:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    @staticmethod
    def 图层文件读取(文件路径):
        return 图层文件类(arcpy.mp.LayerFile(文件路径))

    def 图层列表读取(self, 筛选通配符=""):
        图层列表 = self._内嵌对象.listLayers(筛选通配符)
        return [图层类(x) for x in 图层列表]


class 数据库类:
    def __init__(self, 路径=None):
        self.路径 = 路径
        arcpy.env.workspace = self.路径

    @staticmethod
    def 数据库读取_通过路径(路径=None):
        return 数据库类(路径=路径)

    @staticmethod
    def 要素名称列表获取():
        return arcpy.ListFeatureClasses()

    @staticmethod
    def 要素数据集列表获取():
        return arcpy.ListDatasets()

    @staticmethod
    def 文件列表获取():
        return arcpy.ListFiles()

    @staticmethod
    def 栅格列表获取():
        return arcpy.ListRasters()


class 要素数据集类:
    def __init__(self, 内嵌对象=None, 名称=None):
        if 内嵌对象:
            self.名称 = 内嵌对象.名称
        elif 名称:
            self.名称 = 名称

    @staticmethod
    def 要素数据集创建(要素集名称, 数据库路径=None):
        if 数据库路径 is None:
            数据库路径 = 配置.当前工作空间
        路径 = arcpy.management.CreateFeatureDataset(out_dataset_path=数据库路径, out_name=要素集名称, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]
        return 要素数据集类(名称=路径)

    def 要素数据集删除(self):
        return arcpy.management.Delete(in_data=[self.名称], data_type="")[0]

    @staticmethod
    def 导入从CAD(CAD路径列表, 输出要素数据集名称):
        arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD路径列表, out_gdb_path=配置.当前工作空间, out_dataset_name=输出要素数据集名称, reference_scale=1000, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]
        return 要素数据集类(名称=输出要素数据集名称)


class 拓扑类:
    def __init__(self, 内嵌对象=None, 名称=None) -> None:
        if 内嵌对象:
            self.名称 = 内嵌对象.名称
        elif 名称:
            self.名称 = 名称

    def 拓扑创建(要素数据集名称=None, 拓扑名称=None):
        return 拓扑类(名称=arcpy.management.CreateTopology(in_dataset=要素数据集名称, out_name=拓扑名称, in_cluster_tolerance=None)[0])

    def 拓扑中添加要素(self, 输入要素名称):
        arcpy.management.AddFeatureClassToTopology(in_topology=self.名称, in_featureclass=输入要素名称, xy_rank=1, z_rank=1)[0]
        return self

    def 拓扑中添加规则(self, 输入要素名称=None, 规则="Must Not Overlap (Area)"):
        arcpy.management.AddRuleToTopology(in_topology=self.名称, rule_type=规则, in_featureclass=输入要素名称, subtype="", in_featureclass2="", subtype2="")[0]
        return self

    def 拓扑验证(self):
        arcpy.management.ValidateTopology(in_topology=self.名称, visible_extent="Full_Extent")[0]
        return self

    def 导出到要素(self, 输出要素名称="AA_拓扑导出后要素"):
        arcpy.management.ExportTopologyErrors(self.名称, 配置.当前工作空间, 输出要素名称)
        return (
            要素类(名称=输出要素名称 + "_point"),
            要素类(名称=输出要素名称 + "_line"),
            要素类(名称=输出要素名称 + "_poly"),
        )


class 要素类:
    def __init__(self, 内嵌对象=None, 名称=None):
        if 内嵌对象:
            self.名称 = 内嵌对象.路径
        elif 名称:
            self.名称 = 名称

    def __repr__(self) -> str:
        return f"<bxarcpy.要素类 对象 {{名称:{self.名称}}}>"

    @staticmethod
    def 要素读取_通过名称(名称=None):
        return 要素类(名称=名称)

    def 要素创建_通过复制(self, 输出要素名称="in_memory\\AA_复制"):
        if 输出要素名称 == "in_memory\\AA_复制":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)
        return 要素类(名称=输出要素名称)

    def 要素创建_通过复制并重命名重名要素(self, 输出要素名称="in_memory\\AA_复制"):
        if 输出要素名称 == "in_memory\\AA_复制":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        database = 数据库类.数据库读取_通过路径(配置.当前工作空间)
        要素名称列表 = database.要素名称列表获取()
        if 输出要素名称 in 要素名称列表:
            重命名后名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
            print(f"重名要素被命名为：{重命名后名称}")
            要素类.要素读取_通过名称(输出要素名称).要素创建_通过复制(重命名后名称)
        arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)
        return 要素类(名称=输出要素名称)

    def 要素创建_通过合并(self, 输入要素名称列表=[], 输出要素名称="in_memory\\AA_合并"):
        _输入要素路径列表 = [self.名称]
        _输入要素路径列表.extend(输入要素名称列表)
        if 输出要素名称 == "in_memory\\AA_合并":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.management.Merge(inputs=_输入要素路径列表, output=输出要素名称, field_mappings="", add_source="NO_SOURCE_INFO")
        return 要素类(名称=输出要素名称)

    def 要素创建_通过裁剪(self, 裁剪要素名称, 输出要素名称="in_memory\\AA_裁剪"):
        if 输出要素名称 == "in_memory\\AA_裁剪":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.analysis.Clip(in_features=self.名称, clip_features=裁剪要素名称, out_feature_class=输出要素名称, cluster_tolerance="")
        return 要素类(名称=输出要素名称)

    def 要素创建_通过擦除(self, 擦除要素名称, 输出要素名称="in_memory\\AA_擦除"):
        if 输出要素名称 == "in_memory\\AA_擦除":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.analysis.Erase(in_features=self.名称, erase_features=擦除要素名称, out_feature_class=输出要素名称, cluster_tolerance="")
        return 要素类(名称=输出要素名称)

    def 要素创建_通过擦除并几何修复(self, 擦除要素名称, 输出要素名称="in_memory\\AA_擦除并几何修复"):
        if 输出要素名称 == "in_memory\\AA_擦除并几何修复":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        输入 = self.要素几何修复()
        擦除 = 要素类.要素读取_通过名称(擦除要素名称).要素几何修复()
        arcpy.analysis.Erase(in_features=输入.名称, erase_features=擦除.名称, out_feature_class=输出要素名称, cluster_tolerance="")
        return 要素类(名称=输出要素名称)

    def 要素创建_通过相交(self, 输入要素名称列表=[], 输出要素路径="in_memory\\AA_相交"):
        _输入要素路径列表 = [self.名称]
        _输入要素路径列表.extend(输入要素名称列表)
        if 输出要素路径 == "in_memory\\AA_相交":
            输出要素路径 = 输出要素路径 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        _输入要素路径列表 = [[x, ""] for x in _输入要素路径列表]
        arcpy.analysis.Intersect(in_features=_输入要素路径列表, out_feature_class=输出要素路径, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")
        return 要素类(名称=输出要素路径)

    def 要素创建_通过联合(self, 输入要素名称列表=[], 输出要素名称="in_memory\\AA_联合", 是否保留周长和面积=False):
        _输入要素名称列表 = [self.名称]
        _输入要素名称列表.extend(输入要素名称列表)
        if 输出要素名称 == "in_memory\\AA_联合":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        _输入要素名称列表 = [[x, ""] for x in _输入要素名称列表]
        arcpy.analysis.Union(in_features=_输入要素名称列表, out_feature_class=输出要素名称, join_attributes="ALL", cluster_tolerance="", gaps="GAPS")
        联合后要素 = 要素类(名称=输出要素名称)
        if 是否保留周长和面积 is False:
            字段名称列表 = 联合后要素.字段名称列表获取()
            for 字段名称 in 字段名称列表:
                if "Shape_Length" in 字段名称 or "Shape_Area" in 字段名称:
                    联合后要素.字段删除([字段名称])
        return 联合后要素

    def 要素创建_通过融合(self, 输出要素名称="in_memory\\AA_融合", 融合字段列表=[], 统计字段列表=None):
        if 输出要素名称 == "in_memory\\AA_融合":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.management.Dissolve(in_features=self.名称, out_feature_class=输出要素名称, dissolve_field=融合字段列表, statistics_fields=统计字段列表, multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES", concatenation_separator="")
        return 要素类(名称=输出要素名称)

    def 要素创建_通过更新并合并字段(self, 更新要素名称, 输出要素名称="in_memory\\AA_更新并合并字段"):
        if 输出要素名称 == "in_memory\\AA_更新并合并字段":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        输出 = self.要素创建_通过擦除并几何修复(更新要素名称)
        输出 = 输出.要素创建_通过合并([更新要素名称], 输出要素名称)
        return 输出

    def 要素创建_通过筛选(self, SQL语句="", 输出要素名称="in_memory\\AA_筛选"):
        if 输出要素名称 == "in_memory\\AA_筛选":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.analysis.Select(in_features=self.名称, out_feature_class=输出要素名称, where_clause=SQL语句)
        return 要素类(名称=输出要素名称)

    def 要素创建_通过多部件至单部件(self, 输出要素路径="in_memory\\AA_多部件至单部件"):
        if 输出要素路径 == "in_memory\\AA_多部件至单部件":
            输出要素路径 = 输出要素路径 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        输出要素路径 = arcpy.management.MultipartToSinglepart(in_features=self.名称, out_feature_class=输出要素路径)
        return 要素类(名称=输出要素路径)

    def 要素创建_通过空间连接(self, 连接要素名称, 输出要素名称="in_memory\\AA_空间连接", 连接方式="包含连接要素") -> "要素类":
        _连接方式映射表 = {"INTERSECT": "INTERSECT", "相交": "INTERSECT", "CONTAINS": "CONTAINS", "包含连接要素": "CONTAINS", "COMPLETELY_CONTAINS": "COMPLETELY_CONTAINS", "完全包含连接要素": "COMPLETELY_CONTAINS", "在连接要素内": "WITHIN", "WITHIN": "WITHIN", "完全在连接要素内": "COMPLETELY_WITHIN", "COMPLETELY_WITHIN": "COMPLETELY_WITHIN", "包含连接要素内点": "包含连接要素内点", "内点在连接要素内": "内点在连接要素内"}
        连接方式 = _连接方式映射表[连接方式]
        if 输出要素名称 == "in_memory\\AA_空间连接":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        if 连接方式 == "包含连接要素内点":
            连接要素转内点后名称 = arcpy.management.FeatureToPoint(in_features=连接要素名称, out_feature_class="in_memory\\AA_要素转点" + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime()), point_location="INSIDE")
            return self.要素创建_通过空间连接(连接要素转内点后名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
        if 连接方式 == "内点在连接要素内":
            目标要素转内点后名称 = arcpy.management.FeatureToPoint(in_features=self.名称, out_feature_class="in_memory\\AA_要素转点" + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime()), point_location="INSIDE")
            目标要素 = 要素类.要素读取_通过名称(目标要素转内点后名称)
            目标要素连接后 = 目标要素.要素创建_通过空间连接(连接要素名称, "in_memory\\AA_空间连接", "在连接要素内")
            return self.要素创建_通过空间连接(目标要素连接后.名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
        arcpy.analysis.SpatialJoin(
            target_features=self.名称,
            join_features=连接要素名称,
            out_feature_class=输出要素名称,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            # field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,YD_用地\\YD_不动产登记2,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,YD_用地\\YD_不动产登记2,Shape_Area,-1,-1;地类编号 "地类编号" true true false 50 Text 0 0,First,#,YD_用地\\YD_不动产登记2,地类编号,0,50;Shape_Length_1 "Shape_Length" true true true 8 Double 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,Shape_Length,-1,-1;Shape_Area_1 "Shape_Area" true true true 8 Double 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,Shape_Area,-1,-1;地类编号_1 "地类编号" true true false 100 Text 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,地类编号,0,100;ORIG_FID "ORIG_FID" true true false 0 Long 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,ORIG_FID,-1,-1',
            match_option=连接方式,
            search_radius="",
            distance_field_name="",
        )
        return 要素类(名称=输出要素名称)

    def 要素创建_通过填充空隙(self, 填充范围要素名称, 填充地类编号表达式='"00"', 输出要素名称="in_memory\\AA_填充空隙"):
        # 常用_填充空隙后
        # To allow overwriting outputs change overwriteOutput option to True.
        if 输出要素名称 == "in_memory\\AA_填充空隙":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())

        # Process: 复制要素 (复制要素) (management)
        顶部元素 = 要素类.要素读取_通过名称(self.名称).要素创建_通过复制()
        填充范围1 = 要素类.要素读取_通过名称(填充范围要素名称).要素创建_通过复制()
        填充范围1.字段添加("地类编号").字段计算("地类编号", 填充地类编号表达式)
        ret = 填充范围1.要素创建_通过更新并合并字段(顶部元素.名称, 输出要素名称)
        return ret

    def 要素创建_通过切分(self, 折点数量=200, 输出要素名称="in_memory\\AA_切分"):
        if 输出要素名称 == "in_memory\\AA_切分":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        ret = arcpy.management.Dice(self.名称, 输出要素名称, 折点数量)
        return 要素类(名称=ret)

    def 要素删除(self):
        return arcpy.management.Delete(in_data=[self.名称], data_type="")[0]

    @staticmethod
    def 要素删除_通过要素名称列表(要素名称列表):
        return arcpy.management.Delete(in_data=要素名称列表, data_type="")[0]

    def 要素几何修复(self):
        arcpy.management.RepairGeometry(in_features=self.名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]
        return self

    def 选择集创建_通过属性(self, 选择方式="新建选择集", SQL语句=""):
        _选择方式映射表 = {"新建选择集": "NEW_SELECTION", "NEW_SELECTION": "NEW_SELECTION"}
        选择方式 = _选择方式映射表[选择方式]
        a = arcpy.management.SelectLayerByAttribute(in_layer_or_view=self.名称, selection_type=选择方式, where_clause=SQL语句, invert_where_clause="")[0]
        return 图层类(a)

    def 字段列表获取(self):
        return [字段类(x) for x in arcpy.ListFields(self.名称)]

    def 字段名称列表获取(self):
        字段列表 = self.字段列表获取()
        return [x.名称 for x in 字段列表]

    def 字段删除(self, 删除字段名称列表=None, 保留字段名称列表=None):
        from bxpy import 调试

        if 保留字段名称列表 is None:
            arcpy.management.DeleteField(in_table=self.名称, drop_field=删除字段名称列表, method="DELETE_FIELDS")[0]
        elif 删除字段名称列表 is None:
            字段对象列表 = 要素类(名称=self.名称).字段列表获取()
            字段名称列表 = [x.名称 for x in 字段对象列表]
            调试.输出调试(f"要素拥有的所有字段为：" + str(字段名称列表))
            保留字段名称列表.extend(["OBJECTID", "OBJECTID_1", "Shape", "Shape_Area", "Shape_Length"])
            for x in 保留字段名称列表:
                if x in 字段名称列表:
                    字段名称列表.remove(x)
            调试.输出调试(f"除去保留字段列表后剩余的所有字段为：" + str(字段名称列表))
            if 字段名称列表:
                arcpy.management.DeleteField(in_table=self.名称, drop_field=字段名称列表, method="DELETE_FIELDS")[0]
        return self

    def 字段添加(self, 字段名称, 字段类型="字符串", 字段长度=100, 字段别称=""):
        字段类型 = _字段类型映射[字段类型]
        arcpy.management.DeleteField(in_table=self.名称, drop_field=[字段名称], method="DELETE_FIELDS")
        arcpy.management.AddField(in_table=self.名称, field_name=字段名称, field_type=字段类型, field_precision=None, field_scale=None, field_length=字段长度, field_alias=字段别称, field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
        return self

    def 字段计算(self, 字段名称, 表达式, 字段类型="字符串", 语言类型="PYTHON3", 代码块=""):
        字段类型 = _字段类型映射[字段类型]
        arcpy.management.CalculateField(in_table=self.名称, field=字段名称, expression=表达式, expression_type=语言类型, code_block=代码块, field_type=字段类型, enforce_domains="NO_ENFORCE_DOMAINS")[0]
        return self

    def 字段修改(self, 字段名称=None, 修改后字段名称=None, 修改后字段别称=None, 字段类型=None, 字段长度=None, 清除字段别称=True):
        if 字段类型:
            字段类型 = _字段类型映射[字段类型]
        arcpy.management.AlterField(in_table=self.名称, field=字段名称, new_field_name=修改后字段名称, new_field_alias=修改后字段别称, field_type=字段类型, field_length=字段长度, field_is_nullable="NULLABLE", clear_field_alias=清除字段别称)[0]
        return self

    def 连接创建(self, 输入要素连接字段名称=None, 连接要素名称=None, 连接要素连接字段名称=None):
        arcpy.management.AddJoin(in_layer_or_view=self.名称, in_field=输入要素连接字段名称, join_table=连接要素名称, join_field=连接要素连接字段名称, join_type="KEEP_ALL", index_join_fields="NO_INDEX_JOIN_FIELDS")[0]
        return self

    def 连接取消(self, 连接要素名称):
        arcpy.management.RemoveJoin(in_layer_or_view=self.名称, join_name=连接要素名称)[0]
        return self

    def 导出到CAD(self, 输出路径):
        return arcpy.conversion.ExportCAD(in_features=self.名称, Output_Type="DWG_R2010", Output_File=输出路径, Ignore_FileNames="Ignore_Filenames_in_Tables", Append_To_Existing="Overwrite_Existing_Files", Seed_File="")

    def 导出到要素(self, 输出要素名称):
        # arcpy.conversion.FeatureClassToFeatureClass(in_features=self.名称, out_path=输出目录, out_name=输出文件名, where_clause="", field_mapping="", config_keyword="")[0]
        arcpy.conversion.ExportFeatures(in_features=self.名称, out_features=输出要素名称, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping=None, sort_field=[])
        return 要素类(名称=输出要素名称)


class 字段类:
    def __init__(self, 内嵌对象) -> None:
        self.内嵌对象 = 内嵌对象
        self.名称 = self.内嵌对象.name
        self.类型 = self.内嵌对象.type
        self.长度 = self.内嵌对象.length

    def __repr__(self) -> str:
        return f"<对象 bxarcpy.字段类 {{名称:{self.名称}, 类型:{self.类型}, 长度:{self.长度}}}>"


class 游标类_用于更新:
    _需更新的字段名称列表映射表 = {"SHAPE@": "SHAPE@", "_形状": "SHAPE@"}

    class 行对象:
        def __init__(self, 行数据, 游标对象: "游标类_用于更新") -> None:
            self.数据_字典格式 = {}
            self.数据_列表格式 = []
            self._内嵌对象_游标对象 = 游标对象
            for k, v in zip(游标对象.字段名称列表, 行数据):
                if k == "_形状":
                    self.数据_列表格式.append(游标类_用于更新.形状(v))
                    self.数据_字典格式[k] = 游标类_用于更新.形状(v)
                else:
                    self.数据_列表格式.append(v)
                    self.数据_字典格式[k] = v
            # self.数据_字典格式 = {k: v for k, v in zip(self._内嵌对象_游标对象.字段名称列表, 行数据)}

        def 行删除(self):
            return self._内嵌对象_游标对象._内嵌对象.deleteRow()

        def 行更新_列表格式(self):
            用于更新的列表 = []
            for k, v in zip(self._内嵌对象_游标对象.字段名称列表, self.数据_列表格式):
                if k == "_形状":
                    用于更新的列表.append(v._内嵌对象)
                else:
                    用于更新的列表.append(v)
            return self._内嵌对象_游标对象._内嵌对象.updateRow(用于更新的列表)

        def 行更新_字典格式(self):
            用于更新的列表 = []
            for k in self._内嵌对象_游标对象.字段名称列表:
                if k == "_形状":
                    用于更新的列表.append(self.数据_字典格式[k]._内嵌对象)
                else:
                    用于更新的列表.append(self.数据_字典格式[k])
            return self._内嵌对象_游标对象._内嵌对象.updateRow(用于更新的列表)

    class 形状:
        _类型映射表 = {"polyline": "线", "polygon": "面"}

        def __init__(self, 内嵌对象) -> None:
            # print(f"形状类：{内嵌对象.__class__}")
            self._内嵌对象 = 内嵌对象

        @property
        def 类型(self):
            类型 = self._内嵌对象.type
            return 游标类_用于更新.形状._类型映射表[类型]

        @property
        def 点表(self):
            return self._内嵌对象.getPart()

        @property
        def 折点数量(self):
            return self._内嵌对象.pointCount

        @property
        def 面积(self):
            return self._内嵌对象.area

        def 是否具有孔洞(self):
            return self._内嵌对象.hasOmittedBoundary

        @property
        def 孔洞数量(self):
            折点和孔洞数量总数 = 0
            for 每个部件x in self._内嵌对象.getPart():
                折点和孔洞数量 = len(每个部件x)
                折点和孔洞数量总数 += 折点和孔洞数量
            return 折点和孔洞数量总数 - self.折点数量

        # @property
        # def 孔洞数量(self):
        #     return self._内嵌对象.interiorRingCount()

        def 是否为多部件要素(self):
            return self._内嵌对象.isMultipart

        @property
        def 部件数量(self):
            return self._内嵌对象.partCount

        # def 边界部件获取(self, 索引):
        #     return self._内嵌对象[索引]

        # def 边界组成数量(self):
        #     return self._内嵌对象.getPartCount()

    def __init__(self, 输入要素名称, 需更新的字段名称列表):
        self.字段名称列表 = 需更新的字段名称列表
        需更新的字段名称列表temp = []
        for x in 需更新的字段名称列表:
            if x in 游标类_用于更新._需更新的字段名称列表映射表:
                需更新的字段名称列表temp.append(游标类_用于更新._需更新的字段名称列表映射表[x])
            else:
                需更新的字段名称列表temp.append(x)
        需更新的字段名称列表 = 需更新的字段名称列表temp

        self._内嵌对象 = arcpy.da.UpdateCursor(输入要素名称, 需更新的字段名称列表)

    def __enter__(self):
        self._内嵌对象 = self._内嵌对象.__enter__()
        return self

    def __exit__(self, 异常类型, 异常值, 追溯信息):
        # 如果__exit__返回值为True,代表吞掉了异常，继续运行
        # 如果__exit__返回值不为True,代表吐出了异常
        return self._内嵌对象.__exit__(异常类型, 异常值, 追溯信息)

    def __iter__(self):
        return self

    def __next__(self):
        行数据 = self._内嵌对象.__next__()
        行对象 = 游标类_用于更新.行对象(行数据, self)
        return 行对象

    def 下一个(self):
        return self.__next__()

    def 重置(self):
        行数据 = self._内嵌对象.reset()
        行对象 = 游标类_用于更新.行对象(行数据, self._内嵌对象)
        return 行对象


class 图层类(要素类):
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象
        self.名称 = self._内嵌对象.name

    def __repr__(self) -> str:
        return self._内嵌对象.__repr__()

    @property
    def 符号系统(self):
        return self._内嵌对象.symbology

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

    def 符号系统设置_通过stylx样式文件(self, 样式文件路径, 映射关系="$feature.JQYDDM"):
        return arcpy.management.MatchLayerSymbologyToAStyle(in_layer=self._内嵌对象, match_values=映射关系, in_style=样式文件路径)[0]


class 转换:
    @staticmethod
    def 拓扑导出到要素(拓扑对象: 拓扑类, 输出要素名称="AA_拓扑导出后要素"):
        return 拓扑对象.导出到要素(输出要素名称)

    @staticmethod
    def 要素导出到CAD(要素对象: 要素类, 输出路径):
        return 要素对象.导出到CAD(输出路径)

    @staticmethod
    def 要素导出到要素(要素对象: 要素类, 输出目录=None, 输出文件名=None):
        return 要素对象.导出到要素(输出目录, 输出文件名)

    @staticmethod
    def 要素数据集导入从CAD(CAD路径列表, 输出要素数据集名称):
        return 要素数据集类.导入从CAD(CAD路径列表, 输出要素数据集名称)

    @staticmethod
    def 布局导出到PDF(布局对象: 布局类, PDF路径):
        return 布局对象.导出到PDF(PDF路径)


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


class 地图类_10版本:
    def __init__(self, 内嵌对象=None) -> None:
        self.内嵌对象 = 内嵌对象
        self.比例 = self.内嵌对象.scale
        self.界限 = self.内嵌对象.extent
        self.类型 = self.内嵌对象.type

    def 数据框读取_第一个数据框(文档对象=None):
        return 地图类_10版本(内嵌对象=arcpy.mapping.ListDataFrames(文档对象)[0])


class 图层类_10版本:
    def __init__(self, 内嵌对象=None):
        self._内嵌对象 = 内嵌对象

    @staticmethod
    def 图层创建(图层路径=None):
        return 图层类_10版本(内嵌对象=arcpy.mapping.Layer(图层路径))


# def 视图刷新():
#     arcpy.RefreshTOC()
#     arcpy.RefreshActiveView()


if __name__ == "__main__":
    # 配置.设置当前工作空间(工作空间路径=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb")
    # 获取要素类列表 = 数据库.获取要素类列表()
    # 字段x = 要素类.获取字段列表(获取要素类列表[0])[0]
    # print(字段x.name)
    # print(type(字段x))
    # a.是否覆盖输出要素 = True
    # print(a.是否覆盖输出要素)
    # print(arcpy.env.overwriteOutput)
    # a.是否覆盖输出要素 = False
    # print(a.是否覆盖输出要素)
    # print(arcpy.env.overwriteOutput)
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # with 环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
    #     配置.是否覆盖输出要素 = True
    #     # 目标要素 = 要素类.要素读取_通过名称("YD_不动产登记2")
    #     # 连接要素 = 要素类.要素读取_通过名称("YD_基期")
    #     # 目标要素.要素创建_通过空间连接(连接要素.名称, "AA_空间连接1", "内点在连接要素内")
    #     目标要素 = 要素类.要素读取_通过名称("DIST_用地现状图")
    #     中间要素 = 目标要素.要素创建_通过更新并合并字段("DIST_用地现状图_Dice")
    #     中间要素 = 中间要素.要素创建_通过更新并合并字段("DIST_用地现状图_Dissolve1", "AA_用于输出CAD")
    pass
