# *-* coding:utf8 *-*
from bxpy.日志包 import 日志生成器
import arcpy


class 数据库类:
    # def __init__(self, 路径=None):
    #     self.路径 = 路径
    #     arcpy.env.workspace = self.路径  # type: ignore

    # @staticmethod
    # def 数据库读取_通过路径(路径=None):
    #     return 数据库类(路径=路径)

    @staticmethod
    def 数据库创建(数据库目录, 数据库名称):
        arcpy.management.CreateFileGDB(数据库目录, 数据库名称)  # type: ignore
        from bxpy.路径包 import 路径类

        return 路径类.连接(数据库目录, 数据库名称)

    @staticmethod
    def 属性获取_要素名称列表(数据库路径) -> list:
        当前数据库路径 = arcpy.env.workspace  # type: ignore
        arcpy.env.workspace = 数据库路径  # type: ignore
        ret = arcpy.ListFeatureClasses()
        arcpy.env.workspace = 当前数据库路径  # type: ignore
        return ret  # type: ignore

    @staticmethod
    def 属性获取_要素数据集名称列表(数据库路径) -> list:
        当前数据库路径 = arcpy.env.workspace  # type: ignore
        arcpy.env.workspace = 数据库路径  # type: ignore
        ret = arcpy.ListDatasets()
        arcpy.env.workspace = 当前数据库路径  # type: ignore
        return ret  # type: ignore

    @staticmethod
    def 属性获取_文件名称列表(数据库路径):
        当前数据库路径 = arcpy.env.workspace  # type: ignore
        arcpy.env.workspace = 数据库路径  # type: ignore
        ret = arcpy.ListFiles()
        arcpy.env.workspace = 当前数据库路径  # type: ignore
        return ret  # type: ignore

    @staticmethod
    def 属性获取_栅格名称列表(数据库路径):
        当前数据库路径 = arcpy.env.workspace  # type: ignore
        arcpy.env.workspace = 数据库路径  # type: ignore
        ret = arcpy.ListRasters()
        arcpy.env.workspace = 当前数据库路径  # type: ignore
        return ret  # type: ignore
