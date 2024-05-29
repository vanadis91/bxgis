# -*- coding: utf-8 -*-

import bxarcpy
from typing import Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 入库_设施(
    设施要素名称="SS_配套设施",
    单元名称="临江单元",
    批复时间="",
    批复文号="",
    输出要素名称="XG_PTSS",
    不入库设施名称列表=基本信息.项目信息.不入库设施名称列表,
):
    类型代码字段名称 = 基本信息.设施要素字段映射.类别代码字段名称
    设施代码字段名称 = 基本信息.设施要素字段映射.设施代码字段名称
    设施名称字段名称 = 基本信息.设施要素字段映射.设施名称字段名称
    设施级别字段名称 = 基本信息.设施要素字段映射.设施级别字段名称
    设施所在地块编号字段名称 = 基本信息.设施要素字段映射.设施所在地块编号字段名称
    位置精确度字段名称 = 基本信息.设施要素字段映射.位置精确度字段名称
    远期预留字段名称 = 基本信息.设施要素字段映射.远期预留字段名称
    备注说明字段名称 = 基本信息.设施要素字段映射.备注说明字段名称

    设施要素 = 要素类.要素创建_通过复制(设施要素名称)

    with 游标类.游标创建("更新", 设施要素, [设施名称字段名称]) as 游标:
        for 游标x in 游标类.属性获取_数据_字典形式(游标, [设施名称字段名称]):
            if 游标x[设施名称字段名称] in 不入库设施名称列表:
                游标类.行删除(游标)

    要素类.字段添加(设施要素, "DYMC", "字符串", 50, "规划编制单元名称")
    要素类.字段计算(设施要素, "DYMC", f"'{单元名称}'")

    要素类.字段添加(设施要素, "PFSJ", "日期", None, "批复时间")
    要素类.字段计算(设施要素, "PFSJ", f"'{批复时间}'")

    要素类.字段添加(设施要素, "PFWH", "字符串", 50, "批复文号")
    要素类.字段计算(设施要素, "PFWH", f"'{批复文号}'")

    要素类.字段添加(设施要素, "LB", "字符串", 10, "类别代码")
    要素类.字段计算(设施要素, "LB", f"!{类型代码字段名称}!")

    要素类.字段添加(设施要素, "SSDM", "字符串", 10, "配套设施代码")
    要素类.字段计算(设施要素, "SSDM", f"!{设施代码字段名称}!")

    要素类.字段添加(设施要素, "SSMC", "字符串", 50, "配套设施名称")
    要素类.字段计算(设施要素, "SSMC", f"!{设施名称字段名称}!")

    要素类.字段添加(设施要素, "SSDJ", "字符串", 10, "配套设施等级")
    要素类.字段计算(设施要素, "SSDJ", f"!{设施级别字段名称}!")

    要素类.字段添加(设施要素, "DKBH", "字符串", 50, "地块编号")
    要素类.字段计算(设施要素, "DKBH", f"!{设施所在地块编号字段名称}!")

    要素类.字段添加(设施要素, "WZJD", "字符串", 10, "位置精确度")
    要素类.字段计算(设施要素, "WZJD", f"!{位置精确度字段名称}!")

    要素类.字段添加(设施要素, "YQYL", "字符串", 2, "远期预留")
    要素类.字段计算(设施要素, "YQYL", f"!{远期预留字段名称}!")

    要素类.字段添加(设施要素, "BZ", "字符串", 255, "备注")
    要素类.字段计算(设施要素, "BZ", f"!{备注说明字段名称}!")

    要素类.字段删除(设施要素, 保留字段名称列表=["DYMC", "PFSJ", "PFWH", "LB", "SSDM", "SSMC", "SSDJ", "DKBH", "WZJD", "YQYL", "BZ"])

    数据库 = 基本信息.项目信息.工作空间
    if "入库材料" not in 数据库类.属性获取_要素数据集名称列表(数据库):
        要素数据集 = 要素数据集类.要素数据集创建("入库材料")
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(设施要素, f"入库材料/" + 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        入库_设施(
            设施要素名称="SS_配套设施",
            单元名称=基本信息.项目信息.单元名称,
            批复时间=基本信息.项目信息.批复时间,
            批复文号=基本信息.项目信息.批复文号,
            不入库设施名称列表=基本信息.项目信息.不入库设施名称列表,
        )
