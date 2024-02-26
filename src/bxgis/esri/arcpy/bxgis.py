# -*- coding: utf-8 -*-
r""""""
__all__ = ['BaseperiodFieldsTranslateAndGenerateSubitems',
           'BaseperiodLandtypeConversion', 'ConvertCurveToPolyline',
           'DbCreateControlline', 'DbCreateControllineOfVillage',
           'DbCreateFacilities', 'DbCreateLanduseOfPlanned', 'DbCreateRegion',
           'DbCreateRegionOfIndustrial', 'DbCreateRegionOfUnit',
           'DbCreateZoneuse', 'ExportToCAD', 'ImportFromCAD',
           'LanduseCheckIsFarmlandOccupied', 'LanduseOfCurrentGeneration',
           'LanduseOfPlannedGeneration', 'LanduseUpdate', 'RegionUpdate',
           'RiverEdgeGeneration', 'RoadEdgeGeneration',
           'ZoneuseOfPlannedGeneration']
__alias__ = 'BXGIS工具箱'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# 入库 toolset
@gptooldoc('DbCreateControlline_BXGIS工具箱', None)
def DbCreateControlline(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None, parameter_12=None, parameter_13=None, parameter_14=None, parameter_15=None, parameter_16=None, parameter_17=None, parameter_18=None, parameter_19=None, parameter_20=None, parameter_21=None, parameter_22=None, parameter_23=None, parameter_24=None, parameter_25=None, parameter_26=None, parameter_27=None):
    """DbCreateControlline({parameter_1}, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10}, {parameter_11}, {parameter_12}, {parameter_13}, {parameter_14}, {parameter_15}, {parameter_16}, {parameter_17}, {parameter_18}, {parameter_19}, {parameter_20}, {parameter_21}, {parameter_22}, {parameter_23}, {parameter_24}, {parameter_25}, {parameter_26}, {parameter_27})

     INPUTS:
      单元名称 {字符串}:
          单元名称
      批复时间 {字符串}:
          批复时间
      批复文号 {字符串}:
          批复文号
      道路中线要素名称 {要素类}:
          道路中线要素名称
      道路边线要素名称 {要素类}:
          道路边线要素名称
      高架桥要素名称 {要素类}:
          高架桥要素名称
      隧道要素名称 {要素类}:
          隧道要素名称
      河道边线要素名称 {要素类}:
          河道边线要素名称
      河道中线要素名称 {要素类}:
          河道中线要素名称
      地块要素名称 {要素类}:
          地块要素名称
      铁路线要素名称 {要素类}:
          铁路线要素名称
      输油管要素名称 {要素类}:
          输油管要素名称
      原水输水要素名称 {要素类}:
          原水输水要素名称
      高压线要素名称 {要素类}:
          高压线要素名称
      天然气要素名称 {要素类}:
          天然气要素名称
      综合管廊要素名称 {要素类}:
          综合管廊要素名称
      市政管线要素名称 {要素类}:
          市政管线要素名称
      微波通道要素名称 {要素类}:
          微波通道要素名称
      高度分区要素名称 {要素类}:
          高度分区要素名称
      共用通道要素名称 {要素类}:
          共用通道要素名称
      远景道路要素名称 {要素类}:
          远景道路要素名称
      虚位控制河道要素名称 {要素类}:
          虚位控制河道要素名称
      虚位控制道路要素名称 {要素类}:
          虚位控制道路要素名称
      绿化控制线要素名称 {要素类}:
          绿化控制线要素名称
      景观廊道要素名称 {要素类}:
          景观廊道要素名称
      其他要素名称 {要素类}:
          其他要素名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateControlline_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11, parameter_12, parameter_13, parameter_14, parameter_15, parameter_16, parameter_17, parameter_18, parameter_19, parameter_20, parameter_21, parameter_22, parameter_23, parameter_24, parameter_25, parameter_26, parameter_27), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateControllineOfVillage_BXGIS工具箱', None)
def DbCreateControllineOfVillage(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None):
    """DbCreateControllineOfVillage(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6})

     INPUTS:
      村庄建设边界要素名称 (要素类):
          村庄建设边界要素名称
      单元名称 {字符串}:
          单元名称
      批复时间 {字符串}:
          批复时间
      批复文号 {字符串}:
          批复文号
      单元编号 {字符串}:
          单元编号

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateControllineOfVillage_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateFacilities_BXGIS工具箱', None)
def DbCreateFacilities(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None, parameter_12=None):
    """DbCreateFacilities({parameter_1}, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10}, {parameter_11}, {parameter_12})

     INPUTS:
      单元名称 {字符串}:
          单元名称
      批复时间 {字符串}:
          批复时间
      批复文号 {字符串}:
          批复文号
      类型代码字段名称 {字符串}:
          类型代码字段名称
      设施代码字段名称 {字符串}:
          设施代码字段名称
      设施名称字段名称 {字符串}:
          设施名称字段名称
      设施级别字段名称 {字符串}:
          设施级别字段名称
      设施所在地块编号字段名称 {字符串}:
          设施所在地块编号字段名称
      位置精确度字段名称 {字符串}:
          位置精确度字段名称
      远期预留字段名称 {字符串}:
          远期预留字段名称
      备注说明字段名称 {字符串}:
          备注说明字段名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateFacilities_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11, parameter_12), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateLanduseOfPlanned_BXGIS工具箱', None)
def DbCreateLanduseOfPlanned(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None):
    """DbCreateLanduseOfPlanned(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10})

     INPUTS:
      地块要素名称 (要素类):
          地块要素名称
      单元名称 {字符串}:
          单元名称
      批复时间 {字符串}:
          批复时间
      批复文号 {字符串}:
          批复文号
      地块编号字段名称 {字符串}:
          地块编号字段名称
      地类编号字段名称 {字符串}:
          地类编号字段名称
      性质名称字段名称 {字符串}:
          性质名称字段名称
      地块性质别称字段名称 {字符串}:
          地块性质别称字段名称
      兼容比例字段名称 {字符串}:
          兼容比例字段名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateLanduseOfPlanned_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateRegion_BXGIS工具箱', None)
def DbCreateRegion(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None, parameter_12=None, parameter_13=None, parameter_14=None, parameter_15=None, parameter_16=None, parameter_17=None, parameter_18=None, parameter_19=None):
    """DbCreateRegion(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10}, {parameter_11}, {parameter_12}, {parameter_13}, {parameter_14}, {parameter_15}, {parameter_16}, {parameter_17}, {parameter_18}, {parameter_19})

     INPUTS:
      区域要素名称 (要素类):
          区域要素名称
      单元名称 {字符串}:
          单元名称
      层级 {字符串}:
          层级
      区域编号字段名称 {字符串}:
          区域编号字段名称
      区域主导属性字段名称 {字符串}:
          区域主导属性字段名称
      总城镇居住人数字段名称 {字符串}:
          总城镇居住人数字段名称
      总建筑面积字段名称 {字符串}:
          总建筑面积字段名称
      总住宅建筑面积字段名称 {字符串}:
          总住宅建筑面积字段名称
      总工业建筑面积字段名称 {字符串}:
          总工业建筑面积字段名称
      总商服建筑面积字段名称 {字符串}:
          总商服建筑面积字段名称
      总村庄户籍人数字段名称 {字符串}:
          总村庄户籍人数字段名称
      总村庄居住人数字段名称 {字符串}:
          总村庄居住人数字段名称
      总耕地用地面积字段名称 {字符串}:
          总耕地用地面积字段名称
      总永久基本农田用地面积字段名称 {字符串}:
          总永久基本农田用地面积字段名称
      总生态保护红线用地面积字段名称 {字符串}:
          总生态保护红线用地面积字段名称
      总村庄建设边界用地面积字段名称 {字符串}:
          总村庄建设边界用地面积字段名称
      总城乡建设用地面积字段名称 {字符串}:
          总城乡建设用地面积字段名称
      总村庄建设用地面积字段名称 {字符串}:
          总村庄建设用地面积字段名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateRegion_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11, parameter_12, parameter_13, parameter_14, parameter_15, parameter_16, parameter_17, parameter_18, parameter_19), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateRegionOfIndustrial_BXGIS工具箱', None)
def DbCreateRegionOfIndustrial(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None):
    """DbCreateRegionOfIndustrial(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10}, {parameter_11})

     INPUTS:
      工业片区要素名称 (要素类):
          工业片区要素名称
      单元名称 {字符串}:
          单元名称
      区域编号 {字符串}:
          区域编号
      区域名称 {字符串}:
          区域名称
      总工业用地面积 {字符串}:
          总工业用地面积
      总工业建筑面积 {字符串}:
          总工业建筑面积
      区域主导属性 {字符串}:
          区域主导属性
      配套设施汇总 {字符串}:
          配套设施汇总
      交通设施汇总 {字符串}:
          交通设施汇总
      市政设施汇总 {字符串}:
          市政设施汇总

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateRegionOfIndustrial_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateRegionOfUnit_BXGIS工具箱', None)
def DbCreateRegionOfUnit(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None):
    """DbCreateRegionOfUnit(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10}, {parameter_11})

     INPUTS:
      规划范围线要素名称 (要素类):
          规划范围线要素名称
      单元编号 {字符串}:
          单元编号
      单元名称 {字符串}:
          单元名称
      单元类型 {字符串}:
          单元类型
      批复时间 {字符串}:
          批复时间
      批复文号 {字符串}:
          批复文号
      编制单位 {字符串}:
          编制单位
      单元功能 {字符串}:
          单元功能
      人口规模 {字符串}:
          人口规模
      跨单元平衡情况 {字符串}:
          跨单元平衡情况

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateRegionOfUnit_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateZoneuse_BXGIS工具箱', None)
def DbCreateZoneuse(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None):
    """DbCreateZoneuse({parameter_1}, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8})

     INPUTS:
      分区要素名称 {要素类}:
          分区要素名称
      单元名称 {字符串}:
          单元名称
      批复时间 {字符串}:
          批复时间
      批复文号 {字符串}:
          批复文号
      单元编号 {字符串}:
          单元编号
      分区名称字段名称 {字符串}:
          分区名称字段名称
      分区编号字段名称 {字符串}:
          分区编号字段名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateZoneuse_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8), True)))
        return retval
    except Exception as e:
        raise e


# 分区 toolset
@gptooldoc('ZoneuseOfPlannedGeneration_BXGIS工具箱', None)
def ZoneuseOfPlannedGeneration(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None):
    """ZoneuseOfPlannedGeneration(parameter_1, parameter_2, {parameter_3;parameter_3...}, parameter_4, parameter_5, parameter_6, {parameter_7}, {parameter_8;parameter_8...}, {parameter_9})

     INPUTS:
      规划用地要素名称 (要素类):
          规划用地要素名称
      现状用地要素名称 (要素类):
          现状用地要素名称
      农田整备要素名称列表 {要素类}:
          农田整备要素名称列表
      城镇集建区要素名称 (要素类):
          城镇集建区要素名称
      城镇弹性区要素名称 (要素类):
          城镇弹性区要素名称
      永久基本农田要素名称 (要素类):
          永久基本农田要素名称
      城镇开发边界外集建区修改要素名称 {要素类}:
          城镇开发边界外集建区修改要素名称
      其他需要叠合的要素名称列表 {要素类}:
          其他需要叠合的要素名称列表

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ZoneuseOfPlannedGeneration_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9), True)))
        return retval
    except Exception as e:
        raise e


# 区域 toolset
@gptooldoc('RegionUpdate_BXGIS工具箱', None)
def RegionUpdate(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None):
    """RegionUpdate(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, parameter_5, parameter_6, parameter_7, parameter_8, {parameter_9}, {parameter_10})

     INPUTS:
      区域要素名称 (要素类):
          区域要素名称
      用地要素名称 {要素类}:
          用地要素名称
      用地要素中所属区域字段名称 {字符串}:
          用地要素中所属区域字段名称
      区域要素中编号字段名称 {字符串}:
          区域要素中编号字段名称
      永久基本农田要素名称 (要素类):
          永久基本农田要素名称
      生态保护红线要素名称 (要素类):
          生态保护红线要素名称
      村庄建设边界要素名称 (要素类):
          村庄建设边界要素名称
      设施要素名称 (要素类):
          设施要素名称
      设施要素中所属区域字段名称 {字符串}:
          设施要素中所属区域字段名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RegionUpdate_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10), True)))
        return retval
    except Exception as e:
        raise e


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
def ExportToCAD(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None, parameter_12=None):
    """ExportToCAD(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5;parameter_5...}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9}, {parameter_10;parameter_10...}, {parameter_11}, {parameter_12})

     INPUTS:
      输入要素 (要素类):
          输入要素
      是否将要素按范围裁剪 {布尔}:
          是否将要素按范围裁剪
      规划范围线要素名称 {要素类}:
          规划范围线要素名称
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
        retval = convertArcObjectToPythonObject(gp.ExportToCAD_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11, parameter_12), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('ImportFromCAD_BXGIS工具箱', None)
def ImportFromCAD(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None):
    """ImportFromCAD(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5})

     INPUTS:
      输入CAD数据集中的要素类 (要素类):
          输入CAD数据集中的要素类
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
        retval = convertArcObjectToPythonObject(gp.ImportFromCAD_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5), True)))
        return retval
    except Exception as e:
        raise e


# 用地 toolset
@gptooldoc('LanduseOfCurrentGeneration_BXGIS工具箱', None)
def LanduseOfCurrentGeneration(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None):
    """LanduseOfCurrentGeneration(parameter_1;parameter_1..., {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5})

     INPUTS:
      输入要素名称列表 (要素类):
          输入要素名称列表
      规划范围线要素名称 {要素类}:
          规划范围线要素名称
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
        retval = convertArcObjectToPythonObject(gp.LanduseOfCurrentGeneration_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('LanduseOfPlannedGeneration_BXGIS工具箱', None)
def LanduseOfPlannedGeneration(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None, parameter_10=None, parameter_11=None, parameter_12=None, parameter_13=None):
    """LanduseOfPlannedGeneration(parameter_1;parameter_1..., {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7;parameter_7...}, {parameter_8}, {parameter_9}, {parameter_10}, {parameter_11}, {parameter_12}, {parameter_13})

     INPUTS:
      输入要素名称列表 (要素类):
          输入要素名称列表
      规划范围线要素名称 {要素类}:
          规划范围线要素名称
      是否将CAD合并入GIS {布尔}:
          是否将CAD合并入GIS
      CAD导出色块要素名称 {要素类}:
          CAD导出色块要素名称
      CAD导出色块以外地类调整要素名称 {要素类}:
          CAD导出色块以外地类调整要素名称
      CAD导出色块中空隙的地类 {字符串}:
          CAD导出色块中空隙的地类
      CAD导出色块中有效的地类列表 {字符串}:
          CAD导出色块中有效的地类列表
      是否处理细小面 {布尔}:
          是否处理细小面
      GIS中已处理的细小面要素名称 {要素类}:
          GIS中已处理的细小面要素名称
      细小面面积阈值 {字符串}:
          细小面面积阈值
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
        retval = convertArcObjectToPythonObject(gp.LanduseOfPlannedGeneration_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9, parameter_10, parameter_11, parameter_12, parameter_13), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('LanduseUpdate_BXGIS工具箱', None)
def LanduseUpdate(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None, parameter_5=None, parameter_6=None, parameter_7=None, parameter_8=None, parameter_9=None):
    """LanduseUpdate(parameter_1, {parameter_2}, {parameter_3}, {parameter_4}, {parameter_5}, {parameter_6}, {parameter_7}, {parameter_8}, {parameter_9})

     INPUTS:
      输入要素名称 (要素类):
          输入要素名称
      街坊范围线要素名称 {要素类}:
          街坊范围线要素名称
      分村范围线要素名称 {要素类}:
          分村范围线要素名称
      城镇集建区要素名称 {要素类}:
          城镇集建区要素名称
      城镇弹性区要素名称 {要素类}:
          城镇弹性区要素名称
      有扣除地类系数的要素名称 {要素类}:
          有扣除地类系数的要素名称
      有坐落单位信息的要素名称 {要素类}:
          有坐落单位信息的要素名称
      设施要素名称 {要素类}:
          设施要素名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LanduseUpdate_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4, parameter_5, parameter_6, parameter_7, parameter_8, parameter_9), True)))
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


# 用地\检查 toolset
@gptooldoc('LanduseCheckIsFarmlandOccupied_BXGIS工具箱', None)
def LanduseCheckIsFarmlandOccupied(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None):
    """LanduseCheckIsFarmlandOccupied(parameter_1, {parameter_2}, {parameter_3}, {parameter_4})

     INPUTS:
      输入要素名称 (要素类):
          输入要素名称
      基本农田要素名称 {要素类}:
          基本农田要素名称
      是否输出到CAD {布尔}:
          是否输出到CAD

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LanduseCheckIsFarmlandOccupied_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4), True)))
        return retval
    except Exception as e:
        raise e


# 道路 toolset
@gptooldoc('RiverEdgeGeneration_BXGIS工具箱', None)
def RiverEdgeGeneration(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None):
    """RiverEdgeGeneration(parameter_1, {parameter_2}, {parameter_3}, {parameter_4})

     INPUTS:
      河道中线要素名称 (要素类):
          河道中线要素名称
      用地要素名称 {要素类}:
          用地要素名称
      规划范围线要素名称 {要素类}:
          规划范围线要素名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RiverEdgeGeneration_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('RoadEdgeGeneration_BXGIS工具箱', None)
def RoadEdgeGeneration(parameter_1=None, parameter_2=None, parameter_3=None, parameter_4=None):
    """RoadEdgeGeneration(parameter_1, {parameter_2}, {parameter_3}, {parameter_4})

     INPUTS:
      道路中线要素名称 (要素类):
          道路中线要素名称
      用地要素名称 {要素类}:
          用地要素名称
      规划范围线要素名称 {要素类}:
          规划范围线要素名称

     OUTPUTS:
      输出要素名称 {要素类}:
          输出要素名称"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RoadEdgeGeneration_BXGIS工具箱(*gp_fixargs((parameter_1, parameter_2, parameter_3, parameter_4), True)))
        return retval
    except Exception as e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject