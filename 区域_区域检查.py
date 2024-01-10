# -*- coding: utf-8 -*-

import bxarcpy
from bxpy import 时间


def 区域检查(区域要素名称, 范围要素名称):
    区域要素 = bxarcpy.要素类.要素读取_通过名称(区域要素名称).要素创建_通过复制()
    区域要素.拓扑检查范围(范围要素名称=范围要素名称)


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        区域检查("JX_街坊范围线", "JX_规划范围线")
