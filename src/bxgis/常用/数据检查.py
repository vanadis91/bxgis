# *-* coding:utf8 *-*
# TODO:检查是否为投影坐标系
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.环境包 import 环境管理器类, 环境类
from bxgis.配置.配置包 import 配置类

基本信息 = 配置类.项目信息对象获取()
from bxarcpy.环境包 import 输入输出类
from typing import Union, Literal, Any


def 数据检查(输入要素路径=r"C:\Users\beixiao\Desktop\01.dwg\控规地块", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 是否几何修复=True, 是否多部件检查=False, 碎线检查阈值: Literal["10", None] = None, 输出要素路径="内存临时") -> str:
    from bxarcpy.游标包 import 游标类
    from bxarcpy.几何包 import 几何类

    if 输出要素路径 == "内存临时":
        输出要素路径 = "in_memory\\AA_拓扑检查" + "_" + 工具包.生成短GUID()
    # if 输入CAD图层名称 in ["点", "线", "面"]:
    #     输入CAD图层名称 = bxarcpy.常量._要素类型映射[输入CAD图层名称]

    # 日志类.输出调试(f"当前工作空间{bxarcpy.配置.当前工作空间}")
    # 输出要素集 = bxarcpy.要素数据集类.导入从CAD(输入CAD路径列表, r"AA_CAD导入GEO1")
    # 日志类.输出调试("输出的要素集是：" + 输出要素集.名称 + rf"\{输入CAD图层名称}")

    # 输入要素 = bxarcpy.要素类.要素读取_通过名称(输出要素集.名称 + rf"\{输入CAD图层名称}")

    输入要素 = 要素类.要素创建_通过复制(输入要素路径)

    # 输出要素集.要素数据集删除()
    # if 是否转曲:
    #     输入要素路径_临时 = 要素类.要素创建_通过增密(输入要素路径_临时)
    if 是否几何修复:
        输入要素 = 要素类.要素创建_通过几何修复(输入要素, 是否打印被删除的要素=True)
    if 是否曲线检查:
        是否包含曲线flag = False
        with 游标类.游标创建("查询", 输入要素, ["_形状"]) as 游标:
            for 游标x in 游标类.属性获取_数据_字典形式(游标, ["_形状"]):
                if 几何类.是否包含曲线(游标x["_形状"]):
                    是否包含曲线flag = True
                    输入输出类.输出消息(f"【{输入要素}】存在曲线，建议增密后再继续。")
                    break
        if 是否包含曲线flag is False:
            输入输出类.输出消息(f"该要素不存在曲线。")

    if 是否拓扑检查:
        要素类.拓扑检查重叠(输入要素)

    if 是否范围检查:
        from bxarcpy.数据库包 import 数据库类

        if 基本信息.项目信息.JX_规划范围线要素名称 in 数据库类.属性获取_要素名称列表(环境类.属性获取_当前工作空间()):
            要素类.拓扑检查范围(输入要素, 基本信息.项目信息.JX_规划范围线要素名称)
        else:
            输入输出类.输出消息(f"当前工作空间中尚不存在范围要素：{基本信息.项目信息.JX_规划范围线要素名称}")
    if 是否多部件检查:
        多部件转单部件前几何数量 = 要素类.属性获取_几何数量(输入要素)
        输入要素 = 要素类.要素创建_通过多部件至单部件(输入要素)
        多部件转单部件后几何数量 = 要素类.属性获取_几何数量(输入要素)
        if 多部件转单部件后几何数量 != 多部件转单部件前几何数量:
            输入输出类.输出消息(f"该要素存在多部件，已炸开。")
    if 碎线检查阈值:
        碎线要素 = 要素类.要素创建_通过筛选(输入要素, f"Shape_Length <= {碎线检查阈值}")
        if 要素类.属性获取_几何数量(碎线要素) > 0:
            输入输出类.输出消息(f"该要素存在碎线，已导出碎线要素。")
            要素类.要素创建_通过复制并重命名重名要素(碎线要素, "AA_碎线要素")
    if 输出要素路径:
        输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素路径)
    return 输出要素路径


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\Project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    # 工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        # 数据检查(输入要素路径=r"DIST_用地现状图", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 输出要素路径=None)
        # 数据检查(输入要素路径=r"CZ_CAD导入_用地规划", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 是否几何修复=True, 输出要素路径=None)
        # 数据检查(输入要素路径=r"DIST_用地调整图", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 是否几何修复=False, 输出要素路径=None)
        # 数据检查(输入要素路径=r"DIST_用途分区规划图", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 是否几何修复=False, 输出要素路径=None)
        # 数据检查(输入要素路径=r"DIST_用地规划图", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 是否几何修复=True, 输出要素路径=None)
        # 要素类.要素创建_通过填充空隙("DIST_用地调整图", "JX_规划范围线", "'00'", "AA_test")
        数据检查(输入要素路径=r"AA_审批信息_农转用33", 是否拓扑检查=True, 是否范围检查=False, 是否曲线检查=True, 是否几何修复=False, 是否多部件检查=False, 碎线检查阈值=None, 输出要素路径=r"AA_审批信息_农转用44")
        # 数据检查(输入要素路径=r"JX_规划范围线", 是否拓扑检查=True, 是否范围检查=True, 是否曲线检查=True, 是否几何修复=True, 输出要素路径=r"JX_规划范围线2")
