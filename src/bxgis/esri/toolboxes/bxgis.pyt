# -*- coding: utf-8 -*-
# import sys
# import os

# 项目入口目录 = os.path.dirname(os.path.abspath(__file__))
# 当前工作目录 = os.getcwd()
# os.chdir(项目入口目录)
# 项目根目录 = os.path.abspath("..\\..\\..\\")
# os.chdir(当前工作目录)

# sys.path.append(项目根目录)
# sys.path.append(项目根目录 + "\\.venv\\Lib\\site-packages")
# sys.path.append(项目根目录 + "\\common")
# sys.path.append(项目根目录 + "\\src")

import bxarcpy
import bxgis

# import importlib

# importlib.reload(bxarcpy)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file) 定义了工具箱的属性"""
        self.label = "BXGIS工具箱"  # 定义标签
        self.alias = "BXGIS工具箱"  # 定义别名
        # self.category可以把工具组织成不同工具集
        # List of tool classes associated with this toolbox 定义了包含的所有工具名称列表
        self.tools = [ExportToCAD]


class ExportToCAD(object):
    # "导出到CAD"
    参数名称列表 = []

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "导出到CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用工具"

    def getParameterInfo(self):
        """Define parameter definitions 定义了参数，类似脚本工具属性中的参数界面"""

        输入要素 = bxarcpy.参数类.参数创建("输入要素", "输入要素", "要素类", 参数必要性="必填")._内嵌对象

        范围要素 = bxarcpy.参数类.参数创建("范围要素", "范围要素", "要素类", 默认值="JX_规划范围线")._内嵌对象

        是否对要素进行融合 = bxarcpy.参数类.参数创建("是否对要素进行融合", "是否对要素进行融合", "布尔值", 默认值=False)._内嵌对象

        需融合地类编号列表 = bxarcpy.参数类.参数创建("需融合地类编号列表", "需融合地类编号列表", "字符串", 是否多个值=True, 是否可用=False, 默认值=["1207"])._内嵌对象

        是否对要素进行切分 = bxarcpy.参数类.参数创建("是否对要素进行切分", "是否对要素进行切分", "布尔值", 默认值=False)._内嵌对象

        切分时折点数量阈值 = bxarcpy.参数类.参数创建("切分时折点数量阈值", "切分时折点数量阈值", "长整型", 是否可用=False, 默认值=15000)._内嵌对象

        切分时孔洞数量阈值 = bxarcpy.参数类.参数创建("切分时孔洞数量阈值", "切分时孔洞数量阈值", "长整型", 是否可用=False, 默认值=3)._内嵌对象

        切分时面积阈值 = bxarcpy.参数类.参数创建("切分时面积阈值", "切分时面积阈值", "双精度", 是否可用=False, 默认值=500000)._内嵌对象

        切分时地类编号限制列表 = bxarcpy.参数类.参数创建("切分时地类编号限制列表", "切分时地类编号限制列表", "字符串", 是否多个值=True, 是否可用=False, 默认值=["1207"])._内嵌对象

        是否去孔 = bxarcpy.参数类.参数创建("是否去孔", "是否去孔", "布尔值", 默认值=False)._内嵌对象

        输出CAD路径 = bxarcpy.参数类.参数创建("输出CAD路径", "输出CAD路径", "CAD数据集", 参数类型="输出参数")._内嵌对象

        参数列表 = [输入要素, 范围要素, 是否对要素进行融合, 需融合地类编号列表, 是否对要素进行切分, 切分时折点数量阈值, 切分时孔洞数量阈值, 切分时面积阈值, 切分时地类编号限制列表, 是否去孔, 输出CAD路径]
        ExportToCAD.参数名称列表 = [bxarcpy.参数类.名称读取(x) for x in 参数列表]
        return 参数列表

    def isLicensed(self):
        """Set whether tool is licensed to execute 可以控制许可行为，验证能否执行，检入检出许可"""
        return True

    def updateParameters(self, 参数列表):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed 定义了工具内部验证的过程，比如输入数据达到某个条件，则启用或者禁用某个参数，或者为某个参数设置默认值"""
        参数字典 = {k: v for k, v in zip(ExportToCAD.参数名称列表, 参数列表)}
        if bxarcpy.参数类.值读取(参数字典["是否对要素进行融合"]):
            bxarcpy.参数类.可用性设置(参数字典["需融合地类编号列表"], True)
        else:
            bxarcpy.参数类.可用性设置(参数字典["需融合地类编号列表"], False)
        if bxarcpy.参数类.值读取(参数字典["是否对要素进行切分"]):
            bxarcpy.参数类.可用性设置(参数字典["切分时折点数量阈值"], True)
            bxarcpy.参数类.可用性设置(参数字典["切分时孔洞数量阈值"], True)
            bxarcpy.参数类.可用性设置(参数字典["切分时面积阈值"], True)
            bxarcpy.参数类.可用性设置(参数字典["切分时地类编号限制列表"], True)
        else:
            bxarcpy.参数类.可用性设置(参数字典["切分时折点数量阈值"], False)
            bxarcpy.参数类.可用性设置(参数字典["切分时孔洞数量阈值"], False)
            bxarcpy.参数类.可用性设置(参数字典["切分时面积阈值"], False)
            bxarcpy.参数类.可用性设置(参数字典["切分时地类编号限制列表"], False)
        if str(bxarcpy.参数类.值读取(参数字典["输出CAD路径"]))[-4:] != ".dwg":
            bxarcpy.参数类.值设置(参数字典["输出CAD路径"], str(bxarcpy.参数类.值读取(参数字典["输出CAD路径"])) + ".dwg")
        return None

    def updateMessages(self, 参数列表):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation 定义了工具内部验证并返回消息的过程，比如输入数据不满足要求，则返回消息输入不可用"""
        return None

    def execute(self, 参数列表, 消息):
        """The source code of the tool 定义工具源码，必要方法，只包括该方法也可以运行工具，但是没有参数界面"""
        参数字典 = {k: v for k, v in zip(ExportToCAD.参数名称列表, 参数列表)}
        输入要素名称 = bxarcpy.参数类.值读取_作为字符串(参数字典["输入要素"])
        范围要素名称 = bxarcpy.参数类.值读取_作为字符串(参数字典["范围要素"])
        需融合地类编号列表 = None
        if bxarcpy.参数类.值读取(参数字典["是否对要素进行融合"]):
            需融合地类编号列表 = bxarcpy.参数类.值读取(参数字典["是否对要素进行融合"])
        切分阈值 = None
        if bxarcpy.参数类.值读取(参数字典["是否对要素进行切分"]):
            切分阈值 = {
                "折点数量": bxarcpy.参数类.值读取(参数字典["切分时折点数量阈值"]),
                "孔洞数量": bxarcpy.参数类.值读取(参数字典["切分时孔洞数量阈值"]),
                "面积": bxarcpy.参数类.值读取(参数字典["切分时面积阈值"]),
                "地类编号列表": bxarcpy.参数类.值读取(参数字典["切分时地类编号限制列表"]),
            }
        是否去孔 = bxarcpy.参数类.值读取(参数字典["是否去孔"])
        输出CAD路径 = bxarcpy.参数类.值读取_作为字符串(参数字典["输出CAD路径"])

        bxgis.常用_导出到CAD(输入要素名称, 范围要素名称, 需融合地类编号列表=需融合地类编号列表, 切分阈值=切分阈值, 是否去孔=是否去孔, 输出CAD路径=输出CAD路径)
        return None

    def postExecute(self, 参数列表):
        """This method takes place after outputs are processed and
        added to the display."""
        return None


if __name__ == "__main__":
    # import bxgis

    # print(bxgis.常用_导出到CAD)
    pass
# class TestTool(object):
#     def __init__(self):
#         """Define the tool (tool name is the name of the class)."""
#         self.label = "测试工具"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = "测试\\测试2"

#     def getParameterInfo(self):
#         """Define parameter definitions 定义了参数，类似脚本工具属性中的参数界面"""

#         输入参数1 = bxarcpy.参数类.参数创建("输入要素", "输入要素", "要素图层", "必填", "输入参数")._内嵌对象
#         输入参数1.filter.list = ["Polyline"]

#         输出参数1 = arcpy.Parameter(
#             name="output_features",
#             displayName="Output Features",
#             datatype="GPFeatureLayer",
#             parameterType="Required",
#             direction="Output",
#         )

#         要素数量 = arcpy.Parameter(
#             name="number_of_features",
#             displayName="Number of Features",
#             datatype="GPLong",
#             parameterType="Required",
#             direction="Input",
#         )
#         要素数量.filter.type = "Range"
#         要素数量.filter.list = [1, 1000000000]

#         parameters = [输入参数1, 输出参数1, 要素数量]
#         return parameters

#     def isLicensed(self):
#         """Set whether tool is licensed to execute 可以控制许可行为，验证能否执行，检入检出许可"""
#         return True

#     def updateParameters(self, parameters):
#         """Modify the values and properties of parameters before internal
#         validation is performed.  This method is called whenever a parameter
#         has been changed 定义了工具内部验证的过程，比如输入数据达到某个条件，则启用或者禁用某个参数，或者为某个参数设置默认值"""
#         return

#     def updateMessages(self, parameters):
#         """Modify the messages created by internal validation for each tool
#         parameter.  This method is called after internal validation 定义了工具内部验证并返回消息的过程，比如输入数据不满足要求，则返回消息输入不可用"""
#         return

#     def execute(self, 参数列表, messages):
#         """The source code of the tool 定义工具源码，必要方法，只包括该方法也可以运行工具，但是没有参数界面"""
#         inputfc = 参数列表[0].valueAsText
#         outputfc = 参数列表[1].valueAsText
#         outcount = 参数列表[2].value
#         inlist = []
#         with arcpy.da.SearchCursor(inputfc, "OID@") as cursor:  # type: ignore
#             for row in cursor:
#                 id = row[0]
#                 inlist.append(id)
#         import random

#         randomlist = random.sample(inlist, outcount)
#         desc = arcpy.da.Describe(inputfc)  # type: ignore
#         fldname = desc["OIDFieldName"]
#         sqlfield = arcpy.AddFieldDelimiters(inputfc, fldname)
#         sqlexp = "{} in {}".format(sqlfield, tuple(randomlist))
#         arcpy.Select_analysis(inputfc, outputfc, sqlexp)
#         return None

#     def postExecute(self, parameters):
#         """This method takes place after outputs are processed and
#         added to the display."""
#         return
