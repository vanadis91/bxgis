from bxpy import 日志
import arcpy
import time


class 要素类:
    def __init__(self, 内嵌对象=None, 名称=None):
        if type(内嵌对象) is 要素类:
            self.名称 = 内嵌对象.名称
        elif 名称:
            self.名称 = 名称

    def __repr__(self) -> str:
        return f"<bxarcpy.要素类 对象 {{名称:{self.名称}}}>"

    @property
    def 几何类型(self):
        from . import 常量

        几何类型 = arcpy.Describe(self.名称).shapeType
        return 常量._要素类型反映射[几何类型.upper()]

    @staticmethod
    def 要素读取_通过名称(名称=None):
        return 要素类(名称=名称)

    @staticmethod
    def 要素创建_通过名称(要素名称="AA_新建", 要素类型="面", 模板=None, 数据库路径="in_memory"):
        from .配置类 import 配置
        from . import 常量

        if 要素名称 == "AA_新建":
            要素名称 = 要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        if 数据库路径 is None:
            数据库路径 = 配置.当前工作空间
        elif 数据库路径.upper() in ["临时", "IN_MEMORY", "MEMORY"]:
            数据库路径 = "in_memory"
        要素类型 = 常量._要素类型映射[要素类型]
        arcpy.management.CreateFeatureclass(out_path=数据库路径, out_name=要素名称, geometry_type=要素类型, template=模板, has_m="DISABLED", has_z="DISABLED", spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];526761.4357525 3337536.7866275 209129662504.711;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision', config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0, out_alias="")
        ret = 要素类.要素读取_通过名称(名称=数据库路径 + "\\" + 要素名称)
        # if 数据库路径.upper() in ["临时", "IN_MEMORY", "MEMORY"]:
        #     ret = ret.要素创建_通过复制并重命名重名要素(f"in_memory\\{要素名称}")
        return ret

    def 要素创建_通过复制(self, 输出要素名称="in_memory\\AA_复制"):
        if 输出要素名称 == "in_memory\\AA_复制":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)
        return 要素类(名称=输出要素名称)

    def 要素创建_通过复制并重命名重名要素(self, 输出要素名称="in_memory\\AA_复制"):
        from .数据库类 import 数据库类
        from .配置类 import 配置
        from .环境 import 环境

        if 输出要素名称 == "in_memory\\AA_复制":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        database = 数据库类.数据库读取_通过路径(配置.当前工作空间)
        要素名称列表 = database.要素名称列表获取()
        if 输出要素名称 in 要素名称列表:
            重命名后名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
            环境.输出消息(f"重名要素被命名为：{重命名后名称}")
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

    def 要素创建_通过融合(self, 融合字段列表=[], 统计字段列表=None, 是否单部件=True, 输出要素名称="in_memory\\AA_融合"):
        if 输出要素名称 == "in_memory\\AA_融合":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        if 是否单部件 == True:
            是否单部件 = "SINGLE_PART"
        else:
            是否单部件 = "MULTI_PART"
        arcpy.management.Dissolve(in_features=self.名称, out_feature_class=输出要素名称, dissolve_field=融合字段列表, statistics_fields=统计字段列表, multi_part=是否单部件, unsplit_lines="DISSOLVE_LINES", concatenation_separator="")
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

    def 要素创建_通过排序(self, 排序字段及顺序列表=[["DATE_REP", "ASCENDING"]], 空间排序方式="UR", 输出要素名称="in_memory\\AA_排序"):
        if 输出要素名称 == "in_memory\\AA_排序":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        排序字段及顺序列表temp = []
        for x in 排序字段及顺序列表:
            if x[1] == "ASCENDING" or x[1] == "正序":
                排序字段及顺序列表temp.append([x[0], "ASCENDING"])
            elif x[1] == "DESCENDING" or x[1] == "倒序":
                排序字段及顺序列表temp.append([x[0], "DESCENDING"])
        排序字段及顺序列表 = 排序字段及顺序列表temp
        arcpy.management.Sort(in_dataset=self.名称, out_dataset=输出要素名称, sort_field=排序字段及顺序列表, spatial_sort_method=空间排序方式)
        return 要素类(名称=输出要素名称)

    def 要素创建_通过多部件至单部件(self, 输出要素路径="in_memory\\AA_多部件至单部件"):
        if 输出要素路径 == "in_memory\\AA_多部件至单部件":
            输出要素路径 = 输出要素路径 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        输出要素路径 = arcpy.management.MultipartToSinglepart(in_features=self.名称, out_feature_class=输出要素路径)
        return 要素类(名称=输出要素路径)

    def 要素创建_通过空间连接(self, 连接要素名称, 连接方式="包含连接要素", 输出要素名称="in_memory\\AA_空间连接") -> "要素类":
        _连接方式映射表 = {"INTERSECT": "INTERSECT", "相交": "INTERSECT", "CONTAINS": "CONTAINS", "包含连接要素": "CONTAINS", "COMPLETELY_CONTAINS": "COMPLETELY_CONTAINS", "完全包含连接要素": "COMPLETELY_CONTAINS", "在连接要素内": "WITHIN", "WITHIN": "WITHIN", "完全在连接要素内": "COMPLETELY_WITHIN", "COMPLETELY_WITHIN": "COMPLETELY_WITHIN", "包含连接要素内点": "包含连接要素内点", "内点在连接要素内": "内点在连接要素内", "形心在连接要素内": "HAVE_THEIR_CENTER_IN", "HAVE_THEIR_CENTER_IN": "HAVE_THEIR_CENTER_IN"}
        连接方式 = _连接方式映射表[连接方式]
        if 输出要素名称 == "in_memory\\AA_空间连接":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        if 连接方式 == "包含连接要素内点":
            arcpy.management.RepairGeometry(in_features=连接要素名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]
            连接要素 = 要素类.要素读取_通过名称(连接要素名称)
            连接要素转点后要素 = 连接要素.要素创建_通过转点()
            # 连接要素转内点后名称 = arcpy.management.FeatureToPoint(in_features=连接要素名称, out_feature_class="in_memory\\AA_要素转点" + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime()), point_location="INSIDE")
            return self.要素创建_通过空间连接(连接要素转点后要素.名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
        if 连接方式 == "内点在连接要素内":
            arcpy.management.RepairGeometry(in_features=self.名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]
            # 目标要素转内点后名称 = arcpy.management.FeatureToPoint(in_features=self.名称, out_feature_class="in_memory\\AA_要素转点" + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime()), point_location="INSIDE")
            目标要素转点后要素 = self.要素创建_通过转点()
            目标要素 = 要素类.要素读取_通过名称(目标要素转点后要素.名称)
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

    def 要素创建_通过转点(self, 输出要素名称="in_memory\\AA_转点"):
        from .游标类 import 游标类

        if 输出要素名称 == "in_memory\\AA_转点":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        点要素 = 要素类.要素创建_通过名称("AA_转点" + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime()), "点", 模板=self.名称)
        点要素复制后 = 点要素.要素创建_通过复制(输出要素名称)
        点要素.要素删除()
        点要素 = 点要素复制后
        字段列表 = self.字段名称列表获取()
        字段列表.remove("OBJECTID")
        字段列表.remove("Shape")
        字段列表.remove("Shape_Length")
        字段列表.remove("Shape_Area")
        字段列表.insert(0, "_ID")
        字段列表.insert(0, "_形状")
        # print(字段列表)
        点字段列表 = [x for x in 字段列表]
        点字段列表.pop(1)
        # print(点字段列表)
        with 游标类.游标创建_通过名称("查找", self.名称, 字段列表) as 面要素游标对象:
            with 游标类.游标创建_通过名称("插入", 点要素.名称, 点字段列表) as 点要素游标对象:
                for x in 面要素游标对象:
                    try:
                        # 日志.输出调试(f"x[0]是{x[0]._内嵌对象}")
                        x[0] = x[0].内点
                        x.pop(1)
                        # 日志.输出调试(f"内点是{内点}")
                        点要素游标对象.行插入(x)
                    except Exception as e:
                        print(f"内点获取发生错误：{e}")
                        print(f"ID为 {x[1]} 的对象无法获取到内点，取了端点")
                        x[0] = x[0].点表[0][0]
                        x.pop(1)
                        # 日志.输出调试(f"端点是{端点}")
                        点要素游标对象.行插入(x)
        return 点要素.要素创建_通过复制并重命名重名要素(输出要素名称)

    def 要素创建_通过转线(self, 输出要素名称="in_memory\\AA_转线"):
        if 输出要素名称 == "in_memory\\AA_转线":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        arcpy.management.FeatureToLine(in_features=self.名称, out_feature_class=输出要素名称)
        return 要素类.要素读取_通过名称(输出要素名称)

    def 要素创建_通过面转线(self, 是否识别并存储面邻域信息=True, 输出要素名称="in_memory\\AA_面转线"):
        if 输出要素名称 == "in_memory\\AA_面转线":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        if 是否识别并存储面邻域信息:
            arcpy.management.PolygonToLine(in_features=self.名称, out_feature_class=输出要素名称, neighbor_option="IDENTIFY_NEIGHBORS")
        else:
            arcpy.management.PolygonToLine(in_features=self.名称, out_feature_class=输出要素名称, neighbor_option="IGNORE_NEIGHBORS")
        return 要素类.要素读取_通过名称(输出要素名称)

    def 要素创建_通过缓冲(self, 距离或字段名称, 融合类型="不融合", 融合字段名称列表=None, 输出要素名称="in_memory\\AA_缓冲"):
        if 输出要素名称 == "in_memory\\AA_缓冲":
            输出要素名称 = 输出要素名称 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
        _融合类型映射表 = {"不融合": "NONE", "NONE": "NONE", "融合为单个": "ALL", "ALL": "ALL", "融合按字段": "LIST", "LIST": "LIST"}
        融合类型 = _融合类型映射表[融合类型]
        if 融合字段名称列表:
            融合字段名称列表 = ";".join(融合字段名称列表)
        arcpy.analysis.Buffer(in_features=self.名称, out_feature_class=输出要素名称, buffer_distance_or_field=距离或字段名称, line_side="FULL", line_end_type="ROUND", dissolve_option=融合类型, dissolve_field=融合字段名称列表, method="PLANAR")
        return 要素类.要素读取_通过名称(输出要素名称)

    def 要素删除(self):
        return arcpy.management.Delete(in_data=[self.名称], data_type="")[0]

    @staticmethod
    def 要素删除_通过要素名称列表(要素名称列表):
        return arcpy.management.Delete(in_data=要素名称列表, data_type="")[0]

    def 要素几何修复(self):
        arcpy.management.RepairGeometry(in_features=self.名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]
        return self

    def 选择集创建_通过属性(self, 选择方式="新建选择集", SQL语句=""):
        from .图层类 import 图层类

        _选择方式映射表 = {"新建选择集": "NEW_SELECTION", "NEW_SELECTION": "NEW_SELECTION"}
        选择方式 = _选择方式映射表[选择方式]
        a = arcpy.management.SelectLayerByAttribute(in_layer_or_view=self.名称, selection_type=选择方式, where_clause=SQL语句, invert_where_clause="")[0]
        return 图层类(a)

    def 字段列表获取(self):
        from .字段类 import 字段类

        return [字段类(x) for x in arcpy.ListFields(self.名称)]

    def 字段名称列表获取(self):
        字段列表 = self.字段列表获取()
        return [x.名称 for x in 字段列表]

    def 字段删除(self, 删除字段名称列表=None, 保留字段名称列表=None):
        from bxpy import 日志

        if 保留字段名称列表 is None:
            arcpy.management.DeleteField(in_table=self.名称, drop_field=删除字段名称列表, method="DELETE_FIELDS")[0]
        elif 删除字段名称列表 is None:
            字段对象列表 = 要素类(名称=self.名称).字段列表获取()
            字段名称列表 = [x.名称 for x in 字段对象列表]
            日志.输出调试(f"要素拥有的所有字段为：" + str(字段名称列表))
            保留字段名称列表.extend(["OID", "OBJECTID", "OBJECTID_1", "Shape", "Shape_Area", "Shape_Length"])
            for x in 保留字段名称列表:
                if x in 字段名称列表:
                    字段名称列表.remove(x)
            日志.输出调试(f"除去保留字段列表后剩余的所有字段为：" + str(字段名称列表))
            if 字段名称列表:
                arcpy.management.DeleteField(in_table=self.名称, drop_field=字段名称列表, method="DELETE_FIELDS")[0]
        return self

    def 字段添加(self, 字段名称, 字段类型="字符串", 字段长度=100, 字段别称=""):
        from . import 常量

        字段类型 = 常量._字段类型映射[字段类型]
        arcpy.management.DeleteField(in_table=self.名称, drop_field=[字段名称], method="DELETE_FIELDS")
        arcpy.management.AddField(in_table=self.名称, field_name=字段名称, field_type=字段类型, field_precision=None, field_scale=None, field_length=字段长度, field_alias=字段别称, field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
        return self

    def 字段计算(self, 字段名称, 表达式, 字段类型="字符串", 语言类型="PYTHON3", 代码块=""):
        from . import 常量

        字段类型 = 常量._字段类型映射[字段类型]
        arcpy.management.CalculateField(in_table=self.名称, field=字段名称, expression=表达式, expression_type=语言类型, code_block=代码块, field_type=字段类型, enforce_domains="NO_ENFORCE_DOMAINS")[0]
        return self

    def 字段修改(self, 字段名称=None, 修改后字段名称=None, 修改后字段别称=None, 字段类型=None, 字段长度=None, 清除字段别称=True):
        from . import 常量

        if 字段类型:
            字段类型 = 常量._字段类型映射[字段类型]
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

    def 拓扑创建(self):
        要素类.拓扑创建_通过要素名称列表([self.名称])

    @staticmethod
    def 拓扑创建_通过要素名称列表(输入要素名称列表):
        from .要素数据集类 import 要素数据集类
        from .拓扑类 import 拓扑类
        from .数据库类 import 数据库类
        from .配置类 import 配置

        数据库对象 = 数据库类.数据库读取_通过路径(配置.当前工作空间)
        要素数据集名称列表 = 数据库对象.要素数据集名称列表获取()
        if "拓扑检查" in 要素数据集名称列表:
            要素数据集类.要素数据集读取_通过名称("拓扑检查").要素数据集删除()
        要素数据集 = 要素数据集类.要素数据集创建("拓扑检查")
        拓扑对象 = 拓扑类.拓扑创建(要素数据集.名称, "拓扑")

        for x in 输入要素名称列表:
            输入要素 = 要素类.要素读取_通过名称(x)
            要素数据集中的要素 = 输入要素.导出到要素(要素数据集.名称 + "\\" + 输入要素.名称 + "_1")
            日志.输出调试(f"准备添加要素的名称是：{要素数据集中的要素.名称}")
            拓扑对象.拓扑中添加要素(要素数据集中的要素.名称)
            日志.输出调试(f"准备添加要素的类型是：{要素数据集中的要素.几何类型}")
            if 要素数据集中的要素.几何类型 == "面":
                拓扑对象.拓扑中添加规则(要素数据集中的要素.名称, 规则="面无重叠")
            elif 要素数据集中的要素.几何类型 == "线":
                拓扑对象.拓扑中添加规则(要素数据集中的要素.名称, 规则="线无重叠")
                拓扑对象.拓扑中添加规则(要素数据集中的要素.名称, 规则="线无自重叠")
            拓扑对象.拓扑验证()

        拓扑导出后要素1, 拓扑导出后要素2, 拓扑导出后要素3 = 拓扑对象.导出到要素("AA_拓扑导出后要素")
        if 要素数据集中的要素.几何类型 == "面":
            拓扑导出后要素3.导出到CAD(r"C:\Users\beixiao\Desktop\拓扑检查.dwg")
        elif 要素数据集中的要素.几何类型 == "线":
            拓扑导出后要素2.导出到CAD(r"C:\Users\beixiao\Desktop\拓扑检查.dwg")
        elif 要素数据集中的要素.几何类型 == "点":
            拓扑导出后要素1.导出到CAD(r"C:\Users\beixiao\Desktop\拓扑检查.dwg")

        拓扑导出后要素1.要素删除()
        拓扑导出后要素2.要素删除()
        拓扑导出后要素3.要素删除()
