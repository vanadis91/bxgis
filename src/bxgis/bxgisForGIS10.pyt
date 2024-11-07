# -- coding:cp936 �C
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
#         raise ValueError("�������·��ʧ�ܡ�")

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
        from bxarcpy.ParameterPKG import ParameterCls

        inputElList = ParameterCls.parameterCreate("����Ҫ��·���б�", "DEFeatureClass", None,"Optional","Input",True)

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
        from bxarcpy.ParameterPKG import ParameterCls

        # parameterDict = ParameterCls.parameterListToDictRawValue(parameterList)
        # ��־��.�������̨(�����ֵ�)
        import subprocess

        # process = subprocess.Popen(r'C:\Users\beixiao\Project\bxarcpy\.condavenv\arcgispro-py3-clone\python.exe -m bxgis.����.��ת�� {}'.format(parameterDict['����Ҫ��·���б�']), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.Popen(r'C:\Users\beixiao\Project\bxarcpy\.condavenv\arcgispro-py3-clone\python.exe -m bxgis.����.��ת��', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return_code = process.returncode
        print("�������:\n", stdout)
        print("����������:\n", stderr)
        print("����ִ�з�����:", return_code)
        return None

    # def updateMessages(self, parameters):
    #     """Modify the messages created by internal validation for each tool
    #     parameter.  This method is called after internal validation."""
    #     return
if __name__ == "__main__":
    print('111111111111111111111111111111111')
    import subprocess
    # str = "powershell -NoExit -Command \"Start-Process $env:windir\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList '-Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��'\""
    str = "powershell -NoExit -Command \"\"Start-Process $env:windir\\sysnative\\WindowsPowerShell\\v1.0\\powershell.exe -ArgumentList \'-NoExit -Command C:\\Users\\beixiao\\Project\\bxarcpy\\.condavenv\\arcgispro-py3-clone\\python.exe -m bxgis.����.��ת��\'\"\""
    process = subprocess.Popen(str,close_fds=True,creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP)
    print('222222222222222222222222222222222')
    # process.wait()
    # return_code = process.returncode

    # print(stdout.decode('gbk'))
    # print(stderr.decode('gbk'))
    # print(return_code)