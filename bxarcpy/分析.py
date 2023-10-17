import arcpy
import bxarcpy
import time


def 裁剪(输入要素=None, 裁剪要素=None, 输出要素="in_memory\\AA_裁剪"):
    if 输出要素 == "in_memory\\AA_裁剪":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    arcpy.analysis.Clip(in_features=输入要素, clip_features=裁剪要素, out_feature_class=输出要素, cluster_tolerance="")
    return 输出要素


def 擦除(输入要素=None, 擦除要素=None, 输出要素="in_memory\\AA_擦除"):
    if 输出要素 == "in_memory\\AA_擦除":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    arcpy.analysis.Erase(in_features=输入要素, erase_features=擦除要素, out_feature_class=输出要素, cluster_tolerance="")
    return 输出要素


def 相交(输入要素列表=[], 输出要素="in_memory\\AA_相交"):
    if 输出要素 == "in_memory\\AA_相交":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    输入要素列表 = [[x, ""] for x in 输入要素列表]
    arcpy.analysis.Intersect(in_features=输入要素列表, out_feature_class=输出要素, join_attributes="ALL", cluster_tolerance="", output_type="INPUT")
    return 输出要素


def 联合(输入要素列表=[], 输出要素="in_memory\\AA_联合"):
    if 输出要素 == "in_memory\\AA_联合":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    输入要素列表 = [[x, ""] for x in 输入要素列表]
    arcpy.analysis.Union(in_features=输入要素列表, out_feature_class=输出要素, join_attributes="ALL", cluster_tolerance="", gaps="GAPS")

    return 输出要素


def 融合(输入要素, 输出要素="in_memory\\AA_融合", 融合字段列表=[], 统计字段=[[]]):
    return arcpy.management.Dissolve(in_features=输入要素, out_feature_class=输出要素, dissolve_field=融合字段列表, statistics_fields=统计字段, multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES", concatenation_separator="")


def 擦除并几何修复(输入要素=None, 擦除要素=None, 输出要素="in_memory\\AA_擦除并几何修复"):
    if 输出要素 == "in_memory\\AA_擦除并几何修复":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())

    输入 = bxarcpy.数据管理.几何修复(输入要素=输入要素)
    擦除 = bxarcpy.数据管理.几何修复(输入要素=擦除要素)
    with bxarcpy.环境.环境管理器(输出包含M值="Disabled", 输出包含Z值="Disabled"):
        arcpy.analysis.Erase(in_features=输入, erase_features=擦除, out_feature_class=输出要素, cluster_tolerance="")
    return 输出要素


def 更新并合并字段(输入要素=None, 更新要素=None, 输出要素="in_memory\\AA_更新并合并字段"):
    if 输出要素 == "in_memory\\AA_更新并合并字段":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
    输出 = bxarcpy.分析.擦除并几何修复(输入要素=输入要素, 擦除要素=更新要素)
    # Process: 合并 (合并) (management)
    输出要素 = bxarcpy.数据管理.要素合并(输入要素列表=[输出, 更新要素], 输出要素=输出要素)
    return 输出要素


def 填充空隙(输入要素=None, 填充范围=None, 填充地类编号表达式='"00"', 输出要素="in_memory\\AA_填充空隙"):
    # 常用_填充空隙后
    # To allow overwriting outputs change overwriteOutput option to True.
    if 输出要素 == "in_memory\\AA_填充空隙":
        输出要素 = 输出要素 + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime())

    # Process: 复制要素 (复制要素) (management)
    填充范围1 = bxarcpy.数据管理.要素复制(输入要素=填充范围)
    填充范围1 = bxarcpy.数据管理.字段添加(输入要素=填充范围1, 字段名称="地类编号", 字段类型="字符串", 字段长度=100)
    填充范围1 = bxarcpy.数据管理.字段计算(输入要素=填充范围1, 字段名称="地类编号", 字段类型="字符串", 表达式=填充地类编号表达式)
    输出要素 = 更新并合并字段(输入要素=填充范围1, 更新要素=输入要素, 输出要素=输出要素)
    return 输出要素


def 筛选(输入要素=None, SQL语句="", 输出要素="in_memory\\AA_筛选"):
    if 输出要素 == "in_memory\\AA_筛选":
        输出要素 = 输出要素 + "_" + time.strftime(r"%Y%m%d%H%M%S", time.localtime())
    arcpy.analysis.Select(in_features=输入要素, out_feature_class=输出要素, where_clause=SQL语句)
    return 输出要素
