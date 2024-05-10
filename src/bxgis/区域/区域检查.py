# -*- coding: utf-8 -*-

from typing import Union
import bxarcpy
from bxpy.时间包 import 时间类
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 区域检查(区域要素名称, 范围检查要素名称: Union[str, None] = "JX_规划范围线", 拓扑检查=True):
    区域要素 = 要素类.要素创建_通过复制(区域要素名称)
    if 范围检查要素名称:
        要素类.拓扑检查范围(区域要素, 范围要素路径=范围检查要素名称)
    if 拓扑检查:
        要素类.拓扑检查重叠(区域要素)


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        区域检查("JX_街坊范围线", "JX_规划范围线", True)
