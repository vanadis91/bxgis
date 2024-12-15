# -- coding:cp936 �C
import arcpy
# -*- coding: gbk -*-

data_type_map = {
    u"Ҫ��ͼ��".encode('gbk'): "GPFeatureLayer",
    u"Ҫ����".encode('gbk'): "DEFeatureClass",
    u"����ֵ".encode('gbk'): "GPBoolean",
    u"˫����".encode('gbk'): "GPDouble",
    u"�ֶ�".encode('gbk'): "Field",
    u"������".encode('gbk'): "GPLong",
    u"�ַ���".encode('gbk'): "GPString",
    u"��".encode('gbk'): "DETable",
    u"�����ռ�".encode('gbk'): "DEWorkspace",
    u"ֵ��".encode('gbk'): "GPValueTable",
    u"�ļ�".encode('gbk'): "DEFile",
    u"�ļ���".encode('gbk'): "DEFolder",
    u"�����ļ�".encode('gbk'): "GPDataFile",
    u"CAD���ݼ�".encode('gbk'): "DECadDrawingDataset",
}
required_map = {
    u"����".encode('gbk'): "Required",
    u"ѡ��".encode('gbk'): "Optional",
    u"���ص��������".encode('gbk'): "Derived",
}
args_type_map = {
    u"�������".encode('gbk'): "Input",
    u"�������".encode('gbk'): "Output",
}

def get_prj_info():
    # ��ȡ������·��
    import os
    import toml
    toml_file_path = os.path.join(os.path.dirname(__file__),u'����',u'��Ŀ��Ϣ.toml')
    with open(toml_file_path,mode='r')as f:
        return toml.load(f)

def add_search_path():
    # Ϊpy3�İ�����·������ӱ���Ŀ
    import os
    import shutil
    prj_info_dict = get_prj_info()
    pkg_search_path = prj_info_dict[u'�������Ϣ'][u'������·��_python3']
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
    # �����������ֵ�������ļ�
    import os
    args_path = os.path.join(os.path.dirname(__file__),u'������',u'�����в���.json')
    with open(args_path,mode='w')as f:
        import json
        json.dump(args_dict, f, ensure_ascii=False, indent=4)

def fun_run(module_name, function_name, args_list):
    import subprocess
    import json
    args_dict = ParameterCls.convert_to_dictRawValue(args_list)
    args_dict_str = json.dumps(args_dict,ensure_ascii=False)
    run_cli_dict={
        u'ģ������'.encode('gbk'): module_name.encode('gbk'),
        u'��������'.encode('gbk'): function_name.encode('gbk'),
        u'�����ֵ�'.encode('gbk'): args_dict_str,
    }
    output_args(run_cli_dict)

    prj_info_json = get_prj_info()
    interpreter_path = prj_info_json[u'�������Ϣ'][u'������·��_python3']
    str = u"\"{}\" -m bxgis.������.�����а�".format(interpreter_path)
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
        name=u'δָ��',
        dataType=u'Ҫ��ͼ��',
        discription=None,
        required=u"ѡ��",
        argsDirction=u"�������",
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
        .pyt file) �����˹����������"""
        self.label = "BXGIS������"  # �����ǩ
        self.alias = "BXGIS������"  # �������

        # List of tool classes associated with this toolbox
        self.tools = [common_curveToPolyline,common_importFromCAD,config_projectInit]

class common_importFromCAD(object): 
    def __init__(self):
        self.label = u"�����CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
            {"name": u"����CAD���ݼ��е�Ҫ����·��", "dataType": u"Ҫ����", "required": u'����', "argsDirction": u"�������",'multiValue': False},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':False},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':False},
            {"name": u"�Ƿ�ת��", "dataType": u"����ֵ", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':False},
            {"name": u"���Ҫ��·��", "dataType": u"Ҫ����", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':u'YD_CADɫ��'},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u'bxgis.����.�����CAD',u'�����CAD',parameterList)

class common_curveToPolyline(object): 
    # "��ת��"
    def __init__(self):
        self.label = u"��ת��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        # init_addSearchPath()
        # from bxgis.���� import ������Ϣ
        args_dict_list = [
            {"name": u"����Ҫ��·���б�", "dataType": u"Ҫ����", "required": u'����', "argsDirction": u"�������",'multiValue': True},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    # def isLicensed(self):
    #     """Set whether tool is licensed to execute."""
    #     return True

    # def updateParameters(self, �����б�):
    #     init_addSearchPath()
    #     import bxgis.����.������CAD as ������CAD

    #     return ������CAD.������.������������(�����б�)

    def execute(self, parameterList, message):
        fun_run(u'bxgis.����.��ת��',u'��ת��',parameterList)

    # def updateMessages(self, parameters):
    #     """Modify the messages created by internal validation for each tool
    #     parameter.  This method is called after internal validation."""
    #     return

class config_projectInit(object): 
    def __init__(self):
        self.label = u"��Ŀ��ʼ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
            {"name": u"��Ŀ�ļ���·��", "dataType": u"�ļ���", "required": u'����', "argsDirction": u"�������",'multiValue': False},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u'bxgis.����.��Ŀ��ʼ��',u'��Ŀ��ʼ��',parameterList)
if __name__ == "__main__":
    pass