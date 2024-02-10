from ast import List
from bxpy import 日志
import arcpy


class 数据库类:
    def __init__(self, 路径=None):
        self.路径 = 路径
        arcpy.env.workspace = self.路径  # type: ignore

    @staticmethod
    def 数据库读取_通过路径(路径=None):
        return 数据库类(路径=路径)

    @staticmethod
    def 要素名称列表获取() -> list:
        return arcpy.ListFeatureClasses()  # type: ignore

    @staticmethod
    def 要素数据集名称列表获取() -> list:
        return arcpy.ListDatasets()  # type: ignore

    @staticmethod
    def 文件名称列表获取():
        return arcpy.ListFiles()

    @staticmethod
    def 栅格名称列表获取():
        return arcpy.ListRasters()
