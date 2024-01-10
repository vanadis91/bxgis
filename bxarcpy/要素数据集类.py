from bxpy import 日志
import arcpy
from .配置类 import 配置


class 要素数据集类:
    def __init__(self, 内嵌对象=None, 名称=None):
        if 内嵌对象:
            self.名称 = 内嵌对象.名称
        elif 名称:
            self.名称 = 名称

    @staticmethod
    def 要素数据集读取_通过名称(名称=None):
        return 要素数据集类(名称=名称)

    @staticmethod
    def 要素数据集创建(要素集名称, 数据库路径=None):
        if 数据库路径 is None:
            数据库路径 = 配置.当前工作空间
        路径 = arcpy.management.CreateFeatureDataset(out_dataset_path=数据库路径, out_name=要素集名称, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]
        return 要素数据集类(名称=路径)

    def 要素数据集删除(self):
        return arcpy.management.Delete(in_data=[self.名称], data_type="")[0]

    @staticmethod
    def 导入从CAD(CAD路径列表, 输出要素数据集名称):
        日志.输出调试(f"CAD路径列表：{CAD路径列表}")
        日志.输出调试(f"配置.当前工作空间：{配置.当前工作空间}")
        日志.输出调试(f"输出要素数据集名称：{输出要素数据集名称}")
        arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD路径列表, out_gdb_path=配置.当前工作空间, out_dataset_name=输出要素数据集名称, reference_scale=1000, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]
        return 要素数据集类(名称=输出要素数据集名称)
