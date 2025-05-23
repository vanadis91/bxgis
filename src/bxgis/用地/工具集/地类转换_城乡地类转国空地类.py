# -*- coding: utf-8 -*-

from typing import Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.日志包 import 日志生成器, 日志处理器
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类

from bxgis.属性.属性对比 import 属性对比
from bxgis.配置.配置包 import 配置类

基本信息 = 配置类.项目信息对象获取()

def 地类转换_城乡地类转国空地类(
    输入要素路径="XG_GHDK",
    地类编号字段名称=基本信息.地块要素字段映射.地类编号字段名称,
    输出要素路径="内存临时",
):
    日志生成器.临时关闭日志()
    # 需要提前完成编号、耕地面积计算
    输出要素路径 = 工具包.临时路径生成(["城乡地类转国空地类"]) if 输出要素路径 == "内存临时" else 输出要素路径

    输入要素 = 要素类.要素创建_通过复制(输入要素路径)

    地类编号字段名称_城乡 = f"{地类编号字段名称}_城乡"
    要素类.字段修改(输入要素, 地类编号字段名称, 地类编号字段名称_城乡)
    要素类.字段添加_字符串(输入要素, 地类编号字段名称)

    地块指标测算表 = 基本信息.应用信息.地块指标测算表获取()
    操作字段名称列表 = [地类编号字段名称, 地类编号字段名称_城乡]
    错误提醒集合 = set()
    with 游标类.游标创建("更新", 输入要素, 操作字段名称列表) as 游标:
        for 项x in 游标类.属性获取_数据_字典形式(游标, 操作字段名称列表):
            try:
                地块指标测算字典 = [x for x in 地块指标测算表 if x["地块性质"] == 项x[地类编号字段名称_城乡]][0]
            except Exception as e:
                错误提醒集合.add(f"{项x[地类编号字段名称_城乡]}查找指标测算字典失败，{e}")
                地块指标测算字典 = {"国空地类映射": 项x[地类编号字段名称_城乡]}
            项x[地类编号字段名称] = 地块指标测算字典["国空地类映射"]
            游标类.行更新_字典形式(游标, 项x, 操作字段名称列表)
    if 错误提醒集合:
        输入输出类.输出消息(错误提醒集合)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素路径)
    属性对比(输入要素路径, 输出要素, ["_ID", "_ID"], 对比字段名称列表=[[地类编号字段名称, 地类编号字段名称]])
    return 输出要素


if __name__ == "__main__":
    日志生成器.关闭()
    日志处理器.输出器_文件对象_路径 = r"C:\Users\beixiao\Desktop\01.txt"
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\Common\Project\S申花单元医院西侧商改居地块\S申花单元医院西侧商改居地块_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        地类转换_城乡地类转国空地类(
            输入要素路径="DIST_用地规划图",
            地类编号字段名称="dldm",
            输出要素路径="DIST_用地规划图1",
        )
