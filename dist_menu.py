# *-* coding:utf8 *-*
import ast
from bxpy.基本对象包 import 字类


def 解析py文件(文件路径="src\\bxgis\\常用\\导出到CAD.py"):
    ret = {}
    with open(文件路径, "r", encoding="utf-8") as file:
        源代码 = file.read()
    语法树 = ast.parse(源代码)

    文件路径列表 = 文件路径.split("\\")
    文件路径列表[-1] = 文件路径列表[-1][:-3]
    i = 文件路径列表.index("bxgis")
    ret["模块名称"] = ".".join(文件路径列表[i:])
    ret["分类"] = ".".join(文件路径列表[i:][1:-1])

    for 节点 in ast.walk(语法树):
        if isinstance(节点, ast.FunctionDef):
            ret["函数名称"] = 节点.name
            ret["标签"] = 节点.name
            ret["文档注释"] = ast.get_docstring(节点)

            函数参数列表 = []
            for 参数 in 节点.args.args:
                函数参数列表.append(参数.arg)

            函数参数默认值列表 = []
            for 默认值 in 节点.args.defaults:
                函数参数默认值列表.append(ast.unparse(默认值))  # type: ignore
            第一个有默认值的参数的索引 = len(函数参数列表) - len(函数参数默认值列表)

            参数定义列表 = []
            for i, 参数名称 in enumerate(函数参数列表):
                构造数据 = {"参数名称": 参数名称, "数据类型": "字符串", "是否必须": "必填", "参数类型": "输入参数", "是否多选": "False"}

                if 参数名称.endswith("列表"):
                    构造数据["数据类型"] = "任何值"
                    构造数据["是否多选"] = "True"
                if "输入要素" in 参数名称:
                    构造数据["数据类型"] = "要素类"
                if "是否" in 参数名称:
                    构造数据["数据类型"] = "布尔值"
                if "输出" in 参数名称:
                    构造数据["参数类型"] = "输出参数"
                if i >= 第一个有默认值的参数的索引:
                    默认值 = 函数参数默认值列表[i - 第一个有默认值的参数的索引]
                    if 默认值 == "None":
                        默认值raw = "None"
                        构造数据["是否必须"] = "选填"
                    elif 默认值 in ["True", "False"]:
                        默认值raw = 默认值
                        构造数据["数据类型"] = "布尔值"
                    elif 默认值[0] == "[" and 默认值[-1] == "]":
                        构造数据["是否多选"] = "True"
                        默认值raw = f"{默认值}"
                    elif (默认值[0] == '"' and 默认值[-1] == '"') or (默认值[0] == "'" and 默认值[-1] == "'"):
                        # 默认值raw = 默认值.replace("\\", "\\\\")
                        # 默认值raw = 默认值raw.replace('"', '\\"')
                        默认值raw = f"u{默认值}"
                    else:
                        默认值raw = f'u"{默认值}"'
                    构造数据["默认值"] = 默认值raw
                参数定义列表.append(构造数据)
            ret["参数定义列表"] = 参数定义列表
            break
    # print(ret)
    # print(ast.dump(语法树, indent=2), file=open("src\\bxgis\\常用\\导出到CAD1.txt", "w"))
    try:
        import importlib

        模块 = importlib.import_module(ret["模块名称"])
        if hasattr(模块, "界面类"):
            界面类 = getattr(模块, "界面类")
            if hasattr(界面类, "分类"):
                ret["分类"] = getattr(界面类, "分类")
    except Exception as e:
        raise Exception(f"{文件路径}解析失败，{e}")

    return ret


def 工具界面代码生成(工具标签, 工具分类, 参数定义列表, 模块名称, 函数名称):
    from pypinyin import pinyin, Style

    工具类类名 = "_".join(["".join(item) for item in pinyin(工具标签, style=Style.NORMAL)]).replace("___", "_")
    # 工具类类名 = 字类.字符串生成_短GUID()

    参数定义列表字符串temp = ""
    for 参数定义 in 参数定义列表:
        if "默认值" not in 参数定义:
            参数定义字符串子串 = f"""{{"name": u"{参数定义['参数名称']}", "dataType": u"{参数定义['数据类型']}", "required": u"{参数定义['是否必须']}", "argsDirction": u"{参数定义['参数类型']}", "multiValue": {参数定义['是否多选']}}},
            """
        else:
            参数定义字符串子串 = f"""{{"name": u"{参数定义['参数名称']}", "dataType": u"{参数定义['数据类型']}", "required": u"{参数定义['是否必须']}", "argsDirction": u"{参数定义['参数类型']}", "multiValue": {参数定义['是否多选']}, "default": {参数定义['默认值']}}},
            """
        参数定义列表字符串temp = 参数定义列表字符串temp + 参数定义字符串子串
    参数定义列表字符串 = 参数定义列表字符串temp

    工具分类raw = 工具分类.replace(".", "\\\\")

    工具定义类字符串 = f"""
class {工具类类名}(object):
    # {工具标签}
    def __init__(self):
        self.label = u"{工具标签}"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"{工具分类raw}"

    def getParameterInfo(self):
        args_dict_list = [
        {参数定义列表字符串}]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"{模块名称}", u"{工具标签}", parameterList)
    """
    return 工具定义类字符串, 工具类类名


def main():
    pyt文件原内容字符串 = '''# -- coding:cp936 –
import arcpy
# -*- coding: gbk -*-

data_type_map = {
    u"要素图层".encode('gbk'): "GPFeatureLayer",
    u"要素类".encode('gbk'): "DEFeatureClass",
    u"布尔值".encode('gbk'): "GPBoolean",
    u"双精度".encode('gbk'): "GPDouble",
    u"字段".encode('gbk'): "Field",
    u"长整型".encode('gbk'): "GPLong",
    u"字符串".encode('gbk'): "GPString",
    u"表".encode('gbk'): "DETable",
    u"工作空间".encode('gbk'): "DEWorkspace",
    u"值表".encode('gbk'): "GPValueTable",
    u"文件".encode('gbk'): "DEFile",
    u"文件夹".encode('gbk'): "DEFolder",
    u"数据文件".encode('gbk'): "GPDataFile",
    u"CAD数据集".encode('gbk'): "DECadDrawingDataset",
    u"变量".encode('gbk'): "GPVariant",
    u"任何值".encode('gbk'): "GPType",
}
required_map = {
    u"必填".encode('gbk'): "Required",
    u"选填".encode('gbk'): "Optional",
    u"隐藏的输出参数".encode('gbk'): "Derived",
}
args_type_map = {
    u"输入参数".encode('gbk'): "Input",
    u"输出参数".encode('gbk'): "Output",
}

# def get_prj_info():
#     # 获取项目信息
#     import os
#     import yaml
#     toml_file_path = os.path.join(os.path.dirname(__file__),u'配置',u'项目信息.toml')
#     with open(toml_file_path,mode='r')as f:
#         return yaml.load(f)
def get_registry_value(key_path, value_name):
    import _winreg as winreg
    # 打开注册表项
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        # 获取指定名称的值
        value, regtype = winreg.QueryValueEx(key, value_name)
        # 关闭注册表项
        winreg.CloseKey(key)
        return value
    
    except WindowsError as e:
        raise Exception(u"无法找到arcgis_pro的安装路径".encode('gbk'))

def add_search_path():
    # 为py3的包搜索路径中添加本项目
    import os
    import shutil
    arcgis_pro_install_dir = get_registry_value(r"SOFTWARE\\ESRI\\ArcGISPro",'InstallDir')
    pkg_search_path = os.path.join(arcgis_pro_install_dir,'bin','Python','envs','arcgispro-py3','Lib','site-packages')
    com_pth_path_from = os.path.join(os.path.dirname(__file__),u'com.pth')
    com_pth_path_to = os.path.join(pkg_search_path,u'com.pth')
    if not os.path.isfile(com_pth_path_to):
        shutil.copy2(com_pth_path_from, com_pth_path_to)
    else:
        try:
            os.remove(com_pth_path_to)
            shutil.copy2(com_pth_path_from, com_pth_path_to)
        except Exception as e:
            print(u"无法删除原有的com.pth".encode('gbk'))

add_search_path()

def fun_run(module_name, function_name, args_list):
    import subprocess
    import json
    import os
    import arcpy

    args_dict = ParameterCls.convert_to_dictRawValue(args_list)
    args_dict_str = json.dumps(args_dict,ensure_ascii=False)

    run_cli_dict={
        u'模块名称'.encode('gbk'): module_name.encode('gbk'),
        u'函数名称'.encode('gbk'): function_name.encode('gbk'),
        u'参数字典'.encode('gbk'): args_dict_str,
        u'当前工作空间'.encode('gbk'): arcpy.env.workspace.encode('gbk'),
    }

    args_path = os.path.join(os.path.dirname(__file__),u'命令行',u'命令行参数.json')
    with open(args_path,mode='w')as f:
        json.dump(run_cli_dict, f, ensure_ascii=False, indent=4)

    arcgis_pro_install_dir = get_registry_value(r"SOFTWARE\\ESRI\\ArcGISPro",'InstallDir')
    interpreter_path = os.path.join(arcgis_pro_install_dir,'bin','Python','envs','arcgispro-py3','python.exe')
    str = u"\\"{}\\" -m bxgis.命令行.命令行包".format(interpreter_path)
    process = subprocess.Popen(str.encode('gbk'))
    return None

class ParameterCls:
    @staticmethod
    def parameterCreate_muti(args_dict_list):
        ret_list = []
        for args_dict in args_dict_list:
            a = ParameterCls.parameterCreate(**args_dict)
            ret_list.append(a)
        return ret_list

    @staticmethod
    def parameterCreate(
        name=u'未指定',
        dataType=u'要素图层',
        discription=None,
        required=u"选填",
        argsDirction=u"输入参数",
        multiValue=False,
        enabled=True,
        default=None,
        dependenciesParameterNameList=None,
        parameterOptionType=None,
        parameterOptionList=None,
    ):
        name = name.encode('gbk')
        dataTypeRaw = data_type_map.get(dataType.encode('gbk'),dataType)
        requiredRaw = required_map.get(required.encode('gbk'),required) 
        directionRaw = args_type_map.get(argsDirction.encode('gbk'),argsDirction) 
        discription = name if discription is None else discription
        ret = arcpy.Parameter(
            name=name,
            displayName=discription,
            direction=directionRaw,
            datatype=dataTypeRaw,
            parameterType=requiredRaw,
            enabled=enabled,
            multiValue=multiValue,
        )

        if default:
            ParameterCls.attrSet_value(ret, default)

        if dependenciesParameterNameList:
            ParameterCls.attrGet_dependencies(ret, dependenciesParameterNameList)

        if parameterOptionType == "ValueList":
            ret.filter.type = "ValueList"
        elif parameterOptionType == "Range":
            ret.filter.type = "Range"
        if parameterOptionType and parameterOptionList:
            valueRaw = [x for x in parameterOptionList]
            ret.filter.list = valueRaw
        return ret

    @staticmethod
    def attrGet_value(parameterObject):
        return parameterObject.value

    @staticmethod
    def attrSet_value(parameterObject, value):
        parameterObject.value = value  # type: ignore

    @staticmethod
    def attrGet_valueAsText(parameterObject):
        return parameterObject.valueAsText

    @staticmethod
    def attrGet_name(parameterObject):
        return parameterObject.name

    @staticmethod
    def attrGet_enabled(parameterObject, boolen):
        parameterObject.enabled = boolen  # type: ignore

    @staticmethod
    def attrGet_dependencies(parameterObject, parameterNameList):
        parameterObject.parameterDependencies = parameterNameList  # type: ignore

    @staticmethod
    def attrGet_filter(parameterObject):
        return parameterObject.filter  # type: ignore

    class FilterCls:
        @staticmethod
        def attrSet_type(filterObject, type):
            typeRaw = type
            filterObject.type = typeRaw  # type: ignore

        @staticmethod
        def attrSet_value(filterObject, value):
            valueRaw = [x for x in value]
            filterObject.list = valueRaw

    @staticmethod
    def convert_to_listRawValue(parameterList):
        def getRawValue(parameterObject):
            if type(ParameterCls.attrGet_value(parameterObject)) in [int, float, str, bool]:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif ParameterCls.attrGet_value(parameterObject) is None:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif type(ParameterCls.attrGet_value(parameterObject)) is list:
                ret = [getRawValue(x) for x in parameterObject]
            else:
                ret = ParameterCls.attrGet_valueAsText(parameterObject)
            return ret
        
        patameterListTemp = []
        for x in parameterList:
            patameterListTemp.append(getRawValue(x))
        return patameterListTemp
    
    @staticmethod
    def convert_to_dictRawValue(parameterList):
        parameterNameList = [ParameterCls.attrGet_name(x).encode('gbk') for x in parameterList]
        parameterDict = {k: v for k, v in zip(parameterNameList, parameterList)}
        patameterDictTemp = {}

        def getRawValue(parameterObject):
            if type(ParameterCls.attrGet_value(parameterObject)) in [int, float, bool]:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif type(ParameterCls.attrGet_value(parameterObject)) is str:
                ret = ParameterCls.attrGet_value(parameterObject).encode('gbk')
            elif type(ParameterCls.attrGet_value(parameterObject)) is list:
                ret = [getRawValue(x) for x in parameterObject]
            elif ParameterCls.attrGet_value(parameterObject) is None:
                ret = ParameterCls.attrGet_value(parameterObject)
            else:
                ret = ParameterCls.attrGet_valueAsText(parameterObject).encode('gbk')
            return ret

        for k, v in parameterDict.items():
            patameterDictTemp[k] = getRawValue(v)
        return patameterDictTemp

    @staticmethod
    def convert_to_dict(parameterList):
        parameterNameList = [ParameterCls.attrGet_name(x) for x in parameterList]
        parameterDict = {k: v for k, v in zip(parameterNameList, parameterList)}
        return parameterDict


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file) 定义了工具箱的属性"""
        self.label = "BXGIS工具箱"  # 定义标签
        self.alias = "BXGIS工具箱"  # 定义别名

        # List of tool classes associated with this toolbox
        self.tools = [${模块名称字符串列表},]

# class common_importFromCAD(object): 
#     def __init__(self):
#         self.label = u"导入从CAD"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"常用"

#     def getParameterInfo(self):
#         args_dict_list = [
#             {"name": u"输入CAD数据集中的要素类路径", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False},
#             {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
#             {"name": u"是否范围检查", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
#             {"name": u"是否转曲", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
#             {"name": u"输出要素路径", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输出参数",'multiValue': False,'default':u'YD_CAD色块'},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.常用.导入从CAD',u'导入从CAD',parameterList)

# class common_curveToPolyline(object): 
#     # "曲转折"
#     def __init__(self):
#         self.label = u"曲转折"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"常用"

#     def getParameterInfo(self):
#         # init_addSearchPath()
#         # from bxgis.配置 import 基本信息
#         args_dict_list = [
#             {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输入参数",'multiValue': True},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     # def isLicensed(self):
#     #     """Set whether tool is licensed to execute."""
#     #     return True

#     # def updateParameters(self, 参数列表):
#     #     init_addSearchPath()
#     #     import bxgis.常用.导出到CAD as 导出到CAD

#     #     return 导出到CAD.界面类.函数参数更新(参数列表)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.常用.曲转折',u'曲转折',parameterList)

#     # def updateMessages(self, parameters):
#     #     """Modify the messages created by internal validation for each tool
#     #     parameter.  This method is called after internal validation."""
#     #     return

# class config_projectInit(object): 
#     def __init__(self):
#         self.label = u"项目初始化"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"配置"

#     def getParameterInfo(self):
#         args_dict_list = [
#             {"name": u"项目文件夹路径", "dataType": u"文件夹", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.配置.项目初始化',u'项目初始化',parameterList)
'''

    路径 = r"C:\Users\beixiao\Project\appBXGis\src\bxgis"
    from bxpy.路径包 import 路径类
    from bxpy.基本对象包 import 字类

    子路径列表 = 路径类.子路径(路径, False)
    工具类类名列表 = []
    for 子路径x in 子路径列表:
        if not 字类.匹配正则列表(子路径x[0], [r"bxgis\\常用", r"bxgis\\道路", r"bxgis\\分区", r"bxgis\\分析", r"bxgis\\配置", r"bxgis\\区域", r"bxgis\\入库", r"bxgis\\设施", r"bxgis\\属性", r"bxgis\\用地"]):
            continue
        for 文件x in 子路径x[2]:
            if 文件x.endswith(".py") and 文件x not in ["__init__.py", "__main__.py"] and not 字类.匹配正则(文件x, r"\d{2}\.\d{2}\.\d{2}\.py$"):
                print(f"正在解析{路径类.连接(子路径x[0], 文件x)}")
                try:
                    解析数据 = 解析py文件(路径类.连接(子路径x[0], 文件x))
                    if "函数名称" not in 解析数据:
                        continue
                    工具代码字符串, 工具类类名 = 工具界面代码生成(工具标签=解析数据["标签"], 工具分类=解析数据["分类"], 参数定义列表=解析数据["参数定义列表"], 模块名称=解析数据["模块名称"], 函数名称=解析数据["函数名称"])
                    pyt文件原内容字符串 = pyt文件原内容字符串 + 工具代码字符串
                    工具类类名列表.append(工具类类名)
                except Exception as e:
                    print(f"{路径类.连接(子路径x[0], 文件x)}解析失败，{e}")
                    continue
    工具类列表字符串 = ", ".join(工具类类名列表)
    pyt文件原内容字符串 = pyt文件原内容字符串.replace("${模块名称字符串列表}", 工具类列表字符串)
    with open(r"C:\Users\beixiao\Project\appBXGis\src\bxgis\bxgisForGIS10.pyt", "w") as f:
        f.write(pyt文件原内容字符串)


if __name__ == "__main__":
    main()
    # from bxpy.基本对象包 import 字典类

    # a = 字典类.转换_从文件(r"C:\Users\beixiao\Project\appBXGis\src\bxgis\配置\项目信息.toml")
    # print(a)
    # 字典类.转换_到文件(a, r"C:\Users\beixiao\Project\appBXGis\src\bxgis\配置\项目信息.yml")
