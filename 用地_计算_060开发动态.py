import bxarcpy
from typing import Literal
import 用地_计算_010所属区域


def 用地创建_通过计算开发动态(输入要素名称, 输出要素名称="in_memory\\AA_计算开发动态"):
    if 输出要素名称 == "in_memory\\AA_计算开发动态":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

    用地要素 = 用地_计算_010所属区域.用地创建_通过计算所属区域(输入要素.名称, 区域要素名称="KZX_城镇开发边界", 字段映射列表=[["所属三线", "控制线名称"]], 计算方式="按输入要素内点")
    with bxarcpy.游标类.游标创建_通过名称("更新", 用地要素.名称, ["所属三线", "地类编号", "开发动态"]) as 游标:
        for x in 游标:
            if x["所属三线"] not in ["", " ", None]:
                x["所属三线"] = "开发边界内"

            if x["开发动态"] in ["现状已实施", "现状保留", "保留"]:
                x["开发动态"] = "保留"
            elif x["开发动态"] in ["改/扩建", "改扩建"] and x["所属三线"] == "开发边界内":
                x["开发动态"] = "改/扩建"
            elif x["开发动态"] in ["盘活"] and x["所属三线"] != "开发边界内":
                x["开发动态"] = "盘活"
            elif x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"] and x["所属三线"] == "开发边界内":
                x["开发动态"] = "新建"
            elif x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"] and x["所属三线"] != "开发边界内":
                x["开发动态"] = "新增"

            游标.行更新(x)

    输出要素 = 用地要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地创建_通过计算开发动态("DIST_用地规划图", 输出要素名称="DIST_用地规划图_动态")
