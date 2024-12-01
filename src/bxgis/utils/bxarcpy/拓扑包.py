from bxpy.日志包 import 日志生成器
import arcpy
from bxarcpy.要素包 import 要素类

_规则映射表 = {
    "面无重叠": "Must Not Overlap (Area)",
    "面无空隙": "Must Not Have Gaps (Area)",
    "线无重叠": "Must Not Overlap (Line)",
    "线无自重叠": "Must Not Self-Overlap (Line)",
}


class 拓扑类:
    # def __init__(self, 内嵌对象=None, 名称=None) -> None:
    #     if 内嵌对象:
    #         self.名称 = 内嵌对象.名称
    #     elif 名称:
    #         self.名称 = 名称

    @staticmethod
    def 拓扑创建(要素数据集名称=None, 拓扑名称=None, 拓扑容差=0.0001):
        拓扑名称 = arcpy.management.CreateTopology(in_dataset=要素数据集名称, out_name=拓扑名称, in_cluster_tolerance=拓扑容差)[0]  # type: ignore
        return 拓扑名称

    @staticmethod
    def 拓扑中添加要素(拓扑名称, 输入要素名称):
        arcpy.management.AddFeatureClassToTopology(in_topology=拓扑名称, in_featureclass=输入要素名称, xy_rank=1, z_rank=1)[0]  # type: ignore

        return 拓扑名称

    @staticmethod
    def 拓扑中添加规则(拓扑名称, 输入要素名称=None, 规则="面无重叠"):
        规则 = _规则映射表[规则] if 规则 in _规则映射表 else 规则
        arcpy.management.AddRuleToTopology(in_topology=拓扑名称, rule_type=规则, in_featureclass=输入要素名称, subtype="", in_featureclass2="", subtype2="")[0]  # type: ignore

        return 拓扑名称

    @staticmethod
    def 拓扑验证(拓扑名称):
        arcpy.management.ValidateTopology(in_topology=拓扑名称, visible_extent="Full_Extent")[0]  # type: ignore
        return 拓扑名称

    @staticmethod
    def 转换_到要素(拓扑名称, 输出要素名称="AA_拓扑导出后要素"):
        from bxarcpy.环境包 import 环境类

        arcpy.management.ExportTopologyErrors(拓扑名称, 环境类.属性获取_当前工作空间(), 输出要素名称)  # type: ignore

        return (
            输出要素名称 + "_point",
            输出要素名称 + "_line",
            输出要素名称 + "_poly",
        )
