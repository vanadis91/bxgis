# -- coding:cp936 �C
import arcpy
# -*- coding: gbk -*-

# _��������ӳ�� = {
#     "Ҫ��ͼ��": "GPFeatureLayer",
#     "Ҫ����": "DEFeatureClass",
#     "����ֵ": "GPBoolean",
#     "˫����": "GPDouble",
#     "�ֶ�": "Field",
#     "������": "GPLong",
#     "�ַ���": "GPString",
#     "��": "DETable",
#     "�����ռ�": "DEWorkspace",
#     "ֵ��": "GPValueTable",
#     "�ļ�": "DEFile",
#     "�ļ���": "DEFolder",
#     "�����ļ�": "GPDataFile",
#     "CAD���ݼ�": "DECadDrawingDataset",
# }
# _���ݱ�Ҫ��ӳ�� = {
#     "����": "Required",
#     "ѡ��": "Optional",
#     "���ص��������": "Derived",
# }
# _��������ӳ�� = {
#     "�������": "Input",
#     "�������": "Output",
# }

class ParameterCls:
    @staticmethod
    def parameterCreate(
        name,
        dataType,
        discription=None,
        required="Optional",
        parameterDirection="Input",
        multiValue=False,
        enabled=True,
        default=None,
        dependenciesParameterNameList=None,
        parameterOptionType=None,
        parameterOptionList=None,
    ):
        dataTypeRaw = dataType
        requiredRaw = required
        directionRaw = parameterDirection
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
        parameterNameList = [ParameterCls.attrGet_name(x) for x in parameterList]
        parameterDict = {k: v for k, v in zip(parameterNameList, parameterList)}
        patameterDictTemp = {}

        def getRawValue(parameterObject):
            if type(ParameterCls.attrGet_value(parameterObject)) in [int, float, str, bool]:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif type(ParameterCls.attrGet_value(parameterObject)) is list:
                ret = [getRawValue(x) for x in parameterObject]
            else:
                ret = ParameterCls.attrGet_valueAsText(parameterObject)
            return ret

        for k, v in parameterDict.items():
            patameterDictTemp[k] = getRawValue(v)
        return patameterDictTemp

    @staticmethod
    def convert_to_dict(parameterList):
        parameterNameList = [ParameterCls.attrGet_name(x) for x in parameterList]
        parameterDict = {k: v for k, v in zip(parameterNameList, parameterList)}
        return parameterDict



def init_add_search_path():
    import os
    import sys

    # ���srcĿ¼
    directoryOfThisFile = os.path.dirname(__file__)
    # print(directoryOfThisFile.split('/')[-1])
    # print(directoryOfThisFile.split('/'))
    if directoryOfThisFile.split('/')[-1] == "bxgis":
        directoryOfSrc = os.path.dirname(directoryOfThisFile)
    elif directoryOfThisFile.split('/')[-1] == "toolboxes":
        directoryOfThisFile = os.path.dirname(directoryOfThisFile)
        directoryOfThisFile = os.path.dirname(directoryOfThisFile)
        directoryOfSrc = os.path.dirname(directoryOfThisFile)
    else:
        raise ValueError("failed to add search path.")
    if directoryOfSrc not in sys.path:
        sys.path.insert(0, directoryOfSrc)

    # ���utilsĿ¼
    directoryOfUtils = os.path.join(directoryOfSrc, "bxgis", "utils")
    if directoryOfUtils not in sys.path:
        sys.path.insert(0, directoryOfUtils)

    # ���bxgis�ĵ�����������·��
    if directoryOfSrc.split('/')[-1] == "src":
        directoryOfProj = os.path.dirname(directoryOfSrc)
        directoryOfthirdPKG = os.path.join(directoryOfProj, ".venv", "Lib", "site-packages")
        if directoryOfthirdPKG not in sys.path:
            sys.path.insert(0, directoryOfthirdPKG)
    
    # �Ƴ�10.8������·��
    # for path_x in sys.path:
    #     if 'Program Files (x86)'.upper() in path_x.upper():
    #         print(path_x)
    #         sys.path.remove(path_x)
    # sys.path.remove('C:\\Program Files (x86)\\ArcGIS\\Desktop10.8\\ArcPy')
    
    # if "C:\\Program Files (x86)\\ArcGIS\\Desktop10.8\\bin" in sys.path:
    #     sys.path.remove("C:\\Program Files (x86)\\ArcGIS\\Desktop10.8\\bin")
    # if "c:/program files (x86)/arcgis/desktop10.8/bin" in sys.path:
    #     sys.path.remove("c:/program files (x86)/arcgis/desktop10.8/bin")

    # if "c:\\program files (x86)\\arcgis\\desktop10.8\\arcpy" in sys.path:
    #     sys.path.remove("c:\\program files (x86)\\arcgis\\desktop10.8\\arcpy")
    # if "c:/program files (x86)/arcgis/desktop10.8/arcPy" in sys.path:
    #     sys.path.remove("c:/program files (x86)/arcgis/desktop10.8/arcPy")

    # if "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcToolbox\\Scripts" in sys.path:
    #     sys.path.remove("c:\\program files (x86)\\arcgis\\desktop10.8\\ArcToolbox\\Scripts")
    # if "c:/program files (x86)/arcgis/desktop10.8/ArcToolbox/Scripts" in sys.path:
    #     sys.path.remove("c:/program files (x86)/arcgis/desktop10.8/ArcToolbox/Scripts")
    # print(sys.path)
        

def init_mod_reset(module):
    import importlib

    importlib.reload(module)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file) �����˹����������"""
        self.label = "BXGIS������"  # �����ǩ
        self.alias = "BXGIS������"  # �������

        # List of tool classes associated with this toolbox
        self.tools = [CurveToPolyline]


class CurveToPolyline(object): 
    # "��ת��"
    def __init__(self):
        self.label = "��ת��"
        self.description = ""
        self.canRunInBackground = False
        self.category = "����"

    def getParameterInfo(self):
        # init_addSearchPath()
        # from bxgis.���� import ������Ϣ
        inputElList = ParameterCls.parameterCreate("����Ҫ��·���б�", 
                                                   "DEFeatureClass", 
                                                   None,
                                                   "Required",
                                                   "Input",
                                                   True)
        return [inputElList]

    # def isLicensed(self):
    #     """Set whether tool is licensed to execute."""
    #     return True

    # def updateParameters(self, �����б�):
    #     init_addSearchPath()
    #     import bxgis.����.������CAD as ������CAD

    #     return ������CAD.������.������������(�����б�)

    def execute(self, parameterList, message):
        # init_addSearchPath()
        import json
        import subprocess
        parameterDict = ParameterCls.convert_to_listRawValue(parameterList)
        # ��־��.�������̨(�����ֵ�)
        inputElList = parameterDict[0]
        inputElList = json.dumps(inputElList).encode('gbk').decode('unicode_escape')
        # process = subprocess.Popen(r'C:\Users\beixiao\Project\bxarcpy\.condavenv\arcgispro-py3-clone\python.exe -m bxgis.����.��ת�� {}'.format(parameterDict['����Ҫ��·���б�']), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # str = u"cmd /c \"C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\"".encode('gbk')
        # str1 =u'bxgis.����.��ת��'.encode('gbk')
        # str = "cmd /c \"start %windir%\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m {}\"".format(str1)
        # str = u"cmd /c \"start %windir%\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\"".encode('gbk')
        # str = u"C:\Windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��".encode('gbk')
        
        
        str = u"C:\\Windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת�� {}".format(inputElList).encode('gbk') 
        arcpy.AddMessage(u'��������:'.encode('gbk') + str)
        process = subprocess.Popen(str,close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP)
        # stdout, stderr = process.communicate()
        # return_code = process.returncode
        # if stdout:
        #     arcpy.AddMessage(u'�������:'.encode('gbk') + stdout)
        # if stderr:
        #     arcpy.AddMessage(u'�������:'.encode('gbk') +stderr)
        # if return_code:
        #     arcpy.AddMessage(u'������:'.encode('gbk') + return_code) # type: ignore
        return None

    # def updateMessages(self, parameters):
    #     """Modify the messages created by internal validation for each tool
    #     parameter.  This method is called after internal validation."""
    #     return
if __name__ == "__main__":
    # print('111111111111111111111111111111111')
    # import subprocess
    # str = "powershell -NoExit -Command \"Start-Process $env:windir\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList '-Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��'\""
    
    # str = "cmd /c \"\"c:\\windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList \'-NoExit -Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\'\"\""
    # str = "cmd /c \"start %windir%\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\""
    # init_add_search_path()
    # str = "cmd /c \"C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\""
    # import sys

    # print(sys.path)
    # sys.path.remove("C:\\Program Files\\ArcGIS\\Pro\\Resources\\ArcPy")
    # str = "cmd /c \"C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\""
    # process = subprocess.Popen(str,close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP)
    # print('222222222222222222222222222222222')
    # process.wait()
    # return_code = process.returncode

    # print(stdout.decode('gbk'))
    # print(stderr.decode('gbk'))
    # print(return_code)
    pass