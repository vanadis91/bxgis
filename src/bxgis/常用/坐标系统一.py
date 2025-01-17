# *-* coding:utf8 *-*
import bxarcpy
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.环境包 import 输入输出类, 环境管理器类


def 坐标系统一(输入要素路径列表=["YD_基期初转换"], 坐标系="PROJCS['CGCS2000_3_Degree_GK_CM_120E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',120.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"):
    from bxarcpy.空间参考包 import 空间参考类

    目标空间参考对象 = 空间参考类.转换_从字符串格式(坐标系)
    for 输入要素路径x in 输入要素路径列表:
        输入要素 = 要素类.要素创建_通过复制(输入要素路径x)
        # 输入要素 = 输入要素路径x
        原有空间参考对象 = 要素类.属性获取_空间参考(输入要素)

        if 原有空间参考对象 is None:
            输出要素 = 要素类.要素创建_通过投影定义(输入要素, 坐标系)
            输入输出类.输出消息(f"{输入要素路径x}不存在空间参考，定义为：{空间参考类.属性获取_名称(目标空间参考对象)}")
            要素类.要素创建_通过复制并重命名重名要素(输出要素, 输入要素路径x)
        elif 空间参考类.属性获取_名称(原有空间参考对象) == 空间参考类.属性获取_名称(目标空间参考对象):
            输入输出类.输出消息(f"{输入要素路径x}空间参考与目标空间一致")
        else:
            输出要素 = 要素类.要素创建_通过投影转换(输入要素, 坐标系)
            输入输出类.输出消息(f"{输入要素路径x}空间参考由{空间参考类.属性获取_名称(原有空间参考对象)}，转换为：{空间参考类.属性获取_名称(目标空间参考对象)}")
            要素类.要素创建_通过复制并重命名重名要素(输出要素, 输入要素路径x)


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        坐标系统一(输入要素路径列表=["CZ_三调"])
        # 坐标系统一(输入要素路径列表=["CZ_基本农田"])
    # 曲转折(输入要素路径列表=["JX_规划范围线", "JX_街坊范围线", "JX_街区范围线"])
    # 曲转折(输入要素路径列表=["YD_基期", "DIST_用地基期图"])
    # 曲转折(输入要素名称列表=["YD_基期初转换", "YD_基期细化", "YD_农转用20年及以前", "YD_现状修改1", "YD_农转用21年及以后", "YD_审批信息已实施", "YD_地籍信息", "YD_现状修改2", "YD_审批信息已批未建", "YD_上位_粮食生产功能区", "YD_上位农用地落实_耕地质量提升", "YD_上位农用地落实_旱改水", "YD_上位农用地落实_垦造耕地", "YD_上位农用地落实_新增设施农用地", "YD_上位基本农田落实", "YD_GIS方案_农用地设计", "YD_CAD色块以外建设用地修改", "YD_CAD色块"])
    # with open(r"C:\Users\beixiao\Desktop\123.txt", "w") as f:
    #     print("12311111", file=f)
