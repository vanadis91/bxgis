from bxpy.日志包 import 日志类
from bxpy.时间包 import 时间类

try:
    import arcpy
except Exception as e:
    pass
import time
from . import 常量, 工具集
from typing import Union, Literal


class 要素类:
    def __init__(self, 内嵌对象=None, 名称: Union[str, None] = None):
        # 日志类.输出控制台(名称)
        if type(内嵌对象) is 要素类:
            self.名称 = 内嵌对象.名称
            self.名称_无路径 = 内嵌对象.名称_无路径
        elif type(名称) is str:
            self.名称 = 名称
            if 名称[-1] == "\\":
                self.名称_无路径 = 名称.split("\\")[-2]
            else:
                self.名称_无路径 = 名称.split("\\")[-1]
            # 日志类.输出控制台(self.名称)
            # 日志类.输出控制台(self.名称_无路径)
        else:
            from . import 环境

            环境.输出消息(f"无法将该对象转换为要素类：内嵌对象：{内嵌对象} 名称：{名称}")

    def __repr__(self) -> str:
        return f"<bxarcpy.要素类 对象 {{名称:{self.名称}, 名称_无路径:{self.名称_无路径}}}>"

    @property
    def 几何类型(self):
        from . import 常量

        几何类型 = arcpy.Describe(self.名称).shapeType  # type: ignore
        return 常量._要素类型反映射[几何类型.upper()]

    @property
    def 几何数量(self):
        结果 = arcpy.GetCount_management(self.名称)
        数量 = int(结果.getOutput(0))  # type: ignore
        return 数量

    @staticmethod
    def 要素读取_通过名称(名称):
        return 要素类(名称=名称)

    @staticmethod
    def 要素创建_通过名称(要素名称="AA_新建", 要素类型="面", 模板=None, 数据库路径="in_memory"):
        from .配置类 import 配置
        from . import 常量

        if 要素名称 == "AA_新建":
            要素名称 = 要素名称 + "_" + 工具集.生成短GUID()
        if 数据库路径 is None:
            数据库路径 = 配置.当前工作空间
        elif 数据库路径.upper() in ["内存临时", "临时", "IN_MEMORY", "MEMORY"]:
            数据库路径 = "in_memory"
        要素类型 = 常量._要素类型映射[要素类型]
        arcpy.management.CreateFeatureclass(out_path=数据库路径, out_name=要素名称, geometry_type=要素类型, template=模板, has_m="DISABLED", has_z="DISABLED", spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-495395959010.755 -495395959010.755 9090.90909090909;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision', config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0, out_alias="")  # type: ignore
        ret = 要素类.要素读取_通过名称(名称=数据库路径 + "\\" + 要素名称)
        # if 数据库路径.upper() in ["临时", "IN_MEMORY", "MEMORY"]:
        #     ret = ret.要素创建_通过复制并重命名重名要素(f"in_memory\\{要素名称}")
        return ret

    def 要素创建_通过复制(self, 输出要素名称="内存临时"):
        if 输出要素名称 == "内存临时":
            # 日志类.输出控制台(self)
            # 日志类.输出控制台(self.名称)
            # 日志类.输出控制台(self.名称_无路径)
            输出要素名称 = "in_memory\\AA_" + self.名称_无路径 + "_" + 工具集.生成短GUID()
        try:
            arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        except:
            arcpy.management.CopyFeatures(in_features=self.名称_无路径, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过复制并重命名重名要素(self, 输出要素名称="内存临时", 重名要素后缀=""):
        from .数据库类 import 数据库类
        from .配置类 import 配置
        from .环境 import 环境

        if 输出要素名称 == "内存临时":
            输出要素名称 = "in_memory\\AA_" + self.名称_无路径 + "_" + 工具集.生成短GUID()
        database = 数据库类.数据库读取_通过路径(配置.当前工作空间)
        要素名称列表 = database.要素名称列表获取()
        if 输出要素名称 in 要素名称列表:
            时间类.等待(1)
            重命名后名称 = 输出要素名称 + "_" + 工具集.生成当前时间()
            if 重名要素后缀 != "":
                重命名后名称 = 重命名后名称 + "_" + 重名要素后缀
            try:
                要素类.要素读取_通过名称(输出要素名称).要素创建_通过复制(重命名后名称)
                环境.输出消息(f"将重名要素复制为：{重命名后名称}")
            except Exception as e:
                环境.输出消息(f"找到重名要素但是重命名失败")
            # try:
            #     要素类.要素读取_通过名称(输出要素名称).要素删除()
            #     环境.输出消息(f"将重名要素 {self.名称} 删除")
            # except Exception as e:
            #     环境.输出消息(f"重名要素删除失败")
        try:
            要素类.要素读取_通过名称(输出要素名称).要素删除()
            要素类.要素读取_通过名称(self.名称).要素创建_通过复制(输出要素名称)
            # arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        except Exception as e:
            from .环境 import 环境

            时间类.等待(1)
            输出要素名称 = 输出要素名称 + "_new"

            环境.输出消息(f"覆盖失败，输出要素被重命名为：{输出要素名称}")
            要素类.要素读取_通过名称(self.名称).要素创建_通过复制(输出要素名称)
            # arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore

        return 要素类(名称=输出要素名称)

    def 要素创建_通过合并(self, 输入要素名称列表=[], 输出要素名称="in_memory\\AA_合并"):
        _输入要素路径列表 = [self.名称]
        _输入要素路径列表.extend(输入要素名称列表)
        if 输出要素名称 == "in_memory\\AA_合并":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.management.Merge(inputs=_输入要素路径列表, output=输出要素名称, field_mappings="", add_source="NO_SOURCE_INFO")  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过裁剪(self, 裁剪要素名称, 输出要素名称="in_memory\\AA_裁剪"):
        if 输出要素名称 == "in_memory\\AA_裁剪":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.analysis.Clip(in_features=self.名称, clip_features=裁剪要素名称, out_feature_class=输出要素名称, cluster_tolerance="")  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过擦除(self, 擦除要素名称, 输出要素名称="in_memory\\AA_擦除"):
        if 输出要素名称 == "in_memory\\AA_擦除":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.analysis.Erase(in_features=self.名称, erase_features=擦除要素名称, out_feature_class=输出要素名称, cluster_tolerance="")  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过擦除并几何修复(self, 擦除要素名称, 输出要素名称="in_memory\\AA_擦除并几何修复"):
        if 输出要素名称 == "in_memory\\AA_擦除并几何修复":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        输入 = self.要素几何修复()
        擦除 = 要素类.要素读取_通过名称(擦除要素名称).要素几何修复()
        arcpy.analysis.Erase(in_features=输入.名称, erase_features=擦除.名称, out_feature_class=输出要素名称, cluster_tolerance="")  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过相交(self, 输入要素名称列表=[], 输出字段设置: Literal["所有", "除FID外所有字段", "仅FID字段", "仅第一个要素字段"] = "所有", 输出要素路径="内存临时"):
        if 输出要素路径 == "内存临时":
            输出要素路径 = "in_memory\\AA_相交" + "_" + 工具集.生成短GUID()
        _输出字段设施映射 = {"所有": "ALL", "除FID外所有字段": "NO_FID", "仅FID字段": "ONLY_FID"}
        字段设置raw = _输出字段设施映射[输出字段设置] if 输出字段设置 in _输出字段设施映射 else 输出字段设置
        _输入要素路径列表 = [self.名称]
        _输入要素路径列表.extend(输入要素名称列表)
        _输入要素路径列表 = [[x, ""] for x in _输入要素路径列表]
        if 输出字段设置 == "仅第一个要素字段":
            第一个要素字段名称列表 = self.字段名称列表获取()
            字段设置raw = "ONLY_FID"
        arcpy.analysis.Intersect(in_features=_输入要素路径列表, out_feature_class=输出要素路径, join_attributes=字段设置raw, cluster_tolerance="", output_type="INPUT")  # type: ignore
        输出要素 = 要素类(名称=输出要素路径)
        if 输出字段设置 == "仅第一个要素字段":
            输出要素.字段删除(保留字段名称列表=第一个要素字段名称列表)
        return 输出要素

    def 要素创建_通过联合(self, 输入要素名称列表=[], 是否保留周长和面积=False, 输出要素名称="in_memory\\AA_联合", 是否保留FID=True):
        _输入要素名称列表 = [self.名称]
        _输入要素名称列表.extend(输入要素名称列表)
        if 输出要素名称 == "in_memory\\AA_联合":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        _输入要素名称列表_格式化 = [[x, ""] for x in _输入要素名称列表]
        arcpy.analysis.Union(in_features=_输入要素名称列表_格式化, out_feature_class=输出要素名称, join_attributes="ALL", cluster_tolerance=None, gaps="GAPS")  # type: ignore
        联合后要素 = 要素类(名称=输出要素名称)
        if 是否保留周长和面积 is False:
            字段名称列表 = 联合后要素.字段名称列表获取()
            for 字段名称 in 字段名称列表:
                if "Shape_Length" in 字段名称 or "Shape_Area" in 字段名称:
                    联合后要素.字段删除([字段名称])
        if 是否保留FID is False:
            带FID要素名称列表 = [("FID_" + x.split("\\")[-1]) for x in _输入要素名称列表]
            # 日志类.输出控制台(带FID要素名称列表)
            字段名称列表 = 联合后要素.字段名称列表获取()
            for 字段名称 in 字段名称列表:
                # 日志类.输出控制台(字段名称)
                if 字段名称 in 带FID要素名称列表:
                    联合后要素.字段删除([字段名称])
        return 联合后要素

    def 要素创建_通过联合并赋值字段(self, 区域要素名称="JX_街区范围线", 字段映射列表=[["所属街区", "街区编号"]], 是否检查两者差异=True, 差异是否输出到CAD=False, 输出要素名称="in_memory\\AA_联合并赋值字段"):
        if 输出要素名称 == "in_memory\\AA_联合并赋值字段":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        输入要素 = 要素类.要素读取_通过名称(self.名称)
        输入要素原始无路径名称 = 输入要素.名称_无路径
        输入要素 = 输入要素.要素创建_通过复制()

        区域要素 = 要素类.要素读取_通过名称(区域要素名称)
        区域要素原始无路径名称 = 区域要素.名称_无路径

        区域要素中保留的字段列表 = [x[1] for x in 字段映射列表]

        区域要素 = 区域要素.要素创建_通过复制().字段删除(保留字段名称列表=区域要素中保留的字段列表)
        输入要素 = 输入要素.字段删除(区域要素中保留的字段列表)

        联合后要素 = 输入要素.要素创建_通过联合([区域要素.名称]).要素创建_通过多部件至单部件()

        if 是否检查两者差异:
            应填色但是没填的区域要素 = 要素类.要素创建_通过名称(模板=联合后要素.名称)
            时间类.等待(1)
            不应填色但是填色的区域要素 = 要素类.要素创建_通过名称(模板=联合后要素.名称)
            时间类.等待(1)
            被范围线分割的要素 = 要素类.要素创建_通过名称(模板=联合后要素.名称)
            时间类.等待(1)
            联合后要素字段列表 = 联合后要素.字段名称列表获取(含系统字段=False)
            # print(字段列表)
            # for x in 联合后要素字段列表:
            #     if x in ["OBJECTID", "Shape", "Shape_Length", "Shape_Area"]:
            #         联合后要素字段列表.remove(x)

            联合后要素字段列表.insert(0, "_形状")

            元素FID列表 = []
            元素属性列表 = []
            分割要素已插入列表 = []
            from .游标类 import 游标类
            from .环境 import 环境

            with 游标类.游标创建_通过名称("查找", 联合后要素.名称, 联合后要素字段列表) as 联合后要素游标:
                with 游标类.游标创建_通过名称("插入", 应填色但是没填的区域要素.名称, 联合后要素字段列表) as 应填色但是没填的区域要素游标:
                    with 游标类.游标创建_通过名称("插入", 不应填色但是填色的区域要素.名称, 联合后要素字段列表) as 不应填色但是填色的区域要素游标:
                        with 游标类.游标创建_通过名称("插入", 被范围线分割的要素.名称, 联合后要素字段列表) as 被范围线分割的要素游标:
                            for x in 联合后要素游标:
                                if x[f"FID_{输入要素.名称_无路径}"] == -1:
                                    应填色但是没填的区域要素游标.行插入(x)
                                if x[f"FID_{区域要素.名称_无路径}"] == -1:
                                    不应填色但是填色的区域要素游标.行插入(x)
                                if x[f"FID_{输入要素.名称_无路径}"] in 元素FID列表 and x[f"FID_{输入要素.名称_无路径}"] != -1:
                                    环境.输出消息(f'这个图元被分割了，FID_{输入要素.名称_无路径}是：{x[f"FID_{输入要素.名称_无路径}"]}')
                                    if x[f"FID_{输入要素.名称_无路径}"] in 分割要素已插入列表:
                                        被范围线分割的要素游标.行插入(x)
                                    else:
                                        被范围线分割的要素游标.行插入(x)
                                        被范围线分割的要素游标.行插入(元素属性列表[元素FID列表.index(x[f"FID_{输入要素.名称_无路径}"])])
                                        分割要素已插入列表.append(x[f"FID_{输入要素.名称_无路径}"])
                                元素FID列表.append(x[f"FID_{输入要素.名称_无路径}"])
                                元素属性列表.append(x)
            if 应填色但是没填的区域要素.几何数量 > 0:
                环境.输出消息(f"存在空隙（需填未填）_{输入要素原始无路径名称}_{区域要素原始无路径名称}")
                应填色但是没填的区域要素.要素创建_通过复制并重命名重名要素(f"AA_空隙_{输入要素原始无路径名称}_{区域要素原始无路径名称}")
                if 差异是否输出到CAD:
                    应填色但是没填的区域要素.导出到CAD(rf"AA_空隙_{输入要素原始无路径名称}_{区域要素原始无路径名称}.dwg")

            if 不应填色但是填色的区域要素.几何数量 > 0:
                环境.输出消息(f"存在多余（不需填但被填）_{输入要素原始无路径名称}_{区域要素原始无路径名称}")
                不应填色但是填色的区域要素.要素创建_通过复制并重命名重名要素(f"AA_多余_{输入要素原始无路径名称}_{区域要素原始无路径名称}")
                if 差异是否输出到CAD:
                    不应填色但是填色的区域要素.导出到CAD(rf"AA_多余_{输入要素原始无路径名称}_{区域要素原始无路径名称}.dwg")

            if 被范围线分割的要素.几何数量 > 0:
                环境.输出消息(f"几何对象被分割_{输入要素原始无路径名称}_{区域要素原始无路径名称}")
                被范围线分割的要素.要素创建_通过复制并重命名重名要素(f"AA_被分割_{输入要素原始无路径名称}_{区域要素原始无路径名称}")
                if 差异是否输出到CAD:
                    被范围线分割的要素.导出到CAD(rf"\AA_被分割_{输入要素原始无路径名称}_{区域要素原始无路径名称}.dwg")

        for x in 字段映射列表:
            联合后要素.字段添加(x[0]).字段计算(x[0], f"!{x[1]}!")

        需要删除的字段列表 = [f"FID_{输入要素.名称_无路径}", f"FID_{区域要素.名称_无路径}", "ORIG_FID"]
        需要删除的字段列表.extend([x[1] for x in 字段映射列表])
        输出要素 = 联合后要素.字段删除(需要删除的字段列表).要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    def 要素创建_通过融合(self, 融合字段列表=[], 统计字段列表=None, 是否单部件=True, 输出要素名称="内存临时"):
        if 输出要素名称 == "内存临时":
            输出要素名称 = "in_memory\\AA_融合" + "_" + 工具集.生成短GUID()
        if 是否单部件 == True:
            是否单部件 = "SINGLE_PART"
        else:
            是否单部件 = "MULTI_PART"
        arcpy.management.Dissolve(in_features=self.名称, out_feature_class=输出要素名称, dissolve_field=融合字段列表, statistics_fields=统计字段列表, multi_part=是否单部件, unsplit_lines="DISSOLVE_LINES", concatenation_separator="")  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过更新(self, 更新要素名称, 输出要素名称="in_memory\\AA_更新"):
        if 输出要素名称 == "in_memory\\AA_更新":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.analysis.Update(self.名称, 更新要素名称, 输出要素名称)  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过更新并合并字段(self, 更新要素名称, 输出要素名称="in_memory\\AA_更新并合并字段"):
        if 输出要素名称 == "in_memory\\AA_更新并合并字段":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        输出 = self.要素创建_通过擦除(更新要素名称)
        输出 = 输出.要素创建_通过合并([更新要素名称], 输出要素名称)
        return 输出

    def 要素创建_通过筛选(self, SQL语句="", 输出要素名称="in_memory\\AA_筛选"):
        if 输出要素名称 == "in_memory\\AA_筛选":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.analysis.Select(in_features=self.名称, out_feature_class=输出要素名称, where_clause=SQL语句)  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过排序(self, 排序字段及顺序列表=[["DATE_REP", "ASCENDING"]], 空间排序方式="UR", 输出要素名称="in_memory\\AA_排序"):
        if 输出要素名称 == "in_memory\\AA_排序":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        排序字段及顺序列表temp = []
        for x in 排序字段及顺序列表:
            if x[1] == "ASCENDING" or x[1] == "正序":
                排序字段及顺序列表temp.append([x[0], "ASCENDING"])
            elif x[1] == "DESCENDING" or x[1] == "倒序":
                排序字段及顺序列表temp.append([x[0], "DESCENDING"])
        排序字段及顺序列表 = 排序字段及顺序列表temp
        arcpy.management.Sort(in_dataset=self.名称, out_dataset=输出要素名称, sort_field=排序字段及顺序列表, spatial_sort_method=空间排序方式)  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过多部件至单部件(self, 输出要素名称="in_memory\\AA_多部件至单部件"):
        if 输出要素名称 == "in_memory\\AA_多部件至单部件":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        try:
            arcpy.management.MultipartToSinglepart(in_features=self.名称, out_feature_class=输出要素名称)  # type: ignore
        except Exception as e:
            self.要素几何修复()
            print("错误：多部件至单部件出错")
            arcpy.management.MultipartToSinglepart(in_features=self.名称, out_feature_class=输出要素名称)  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过空间连接(self, 连接要素名称, 连接方式: Literal["相交", "包含连接要素", "完全包含连接要素", "在连接要素内", "完全在连接要素内", "包含连接要素内点", "内点在连接要素内", "形心在连接要素内", "大部分在连接要素内"] = "包含连接要素", 输出要素名称="内存临时") -> "要素类":
        _连接方式映射表 = {"相交": "INTERSECT", "包含连接要素": "CONTAINS", "完全包含连接要素": "COMPLETELY_CONTAINS", "在连接要素内": "WITHIN", "完全在连接要素内": "COMPLETELY_WITHIN", "形心在连接要素内": "HAVE_THEIR_CENTER_IN", "大部分在连接要素内": "LARGEST_OVERLAP"}
        连接方式raw = _连接方式映射表[连接方式] if 连接方式 in _连接方式映射表 else 连接方式

        if 输出要素名称 == "内存临时":
            输出要素名称 = "in_memory\\AA_空间连接" + "_" + 工具集.生成短GUID()

        if 连接方式raw == "包含连接要素内点":
            arcpy.management.RepairGeometry(in_features=连接要素名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]  # type: ignore
            连接要素 = 要素类.要素读取_通过名称(连接要素名称)
            连接要素转点后要素 = 连接要素.要素创建_通过转点()
            # 连接要素转内点后名称 = arcpy.management.FeatureToPoint(in_features=连接要素名称, out_feature_class="in_memory\\AA_要素转点" + "_" + 工具集.生成SUUID(), point_location="INSIDE")
            return self.要素创建_通过空间连接(连接要素转点后要素.名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
        if 连接方式raw == "内点在连接要素内":
            arcpy.management.RepairGeometry(in_features=self.名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]  # type: ignore
            目标要素 = self.要素创建_通过复制()
            目标要素转点后要素 = 目标要素.要素创建_通过转点()

            # 日志类.输出控制台(f"目标要素转点后要素字段列表{目标要素转点后要素.字段名称列表获取()}")
            # 日志类.输出控制台(f"目标要素名称{目标要素.名称_无路径}")

            连接要素 = 要素类.要素读取_通过名称(连接要素名称)

            目标要素转点后带连接要素字段 = 目标要素转点后要素.要素创建_通过空间连接(连接要素.名称, "在连接要素内")

            保留字段名称列表raw = 连接要素.字段名称列表获取(含系统字段=False)
            保留字段名称列表raw.append("FID_" + 目标要素.名称_无路径)
            目标要素转点后带连接要素字段.字段删除(保留字段名称列表=保留字段名称列表raw)

            连接要素字段列表 = 连接要素.字段列表获取(含系统字段=False)
            for x in 连接要素字段列表:
                目标要素.字段添加_通过字段对象(x)

            from bxarcpy import 游标类

            with 游标类.游标创建_通过名称("更新", 目标要素.名称, ["_ID", *连接要素.字段名称列表获取(含系统字段=False)]) as 面要素游标对象:  # type: ignore
                with 游标类.游标创建_通过名称("查询", 目标要素转点后带连接要素字段.名称, 目标要素转点后带连接要素字段.字段名称列表获取(含系统字段=False)) as 点要素游标对象:
                    for x in 面要素游标对象:
                        findFlag = False
                        for y in 点要素游标对象:
                            if int(x["_ID"]) == y["FID_" + 目标要素.名称_无路径]:
                                y["_ID"] = x["_ID"]
                                del y["FID_" + 目标要素.名称_无路径]
                                面要素游标对象.行更新(y)
                                findFlag = True
                                break
                        if findFlag == False:
                            日志类.输出信息(f'未找到ID为{x["_ID"]}的对象所对应的点')

            输出要素 = 目标要素.要素创建_通过复制并重命名重名要素(输出要素名称)

            # ret = self.要素创建_通过空间连接(目标要素连接后.名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
            # print("ret" + str(ret.字段名称列表获取()))

            return 输出要素
        arcpy.analysis.SpatialJoin(  # type: ignore
            target_features=self.名称,
            join_features=连接要素名称,
            out_feature_class=输出要素名称,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            # field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,YD_用地\\YD_不动产登记2,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,YD_用地\\YD_不动产登记2,Shape_Area,-1,-1;地类编号 "地类编号" true true false 50 Text 0 0,First,#,YD_用地\\YD_不动产登记2,地类编号,0,50;Shape_Length_1 "Shape_Length" true true true 8 Double 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,Shape_Length,-1,-1;Shape_Area_1 "Shape_Area" true true true 8 Double 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,Shape_Area,-1,-1;地类编号_1 "地类编号" true true false 100 Text 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,地类编号,0,100;ORIG_FID "ORIG_FID" true true false 0 Long 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,ORIG_FID,-1,-1',
            match_option=连接方式raw,
            search_radius="",
            distance_field_name="",
        )
        return 要素类(名称=输出要素名称)

    def 要素创建_通过填充空隙(self, 填充范围要素名称, 填充地类编号表达式='"00"', 输出要素名称="in_memory\\AA_填充空隙"):
        # 常用_填充空隙后
        # To allow overwriting outputs change overwriteOutput option to True.
        if 输出要素名称 == "in_memory\\AA_填充空隙":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()

        # Process: 复制要素 (复制要素) (management)
        输入要素 = 要素类.要素读取_通过名称(self.名称).要素创建_通过复制()
        填充范围要素 = 要素类.要素读取_通过名称(填充范围要素名称).要素创建_通过复制()
        填充范围要素.字段添加("地类编号").字段计算("地类编号", 填充地类编号表达式)
        更新后要素 = 输入要素.要素创建_通过更新(填充范围要素.名称).要素创建_通过更新(输入要素.名称)
        输出要素 = 更新后要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    def 要素创建_通过切分(self, 折点数量=200, 输出要素名称="in_memory\\AA_切分"):
        if 输出要素名称 == "in_memory\\AA_切分":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.management.Dice(self.名称, 输出要素名称, 折点数量)  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素创建_通过转点(self, 输出要素名称="in_memory\\AA_转点"):
        from .游标类 import 游标类

        if 输出要素名称 == "in_memory\\AA_转点":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()

        点要素 = 要素类.要素创建_通过名称("AA_转点" + "_" + 工具集.生成短GUID(), "点", 模板=self.名称)
        点要素复制后 = 点要素.要素创建_通过复制("in_memory\\AA_转点" + "_" + 工具集.生成短GUID())
        点要素.要素删除()
        点要素 = 点要素复制后
        点要素.字段添加("FID_" + self.名称_无路径, "长整型")

        字段列表 = self.字段名称列表获取()
        字段列表.remove("OBJECTID")
        字段列表.remove("Shape")
        字段列表.remove("Shape_Length")
        字段列表.remove("Shape_Area")
        字段列表.insert(0, "_ID")
        字段列表.insert(0, "_形状")
        # print(字段列表)

        点字段列表 = [x for x in 字段列表]
        点字段列表.pop(1)
        点字段列表.insert(0, "FID_" + self.名称_无路径)

        # print(点字段列表)
        with 游标类.游标创建_通过名称("查找", self.名称, 字段列表) as 面要素游标对象:
            with 游标类.游标创建_通过名称("插入", 点要素.名称, 点字段列表) as 点要素游标对象:
                from .几何对象类 import 几何对象类

                for x in 面要素游标对象:
                    try:
                        # 日志类.输出调试(f"x[0]是{x[0]._内嵌对象}")
                        x["_形状"] = 几何对象类.内点获取(x["_形状"])
                        x["FID_" + self.名称_无路径] = x["_ID"]
                        del x["_ID"]
                        # 日志类.输出调试(f"内点是{内点}")
                        点要素游标对象.行插入(x)
                    except Exception as e:
                        print(f"内点获取发生错误：{e}")
                        print(f"ID为 {x['_ID']} 的对象无法获取到内点，取了端点")
                        x["_形状"] = 几何对象类.点表获取(x["_形状"])[0][0]
                        x["FID_" + self.名称_无路径] = x["_ID"]
                        del x["_ID"]
                        # 日志类.输出调试(f"端点是{端点}")
                        点要素游标对象.行插入(x)
        return 点要素.要素创建_通过复制并重命名重名要素(输出要素名称)

    def 要素创建_通过转线(self, 输出要素名称="in_memory\\AA_转线"):
        if 输出要素名称 == "in_memory\\AA_转线":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        arcpy.management.FeatureToLine(in_features=self.名称, out_feature_class=输出要素名称)  # type: ignore
        return 要素类.要素读取_通过名称(输出要素名称)

    def 要素创建_通过面转线(self, 是否识别并存储面邻域信息=True, 输出要素名称="in_memory\\AA_面转线"):
        if 输出要素名称 == "in_memory\\AA_面转线":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        if 是否识别并存储面邻域信息:
            arcpy.management.PolygonToLine(in_features=self.名称, out_feature_class=输出要素名称, neighbor_option="IDENTIFY_NEIGHBORS")  # type: ignore
        else:
            arcpy.management.PolygonToLine(in_features=self.名称, out_feature_class=输出要素名称, neighbor_option="IGNORE_NEIGHBORS")  # type: ignore
        return 要素类.要素读取_通过名称(输出要素名称)

    def 要素创建_通过缓冲(self, 距离或字段名称, 融合类型="不融合", 融合字段名称列表=None, 末端类型="圆形", 输出要素名称="in_memory\\AA_缓冲"):
        if 输出要素名称 == "in_memory\\AA_缓冲":
            输出要素名称 = 输出要素名称 + "_" + 工具集.生成短GUID()
        _融合类型映射表 = {"不融合": "NONE", "NONE": "NONE", "融合为单个": "ALL", "ALL": "ALL", "融合按字段": "LIST", "LIST": "LIST"}
        融合类型 = _融合类型映射表[融合类型]
        _末端类型映射表 = {"圆形": "ROUND", "ROUND": "ROUND", "方形": "FLAT", "FLAT": "FLAT"}
        末端类型 = _末端类型映射表[末端类型]
        if 融合字段名称列表:
            融合字段名称列表 = ";".join(融合字段名称列表)
        arcpy.analysis.Buffer(in_features=self.名称, out_feature_class=输出要素名称, buffer_distance_or_field=距离或字段名称, line_side="FULL", line_end_type=末端类型, dissolve_option=融合类型, dissolve_field=融合字段名称列表, method="PLANAR")  # type: ignore
        return 要素类.要素读取_通过名称(输出要素名称)

    def 要素创建_通过增密(self, 增密方法: Literal["固定距离", "偏转距离", "偏转角度"] = "偏转距离", 固定距离="10 Meters", 偏转距离="0.0001 Meters", 偏转角度=1, 最大折点计数=None, 输出要素名称="内存临时"):
        if 输出要素名称 == "内存临时":
            输出要素名称 = "in_memory\\AA_增密" + "_" + 工具集.生成短GUID()
        _增密方法映射 = {"固定距离": "DISTANCE", "偏转距离": "OFFSET", "偏转角度": "ANGLE"}
        复制后要素 = self.要素创建_通过复制(输出要素名称)
        增密方法raw = _增密方法映射[增密方法] if 增密方法 in _增密方法映射 else 增密方法
        arcpy.edit.Densify(in_features=复制后要素.名称, densification_method=增密方法raw, distance=固定距离, max_deviation=偏转距离, max_angle=偏转角度, max_vertex_per_segment=最大折点计数)  # type: ignore
        return 复制后要素

    def 要素创建_通过投影定义(self, 坐标系='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', 输出要素名称="内存临时"):
        # 坐标系有效值可以是 SpatialReference 对象、扩展名为 .prj 的文件或坐标系的字符串表达形式。
        if 输出要素名称 == "内存临时":
            输出要素名称 = "in_memory\\AA_投影定义" + "_" + 工具集.生成短GUID()
        要素 = 要素类.要素读取_通过名称(self.名称).要素创建_通过复制()
        arcpy.management.DefineProjection(in_dataset=要素.名称, coor_system=坐标系)  # type: ignore
        输出要素 = 要素.要素创建_通过复制并重命名重名要素(输出要素名称=输出要素名称)
        return 输出要素

    def 要素创建_通过投影转换(self, 输出坐标系='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', 输出要素名称="内存临时"):
        # 坐标系有效值可以是 SpatialReference 对象、扩展名为 .prj 的文件或坐标系的字符串表达形式。
        if 输出要素名称 == "内存临时":
            输出要素名称 = "in_memory\\AA_投影转换" + "_" + 工具集.生成短GUID()
        要素 = 要素类.要素读取_通过名称(self.名称).要素创建_通过复制()
        arcpy.management.Project(in_dataset=要素.名称, out_dataset=输出要素名称, out_coor_system=输出坐标系, transform_method=None, in_coor_system=None, preserve_shape="NO_PRESERVE_SHAPE", max_deviation=None, vertical="NO_VERTICAL")  # type: ignore
        return 要素类(名称=输出要素名称)

    def 要素删除(self):
        return arcpy.management.Delete(in_data=[self.名称], data_type="")[0]  # type: ignore

    def 要素重命名(self, 新名称):
        arcpy.management.Rename(self.名称, 新名称)  # type: ignore
        return 要素类(名称=新名称)

    @staticmethod
    def 要素删除_通过要素名称列表(要素名称列表):
        return arcpy.management.Delete(in_data=要素名称列表, data_type="")[0]  # type: ignore

    def 要素几何修复(self):
        arcpy.management.RepairGeometry(in_features=self.名称, delete_null="KEEP_NULL", validation_method="ESRI")[0]  # type: ignore
        # arcpy.management.RepairGeometry(in_features=self.名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]
        return self

    def 选择集创建_通过属性(self, 选择方式="新建选择集", SQL语句=""):
        from .图层类 import 图层类

        _选择方式映射表 = {"新建选择集": "NEW_SELECTION", "NEW_SELECTION": "NEW_SELECTION"}
        选择方式 = _选择方式映射表[选择方式]
        a = arcpy.management.SelectLayerByAttribute(in_layer_or_view=self.名称, selection_type=选择方式, where_clause=SQL语句, invert_where_clause="")[0]  # type: ignore
        return 图层类(a)

    def 字段列表获取(self, 含系统字段=True):
        from .字段类 import 字段类

        if 含系统字段:
            字段列表 = [字段类(x) for x in arcpy.ListFields(self.名称)]  # type: ignore
        else:
            字段列表 = [字段类(x) for x in arcpy.ListFields(self.名称)]  # type: ignore
            字段列表 = [x for x in 字段列表 if x.名称 not in ["OBJECTID", "OBJECTID_1", "Shape", "Shape_1", "Shape_Length", "Shape_Length_1", "Shape_Area", "Shape_Area_1"]]
        return 字段列表

    def 字段名称列表获取(self, 含系统字段=True):
        字段列表 = self.字段列表获取(含系统字段=含系统字段)
        return [x.名称 for x in 字段列表]

    def 字段删除(self, 删除字段名称列表=None, 保留字段名称列表=None):
        from bxpy.日志包 import 日志类

        if 删除字段名称列表:
            # 日志类.输出控制台(f"即将被删除的字段为：" + str(删除字段名称列表))
            arcpy.management.DeleteField(in_table=self.名称, drop_field=删除字段名称列表, method="DELETE_FIELDS")[0]  # type: ignore
        if 保留字段名称列表:
            字段名称列表 = 要素类(名称=self.名称).字段名称列表获取()
            # 日志类.输出调试(f"要素拥有的所有字段为：" + str(字段名称列表))
            保留字段名称列表.extend(["OID", "OBJECTID", "OBJECTID_1", "Shape", "Shape_Area", "Shape_Length"])
            for x in 保留字段名称列表:
                if x in 字段名称列表:
                    字段名称列表.remove(x)
            # 日志类.输出调试(f"即将被删除的字段为：" + str(字段名称列表))
            if len(字段名称列表) > 0:
                arcpy.management.DeleteField(in_table=self.名称, drop_field=字段名称列表, method="DELETE_FIELDS")[0]  # type: ignore
        return self

    def 字段添加(self, 字段名称, 字段类型: Literal["字符串", "双精度", "长整型", "短整型", "日期", "单精度", "对象ID", "定长字符串"] = "字符串", 字段长度: Union[None, int] = 100, 字段别称="", 删除既有字段=True):
        """
        如果输入表是文件地理数据库，则将忽略字段精度值和小数位数值。
        """
        from . import 常量

        字段类型raw = 常量._字段类型映射[字段类型]

        if 删除既有字段:
            arcpy.management.DeleteField(in_table=self.名称, drop_field=[字段名称], method="DELETE_FIELDS")  # type: ignore

        字段名称列表 = self.字段名称列表获取()
        if 字段名称 not in 字段名称列表:
            arcpy.management.AddField(in_table=self.名称, field_name=字段名称, field_type=字段类型raw, field_precision=None, field_scale=None, field_length=字段长度, field_alias=字段别称, field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")  # type: ignore
        else:
            from . import 环境

            环境.输出消息(f"{self.名称}中已存在{字段名称}字段")

        return self

    def 字段添加_通过字段对象(self, 字段对象):
        self.字段添加(字段名称=字段对象.名称, 字段类型=字段对象.类型, 字段长度=字段对象.长度, 字段别称=字段对象.别称)
        return self

    def 字段计算(self, 字段名称, 表达式, 字段类型="字符串", 语言类型="PYTHON3", 代码块=""):
        from . import 常量

        字段类型 = 常量._字段类型映射[字段类型]
        arcpy.management.CalculateField(in_table=self.名称, field=字段名称, expression=表达式, expression_type=语言类型, code_block=代码块, field_type=字段类型, enforce_domains="NO_ENFORCE_DOMAINS")[0]  # type: ignore
        return self

    def 字段修改(self, 字段名称=None, 修改后字段名称=None, 修改后字段别称=None, 字段类型=None, 字段长度=None, 清除字段别称=True):
        from . import 常量

        if 字段类型:
            字段类型 = 常量._字段类型映射[字段类型]
        arcpy.management.AlterField(in_table=self.名称, field=字段名称, new_field_name=修改后字段名称, new_field_alias=修改后字段别称, field_type=字段类型, field_length=字段长度, field_is_nullable="NULLABLE", clear_field_alias=清除字段别称)[0]  # type: ignore
        return self

    def 连接创建(self, 输入要素连接字段名称=None, 连接要素名称=None, 连接要素连接字段名称=None):
        arcpy.management.AddJoin(in_layer_or_view=self.名称, in_field=输入要素连接字段名称, join_table=连接要素名称, join_field=连接要素连接字段名称, join_type="KEEP_ALL", index_join_fields="NO_INDEX_JOIN_FIELDS")[0]  # type: ignore
        return self

    def 连接取消(self, 连接要素名称):
        arcpy.management.RemoveJoin(in_layer_or_view=self.名称, join_name=连接要素名称)[0]  # type: ignore
        return self

    def 导出到CAD(self, 输出路径):
        return arcpy.conversion.ExportCAD(in_features=self.名称, Output_Type="DWG_R2010", Output_File=输出路径, Ignore_FileNames="Ignore_Filenames_in_Tables", Append_To_Existing="Overwrite_Existing_Files", Seed_File="")  # type: ignore

    def 导出到要素(self, 输出要素名称):
        # arcpy.conversion.FeatureClassToFeatureClass(in_features=self.名称, out_path=输出目录, out_name=输出文件名, where_clause="", field_mapping="", config_keyword="")[0]
        arcpy.conversion.ExportFeatures(in_features=self.名称, out_features=输出要素名称, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping=None, sort_field=[])  # type: ignore
        return 要素类(名称=输出要素名称)

    def 拓扑检查重叠(self, 是否导出到CAD=None):
        要素类.拓扑检查重叠_通过要素名称列表([self.名称], 是否导出到CAD=是否导出到CAD)

    @staticmethod
    def 拓扑检查重叠_通过要素名称列表(输入要素名称列表, 是否导出到CAD=None):
        from .要素数据集类 import 要素数据集类
        from .拓扑类 import 拓扑类

        要素数据集 = 要素数据集类.要素数据集创建("拓扑检查")
        拓扑对象 = 拓扑类.拓扑创建(要素数据集.名称, "拓扑")

        for x in 输入要素名称列表:
            输入要素 = 要素类.要素读取_通过名称(x)
            要素数据集中的要素 = 输入要素.导出到要素(要素数据集.名称 + "\\" + 输入要素.名称_无路径 + "_拓扑检查")
            # 日志类.输出调试(f"准备添加要素的名称是：{要素数据集中的要素.名称}")
            拓扑对象.拓扑中添加要素(要素数据集中的要素.名称)
            # 日志类.输出调试(f"准备添加要素的类型是：{要素数据集中的要素.几何类型}")
            if 要素数据集中的要素.几何类型 == "面":
                拓扑对象.拓扑中添加规则(要素数据集中的要素.名称, 规则="面无重叠")
            elif 要素数据集中的要素.几何类型 == "线":
                拓扑对象.拓扑中添加规则(要素数据集中的要素.名称, 规则="线无重叠")
                拓扑对象.拓扑中添加规则(要素数据集中的要素.名称, 规则="线无自重叠")
            拓扑对象.拓扑验证()

        拓扑导出后要素1, 拓扑导出后要素2, 拓扑导出后要素3 = 拓扑对象.导出到要素("AA_拓扑导出后要素")
        from bxarcpy import 环境

        if 拓扑导出后要素3.几何数量 > 0:
            环境.输出消息(f"拓扑检查存在面错误")
            if 是否导出到CAD:
                拓扑导出后要素3.要素创建_通过多部件至单部件().导出到CAD(r"AA_拓扑_面.dwg")
        if 拓扑导出后要素2.几何数量 > 0:
            环境.输出消息(f"拓扑检查存在线错误")
            if 是否导出到CAD:
                拓扑导出后要素2.要素创建_通过多部件至单部件().导出到CAD(r"AA_拓扑_线.dwg")
        if 拓扑导出后要素1.几何数量 > 0:
            环境.输出消息(f"拓扑检查存在点错误")
            if 是否导出到CAD:
                拓扑导出后要素1.要素创建_通过多部件至单部件().导出到CAD(r"AA_拓扑_点.dwg")
        if 拓扑导出后要素3.几何数量 <= 0 and 拓扑导出后要素2.几何数量 <= 0 and 拓扑导出后要素1.几何数量 <= 0:
            环境.输出消息(f"拓扑检查没有错误")

        拓扑导出后要素1.要素删除()
        拓扑导出后要素2.要素删除()
        拓扑导出后要素3.要素删除()

    def 拓扑检查范围(self, 范围要素名称, 是否导出到CAD=None):
        要素类.拓扑检查范围_通过要素名称列表([self.名称], 范围要素名称, 是否导出到CAD)

    @staticmethod
    def 拓扑检查范围_通过要素名称列表(输入要素名称列表, 范围要素名称, 是否导出到CAD=None):
        for x in 输入要素名称列表:
            范围要素 = 要素类.要素读取_通过名称(范围要素名称).要素创建_通过复制()
            已填色要素 = 要素类.要素读取_通过名称(x).要素创建_通过复制()
            from .环境 import 环境

            需填未填 = 范围要素.要素创建_通过擦除(已填色要素.名称).要素创建_通过多部件至单部件()
            if 需填未填.几何数量 > 0:
                环境.输出消息(f"存在空隙（需填未填）_{已填色要素.名称_无路径}_{范围要素名称}")
                需填未填.要素创建_通过复制并重命名重名要素(f"AA_空隙_{已填色要素.名称_无路径}_{范围要素名称}")
                if 是否导出到CAD:
                    需填未填.导出到CAD(rf"AA_空隙_{已填色要素.名称_无路径}_{范围要素名称}.dwg")

            不需填但被填 = 已填色要素.要素创建_通过擦除(范围要素.名称).要素创建_通过多部件至单部件()
            if 不需填但被填.几何数量 > 0:
                环境.输出消息(f"存在多余（不需填但被填）_{已填色要素.名称_无路径}_{范围要素名称}")
                不需填但被填.要素创建_通过复制并重命名重名要素(f"AA_多余_{已填色要素.名称_无路径}_{范围要素名称}")
                if 是否导出到CAD:
                    不需填但被填.导出到CAD(rf"AA_多余_{已填色要素.名称_无路径}_{范围要素名称}.dwg")
            if 需填未填.几何数量 <= 0 and 不需填但被填.几何数量 <= 0:
                环境.输出消息(f"{已填色要素.名称_无路径}与{范围要素名称}之间契合")

    # def 符号系统设置_通过样式文件(图层名称="DIST_用地规划图"):
    #     from . import 文档类
    #     文档 = 文档类.文档读取_通过名称("CURRENT")
    #     # 文档 = bxarcpy.文档类.文档读取_通过名称(文档路径=r"C:\Users\common\Project\J江东区临江控规\临江控规_数据库.aprx")
    #     地图 = 文档.地图列表读取("*")[0]
    #     # bxarcpy.环境.输出消息(f"选取到的地图是：{地图}")
    #     # 日志类.输出调试(地图)
    #     图层名称_无路径 = 图层名称.split("\\")[-1]
    #     图层 = 地图.图层列表读取(图层名称_无路径)[0]
    #     # bxarcpy.环境.输出消息(f"{图层._内嵌对象.name}")
    #     图层.符号系统设置_通过stylx样式文件()
    #     符号系统图层 = bxarcpy.图层文件类.图层文件读取(r"C:\Users\beixiao\appconfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.lyr").图层列表读取()[0]
    #     bxarcpy.环境.输出消息(f"符号系统图层：{符号系统图层}")
    #     图层.符号系统设置_通过图层文件(符号系统图层, [["值字段", "地类编号", "地类编号"]])

    # 输出图层 = rf'arcpy.management.MatchLayerSymbologyToAStyle(in_layer={DIST_用地规划图}, match_values="$feature.地类编号", in_style="C:\\Users\\Beixiao\\AppConfig\\ArcGIS\\010.符号系统\\符号系统_省国空地类_根据编号.stylx")[0]'
    # python_window_extension.execute_script(输出图层)
    # 日志类.输出调试(图层)
    # 图层对象 = 图层.getDefinition("V3")
    # symLvl2 = 图层对象.renderer.symbol.symbol.symbolLayers[1]
    # symLvl2.color.values = [140, 70, 20, 20]
    # 图层.setDefinition(图层对象)


# if __name__ == "__main__":
#     工作空间 = bxarcpy.环境.输入参数获取_以字符串形式(0, r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb")
#     图层名称 = bxarcpy.环境.输入参数获取_以字符串形式(1, r"DIST_用地规划图", False)
#     # arcpy.management.MatchLayerSymbologyToAStyle(r"DIST_用地规划图", "地类编号", r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx")

#     # 日志类.开启()
#     符号系统设置(图层名称)
if __name__ == "__main__":
    import bxarcpy

    工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规"
    # 道路中线要素名称 = bxarcpy.环境.输入参数获取_以字符串形式(0, "DL_道路中线", True)
    with bxarcpy.环境.环境管理器(工作空间):
        要素 = 要素类.要素读取_通过名称("XG_KZX1").要素创建_通过复制()
        要素.要素创建_通过增密()
