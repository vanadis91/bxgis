from .常量 import _要素类型反映射

try:
    import arcpy
except Exception as e:
    pass


class 几何对象类:
    def __init__(self, 内嵌对象) -> None:
        # print(f"形状类：{内嵌对象.__class__}")
        self._内嵌对象 = 内嵌对象

    def 类型获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)  # type: ignore
        类型 = 内嵌对象.type  # type: ignore
        return _要素类型反映射[类型.upper()] if 类型.upper() in _要素类型反映射 else 类型.upper()

    def 点表获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.getPart()  # type: ignore

    def json格式获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        import json

        return json.loads(内嵌对象.JSON)  # type: ignore

    def wkt格式获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.WKT  # type: ignore

    def 集合_交集(self, 几何对象, 类型="面"):
        _交集类型映射表 = {4: 4, "面": 4, 2: 2, "线": 2, 1: 1, "点": 1}
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        ret = 内嵌对象.intersect(几何对象, _交集类型映射表[类型])  # type: ignore
        return ret

    def 集合_差集(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        ret = 内嵌对象.difference(几何对象)  # type: ignore
        return ret

    def 集合_并集(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        ret = 内嵌对象.union(几何对象)  # type: ignore
        return ret

    def 关系_包含(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.contains(几何对象)  # type: ignore

    def 关系_被包含(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.within(几何对象)  # type: ignore

    def 关系_相离(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.disjoint(几何对象)  # type: ignore

    def 关系_相接(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.touches(几何对象)  # type: ignore

    def 关系_相交_但不包含或被包含(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.crosses(几何对象)  # type: ignore

    def 关系_相交(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.intersects(几何对象)  # type: ignore

    def 关系_重叠(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.overlaps(几何对象)  # type: ignore

    def 缓冲(self, 距离):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.buffer(距离)  # type: ignore

    def 最短距离(self, 几何对象):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.distanceTo(几何对象)  # type: ignore

    # def 转线(self, 输出要素名称):
    #     arcpy.PolygonToLine_management(self._内嵌对象, neighbor_option="IGNORE_NEIGHBORS")

    def 内点获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.labelPoint  # type: ignore

    def 质点获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.centroid  # type: ignore

    def 凸包获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.convexHull  # type: ignore

    def 部件数量获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.partCount  # type: ignore

    def 折点数量获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.pointCount  # type: ignore

    def 面积获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.area  # type: ignore

    def 边界获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.boundary()  # type: ignore

    def 是否具有孔洞(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.hasOmittedBoundary  # type: ignore

    def 是否为多部件要素(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.isMultipart  # type: ignore

    def 是否包含曲线(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        ret = [x for x in 几何对象类.json格式获取(内嵌对象).keys() if "curve" in x]
        if len(ret) > 0:
            return True
        return False

    def 孔洞数量获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        折点和孔洞数量总数 = 0
        for 每个部件x in 内嵌对象.getPart():  # type: ignore
            折点和孔洞数量 = len(每个部件x)
            折点和孔洞数量总数 += 折点和孔洞数量
        return 折点和孔洞数量总数 - 内嵌对象.pointCount  # type: ignore

    def 转换_到shapely几何对象(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        wkt格式数据 = 几何对象类.wkt格式获取(内嵌对象)
        import bxgeo

        return bxgeo.转换.wkt字符串转图形(wkt格式数据)

    @staticmethod
    def 转换_从wkt(wkt字符串):
        return arcpy.FromWKT(wkt字符串)

    def 转换_到wkt(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if type(self) is 几何对象类 else (False, self)
        return 内嵌对象.WKT  # type: ignore

    # @property
    # def 孔洞数量(self):
    #     return self._内嵌对象.interiorRingCount()

    # def 边界部件获取(self, 索引):
    #     return self._内嵌对象[索引]

    # def 边界组成数量(self):
    #     return self._内嵌对象.getPartCount()


class 点:
    def __init__(self, 内嵌对象) -> None:
        if hasattr(内嵌对象, "_内嵌对象"):
            self._内嵌对象 = 内嵌对象._内嵌对象
        else:
            self._内嵌对象 = 内嵌对象

    @staticmethod
    def 点创建(X, Y, Z=None, M=None, ID=None):
        return 点(arcpy.Point(X, Y, Z, M, ID))

    def X坐标获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 内嵌对象.X  # type: ignore

    def Y坐标获取(self):
        self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 内嵌对象.Y  # type: ignore


class 线:
    def __init__(self, 内嵌对象):
        if hasattr(内嵌对象, "_内嵌对象"):
            self._内嵌对象 = 内嵌对象._内嵌对象
        else:
            self._内嵌对象 = 内嵌对象

    @staticmethod
    def 线创建(数组):
        return 线(arcpy.Polyline(数组))
