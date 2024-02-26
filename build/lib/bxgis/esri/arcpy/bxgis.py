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
def DbCreateControlline():
    """DbCreateControlline()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateControlline_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateControllineOfVillage_BXGIS工具箱', None)
def DbCreateControllineOfVillage():
    """DbCreateControllineOfVillage()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateControllineOfVillage_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateFacilities_BXGIS工具箱', None)
def DbCreateFacilities():
    """DbCreateFacilities()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateFacilities_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateLanduseOfPlanned_BXGIS工具箱', None)
def DbCreateLanduseOfPlanned():
    """DbCreateLanduseOfPlanned()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateLanduseOfPlanned_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateRegion_BXGIS工具箱', None)
def DbCreateRegion():
    """DbCreateRegion()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateRegion_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateRegionOfIndustrial_BXGIS工具箱', None)
def DbCreateRegionOfIndustrial():
    """DbCreateRegionOfIndustrial()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateRegionOfIndustrial_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateRegionOfUnit_BXGIS工具箱', None)
def DbCreateRegionOfUnit():
    """DbCreateRegionOfUnit()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateRegionOfUnit_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('DbCreateZoneuse_BXGIS工具箱', None)
def DbCreateZoneuse():
    """DbCreateZoneuse()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.DbCreateZoneuse_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 分区 toolset
@gptooldoc('ZoneuseOfPlannedGeneration_BXGIS工具箱', None)
def ZoneuseOfPlannedGeneration():
    """ZoneuseOfPlannedGeneration()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ZoneuseOfPlannedGeneration_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 区域 toolset
@gptooldoc('RegionUpdate_BXGIS工具箱', None)
def RegionUpdate():
    """RegionUpdate()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RegionUpdate_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 常用 toolset
@gptooldoc('ConvertCurveToPolyline_BXGIS工具箱', None)
def ConvertCurveToPolyline():
    """ConvertCurveToPolyline()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ConvertCurveToPolyline_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('ExportToCAD_BXGIS工具箱', None)
def ExportToCAD():
    """ExportToCAD()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ExportToCAD_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('ImportFromCAD_BXGIS工具箱', None)
def ImportFromCAD():
    """ImportFromCAD()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ImportFromCAD_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 用地 toolset
@gptooldoc('LanduseOfCurrentGeneration_BXGIS工具箱', None)
def LanduseOfCurrentGeneration():
    """LanduseOfCurrentGeneration()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LanduseOfCurrentGeneration_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('LanduseOfPlannedGeneration_BXGIS工具箱', None)
def LanduseOfPlannedGeneration():
    """LanduseOfPlannedGeneration()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LanduseOfPlannedGeneration_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('LanduseUpdate_BXGIS工具箱', None)
def LanduseUpdate():
    """LanduseUpdate()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LanduseUpdate_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 用地\基期 toolset
@gptooldoc('BaseperiodFieldsTranslateAndGenerateSubitems_BXGIS工具箱', None)
def BaseperiodFieldsTranslateAndGenerateSubitems():
    """BaseperiodFieldsTranslateAndGenerateSubitems()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.BaseperiodFieldsTranslateAndGenerateSubitems_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('BaseperiodLandtypeConversion_BXGIS工具箱', None)
def BaseperiodLandtypeConversion():
    """BaseperiodLandtypeConversion()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.BaseperiodLandtypeConversion_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 用地\检查 toolset
@gptooldoc('LanduseCheckIsFarmlandOccupied_BXGIS工具箱', None)
def LanduseCheckIsFarmlandOccupied():
    """LanduseCheckIsFarmlandOccupied()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LanduseCheckIsFarmlandOccupied_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# 道路 toolset
@gptooldoc('RiverEdgeGeneration_BXGIS工具箱', None)
def RiverEdgeGeneration():
    """RiverEdgeGeneration()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RiverEdgeGeneration_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('RoadEdgeGeneration_BXGIS工具箱', None)
def RoadEdgeGeneration():
    """RoadEdgeGeneration()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RoadEdgeGeneration_BXGIS工具箱(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject