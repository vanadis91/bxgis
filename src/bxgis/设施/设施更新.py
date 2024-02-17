import bxarcpy
from bxgis import 常用
from bxgis import 配置


def 设施更新(输入要素名称='SS_配套设施', 规划范围线要素名称="JX_规划范围线", 工业片区范围线要素名称="JX_工业片区范围线", 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_设施更新"):
    if 输出要素名称 == "in_memory\\AA_设施更新":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()
    设施要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    设施要素 = 移动至正确位置(输入要素名称=设施要素.名称)
    设施要素 = 清理范围外设施(输入要素名称=设施要素.名称, 范围要素名称=规划范围线要素名称)
    设施要素 = 常用.计算所属区域(输入要素名称=设施要素.名称, 区域要素名称=工业片区范围线要素名称, 字段映射列表=[[配置.设施要素字段映射.所属工业片区字段名称, 配置.区域要素字段映射.区域编号字段名称]], 计算方式="内点在区域要素内")
    设施要素 = 计算远期预留(输入要素名称=设施要素.名称, 城镇集建区要素名称=城镇集建区要素名称, 城镇弹性区要素名称=城镇弹性区要素名称)
    输出要素 = 设施要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素
    # task: 计算开发动态字段


def 移动至正确位置(输入要素名称, 输出要素名称="in_memory\\AA_移动至正确位置"):
    if 输出要素名称 == "in_memory\\AA_移动至正确位置":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    设施要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

    with bxarcpy.游标类.游标创建_通过名称("更新", 设施要素.名称, ["SHAPE@XY", "设施坐标"]) as 游标:
        for x in 游标:
            import re

            设施坐标 = re.split(r"[()\s]", x["设施坐标"])
            x["SHAPE@XY"] = (float(设施坐标[1]), float(设施坐标[2]))

            游标.行更新(x)
    输出要素 = 设施要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 清理范围外设施(输入要素名称, 范围要素名称="JX_规划范围线", 输出要素名称="in_memory\\AA_清理范围外设施"):
    if 输出要素名称 == "in_memory\\AA_清理范围外设施":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    设施要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    范围要素 = bxarcpy.要素类.要素读取_通过名称(范围要素名称).要素创建_通过复制()

    相交后要素 = 设施要素.要素创建_通过相交([范围要素.名称])
    相交后要素.字段删除(保留字段名称列表=设施要素.字段名称列表获取())

    输出要素 = 相交后要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 计算远期预留(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_计算远期预留"):
    if 输出要素名称 == "in_memory\\AA_计算远期预留":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    设施要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    集建区要素 = bxarcpy.要素类.要素读取_通过名称(城镇集建区要素名称).要素创建_通过复制()
    弹性区要素 = bxarcpy.要素类.要素读取_通过名称(城镇弹性区要素名称).要素创建_通过复制()
    开发边界要素 = 集建区要素.要素创建_通过合并([弹性区要素.名称])
    if "控制线名称" not in 开发边界要素.字段名称列表获取():
        raise ValueError(f"{城镇集建区要素名称}和{城镇弹性区要素名称}中未包括 控制线名称 字段。")

    设施要素 = 常用.计算所属区域(输入要素名称=设施要素.名称, 区域要素名称=开发边界要素.名称, 字段映射列表=[["所属三线", "控制线名称"]], 计算方式="内点在区域要素内")
    设施要素.字段添加(配置.设施要素字段映射.远期预留字段名称)

    with bxarcpy.游标类.游标创建_通过名称("更新", 设施要素.名称, [配置.设施要素字段映射.远期预留字段名称, "所属三线", 配置.设施要素字段映射.开发动态字段名称]) as 游标:
        for x in 游标:
            if x["所属三线"] in ["", " ", None] and x[配置.设施要素字段映射.开发动态字段名称] not in ["现状", "现状已实施", "现状保留"]:
                x[配置.设施要素字段映射.远期预留字段名称] = "是"
            else:
                x[配置.设施要素字段映射.远期预留字段名称] = "否"
            游标.行更新(x)
    设施要素.字段删除(["所属三线"])
    输出要素 = 设施要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        设施更新("SS_配套设施", 规划范围线要素名称="JX_规划范围线", 工业片区范围线要素名称="JX_工业片区范围线", 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="SS_配套设施_更新后")
