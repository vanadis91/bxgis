import shapely
from shapely.geometry import LineString, Point, LinearRing, MultiLineString
from typing import Union, Literal
from .通用对象包 import _点线面通用类, _点集线集面集通用类
from shapely import wkt


class 转换工具:
    @staticmethod
    def wkb字符串转几何对象(wkb字符串):
        return shapely.from_wkb(wkb字符串)

    @staticmethod
    def wkt字符串转几何对象(wkt字符串):
        return shapely.from_wkt(wkt字符串)

    @staticmethod
    def 几何对象转wkb字符串(图形):
        return shapely.to_wkb(图形)

    @staticmethod
    def 几何对象转wkt字符串(图形):
        return shapely.to_wkt(图形)


if __name__ == "__main__":
    pass
