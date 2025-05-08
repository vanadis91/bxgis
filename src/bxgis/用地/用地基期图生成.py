# *-* coding:utf8 *-*
import bxarcpy
from bxpy.时间包 import 时间类
from bxpy.日志包 import 日志生成器
from bxgis import 配置
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.时间包 import 时间类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置.配置包 import 配置类

基本信息 = 配置类.项目信息对象获取()


@时间类.装饰器_运行时长
def 用地基期图生成(
    输入要素名称列表: list = [
        "YD_基期细化",
        "YD_农转用20年及以前",
    ],
    规划范围线要素名称="JX_规划范围线",
    是否拓扑检查=False,
    是否范围检查=False,
    是否曲线检查=True,
    输出要素名称: str = "DIST_用地基期图",
):
    if 是否拓扑检查:
        日志生成器.输出调试(f"开始拓扑检查")
        需要拓扑的要素名称列表 = [x for x in 输入要素名称列表]
        要素类.拓扑检查重叠_通过要素名称列表(需要拓扑的要素名称列表)
    if 是否曲线检查:
        需要曲线检查的要素名称列表 = [x for x in 输入要素名称列表]
        是否包含曲线flag = False
        for 要素x in 需要曲线检查的要素名称列表:
            with 游标类.游标创建("查询", 要素x, ["_形状"]) as 游标:
                for 游标x in 游标类.属性获取_数据_字典形式(游标, ["_形状"]):
                    if 几何类.是否包含曲线(游标x["_形状"]):
                        是否包含曲线flag = True
                        输入输出类.输出消息(f"【{要素x}】存在曲线，请增密后再继续。")
        if 是否包含曲线flag is False:
            输入输出类.输出消息(f"所有要素不存在曲线。")
        else:
            raise Exception("存在曲线，请增密后再继续。")
    from bxgis.用地.用地规划图生成 import _合并输入要素图层

    输出要素 = _合并输入要素图层(输入要素名称列表)

    from bxgis.用地.用地规划图生成 import _整理输出要素字段

    输出要素 = _整理输出要素字段(输出要素, 规划范围线要素名称, 输出要素名称)

    if 是否拓扑检查:
        日志生成器.输出调试(f"开始拓扑检查")
        需要拓扑的要素名称列表 = []
        需要拓扑的要素名称列表.append(输出要素)
        要素类.拓扑检查重叠_通过要素名称列表(需要拓扑的要素名称列表)

    if 是否范围检查:
        日志生成器.输出调试(f"开始范围检查")
        要素类.拓扑检查范围(输出要素, 规划范围线要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        用地基期图生成(
            输入要素名称列表=[
                "YD_基期",
                "DIST_用地基期图",
            ],
            规划范围线要素名称="JX_规划范围线",
            是否拓扑检查=True,
            是否范围检查=True,
            是否曲线检查=True,
            输出要素名称="DIST_用地基期图1",
        )
    # with 环境管理器类.环境管理器类创建(工作空间):
    #     用地基期图生成(
    #         输入要素名称列表=[
    #             "YD_基期细化",
    #             "YD_农转用20年及以前",
    #         ],
    #         规划范围线要素名称="JX_规划范围线",
    #         是否拓扑检查=True,
    #         是否范围检查=True,
    #         是否曲线检查=True,
    #         输出要素名称="DIST_用地基期图",
    #     )
