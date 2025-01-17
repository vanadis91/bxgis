# -*- coding: utf-8 -*-

from typing import Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.日志包 import 日志生成器
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息

控制线类型与名称映射 = [
    {"类型名称": "道路中心线-公路", "类型编码": "DLZX-GL", "图层名称": "DL_道路中线"},
    {"类型名称": "道路边线-公路", "类型编码": "DLBX-GL", "图层名称": "DL_道路边线"},
    {"类型名称": "道路中心线-快速路", "类型编码": "DLZX-KS", "图层名称": "DL_道路中线"},
    {"类型名称": "道路边线-快速路", "类型编码": "DLBX-KS", "图层名称": "DL_道路边线"},
    {"类型名称": "道路中心线-主干路", "类型编码": "DLZX-ZG", "图层名称": "DL_道路中线"},
    {"类型名称": "道路边线-主干路", "类型编码": "DLBX-ZG", "图层名称": "DL_道路边线"},
    {"类型名称": "道路中心线-次干路", "类型编码": "DLZX-CG", "图层名称": "DL_道路中线"},
    {"类型名称": "道路边线-次干路", "类型编码": "DLBX-CG", "图层名称": "DL_道路边线"},
    {"类型名称": "道路中心线-支路", "类型编码": "DLZX-ZL", "图层名称": "DL_道路中线"},
    {"类型名称": "道路边线-支路", "类型编码": "DLBX-ZL", "图层名称": "DL_道路边线"},
    {"类型名称": "道路边线-高架", "类型编码": "DLBX-GJ", "图层名称": "GZW_高架桥"},
    {"类型名称": "道路边线-隧道", "类型编码": "DLBX-SD", "图层名称": "GZW_隧道"},
    {"类型名称": "河道中心线", "类型编码": "HDZX", "图层名称": "DL_河道中线"},  # 开发边界外河道以及开发边界内的现状河道不需河道中心线
    {"类型名称": "河道边线", "类型编码": "HDBX", "图层名称": "DL_河道边线"},
    {"类型名称": "绿化线", "类型编码": "LHX", "图层名称": "GZW_绿化线"},
    {"类型名称": "铁路", "类型编码": "TL", "图层名称": "GZW_铁路线"},  # 铁路轨道中心线以及两条控制廊道
    {"类型名称": "输油管道|设施线", "类型编码": "SYG", "图层名称": "GZW_输油管"},  # 设施线以及两条控制廊道
    {"类型名称": "原水输水管线", "类型编码": "YS", "图层名称": "GZW_原水管"},  # 设施线以及两条控制廊道
    {"类型名称": "高压电力架空线", "类型编码": "GYX", "图层名称": "GZW_高压线"},  # 架空的电力线路，设施线以及两条控制廊道
    {"类型名称": "高压燃气设施线", "类型编码": "TRQ", "图层名称": "GZW_天然气"},  # 设施线以及两条控制廊道，注明省管或市管天然气
    {"类型名称": "综合管廊", "类型编码": "ZHGL", "图层名称": "GZW_综合管廊"},
    {"类型名称": "自来水管线", "类型编码": "GX-S", "图层名称": "SZ_给水管"},
    {"类型名称": "污水管线", "类型编码": "GX-W", "图层名称": "SZ_污水管"},
    {"类型名称": "雨水管线", "类型编码": "GX-Y", "图层名称": "SZ_雨水管"},
    {"类型名称": "地下电力管线", "类型编码": "GX-D", "图层名称": "SZ_电力线"},
    {"类型名称": "中压燃气管线", "类型编码": "GX-Q", "图层名称": "SZ_燃气管"},
    {"类型名称": "热力管线", "类型编码": "RL", "图层名称": "SZ_热力管"},
    {"类型名称": "通信管线", "类型编码": "TX", "图层名称": "SZ_通信线"},
    {"类型名称": "防洪（潮）设施控制线", "类型编码": "FH", "图层名称": "GZW_防洪设施"},
    {"类型名称": "综合防灾减灾设施控制线", "类型编码": "FZ", "图层名称": "GZW_综合防灾设施"},
    {"类型名称": "微波通道", "类型编码": "WBTD", "图层名称": "GZW_微波通道"},
    {"类型名称": "建筑控制高度分区线", "类型编码": "GDFQ", "图层名称": "GZW_高度分区"},
    {"类型名称": "地块间公共通道", "类型编码": "DKJGGTD", "图层名称": "GZW_共用通道"},
    {"类型名称": "远景道路控制线", "类型编码": "YJDLKZ", "图层名称": "GZW_远景道路"},
    {"类型名称": "控制绿化线", "类型编码": "KZLHX", "图层名称": "GZW_虚位控制绿地"},
    {"类型名称": "虚位控制河道", "类型编码": "XWKZHD", "图层名称": "GZW_虚位控制河道"},
    {"类型名称": "虚位控制道路", "类型编码": "XWKZDL", "图层名称": "GZW_虚位控制道路"},
    {"类型名称": "景观控制廊道线", "类型编码": "JGKZLD", "图层名称": "GZW_景观控制廊道"},
    {"类型名称": "其他控制线", "类型编码": "QT", "图层名称": "GZW_其他控制线"},
]


def 道路_工具集_根据入库要素生成控制线(
    控制线要素名称="XG_KZX",
    输出要素名称后缀="1",
):
    日志生成器.临时关闭日志()

    控制线要素 = 要素类.要素创建_通过复制(控制线要素名称)

    字段名称列表 = 要素类.字段名称列表获取(控制线要素, False)

    for 字段名称x in 字段名称列表:
        要素类.字段修改(控制线要素, 字段名称x, 字段名称x.upper())

    控制线名称字段名称 = 基本信息.控制线要素字段映射.控制线名称字段名称
    控制线类型字段名称 = 基本信息.控制线要素字段映射.控制线类型字段名称
    控制线开发动态字段名称 = 基本信息.控制线要素字段映射.控制线开发动态字段名称
    控制线备注字段名称 = 基本信息.控制线要素字段映射.控制线备注字段名称

    要素类.字段删除(控制线要素, ["DYMC", "PFSJ", "PFWH", "LXDM"])
    要素类.字段修改(控制线要素, "LXMC", 控制线类型字段名称)
    要素类.字段修改(控制线要素, "MC", 控制线名称字段名称)
    要素类.字段修改(控制线要素, "ZT", 控制线开发动态字段名称)
    要素类.字段修改(控制线要素, "BZ", 控制线备注字段名称)

    操作字段名称 = ["_形状", 控制线类型字段名称, 控制线名称字段名称, 控制线开发动态字段名称, 控制线备注字段名称]
    with 游标类.游标创建("查询", 控制线要素, 操作字段名称) as 游标:
        既有控制线类型字典 = {}
        for 控制线x in 游标类.属性获取_数据_字典形式(游标, 操作字段名称):

            控制线预设字典列表 = [x for x in 控制线类型与名称映射 if x["类型名称"] == 控制线x[控制线类型字段名称]]
            if len(控制线预设字典列表) != 1:
                raise Exception("控制线类型与名称映射错误")
            else:
                控制线预设字典 = 控制线预设字典列表[0]

            if 控制线预设字典["图层名称"] not in 既有控制线类型字典:
                新建要素 = 要素类.要素创建_通过名称("内存临时", "线", 控制线要素)
                既有控制线类型字典[控制线预设字典["图层名称"]] = 新建要素
                # print(f"创建要素：{新建要素}")
                # print(f"既有控制线类型字典：{既有控制线类型字典}")

            分类型要素 = 既有控制线类型字典[控制线预设字典["图层名称"]]
            with 游标类.游标创建("插入", 分类型要素, 操作字段名称) as 游标_分类型:
                游标类.行插入_字典形式(游标_分类型, 控制线x, 操作字段名称)

    输出要素列表 = []
    for 图层名称, 临时名称 in 既有控制线类型字典.items():
        输出要素 = 要素类.要素创建_通过复制并重命名重名要素(临时名称, 图层名称 + 输出要素名称后缀)
        输出要素列表.append(输出要素)
    print(f"输出要素列表：{输出要素列表}")
    return 输出要素列表


if __name__ == "__main__":
    日志生成器.开启()
    # 工作空间 = r"C:\Users\common\Project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        道路_工具集_根据入库要素生成控制线(
            控制线要素名称="XG/XG_KZX",
            输出要素名称后缀="1",
        )
