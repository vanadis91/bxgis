import bxarcpy
from bxpy import 时间
from bxgis import 配置


def 用地现状图生成(
    输入要素名称列表: list = ["YD_三调", "YD_三调细化和更正", "YD_审批信息，已实施"],
    规划范围线要素名称="JX_规划范围线",
    是否拓扑检查=False,
    是否范围检查=False,
    输出要素名称: str = "DIST_用地现状图",
):
    底层要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称列表[0]).要素创建_通过复制()
    for x in 输入要素名称列表[1:]:
        底层要素 = 底层要素.要素创建_通过更新(x)
        时间.等待(0.5)
        bxarcpy.环境.输出消息(f"完成了 {x} 的合并")
        时间.等待(1)
    底层要素.字段删除(保留字段名称列表=[配置.地块要素字段映射.地类编号字段名称])

    if 规划范围线要素名称:
        输出要素 = 底层要素.要素创建_通过裁剪(规划范围线要素名称)
    else:
        输出要素 = 底层要素

    输出要素 = 输出要素.要素创建_通过多部件至单部件().要素创建_通过复制并重命名重名要素(输出要素名称)

    if 是否拓扑检查:
        需要拓扑的要素名称列表 = [x for x in 输入要素名称列表]
        需要拓扑的要素名称列表.append(输出要素.名称)
        bxarcpy.要素类.拓扑检查重叠_通过要素名称列表(需要拓扑的要素名称列表)
    if 是否范围检查:
        输出要素.拓扑检查范围(规划范围线要素名称)

    return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地现状图生成(
            输入要素名称列表=["YD_基期细化", "YD_农转用20年及以前", "YD_现状修改1", "YD_农转用21年及以后", "YD_审批信息已实施", "YD_地籍信息", "YD_现状修改2"],
            规划范围线要素名称="JX_规划范围线",
            是否拓扑检查=True,
            是否范围检查=True,
            输出要素名称="DIST_用地现状图",
        )
