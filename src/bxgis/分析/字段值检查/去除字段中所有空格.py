# -*- coding: utf-8 -*-

from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxpy.日志包 import 日志生成器
from bxarcpy.环境包 import 环境管理器类
import bxarcpy.工具包 as 工具包


def 去除字段中所有空格(
    地块要素路径="XG_GHDK",
    去除字段值中前后的空格=True,
    去除字段值内的空格=True,
    输出要素路径="内存临时",
):
    日志生成器.临时开启日志()
    输出要素路径 = 工具包.输出路径生成_当采用内存临时时([输出要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径
    日志生成器.输出调试(f"输出要素路径 {输出要素路径}")

    地块要素 = 要素类.要素创建_通过复制(地块要素路径)

    操作字段 = 要素类.字段名称列表获取(地块要素, 含系统字段=False)
    操作字段.append("_ID")
    with 游标类.游标创建("更新", 地块要素, 操作字段) as 地块游标:
        for 地块数据x in 游标类.属性获取_数据_字典形式(地块游标, 操作字段):
            for k, v in 地块数据x.items():
                from bxpy.基本对象包 import 基本对象类

                修改后的v = 基本对象类.深拷贝(v)
                if isinstance(v, str) and 去除字段值中前后的空格:
                    修改后的v = v.strip()
                if isinstance(v, str) and 去除字段值内的空格:
                    修改后的v = 修改后的v.replace(" ", "")
                if 修改后的v != v:
                    日志生成器.输出调试(f'ID {地块数据x["_ID"]} 的 {k} 字段值 "{v}" 修改为 "{修改后的v}"')
                地块数据x[k] = 修改后的v
            游标类.行更新_字典形式(地块游标, 地块数据x, 操作字段)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(地块要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":

    工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\受降北_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        去除字段中所有空格(
            地块要素路径="XG/XG_KZX",
            去除字段值中前后的空格=True,
            去除字段值内的空格=True,
            输出要素路径="XG/XG_KZX1",
        )
