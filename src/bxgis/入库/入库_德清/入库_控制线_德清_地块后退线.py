# -*- coding: utf-8 -*-

from typing import Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.日志包 import 日志生成器
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置.配置包 import 配置类

基本信息 = 配置类.项目信息对象获取()
from bxpy.基本对象包 import 浮类


def 入库_控制线_德清_地块后退线(
    多层后退线要素路径="KZX_后退线_多层",
    高层后退线要素路径="KZX_后退线_高层",
    入库要素模板="AC_RK_地块后退线",
    输出要素路径="AC_RK_地块后退线1",
):
    日志生成器.临时开启日志()
    多层控制线要素 = 要素类.要素创建_通过复制(多层后退线要素路径)
    高层控制线要素 = 要素类.要素创建_通过复制(高层后退线要素路径)
    入库要素 = 要素类.要素创建_通过复制(入库要素模板)

    with 游标类.游标创建("更新", 入库要素, ["_形状"]) as 游标:
        for 游标x in 游标类.属性获取_数据_字典形式(游标, ["_形状"]):
            游标类.行删除(游标)

    控制线要素需操作的字段名称列表 = ["_形状", "*"]
    入库要素需操作的字段名称列表 = ["_形状", "匹配字段", "LX", "HTJL"]
    with 游标类.游标创建("查询", 多层控制线要素, 控制线要素需操作的字段名称列表) as 游标_控制线_多层, 游标类.游标创建("查询", 高层控制线要素, 控制线要素需操作的字段名称列表) as 游标_控制线_高层, 游标类.游标创建("插入", 入库要素, 入库要素需操作的字段名称列表) as 游标_入库:
        for 控制线_多层x in 游标类.属性获取_数据_字典形式(游标_控制线_多层, 控制线要素需操作的字段名称列表):
            构造数据 = {}
            构造数据["_形状"] = 控制线_多层x["_形状"]
            构造数据["匹配字段"] = 控制线_多层x["控制线名称"]
            构造数据["LX"] = 控制线_多层x["控制线名称"].replace("后退线", "")
            构造数据["HTJL"] = 浮类.转换_到浮(控制线_多层x["自定义字段1"])

            游标类.行插入_字典形式(游标_入库, 构造数据, 入库要素需操作的字段名称列表)

        for 控制线_高层x in 游标类.属性获取_数据_字典形式(游标_控制线_高层, 控制线要素需操作的字段名称列表):
            构造数据 = {}
            构造数据["_形状"] = 控制线_高层x["_形状"]
            构造数据["匹配字段"] = 控制线_高层x["控制线名称"]
            构造数据["LX"] = 控制线_高层x["控制线名称"].replace("后退线", "")
            构造数据["HTJL"] = 浮类.转换_到浮(控制线_高层x["自定义字段1"])

            游标类.行插入_字典形式(游标_入库, 构造数据, 入库要素需操作的字段名称列表)

    输出要素路径 = 工具包.输出路径生成_当采用内存临时时([多层后退线要素路径, 高层后退线要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(入库要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    日志生成器.开启()
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        入库_控制线_德清_地块后退线(
            多层后退线要素路径="YD_TZ_后退界线_多层",
            高层后退线要素路径="YD_TZ_后退界线_高层",
            入库要素模板="AC_RK_地块后退线",
            输出要素路径="AC_RK_地块后退线1",
        )
