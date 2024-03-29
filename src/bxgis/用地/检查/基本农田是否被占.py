import bxarcpy
from bxpy import 日志
from bxgis import 配置


def 基本农田是否被占(输入要素名称="DIST_用地规划图", 基本农田要素名称="KZX_永久基本农田", 是否输出到CAD=True, 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_基本农田是否被占" + "_" + bxarcpy.工具集.生成短GUID()

    用地要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    基本农田要素 = bxarcpy.要素类.要素读取_通过名称(基本农田要素名称).要素创建_通过复制()

    if 配置.控制线要素字段映射.控制线名称字段名称 not in 基本农田要素.字段名称列表获取():
        raise ValueError(f"{基本农田要素名称}中未包括{配置.控制线要素字段映射.控制线名称字段名称}字段。")
    基本农田要素.字段删除(保留字段名称列表=[配置.控制线要素字段映射.控制线名称字段名称])

    基本农田范围内用地 = 用地要素.要素创建_通过相交([基本农田要素.名称])

    基本农田范围内非农田 = 基本农田范围内用地.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} NOT LIKE '01%'")
    if 基本农田范围内非农田.几何数量 > 0:
        bxarcpy.环境.输出消息(f"基本农田范围内存在非农田用地")
        输出要素 = 基本农田范围内非农田.要素创建_通过复制并重命名重名要素(输出要素名称)
        if 是否输出到CAD:
            基本农田范围内非农田.导出到CAD(配置.计算机信息.CAD输出目录 + "\\AA_基本农田范围内非农田.dwg")
        return 输出要素
    else:
        bxarcpy.环境.输出消息(f"基本农田范围内不存在非农田用地")
        return None


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        基本农田是否被占("DIST_用地规划图", "CZ_控制线_三线_基本农田_图界内")
