# -*- coding: utf-8 -*-

import bxarcpy
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 开发边界内工业用地(
    输入要素名称="DIST_用地规划图",
    控制线_城镇开发边界="KZX_城镇开发边界",
    输出要素名称="AA_开发边界内工业用地",
):
    用地规划图 = 要素类.要素创建_通过复制(输入要素名称)
    相交后 = 要素类.要素创建_通过相交([用地规划图, 控制线_城镇开发边界])
    输出要素 = 要素类.要素创建_通过筛选(相交后, "地类编号 LIKE '%1001%'")
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输出要素, 输出要素名称)


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        开发边界内工业用地(
            输入要素名称="DIST_用地规划图",
            控制线_城镇开发边界="KZX_城镇开发边界",
            输出要素名称="AA_开发边界内工业用地",
        )
