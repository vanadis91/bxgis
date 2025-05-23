# *-* coding:utf8 *-*
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.环境包 import 输入输出类, 环境管理器类
from bxarcpy.工具包 import 临时路径生成


def 字段名称小写改大写(输入要素路径列表=["JX_规划范围线"], 输出要素路径列表=["内存临时"]):
    ret = []
    for 输入要素路径x, 输出要素路径x in zip(输入要素路径列表, 输出要素路径列表):
        输出要素路径x = 临时路径生成([输入要素路径x]) if 输出要素路径x == "内存临时" else 输出要素路径x
        输入要素x = 要素类.要素创建_通过复制(输入要素路径x)

        字段名称列表 = 要素类.字段名称列表获取(输入要素x, 含系统字段=False)
        # input(字段名称列表)
        for 字段名称x in 字段名称列表:
            if 字段名称x.upper() != 字段名称x:
                要素类.字段修改(输入要素x, 字段名称x, 字段名称x.upper(), 清除字段别称=False)

        输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素x, 输出要素路径x)
        ret.append(输出要素)
    return ret


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    # 工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        字段名称小写改大写(["XG/XG_KZX"], ["XG/XG_KZX1"])
        # 坐标系统一(输入要素路径列表=["CZ_基本农田"])
    # 曲转折(输入要素路径列表=["JX_规划范围线", "JX_街坊范围线", "JX_街区范围线"])
    # 曲转折(输入要素路径列表=["YD_基期", "DIST_用地基期图"])
    # 曲转折(输入要素名称列表=["YD_基期初转换", "YD_基期细化", "YD_农转用20年及以前", "YD_现状修改1", "YD_农转用21年及以后", "YD_审批信息已实施", "YD_地籍信息", "YD_现状修改2", "YD_审批信息已批未建", "YD_上位_粮食生产功能区", "YD_上位农用地落实_耕地质量提升", "YD_上位农用地落实_旱改水", "YD_上位农用地落实_垦造耕地", "YD_上位农用地落实_新增设施农用地", "YD_上位基本农田落实", "YD_GIS方案_农用地设计", "YD_CAD色块以外建设用地修改", "YD_CAD色块"])
    # with open(r"C:\Users\beixiao\Desktop\123.txt", "w") as f:
    #     print("12311111", file=f)
