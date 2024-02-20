# -*- coding: utf-8 -*-

import bxarcpy
from typing import Literal


def 入库_单元(规划范围要素名称, 单元编号, 单元名称, 单元类型: Literal["城镇单元", "乡村单元"], 批复时间, 批复文号, 编制单位, 单元功能, 人口规模, 跨单元平衡情况=""):
    规划范围要素 = bxarcpy.要素类.要素读取_通过名称(规划范围要素名称).要素创建_通过复制()
    with bxarcpy.游标类.游标创建_通过名称("查询", 规划范围要素.名称, ["_形状"]) as 游标:
        for x in 游标:
            if bxarcpy.几何对象类.是否包含曲线(x["_形状"]):
                print(f"要素包括曲线，请转换成折线")
                break
    规划范围要素.字段添加("DYBH", "字符串", 20, "规划编制单元编号").字段计算("DYBH", f"'{单元编号}'")
    规划范围要素.字段添加("DYMC", "字符串", 50, "规划编制单元名称").字段计算("DYMC", f"'{单元名称}'")
    规划范围要素.字段添加("LX", "字符串", 10, "单元类型").字段计算("LX", f"'{单元类型}'")
    规划范围要素.字段添加("PFSJ", "日期", None, "批复时间").字段计算("PFSJ", f"'{批复时间}'")
    规划范围要素.字段添加("PFWH", "字符串", 50, "批复文号").字段计算("PFWH", f"'{批复文号}'")
    规划范围要素.字段添加("BZDW", "字符串", 255, "编制单位").字段计算("BZDW", f"'{编制单位}'")
    规划范围要素.字段添加("DYMJ", "双精度", 50, "单元面积").字段计算("DYMJ", "round(!Shape_Area!/10000, 4)")
    规划范围要素.字段添加("DYGN", "字符串", 255, "单元功能").字段计算("DYGN", f"'{单元功能}'")
    规划范围要素.字段添加("RK", "双精度", 50, "人口规模").字段计算("RK", f"float({人口规模})")
    规划范围要素.字段添加("KDYPH", "字符串", 255, "跨单元平衡情况").字段计算("KDYPH", f"'{跨单元平衡情况}'")
    规划范围要素.字段添加("BZ", "字符串", 255, "备注")
    规划范围要素.字段删除(保留字段名称列表=["DYBH", "DYMC", "LX", "PFSJ", "PFWH", "BZDW", "DYMJ", "DYGN", "RK", "KDYPH", "BZ"])

    数据库 = bxarcpy.数据库类.数据库读取_通过路径(bxarcpy.配置.当前工作空间)
    if "入库材料" not in 数据库.要素数据集名称列表获取():
        要素数据集 = bxarcpy.要素数据集类.要素数据集创建("入库材料")
    规划范围要素.要素创建_通过复制并重命名重名要素("入库材料/XG_GHFW")


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        入库_单元(规划范围要素名称="JX_规划范围线", 单元编号="QT12", 单元名称="临江单元", 单元类型="城镇单元", 批复时间="2023/12/18", 批复文号="杭政函〔2023〕109号", 编制单位="浙江大学建筑设计研究院有限公司", 单元功能="以打造中国先进制造业的重要窗口为使命，以新材料产业为主导，生物医药和装备制造产业为特色，融高端智造、产业服务、现代物流于一体的一流示范产业园区。", 人口规模="3.1809", 跨单元平衡情况="")
