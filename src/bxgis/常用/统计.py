# *-* coding:utf8 *-*
import bxarcpy
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.环境包 import 输入输出类, 环境管理器类


def 统计(输入要素路径="YD_基期初转换", 需统计字段及统计方式列表=[{"字段名称": "", "统计方式": "求和"}], 分组字段列表=["分组1"], 是否显示进度条=True):
    输入要素 = 要素类.要素创建_通过复制(输入要素路径)
    ret = 要素类.统计(输入要素, 需统计字段及统计方式列表=需统计字段及统计方式列表, 分组字段列表=分组字段列表, 是否显示进度条=是否显示进度条)
    print(ret)
    return ret


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        统计(输入要素路径="DIST_用地规划图", 需统计字段及统计方式列表=[{"字段名称": "耕地保有量", "统计方式": "求和"}, {"字段名称": "居住人数", "统计方式": "求和"}, {"字段名称": "居住户数", "统计方式": "求和"}, {"字段名称": "用水量", "统计方式": "求和"}, {"字段名称": "用电负荷量", "统计方式": "求和"}, {"字段名称": "固话装机量", "统计方式": "求和"}, {"字段名称": "有线电视量", "统计方式": "求和"}, {"字段名称": "污水量", "统计方式": "求和"}], 分组字段列表=[])
        # 统计(输入要素路径="JX_街区范围线", 需统计字段及统计方式列表=[{"字段名称": "总永久基本农田用地面积", "统计方式": "求和"}, {"字段名称": "总耕地保有量", "统计方式": "求和"}, {"字段名称": "总耕地用地面积", "统计方式": "求和"}, {"字段名称": "总村庄建设边界用地面积", "统计方式": "求和"}, {"字段名称": "总建筑面积", "统计方式": "求和"}, {"字段名称": "总住宅建筑面积", "统计方式": "求和"}, {"字段名称": "总公服建筑面积", "统计方式": "求和"}, {"字段名称": "总商服建筑面积", "统计方式": "求和"}, {"字段名称": "总工业建筑面积", "统计方式": "求和"}], 分组字段列表=[])
        # 统计(输入要素路径="JX_街坊范围线", 需统计字段及统计方式列表=[{"字段名称": "总永久基本农田用地面积", "统计方式": "求和"}, {"字段名称": "总耕地保有量", "统计方式": "求和"}, {"字段名称": "总耕地用地面积", "统计方式": "求和"}, {"字段名称": "总村庄建设边界用地面积", "统计方式": "求和"}, {"字段名称": "总建筑面积", "统计方式": "求和"}, {"字段名称": "总住宅建筑面积", "统计方式": "求和"}, {"字段名称": "总公服建筑面积", "统计方式": "求和"}, {"字段名称": "总商服建筑面积", "统计方式": "求和"}, {"字段名称": "总工业建筑面积", "统计方式": "求和"}], 分组字段列表=[])
        # 统计(输入要素路径="DIST_用途分区规划图", 需统计字段及统计方式列表=[{"字段名称": "Shape_Area", "统计方式": "求和"}], 分组字段列表=["分区名称"])
    # 曲转折(输入要素路径列表=["JX_规划范围线", "JX_街坊范围线", "JX_街区范围线"])
    # 曲转折(输入要素路径列表=["YD_基期", "DIST_用地基期图"])
    # 曲转折(输入要素名称列表=["YD_基期初转换", "YD_基期细化", "YD_农转用20年及以前", "YD_现状修改1", "YD_农转用21年及以后", "YD_审批信息已实施", "YD_地籍信息", "YD_现状修改2", "YD_审批信息已批未建", "YD_上位_粮食生产功能区", "YD_上位农用地落实_耕地质量提升", "YD_上位农用地落实_旱改水", "YD_上位农用地落实_垦造耕地", "YD_上位农用地落实_新增设施农用地", "YD_上位基本农田落实", "YD_GIS方案_农用地设计", "YD_CAD色块以外建设用地修改", "YD_CAD色块"])
    # with open(r"C:\Users\beixiao\Desktop\123.txt", "w") as f:
    #     print("12311111", file=f)
