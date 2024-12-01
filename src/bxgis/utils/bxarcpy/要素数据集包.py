from bxpy.日志包 import 日志生成器
import arcpy


class 要素数据集类:
    # def __init__(self, 内嵌对象=None, 名称=None):
    #     if 内嵌对象:
    #         self.名称 = 内嵌对象.名称
    #     elif 名称:
    #         self.名称 = 名称

    # @staticmethod
    # def 要素数据集读取_通过名称(名称=None):
    #     return 要素数据集类(名称=名称)

    @staticmethod
    def 要素数据集创建(要素集名称, 数据库路径="当前工作空间", 删除既有同名要素数据集=True):
        from bxarcpy.环境包 import 环境类

        if 数据库路径 == "当前工作空间":
            数据库路径 = 环境类.属性获取_当前工作空间()

        from bxarcpy.要素数据集包 import 要素数据集类
        from bxarcpy.数据库包 import 数据库类

        要素数据集名称列表 = 数据库类.属性获取_要素数据集名称列表(数据库路径)

        if 要素集名称 in 要素数据集名称列表:
            if 删除既有同名要素数据集:
                要素数据集类.删除(要素集名称)
                新建的要素数据集名称 = arcpy.management.CreateFeatureDataset(out_dataset_path=数据库路径, out_name=要素集名称, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]  # type: ignore
            else:
                新建的要素数据集名称 = 要素集名称
        else:
            新建的要素数据集名称 = arcpy.management.CreateFeatureDataset(out_dataset_path=数据库路径, out_name=要素集名称, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]  # type: ignore
        return 新建的要素数据集名称

    @staticmethod
    def 删除(要素数据集名称):
        return arcpy.management.Delete(in_data=[要素数据集名称], data_type="")[0]  # type: ignore

    @staticmethod
    def 转换_从CAD(CAD路径列表, 输出要素数据集名称):
        from bxarcpy.环境包 import 环境类

        日志生成器.输出调试(f"CAD路径列表：{CAD路径列表}")
        日志生成器.输出调试(f"配置.当前工作空间：{环境类.属性获取_当前工作空间()}")
        日志生成器.输出调试(f"输出要素数据集名称：{输出要素数据集名称}")
        arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD路径列表, out_gdb_path=环境类.属性获取_当前工作空间(), out_dataset_name=输出要素数据集名称, reference_scale=1000, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]  # type: ignore
        return 输出要素数据集名称
