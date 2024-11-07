# -*- coding: utf-8 -*-

from typing import Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.日志包 import 日志类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 区域_工具集_根据入库要素生成区域(
    区域要素路径="JX_分村范围线",
    区域要素类型: Literal["街区街坊分村", "工业片区"] = "街区街坊分村",
    输出要素路径="内存临时",
):
    日志类.临时关闭日志()
    # 需要提前完成编号、耕地面积计算
    输出要素路径 = 工具包.输出路径生成_当采用内存临时时(["根据入库要素生成区域"]) if 输出要素路径 == "内存临时" else 输出要素路径
    # if 输出要素名称 == "内存临时":
    #     输出要素名称 = "in_memory\\AA_根据入库要素生成用地" + "_" + 工具包.生成短GUID()
    区域要素 = 要素类.要素创建_通过复制(区域要素路径)

    字段名称列表 = 要素类.字段名称列表获取(区域要素, False)
    日志类.输出调试(f"字段名称列表：{字段名称列表}")
    for 字段名称x in 字段名称列表:
        要素类.字段修改(区域要素, 字段名称x, 字段名称x + "1")
        要素类.字段修改(区域要素, 字段名称x + "1", 字段名称x.upper())
    字段名称列表 = 要素类.字段名称列表获取(区域要素, False)
    日志类.输出调试(f"字段名称列表改大写后：{字段名称列表}")

    区域编号字段名称 = 基本信息.区域要素字段映射.区域编号字段名称
    区域名称字段名称 = 基本信息.区域要素字段映射.区域名称字段名称
    区域类型字段名称 = 基本信息.区域要素字段映射.区域类型字段名称
    总工业用地面积字段名称 = 基本信息.区域要素字段映射.总工业用地面积字段名称
    总耕地用地面积字段名称 = 基本信息.区域要素字段映射.总耕地用地面积字段名称
    总永久基本农田用地面积字段名称 = 基本信息.区域要素字段映射.总永久基本农田用地面积字段名称
    总生态保护红线用地面积字段名称 = 基本信息.区域要素字段映射.总生态保护红线用地面积字段名称
    总村庄建设边界用地面积字段名称 = 基本信息.区域要素字段映射.总村庄建设边界用地面积字段名称
    总城乡建设用地面积字段名称 = 基本信息.区域要素字段映射.总城乡建设用地面积字段名称
    总村庄建设用地面积字段名称 = 基本信息.区域要素字段映射.总村庄建设用地面积字段名称
    总城镇居住人数字段名称 = 基本信息.区域要素字段映射.总城镇居住人数字段名称
    总村庄户籍人数字段名称 = 基本信息.区域要素字段映射.总村庄户籍人数字段名称
    总村庄居住人数字段名称 = 基本信息.区域要素字段映射.总村庄居住人数字段名称
    总建筑面积字段名称 = 基本信息.区域要素字段映射.总建筑面积字段名称
    总住宅建筑面积字段名称 = 基本信息.区域要素字段映射.总住宅建筑面积字段名称
    总工业建筑面积字段名称 = 基本信息.区域要素字段映射.总工业建筑面积字段名称
    总商服建筑面积字段名称 = 基本信息.区域要素字段映射.总商服建筑面积字段名称
    区域主导属性字段名称 = 基本信息.区域要素字段映射.区域主导属性字段名称
    配套设施汇总字段名称 = 基本信息.区域要素字段映射.配套设施汇总字段名称
    交通设施汇总字段名称 = 基本信息.区域要素字段映射.交通设施汇总字段名称
    市政设施汇总字段名称 = 基本信息.区域要素字段映射.市政设施汇总字段名称
    备注字段名称 = 基本信息.区域要素字段映射.备注字段名称
    if 区域要素类型 == "街区街坊分村":
        要素类.字段删除(区域要素, ["DYMC", "MJ"])

        要素类.字段修改(区域要素, "CJ", 区域类型字段名称)
        要素类.字段修改(区域要素, "BM", 区域编号字段名称)
        要素类.字段修改(区域要素, "LX", 区域主导属性字段名称)
        要素类.字段修改(区域要素, "RK", 总城镇居住人数字段名称)
        要素类.字段修改(区域要素, "JZZL", 总建筑面积字段名称)
        要素类.字段修改(区域要素, "ZZZL", 总住宅建筑面积字段名称)
        要素类.字段修改(区域要素, "GYZL", 总工业建筑面积字段名称)
        要素类.字段修改(区域要素, "SYZL", 总商服建筑面积字段名称)
        要素类.字段修改(区域要素, "HJRK", 总村庄户籍人数字段名称)
        要素类.字段修改(区域要素, "CZRK", 总村庄居住人数字段名称)
        要素类.字段修改(区域要素, "GD", 总耕地用地面积字段名称)
        要素类.字段修改(区域要素, "YN", 总永久基本农田用地面积字段名称)
        要素类.字段修改(区域要素, "ST", 总生态保护红线用地面积字段名称)
        要素类.字段修改(区域要素, "CZBJ", 总村庄建设边界用地面积字段名称)
        要素类.字段修改(区域要素, "CXMJ", 总城乡建设用地面积字段名称)
        要素类.字段修改(区域要素, "CZMJ", 总村庄建设用地面积字段名称)
        要素类.字段修改(区域要素, "BZ", 备注字段名称)

        # 要素类.字段添加(区域要素, 绿地率字段名称)
        # 要素类.字段计算(区域要素, 绿地率字段名称, f"str(round(!LDL!, 2))")
        # 要素类.字段删除(区域要素, ["LDL"])

    elif 区域要素类型 == "工业片区":
        要素类.字段删除(区域要素, ["DYMC", "PQMJ"])

        # 要素类.字段修改(区域要素, "CJ", 区域类型字段名称)
        要素类.字段修改(区域要素, "PQBM", 区域编号字段名称)
        要素类.字段修改(区域要素, "PQMC", 区域名称字段名称)
        要素类.字段修改(区域要素, "YDZL", 总工业用地面积字段名称)
        要素类.字段修改(区域要素, "JZZL", 总工业建筑面积字段名称)
        要素类.字段修改(区域要素, "ZDGN", 区域主导属性字段名称)
        要素类.字段修改(区域要素, "PTSS", 配套设施汇总字段名称)
        if "PTSS1" in 字段名称列表:
            要素类.字段修改(区域要素, "PTSS1", 配套设施汇总字段名称 + "1")
        if "PTSS2" in 字段名称列表:
            要素类.字段修改(区域要素, "PTSS2", 配套设施汇总字段名称 + "2")
        if "PTSS3" in 字段名称列表:
            要素类.字段修改(区域要素, "PTSS3", 配套设施汇总字段名称 + "3")
        要素类.字段修改(区域要素, "JTSS", 交通设施汇总字段名称)
        if "JTSS1" in 字段名称列表:
            要素类.字段修改(区域要素, "JTSS1", 交通设施汇总字段名称 + "1")
        if "JTSS2" in 字段名称列表:
            要素类.字段修改(区域要素, "JTSS2", 交通设施汇总字段名称 + "2")
        if "JTSS3" in 字段名称列表:
            要素类.字段修改(区域要素, "JTSS3", 交通设施汇总字段名称 + "3")
        要素类.字段修改(区域要素, "SZSS", 市政设施汇总字段名称)
        if "SZSS1" in 字段名称列表:
            要素类.字段修改(区域要素, "SZSS1", 市政设施汇总字段名称 + "1")
        if "SZSS2" in 字段名称列表:
            要素类.字段修改(区域要素, "SZSS2", 市政设施汇总字段名称 + "2")
        if "SZSS3" in 字段名称列表:
            要素类.字段修改(区域要素, "SZSS3", 市政设施汇总字段名称 + "3")
        要素类.字段修改(区域要素, "BZ", 备注字段名称)

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(区域要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    日志类.开启()
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        # 区域_工具集_根据入库要素生成区域(
        #     区域要素路径="XG/XG_JQJF",
        #     输出要素路径="JX_街区范围线1",
        # )
        区域_工具集_根据入库要素生成区域(
            区域要素路径="XG/XG_GYPQ",
            区域要素类型="工业片区",
            输出要素路径="JX_工业片区范围线1",
        )
        # 区域_工具集_根据入库要素生成区域(
        #     区域要素路径="JX_分村范围线",
        #     输出要素路径="JX_分村范围线1",
        # )
