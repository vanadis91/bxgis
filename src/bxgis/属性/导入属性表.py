# *-* coding:utf8 *-*

from bxpy.日志包 import 日志生成器, 日志处理器
from bxpy.基本对象包 import 字类, 字典类
from typing import Union, Literal, Optional, List
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类, 字段类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息
from bxgis.常用 import 属性更新


def 导入属性表(
    输入要素路径="DIST_用地规划图",
    EXCEL文件路径=r"C:\Users\beixiao\Desktop\1-核对机动车位.xlsx",
    EXCEL文件中表格名称="sheet1",
    映射字段名称="实体GUID",
    需更新字段名称列表=["*"],
    需更新字段类型列表: List[Literal["字符串", "浮点数", "整数", "*"]] = ["*"],
    输出要素路径="内存临时",
):
    from bxpy.基本对象包 import 字典类

    输入要素 = 要素类.要素创建_通过复制(输入要素路径)

    需更新字段名称列表raw = None if "*" in 需更新字段名称列表 else 需更新字段名称列表
    需更新字段类型列表raw = None if "*" in 需更新字段类型列表 else 需更新字段类型列表

    类型映射 = {"字符串": str, "浮点数": float, "整数": int}
    if 需更新字段名称列表raw and 需更新字段类型列表raw:
        需更新字段类型列表raw = [类型映射.get(x, x) for x in 需更新字段类型列表raw]
        需更新字段类型列表raw = dict(zip(需更新字段名称列表raw, 需更新字段类型列表raw))

    更新的字典列表: list = 字典类.转换_从excel(excel路径=EXCEL文件路径, excel表名称=EXCEL文件中表格名称, 要读取的列=需更新字段名称列表raw, 指定数据类型=需更新字段类型列表raw)

    操作字段名称列表 = 要素类.字段名称列表获取(输入要素) if 需更新字段名称列表raw == None else 需更新字段名称列表raw
    with 游标类.游标创建("更新", 输入要素, 操作字段名称列表) as 游标:
        没有被更新的项列表 = []
        for 项x in 游标类.属性获取_数据_字典形式(游标, 操作字段名称列表):
            是否被更新flag = False
            for i, 更新字典x in enumerate(更新的字典列表):
                if 映射字段名称 == "实体GUID":
                    对比项1 = "-".join(项x[映射字段名称].split("-")[0:-1])
                    对比项2 = "-".join(更新字典x[映射字段名称].split("-")[0:-1])
                else:
                    对比项1 = 项x[映射字段名称]
                    对比项2 = 更新字典x[映射字段名称]
                if 对比项1 == 对比项2:
                    是否有变化flag = False
                    import copy

                    原始项 = copy.copy(项x)
                    for k, v in 更新字典x.items():
                        if 项x[k] != v and k != 映射字段名称:
                            项x[k] = v
                            是否有变化flag = True
                    if 是否有变化flag:
                        输入输出类.输出消息(f"{原始项}更新为{项x}")

                    游标类.行更新_字典形式(游标, 项x)
                    是否被更新flag = True
                    被利用项索引 = i
                    break
            if 是否被更新flag:
                更新的字典列表.pop(被利用项索引)
            else:
                没有被更新的项列表.append(项x)
    import json

    输入输出类.输出消息(f"要素中没有被更新的项共{len(没有被更新的项列表)}个：{json.dumps(没有被更新的项列表,ensure_ascii=False,indent=2)}")
    输入输出类.输出消息(f"表格中没有被使用的项共{len(更新的字典列表)}个：{json.dumps(更新的字典列表,ensure_ascii=False,indent=2)}")

    输出要素路径 = 工具包.输出路径生成_当采用内存临时时(["用地更新"]) if 输出要素路径 == "内存临时" else 输出要素路径
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        导入属性表(
            输入要素路径="DIST_用地规划图",
            EXCEL文件路径=r"C:\Users\beixiao\Desktop\1-核对机动车位.xlsx",
            EXCEL文件中表格名称=r"sheet1",
            映射字段名称="实体GUID",
            需更新字段名称列表=["实体GUID", "机动车位量", "机动车指标", "机动车公式"],
            需更新字段类型列表=["字符串", "字符串", "字符串", "字符串"],
            输出要素路径="DIST_用地规划图1",
        )
