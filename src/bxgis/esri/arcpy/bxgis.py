# -*- coding: utf-8 -*-
r""""""
__all__ = ['BaseperiodFieldsTranslateAndGenerateSubitems',
           'BaseperiodLandtypeConversion', 'ConvertCurveToPolyline',
           'ExportToCAD', 'GenerationOfLandusePlanning', 'ImportFromCAD']
__alias__ = 'BXGIS工具箱'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# 常用 toolset
@gptooldoc('ConvertCurveToPolyline_BXGIS工具箱', None)
def ConvertCurveToPolyline(parameter_1=None):
    """ConvertCurveToPolyline(parameter_1;parameter_1...)

     INPUTS:
      输入要素名称列表 (要素类):
          输入要素名称列表"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ConvertCurveToPolyline_BXGIS工具箱(*gp_fixargs((parameter_1,), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('ExportToCAD_BXGIS工具箱', None)
def ExportToCAD(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None):
    """ExportToCAD(parameter_1, {parameter_2}, {parameter_3}, {parameter_4;parameter_4...}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9;parameter_9...}, {parameter_10}, {parameter_11})

     INPUTS:
      输入要素 (要素类):
          输入要素
      范围要素 {要素类}:
          范围要素
      是否对要素进行融合 {布尔}:
          是否对要素进行融合
      需融合地类编号列表 {字符串}:
          需融合地类编号列表
      是否对要素进行切分 {布尔}:
          是否对要素进行切分
      切分时折点数量阈值 {长整型}:
          切分时折点数量阈值
      切分时孔洞数量阈值 {长整型}:
          切分时孔洞数量阈值
      切分时面积阈值 {双精度型}:
          切分时面积阈值
      切分时地类编号限制列表 {字符串}:
          切分时地类编号限制列表
      是否去孔 {布尔}:
          是否去孔

     OUTPUTS:
      输出CAD路径 {CAD 工程图数据集}:
          输出CAD路径"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExportToCAD_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('ImportFromCAD_BXGIS工具箱', None)
def ImportFromCAD(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None):
    """ImportFromCAD(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6})

     INPUTS:
      输入CAD路径 (CAD 工程图数据集):
          输入CAD路径
      输入CAD图层名称 {字符串}:
          输入CAD图层名称
      是否拓扑检查 {布尔}:
          是否拓扑检查
      是否范围检查 {布尔}:
          是否范围检查
      是否转曲 {布尔}:
          是否转曲

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ImportFromCAD_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6), True)))
        return retval
    except Exception as e:
        raise e


# 用地 toolset
@gptooldoc('GenerationOfLandusePlanning_BXGIS工具箱', None)
def GenerationOfLandusePlanning(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None):
    """GenerationOfLandusePlanning(parameter_1;parameter_1..., {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9})

     INPUTS:
      输入要素名称列表 (要素类):
          输入要素名称列表
      CAD导出色块要素名称 {要素类}:
          CAD导出色块要素名称
      对CAD导出色块进行调整要素名称 {要素类}:
          对CAD导出色块进行调整要素名称
      SQL_CAD导出色块中未填色区域地类 {字符串}:
          SQL_CAD导出色块中未填色区域地类
      SQL_CAD导出色块中保留的地类 {字符串}:
          SQL_CAD导出色块中保留的地类
      范围要素 {要素类}:
          范围要素
      是否拓扑检查 {布尔}:
          是否拓扑检查
      是否范围检查 {布尔}:
          是否范围检查

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.GenerationOfLandusePlanning_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9), True)))
        return retval
    except Exception as e:
        raise e


# 用地\基期 toolset
@gptooldoc('BaseperiodFieldsTranslateAndGenerateSubitems_BXGIS工具箱', None)
def BaseperiodFieldsTranslateAndGenerateSubitems(parameter_1=None, parameter_2=None):
    """BaseperiodFieldsTranslateAndGenerateSubitems(parameter_1, {parameter_2})

     INPUTS:
      输入要素名称 (要素类):
          输入要素名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.BaseperiodFieldsTranslateAndGenerateSubitems_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('BaseperiodLandtypeConversion_BXGIS工具箱', None)
def BaseperiodLandtypeConversion(parameter_1=None, parameter_2=None):
    """BaseperiodLandtypeConversion(parameter_1, {parameter_2})

     INPUTS:
      输入要素名称 (要素类):
          输入要素名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.BaseperiodLandtypeConversion_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2), True)))
        return retval
    except Exception as e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject