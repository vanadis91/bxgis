import shapely
from shapely.geometry import LineString, Point, LinearRing, MultiLineString
from typing import Union, Literal
from .通用对象包 import _点线面通用类, _点集线集面集通用类
from shapely import wkt


class _线通用类(_点线面通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 角度获取(实例) -> float:  # type: ignore
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)

        import math
        from math import pi as PI

        line1 = 线类.坐标获取(实例)  # type: ignore
        x差值 = line1[1][0] - line1[0][0]
        y差值 = line1[1][1] - line1[0][1]
        line1 = [(0, 0), (x差值, y差值)]
        if x差值 == 0 and y差值 > 0:
            return 90
        if x差值 == 0 and y差值 < 0:
            return 270
        if x差值 > 0 and y差值 == 0:
            return 0
        if x差值 < 0 and y差值 == 0:
            return 180
        if x差值 == 0 and y差值 == 0:
            raise Exception("无法求取角度")
        angle_rad = abs(math.atan(y差值 / x差值))
        angle_deg = angle_rad * 180 / PI
        if x差值 > 0 and y差值 > 0:
            return angle_deg
        if x差值 > 0 and y差值 < 0:
            return 360 - angle_deg
        if x差值 < 0 and y差值 > 0:
            return 180 - angle_deg
        if x差值 < 0 and y差值 < 0:
            return 180 + angle_deg

    @staticmethod
    def 点转距离(实例, pt: Point, 归一化=False):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.project(pt, normalized=归一化)  # type: ignore

    @staticmethod
    def 点转参数(实例, pt: Point):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .点包 import 点集类, 点类

        距离 = 实例.project(pt)  # type: ignore
        点表 = 线类.折点获取(实例)  # type: ignore
        # print(点表)

        for i, x in zip(range(len(点表)), 点表):
            if i == len(点表) - 1:
                return False
            附近点1索引 = i
            附近点1距离 = 线类.点转距离(实例, x)  # type: ignore
            附近点2索引 = i + 1
            附近点2距离 = 线类.点转距离(实例, 点表[附近点2索引])  # type: ignore
            if 附近点1距离 <= 距离 <= 附近点2距离:
                参数 = 附近点1索引 + (距离 - 附近点1距离) / (附近点2距离 - 附近点1距离)
                return 参数
        return False

    @staticmethod
    def 距离转点(实例, 距离, 归一化=False):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.interpolate(距离, normalized=归一化)  # type: ignore

    @staticmethod
    def 距离转参数(实例, 距离):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from bxshapely.点包 import 点集类, 点类

        pt = 线类.距离转点(实例, 距离)  # type: ignore
        return 线类.点转参数(实例, pt)  # type: ignore

    @staticmethod
    def 参数转距离(实例, 参数):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from bxshapely.点包 import 点集类, 点类

        点表 = [Point(ii) for ii in 线类.坐标获取(实例)]  # type: ignore
        # print(点表)
        参数整数部分 = int(参数)
        参数小数部分 = 参数 - 参数整数部分

        附近点1距离 = 线类.点转距离(实例, 点表[参数整数部分])  # type: ignore
        附近点2距离 = 线类.点转距离(实例, 点表[参数整数部分 + 1])  # type: ignore

        距离 = (附近点2距离 - 附近点1距离) * 参数小数部分 + 附近点1距离
        return 距离

    @staticmethod
    def 参数转点(实例, 参数):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        距离 = 线类.参数转距离(实例, 参数)  # type: ignore
        return 线类.距离转点(实例, 距离)  # type: ignore

    @staticmethod
    def 图形是否闭合(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return 实例.is_ring  # type: ignore

    @staticmethod
    def 截取一部分线(实例, 起点, 终点, 归一化=False):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        return shapely.ops.substring(实例, 起点, 终点, normalized=归一化)  # type: ignore

    @staticmethod
    def 偏移(实例, 距离, 方向="左", 四分之一圆转折后段数=16, 折点样式="圆角", 斜角比=5.0):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        _方向映射 = {"左": "left", "右": "right"}
        方向raw = _方向映射[方向]
        _折点样式映射 = {"圆角": 1, "方角": 2, "倒角": 3}
        折点样式raw = _折点样式映射[折点样式]
        return 实例.parallel_offset(距离, 方向raw, resolution=四分之一圆转折后段数, join_style=折点样式raw, mitre_limit=斜角比)  # type: ignore

    @staticmethod
    def 整理(实例):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        from .线包 import 线类
        from .点包 import 点类

        点表 = 线类.折点获取(实例)  # type: ignore
        临时点表 = []
        for i, x in zip(range(len(点表)), 点表):
            if i == len(点表) - 1:
                临时点表.append(点表[i])
                return 线类.线创建_通过点表(临时点表)
            if 点类.两图形间最短距离(点表[i], 点表[i + 1]) > 0.00001:
                临时点表.append(点表[i])

    @staticmethod
    def 多部件连接(实例, x2):
        # self为自定义类, 内嵌对象 = (True, self._内嵌对象) if hasattr(self, "_内嵌对象") else (False, self)
        pt1, pt2 = 线类.两图形间最近点(实例, x2)  # type: ignore

        lin1点表 = 线类.折点获取(实例)  # type: ignore
        lin2点表 = 线类.折点获取(x2)

        参数1 = 线类.点转参数(实例, pt1)  # type: ignore
        参数2 = 线类.点转参数(x2, pt2)

        参数1上一个点 = int(参数1)
        参数2下一个点 = int(参数2) + 1

        合并后点表 = lin1点表[0 : 参数1上一个点 + 1]
        合并后点表.append(pt1)
        合并后点表.append(pt2)
        合并后点表.extend(lin2点表[参数2下一个点:])
        合并后点表.extend(lin2点表[0:参数2下一个点])
        合并后点表.append(pt2)
        合并后点表.append(pt1)
        合并后点表.extend(lin1点表[参数1上一个点 + 1 :])

        ret = 环类.整理(环类.环创建_通过点表(合并后点表))
        return ret


class 线集类(_点集线集面集通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 线集创建_通过点表列表(x):
        return MultiLineString(x)


class 线类(_线通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 线创建_通过点表(点表):
        return LineString(点表)

    # @staticmethod
    # def 线创建_通过线实例(x: LineString):
    #     return LineString(x)


class 环类(_线通用类):
    # def __init__(self, 内嵌对象) -> None:
    #     super().__init__(内嵌对象)
    #     if hasattr(内嵌对象, "_内嵌对象"):
    #         self._内嵌对象 = 内嵌对象._内嵌对象
    #     else:
    #         self._内嵌对象 = 内嵌对象

    @staticmethod
    def 环创建_通过点表(点表):
        return LinearRing(点表)

    # @staticmethod
    # def 环创建_通过环实例(x: LinearRing):
    #     return 环类(LinearRing(x))


if __name__ == "__main__":
    # import 环

    a = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
    b = 环类.环创建_通过点表(a)
    print(环类.面积获取(b))
    # b = 面.外环获取(a)
    # print(b)
    # print(线.图形是否为逆时针(b))

    # print(线.角度获取(x1) - 线.角度获取(x2))
    # 线.线创建_通过点表(合并后点表)
    # print(线.点转参数(line1, point2))
    # print(线.距离转点(line1, 线.点转距离(line1, pt1)))
    # 线.插入点(line2, 线.点转参数(line2, pt2))
    # line1.union(line3)
    # line1上最近点距离 = 线.点转距离(line1, pt1)
    # line2上最近点距离 = 线.点转距离(line2, pt2)
    # line1点表 = list(线.点表获取(line1))
    # poly1 = wkt.loads("POLYGON((1 1,2 1,2 2,1 2,1 1))")
    # poly2 = wkt.loads("POLYGON((1.5 2,2.5 2,2.5 3,1.5 3,1.5 2))")
    # shared_line = poly1.intersection(poly2)
    # poly1 = poly1.union(shared_line)
    # poly2 = poly2.union(shared_line)
    # print(list(poly1.exterior.coords))
