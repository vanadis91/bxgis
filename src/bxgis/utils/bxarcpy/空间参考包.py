import arcpy


class 空间参考类:
    @staticmethod
    def 属性获取_名称(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.name

    @staticmethod
    def 属性获取_类型(坐标系对象: arcpy.SpatialReference):
        if 坐标系对象.type == "Geographic":
            return "地理坐标系"
        elif 坐标系对象.type == "Projected":
            return "投影坐标系"
        elif 坐标系对象.type == "Geocentric":
            return "地理entric坐标系"
        elif 坐标系对象.type == "UserDefined":
            return "用户定义坐标系"

    @staticmethod
    def 属性获取_工厂代码(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.factoryCode

    @staticmethod
    def 属性获取_线性单位名称(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.linearUnitName

    @staticmethod
    def 属性获取_角度单位名称(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.angularUnitName

    @staticmethod
    def 属性获取_中央子午线(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.centralMeridian

    @staticmethod
    def 属性获取_东偏移量(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.falseEasting

    @staticmethod
    def 属性获取_北偏移量(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.falseNorthing

    @staticmethod
    def 属性获取_原点纬度(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.latitudeOfOrigin

    @staticmethod
    def 属性获取_比例因子(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.scaleFactor

    @staticmethod
    def 转换_到字符串格式(坐标系对象: arcpy.SpatialReference):
        return 坐标系对象.exportToString()

    @staticmethod
    def 转换_从字符串格式(字符串格式坐标系):
        sr = arcpy.SpatialReference()
        sr.loadFromString(字符串格式坐标系)
        return sr  # type: ignore

    @staticmethod
    def 转换_从工厂代码(工厂代码):
        return arcpy.SpatialReference(工厂代码)  # type: ignore
