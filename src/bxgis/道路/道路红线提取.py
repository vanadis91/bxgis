# -*- coding: utf-8 -*-

# import arcpy
# from sys import argv
import bxarcpy
from bxgis.配置 import 基本信息
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.环境包 import 环境管理器类


def 道路红线提取(用地要素名称="DIST_用地规划图", 地类编号字段名称=基本信息.地块要素字段映射.地类编号字段名称, 导出到CAD路径=r"C:\Users\beixiao\Desktop\01.dwg", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_道路红线提取" + "_" + 工具包.生成短GUID()
    地块要素_复制后 = 要素类.要素创建_通过复制(用地要素名称)

    道路边线要素 = 要素类.要素创建_通过筛选(地块要素_复制后, f"{地类编号字段名称} LIKE '1207%'")
    道路边线要素 = 要素类.要素创建_通过融合(道路边线要素, [地类编号字段名称])
    道路边线要素 = 要素类.要素几何修复(道路边线要素)
    道路边线要素 = 要素类.要素创建_通过转线(道路边线要素)
    if 导出到CAD路径:
        要素类.转换_到CAD(道路边线要素, 导出到CAD路径)

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(道路边线要素, 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\受降北_数据库.gdb"
    # 道路中线要素名称 = bxarcpy.环境.输入参数获取_以字符串形式(0, "DL_道路中线", True)
    with 环境管理器类.环境管理器类创建(工作空间):
        道路红线提取("XG_GHDK", "dldm")
