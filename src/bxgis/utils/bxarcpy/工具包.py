# *-* coding:utf8 *-*
from typing import Union, Literal, Any, List, Dict, Optional, TypedDict
import arcpy


# from pydantic import BaseModel
def 生成当前时间():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")


def 生成当前时间_微秒():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%f")


def 生成短GUID():
    from bxpy.基本对象包 import 字类

    return 字类.字符串生成_短GUID()


def 临时路径生成(文件名列表, 工作空间: Literal["内存临时", "临时工作空间", "当前工作空间", "内存"] = "内存临时"):
    from bxpy.基本对象包 import 字类
    from bxpy.路径包 import 路径类

    要素名称列表 = [路径类.属性获取_文件名(路径类.规范化(x)) for x in 文件名列表]
    要素名称 = "_".join(要素名称列表)

    要素名称列表 = 要素名称.split("_")
    要素名称列表 = [x for x in 要素名称列表 if not 字类.匹配正则(x, r"^[A-Za-z0-9]{10}$") and not 字类.匹配正则(x, r"^[A-Za-z0-9]{22}$") and x.upper() not in ["AA", "KZX", "DIST", "YD", "GZW", "CZ", "AC", "DL", "JX", "SS", "TK", "YT"]]
    要素名称 = "_".join(要素名称列表)
    if len(要素名称) > 15:
        要素名称 = 要素名称[0:15]
    输出要素路径 = "AA_" + 要素名称 + "_" + 生成短GUID()
    if 工作空间 in ["内存临时", "内存"]:
        return 路径类.连接("in_memory", 输出要素路径)
    elif 工作空间 in ["临时工作空间"]:
        return 路径类.连接(arcpy.env.scratchWorkspace, 输出要素路径)  # type: ignore
    elif 工作空间 in ["当前工作空间"]:
        return 路径类.连接(arcpy.env.workspace, 输出要素路径)  # type: ignore
    else:
        return 路径类.连接("in_memory", 输出要素路径)


def 临时字段名称生成(字段名称列表):

    from bxpy.基本对象包 import 字类

    既有字段名称 = "_".join(字段名称列表)
    字段名称列表 = 既有字段名称.split("_")
    字段名称列表 = [x for x in 字段名称列表 if not 字类.匹配正则(x, r"^[A-Za-z0-9]{10}$") and not 字类.匹配正则(x, r"^[A-Za-z0-9]{22}$") and x.upper() not in ["AA", "KZX", "DIST", "YD", "GZW", "CZ", "AC", "DL", "JX", "SS", "TK", "YT"]]
    既有字段名称 = "_".join(字段名称列表)
    if len(既有字段名称) > 18:
        既有字段名称 = 既有字段名称[0:18]
    输出要素路径 = 既有字段名称 + "_" + 生成短GUID()
    return 输出要素路径


def 输出路径生成_当采用内存临时时(输入要素路径列表):
    from bxpy.基本对象包 import 字类
    from bxpy.路径包 import 路径类

    要素名称列表 = [路径类.属性获取_文件名(路径类.规范化(x)) for x in 输入要素路径列表]
    要素名称 = "_".join(要素名称列表)

    要素名称列表 = 要素名称.split("_")
    要素名称列表 = [x for x in 要素名称列表 if not 字类.匹配正则(x, r"^[A-Za-z0-9]{10}$") and not 字类.匹配正则(x, r"^[A-Za-z0-9]{22}$") and x.upper() not in ["AA", "KZX", "DIST", "YD", "GZW", "CZ", "AC", "DL", "JX", "SS", "TK", "YT"]]
    要素名称 = "_".join(要素名称列表)
    if len(要素名称) > 15:
        要素名称 = 要素名称[0:15]
    输出要素路径 = "in_memory\\AA_" + 要素名称 + "_" + 生成短GUID()
    return 输出要素路径


def 输出路径生成_当采用临时工作空间临时时(输入要素路径列表):
    ret = 输出路径生成_当采用内存临时时(输入要素路径列表)
    from bxpy.路径包 import 路径类
    import arcpy

    return 路径类.连接(arcpy.env.scratchWorkspace, ret[11:])  # type: ignore


def 输出路径生成_当采用当前工作空间临时时(输入要素路径列表):
    ret = 输出路径生成_当采用内存临时时(输入要素路径列表)
    from bxpy.路径包 import 路径类
    import arcpy

    return 路径类.连接(arcpy.env.workspace, ret[11:])  # type: ignore


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    from bxarcpy.环境包 import 环境管理器类

    with 环境管理器类.环境管理器类创建(工作空间):
        print(输出路径生成_当采用临时工作空间临时时(["CZ_基本农田"]))
        print(输出路径生成_当采用当前工作空间临时时(["CZ_基本农田"]))
        # 坐标系统一(输入要素路径列表=["AA_彩虹快速路修正", "CZ_农转用_部备案09年前", "CZ_农转用_部备案09年后", "CZ_城镇开发边界_范围内", "CZ_基本农田", "CZ_基本农田_范围内"])
    # 曲转折(输入要素路径列表=["JX_规划范围线", "JX_街坊范围线", "JX_街区范围线"])
    # 曲转折(输入要素路径列表=["YD_基期", "DIST_用地基期图"])
    # 曲转折(输入要素名称列表=["YD_基期初转换", "YD_基期细化", "YD_农转用20年及以前", "YD_现状修改1", "YD_农转用21年及以后", "YD_审批信息已实施", "YD_地籍信息", "YD_现状修改2", "YD_审批信息已批未建", "YD_上位_粮食生产功能区", "YD_上位农用地落实_耕地质量提升", "YD_上位农用地落实_旱改水", "YD_上位农用地落实_垦造耕地", "YD_上位农用地落实_新增设施农用地", "YD_上位基本农田落实", "YD_GIS方案_农用地设计", "YD_CAD色块以外建设用地修改", "YD_CAD色块"])
    # with open(r"C:\Users\beixiao\Desktop\123.txt", "w") as f:
    #     print("12311111", file=f)
