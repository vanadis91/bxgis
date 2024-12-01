# -*- coding: utf-8 -*-
r""""""
__all__ = ['ExportToCAD', 'ImportFromCAD']
__alias__ = 'BXGIS工具箱'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# 常用 toolset
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


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject