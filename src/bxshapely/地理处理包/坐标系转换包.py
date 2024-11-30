import numpy as np
from bxpandas.数组包 import 数组类
import sympy as sp
import math


class 平面四参数转换工具:
    @staticmethod
    def 参数计算(转换前点表, 转换后点表):
        if len(转换前点表) != len(转换后点表):
            return False
        if len(转换前点表) < 3:
            return False
        点的个数 = len(转换前点表)
        矩阵B = 数组类.数组创建_全0(形状=(点的个数 * 2, 4))
        矩阵L = 数组类.数组创建_全0(形状=(点的个数 * 2, 1))
        解 = 数组类.数组创建_全1(形状=(4, 1))
        迭代增量 = 数组类.数组创建_全1(形状=(4, 1))

        # 四参数的初始值
        x平移 = 0.0
        y平移 = 0.0
        缩放因子 = 1.0
        旋转因子 = 0.0
        解[0] = x平移
        解[1] = y平移
        解[2] = 缩放因子 * np.cos(旋转因子)
        解[3] = 缩放因子 * np.sin(旋转因子)

        # 构建计算所需矩阵
        for i in range(0, 点的个数):
            矩阵B[2 * i, 0] = 1
            矩阵B[2 * i, 1] = 0
            矩阵B[2 * i, 2] = 转换前点表[i][0]
            矩阵B[2 * i, 3] = -转换前点表[i][1]

            矩阵B[2 * i + 1, 0] = 0
            矩阵B[2 * i + 1, 1] = 1
            矩阵B[2 * i + 1, 2] = 转换前点表[i][1]
            矩阵B[2 * i + 1, 3] = 转换前点表[i][0]

            矩阵L[2 * i] = 转换后点表[i][0]
            矩阵L[2 * i + 1] = 转换后点表[i][1]

        迭代次数 = 0
        while np.linalg.norm(迭代增量) > 0.0001:  # type: ignore
            l = 矩阵L - 矩阵B.dot(解)  # type: ignore
            NBB = 矩阵B.T.dot(矩阵B)  # type: ignore
            W = 矩阵B.T.dot(l)
            迭代增量 = np.linalg.inv(NBB).dot(W)  # type: ignore

            解 += 迭代增量
            迭代次数 += 1
            if 迭代次数 >= 10:
                break

        s, r = sp.symbols("缩放因子, 旋转因子")  # type: ignore
        解列表 = sp.solve([s * sp.cos(r) - 解[2][0], s * sp.sin(r) - 解[3][0]], [s, r])
        缩放因子 = 解列表[0][0]
        旋转因子 = 解列表[0][1]
        解 = [解[0][0], 解[1][0], 缩放因子, 旋转因子]

        print(f"迭代次数：{迭代次数}")
        print(f"四参数：x平移，{解[0]}，y平移，{解[1]}，缩放因子，{解[2]}，旋转因子，{解[3]}")

        残差列表 = 平面四参数转换工具.残差计算(转换前点表, 转换后点表, 解)
        print(f"各点残差：{[format(x, '.10f') for x in 残差列表]}")

        中误差 = 平面四参数转换工具.中误差计算(转换前点表, 转换后点表, 解)
        if 中误差 > 0.05:
            print(f"内符合精度（中误差）：{format(中误差, '.10f')}，大于0.05，不满足1：500地形图精度要求，请重新计算")
        else:
            print(f"内符合精度（中误差）：{format(中误差, '.10f')}，小于等于0.05，满足1：500地形图精度要求")

        误差过大的点的列表 = [(索引, 单点残差) for 单点残差, 索引 in zip(残差列表, range(len(残差列表))) if 单点残差 > 中误差 * 3]
        if len(误差过大的点的列表) > 0:
            print(f"误差过大的点：{误差过大的点的列表}，请去除点")
        else:
            print(f"所有点的误差均在3倍中误差内")

        if len(转换前点表) - len(误差过大的点的列表) < 5:
            print(f"除去误差过大的点后，剩余点不足5个，请补充点")

        return 解

    @staticmethod
    def 中误差计算(转换前点表, 转换后点表, 四参数列表):
        点个数 = len(转换前点表)

        def 单点x残差和y残差(点, 点_观测, 四参数列表):
            点_计算 = 平面四参数转换工具.坐标转换([点], 四参数列表)[0]
            x残差 = 点_计算[0] - 点_观测[0]
            y残差 = 点_计算[1] - 点_观测[1]
            return x残差, y残差

        参数 = list(zip(转换前点表, 转换后点表, [四参数列表 for _ in range(点个数)]))
        x残差平方和 = 0.0
        y残差平方和 = 0.0
        for 参数x in 参数:
            x残差, y残差 = 单点x残差和y残差(*参数x)
            x残差平方和 += x残差**2
            y残差平方和 += y残差**2
        中误差 = (x残差平方和 / (点个数 - 1) + y残差平方和 / (点个数 - 1)) ** 0.5
        return 中误差

    @staticmethod
    def 残差计算(转换前点表, 转换后点表, 四参数列表):
        def 单点残差(点, 点_观测, 四参数列表):
            点_计算 = 平面四参数转换工具.坐标转换([点], 四参数列表)[0]
            残差 = ((点_计算[0] - 点_观测[0]) ** 2 + (点_计算[1] - 点_观测[1]) ** 2) ** 0.5
            return 残差

        参数 = list(zip(转换前点表, 转换后点表, [四参数列表 for _ in range(len(转换前点表))]))
        残差列表 = [单点残差(*参数x) for 参数x in 参数]
        return 残差列表

    @staticmethod
    def 坐标转换(点表, 四参数列表):
        x平移, y平移, 缩放因子, 旋转因子 = 四参数列表

        def 单点转换(pt):
            x转换前 = pt[0]
            y转换前 = pt[1]

            cos = sp.cos(旋转因子)  # 计算cos
            sin = sp.sin(旋转因子)  # 计算sin

            x转换后 = x平移 + 缩放因子 * (cos * x转换前 - sin * y转换前)
            y转换后 = y平移 + 缩放因子 * (sin * x转换前 + cos * y转换前)
            return [x转换后, y转换后]

        ret = [单点转换(pt) for pt in 点表]
        return ret


class 加密坐标系转换工具:
    def __init__(self):
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = math.pi  # π
        self.a = 6378245.0  # 长半轴
        self.es = 0.00669342162296594323  # 偏心率平方
        pass

    def GCJ02_to_BD09(self, gcj_lng, gcj_lat):
        """
        实现GCJ02向BD09坐标系的转换
        :param lng: GCJ02坐标系下的经度
        :param lat: GCJ02坐标系下的纬度
        :return: 转换后的BD09下经纬度
        """
        z = math.sqrt(gcj_lng * gcj_lng + gcj_lat * gcj_lat) + 0.00002 * math.sin(gcj_lat * self.x_pi)
        theta = math.atan2(gcj_lat, gcj_lng) + 0.000003 * math.cos(gcj_lng * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return bd_lng, bd_lat

    def BD09_to_GCJ02(self, bd_lng, bd_lat):
        """
        实现BD09坐标系向GCJ02坐标系的转换
        :param bd_lng: BD09坐标系下的经度
        :param bd_lat: BD09坐标系下的纬度
        :return: 转换后的GCJ02下经纬度
        """
        x = bd_lng - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gcj_lng = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        return gcj_lng, gcj_lat

    def WGS84_to_GCJ02(self, lng, lat):
        """
        实现WGS84坐标系向GCJ02坐标系的转换
        :param lng: WGS84坐标系下的经度
        :param lat: WGS84坐标系下的纬度
        :return: 转换后的GCJ02下经纬度
        """
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.es * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.es)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        gcj_lat = lat + dlat
        gcj_lng = lng + dlng
        return gcj_lng, gcj_lat

    def GCJ02_to_WGS84(self, gcj_lng, gcj_lat):
        """
        实现GCJ02坐标系向WGS84坐标系的转换
        :param gcj_lng: GCJ02坐标系下的经度
        :param gcj_lat: GCJ02坐标系下的纬度
        :return: 转换后的WGS84下经纬度
        """
        dlat = self._transformlat(gcj_lng - 105.0, gcj_lat - 35.0)
        dlng = self._transformlng(gcj_lng - 105.0, gcj_lat - 35.0)
        radlat = gcj_lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.es * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.es)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = gcj_lat + dlat
        mglng = gcj_lng + dlng
        lng = gcj_lng * 2 - mglng
        lat = gcj_lat * 2 - mglat
        return lng, lat

    def BD09_to_WGS84(self, bd_lng, bd_lat):
        """
        实现BD09坐标系向WGS84坐标系的转换
        :param bd_lng: BD09坐标系下的经度
        :param bd_lat: BD09坐标系下的纬度
        :return: 转换后的WGS84下经纬度
        """
        lng, lat = self.BD09_to_GCJ02(bd_lng, bd_lat)
        return self.GCJ02_to_WGS84(lng, lat)

    def WGS84_to_BD09(self, lng, lat):
        """
        实现WGS84坐标系向BD09坐标系的转换
        :param lng: WGS84坐标系下的经度
        :param lat: WGS84坐标系下的纬度
        :return: 转换后的BD09下经纬度
        """
        lng, lat = self.WGS84_to_GCJ02(lng, lat)
        return self.GCJ02_to_BD09(lng, lat)

    def _transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 * math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 * math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 * math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 * math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 * math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 * math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def WGS84_to_WebMercator(self, lng, lat):
        """
        实现WGS84向web墨卡托的转换
        :param lng: WGS84经度
        :param lat: WGS84纬度
        :return: 转换后的web墨卡托坐标
        """
        x = lng * 20037508.342789 / 180
        y = math.log(math.tan((90 + lat) * self.pi / 360)) / (self.pi / 180)
        y = y * 20037508.34789 / 180
        return x, y

    def WebMercator_to_WGS84(self, x, y):
        """
        实现web墨卡托向WGS84的转换
        :param x: web墨卡托x坐标
        :param y: web墨卡托y坐标
        :return: 转换后的WGS84经纬度
        """
        lng = x / 20037508.34 * 180
        lat = y / 20037508.34 * 180
        lat = 180 / self.pi * (2 * math.atan(math.exp(lat * self.pi / 180)) - self.pi / 2)
        return lng, lat


if __name__ == "__main__":
    转换后点表 = 数组类.数组创建_通过列表(
        [
            [3355717.6656, 557130.2740, 0.0000],
            [3353859.6578, 556064.7159, 0.0000],
            [3353274.4557, 553737.9100, 0.0000],
            [3346504.2112, 554661.8482, 0.0000],
            [3346717.1550, 557907.7125, 0.0000],
            [3350818.0883, 558897.1941, 0.0000],
            [3353299.6411, 558199.3822, 0.0000],
            [3355717.6656, 557130.2740, 0.0000],
        ],
    )
    转换前点表 = 数组类.数组创建_通过列表(
        [
            [88287.0640, 121706.6097, 0.0000],
            [86430.4994, 120638.5774, 0.0000],
            [85848.4142, 118311.0117, 0.0000],
            [79076.9998, 119225.8873, 0.0000],
            [79285.6010, 122472.0049, 0.0000],
            [83385.1714, 123466.9608, 0.0000],
            [85867.6333, 122772.4742, 0.0000],
            [88287.0640, 121706.6097, 0.0000],
        ],
    )
    ret = 平面四参数转换工具.参数计算(转换前点表, 转换后点表)
    转换后点表 = 平面四参数转换工具.坐标转换(点表=转换前点表, 四参数列表=ret)
    print(ret)
    print(转换后点表)
