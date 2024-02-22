# -*- coding: utf-8 -*-

import bxarcpy
from typing import Literal


def 入库_规划地块(地块要素名称="DIST_用地规划图", 单元名称="临江单元", 批复时间="", 批复文号="", 地块编号字段名称="地块编号", 地类编号字段名称="地类编号", 性质名称字段名称="性质名称", 地块性质别称字段名称="地块性质别称", 兼容比例字段名称="兼容比例", 输出要素名称="XG_GHDK"):
    # 需要提前完成编号、耕地面积计算

    地块要素 = bxarcpy.要素类.要素读取_通过名称(地块要素名称).要素创建_通过复制()

    地块要素.字段添加("DYMC", "字符串", 50, "规划编制单元名称").字段计算("DYMC", f"'{单元名称}'")
    地块要素.字段添加("PFSJ", "日期", None, "批复时间").字段计算("PFSJ", f"'{批复时间}'")
    地块要素.字段添加("PFWH", "字符串", 50, "批复文号").字段计算("PFWH", f"'{批复文号}'")
    地块要素.字段添加("DKBH", "字符串", 50, "地块编号").字段计算("DKBH", f"!{地块编号字段名称}!")
    地块要素.字段添加("DLDM", "字符串", 255, "地类代码").字段计算("DLDM", f"!{地类编号字段名称}!.replace('v','')")
    地块要素.字段添加("DLMC", "字符串", 255, "地类名称").字段计算("DLMC", f"!{性质名称字段名称}!")
    地块要素.字段添加("DLBM", "字符串", 100, "地类编码").字段计算("DLBM", f"!{地块性质别称字段名称}!")
    地块要素.字段添加("ZDLDM", "字符串", 10, "主地类代码").字段计算("ZDLDM", f'!{地类编号字段名称}!.split("(")[0].split("/")[0].replace("v","")')
    地块要素.字段添加("JRBL", "字符串", 10, "用地兼容比例")
    地块要素.字段添加("MJ", "双精度", 50, "用地面积").字段计算("MJ", "round(!Shape_Area!/10000, 4)")
    地块要素.字段添加("RJL", "单精度", 50, "容积率")
    地块要素.字段添加("LDL", "单精度", 50, "绿地率")
    地块要素.字段添加("JZMD", "单精度", 50, "建筑密度")
    地块要素.字段添加("JZGD", "单精度", 50, "建筑高度")
    地块要素.字段添加("XGLX", "字符串", 20, "限高类型")
    地块要素.字段添加("FJSS1", "字符串", 255, "附建设施1")
    地块要素.字段添加("FJSS2", "字符串", 255, "附建设施2")
    地块要素.字段添加("GXYQ", "字符串", 255, "城市设计刚性要求")
    地块要素.字段添加("TXYQ", "字符串", 255, "城市设计弹性要求")
    # 保留、改/扩建、新建 保留、盘活、新增
    地块要素.字段添加("GHDT", "字符串", 10, "规划动态")
    地块要素.字段添加("XZYD", "字符串", 255, "选择用地")
    地块要素.字段添加("GDMJ", "双精度", 50, "耕地净面积").字段计算("GDMJ", "round(!耕地保有量!, 2)")
    # 非建设用地、城镇建设用地、村庄建设用地、区域建设用地、其他建设用地
    地块要素.字段添加("FL", "字符串", 20, "用地分类")
    地块要素.字段添加("TDM", "字符串", 50, "土地码").字段计算("TDM", "!土地码!")
    地块要素.字段添加("BZ", "字符串", 255, "备注")

    需操作的字段名称列表 = ["XGLX", "绝对高度", "配套设施规模", "FJSS1", "FJSS2", "开发动态", "GHDT", "地块编号", "TDM", "地类编号", "所属街区", "所属街坊", "BZ", "备注说明", "兼容比例", "JRBL", "RJL", "容积率", "LDL", "绿地率", "JZMD", "建筑密度", "JZGD", "建筑限高", "FL", "用地构成"]

    with bxarcpy.游标类.游标创建_通过名称("更新", 地块要素.名称, 需操作的字段名称列表) as 游标:
        for x in 游标:
            if x["绝对高度"] in ["51.7", "65", "156.7"]:
                x["XGLX"] = "机场限高"
                if x["备注说明"] in ["", " ", None]:
                    x["BZ"] = f'限高{x["绝对高度"]}米（1985国家高程基准）'
                else:
                    x["BZ"] = x["备注说明"] + f'，限高{x["绝对高度"]}米（1985国家高程基准）'

            if len(x["配套设施规模"]) > 510:
                bxarcpy.环境.输出消息("有地块配套栏字符大于510")
            elif len(x["配套设施规模"]) > 255:
                x["FJSS1"] = x["配套设施规模"][0:255]
                x["FJSS2"] = x["配套设施规模"][255:]
            else:
                x["FJSS1"] = x["配套设施规模"]

            x["GHDT"] = x["开发动态"]

            if x[兼容比例字段名称] not in ["", " ", None]:
                x["JRBL"] = x[兼容比例字段名称].replace("/", ":")

            if x["容积率"] not in ["", " ", None]:
                x["RJL"] = float(x["容积率"])
            else:
                x["RJL"] = 0.0

            if x["绿地率"] not in ["", " ", None]:
                x["LDL"] = float(x["绿地率"])
            else:
                x["LDL"] = 0.0

            if x["建筑密度"] not in ["", " ", None]:
                x["JZMD"] = float(x["建筑密度"])
            else:
                x["JZMD"] = 0.0

            if x["建筑限高"] not in ["", " ", None]:
                x["JZGD"] = float(x["建筑限高"])
            else:
                x["JZGD"] = 0.0

            if x["用地构成"] in ["农园地", "林草地", "农业设施建设用地", "水域"]:
                x["FL"] = "非建设用地"
            elif x["用地构成"] in ["城镇建设用地"]:
                x["FL"] = "城镇建设用地"
            elif x["用地构成"] in ["村庄建设用地"]:
                x["FL"] = "村庄建设用地"
            elif x["用地构成"] in ["区域基础设施用地"]:
                x["FL"] = "区域建设用地"
            elif x["用地构成"] in ["其他建设用地"]:
                x["FL"] = "其他建设用地"

            游标.行更新(x)

    地块要素.字段删除(保留字段名称列表=["DYMC", "PFSJ", "PFWH", "DKBH", "DLDM", "DLMC", "DLBM", "ZDLDM", "JRBL", "MJ", "RJL", "LDL", "JZMD", "JZGD", "XGLX", "FJSS1", "FJSS2", "GXYQ", "TXYQ", "GHDT", "XZYD", "GDMJ", "FL", "TDM", "BZ"])

    数据库 = bxarcpy.数据库类.数据库读取_通过路径(bxarcpy.配置.当前工作空间)
    if "入库材料" not in 数据库.要素数据集名称列表获取():
        要素数据集 = bxarcpy.要素数据集类.要素数据集创建("入库材料")
    输出要素 = 地块要素.要素创建_通过复制并重命名重名要素("入库材料" + "/" + 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        入库_规划地块(地块要素名称="DIST_用地规划图", 单元名称="临江单元", 批复时间="2023/12/18", 批复文号="杭政函〔2023〕109号", 地块编号字段名称="地块编号", 地类编号字段名称="地类编号", 性质名称字段名称="性质名称", 地块性质别称字段名称="地块性质别称", 兼容比例字段名称="兼容比例")
