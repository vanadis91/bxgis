import arcpy
import time
import bxarcpy

# __all__ = ["要素复制", "要素合并", "字段删除", "字段添加", "字段计算", "多部件至单部件", "几何修复"]
_字段类型映射 = {"字符串": "TEXT", "TEXT": "TEXT", "双精度": "DOUBLE", "DOUBLE": "DOUBLE", "长整型": "LONG", "LONG": "LONG", "短整型": "SHORT", "SHORT": "SHORT", "日期": "DATE", "DATE": "DATE", "单精度": "FLOAT", "FLOAT": "FLOAT"}


def 要素复制(输入要素=None, 输出要素="in_memory\\AA_复制"):
    if 输出要素 == "in_memory\\AA_复制":
        输出要素 = 输出要素 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
    arcpy.management.CopyFeatures(in_features=输入要素, out_feature_class=输出要素, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)
    return 输出要素


def 要素合并(输入要素列表=None, 输出要素="in_memory\\AA_合并"):
    if 输出要素 == "in_memory\\AA_合并":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    arcpy.management.Merge(inputs=输入要素列表, output=输出要素, field_mappings="", add_source="NO_SOURCE_INFO")
    return 输出要素


def 要素删除(输入要素列表=None):
    return arcpy.management.Delete(in_data=输入要素列表, data_type="")[0]


def 要素字段列表获取(输入要素=None):
    字段列表 = arcpy.ListFields(输入要素)
    字段列表 = [bxarcpy.字段(x) for x in 字段列表]
    return 字段列表


def 要素集创建(数据库=None, 要素集名称=None):
    return arcpy.management.CreateFeatureDataset(out_dataset_path=数据库, out_name=要素集名称, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]


def 要素多部件至单部件(输入要素=None, 输出要素="in_memory\\AA_多部件至单部件"):
    if 输出要素 == "in_memory\\AA_多部件至单部件":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    return arcpy.management.MultipartToSinglepart(in_features=输入要素, out_feature_class=输出要素)


def 要素几何修复(输入要素=None):
    return arcpy.management.RepairGeometry(in_features=输入要素, delete_null="DELETE_NULL", validation_method="ESRI")[0]


def 要素选择_通过属性(输入要素=None, 选择方式="新建选择集", SQL语句=""):
    选择方式映射表 = {"新建选择集": "NEW_SELECTION", "NEW_SELECTION": "NEW_SELECTION"}
    选择方式 = 选择方式映射表[选择方式]
    return arcpy.management.SelectLayerByAttribute(in_layer_or_view=输入要素, selection_type=选择方式, where_clause=SQL语句, invert_where_clause="")[0]


def 拓扑创建(要素集=None, 拓扑名称=None):
    return arcpy.management.CreateTopology(in_dataset=要素集, out_name=拓扑名称, in_cluster_tolerance=None)[0]


def 拓扑中添加要素(拓扑名称=None, 输入要素=None):
    return arcpy.management.AddFeatureClassToTopology(in_topology=拓扑名称, in_featureclass=输入要素, xy_rank=1, z_rank=1)[0]


def 拓扑中添加规则(拓扑名称=None, 输入要素=None, 规则="Must Not Overlap (Area)"):
    return arcpy.management.AddRuleToTopology(in_topology=拓扑名称, rule_type=规则, in_featureclass=输入要素, subtype="", in_featureclass2="", subtype2="")[0]


def 拓扑验证(拓扑名称=None):
    return arcpy.management.ValidateTopology(in_topology=拓扑名称, visible_extent="Full_Extent")[0]


def 拓扑导出(拓扑名称=r"C:\Users\beixiao\Desktop\新建文件地理数据库.gdb\拓扑检查\拓扑", 数据库名称=r"C:\Users\beixiao\Desktop\新建文件地理数据库.gdb", 导出要素名称="拓扑导出后要素"):
    拓扑导出后要素 = arcpy.management.ExportTopologyErrors(拓扑名称, 数据库名称, 导出要素名称)
    return (导出要素名称 + "_point", 导出要素名称 + "_line", 导出要素名称 + "_poly")


def 字段删除(输入要素=None, 删除字段列表=None, 保留字段列表=None):
    from bxpy import 调试

    if 保留字段列表 is None:
        return arcpy.management.DeleteField(in_table=输入要素, drop_field=删除字段列表, method="DELETE_FIELDS")[0]
    elif 删除字段列表 is None:
        字段对象列表 = bxarcpy.要素类(路径=输入要素).字段列表获取()
        字段名称列表 = [x.名称 for x in 字段对象列表]
        调试.输出调试(f"要素拥有的所有字段为：" + str(字段名称列表))
        for x in 保留字段列表:
            字段名称列表.remove(x)
        字段名称列表.remove("OBJECTID")
        字段名称列表.remove("Shape")
        调试.输出调试(f"除去保留字段列表后剩余的所有字段为：" + str(字段名称列表))
        return arcpy.management.DeleteField(in_table=输入要素, drop_field=字段名称列表, method="DELETE_FIELDS")[0]


def 字段添加(输入要素=None, 字段名称="", 字段类型="字符串", 字段长度=100, 字段别称=""):
    字段类型 = _字段类型映射[字段类型]
    return arcpy.management.AddField(in_table=输入要素, field_name=字段名称, field_type=字段类型, field_precision=None, field_scale=None, field_length=字段长度, field_alias=字段别称, field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]


def 字段计算(输入要素=None, 字段名称="", 表达式="", 字段类型="字符串", 语言类型="Python", 代码块=""):
    字段类型映射 = {"字符串": "TEXT", "TEXT": "TEXT"}
    字段类型 = 字段类型映射[字段类型]
    return arcpy.management.CalculateField(in_table=输入要素, field=字段名称, expression=表达式, expression_type=语言类型, code_block=代码块, field_type=字段类型, enforce_domains="NO_ENFORCE_DOMAINS")[0]


def 字段修改(输入要素=None, 字段名称=None, 修改后字段名称=None, 修改后字段别称=None, 字段类型=None, 字段长度=None, 清除字段别称=True):
    字段类型 = _字段类型映射[字段类型]
    return arcpy.management.AlterField(in_table=输入要素, field=字段名称, new_field_name=修改后字段名称, new_field_alias=修改后字段别称, field_type=字段类型, field_length=字段长度, field_is_nullable="NULLABLE", clear_field_alias=清除字段别称)[0]


def 数据库要素类列表获取():
    return arcpy.ListFeatureClasses()


def 数据库要素数据集列表获取():
    return arcpy.ListDatasets()


def 数据库文件列表获取():
    return arcpy.ListFiles()


def 数据库栅格列表获取():
    return arcpy.ListRasters()


def 连接创建(输入要素=None, 输入要素连接字段=None, 连接要素=None, 连接要素连接字段=None):
    return arcpy.management.AddJoin(in_layer_or_view=输入要素, in_field=输入要素连接字段, join_table=连接要素, join_field=连接要素连接字段, join_type="KEEP_ALL", index_join_fields="NO_INDEX_JOIN_FIELDS")[0]


def 连接取消(输入要素=None, 连接要素=None):
    return arcpy.management.RemoveJoin(in_layer_or_view=输入要素, join_name=连接要素)[0]
