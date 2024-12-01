import arcpy


class 几何类:
    # def __init__(self, 内嵌对象) -> None:
    #     # print(f"形状类：{内嵌对象.__class__}")
    #     self._内嵌对象 = 内嵌对象
    @staticmethod
    def 属性获取_类型(几何对象):
        from bxarcpy.基本对象包 import 枚举类

        类型 = 几何对象.type  # type: ignore
        return 枚举类.要素类型.名称获取(类型.upper())

    @staticmethod
    def 属性获取_折点列表(几何对象):
        return 几何对象.getPart()  # type: ignore

    @staticmethod
    def 属性获取_坐标列表(几何对象):
        多部件temp = []
        for 点表 in 几何对象.getPart():
            点表temp = []
            for 点 in 点表:
                点表temp.append([点.X, 点.Y])
            多部件temp.append(点表temp)
        return 多部件temp  # type: ignore

    @staticmethod
    def 集合_交集(几何对象1, 几何对象2, 类型="面"):
        _交集类型映射表 = {4: 4, "面": 4, 2: 2, "线": 2, 1: 1, "点": 1}
        ret = 几何对象1.intersect(几何对象2, _交集类型映射表[类型])  # type: ignore
        return ret

    @staticmethod
    def 集合_差集(几何对象1, 几何对象2):
        ret = 几何对象1.difference(几何对象2)  # type: ignore
        return ret

    @staticmethod
    def 集合_并集(几何对象1, 几何对象2):
        ret = 几何对象1.union(几何对象2)  # type: ignore
        return ret

    @staticmethod
    def 关系_包含(几何对象1, 几何对象2):
        # from bxshapely.通用对象包 import _点线面通用类

        ret = 几何对象1.contains(几何对象2)
        # 几何对象1 = 几何类.转换_到shapely几何对象(几何对象1)
        # 几何对象2 = 几何类.转换_到shapely几何对象(几何对象2)
        # ret = _点线面通用类.关系_包含_前者边界和内部包含后者(几何对象1, 几何对象2)
        return ret  # type: ignore

    @staticmethod
    def 关系_被包含(几何对象1, 几何对象2):
        # from bxshapely.通用对象包 import _点线面通用类

        ret = 几何对象1.within(几何对象2)
        # 几何对象1 = 几何类.转换_到shapely几何对象(几何对象1)
        # 几何对象2 = 几何类.转换_到shapely几何对象(几何对象2)
        # ret = _点线面通用类.关系_内部_前者边界和内部均位于后者内部(几何对象1, 几何对象2)
        return ret  # type: ignore

    @staticmethod
    def 关系_相离(几何对象1, 几何对象2):
        # from bxshapely.通用对象包 import _点线面通用类

        ret = 几何对象1.disjoint(几何对象2)
        # 几何对象1 = 几何类.转换_到shapely几何对象(几何对象1)
        # 几何对象2 = 几何类.转换_到shapely几何对象(几何对象2)
        # ret = _点线面通用类.关系_相离(几何对象1, 几何对象2)
        return ret  # type: ignore

    @staticmethod
    def 关系_相接(几何对象1, 几何对象2):
        # from bxshapely.通用对象包 import _点线面通用类

        ret = 几何对象1.touches(几何对象2)
        # 几何对象1 = 几何类.转换_到shapely几何对象(几何对象1)
        # 几何对象2 = 几何类.转换_到shapely几何对象(几何对象2)
        # ret = _点线面通用类.关系_接触_仅边界(几何对象1, 几何对象2)
        return ret  # type: ignore

    @staticmethod
    def 关系_交叉(几何对象1, 几何对象2):
        return 几何对象1.crosses(几何对象2)  # type: ignore

    @staticmethod
    def 关系_相交(几何对象1, 几何对象2):
        # from bxshapely.通用对象包 import _点线面通用类

        ret = 几何对象1.overlaps(几何对象2)
        # 几何对象1 = 几何类.转换_到shapely几何对象(几何对象1)
        # 几何对象2 = 几何类.转换_到shapely几何对象(几何对象2)
        # ret = _点线面通用类.关系_相交_前者边界和内部与后者(几何对象1, 几何对象2)
        return ret  # type: ignore

    @staticmethod
    def 关系_完全重叠(几何对象1, 几何对象2):
        # from bxshapely.通用对象包 import _点线面通用类

        ret = 几何对象1.equals(几何对象2)
        # 几何对象1 = 几何类.转换_到shapely几何对象(几何对象1)
        # 几何对象2 = 几何类.转换_到shapely几何对象(几何对象2)
        # ret = _点线面通用类.关系_重叠(几何对象1, 几何对象2)
        return ret  # type: ignore

    # @staticmethod
    # def 关系_重叠(几何对象1, 几何对象2):
    #     return 几何对象1.overlaps(几何对象2)  # type: ignore

    @staticmethod
    def 缓冲(几何对象, 距离):
        return 几何对象.buffer(距离)  # type: ignore

    @staticmethod
    def 最短距离(几何对象1, 几何对象2):
        return 几何对象1.distanceTo(几何对象2)  # type: ignore

    # def 转线(self, 输出要素名称):
    #     arcpy.PolygonToLine_management(self._内嵌对象, neighbor_option="IGNORE_NEIGHBORS")

    @staticmethod
    def 属性获取_内点(几何对象):
        return 几何对象.labelPoint  # type: ignore

    @staticmethod
    def 属性获取_质点(几何对象):
        return 几何对象.centroid  # type: ignore

    @staticmethod
    def 属性获取_凸包(几何对象):
        return 几何对象.convexHull  # type: ignore

    @staticmethod
    def 属性获取_部件数量(几何对象):
        return 几何对象.partCount  # type: ignore

    @staticmethod
    def 属性获取_折点数量(几何对象):
        return 几何对象.pointCount  # type: ignore

    @staticmethod
    def 属性获取_面积(几何对象):
        return 几何对象.area  # type: ignore

    @staticmethod
    def 属性获取_边界(几何对象):
        return 几何对象.boundary()  # type: ignore

    @staticmethod
    def 是否具有孔洞(几何对象):
        return 几何对象.hasOmittedBoundary  # type: ignore

    @staticmethod
    def 是否为多部件要素(几何对象):
        return 几何对象.isMultipart  # type: ignore

    @staticmethod
    def 是否包含曲线(几何对象):
        ret = [x for x in 几何类.转换_到json(几何对象).keys() if "curve" in x]
        if len(ret) > 0:
            return True
        return False

    @staticmethod
    def 属性获取_孔洞数量(几何对象):
        折点和孔洞数量总数 = 0
        for 每个部件x in 几何类.属性获取_折点列表(几何对象):  # type: ignore
            折点和孔洞数量 = len(每个部件x)
            折点和孔洞数量总数 += 折点和孔洞数量
        return 折点和孔洞数量总数 - 几何类.属性获取_折点数量(几何对象)  # type: ignore

    @staticmethod
    def 转换_到shapely几何对象(几何对象):
        wkt格式数据 = 几何类.转换_到wkt(几何对象)
        from bxshapely.工具包 import 转换工具

        return 转换工具.wkt字符串转几何对象(wkt格式数据)

    @staticmethod
    def 转换_从wkt(wkt字符串):
        return arcpy.FromWKT(wkt字符串)

    @staticmethod
    def 转换_到wkt(几何对象):
        return 几何对象.WKT  # type: ignore

    @staticmethod
    def 转换_到json(几何对象):
        import json

        return json.loads(几何对象.JSON)  # type: ignore

    # @property
    # def 孔洞数量(self):
    #     return self._内嵌对象.interiorRingCount()

    # def 边界部件获取(self, 索引):
    #     return self._内嵌对象[索引]

    # def 边界组成数量(self):
    #     return self._内嵌对象.getPartCount()


class 点类:
    # def __init__(self, 内嵌对象) -> None:
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 点创建(X, Y, Z=None, M=None, ID=None):
        return arcpy.Point(X, Y, Z, M, ID)

    @staticmethod
    def 属性获取_x坐标(点对象):
        return 点对象.X  # type: ignore

    @staticmethod
    def 属性获取_y坐标(点对象):
        return 点对象.Y  # type: ignore


class 线类:
    # def __init__(self, 内嵌对象):
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 线创建(arcpy数组对象):
        return arcpy.Polyline(arcpy数组对象)
