# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-09-25 16:31:40
"""
import bxarcpy

# from sys import argv


def main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 规划范围要素名称="JX_规划范围线"):
    with bxarcpy.类.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        # To allow overwriting outputs change overwriteOutput option to True.
        bxarcpy.类.配置.是否覆盖输出要素 = True
        规划范围输入要素 = bxarcpy.类.要素类.要素读取_通过名称(规划范围要素名称)
        规划范围输出要素 = 规划范围输入要素.要素创建_通过复制并重命名重名要素("XG_GHFW")
        规划范围输出要素.字段修改("规划编制单元编号", "DYBH", "规划编制单元编号")
        规划范围输出要素.字段添加("DYMC", "字符串", 50, "规划编制单元名称").字段计算("DYMC", 单元名称)
        规划范围输出要素.字段添加("PFSJ", "日期", None, "批复时间").字段计算("PFSJ", 批复时间)
        规划范围输出要素.字段添加("PFWH", "字符串", 50, "批复文号").字段计算("PFWH", 批复文号)
        规划范围输出要素.字段添加("BZDW", "字符串", 255, "编制单位").字段计算("BZDW", 编制单位)
        规划范围输出要素.字段添加("DYMJ", "双精度", 50, "单元面积").字段计算("DYMJ", "round(!Shape_Area!/10000, 2)")
        规划范围输出要素.字段添加("DYGN", "字符串", 255, "单元功能").字段计算("DYGN", 单元功能)
        规划范围输出要素.字段添加("RK", "双精度", 50, "人口规模").字段计算("RK", 人口规模)
        规划范围输出要素.字段添加("BZ", "字符串", 255, "备注")

        街区范围输入要素 = bxarcpy.类.要素类.要素读取_通过名称(街区范围要素名称)


if __name__ == "__main__":
    main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 规划范围要素名称="JX_规划范围线")
    # import arcpy

    # bxarcpy.配置.设置当前工作空间(工作空间路径=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb")

    # fcs = arcpy.ListFeatureClasses()
    # fcCount11 = len(fcs)
    # for fc11 in fcs:
    #     print(fc11)
    # print(fcCount11)
