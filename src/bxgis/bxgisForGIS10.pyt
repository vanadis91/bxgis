# -- coding:cp936 –
import arcpy
# -*- coding: gbk -*-


# def init_addSearchPath():
#     import os
#     import sys

#     dirnameOfThisFlie = os.path.dirname(__file__)
#     if dirnameOfThisFlie.split(os.sep)[-1] == "bxgis":
#         workPath = os.getcwd()
#         os.chdir(dirnameOfThisFlie)
#         srcPath = os.path.abspath("..")
#         os.chdir(workPath)
#     elif dirnameOfThisFlie.split(os.sep)[-1] == "toolboxes":
#         workPath = os.getcwd()
#         os.chdir(dirnameOfThisFlie)
#         srcPath = os.path.abspath("..{0}..{0}..{0}".format(os.sep))
#         os.chdir(workPath)
#     else:
#         raise ValueError("添加搜索路径失败。")

#     if srcPath not in sys.path:
#         sys.path.insert(0, srcPath)
#     projRootPath = os.path.dirname(srcPath)
#     pathOfThirdPkg = os.path.join(projRootPath, ".venv", "Lib", "site-packages")
#     if pathOfThirdPkg not in sys.path:
#         sys.path.insert(0, pathOfThirdPkg)


def init_modReset(module):
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

        inputElList = ParameterCls.parameterCreate("输入要素路径列表", "DEFeatureClass", None,"Optional","Input",True)

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

        # parameterDict = ParameterCls.parameterListToDictRawValue(parameterList)
        # 日志类.输出控制台(参数字典)
        import subprocess

        # process = subprocess.Popen(r'C:\Users\beixiao\Project\bxarcpy\.condavenv\arcgispro-py3-clone\python.exe -m bxgis.常用.曲转折 {}'.format(parameterDict['输入要素路径列表']), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.Popen(r'C:\Users\beixiao\Project\bxarcpy\.condavenv\arcgispro-py3-clone\python.exe -m bxgis.常用.曲转折', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        print("命令输出:\n", stdout)
        print("命令错误输出:\n", stderr)
        print("命令执行返回码:", return_code)
        return None

    # def updateMessages(self, parameters):
    #     """Modify the messages created by internal validation for each tool
    #     parameter.  This method is called after internal validation."""
    #     return
if __name__ == "__main__":
    print('111111111111111111111111111111111')
    import subprocess
    # str = "powershell -NoExit -Command \"Start-Process $env:windir\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList '-Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折'\""
    str = "powershell -NoExit -Command \"\"Start-Process $env:windir\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList \'-NoExit -Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.常用.曲转折\'\"\""
    process = subprocess.Popen(str,close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP)
    print('222222222222222222222222222222222')
    # process.wait()
    # return_code = process.returncode

    # print(stdout.decode('gbk'))
    # print(stderr.decode('gbk'))
    # print(return_code)