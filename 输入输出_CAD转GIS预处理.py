# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-09-24 17:43:33
"""
import bxarcpy
from bxpy import 调试

# from sys import argv


def main(
    工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb",
    CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"],
    输出要素=r"YD_CAD色块",
):
    with bxarcpy.类.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        # 输入输出_CAD转GIS预处理_PY3
        # To allow overwriting outputs change overwriteOutput option to True.
        bxarcpy.类.配置.是否覆盖输出要素 = True
        # arcpy.env.overwriteOutput = False
        输出要素集 = bxarcpy.类.要素数据集类.导入从CAD(CAD路径列表, r"AA_CAD导入GEO1")
        # 输出要素集 = bxarcpy.转换.CAD导入到GEO(CAD路径列表=CAD路径列表, 输出数据库=工作空间, 输出要素集名称=r"AA_CAD导入GEO1")
        调试.输出调试("输出的要素集是：" + 输出要素集.名称 + r"\控规地块")
        # print("输出要素是：" + 工作空间 + 输出要素)

        if CAD路径列表 == [r"C:\Users\beixiao\Desktop\01.dwg"]:
            输入要素 = bxarcpy.类.要素类.要素读取_通过名称(输出要素集.名称 + r"\控规地块")
            复制后要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素)
            # 输出要素 = bxarcpy.数据管理.要素复制(输入要素=输出要素集 + r"\控规地块", 输出要素=工作空间 + 输出要素)
        else:
            输入要素 = bxarcpy.类.要素类.要素读取_通过名称(输出要素集.名称 + r"\Polygon")
            复制后要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素)
            # 输出要素 = bxarcpy.数据管理.要素复制(输入要素=输出要素集 + r"\Polygon", 输出要素=工作空间 + 输出要素)

        输出要素集.要素数据集删除()
        # bxarcpy.数据管理.要素删除(输入要素列表=[输出要素集])

        # Process: 修复几何 (修复几何) (management)
        复制后要素.要素几何修复().字段添加("地类编号").字段计算("地类编号", "!Layer!.split(\"#\")[0].split(\"-\")[1].replace('／','/')").字段删除(["Entity", "Handle", "Layer", "Color", "Linetype", "Elevation", "LineWt", "RefName", "LyrColor", "LyrLnType", "LyrLineWt"])
        # 输出要素 = bxarcpy.数据管理.几何修复(输入要素=输出要素)

        # Process: 添加字段 (添加字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="地类编号", 字段类型="字符串", 字段长度=100)

        # Process: 计算字段 (计算字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="地类编号", 表达式="!Layer!.split(\"#\")[0].split(\"-\")[1].replace('／','/')", 字段类型="字符串")

        # 输出要素 = bxarcpy.数据管理.字段删除(输入要素=输出要素, 删除字段列表=["Entity", "Handle", "Layer", "Color", "Linetype", "Elevation", "LineWt", "RefName", "LyrColor", "LyrLnType", "LyrLineWt"])


if __name__ == "__main__":
    # Global Environment settings
    main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"], 输出要素=r"YD_CAD色块")
    # main(工作空间=r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"], 输出要素=r"YD_CAD色块")
