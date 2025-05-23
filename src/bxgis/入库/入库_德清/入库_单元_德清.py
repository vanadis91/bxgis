# -*- coding: utf-8 -*-

import bxarcpy
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


def 入库_单元_德清(
    单元要素路径="JX_规划范围线",
    入库要素模板="AC_RK_控规单元",
    输出要素路径="AC_RK_控规单元1",
):
    from bxpy.基本对象包 import 浮类, 字类, 整类, 字典类, 表类
    from bxpy.路径包 import 路径类

    单元要素 = 要素类.要素创建_通过复制(单元要素路径)
    入库要素 = 要素类.要素创建_通过复制(入库要素模板)

    with 游标类.游标创建("更新", 入库要素, ["_形状"]) as 游标:
        for 游标x in 游标类.属性获取_数据_字典形式(游标, ["_形状"]):
            游标类.行删除(游标)

    信息文件路径 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_信息.json"
    if not 路径类.是否存在(信息文件路径):
        路径类.新增文件(信息文件路径)
    信息json = 字典类.转换_从文件(信息文件路径)

    单元要素需操作的字段名称列表 = ["_形状", "_面积", "*"]
    入库要素需操作的字段名称列表 = ["_形状", "DYBH", "DYMC", "BZ", "DYMJ", "GHFWMJ", "PZWH", "PZSJ", "匹配字段", "LSPZWH", "JZYD", "GGGLFWYD", "SYFWYSSYD", "GYYD", "WLCCYD", "DLJTSSYD", "LVYGCYD", "GYSSYD", "JSYD", "FJSYD", "风景游赏用地", "游览设施用地", "交通与工程用地", "林地", "园地", "水域", "居民社会用地", "滞留用地", "ZJRK", "PJRJL", "JZRL", "RKSJ"]
    with 游标类.游标创建("查询", 单元要素, 单元要素需操作的字段名称列表) as 游标_地块, 游标类.游标创建("插入", 入库要素, 入库要素需操作的字段名称列表) as 游标_入库:
        for 单元x in 游标类.属性获取_数据_字典形式(游标_地块, 单元要素需操作的字段名称列表):
            构造数据 = {}
            构造数据["_形状"] = 单元x["_形状"]

            构造数据["DYBH"] = "330521-40"
            构造数据["DYMC"] = "德清县洛舍镇杨树湾单元（ZX-40）详细规划"
            构造数据["BZ"] = None
            构造数据["DYMJ"] = 浮类.转换_到浮(单元x["_面积"]) * 0.0001
            构造数据["GHFWMJ"] = 浮类.转换_到浮(单元x["_面积"]) * 0.000001
            构造数据["PZWH"] = "德政函〔2024〕113号"
            构造数据["PZSJ"] = "2024/12/11"
            构造数据["匹配字段"] = "控规单元"
            构造数据["LSPZWH"] = None  # 历史批复文号

            构造数据["JZYD"] = f'{信息json["技术指标"]["统计数据"]["居住用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["居住用地_比例_占总"]:.2f}%）'  # 居住用地
            构造数据["GGGLFWYD"] = f'{信息json["技术指标"]["统计数据"]["公共管理与公共服务用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["公共管理与公共服务用地_比例_占总"]:.2f}%）'  # 公共管理服务用地
            构造数据["SYFWYSSYD"] = f'{信息json["技术指标"]["统计数据"]["商业服务业用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["商业服务业用地_比例_占总"]:.2f}%）'  # 商业服务业用地
            构造数据["GYYD"] = f'{信息json["技术指标"]["统计数据"]["工矿用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["工矿用地_比例_占总"]:.2f}%）'  # 工业用地
            构造数据["WLCCYD"] = f'{信息json["技术指标"]["统计数据"]["仓储用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["仓储用地_比例_占总"]:.2f}%）'  # 仓储用地
            构造数据["DLJTSSYD"] = f'{信息json["技术指标"]["统计数据"]["交通运输用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["交通运输用地_比例_占总"]:.2f}%）'  # 交通运输用地
            构造数据["LVYGCYD"] = f'{信息json["技术指标"]["统计数据"]["绿地与开敞空间用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["绿地与开敞空间用地_比例_占总"]:.2f}%）'  # 绿地与开敞空间用地
            构造数据["GYSSYD"] = f'{信息json["技术指标"]["统计数据"]["公用设施用地"] * 0.0001:.2f}公顷（{信息json["技术指标"]["统计数据比例"]["公用设施用地_比例_占总"]:.2f}%）'  # 公用设施用地
            构造数据["JSYD"] = f'{信息json["技术指标"]["统计数据"]["建设用地面积"] * 0.0001:.2f}公顷'  # 建设用地面积
            构造数据["FJSYD"] = f'{信息json["技术指标"]["统计数据"]["非建设用地面积"] * 0.0001:.2f}公顷'  # 非建设用地面积
            构造数据["风景游赏用地"] = None
            构造数据["游览设施用地"] = None
            构造数据["交通与工程用地"] = None
            构造数据["林地"] = None
            构造数据["园地"] = None
            构造数据["水域"] = None
            构造数据["居民社会用地"] = None
            构造数据["滞留用地"] = None
            构造数据["ZJRK"] = f'{信息json["技术指标"]["区域统计数据"]["330521-40"]["总居住人数"]:.0f}'
            构造数据["PJRJL"] = f"{1.9:.1f}"
            构造数据["JZRL"] = f'{信息json["技术指标"]["区域统计数据"]["330521-40"]["总建筑面积"]:.0f}'
            构造数据["RKSJ"] = None  # 入库时间

            游标类.行插入_字典形式(游标_入库, 构造数据, 入库要素需操作的字段名称列表)

    输出要素路径 = 工具包.输出路径生成_当采用内存临时时([单元要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(入库要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    日志生成器.开启()
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        入库_单元_德清(
            单元要素路径="JX_规划范围线",
            入库要素模板="AC_RK_控规单元",
            输出要素路径="AC_RK_控规单元1",
        )
