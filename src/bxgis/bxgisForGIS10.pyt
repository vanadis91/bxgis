# -- coding:cp936 –
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

def get_prj_info():
    # 获取解释器路径
    import os
    import toml
    toml_file_path = os.path.join(os.path.dirname(__file__),u'配置',u'项目信息.toml')
    with open(toml_file_path,mode='r')as f:
        return toml.load(f)

def add_search_path():
    # 为py3的包搜索路径中添加本项目
    import os
    import shutil
    prj_info_dict = get_prj_info()
    pkg_search_path = prj_info_dict[u'计算机信息'][u'包搜索路径_python3']
    com_pth_path_from = os.path.join(os.path.dirname(__file__),u'com.pth')
    com_pth_path_to = os.path.join(pkg_search_path,u'com.pth')
    if not os.path.isfile(com_pth_path_to):
        shutil.copy2(com_pth_path_from, com_pth_path_to)
    else:
        try:
            os.remove(com_pth_path_to)
            shutil.copy2(com_pth_path_from, com_pth_path_to)
        except Exception as e:
            print(e)

add_search_path()

def output_args(args_dict):
    # 将运行命令字典输出到文件
    import os
    args_path = os.path.join(os.path.dirname(__file__),u'命令行',u'命令行参数.json')
    with open(args_path,mode='w')as f:
        import json
        json.dump(args_dict, f, ensure_ascii=False, indent=4)

def fun_run(module_name, function_name, args_list):
    import subprocess
    import json
    args_dict = ParameterCls.convert_to_dictRawValue(args_list)
    args_dict_str = json.dumps(args_dict,ensure_ascii=False)
    run_cli_dict={
        u'模块名称'.encode('gbk'): module_name.encode('gbk'),
        u'函数名称'.encode('gbk'): function_name.encode('gbk'),
        u'参数字典'.encode('gbk'): args_dict_str,
    }
    output_args(run_cli_dict)

    prj_info_json = get_prj_info()
    interpreter_path = prj_info_json[u'计算机信息'][u'解释器路径_python3']
    str = u"\"{}\" -m bxgis.命令行.命令行包".format(interpreter_path)
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
        self.tools = [common_curveToPolyline,common_importFromCAD,config_projectInit]

class common_importFromCAD(object): 
    def __init__(self):
        self.label = u"导入从CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
            {"name": u"输入CAD数据集中的要素类路径", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
            {"name": u"是否转曲", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
            {"name": u"输出要素路径", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输出参数",'multiValue': False,'default':u'YD_CAD色块'},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u'bxgis.常用.导入从CAD',u'导入从CAD',parameterList)

class common_curveToPolyline(object): 
    # "曲转折"
    def __init__(self):
        self.label = u"曲转折"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        # init_addSearchPath()
        # from bxgis.配置 import 基本信息
        args_dict_list = [
            {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输入参数",'multiValue': True},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    # def isLicensed(self):
    #     """Set whether tool is licensed to execute."""
    #     return True

    # def updateParameters(self, 参数列表):
    #     init_addSearchPath()
    #     import bxgis.常用.导出到CAD as 导出到CAD

    #     return 导出到CAD.界面类.函数参数更新(参数列表)

    def execute(self, parameterList, message):
        fun_run(u'bxgis.常用.曲转折',u'曲转折',parameterList)

    # def updateMessages(self, parameters):
    #     """Modify the messages created by internal validation for each tool
    #     parameter.  This method is called after internal validation."""
    #     return

class config_projectInit(object): 
    def __init__(self):
        self.label = u"项目初始化"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"配置"

    def getParameterInfo(self):
        args_dict_list = [
            {"name": u"项目文件夹路径", "dataType": u"文件夹", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u'bxgis.配置.项目初始化',u'项目初始化',parameterList)
if __name__ == "__main__":
    pass