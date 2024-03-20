from bxpy.日志包 import 日志类
import arcpy
from .配置类 import 配置
from .要素类 import 要素类


class 拓扑类:
    _规则映射表 = {
        "Must Not Overlap (Area)": "Must Not Overlap (Area)",
        "面无重叠": "Must Not Overlap (Area)",
        "Must Not Have Gaps (Area)": "Must Not Have Gaps (Area)",
        "面无空隙": "Must Not Have Gaps (Area)",
        "Must Not Overlap (Line)": "Must Not Overlap (Line)",
        "线无重叠": "Must Not Overlap (Line)",
        "Must Not Self-Overlap (Line)": "Must Not Self-Overlap (Line)",
        "线无自重叠": "Must Not Self-Overlap (Line)",
    }

    def __init__(self, 内嵌对象=None, 名称=None) -> None:
        if 内嵌对象:
            self.名称 = 内嵌对象.名称
        elif 名称:
            self.名称 = 名称

    @staticmethod
    def 拓扑创建(要素数据集名称=None, 拓扑名称=None):
        return 拓扑类(名称=arcpy.management.CreateTopology(in_dataset=要素数据集名称, out_name=拓扑名称, in_cluster_tolerance=None)[0])

    def 拓扑中添加要素(self, 输入要素名称):
        arcpy.management.AddFeatureClassToTopology(in_topology=self.名称, in_featureclass=输入要素名称, xy_rank=1, z_rank=1)[0]
        return self

    def 拓扑中添加规则(self, 输入要素名称=None, 规则="面无重叠"):
        规则 = 拓扑类._规则映射表[规则]
        arcpy.management.AddRuleToTopology(in_topology=self.名称, rule_type=规则, in_featureclass=输入要素名称, subtype="", in_featureclass2="", subtype2="")[0]
        return self

    def 拓扑验证(self):
        arcpy.management.ValidateTopology(in_topology=self.名称, visible_extent="Full_Extent")[0]
        return self

    def 导出到要素(self, 输出要素名称="AA_拓扑导出后要素"):
        arcpy.management.ExportTopologyErrors(self.名称, 配置.当前工作空间, 输出要素名称)
        return (
            要素类(名称=输出要素名称 + "_point"),
            要素类(名称=输出要素名称 + "_line"),
            要素类(名称=输出要素名称 + "_poly"),
        )
