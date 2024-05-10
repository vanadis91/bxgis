import bxarcpy
from bxpy.日志包 import 日志类
from bxgis import 配置
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 基本农田是否被占(输入要素名称="DIST_用地规划图", 基本农田要素名称="KZX_永久基本农田", 是否输出到CAD=True, 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_基本农田是否被占" + "_" + 工具包.生成短GUID()

    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    基本农田要素 = 要素类.要素创建_通过复制(基本农田要素名称)

    if 基本信息.控制线要素字段映射.控制线名称字段名称 not in 要素类.字段名称列表获取(基本农田要素):
        raise ValueError(f"{基本农田要素名称}中未包括{基本信息.控制线要素字段映射.控制线名称字段名称}字段。")
    基本农田要素 = 要素类.字段删除(基本农田要素, 保留字段名称列表=[基本信息.控制线要素字段映射.控制线名称字段名称])

    基本农田范围内用地 = 要素类.要素创建_通过相交([用地要素, 基本农田要素])

    基本农田范围内非农田 = 要素类.要素创建_通过筛选(基本农田范围内用地, f"{基本信息.地块要素字段映射.地类编号字段名称} NOT LIKE '01%'")
    if 要素类.属性获取_几何数量(基本农田范围内非农田) > 0:
        输入输出类.输出消息(f"基本农田范围内存在非农田用地")
        输出要素 = 要素类.要素创建_通过复制并重命名重名要素(基本农田范围内非农田, 输出要素名称)
        if 是否输出到CAD:
            要素类.转换_到CAD(基本农田范围内非农田, 基本信息.计算机信息.CAD输出目录 + "\\AA_基本农田范围内非农田.dwg")
        return 输出要素
    else:
        输入输出类.输出消息(f"基本农田范围内不存在非农田用地")
        return None


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        基本农田是否被占("DIST_用地规划图", "CZ_控制线_三线_基本农田_图界内")
