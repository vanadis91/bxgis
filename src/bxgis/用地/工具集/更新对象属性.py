# -*- coding: utf-8 -*-

from typing import Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.几何包 import 几何类
from bxpy.日志包 import 日志生成器
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置.配置包 import 配置类
基本信息 = 配置类.项目信息对象获取()


def 用地_工具集_更新对象属性(
    输入要素路径="XG_GHDK",
    属性所在要素路径="AA_户数指标",
    属性所在字段名称="Text",
    输出要素路径="内存临时",
):
    输出要素路径 = 工具包.输出路径生成_当采用内存临时时(["更新对象属性"]) if 输出要素路径 == "内存临时" else 输出要素路径

    输入要素 = 要素类.要素创建_通过复制(输入要素路径)
    属性所在要素 = 要素类.要素创建_通过复制(属性所在要素路径)

    操作字段名称列表1 = [*要素类.字段名称列表获取(输入要素), "_形状"]
    with 游标类.游标创建("更新", 输入要素, 操作字段名称列表1) as 游标_输入要素:
        操作字段名称列表2 = [属性所在字段名称, "_形状"]
        with 游标类.游标创建("查询", 属性所在要素, 操作字段名称列表2) as 游标_属性所在要素:
            for 输入要素x in 游标类.属性获取_数据_字典形式(游标_输入要素, 操作字段名称列表1):
                for 属性所在要素x in 游标类.属性获取_数据_字典形式(游标_属性所在要素, 操作字段名称列表2):
                    if 几何类.关系_包含(输入要素x["_形状"], 属性所在要素x["_形状"]):
                        键 = 属性所在要素x[属性所在字段名称].split(":")[0]
                        值 = 属性所在要素x[属性所在字段名称].split(":")[1]
                        输入要素x[键] = 值
                游标类.重置(游标_属性所在要素)
                游标类.行更新_字典形式(游标_输入要素, 输入要素x)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        用地_工具集_更新对象属性(
            输入要素路径="DIST_用地规划图",
            属性所在要素路径="AA_户数指标",
            属性所在字段名称="Text",
            输出要素路径="DIST_用地规划图1",
        )
