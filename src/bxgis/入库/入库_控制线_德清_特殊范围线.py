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
from bxpy.基本对象包 import 浮类


def 入库_用途分区(
    控制线要素路径列表=["GZW_虚位控制绿地", "GZW_虚位控制道路", "GZW_用地功能引导"],
    入库要素模板="AC_RK_特殊范围线",
    输出要素路径="AC_RK_特殊范围线1",
):
    日志生成器.临时开启日志()
    入库要素 = 要素类.要素创建_通过复制(入库要素模板)
    with 游标类.游标创建("更新", 入库要素, ["_形状"]) as 游标:
        for 游标x in 游标类.属性获取_数据_字典形式(游标, ["_形状"]):
            游标类.行删除(游标)

    for 控制线x in 控制线要素路径列表:
        控制线要素 = 要素类.要素创建_通过复制(控制线x)
        控制线要素需操作的字段名称列表 = ["_形状", "*"]
        入库要素需操作的字段名称列表 = ["_形状", "匹配字段", "LX", "BZ"]
        with 游标类.游标创建("查询", 控制线要素, 控制线要素需操作的字段名称列表) as 游标_控制线, 游标类.游标创建("插入", 入库要素, 入库要素需操作的字段名称列表) as 游标_入库:
            for 控制线x in 游标类.属性获取_数据_字典形式(游标_控制线, 控制线要素需操作的字段名称列表):
                构造数据 = {}
                构造数据["_形状"] = 控制线x["_形状"]
                构造数据["匹配字段"] = 控制线x["控制线名称"]
                构造数据["LX"] = 控制线x["控制线名称"]
                构造数据["BZ"] = 控制线x["备注"]

                游标类.行插入_字典形式(游标_入库, 构造数据, 入库要素需操作的字段名称列表)

    输出要素路径 = 工具包.输出路径生成_当采用内存临时时(控制线要素路径列表) if 输出要素路径 == "内存临时" else 输出要素路径
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(入库要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    日志生成器.开启()
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        入库_用途分区(
            控制线要素路径列表=["GZW_虚位控制绿地", "GZW_虚位控制道路", "GZW_用地功能引导"],
            入库要素模板="AC_RK_特殊范围线",
            输出要素路径="AC_RK_特殊范围线1",
        )
