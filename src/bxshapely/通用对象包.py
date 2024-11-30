import shapely
from shapely.geometry import LineString, Point, Polygon
from shapely import wkb, wkt
from typing import Union, Literal


class _点线面通用类:
    # def __init__(self, 内嵌对象) -> None:
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象
    @staticmethod
    def 图形是否有效(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.is_valid  # type: ignore

    @staticmethod
    def 图形有效性字符串(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from shapely.validation import explain_validity

        return explain_validity(实例)

    @staticmethod
    def 图形是否为空(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from shapely.validation import explain_validity

        return 实例.is_empty  # type: ignore

    @staticmethod
    def 图形是否自相交(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.is_simple  # type: ignore

    @staticmethod
    def 图形是否有Z坐标(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.has_z  # type: ignore

    @staticmethod
    def 边界框获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.bounds  # type: ignore

    @staticmethod
    def 最小正矩形获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.envelope  # type: ignore

    @staticmethod
    def 最小矩形获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.minimum_rotated_rectangle  # type: ignore

    @staticmethod
    def 长度获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.length  # type: ignore

    @staticmethod
    def 凸包获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.convex_hull  # type: ignore

    @staticmethod
    def 几何类型获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.geom_type  # type: ignore

    @staticmethod
    def 面积获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        if _点线面通用类.几何类型获取(实例) != "LinearRing":
            return 实例.area  # type: ignore
        else:
            from bxshapely.面包 import 面类
            from bxshapely.线包 import 环类

            mian = 面类.面创建_通过点表(环类.折点获取(实例))  # type: ignore
            return 面类.面积获取(mian)

    @staticmethod
    def 缓冲(实例, 距离, 四分之一圆转折后段数=16, 端点样式="圆形", 交点样式="圆角"):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        _端点样式映射 = {"圆形": 1, "扁平": 2, "正方形": 3}
        端点样式raw = _端点样式映射[端点样式]
        _交点样式映射 = {"圆角": 1, "方角": 2, "倒角": 3}
        交点样式raw = _交点样式映射[交点样式]
        # 距离为0，可清除自接触或者自交多边形。
        # 四分之一圆转折后段数为1，缓冲区是一个矩形。
        return 实例.buffer(距离, resolution=四分之一圆转折后段数, cap_style=端点样式raw, join_style=交点样式raw)  # type: ignore

    @staticmethod
    def 简化(实例, 容差, 是否保持拓扑关系=True):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # 距离为0，可清除自接触或者自交多边形。
        # 四分之一圆转折后段数为1，缓冲区是一个矩形。
        return 实例.simplify(容差, preserve_topology=是否保持拓扑关系)  # type: ignore

    @staticmethod
    def 集合_交集(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.intersection(x2)  # type: ignore

    @staticmethod
    def 集合_并集(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # return shapely.ops.unary_union()(x1, x2)  # type: ignore
        # return shapely.ops.cascaded_union(x1, x2)  # type: ignore
        return 实例.union(x2)  # type: ignore

    @staticmethod
    def 集合_并集_级联(图形列表或图形集):
        return shapely.ops.unary_union(图形列表或图形集)  # type: ignore
        # return shapely.ops.cascaded_union(x1, x2)  # type: ignore
        # return x1.union(x2)

    @staticmethod
    def 集合_差集(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.difference(x2)  # type: ignore

    @staticmethod
    def 集合_补集(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.symmetric_difference(x2)  # type: ignore

    @staticmethod
    def wkt格式获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.wkt  # type: ignore

    @staticmethod
    def svg格式获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例._repr_svg_()  # type: ignore

    @staticmethod
    def wkb格式获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.wkb  # type: ignore

    @staticmethod
    def 关系_相离(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.disjoint(x2)  # type: ignore

    @staticmethod
    def 关系_接触_仅边界(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # 线与线上的点不相交
        return 实例.touches(x2)  # type: ignore

    @staticmethod
    def 关系_相交_前者边界和内部与后者(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # 线与线上的点不相交
        return 实例.intersects(x2)  # type: ignore

    @staticmethod
    def 关系_相交_前者内部与后者内部(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # 线与线上的点不相交
        return 实例.crosses(x2)  # type: ignore

    @staticmethod
    def 关系_包含_前者边界和内部包含后者(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.contains(x2)  # type: ignore

    @staticmethod
    def 关系_内部_前者边界和内部均位于后者内部(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # 线不包含线上的点
        return 实例.within(x2)  # type: ignore

    @staticmethod
    def 关系_重叠(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        # 线不包含线上的点
        return 实例.overlaps(x2)  # type: ignore

    @staticmethod
    def 关系_九交关系(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.relate(x2)  # type: ignore

    @staticmethod
    def 关系_是否符合指定九交关系(实例, x2, 九交关系字符串):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.relate_pattern(x2, 九交关系字符串)  # type: ignore

    @staticmethod
    def 两图形间最近点(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from shapely.ops import nearest_points

        p1, p2 = nearest_points(实例, x2)

        return p1, p2

    @staticmethod
    def 两图形间最短距离(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.distance(x2)  # type: ignore

    @staticmethod
    def 前者到后者最近点的最远距离(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.hausdorff_distance(x2)  # type: ignore

    @staticmethod
    def 两图形是否几乎相等(实例, x2, 小数点后位数=6):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.equals_exact(x2, decimal=小数点后位数)  # type: ignore

    @staticmethod
    def 两图形是否相等(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.equals(x2)  # type: ignore

    @staticmethod
    def 坐标获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .面包 import 面类

        if _点线面通用类.几何类型获取(实例) == "Polygon":
            外环坐标 = 面类.坐标获取_外环(实例)  # type: ignore
            内环列表坐标 = 面类.坐标获取_内环列表(实例)  # type: ignore
            return [外环坐标, *内环列表坐标]
        return list(实例.coords)  # type: ignore

    @staticmethod
    def 折点获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .面包 import 面类

        if _点线面通用类.几何类型获取(实例) == "Polygon":
            外环折点 = 面类.折点获取_外环(实例)  # type: ignore
            内环列表折点 = 面类.折点获取_内环列表(实例)  # type: ignore
            return [外环折点, *内环列表折点]
        return [Point(ii) for ii in 实例.coords]  # type: ignore

    @staticmethod
    def 转换_从wkt(wkt数据):
        from .工具包 import 转换工具

        return 转换工具.wkt字符串转几何对象(wkt数据)

    @staticmethod
    def 转换_到wkt(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .工具包 import 转换工具

        return 转换工具.几何对象转wkt字符串(实例)

    @staticmethod
    def 转换_从wkb(wkb数据):
        from .工具包 import 转换工具

        return 转换工具.wkb字符串转几何对象(wkb数据)

    @staticmethod
    def 转换_到wkb(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .工具包 import 转换工具

        return 转换工具.几何对象转wkb字符串(实例)


class _线面通用类:
    # def __init__(self, 内嵌对象) -> None:
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象
    @staticmethod
    def 方向设置(实例, 方向="顺时针"):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        _方向映射 = {"顺时针": 1.0, "逆时针": -1.0}
        方向raw = _方向映射[方向]
        return shapely.geometry.polygon.orient(实例, sign=方向raw)  # type: ignore

    @staticmethod
    def 质点获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .面包 import 面类

        if _点线面通用类.几何类型获取(实例) != "Polygon":  # type: ignore
            x = 面类.面创建_通过点表(_点线面通用类.坐标获取(实例))  # type: ignore
            return x.centroid  # type: ignore
        return 实例.centroid  # type: ignore

    @staticmethod
    def 内点获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .面包 import 面类

        if _点线面通用类.几何类型获取(实例) != "Polygon":  # type: ignore
            x = 面类.面创建_通过点表(_点线面通用类.坐标获取(实例))  # type: ignore
            return x.representative_point()  # type: ignore
        return 实例.representative_point()  # type: ignore

    @staticmethod
    def 图形是否为逆时针(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        if _点线面通用类.图形是否有效(实例):  # type: ignore
            return 实例.is_ccw  # type: ignore
        else:
            from .面包 import 面类
            from .点包 import 点类
            from .线包 import 线类

            if _点线面通用类.几何类型获取(实例) == "Polygon":  # type: ignore
                内点 = 点类.坐标获取(_线面通用类.内点获取(实例))[0]
                点表 = 面类.坐标获取_外环(实例)  # type: ignore
            else:
                内点 = 点类.坐标获取(_线面通用类.内点获取(面类.面创建_通过点表(线类.坐标获取(实例))))[0]  # type: ignore
                点表 = list(线类.坐标获取(实例))  # type: ignore
            # print(f"内点:{内点}")
            # print(f"点表:{点表}")
            总角度 = 0
            for i, x in zip(range(len(点表)), 点表):
                if i == len(点表) - 1:
                    if 总角度 > 359:
                        # print(总角度)
                        return True
                    elif 总角度 < -359:
                        return False
                    else:
                        raise Exception("图形方向判断失败")
                ln1 = 线类.线创建_通过点表([内点, 点表[i]])
                # print(f"ln1:{[内点, 点表[i]]}")
                ln2 = 线类.线创建_通过点表([内点, 点表[i + 1]])
                # print(f"ln2:{[内点, 点表[i+1]]}")
                ang1 = 线类.角度获取(ln1)
                ang2 = 线类.角度获取(ln2)
                ang = ang2 - ang1
                if ang < -180:
                    ang = 360 + ang
                elif ang > 180:
                    ang = ang - 360

                总角度 += ang
                # print(f"ang1:{ang1}，ang2:{ang2}，ang:{ang}，总角度:{总角度}")


class _点集线集面集通用类(_点线面通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象
    @staticmethod
    def 图形列表获取(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return list(实例.geoms)  # type: ignore


if __name__ == "__main__":
    pass
