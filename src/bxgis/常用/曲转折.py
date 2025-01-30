# *-* coding:utf8 *-*
# import sys

# with open(r"C:\Users\beixiao\Desktop\123.txt", "w") as f:
#     print(sys.path, file=f)
# if "c:\\program files (x86)\\arcgis\\desktop10.8\\bin" in sys.path:
#     sys.path.remove("c:\\program files (x86)\\arcgis\\desktop10.8\\bin")
# if "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcPy" in sys.path:
#     sys.path.remove("c:\\program files (x86)\\arcgis\\desktop10.8\\ArcPy")
# if "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcToolbox\\Scripts" in sys.path:
#     sys.path.remove("c:\\program files (x86)\\arcgis\\desktop10.8\\ArcToolbox\\Scripts")

from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.环境包 import 输入输出类, 环境管理器类


def 曲转折(输入要素路径列表=["YD_基期初转换"], 手动确认是否转换=False):
    for 输入要素名称 in 输入要素路径列表:
        输入要素 = 要素类.要素创建_通过复制(输入要素名称)
        是否转换flag = "-1"
        with 游标类.游标创建("查询", 输入要素, ["_形状", "_ID"]) as 游标:
            for y in 游标类.属性获取_数据_字典形式(游标, ["_形状", "_ID"]):
                if 几何类.是否包含曲线(y["_形状"]):
                    输入输出类.输出消息(f"{输入要素名称}中ID为{y['_ID']}的项包含曲线")
                    if 手动确认是否转换:
                        是否转换flag = input("是否转换 [是(1)/否(0)]：")
                        break
                    else:
                        是否转换flag = "1"
        if 是否转换flag == "1":
            输入要素 = 要素类.要素创建_通过增密(输入要素)
            输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输入要素名称, "转折前")
        elif 是否转换flag == "-1":
            输入输出类.输出消息(f"{输入要素名称} 不包含曲线")


if __name__ == "__main__":
    # from bxpy.系统包 import 系统类
    # from bxgis.配置.配置包 import 配置类
    # import json

    # 参数列表 = 系统类.属性获取_当前进程参数()
    # print(参数列表)
    # if len(参数列表) == 1:
    #     # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    #     # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    #     # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    #     工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    #     参数 = {"输入要素路径列表": ["JX_街坊范围线"]}
    #     参数_字符串形式 = json.dumps(参数, ensure_ascii=False)
    # else:
    #     工作空间 = 配置类.获取工作空间()
    #     参数_字符串形式 = 参数列表[1]

    # 参数字典 = json.loads(参数_字符串形式)

    # 工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Desktop\杭州市钱塘区临江单元入库数据.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        曲转折(["XG/XG_GHDK", "XG/XG_GHFW", "XG/XG_GYPQ", "XG/XG_JQJF", "XG/XG_JSBJ", "XG/XG_KZX", "XG/XG_PTSS", "XG/XG_TZD", "XG/XG_TZM", "XG/XG_TZX", "XG/XG_YTFQ"])
        # 曲转折(["JX_工业片区范围线"])
        # 曲转折(["DL_道路中线", "DL_道路边线", "DL_河道边线", "DL_河道中线", "SZ_电力线", "GZW_高架桥", "GZW_绿化线", "GZW_天然气", "GZW_高压线", "GZW_虚位控制河道", "GZW_虚位控制绿地", "GZW_虚位控制道路"])
    # 曲转折(输入要素路径列表=["YD_基期", "DIST_用地基期图"])
    # 曲转折(输入要素名称列表=["YD_基期初转换", "YD_基期细化", "YD_农转用20年及以前", "YD_现状修改1", "YD_农转用21年及以后", "YD_审批信息已实施", "YD_地籍信息", "YD_现状修改2", "YD_审批信息已批未建", "YD_上位_粮食生产功能区", "YD_上位农用地落实_耕地质量提升", "YD_上位农用地落实_旱改水", "YD_上位农用地落实_垦造耕地", "YD_上位农用地落实_新增设施农用地", "YD_上位基本农田落实", "YD_GIS方案_农用地设计", "YD_CAD色块以外建设用地修改", "YD_CAD色块"])
    # with open(r"C:\Users\beixiao\Desktop\123.txt", "w") as f:
    # pass
    # print("12311111", file=f)
