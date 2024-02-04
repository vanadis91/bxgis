# -*- coding: utf-8 -*-

import bxarcpy
from typing import Literal


def 入库_设施(设施要素名称="SS_配套设施", 单元名称="临江单元", 批复时间="", 批复文号=""):
    设施要素 = bxarcpy.要素类.要素读取_通过名称(设施要素名称).要素创建_通过复制()

    设施要素.字段添加("DYMC", "字符串", 50, "规划编制单元名称").字段计算("DYMC", f"'{单元名称}'")
    设施要素.字段添加("PFSJ", "日期", None, "批复时间").字段计算("PFSJ", f"'{批复时间}'")
    设施要素.字段添加("PFWH", "字符串", 50, "批复文号").字段计算("PFWH", f"'{批复文号}'")
    设施要素.字段添加("LB", "字符串", 10, "类别代码").字段计算("LB", "!类型代码!")
    设施要素.字段添加("SSDM", "字符串", 10, "配套设施代码").字段计算("SSDM", "!设施代码!")
    设施要素.字段添加("SSMC", "字符串", 50, "配套设施名称").字段计算("SSMC", "!设施名称!")
    设施要素.字段添加("SSDJ", "字符串", 10, "配套设施等级").字段计算("SSDJ", "!设施级别!")
    设施要素.字段添加("DKBH", "字符串", 50, "地块编号").字段计算("DKBH", "!设施所在地块编号!")
    设施要素.字段添加("WZJD", "字符串", 10, "位置精确度").字段计算("WZJD", "'地块级'")
    设施要素.字段添加("YQYL", "字符串", 2, "远期预留").字段计算("YQYL", "!远期预留!")
    设施要素.字段添加("BZ", "字符串", 255, "备注").字段计算("BZ", "!备注说明!")

    设施要素.字段删除(保留字段名称列表=["DYMC", "PFSJ", "PFWH", "LB", "SSDM", "SSMC", "SSDJ", "DKBH", "WZJD", "YQYL", "BZ"])
    设施要素 = 设施要素.要素创建_通过复制并重命名重名要素("XG_PTSS")


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        入库_设施(设施要素名称="SS_配套设施", 单元名称="临江单元", 批复时间="", 批复文号="")
