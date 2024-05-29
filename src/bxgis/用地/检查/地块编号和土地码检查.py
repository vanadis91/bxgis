from bxpy.日志包 import 日志类
from bxpy.基本对象包 import 字类, 字典类, 表类
from typing import Union, Literal
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类, 字段类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息
from bxgis.常用 import 属性更新


def 检查地块编号和土地码是否有问题(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_检查地块编号"):
    日志类.临时关闭日志()
    if 输出要素名称 == "in_memory\\AA_检查地块编号":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()
    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    地块编号字段名称 = 基本信息.地块要素字段映射.地块编号字段名称
    街区编号字典 = {}
    地块编号缺失flag = False
    地块编号重复flag = False
    with 游标类.游标创建("查询", 用地要素, [地块编号字段名称, "_ID"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [地块编号字段名称, "_ID"]):
            if x[地块编号字段名称] in ["", " ", None]:
                地块编号缺失flag = True
                输入输出类.输出消息(f"ID为【{x['_ID']}】的地块，地块编号缺失")
                continue
            地块编号前半段, 地块编号后半段 = x[地块编号字段名称].split("-")
            街区编号字典.setdefault(地块编号前半段, [])
            if 地块编号后半段 not in 街区编号字典[地块编号前半段]:
                街区编号字典[地块编号前半段].append(地块编号后半段)
            else:
                地块编号重复flag = True
                输入输出类.输出消息(f"ID为【{x['_ID']}】的地块，地块编号重复，重复的编号是【{x[地块编号字段名称]}】")
    if not 地块编号缺失flag:
        输入输出类.输出消息(f"所有地块都有地块编号，没有地块缺失")
    if not 地块编号重复flag:
        输入输出类.输出消息(f"所有地块的地块编号都没有重复")
    地块编号不连续flag = False
    街区编号字典键值对列表 = 表类.排序(None, 街区编号字典.items())
    for k, v in 街区编号字典键值对列表:
        v = 表类.排序(None, v)
        日志类.输出调试(f"【{k}】区域的编号列表为：{v}")
        v = [vi for vi in v if vi.isdigit()]
        v = 表类.排序(lambda x: int(x), v)
        应得到的编号 = 1
        for 实际得到的编号 in v:
            whileFlag = 0
            while 字类.格式_补位(str(应得到的编号), 2) != 实际得到的编号 and whileFlag < 30:
                地块编号不连续flag = True
                输入输出类.输出消息(f"缺少地块编号{k}-{字类.格式_补位(str(应得到的编号), 2)}")
                应得到的编号 += 1
                whileFlag += 1
            if whileFlag == 30:
                raise Exception(f"编号检查似乎一直找不到正确的编号顺序")
            应得到的编号 += 1
    if not 地块编号不连续flag:
        输入输出类.输出消息(f"区域内的地块编号都是连续的")

    土地码字段名称 = 基本信息.地块要素字段映射.土地码字段名称
    地块编号字段名称 = 基本信息.地块要素字段映射.地块编号字段名称
    土地码列表 = []
    土地码缺失flag = False
    土地码重复flag = False
    from bxarcpy.几何包 import 几何类

    with 游标类.游标创建("查询", 用地要素, [土地码字段名称, 地块编号字段名称, "_ID"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [土地码字段名称, 地块编号字段名称, "_ID"]):
            if x[土地码字段名称] in ["", " ", None] and len(x[地块编号字段名称].split("-")[0]) == 8:
                土地码缺失flag = True
                输入输出类.输出消息(f"ID为【{x['_ID']}】的地块，土地码缺失")
                continue
            if x[土地码字段名称] not in 土地码列表 and x[土地码字段名称] != None:
                土地码列表.append(x[土地码字段名称])
            elif x[土地码字段名称] in 土地码列表:
                土地码重复flag = True
                输入输出类.输出消息(f"ID为【{x['_ID']}】的地块，土地码重复，重复的土地码是【{x[土地码字段名称]}】")
    if not 土地码缺失flag:
        输入输出类.输出消息(f"所有地块都有土地码，没有地块缺失")
    if not 土地码重复flag:
        输入输出类.输出消息(f"所有地块的土地码都没有重复")


if __name__ == "__main__":
    日志类.开启()
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        检查地块编号和土地码是否有问题(
            输入要素名称="DIST_用地规划图",
            输出要素名称="DIST_用地规划图",
        )
