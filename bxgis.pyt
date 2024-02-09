# -*- coding: utf-8 -*-
import sys
import os

工具箱所在目录 = os.path.dirname(os.path.abspath(__file__))
sys.path.append(工具箱所在目录)
sys.path.append(工具箱所在目录 + ".venv\\Lib\\site-packages")
sys.path.append(工具箱所在目录 + "common")

import arcpy
import bxarcpy


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
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "导出到CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用工具"

    def getParameterInfo(self):
        """Define parameter definitions 定义了参数，类似脚本工具属性中的参数界面"""

        输入参数1 = bxarcpy.参数类.参数创建("输入要素", "输入要素", "要素图层", "必填", "输入参数")._内嵌对象
        输入参数2 = bxarcpy.参数类.参数创建("范围要素", "范围要素", "要素图层", "必填", "输入参数")._内嵌对象

        输出参数1 = arcpy.Parameter(
            name="output_features",
            displayName="Output Features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output",
        )

        要素数量 = arcpy.Parameter(
            name="number_of_features",
            displayName="Number of Features",
            datatype="GPLong",
            parameterType="Required",
            direction="Input",
        )
        要素数量.filter.type = "Range"
        要素数量.filter.list = [1, 1000000000]

        parameters = [输入参数1, 输出参数1, 要素数量]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute 可以控制许可行为，验证能否执行，检入检出许可"""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed 定义了工具内部验证的过程，比如输入数据达到某个条件，则启用或者禁用某个参数，或者为某个参数设置默认值"""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation 定义了工具内部验证并返回消息的过程，比如输入数据不满足要求，则返回消息输入不可用"""
        return

    def execute(self, 参数列表, messages):
        """The source code of the tool 定义工具源码，必要方法，只包括该方法也可以运行工具，但是没有参数界面"""
        inputfc = 参数列表[0].valueAsText
        outputfc = 参数列表[1].valueAsText
        outcount = 参数列表[2].value
        inlist = []
        with arcpy.da.SearchCursor(inputfc, "OID@") as cursor:  # type: ignore
            for row in cursor:
                id = row[0]
                inlist.append(id)
        import random

        randomlist = random.sample(inlist, outcount)
        desc = arcpy.da.Describe(inputfc)  # type: ignore
        fldname = desc["OIDFieldName"]
        sqlfield = arcpy.AddFieldDelimiters(inputfc, fldname)
        sqlexp = "{} in {}".format(sqlfield, tuple(randomlist))
        arcpy.Select_analysis(inputfc, outputfc, sqlexp)
        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return


class TestTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "测试工具"
        self.description = ""
        self.canRunInBackground = False
        self.category = "测试\\测试2"

    def getParameterInfo(self):
        """Define parameter definitions 定义了参数，类似脚本工具属性中的参数界面"""

        输入参数1 = bxarcpy.参数类.参数创建("输入要素", "输入要素", "要素图层", "必填", "输入参数")._内嵌对象
        输入参数1.filter.list = ["Polyline"]

        输出参数1 = arcpy.Parameter(
            name="output_features",
            displayName="Output Features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output",
        )

        要素数量 = arcpy.Parameter(
            name="number_of_features",
            displayName="Number of Features",
            datatype="GPLong",
            parameterType="Required",
            direction="Input",
        )
        要素数量.filter.type = "Range"
        要素数量.filter.list = [1, 1000000000]

        parameters = [输入参数1, 输出参数1, 要素数量]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute 可以控制许可行为，验证能否执行，检入检出许可"""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed 定义了工具内部验证的过程，比如输入数据达到某个条件，则启用或者禁用某个参数，或者为某个参数设置默认值"""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation 定义了工具内部验证并返回消息的过程，比如输入数据不满足要求，则返回消息输入不可用"""
        return

    def execute(self, 参数列表, messages):
        """The source code of the tool 定义工具源码，必要方法，只包括该方法也可以运行工具，但是没有参数界面"""
        inputfc = 参数列表[0].valueAsText
        outputfc = 参数列表[1].valueAsText
        outcount = 参数列表[2].value
        inlist = []
        with arcpy.da.SearchCursor(inputfc, "OID@") as cursor:  # type: ignore
            for row in cursor:
                id = row[0]
                inlist.append(id)
        import random

        randomlist = random.sample(inlist, outcount)
        desc = arcpy.da.Describe(inputfc)  # type: ignore
        fldname = desc["OIDFieldName"]
        sqlfield = arcpy.AddFieldDelimiters(inputfc, fldname)
        sqlexp = "{} in {}".format(sqlfield, tuple(randomlist))
        arcpy.Select_analysis(inputfc, outputfc, sqlexp)
        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
