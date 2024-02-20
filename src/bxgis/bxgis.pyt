# -*- coding: utf-8 -*-


def 添加搜索路径():
    import os
    import sys

    该文件的目录 = os.path.dirname(__file__)
    if 该文件的目录.split("\\")[-1] == "bxgis":
        当前工作路径 = os.getcwd()
        os.chdir(该文件的目录)
        项目根目录 = os.path.abspath("..\\..\\")
        os.chdir(当前工作路径)
        if 项目根目录 + "\\src" not in sys.path:
            sys.path.append(项目根目录 + "\\.venv\\Lib\\site-packages")
            sys.path.append(项目根目录 + "\\src\\bxgis\\common")
            sys.path.append(项目根目录 + "\\src")
    elif 该文件的目录.split("\\")[-1] == "toolboxes":
        当前工作路径 = os.getcwd()
        os.chdir(该文件的目录)
        项目根目录 = os.path.abspath("..\\..\\..\\..\\")
        os.chdir(当前工作路径)
        if 项目根目录 + "\\src" not in sys.path:
            sys.path.append(项目根目录 + "\\.venv\\Lib\\site-packages")
            sys.path.append(项目根目录 + "\\src\\bxgis\\common")
            sys.path.append(项目根目录 + "\\src")
    else:
        raise ValueError("添加搜索路径失败。")


def 参数组字典生成_转换值(参数列表):
    参数名称列表 = [bxarcpy.参数类.名称读取(x) for x in 参数列表]
    参数字典 = {k: v for k, v in zip(参数名称列表, 参数列表)}
    参数字典temp = {}

    def 根据类型取值(参数对象):
        if type(bxarcpy.参数类.值读取(参数对象)) in [int, float, str, bool]:
            ret = bxarcpy.参数类.值读取(参数对象)
        elif type(bxarcpy.参数类.值读取(参数对象)) is list:
            ret = [根据类型取值(x) for x in 参数对象]
        else:
            ret = bxarcpy.参数类.值读取_作为字符串(参数对象)
        return ret

    for k, v in 参数字典.items():
        参数字典temp[k] = 根据类型取值(v)
    return 参数字典temp


def 参数组字典生成(参数列表):
    参数名称列表 = [bxarcpy.参数类.名称读取(x) for x in 参数列表]
    参数字典 = {k: v for k, v in zip(参数名称列表, 参数列表)}
    return 参数字典


添加搜索路径()
import bxarcpy
import bxgis
from bxpy import 日志

# import importlib


# importlib.reload(bxarcpy)
# importlib.reload(bxgis)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file) 定义了工具箱的属性"""
        self.label = "BXGIS工具箱"  # 定义标签
        self.alias = "BXGIS工具箱"  # 定义别名
        # self.category可以把工具组织成不同工具集
        # List of tool classes associated with this toolbox 定义了包含的所有工具名称列表
        self.tools = [
            ExportToCAD,
            ImportFromCAD,
            ConvertCurveToPolyline,
            LandusePlanningGeneration,
            BaseperiodLandtypeConversion,
            BaseperiodFieldsTranslateAndGenerateSubitems,
            LanduseUpdate,
            LanduseCheckIsFarmlandOccupied,
            RoadEdgeGeneration,
            RiverEdgeGeneration,
        ]


class ExportToCAD(object):
    # "导出到CAD"
    # 参数名称列表 = []
    # class 参数组对象:
    #     参数名称列表 = []
    #     输入要素 = None
    #     范围要素 = None
    #     是否对要素进行融合 = None
    #     需融合地类编号列表 = None
    #     是否对要素进行切分 = None
    #     切分时折点数量阈值 = None
    #     切分时孔洞数量阈值 = None
    #     切分时面积阈值 = None
    #     切分时地类编号限制列表 = None
    #     是否去孔 = None
    #     输出CAD路径 = None

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "导出到CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用"

    def getParameterInfo(self):
        """Define parameter definitions 定义了参数，类似脚本工具属性中的参数界面"""
        # 参数组字典列表 = [
        #     {"名称": "输入要素", "数据类型": "要素类", "参数必要性": "必填"},
        #     {"名称": "范围要素", "数据类型": "要素类", "默认值": "JX_规划范围线"},
        #     {"名称": "是否对要素进行融合", "数据类型": "布尔值", "默认值": False},
        #     {"名称": "需融合地类编号列表", "数据类型": "字符串", "是否多个值": True, "是否可用": False, "默认值": ["1207"]},
        #     {"名称": "是否对要素进行切分", "数据类型": "布尔值", "默认值": False},
        #     {"名称": "切分时折点数量阈值", "数据类型": "长整型", "是否可用": False, "默认值": 15000},
        #     {"名称": "切分时孔洞数量阈值", "数据类型": "长整型", "是否可用": False, "默认值": 3},
        #     {"名称": "切分时面积阈值", "数据类型": "双精度", "是否可用": False, "默认值": 500000},
        #     {"名称": "切分时地类编号限制列表", "数据类型": "字符串", "是否多个值": True, "是否可用": False, "默认值": ["1207"]},
        #     {"名称": "是否去孔", "数据类型": "布尔值", "默认值": False},
        #     {"名称": "输出CAD路径", "数据类型": "CAD数据集", "参数类型": "输出参数"},
        # ]
        # 参数列表 = []
        # for x in 参数组字典列表:
        #     参数组字符串 = ""
        #     if "名称" in x:
        #         参数组字符串 = 参数组字符串 + "名称=" + f"'{x['名称']}'" + ", "
        #     if "描述" in x:
        #         参数组字符串 = 参数组字符串 + "描述=" + f"'{x['描述']}'" + ", "
        #     else:
        #         参数组字符串 = 参数组字符串 + "描述=" + f"'{x['名称']}'" + ", "
        #     if "数据类型" in x:
        #         参数组字符串 = 参数组字符串 + "数据类型=" + f"'{x['数据类型']}'" + ", "
        #     if "参数必要性" in x:
        #         参数组字符串 = 参数组字符串 + "参数必要性=" + f"'{x['参数必要性']}'" + ", "
        #     if "参数类型" in x:
        #         参数组字符串 = 参数组字符串 + "参数类型=" + f"'{x['参数类型']}'" + ", "
        #     if "是否多个值" in x:
        #         参数组字符串 = 参数组字符串 + "是否多个值=" + f"{x['是否多个值']}" + ", "
        #     if "是否可用" in x:
        #         参数组字符串 = 参数组字符串 + "是否可用=" + f"{x['是否可用']}" + ", "
        #     if "默认值" in x:
        #         if type(x["默认值"]) is str:
        #             参数组字符串 = 参数组字符串 + "默认值=" + f"'{x['默认值']}'" + ", "
        #         else:
        #             参数组字符串 = 参数组字符串 + "默认值=" + f"{x['默认值']}" + ", "
        #     exec(f"{x['名称']} = bxarcpy.参数类.参数创建({参数组字符串})._内嵌对象")
        #     参数列表.append(eval(x["名称"]))
        #     ExportToCAD.参数组对象.参数名称列表.append(x["名称"])

        输入要素 = bxarcpy.参数类.参数创建("输入要素", "要素类", 参数必要性="必填")._内嵌对象

        范围要素 = bxarcpy.参数类.参数创建("范围要素", "要素类", 默认值="JX_规划范围线")._内嵌对象

        是否对要素进行融合 = bxarcpy.参数类.参数创建("是否对要素进行融合", "布尔值", 默认值=False)._内嵌对象

        需融合地类编号列表 = bxarcpy.参数类.参数创建("需融合地类编号列表", "字符串", 是否多个值=True, 是否可用=False, 默认值=["1207"])._内嵌对象

        是否对要素进行切分 = bxarcpy.参数类.参数创建("是否对要素进行切分", "布尔值", 默认值=False)._内嵌对象

        切分时折点数量阈值 = bxarcpy.参数类.参数创建("切分时折点数量阈值", "长整型", 是否可用=False, 默认值=15000)._内嵌对象

        切分时孔洞数量阈值 = bxarcpy.参数类.参数创建("切分时孔洞数量阈值", "长整型", 是否可用=False, 默认值=3)._内嵌对象

        切分时面积阈值 = bxarcpy.参数类.参数创建("切分时面积阈值", "双精度", 是否可用=False, 默认值=500000)._内嵌对象

        切分时地类编号限制列表 = bxarcpy.参数类.参数创建("切分时地类编号限制列表", "字符串", 是否多个值=True, 是否可用=False, 默认值=["1207"])._内嵌对象

        是否去孔 = bxarcpy.参数类.参数创建("是否去孔", "布尔值", 默认值=False)._内嵌对象

        输出CAD路径 = bxarcpy.参数类.参数创建("输出CAD路径", "CAD数据集", 参数类型="输出参数")._内嵌对象

        return [输入要素, 范围要素, 是否对要素进行融合, 需融合地类编号列表, 是否对要素进行切分, 切分时折点数量阈值, 切分时孔洞数量阈值, 切分时面积阈值, 切分时地类编号限制列表, 是否去孔, 输出CAD路径]

    def isLicensed(self):
        """Set whether tool is licensed to execute 可以控制许可行为，验证能否执行，检入检出许可"""
        return True

    def updateParameters(self, 参数列表):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed 定义了工具内部验证的过程，比如输入数据达到某个条件，则启用或者禁用某个参数，或者为某个参数设置默认值"""
        参数字典 = 参数组字典生成(参数列表)
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
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        # 日志.输出控制台(参数字典)
        需融合地类编号列表 = 参数字典["需融合地类编号列表"] if 参数字典["是否对要素进行融合"] else None
        切分阈值 = {"折点数量": 参数字典["切分时折点数量阈值"], "孔洞数量": 参数字典["切分时孔洞数量阈值"], "面积": 参数字典["切分时面积阈值"], "地类编号列表": 参数字典["切分时地类编号限制列表"]} if 参数字典["是否对要素进行切分"] else None
        bxgis.常用.导出到CAD(
            输入要素名称=参数字典["输入要素"],
            范围要素名称=参数字典["范围要素"],
            需融合地类编号列表=需融合地类编号列表,
            切分阈值=切分阈值,
            是否去孔=参数字典["是否去孔"],
            输出CAD路径=参数字典["输出CAD路径"],
        )
        return None

    def postExecute(self, 参数列表):
        """This method takes place after outputs are processed and
        added to the display."""
        return None


class ImportFromCAD(object):
    # "导入从CAD"
    def __init__(self):
        self.label = "导入从CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用"

    def getParameterInfo(self):
        输入CAD路径 = bxarcpy.参数类.参数创建("输入CAD路径", "CAD数据集", 参数必要性="必填")._内嵌对象

        输入CAD图层名称 = bxarcpy.参数类.参数创建("输入CAD图层名称", "字符串", 默认值="控规地块")._内嵌对象

        是否拓扑检查 = bxarcpy.参数类.参数创建("是否拓扑检查", "布尔值", 默认值=False)._内嵌对象

        是否范围检查 = bxarcpy.参数类.参数创建("是否范围检查", "布尔值", 默认值=False)._内嵌对象

        是否转曲 = bxarcpy.参数类.参数创建("是否转曲", "布尔值", 默认值=False)._内嵌对象

        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数", 默认值="YD_CAD色块")._内嵌对象

        return [输入CAD路径, 输入CAD图层名称, 是否拓扑检查, 是否范围检查, 是否转曲, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)

        bxgis.常用.导入从CAD(
            输入CAD路径列表=[参数字典["输入CAD路径"]],
            输入CAD图层名称=参数字典["输入CAD图层名称"],
            是否拓扑检查=参数字典["是否拓扑检查"],
            是否范围检查=参数字典["是否范围检查"],
            是否转曲=参数字典["是否转曲"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        """This method takes place after outputs are processed and
        added to the display."""
        return None


class ConvertCurveToPolyline(object):
    # "曲转折"
    def __init__(self):
        self.label = "曲转折"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用"

    def getParameterInfo(self):
        输入要素名称列表 = bxarcpy.参数类.参数创建("输入要素名称列表", "要素类", 参数必要性="必填", 是否多个值=True)._内嵌对象

        return [输入要素名称列表]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.常用.曲转折(输入要素名称列表=参数字典["输入要素名称列表"])
        return None

    def postExecute(self, 参数列表):
        return None


class LandusePlanningGeneration(object):
    # "用地规划图生成"
    def __init__(self):
        self.label = "用地规划图生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = "用地"

    def getParameterInfo(self):
        输入要素名称列表 = bxarcpy.参数类.参数创建(名称="输入要素名称列表", 数据类型="要素类", 参数必要性="必填", 是否多个值=True)._内嵌对象

        规划范围线要素名称 = bxarcpy.参数类.参数创建(名称="规划范围线要素名称", 数据类型="要素类", 默认值="JX_规划范围线")._内嵌对象

        是否将CAD合并入GIS = bxarcpy.参数类.参数创建(名称="是否将CAD合并入GIS", 数据类型="布尔值", 默认值=False)._内嵌对象
        CAD导出色块要素名称 = bxarcpy.参数类.参数创建(名称="CAD导出色块要素名称", 数据类型="要素类", 默认值="YD_CAD色块", 是否可用=False)._内嵌对象
        CAD导出色块中空隙的地类 = bxarcpy.参数类.参数创建("CAD导出色块中空隙的地类", 数据类型="字符串", 默认值="00", 是否可用=False)._内嵌对象
        CAD导出色块中有效的地类列表 = bxarcpy.参数类.参数创建(名称="CAD导出色块中有效的地类列表描述=", 数据类型="字符串", 默认值=["07%", "08%", "09%", "10%", "11%", "12%", "13%", "14%", "15%", "16%", "1701%", "1702%", "1703%", "23%"], 是否多个值=True, 是否可用=False)._内嵌对象
        CAD导出色块以外地类调整要素名称 = bxarcpy.参数类.参数创建(名称="CAD导出色块以外地类调整要素名称", 数据类型="要素类", 默认值="YD_CAD色块以外建设用地修改", 是否可用=False)._内嵌对象

        是否处理细小面 = bxarcpy.参数类.参数创建(名称="是否处理细小面", 数据类型="布尔值", 默认值=False)._内嵌对象
        GIS中已处理的细小面要素名称 = bxarcpy.参数类.参数创建(名称="GIS中已处理的细小面要素名称", 数据类型="要素类", 是否可用=False, 默认值="YD_已处理的细小面")._内嵌对象
        细小面面积阈值 = bxarcpy.参数类.参数创建(名称="细小面面积阈值", 数据类型="字符串", 是否可用=False, 默认值="10")._内嵌对象

        是否拓扑检查 = bxarcpy.参数类.参数创建(名称="是否拓扑检查", 数据类型="布尔值", 默认值=False)._内嵌对象
        是否范围检查 = bxarcpy.参数类.参数创建(名称="是否范围检查", 数据类型="布尔值", 默认值=False)._内嵌对象

        输出要素名称 = bxarcpy.参数类.参数创建(名称="输出要素名称", 数据类型="要素类", 参数类型="输出参数", 默认值="DIST_用地规划图")._内嵌对象

        return [输入要素名称列表, 规划范围线要素名称, 是否将CAD合并入GIS, CAD导出色块要素名称, CAD导出色块以外地类调整要素名称, CAD导出色块中空隙的地类, CAD导出色块中有效的地类列表, 是否处理细小面, GIS中已处理的细小面要素名称, 细小面面积阈值, 是否拓扑检查, 是否范围检查, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        添加搜索路径()
        参数字典 = 参数组字典生成(参数列表)
        if bxarcpy.参数类.值读取(参数字典["是否处理细小面"]):
            bxarcpy.参数类.可用性设置(参数字典["GIS中已处理的细小面要素名称"], True)
            bxarcpy.参数类.可用性设置(参数字典["细小面面积阈值"], True)
        else:
            bxarcpy.参数类.可用性设置(参数字典["GIS中已处理的细小面要素名称"], False)
            bxarcpy.参数类.可用性设置(参数字典["细小面面积阈值"], False)
        if bxarcpy.参数类.值读取(参数字典["是否将CAD合并入GIS"]):
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块要素名称"], True)
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块以外地类调整要素名称"], True)
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块中空隙的地类"], True)
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块中有效的地类列表"], True)
        else:
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块要素名称"], False)
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块以外地类调整要素名称"], False)
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块中空隙的地类"], False)
            bxarcpy.参数类.可用性设置(参数字典["CAD导出色块中有效的地类列表"], False)

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)

        bxgis.用地.用地规划图生成(
            输入要素名称列表=参数字典["输入要素名称列表"],
            规划范围线要素名称=参数字典["规划范围线要素名称"],
            是否将CAD合并入GIS=参数字典["是否将CAD合并入GIS"],
            CAD导出色块要素名称=参数字典["CAD导出色块要素名称"],
            CAD导出色块以外地类调整要素名称=参数字典["CAD导出色块以外地类调整要素名称"],
            CAD导出色块中空隙的地类=参数字典["CAD导出色块中空隙的地类"],
            CAD导出色块中有效的地类列表=参数字典["CAD导出色块中有效的地类列表"],
            是否处理细小面=参数字典["是否处理细小面"],
            GIS中已处理的细小面要素名称=参数字典["GIS中已处理的细小面要素名称"],
            是否拓扑检查=参数字典["是否拓扑检查"],
            是否范围检查=参数字典["是否范围检查"],
            细小面面积阈值=参数字典["细小面面积阈值"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


class BaseperiodLandtypeConversion(object):
    # "初步基数转换"
    def __init__(self):
        self.label = "初步基数转换"
        self.description = ""
        self.canRunInBackground = False
        self.category = "用地\\基期"

    def getParameterInfo(self):
        输入要素名称 = bxarcpy.参数类.参数创建("输入要素名称", "要素类", 参数必要性="必填", 默认值="CZ_三调_原始")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象
        return [输入要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.用地.基期.初步基数转换(输入要素名称=参数字典["输入要素名称"], 输出要素名称=参数字典["输出要素名称"])
        return None

    def postExecute(self, 参数列表):
        return None


class BaseperiodFieldsTranslateAndGenerateSubitems(object):
    # "字段处理并生成分项"
    def __init__(self):
        self.label = "字段处理并生成分项"
        self.description = ""
        self.canRunInBackground = False
        self.category = "用地\\基期"

    def getParameterInfo(self):
        输入要素名称 = bxarcpy.参数类.参数创建("输入要素名称", "要素类", 参数必要性="必填", 默认值="YD_三调")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象
        return [输入要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.用地.基期.字段处理并生成分项(输入要素名称=参数字典["输入要素名称"], 输出要素名称=参数字典["输出要素名称"])
        return None

    def postExecute(self, 参数列表):
        return None


class LanduseUpdate(object):
    # 用地更新
    def __init__(self):
        self.label = "用地更新"
        self.description = ""
        self.canRunInBackground = False
        self.category = "用地"

    def getParameterInfo(self):
        输入要素名称 = bxarcpy.参数类.参数创建("输入要素名称", "要素类", 参数必要性="必填", 默认值="DIST_用地规划图")._内嵌对象
        街坊范围线要素名称 = bxarcpy.参数类.参数创建("街坊范围线要素名称", "要素类", 默认值="JX_街坊范围线")._内嵌对象
        分村范围线要素名称 = bxarcpy.参数类.参数创建("分村范围线要素名称", "要素类", 默认值="JX_分村范围线")._内嵌对象
        城镇集建区要素名称 = bxarcpy.参数类.参数创建("城镇集建区要素名称", "要素类", 默认值="KZX_城镇集建区")._内嵌对象
        城镇弹性区要素名称 = bxarcpy.参数类.参数创建("城镇弹性区要素名称", "要素类", 默认值="KZX_城镇弹性区")._内嵌对象
        有扣除地类系数的要素名称 = bxarcpy.参数类.参数创建("有扣除地类系数的要素名称", "要素类", 默认值="CZ_三调筛选_扣除地类系数")._内嵌对象
        有坐落单位信息的要素名称 = bxarcpy.参数类.参数创建("有坐落单位信息的要素名称", "要素类", 默认值="CZ_三调筛选_坐落单位名称")._内嵌对象
        设施要素名称 = bxarcpy.参数类.参数创建("设施要素名称", "要素类", 默认值="SS_配套设施")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象

        return [输入要素名称, 街坊范围线要素名称, 分村范围线要素名称, 城镇集建区要素名称, 城镇弹性区要素名称, 有扣除地类系数的要素名称, 有坐落单位信息的要素名称, 设施要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.用地.用地更新(
            输入要素名称=参数字典["输入要素名称"],
            街坊范围线要素名称=参数字典["街坊范围线要素名称"],
            分村范围线要素名称=参数字典["分村范围线要素名称"],
            城镇集建区要素名称=参数字典["城镇集建区要素名称"],
            城镇弹性区要素名称=参数字典["城镇弹性区要素名称"],
            有扣除地类系数的要素名称=参数字典["有扣除地类系数的要素名称"],
            有坐落单位信息的要素名称=参数字典["有坐落单位信息的要素名称"],
            设施要素名称=参数字典["设施要素名称"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


class FacilitiesUpdate(object):
    # 设施更新
    def __init__(self):
        self.label = "设施更新"
        self.description = ""
        self.canRunInBackground = False
        self.category = "设施"

    def getParameterInfo(self):
        输入要素名称 = bxarcpy.参数类.参数创建("输入要素名称", "要素类", 参数必要性="必填", 默认值="SS_配套设施")._内嵌对象
        是否根据坐标字段移动设施坐标 = bxarcpy.参数类.参数创建("是否根据坐标字段移动设施坐标", "布尔值", 默认值=True)._内嵌对象
        规划范围线要素名称 = bxarcpy.参数类.参数创建("规划范围线要素名称", "要素类", 默认值="JX_规划范围线")._内嵌对象
        工业片区范围线要素名称 = bxarcpy.参数类.参数创建("工业片区范围线要素名称", "要素类", 默认值="JX_工业片区范围线")._内嵌对象
        城镇集建区要素名称 = bxarcpy.参数类.参数创建("城镇集建区要素名称", "要素类", 默认值="KZX_城镇集建区")._内嵌对象
        城镇弹性区要素名称 = bxarcpy.参数类.参数创建("城镇弹性区要素名称", "要素类", 默认值="KZX_城镇弹性区")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象
        return [输入要素名称, 是否根据坐标字段移动设施坐标, 规划范围线要素名称, 工业片区范围线要素名称, 城镇集建区要素名称, 城镇弹性区要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.设施.设施更新(
            输入要素名称=参数字典["输入要素名称"],
            是否根据坐标字段移动设施坐标=参数字典["是否根据坐标字段移动设施坐标"],
            规划范围线要素名称=参数字典["规划范围线要素名称"],
            工业片区范围线要素名称=参数字典["工业片区范围线要素名称"],
            城镇集建区要素名称=参数字典["城镇集建区要素名称"],
            城镇弹性区要素名称=参数字典["KZX_城镇弹性区"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


class LanduseCheckIsFarmlandOccupied(object):
    # 基本农田是否被占
    def __init__(self):
        self.label = "基本农田是否被占"
        self.description = ""
        self.canRunInBackground = False
        self.category = "用地\\检查"

    def getParameterInfo(self):
        输入要素名称 = bxarcpy.参数类.参数创建("输入要素名称", "要素类", 参数必要性="必填", 默认值="DIST_用地规划图")._内嵌对象
        基本农田要素名称 = bxarcpy.参数类.参数创建("基本农田要素名称", "要素类", 默认值="KZX_永久基本农田")._内嵌对象
        是否输出到CAD = bxarcpy.参数类.参数创建("是否输出到CAD", "布尔值", 默认值=True)._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象

        return [输入要素名称, 基本农田要素名称, 是否输出到CAD, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)

        bxgis.用地.检查.基本农田是否被占(
            输入要素名称=参数字典["输入要素名称"],
            基本农田要素名称=参数字典["基本农田要素名称"],
            是否输出到CAD=参数字典["是否输出到CAD"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


class RoadEdgeGeneration(object):
    # 道路边线生成
    def __init__(self):
        self.label = "道路边线生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = "道路"

    def getParameterInfo(self):
        道路中线要素名称 = bxarcpy.参数类.参数创建("道路中线要素名称", "要素类", 参数必要性="必填", 默认值="DL_道路中线")._内嵌对象
        用地要素名称 = bxarcpy.参数类.参数创建("用地要素名称", "要素类", 默认值="DIST_用地规划图")._内嵌对象
        规划范围线要素名称 = bxarcpy.参数类.参数创建("规划范围线要素名称", "要素类", 默认值="JX_规划范围线")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象

        return [道路中线要素名称, 用地要素名称, 规划范围线要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.道路.道路边线生成(
            道路中线要素名称=参数字典["道路中线要素名称"],
            用地要素名称=参数字典["用地要素名称"],
            规划范围线要素名称=参数字典["规划范围线要素名称"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


class RiverEdgeGeneration(object):
    # 河道边线生成
    def __init__(self):
        self.label = "河道边线生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = "道路"

    def getParameterInfo(self):
        河道中线要素名称 = bxarcpy.参数类.参数创建("河道中线要素名称", "要素类", 参数必要性="必填", 默认值="DL_河道中线")._内嵌对象
        用地要素名称 = bxarcpy.参数类.参数创建("用地要素名称", "要素类", 默认值="DIST_用地规划图")._内嵌对象
        规划范围线要素名称 = bxarcpy.参数类.参数创建("规划范围线要素名称", "要素类", 默认值="JX_规划范围线")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象

        return [河道中线要素名称, 用地要素名称, 规划范围线要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.道路.河道边线生成(
            河道中线要素名称=参数字典["河道中线要素名称"],
            用地要素名称=参数字典["用地要素名称"],
            规划范围线要素名称=参数字典["规划范围线要素名称"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


class RegionUpdate(object):
    # 区域更新
    def __init__(self):
        self.label = "区域更新"
        self.description = ""
        self.canRunInBackground = False
        self.category = "区域"

    def getParameterInfo(self):
        区域要素名称 = bxarcpy.参数类.参数创建("区域要素名称", "要素类", 参数必要性="必填", 默认值="JX_街坊范围线")._内嵌对象
        用地要素名称 = bxarcpy.参数类.参数创建("用地要素名称", "要素类", 默认值="DIST_用地规划图")._内嵌对象
        规划范围线要素名称 = bxarcpy.参数类.参数创建("规划范围线要素名称", "要素类", 默认值="JX_规划范围线")._内嵌对象
        输出要素名称 = bxarcpy.参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数")._内嵌对象

        return [区域要素名称, 用地要素名称, 规划范围线要素名称, 输出要素名称]

    def isLicensed(self):
        return True

    def updateParameters(self, 参数列表):
        return None

    def updateMessages(self, 参数列表):
        return None

    def execute(self, 参数列表, 消息):
        添加搜索路径()
        参数字典 = 参数组字典生成_转换值(参数列表)
        bxgis.道路.河道边线生成(
            河道中线要素名称=参数字典["河道中线要素名称"],
            用地要素名称=参数字典["用地要素名称"],
            规划范围线要素名称=参数字典["规划范围线要素名称"],
            输出要素名称=参数字典["输出要素名称"],
        )
        return None

    def postExecute(self, 参数列表):
        return None


if __name__ == "__main__":
    # def aaaa():
    #     print(locals())
    #     for i in ['a', 'b', 'c']:
    #         locals()[i] = 1
    #     print(locals())
    #     print(a)
    # aaaa()

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
