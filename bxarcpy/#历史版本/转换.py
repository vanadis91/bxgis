import arcpy


def GEO导出到CAD(输入要素列表=None, 输出路径=None):
    return arcpy.conversion.ExportCAD(in_features=输入要素列表, Output_Type="DWG_R2010", Output_File=输出路径, Ignore_FileNames="Ignore_Filenames_in_Tables", Append_To_Existing="Overwrite_Existing_Files", Seed_File="")


def 要素导出到要素(输入要素=None, 输出路径=None, 输出文件名=None):
    return arcpy.conversion.FeatureClassToFeatureClass(in_features=输入要素, out_path=输出路径, out_name=输出文件名, where_clause="", field_mapping="", config_keyword="")[0]


def CAD导入到GEO(CAD路径列表=None, 输出数据库=None, 输出要素集名称=None):
    return arcpy.conversion.CADToGeodatabase(input_cad_datasets=CAD路径列表, out_gdb_path=输出数据库, out_dataset_name=输出要素集名称, reference_scale=1000, spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision')[0]
