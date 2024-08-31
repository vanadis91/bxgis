# -*- coding: utf-8 -*-

from bxarcpy.要素包 import 要素类, 字段类
from bxarcpy.游标包 import 游标类
from bxpy.日志包 import 日志类
from bxpy.基本对象包 import 整类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxarcpy.几何包 import 几何类
from bxgis.配置 import 基本信息
import bxarcpy.工具包 as 工具包


def 根据街坊生成街区(
    地块要素路径="XG_GHDK",
    输出要素名称="内存临时",
):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_规划地块" + "_" + 工具包.生成短GUID()
    地块要素 = 要素类.要素创建_通过复制(地块要素路径)

    操作字段 = 要素类.字段名称列表获取(地块要素, 含系统字段=False)
    with 游标类.游标创建("更新", 地块要素, 操作字段) as 地块游标:
        for 地块数据x in 游标类.属性获取_数据_字典形式(地块游标, 操作字段):
            for k, v in 地块数据x.items():
                if isinstance(v, str):
                    地块数据x[k] = v.strip()
            游标类.行更新_字典形式(地块游标, 地块数据x, 操作字段)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(地块要素, 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    日志类.开启(级别列表过滤=["调试", "信息", "警告", "错误", "危险"])
    工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        根据街坊生成街区(
            地块要素路径="XG_GHDK",
            输出要素名称="XG_GHDK1",
        )
