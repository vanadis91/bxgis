# -- coding:cp936 –
import arcpy
# -*- coding: gbk -*-


def init_add_search_path():
    import os
    import sys

    # 添加src目录
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

    # 添加utils目录
    directoryOfUtils = os.path.join(directoryOfSrc, "bxgis", "utils")
    if directoryOfUtils not in sys.path:
        sys.path.insert(0, directoryOfUtils)

    # 添加bxgis的第三方包搜索路径
    if directoryOfSrc.split('/')[-1] == "src":
        directoryOfProj = os.path.dirname(directoryOfSrc)
        directoryOfthirdPKG = os.path.join(directoryOfProj, ".venv", "Lib", "site-packages")
        if directoryOfthirdPKG not in sys.path:
            sys.path.insert(0, directoryOfthirdPKG)
    
    # 移除10.8的搜索路径
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
        .pyt file) 定义了工具箱的属性"""
        self.label = "BXGIS工具箱"  # 定义标签
        self.alias = "BXGIS工具箱"  # 定义别名

        # List of tool classes associated with this toolbox
        self.tools = [CurveToPolyline]


class CurveToPolyline(object): 
    # "曲转折"
    def __init__(self):
        self.label = "曲转折"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用"

    def getParameterInfo(self):
        # init_addSearchPath()
        # from bxgis.配置 import 基本信息
        from bxarcpy.ParameterPKG import ParameterCls
        inputElList = ParameterCls.parameterCreate("输入要素路径列表", 
                                                   "DEFeatureClass", 
                                                   None,
                                                   "Required",
                                                   "Input",
                                                   True)

        return [inputElList]

    # def isLicensed(self):
    #     """Set whether tool is licensed to execute."""
    #     return True

    # def updateParameters(self, 参数列表):
    #     init_addSearchPath()
    #     import bxgis.常用.导出到CAD as 导出到CAD

    #     return 导出到CAD.界面类.函数参数更新(参数列表)

    def execute(self, parameterList, message):
        # init_addSearchPath()

        from bxarcpy.ParameterPKG import ParameterCls

        parameterDict = ParameterCls.parameterListToListRawValue(parameterList)
        # 日志类.输出控制台(参数字典)
        inputElList = parameterDict[0]
        import json
        inputElList = json.dumps(inputElList)
        import subprocess

        # process = subprocess.Popen(r'C:\Users\beixiao\Project\bxarcpy\.condavenv\arcgispro-py3-clone\python.exe -m bxgis.常用.曲转折 {}'.format(parameterDict['输入要素路径列表']), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # str = u"cmd /c \"C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\"".encode('gbk')
        # str1 =u'bxgis.常用.曲转折'.encode('gbk')
        # str = "cmd /c \"start %windir%\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m {}\"".format(str1)
        # str = u"cmd /c \"start %windir%\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\"".encode('gbk')
        # str = u"C:\Windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折".encode('gbk')
        inputElList = inputElList.encode('gbk').decode('unicode_escape')
        
        str = u"C:\\Windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\appBXGis\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折 " + inputElList
        str = str.encode('gbk') 
        arcpy.AddMessage(u'运行命令:'.encode('gbk') + str)
            # print(str, file=f)

        process = subprocess.Popen(str,close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP)
        # stdout, stderr = process.communicate()
        # return_code = process.returncode
        # if stdout:
        #     arcpy.AddMessage(u'输出内容:'.encode('gbk') + stdout)
        # if stderr:
        #     arcpy.AddMessage(u'输出错误:'.encode('gbk') +stderr)
        # if return_code:
        #     arcpy.AddMessage(u'返回码:'.encode('gbk') + return_code) # type: ignore
        return None

    # def updateMessages(self, parameters):
    #     """Modify the messages created by internal validation for each tool
    #     parameter.  This method is called after internal validation."""
    #     return
if __name__ == "__main__":
    # print('111111111111111111111111111111111')
    # import subprocess
    # str = "powershell -NoExit -Command \"Start-Process $env:windir\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList '-Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折'\""
    
    # str = "cmd /c \"\"c:\\windows\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList \'-NoExit -Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\'\"\""
    # str = "cmd /c \"start %windir%\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -NoExit -Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\""
    # init_add_search_path()
    # str = "cmd /c \"C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\""
    # import sys

    # print(sys.path)
    # sys.path.remove("C:\\Program Files\\ArcGIS\\Pro\\Resources\\ArcPy")
    # str = "cmd /c \"C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\""
    # process = subprocess.Popen(str,close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP)
    # print('222222222222222222222222222222222')
    # process.wait()
    # return_code = process.returncode

    # print(stdout.decode('gbk'))
    # print(stderr.decode('gbk'))
    # print(return_code)
    pass