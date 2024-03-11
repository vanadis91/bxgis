# -*- coding: utf-8 -*-

# import arcpy
# from sys import argv
import bxarcpy
from bxgis import 配置


def 道路红线提取(用地要素名称="DIST_用地规划图", 地类编号字段名称=配置.地块要素字段映射.地类编号字段名称, 导出到CAD路径=r"C:\Users\beixiao\Desktop\01.dwg", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_道路红线提取" + "_" + bxarcpy.工具集.生成短GUID()
    地块要素 = bxarcpy.要素类.要素读取_通过名称(用地要素名称).要素创建_通过复制()

    道路边线要素 = 地块要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '1207%'")
    道路边线要素 = 道路边线要素.要素创建_通过融合([地类编号字段名称]).要素几何修复()
    道路边线要素 = 道路边线要素.要素创建_通过转线()
    if 导出到CAD路径:
        道路边线要素.导出到CAD(导出到CAD路径)
    输出要素 = 道路边线要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\受降北_数据库.gdb"
    # 道路中线要素名称 = bxarcpy.环境.输入参数获取_以字符串形式(0, "DL_道路中线", True)
    with bxarcpy.环境.环境管理器(工作空间):
        道路红线提取("XG_GHDK", "dldm")
