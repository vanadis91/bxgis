from bxpy.日志包 import 日志生成器
from bxpy.时间包 import 时间类
from bxpy.路径包 import 路径类
from bxpy.元数据包 import 追踪元数据类
import bxarcpy.工具包 as 工具包
from bxarcpy.工具包 import 输出路径生成_当采用内存临时时, 输出路径生成_当采用临时工作空间临时时, 输出路径生成_当采用当前工作空间临时时
from bxarcpy.基本对象包 import 枚举类
import arcpy
from bxarcpy.枚举包 import 特殊字段_枚举
from typing import Union, Literal


# def 输出路径生成_当采用内存临时时(输入要素路径列表):
#     日志类.临时关闭日志()
#     from bxpy.基本对象包 import 字类

#     要素名称列表 = [要素类.属性获取_要素名称(x) for x in 输入要素路径列表]
#     要素名称 = "_".join(要素名称列表)

#     要素名称列表 = 要素名称.split("_")
#     要素名称列表 = [x for x in 要素名称列表 if not 字类.匹配正则(x, r"^[A-Za-z0-9]{10}$") and not 字类.匹配正则(x, r"^[A-Za-z0-9]{22}$") and x.upper() not in ["AA", "KZX", "DIST", "YD", "GZW", "CZ", "AC", "DL", "JX", "SS", "TK", "YT"]]
#     要素名称 = "_".join(要素名称列表)
#     日志类.输出调试(f"要素名称为：{要素名称}")
#     if len(要素名称) > 15:
#         要素名称 = 要素名称[0:15]
#     输出要素路径 = "in_memory\\AA_" + 要素名称 + "_" + 工具包.生成短GUID()
#     return 输出要素路径


def _字段名称生成_根据既有字段名称(既有字段名称列表):

    日志生成器.临时关闭日志()
    from bxpy.基本对象包 import 字类

    既有字段名称 = "_".join(既有字段名称列表)

    既有字段名称列表 = 既有字段名称.split("_")
    既有字段名称列表 = [x for x in 既有字段名称列表 if not 字类.匹配正则(x, r"^[A-Za-z0-9]{10}$") and not 字类.匹配正则(x, r"^[A-Za-z0-9]{22}$") and x.upper() not in ["AA", "KZX", "DIST", "YD", "GZW", "CZ", "AC", "DL", "JX", "SS", "TK", "YT"]]
    既有字段名称 = "_".join(既有字段名称列表)
    日志生成器.输出调试(f"要素名称为：{既有字段名称}")
    if len(既有字段名称) > 18:
        既有字段名称 = 既有字段名称[0:18]
    输出要素路径 = 既有字段名称 + "_" + 工具包.生成短GUID()
    return 输出要素路径


class 要素类:
    @staticmethod
    def 属性获取_空间参考(要素路径):
        坐标系 = arcpy.Describe(要素路径).spatialReference  # type: ignore
        if 坐标系 is None or 坐标系.name == "Unknown":
            return None
        return 坐标系

    @staticmethod
    def 属性获取_几何类型(要素路径):
        几何类型 = arcpy.Describe(要素路径).shapeType  # type: ignore
        return 枚举类.要素类型.名称获取(几何类型)

    @staticmethod
    def 属性获取_几何数量(要素路径):

        结果 = arcpy.GetCount_management(要素路径)
        数量 = int(结果.getOutput(0))  # type: ignore
        return 数量

    @staticmethod
    def 属性获取_要素名称(要素路径):
        要素名称 = 路径类.属性获取_文件名(路径类.规范化(要素路径))
        return 要素名称

    @staticmethod
    def 要素创建_通过名称(要素名称="内存临时", 要素类型="面", 模板=None, 数据库路径="内存临时"):
        from bxarcpy.环境包 import 环境类

        if 要素名称 == "内存临时":
            要素名称 = "AA_新建" + "_" + 工具包.生成短GUID()

        if 数据库路径 == "内存临时":
            数据库路径第一次 = 环境类.属性获取_当前工作空间()
            数据库路径第二次 = "in_memory"
        else:
            数据库路径第一次 = 数据库路径
            数据库路径第二次 = None
        # elif 数据库路径.upper() in ["内存临时", "临时", "IN_MEMORY", "MEMORY"]:
        #     数据库路径 = "in_memory"
        要素类型 = 枚举类.要素类型.值获取(要素类型)
        arcpy.management.CreateFeatureclass(out_path=数据库路径第一次, out_name=要素名称, geometry_type=要素类型, template=模板, has_m="DISABLED", has_z="DISABLED", spatial_reference='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-495395959010.755 -495395959010.755 9090.90909090909;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision', config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0, out_alias="")  # type: ignore
        ret = 要素名称
        if 数据库路径第二次:
            要素类.要素创建_通过复制(数据库路径第一次 + "\\" + ret, 数据库路径第二次 + "\\" + 要素名称)
            要素类.要素删除(数据库路径第一次 + "\\" + ret)
            ret = 数据库路径第二次 + "\\" + 要素名称
        # if 数据库路径.upper() in ["临时", "IN_MEMORY", "MEMORY"]:
        #     ret = ret.要素创建_通过复制并重命名重名要素(f"in_memory\\{要素名称}")
        return ret

    @staticmethod
    def 要素创建_通过复制(要素路径, 输出要素路径="临时工作空间临时"):
        日志生成器.临时关闭日志()
        from bxpy.路径包 import 路径类
        from bxpy.基本对象包 import 字类

        日志生成器.输出调试(f"要素路径为：{要素路径}")
        输出要素路径 = 输出路径生成_当采用临时工作空间临时时([要素路径]) if 输出要素路径 == "临时工作空间临时" else 输出要素路径
        from bxarcpy.空间参考包 import 空间参考类
        from bxarcpy.环境包 import 输入输出类

        try:
            arcpy.management.Copy(in_data=要素路径, out_data=输出要素路径)  # type: ignore
        except Exception as e:
            空间参考对象 = 要素类.属性获取_空间参考(要素路径)
            if 空间参考对象:
                if 空间参考类.属性获取_类型(空间参考对象) == "地理坐标系":
                    输入输出类.输出消息(f"{要素路径}为地理坐标系，操作中可能精度会损失，建议先转换为投影坐标系")
            arcpy.management.CopyFeatures(in_features=要素路径, out_feature_class=输出要素路径, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        # arcpy.conversion.ExportFeatures(in_features=要素路径, out_features=输出要素路径) # type: ignore
        # except:
        #     arcpy.management.CopyFeatures(in_features=要素名称, out_feature_class=输出要素路径, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        # 要素类.字段删除(输出要素路径, ["ORIG_FID"])
        return 输出要素路径

    @staticmethod
    def 要素创建_通过复制并重命名重名要素(输入要素路径, 输出要素路径="临时工作空间临时", 重名时原要素被重命名后后缀=""):
        from bxarcpy.数据库包 import 数据库类
        from bxpy.路径包 import 路径类
        from bxarcpy.环境包 import 环境类, 输入输出类

        输出要素路径 = 输出路径生成_当采用临时工作空间临时时([输入要素路径]) if 输出要素路径 == "临时工作空间临时" else 输出要素路径

        要素名称列表 = 数据库类.属性获取_要素名称列表(环境类.属性获取_当前工作空间())
        存在重复flag = False
        outText = ""
        if 输出要素路径 in 要素名称列表:
            # 时间类.等待(1)
            存在重复flag = True
            原要素被重命名后路径 = 输出要素路径 + "_" + 工具包.生成当前时间()
            if 重名时原要素被重命名后后缀 != "":
                原要素被重命名后路径 = 原要素被重命名后路径 + "_" + 重名时原要素被重命名后后缀
            try:
                if 路径类.是否为绝对路径(输出要素路径):
                    要素类.要素创建_通过复制(输出要素路径, 原要素被重命名后路径)
                    outText = outText + f"存在重名要素，原要素备份为【{原要素被重命名后路径}】"
                else:
                    要素类.要素创建_通过复制(输出要素路径, 路径类.连接(环境类.属性获取_当前临时工作空间(), 原要素被重命名后路径))
                    outText = outText + f"存在重名要素，原要素备份为【{原要素被重命名后路径}】，存至临时空间"
            except Exception as e:
                outText = outText + f"存在重名要素，原要素备份失败，【{追踪元数据类.追踪信息获取()}】"
        try:
            要素类.要素删除(输出要素路径)
            要素类.要素创建_通过复制(输入要素路径, 输出要素路径)
            outText = outText + "，同时进行删除成功，" if 存在重复flag else outText
            outText = outText + f"新要素命名为【{输出要素路径}】" if 存在重复flag else outText
            # 输入输出类.输出消息(f"存在重名要素，原要素删除成功，输出要素为：{输出要素路径}")
            # arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        except Exception as e:
            from bxarcpy.环境包 import 环境类, 输入输出类

            输出要素路径 = 输出要素路径 + "new_" + 工具包.生成当前时间()

            要素类.要素创建_通过复制(输入要素路径, 输出要素路径)
            outText = outText + "，同时进行删除失败，" if 存在重复flag else outText + "复制出错，"
            outText = outText + f"新要素命名为【{输出要素路径}】"
            # arcpy.management.CopyFeatures(in_features=self.名称, out_feature_class=输出要素名称, config_keyword="", spatial_grid_1=0, spatial_grid_2=0, spatial_grid_3=0)  # type: ignore
        if len(outText) > 0:
            输入输出类.输出消息(outText, 级别="信息")
        return 输出要素路径

    @staticmethod
    def 要素创建_通过合并(输入要素路径列表=[], 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时(输入要素路径列表) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.management.Merge(inputs=输入要素路径列表, output=输出要素路径, field_mappings="", add_source="NO_SOURCE_INFO")  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过裁剪(输入要素路径, 裁剪要素路径, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 裁剪要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.analysis.Clip(in_features=输入要素路径, clip_features=裁剪要素路径, out_feature_class=输出要素路径, cluster_tolerance="")  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过擦除_原始(输入要素路径, 擦除要素路径, 输出要素路径="内存临时"):
        # 这个函数如果和相交函数运行后的部分合并，会有缝隙
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 擦除要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.analysis.Erase(in_features=输入要素路径, erase_features=擦除要素路径, out_feature_class=输出要素路径, cluster_tolerance="")  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过擦除(输入要素路径, 擦除要素路径, 是否多部件转单部件=True, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 擦除要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        输出要素路径 = 要素类.要素创建_通过联合并赋值字段(输入要素路径, 擦除要素路径, 字段映射列表=None, 是否多部件转单部件=是否多部件转单部件, 是否去除输入无联合有的部分=True, 是否去除输入有联合有的部分=True, 是否检查两者差异=False, 输出要素路径=输出要素路径)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过分割(输入要素路径, 分割要素路径, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 分割要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        分割要素裁剪后 = 要素类.要素创建_通过裁剪(分割要素路径, 输入要素路径)
        输入要素字段列表 = 要素类.字段名称列表获取(输入要素路径)

        分割后要素 = 要素类.要素创建_通过联合([输入要素路径, 分割要素裁剪后], 是否保留FID=False)
        要素类.字段删除(分割后要素, 保留字段名称列表=输入要素字段列表)
        输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(分割后要素, 输出要素路径)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过擦除并几何修复(输入要素路径, 擦除要素路径, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 擦除要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        输入要素路径 = 要素类.要素创建_通过几何修复(输入要素路径)
        擦除要素路径 = 要素类.要素创建_通过几何修复(擦除要素路径)
        arcpy.analysis.Erase(in_features=输入要素路径, erase_features=擦除要素路径, out_feature_class=输出要素路径, cluster_tolerance="")  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过几何修复(输入要素路径, 删除几何为空的要素=True, 是否打印被删除的要素=False, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        输入要素名称 = 要素类.属性获取_要素名称(输入要素路径)
        输出要素路径 = 要素类.要素创建_通过复制(输入要素路径, 输出要素路径)
        删除几何为空的要素 = "KEEP_NULL" if 删除几何为空的要素 is False else "DELETE_NULL"
        arcpy.management.RepairGeometry(in_features=输出要素路径, delete_null=删除几何为空的要素, validation_method="ESRI")[0]  # type: ignore
        # arcpy.management.RepairGeometry(in_features=self.名称, delete_null="DELETE_NULL", validation_method="ESRI")[0]
        if 是否打印被删除的要素:
            from bxarcpy.游标包 import 游标类
            from bxarcpy.环境包 import 输入输出类

            原要素ID列表 = []
            修复后要素ID列表 = []
            with 游标类.游标创建("查询", 输入要素路径, ["_ID"]) as 游标:
                for row in 游标类.属性获取_数据_字典形式(游标, ["_ID"]):
                    原要素ID列表.append(row["_ID"])
            with 游标类.游标创建("查询", 输出要素路径, ["_ID"]) as 游标:
                for row in 游标类.属性获取_数据_字典形式(游标, ["_ID"]):
                    修复后要素ID列表.append(row["_ID"])
            被删除的要素列表 = [x for x in 原要素ID列表 if x not in 修复后要素ID列表]
            被删除的要素数据列表 = []
            操作列表 = 要素类.字段名称列表获取(输入要素路径)
            操作列表.append("_ID")
            with 游标类.游标创建("查询", 输入要素路径, 操作列表) as 游标:
                for row in 游标类.属性获取_数据_字典形式(游标, 操作列表):
                    if row["_ID"] in 被删除的要素列表:
                        被删除的要素数据列表.append(row)
            if len(被删除的要素数据列表) > 0:
                from bxpy.基本对象包 import 字类

                被删除的要素数据列表_转字 = 字类.转换_到字(被删除的要素数据列表, json缩进=2)
                输入输出类.输出消息(f"{输入要素名称}几何修复后被删除的数据为：\n{被删除的要素数据列表_转字}")
        return 输出要素路径

    @staticmethod
    def 要素创建_通过相交_原始(输入要素路径列表=[], 输出字段设置: Literal["所有", "除FID外所有字段", "仅FID字段", "仅第一个要素字段"] = "所有", 输出要素路径="内存临时"):
        # 这个函数如果和擦除函数运行后的部分合并，会有缝隙
        输出要素路径 = 输出路径生成_当采用内存临时时(输入要素路径列表) if 输出要素路径 == "内存临时" else 输出要素路径

        _输出字段设施映射 = {"所有": "ALL", "除FID外所有字段": "NO_FID", "仅FID字段": "ONLY_FID"}
        字段设置raw = _输出字段设施映射[输出字段设置] if 输出字段设置 in _输出字段设施映射 else 输出字段设置
        输入要素路径列表 = [[x, ""] for x in 输入要素路径列表]
        if 输出字段设置 == "仅第一个要素字段":
            第一个要素字段名称列表 = 要素类.字段名称列表获取(输入要素路径列表[0][0])
            字段设置raw = "ALL"
        arcpy.analysis.Intersect(in_features=输入要素路径列表, out_feature_class=输出要素路径, join_attributes=字段设置raw, cluster_tolerance="", output_type="INPUT")  # type: ignore
        if 输出字段设置 == "仅第一个要素字段":
            要素类.字段删除(输出要素路径, 保留字段名称列表=第一个要素字段名称列表)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过相交(输入要素路径列表=[], 输出字段设置: Literal["所有", "除FID外所有字段", "仅FID字段", "仅第一个要素字段"] = "所有", 是否多部件转单部件=True, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时(输入要素路径列表) if 输出要素路径 == "内存临时" else 输出要素路径

        if len(输入要素路径列表) > 2:
            raise Exception("当前仅支持两个要素相交")

        输出要素路径 = 要素类.要素创建_通过联合并赋值字段(输入要素路径列表[0], 输入要素路径列表[1], 字段映射列表=None, 是否多部件转单部件=是否多部件转单部件, 是否去除输入有联合无的部分=True, 是否去除输入无联合有的部分=True, 是否检查两者差异=False, 输出字段设置=输出字段设置, 输出要素路径=输出要素路径)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过联合(输入要素路径列表=[], 是否保留周长和面积=False, 是否保留FID=True, 删除各要素间重名字段=True, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时(输入要素路径列表) if 输出要素路径 == "内存临时" else 输出要素路径

        if 删除各要素间重名字段:
            唯一字段名称列表 = []
            for 要素 in 输入要素路径列表:
                for 字段名称 in 要素类.字段名称列表获取(要素):
                    if 字段名称 not in 唯一字段名称列表:
                        唯一字段名称列表.append(字段名称)
                    else:
                        要素类.字段删除(要素, [字段名称])
        _输入要素名称列表_格式化 = [[x, ""] for x in 输入要素路径列表]
        arcpy.analysis.Union(in_features=_输入要素名称列表_格式化, out_feature_class=输出要素路径, join_attributes="ALL", cluster_tolerance=None, gaps="GAPS")  # type: ignore
        if 是否保留周长和面积 is False:
            字段名称列表 = 要素类.字段名称列表获取(输出要素路径)
            for 字段名称 in 字段名称列表:
                if "Shape_Length" in 字段名称 or "Shape_Area" in 字段名称:
                    要素类.字段删除(输出要素路径, [字段名称])
        if 是否保留FID is False:
            带FID要素名称列表 = ["FID_" + 要素类.属性获取_要素名称(x) for x in 输入要素路径列表]
            # 日志类.输出控制台(带FID要素名称列表)
            字段名称列表 = 要素类.字段名称列表获取(输出要素路径)
            for 字段名称 in 字段名称列表:
                # 日志类.输出控制台(字段名称)
                if 字段名称 in 带FID要素名称列表:
                    要素类.字段删除(输出要素路径, [字段名称])
        return 输出要素路径

    @staticmethod
    def 要素创建_通过联合并赋值字段(输入要素路径, 联合要素路径="JX_街区范围线", 字段映射列表=[["所属街区", "街区编号"]], 是否多部件转单部件=True, 是否去除输入有联合无的部分=False, 是否去除输入无联合有的部分=False, 是否去除输入有联合有的部分=False, 是否检查两者差异=True, 差异是否输出到要素类=False, 差异是否输出到CAD=False, 要素被分割时提示信息中包括的字段=[], 是否删除字段的既有值=True, 输出字段设置: Literal["所有", "除FID外所有字段", "仅FID字段", "仅第一个要素字段"] = "仅第一个要素字段", 输出要素路径="内存临时"):
        日志生成器.临时关闭日志()
        from bxpy.基本对象包 import 字类, 表类
        from bxarcpy.环境包 import 输入输出类
        from bxarcpy.游标包 import 游标类

        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 联合要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        输入要素原始名称 = 要素类.属性获取_要素名称(输入要素路径)
        输入要素路径 = 要素类.要素创建_通过复制(输入要素路径)
        if 是否多部件转单部件:
            输入要素路径 = 要素类.要素创建_通过多部件至单部件(输入要素路径)
        输入要素名称 = 要素类.属性获取_要素名称(输入要素路径)

        联合要素原始名称 = 要素类.属性获取_要素名称(联合要素路径)
        联合要素路径 = 要素类.要素创建_通过复制(联合要素路径)
        if 是否多部件转单部件:
            联合要素路径 = 要素类.要素创建_通过多部件至单部件(联合要素路径)
        联合要素名称 = 要素类.属性获取_要素名称(联合要素路径)

        # 处理字段
        if 字段映射列表:
            # 输入要素添加字段映射列表中的值
            输入要素字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
            联合要素字段列表 = 要素类.字段列表获取(联合要素路径)
            for 字段映射元祖 in 字段映射列表:
                from bxarcpy.要素包 import 字段类

                if 字段映射元祖[0] not in 输入要素字段名称列表:
                    匹配的字段列表2 = [x for x in 联合要素字段列表 if 字段类.属性获取_名称(x) == 字段映射元祖[1]]
                    字段类型 = 字段类.属性获取_类型(匹配的字段列表2[0])
                    字段长度 = 字段类.属性获取_长度(匹配的字段列表2[0])
                    要素类.字段添加(输入要素路径, 字段映射元祖[0], 字段类型, 字段长度)
                    输入输出类.输出消息(f"【{输入要素原始名称}】中无【{字段映射元祖[0]}】字段，已自动添加")

        输入要素字段名称列表 = 要素类.字段名称列表获取(输入要素路径, 含系统字段=False)
        联合要素字段名称列表 = 要素类.字段名称列表获取(联合要素路径, 含系统字段=False)
        for 联合要素字段名称n in 联合要素字段名称列表:
            # 重命名联合要素中重名的字段
            if 联合要素字段名称n in 输入要素字段名称列表:
                修改后字段名称 = _字段名称生成_根据既有字段名称([联合要素字段名称n])
                要素类.字段修改(联合要素路径, 联合要素字段名称n, 修改后字段名称)
                输入输出类.输出消息(f"【{输入要素原始名称}】中已存在联合要素中【{联合要素字段名称n}】字段，已将联合要素中字段重命名为【{修改后字段名称}】")
                if 字段映射列表:
                    字段映射列表zip = list(zip(*字段映射列表))
                    if 联合要素字段名称n in 字段映射列表zip[1]:
                        输入要素字段列表 = list(字段映射列表zip[0])
                        联合要素字段列表 = list(字段映射列表zip[1])
                        索引 = 联合要素字段列表.index(联合要素字段名称n)
                        联合要素字段列表[索引] = 修改后字段名称
                        字段映射列表 = list(zip(输入要素字段列表, 联合要素字段列表))
                        字段映射列表 = [list(x) for x in 字段映射列表]
                        输入输出类.输出消息(f"【{联合要素字段名称n}】在字段映射列表中，因此字段映射列表改成了【{字段映射列表}】")

        输入要素字段名称列表 = 要素类.字段名称列表获取(输入要素路径, 含系统字段=False)
        联合要素字段名称列表 = 要素类.字段名称列表获取(联合要素路径, 含系统字段=False)
        日志生成器.输出调试(f"修改后的字段映射列表：{字段映射列表}")

        # 正式开始联合
        联合后要素路径 = 要素类.要素创建_通过联合([输入要素路径, 联合要素路径])
        if 是否多部件转单部件:
            联合后要素路径 = 要素类.要素创建_通过多部件至单部件(联合后要素路径)

        if 是否检查两者差异:
            要素路径_应填色但是没填 = 要素类.要素创建_通过名称(模板=联合后要素路径)
            时间类.等待(1)
            要素路径_不应填色但是填色 = 要素类.要素创建_通过名称(模板=联合后要素路径)
            时间类.等待(1)
            要素路径_被范围线分割 = 要素类.要素创建_通过名称(模板=联合后要素路径)
            时间类.等待(1)
            联合后要素字段列表 = 要素类.字段名称列表获取(联合后要素路径, 含系统字段=False)
            联合后要素字段列表.insert(0, "_ID")
            联合后要素字段列表.insert(1, "_形状")

            日志生成器.输出调试(f"联合后要素字段列表为：{联合后要素字段列表}")
            元素FID列表 = []
            元素属性列表 = []
            分割要素已插入列表 = []
            from bxarcpy.游标包 import 游标类
            from bxarcpy.环境包 import 输入输出类

            日志生成器.输出调试(f"输入要素路径为：{输入要素路径}")
            输入要素名称 = 要素类.属性获取_要素名称(输入要素路径)
            联合要素名称 = 要素类.属性获取_要素名称(联合要素路径)
            with 游标类.游标创建("查询", 联合后要素路径, 联合后要素字段列表) as 联合后要素游标:
                with 游标类.游标创建("插入", 要素路径_应填色但是没填, 联合后要素字段列表) as 应填色但是没填的区域要素游标:
                    with 游标类.游标创建("插入", 要素路径_不应填色但是填色, 联合后要素字段列表) as 不应填色但是填色的区域要素游标:
                        with 游标类.游标创建("插入", 要素路径_被范围线分割, 联合后要素字段列表) as 被范围线分割的要素游标:
                            for 联合后要素x in 游标类.属性获取_数据_字典形式(联合后要素游标, 联合后要素字段列表):
                                if 联合后要素x[f"FID_{输入要素名称}"] == -1:
                                    游标类.行插入_字典形式(应填色但是没填的区域要素游标, 联合后要素x, 联合后要素字段列表)
                                if 联合后要素x[f"FID_{联合要素名称}"] == -1:
                                    游标类.行插入_字典形式(不应填色但是填色的区域要素游标, 联合后要素x, 联合后要素字段列表)
                                if 联合后要素x[f"FID_{输入要素名称}"] in 元素FID列表 and 联合后要素x[f"FID_{输入要素名称}"] != -1:
                                    输出消息 = f'要素被分割了，FID_{输入要素名称}: {联合后要素x[f"FID_{输入要素名称}"]}, '
                                    if 要素被分割时提示信息中包括的字段:
                                        for 字段名称x in 要素被分割时提示信息中包括的字段:
                                            if 字段名称x in 联合后要素字段列表:
                                                输出消息 += f"{字段名称x}: { 联合后要素x[字段名称x]}, "
                                    输出消息 = 输出消息[:-2]
                                    输入输出类.输出消息(输出消息)
                                    if 联合后要素x[f"FID_{输入要素名称}"] in 分割要素已插入列表:
                                        游标类.行插入_字典形式(被范围线分割的要素游标, 联合后要素x, 联合后要素字段列表)
                                    else:
                                        游标类.行插入_字典形式(被范围线分割的要素游标, 联合后要素x, 联合后要素字段列表)
                                        游标类.行插入_字典形式(被范围线分割的要素游标, 元素属性列表[元素FID列表.index(联合后要素x[f"FID_{输入要素名称}"])], 联合后要素字段列表)
                                        分割要素已插入列表.append(联合后要素x[f"FID_{输入要素名称}"])
                                元素FID列表.append(联合后要素x[f"FID_{输入要素名称}"])
                                元素属性列表.append(联合后要素x)
            if 要素类.属性获取_几何数量(要素路径_应填色但是没填) > 0:
                输入输出类.输出消息(f"输入要素存在缺失：{输入要素原始名称}与{联合要素原始名称}")
                if 差异是否输出到要素类:
                    要素类.要素创建_通过复制并重命名重名要素(要素路径_应填色但是没填, f"AA_缺失_{输入要素原始名称}与{联合要素原始名称}")
                if 差异是否输出到CAD:
                    要素类.转换_到CAD(要素路径_应填色但是没填, rf"AA_缺失_{输入要素原始名称}与{联合要素原始名称}.dwg")

            if 要素类.属性获取_几何数量(要素路径_不应填色但是填色) > 0:
                输入输出类.输出消息(f"输入要素存在多余：{输入要素原始名称}与{联合要素原始名称}")
                if 差异是否输出到要素类:
                    要素类.要素创建_通过复制并重命名重名要素(要素路径_不应填色但是填色, f"AA_多余_{输入要素原始名称}与{联合要素原始名称}")
                if 差异是否输出到CAD:
                    要素类.转换_到CAD(要素路径_不应填色但是填色, rf"AA_多余_{输入要素原始名称}与{联合要素原始名称}.dwg")

            if 要素类.属性获取_几何数量(要素路径_被范围线分割) > 0:
                输入输出类.输出消息(f"几何对象被分割：{输入要素原始名称}与{联合要素原始名称}")
                if 差异是否输出到要素类:
                    要素类.要素创建_通过复制并重命名重名要素(要素路径_被范围线分割, f"AA_被分割_{输入要素原始名称}与{联合要素原始名称}")
                if 差异是否输出到CAD:
                    要素类.转换_到CAD(要素路径_被范围线分割, rf"AA_被分割_{输入要素原始名称}与{联合要素原始名称}.dwg")

        # 开始操作字段
        日志生成器.输出调试(f"联合后要素的字段列表：{要素类.字段名称列表获取(联合后要素路径)}", 内容长度=20000)
        if 是否删除字段的既有值 and 字段映射列表:
            for 字段映射元祖 in 字段映射列表:
                要素类.字段计算(联合后要素路径, 字段映射元祖[0], "None")
                要素类.字段计算(联合后要素路径, 字段映射元祖[0], f"!{字段映射元祖[1]}!")
        elif 是否删除字段的既有值 is False and 字段映射列表:
            操作字段 = set()
            for 字段映射元祖 in 字段映射列表:
                for y in 字段映射元祖:
                    操作字段.add(y)
            操作字段 = list(操作字段)
            from bxarcpy.游标包 import 游标类

            with 游标类.游标创建("更新", 联合后要素路径, 操作字段) as 游标:
                for 数据x in 游标类.属性获取_数据_字典形式(游标, 操作字段):
                    for 字段映射元祖 in 字段映射列表:
                        if 数据x[字段映射元祖[1]] not in [None, "", " "]:
                            数据x[字段映射元祖[0]] = 数据x[字段映射元祖[1]]
                    游标类.行更新_字典形式(游标, 数据x)

        # 开始处理空间差异关系
        if 是否去除输入有联合无的部分 or 是否去除输入无联合有的部分 or 是否去除输入有联合有的部分:
            操作字段列表1 = [f"FID_{输入要素名称}", f"FID_{联合要素名称}"]
            with 游标类.游标创建("更新", 联合后要素路径, 操作字段列表1) as 游标:
                for 数据x in 游标类.属性获取_数据_字典形式(游标, 操作字段列表1):
                    if 数据x[f"FID_{联合要素名称}"] == -1 and 是否去除输入有联合无的部分:
                        游标类.行删除(游标)
                    if 数据x[f"FID_{输入要素名称}"] == -1 and 是否去除输入无联合有的部分:
                        游标类.行删除(游标)
                    if 数据x[f"FID_{输入要素名称}"] != -1 and 数据x[f"FID_{联合要素名称}"] != -1 and 是否去除输入有联合有的部分:
                        游标类.行删除(游标)

        if 输出字段设置 == "仅第一个要素字段":
            要素类.字段删除(联合后要素路径, 保留字段名称列表=输入要素字段名称列表)
        elif 输出字段设置 == "仅FID字段":
            要素类.字段删除(联合后要素路径, 保留字段名称列表=[f"FID_{输入要素名称}", f"FID_{联合要素名称}"])
        elif 输出字段设置 == "除FID外所有字段":
            要素类.字段删除(联合后要素路径, [f"FID_{输入要素名称}", f"FID_{联合要素名称}", "ORIG_FID"])
        输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(联合后要素路径, 输出要素路径)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过融合(输入要素路径, 融合字段列表=[], 统计字段列表=None, 是否单部件=True, 是否计算面积字段=False, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        if 是否单部件 == True:
            是否单部件 = "SINGLE_PART"
        else:
            是否单部件 = "MULTI_PART"
        arcpy.management.Dissolve(in_features=输入要素路径, out_feature_class=输出要素路径, dissolve_field=融合字段列表, statistics_fields=统计字段列表, multi_part=是否单部件, unsplit_lines="DISSOLVE_LINES", concatenation_separator="")  # type: ignore
        if 是否计算面积字段:
            要素类.字段添加_添加面积字段(输出要素路径)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过更新(输入要素路径, 更新要素路径, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 更新要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.analysis.Update(输入要素路径, 更新要素路径, 输出要素路径)  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过更新并合并字段(输入要素路径, 更新要素路径, 是否多部件转单部件=True, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 更新要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        输出 = 要素类.要素创建_通过擦除(输入要素路径, 更新要素路径, 是否多部件转单部件=是否多部件转单部件)
        输出要素路径 = 要素类.要素创建_通过合并([输出, 更新要素路径], 输出要素路径)
        return 输出要素路径

    @staticmethod
    def 要素创建_通过筛选(输入要素路径, SQL语句="地类编号 LIKE '01%'", 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.analysis.Select(in_features=输入要素路径, out_feature_class=输出要素路径, where_clause=SQL语句)  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过排序(输入要素路径, 排序字段及顺序列表=[["DATE_REP", "正序"]], 空间排序方式="UR", 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        排序字段及顺序列表temp = []
        for x in 排序字段及顺序列表:
            if x[1] == "ASCENDING" or x[1] == "正序":
                排序字段及顺序列表temp.append([x[0], "ASCENDING"])
            elif x[1] == "DESCENDING" or x[1] == "倒序":
                排序字段及顺序列表temp.append([x[0], "DESCENDING"])
        排序字段及顺序列表 = 排序字段及顺序列表temp
        arcpy.management.Sort(in_dataset=输入要素路径, out_dataset=输出要素路径, sort_field=排序字段及顺序列表, spatial_sort_method=空间排序方式)  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过多部件至单部件(输入要素路径, 清除ORIG_FID=True, 输出要素路径="内存临时"):
        from bxpy.基本对象包 import 字类

        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.management.MultipartToSinglepart(in_features=输入要素路径, out_feature_class=输出要素路径)  # type: ignore
        if 清除ORIG_FID:
            要素类.字段删除(输出要素路径, ["ORIG_FID"])
        return 输出要素路径

    @staticmethod
    def 要素创建_通过空间连接(输入要素路径, 连接要素路径, 连接方式: Literal["相交", "包含连接要素", "完全包含连接要素", "在连接要素内", "完全在连接要素内", "包含连接要素内点", "内点在连接要素内", "形心在连接要素内", "大部分在连接要素内"] = "包含连接要素", 输出要素路径="内存临时"):
        日志生成器.临时关闭日志()
        _连接方式映射表 = {"相交": "INTERSECT", "包含连接要素": "CONTAINS", "完全包含连接要素": "COMPLETELY_CONTAINS", "在连接要素内": "WITHIN", "完全在连接要素内": "COMPLETELY_WITHIN", "形心在连接要素内": "HAVE_THEIR_CENTER_IN", "大部分在连接要素内": "LARGEST_OVERLAP"}
        连接方式raw = _连接方式映射表[连接方式] if 连接方式 in _连接方式映射表 else 连接方式

        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 连接要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        if 连接方式raw == "包含连接要素内点":
            arcpy.management.RepairGeometry(in_features=连接要素路径, delete_null="DELETE_NULL", validation_method="ESRI")[0]  # type: ignore
            连接要素路径_转点后 = 要素类.要素创建_通过转点(连接要素路径)
            # 连接要素转内点后名称 = arcpy.management.FeatureToPoint(in_features=连接要素名称, out_feature_class="in_memory\\AA_要素转点" + "_" + 工具集.生成SUUID(), point_location="INSIDE")
            # return 输入要素路径.要素创建_通过空间连接(连接要素路径_转点后.名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
            return 要素类.要素创建_通过空间连接(输入要素路径, 连接要素路径_转点后, 输出要素路径=输出要素路径, 连接方式="包含连接要素")
        if 连接方式raw == "内点在连接要素内":
            arcpy.management.RepairGeometry(in_features=输入要素路径, delete_null="DELETE_NULL", validation_method="ESRI")[0]  # type: ignore
            目标要素路径 = 要素类.要素创建_通过复制(输入要素路径)
            目标要素路径_转点后 = 要素类.要素创建_通过转点(目标要素路径)

            # 日志类.输出控制台(f"目标要素转点后要素字段列表{目标要素转点后要素.字段名称列表获取()}")
            # 日志类.输出控制台(f"目标要素名称{目标要素.名称_无路径}")
            目标要素路径_转点后_带连接要素字段 = 要素类.要素创建_通过空间连接(目标要素路径_转点后, 连接要素路径, "在连接要素内")
            if 日志生成器.属性获取_当前函数内日志开启状态():
                要素类.要素创建_通过复制并重命名重名要素(目标要素路径_转点后_带连接要素字段, "AA_内点与连接要素空间连接后")
                日志生成器.输出并暂停("内点与连接要素空间连接后")

            保留字段名称列表raw = 要素类.字段名称列表获取(连接要素路径, False)
            目标要素名称 = 要素类.属性获取_要素名称(目标要素路径)
            保留字段名称列表raw.append("FID_" + 目标要素名称)
            要素类.字段删除(目标要素路径_转点后_带连接要素字段, 保留字段名称列表=保留字段名称列表raw)
            连接要素字段列表 = 要素类.字段列表获取(连接要素路径, False)

            for x in 连接要素字段列表:
                要素类.字段添加_通过字段对象(目标要素路径, x)

            from bxarcpy.游标包 import 游标类

            目标要素操作字段列表 = ["_ID", *要素类.字段名称列表获取(连接要素路径, False)]
            目标要素转点后操作字段列表 = 要素类.字段名称列表获取(目标要素路径_转点后_带连接要素字段, False)
            with 游标类.游标创建("更新", 目标要素路径, 目标要素操作字段列表) as 面要素游标对象:  # type: ignore
                with 游标类.游标创建("查询", 目标要素路径_转点后_带连接要素字段, 目标要素转点后操作字段列表) as 点要素游标对象:
                    for x in 游标类.属性获取_数据_字典形式(面要素游标对象, 目标要素操作字段列表):
                        findFlag = False
                        for y in 游标类.属性获取_数据_字典形式(点要素游标对象, 目标要素转点后操作字段列表):
                            if int(x["_ID"]) == y["FID_" + 目标要素名称]:
                                y["_ID"] = x["_ID"]
                                del y["FID_" + 目标要素名称]
                                游标类.行更新_字典形式(面要素游标对象, y, 目标要素操作字段列表)
                                findFlag = True
                                break
                        if findFlag == False:
                            日志生成器.输出信息(f'未找到ID为{x["_ID"]}的对象所对应的点')

            输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(目标要素路径, 输出要素路径)
            # ret = self.要素创建_通过空间连接(目标要素连接后.名称, 输出要素名称=输出要素名称, 连接方式="包含连接要素")
            # print("ret" + str(ret.字段名称列表获取()))

            return 输出要素路径
        arcpy.analysis.SpatialJoin(  # type: ignore
            target_features=输入要素路径,
            join_features=连接要素路径,
            out_feature_class=输出要素路径,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            # field_mapping='Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,YD_用地\\YD_不动产登记2,Shape_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0,First,#,YD_用地\\YD_不动产登记2,Shape_Area,-1,-1;地类编号 "地类编号" true true false 50 Text 0 0,First,#,YD_用地\\YD_不动产登记2,地类编号,0,50;Shape_Length_1 "Shape_Length" true true true 8 Double 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,Shape_Length,-1,-1;Shape_Area_1 "Shape_Area" true true true 8 Double 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,Shape_Area,-1,-1;地类编号_1 "地类编号" true true false 100 Text 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,地类编号,0,100;ORIG_FID "ORIG_FID" true true false 0 Long 0 0,First,#,C:\\Users\\common\\project\\F富阳受降控规\\受降北_数据库.gdb\\YD_不动产登记2_FeatureToPoint,ORIG_FID,-1,-1',
            match_option=连接方式raw,
            search_radius="",
            distance_field_name="",
        )
        return 输出要素路径

    @staticmethod
    def 要素创建_通过填充空隙(输入要素路径, 填充范围要素路径, 填充地类编号表达式='"00"', 输出要素路径="内存临时"):
        # 常用_填充空隙后
        # To allow overwriting outputs change overwriteOutput option to True.
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径, 填充范围要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        # Process: 复制要素 (复制要素) (management)

        输入要素路径_temp = 要素类.要素创建_通过复制(输入要素路径)
        填充范围要素路径_temp = 要素类.要素创建_通过复制(填充范围要素路径)
        要素类.字段添加(填充范围要素路径_temp, "地类编号")
        要素类.字段计算(填充范围要素路径_temp, "地类编号", 填充地类编号表达式)
        更新后要素路径_temp = 要素类.要素创建_通过更新(输入要素路径_temp, 填充范围要素路径_temp)
        更新后要素路径 = 要素类.要素创建_通过更新(更新后要素路径_temp, 输入要素路径_temp)
        输出要素 = 要素类.要素创建_通过复制并重命名重名要素(更新后要素路径, 输出要素路径)
        return 输出要素

    @staticmethod
    def 要素创建_通过切分(输入要素路径, 折点数量=200, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.management.Dice(输入要素路径, 输出要素路径, 折点数量)  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过转点(输入要素路径, 输出要素路径="内存临时"):
        from bxarcpy.游标包 import 游标类

        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        点要素路径 = 要素类.要素创建_通过名称("内存临时", "点", 输入要素路径, "内存临时")
        输入要素名称 = 要素类.属性获取_要素名称(输入要素路径)

        要素类.字段添加(点要素路径, "FID_" + 输入要素名称, "长整型")

        字段列表 = 要素类.字段名称列表获取(输入要素路径)
        删除列表 = ["OBJECTID", "Shape", "Shape_Length", "Shape_Area", "OID", "SHAPE"]
        for x in 删除列表:
            if x in 字段列表:
                字段列表.remove(x)

        字段列表.insert(0, "_ID")
        字段列表.insert(0, "_形状")
        # print(字段列表)

        点字段列表 = [x for x in 字段列表]
        点字段列表.pop(1)
        点字段列表.insert(0, "FID_" + 输入要素名称)

        # print(点字段列表)
        with 游标类.游标创建("查询", 输入要素路径, 字段列表) as 面要素游标对象:
            with 游标类.游标创建("插入", 点要素路径, 点字段列表) as 点要素游标对象:
                from bxarcpy.几何包 import 几何类

                for 面要素x in 游标类.属性获取_数据_字典形式(面要素游标对象, 字段列表):
                    try:
                        # 日志类.输出调试(f"x[0]是{x[0]._内嵌对象}")
                        构造字典 = 面要素x
                        构造字典["_形状"] = 几何类.属性获取_内点(面要素x["_形状"])
                        构造字典["FID_" + 输入要素名称] = 面要素x["_ID"]
                        del 构造字典["_ID"]
                        # 日志类.输出调试(f"内点是{内点}")
                        游标类.行插入_字典形式(点要素游标对象, 构造字典, 点字段列表)
                    except Exception as e:
                        print(f"内点获取发生错误：{e}")
                        print(f"ID为 {面要素x['_ID']} 的对象无法获取到内点，取了端点")
                        构造字典 = 面要素x
                        构造字典["_形状"] = 几何类.属性获取_折点列表(构造字典["_形状"])[0][0]
                        构造字典["FID_" + 输入要素名称] = 面要素x["_ID"]
                        del 构造字典["_ID"]
                        # 日志类.输出调试(f"端点是{端点}")
                        游标类.行插入_字典形式(点要素游标对象, 构造字典)
        return 要素类.要素创建_通过复制并重命名重名要素(点要素路径, 输出要素路径)

    @staticmethod
    def 要素创建_通过转线(输入要素路径, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        arcpy.management.FeatureToLine(in_features=输入要素路径, out_feature_class=输出要素路径)  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过面转线(输入要素路径, 是否识别并存储面邻域信息=True, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        if 是否识别并存储面邻域信息:
            arcpy.management.PolygonToLine(in_features=输入要素路径, out_feature_class=输出要素路径, neighbor_option="IDENTIFY_NEIGHBORS")  # type: ignore
        else:
            arcpy.management.PolygonToLine(in_features=输入要素路径, out_feature_class=输出要素路径, neighbor_option="IGNORE_NEIGHBORS")  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过缓冲(输入要素路径, 距离或字段名称, 融合类型="不融合", 融合字段名称列表=None, 末端类型="圆形", 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        _融合类型映射表 = {"不融合": "NONE", "NONE": "NONE", "融合为单个": "ALL", "ALL": "ALL", "融合按字段": "LIST", "LIST": "LIST"}
        融合类型 = _融合类型映射表[融合类型]
        _末端类型映射表 = {"圆形": "ROUND", "ROUND": "ROUND", "方形": "FLAT", "FLAT": "FLAT"}
        末端类型 = _末端类型映射表[末端类型]
        if 融合字段名称列表:
            融合字段名称列表 = ";".join(融合字段名称列表)
        arcpy.analysis.Buffer(in_features=输入要素路径, out_feature_class=输出要素路径, buffer_distance_or_field=距离或字段名称, line_side="FULL", line_end_type=末端类型, dissolve_option=融合类型, dissolve_field=融合字段名称列表, method="PLANAR")  # type: ignore
        return 输出要素路径

    @staticmethod
    def 要素创建_通过增密(输入要素路径, 增密方法: Literal["固定距离", "偏转距离", "偏转角度"] = "偏转距离", 固定距离="10 Meters", 偏转距离="0.0001 Meters", 偏转角度=1, 最大折点计数=None, 输出要素路径="内存临时"):
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        _增密方法映射 = {"固定距离": "DISTANCE", "偏转距离": "OFFSET", "偏转角度": "ANGLE"}

        复制后要素路径 = 要素类.要素创建_通过复制(输入要素路径, 输出要素路径)
        增密方法raw = _增密方法映射[增密方法] if 增密方法 in _增密方法映射 else 增密方法
        arcpy.edit.Densify(in_features=复制后要素路径, densification_method=增密方法raw, distance=固定距离, max_deviation=偏转距离, max_angle=偏转角度, max_vertex_per_segment=最大折点计数)  # type: ignore
        return 复制后要素路径

    @staticmethod
    def 要素创建_通过投影定义(输入要素路径, 坐标系='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', 输出要素路径="内存临时"):
        # 坐标系有效值可以是 SpatialReference 对象、扩展名为 .prj 的文件或坐标系的字符串表达形式。
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

        复制后要素路径 = 要素类.要素创建_通过复制(输入要素路径)
        arcpy.management.DefineProjection(in_dataset=复制后要素路径, coor_system=坐标系)  # type: ignore
        ret = 要素类.要素创建_通过复制并重命名重名要素(复制后要素路径, 输出要素路径)
        return ret

    @staticmethod
    def 要素创建_通过投影转换(输入要素路径, 输出坐标系='PROJCS["CGCS2000_3_Degree_GK_CM_120E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",120.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]', 输出要素路径="内存临时"):
        # 坐标系有效值可以是 SpatialReference 对象、扩展名为 .prj 的文件或坐标系的字符串表达形式。
        输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径
        
        输入要素唯一路径 = 输出路径生成_当采用临时工作空间临时时([输入要素路径])
        复制后要素路径 = 要素类.要素创建_通过复制(输入要素路径, 输入要素唯一路径)

        输出要素唯一路径 = 输出路径生成_当采用临时工作空间临时时([输入要素路径]) + "1"
        arcpy.management.Project(in_dataset=复制后要素路径, out_dataset=输出要素唯一路径, out_coor_system=输出坐标系, transform_method=None, in_coor_system=None, preserve_shape="NO_PRESERVE_SHAPE", max_deviation=None, vertical="NO_VERTICAL")  # type: ignore
        ret = 要素类.要素创建_通过复制并重命名重名要素(输出要素唯一路径, 输出要素路径)
        要素类.要素删除(输出要素唯一路径)
        要素类.要素删除(输入要素唯一路径)
        return ret

    @staticmethod
    def 要素删除(要素路径):
        return arcpy.management.Delete(in_data=要素路径, data_type="")[0]  # type: ignore

    @staticmethod
    def 要素删除_通过要素名称列表(要素路径列表):
        return arcpy.management.Delete(in_data=要素路径列表, data_type="")[0]  # type: ignore

    @staticmethod
    def 要素重命名(要素路径, 新要素路径):
        arcpy.management.Rename(要素路径, 新要素路径)  # type: ignore
        return 新要素路径

    @staticmethod
    def 选择集创建_通过属性(输入要素路径, 选择方式="新建选择集", SQL语句=""):
        _选择方式映射表 = {"新建选择集": "NEW_SELECTION", "NEW_SELECTION": "NEW_SELECTION"}
        选择方式 = _选择方式映射表[选择方式]
        a = arcpy.management.SelectLayerByAttribute(in_layer_or_view=输入要素路径, selection_type=选择方式, where_clause=SQL语句, invert_where_clause="")[0]  # type: ignore
        # 返回是图层
        return a

    @staticmethod
    def 字段列表获取(输入要素路径, 含系统字段=True):
        if 含系统字段:
            字段列表 = [x for x in arcpy.ListFields(输入要素路径)]  # type: ignore
        else:
            字段列表 = [x for x in arcpy.ListFields(输入要素路径)]  # type: ignore
            字段列表 = [x for x in 字段列表 if 字段类.属性获取_名称(x) not in ["OBJECTID", "OBJECTID_1", "Shape", "Shape_1", "Shape_Length", "Shape_Length_1", "Shape_Area", "Shape_Area_1", "OID", "SHAPE"]]
        return 字段列表

    @staticmethod
    def 字段名称列表获取(输入要素路径, 含系统字段=True):
        字段列表 = 要素类.字段列表获取(输入要素路径, 含系统字段)
        return [字段类.属性获取_名称(x) for x in 字段列表]

    @staticmethod
    def 字段删除(输入要素路径, 删除字段名称列表=None, 保留字段名称列表=None, 忽略系统字段=True):
        from bxpy.日志包 import 日志生成器

        字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
        if 删除字段名称列表 != None:
            # 日志类.输出控制台(f"即将被删除的字段为：" + str(删除字段名称列表))
            if 忽略系统字段:
                一般不删除的字段名称列表 = ["OID", "OBJECTID", "OBJECTID_1", "Shape", "Shape_Area", "Shape_Length", "SHAPE"]
                for x in 一般不删除的字段名称列表:
                    if x in 删除字段名称列表:
                        删除字段名称列表.remove(x)
            删除字段名称列表 = [x for x in 删除字段名称列表 if x in 字段名称列表]
            if 删除字段名称列表:
                arcpy.management.DeleteField(in_table=输入要素路径, drop_field=删除字段名称列表, method="DELETE_FIELDS")[0]  # type: ignore
        if 保留字段名称列表 != None:
            字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
            # 日志类.输出调试(f"要素拥有的所有字段为：" + str(字段名称列表))
            if 忽略系统字段:
                保留字段名称列表.extend(["OID", "OBJECTID", "OBJECTID_1", "Shape", "Shape_Area", "Shape_Length", "SHAPE"])
            for x in 保留字段名称列表:
                if x in 字段名称列表:
                    字段名称列表.remove(x)
            # 日志类.输出调试(f"即将被删除的字段为：" + str(字段名称列表))
            if len(字段名称列表) > 0:
                arcpy.management.DeleteField(in_table=输入要素路径, drop_field=字段名称列表, method="DELETE_FIELDS")[0]  # type: ignore
        return 输入要素路径

    @staticmethod
    def 字段添加(输入要素路径, 字段名称, 字段类型: Literal["字符串", "双精度", "长整型", "短整型", "日期", "单精度", "对象ID", "定长字符串", "GUID"] = "字符串", 字段长度: Union[None, int] = 100, 字段别称="", 删除既有字段=True):
        """
        如果输入表是文件地理数据库，则将忽略字段精度值和小数位数值。
        """
        # 日志类.输出调试(f"字段类型：{字段类型}")
        字段类型raw = 枚举类.字段类型.值获取(字段类型)
        # 日志类.输出调试(f"字段类型raw：{字段类型raw}")
        if 删除既有字段:
            arcpy.management.DeleteField(in_table=输入要素路径, drop_field=[字段名称], method="DELETE_FIELDS")  # type: ignore

        字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
        if 字段名称 not in 字段名称列表:
            arcpy.management.AddField(in_table=输入要素路径, field_name=字段名称, field_type=字段类型raw, field_precision=None, field_scale=None, field_length=字段长度, field_alias=字段别称, field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")  # type: ignore
        else:
            from bxarcpy.环境包 import 输入输出类

            输入输出类.输出消息(f"{输入要素路径}中已存在{字段名称}字段，不再添加")

        return 输入要素路径

    @staticmethod
    def 字段添加_字符串(输入要素路径, 字段名称, 字段长度: Union[None, int] = 255, 字段别称="", 删除既有字段=True):
        return 要素类.字段添加(输入要素路径=输入要素路径, 字段名称=字段名称, 字段类型="字符串", 字段长度=字段长度, 字段别称=字段别称, 删除既有字段=删除既有字段)

    @staticmethod
    def 字段添加_双精度(输入要素路径, 字段名称, 字段长度: Union[None, int] = 100, 字段别称="", 删除既有字段=True):
        return 要素类.字段添加(输入要素路径=输入要素路径, 字段名称=字段名称, 字段类型="双精度", 字段长度=字段长度, 字段别称=字段别称, 删除既有字段=删除既有字段)

    @staticmethod
    def 字段添加_添加面积字段(输入要素路径, 强制重生成=True):
        字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
        if "Shape_Area" not in 字段名称列表 or 强制重生成:
            要素类.字段添加_双精度(输入要素路径, "Shape_Area")
            from bxarcpy.游标包 import 游标类

            with 游标类.游标创建("更新", 输入要素路径, ["_面积", "Shape_Area"]) as 游标:
                for 游标x in 游标类.属性获取_数据_字典形式(游标, ["_面积", "Shape_Area"]):
                    游标x["Shape_Area"] = 游标x["_面积"]
                    游标类.行更新_字典形式(游标, 游标x)

    @staticmethod
    def 字段添加_通过字段对象(输入要素路径, 字段对象):
        字段名称 = 字段类.属性获取_名称(字段对象)
        字段类型 = 字段类.属性获取_类型(字段对象)
        字段长度 = 字段类.属性获取_长度(字段对象)
        字段别称 = 字段类.属性获取_别称(字段对象)
        要素类.字段添加(输入要素路径, 字段名称=字段名称, 字段类型=字段类型, 字段长度=字段长度, 字段别称=字段别称)
        return 输入要素路径

    @staticmethod
    def 字段计算(输入要素路径, 字段名称, 表达式, 字段类型="字符串", 语言类型="PYTHON3", 代码块=""):
        字段类型 = 枚举类.字段类型.值获取(字段类型)
        arcpy.management.CalculateField(in_table=输入要素路径, field=字段名称, expression=表达式, expression_type=语言类型, code_block=代码块, field_type=字段类型, enforce_domains="NO_ENFORCE_DOMAINS")[0]  # type: ignore
        return 输入要素路径

    @staticmethod
    def 字段修改(输入要素路径, 字段名称=None, 修改后字段名称=None, 修改后字段别称=None, 字段类型=None, 字段长度=None, 字段是否可为空: Literal["NULLABLE", None] = None, 清除字段别称=True):
        if 字段类型:
            字段类型 = 枚举类.字段类型.值获取(字段类型)
        arcpy.management.AlterField(in_table=输入要素路径, field=字段名称, new_field_name=修改后字段名称, new_field_alias=修改后字段别称, field_type=字段类型, field_length=字段长度, field_is_nullable=字段是否可为空, clear_field_alias=清除字段别称)[0]  # type: ignore
        return 输入要素路径

    @staticmethod
    def 字段排序(输入要素路径, 字段名称顺序列表, 字段放置于尾部=True):
        if 字段放置于尾部:
            from bxpy.基本对象包 import 字类

            字段列表 = 要素类.字段列表获取(输入要素路径=输入要素路径)
            for 字段名称 in 字段名称顺序列表:
                字段对象 = [x for x in 字段列表 if 字段类.属性获取_名称(x) == 字段名称][0]
                随机新字段名称 = f"{字段名称}_{字类.字符串生成_短GUID()}"
                要素类.字段添加(
                    输入要素路径,
                    随机新字段名称,
                    字段类型=字段类.属性获取_类型(字段对象),
                    字段长度=字段类.属性获取_长度(字段对象),
                )
                要素类.字段计算(输入要素路径, 随机新字段名称, f"!{字段名称}!")
                要素类.字段删除(输入要素路径, [字段名称])
                要素类.字段修改(输入要素路径, 随机新字段名称, 字段名称)
        else:
            字段名称列表 = 要素类.字段名称列表获取(输入要素路径=输入要素路径, 含系统字段=False)
            for x in 字段名称列表:
                if x not in 字段名称顺序列表:
                    字段名称顺序列表.append(x)
            要素类.字段排序(输入要素路径, 字段名称顺序列表)
        return 输入要素路径

    @staticmethod
    def 统计(输入要素路径, 需统计字段及统计方式列表=[{"字段名称": "", "统计方式": "求和"}], 分组字段列表=["字段1"], 是否显示进度条=False):
        from bxarcpy.游标包 import 游标类
        from bxpy.进度条包 import 进度条类
        from bxpy.基本对象包 import 浮类

        需操作的字段名称列表 = []

        for x in 需统计字段及统计方式列表:
            需操作的字段名称列表.append(x["字段名称"])
        for x in 分组字段列表:
            需操作的字段名称列表.append(x)
        with 游标类.游标创建(游标类型="查询", 输入要素路径=输入要素路径, 需操作的字段名称列表=需操作的字段名称列表) as 游标:
            # 导入有序字典
            返回数据temp = {}
            if 是否显示进度条:
                进度条 = 进度条类.进度条创建(总进度=要素类.属性获取_几何数量(输入要素路径))
            for 游标x in 游标类.属性获取_数据_字典形式(游标, 需操作的字段名称列表):
                if 是否显示进度条:
                    进度条类.更新(进度条, 1)
                分组字符串 = ""
                if len(分组字段列表) == 0:
                    数据字典 = 返回数据temp.setdefault("无分组", {})
                    for i, y in enumerate(需统计字段及统计方式列表):
                        数据列表 = 数据字典.setdefault(y["字段名称"], [])
                        数据列表.append(游标x[y["字段名称"]])
                for i, x in enumerate(分组字段列表):
                    分组字符串 = 分组字符串 + str(游标x[分组字段列表[i]]) + "||"
                    数据字典 = 返回数据temp.setdefault(分组字符串[:-2], {})
                    for i, y in enumerate(需统计字段及统计方式列表):
                        数据列表 = 数据字典.setdefault(y["字段名称"], [])
                        数据列表.append(游标x[y["字段名称"]])
            for k, v in 返回数据temp.items():
                for x in 需统计字段及统计方式列表:
                    if x["统计方式"] == "求和":
                        v[x["字段名称"]] = sum([浮类.转换_到浮(x) for x in v[x["字段名称"]]])
            from collections import OrderedDict

            最终返回数据 = OrderedDict(返回数据temp)
            最终返回数据 = OrderedDict(sorted(最终返回数据.items()))
        return 最终返回数据

    @staticmethod
    def 连接创建(输入要素路径, 输入要素连接字段名称=None, 连接要素路径=None, 连接要素连接字段名称=None):
        arcpy.management.AddJoin(in_layer_or_view=输入要素路径, in_field=输入要素连接字段名称, join_table=连接要素路径, join_field=连接要素连接字段名称, join_type="KEEP_ALL", index_join_fields="NO_INDEX_JOIN_FIELDS")[0]  # type: ignore
        return 输入要素路径

    @staticmethod
    def 连接取消(输入要素名称, 连接要素名称):
        arcpy.management.RemoveJoin(in_layer_or_view=输入要素名称, join_name=连接要素名称)[0]  # type: ignore
        return 输入要素名称

    @staticmethod
    def 转换_到CAD(输入要素名称, 输出路径):
        return arcpy.conversion.ExportCAD(in_features=输入要素名称, Output_Type="DWG_R2010", Output_File=输出路径, Ignore_FileNames="Ignore_Filenames_in_Tables", Append_To_Existing="Overwrite_Existing_Files", Seed_File="")  # type: ignore

    @staticmethod
    def 转换_到要素(输入要素路径, 输出要素路径):
        # arcpy.conversion.FeatureClassToFeatureClass(in_features=self.名称, out_path=输出目录, out_name=输出文件名, where_clause="", field_mapping="", config_keyword="")[0]
        arcpy.conversion.ExportFeatures(in_features=输入要素路径, out_features=输出要素路径, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping=None, sort_field=[])  # type: ignore
        return 输出要素路径

    @staticmethod
    def 转换_到numpy(输入要素路径, 需操作的字段名称列表, 返回字典形式=True, 自动创建缺失的字段=True, SQL语句="", 空间参考=None, 降维为点=False, 跳过使用空值的记录=False, 在判断是否跳过使用空值的记录前替换空值=None):
        # arcpy.conversion.FeatureClassToFeatureClass(in_features=self.名称, out_path=输出目录, out_name=输出文件名, where_clause="", field_mapping="", config_keyword="")[0]
        if "*" in 需操作的字段名称列表:
            需操作的字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
        所有字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
        缺失的字段 = [字段名称 for 字段名称 in 需操作的字段名称列表 if 字段名称 not in 所有字段名称列表 and 字段名称 not in 特殊字段_枚举.keys() and 字段名称 not in 特殊字段_枚举.values()]
        if len(缺失的字段) > 0:
            if 自动创建缺失的字段:
                from bxarcpy.环境包 import 输入输出类

                输入输出类.输出消息(f"{输入要素路径}缺少以下字段：{缺失的字段}，将自动创建", 级别="警告")

                for 缺失的字段x in 缺失的字段:
                    要素类.字段添加(输入要素路径, 缺失的字段x)
            else:
                raise Exception(f"{输入要素路径}缺少以下字段：{缺失的字段}")

        需操作的字段名称列表temp = []
        for x in 需操作的字段名称列表:
            if x in 特殊字段_枚举:
                需操作的字段名称列表temp.append(特殊字段_枚举[x])
            else:
                需操作的字段名称列表temp.append(x)
        需操作的字段名称列表raw = 需操作的字段名称列表temp

        if SQL语句 == "":
            ret = arcpy.da.FeatureClassToNumPyArray(输入要素路径, 需操作的字段名称列表raw, spatial_reference=空间参考, explode_to_points=降维为点, skip_nulls=跳过使用空值的记录, null_value=在判断是否跳过使用空值的记录前替换空值)  # type: ignore
        else:
            ret = arcpy.da.FeatureClassToNumPyArray(输入要素路径, 需操作的字段名称列表raw, where_clause=SQL语句, spatial_reference=空间参考, explode_to_points=降维为点, skip_nulls=跳过使用空值的记录, null_value=在判断是否跳过使用空值的记录前替换空值)  # type: ignore
        if not 返回字典形式:
            return ret
        else:
            字段信息字典 = ret.dtype.fields
            字段定义 = [[x[0], 字段信息字典[x[1]][0], 字段信息字典[x[1]][1]] for x in zip(需操作的字段名称列表, 需操作的字段名称列表raw)]
            return [dict(zip(需操作的字段名称列表, x)) for x in ret], 字段定义

    @staticmethod
    def 转换_从numpy(输入要素路径, numpy数据或字典列表, 匹配字段名称对=[], 字段定义=None, 只添加字段不更新既有字段=False):
        if isinstance(numpy数据或字典列表, dict):
            if 字段定义 is None:
                raise Exception("字段定义为空时，numpy数据或字典列表 参数只接受numpy数据")
            numpy数据或字典列表temp = []
            for 字典x in numpy数据或字典列表:
                列表temp = []
                for 字段定义x in 字段定义:
                    列表temp.append(字典x[字段定义x[0]])
                numpy数据或字典列表temp.append(tuple(列表temp))
            from bxarcpy.枚举包 import 特殊字段_枚举

            字段定义temp = []
            for 字段定义x in 字段定义:
                if 字段定义x[0] in 特殊字段_枚举:
                    字段定义temp.append((特殊字段_枚举[字段定义x[0]], 字段定义x[1], 字段定义x[2]))
                else:
                    字段定义temp.append((字段定义x[0], 字段定义x[1], 字段定义x[2]))

            import numpy

            numpy数据或字典列表 = numpy.array(numpy数据或字典列表temp, dtype=numpy.dtype(字段定义temp))

        匹配字段名称对temp = []
        for 匹配字段名称对x in 匹配字段名称对:
            if 匹配字段名称对x in 特殊字段_枚举:
                匹配字段名称对temp.append(特殊字段_枚举[匹配字段名称对x])
            else:
                匹配字段名称对temp.append(匹配字段名称对x)
        匹配字段名称对 = 匹配字段名称对temp

        return arcpy.da.ExtendTable(输入要素路径, 匹配字段名称对[0], numpy数据或字典列表, 匹配字段名称对[1], 只添加字段不更新既有字段)  # type: ignore

    @staticmethod
    def 拓扑检查重叠(输入要素名称, 是否导出到CAD=None):
        要素类.拓扑检查重叠_通过要素名称列表([输入要素名称], 是否导出到CAD=是否导出到CAD)

    @staticmethod
    def 拓扑检查重叠_通过要素名称列表(输入要素路径列表, 是否导出到CAD=None):
        日志生成器.临时关闭日志()
        from bxarcpy.要素数据集包 import 要素数据集类
        from bxarcpy.拓扑包 import 拓扑类
        from bxpy.进度条包 import 进度条类
        from bxpy.基本对象包 import 字类
        from bxarcpy.工具包 import 生成当前时间_微秒

        要素数据集路径 = 要素数据集类.要素数据集创建("拓扑检查", 删除既有同名要素数据集=False)
        拓扑路径 = 拓扑类.拓扑创建(要素数据集路径, "拓扑_" + 生成当前时间_微秒())
        进度条 = 进度条类.进度条创建(输入要素路径列表, 前置信息="开始拓扑检查")
        for 输入要素路径x in 进度条:
            进度条类.后置信息设置(进度条, {"当前操作的要素": 输入要素路径x})
            日志生成器.输出调试(f"开始对以下要素类进行拓扑检查：{输入要素路径x}")
            输入要素名称x = 要素类.属性获取_要素名称(输入要素路径x)
            要素数据集中的要素路径 = 要素类.转换_到要素(输入要素路径x, 要素数据集路径 + "\\" + 输入要素名称x + "_拓扑检查_" + 生成当前时间_微秒())
            # 日志类.输出调试(f"准备添加要素的名称是：{要素数据集中的要素.名称}")
            拓扑类.拓扑中添加要素(拓扑路径, 要素数据集中的要素路径)
            # 日志类.输出调试(f"准备添加要素的类型是：{要素类.属性获取_几何类型(要素数据集中的要素路径)}")
            if 要素类.属性获取_几何类型(要素数据集中的要素路径) == "面":
                拓扑类.拓扑中添加规则(拓扑路径, 要素数据集中的要素路径, "面无重叠")
            elif 要素类.属性获取_几何类型(要素数据集中的要素路径) == "线":
                拓扑类.拓扑中添加规则(拓扑路径, 要素数据集中的要素路径, "线无重叠")
                拓扑类.拓扑中添加规则(拓扑路径, 要素数据集中的要素路径, "线无自重叠")
        拓扑类.拓扑验证(拓扑路径)
        拓扑导出后要素1路径, 拓扑导出后要素2路径, 拓扑导出后要素3路径 = 拓扑类.转换_到要素(拓扑路径, "AA_拓扑导出后要素")
        from bxarcpy.环境包 import 输入输出类

        if 要素类.属性获取_几何数量(拓扑导出后要素3路径) > 0:
            输入输出类.输出消息(f"拓扑检查存在面错误")
            if 是否导出到CAD:
                单部件路径 = 要素类.要素创建_通过多部件至单部件(拓扑导出后要素3路径)
                要素类.转换_到CAD(单部件路径, r"AA_拓扑_面.dwg")

        if 要素类.属性获取_几何数量(拓扑导出后要素2路径) > 0:
            输入输出类.输出消息(f"拓扑检查存在线错误")
            if 是否导出到CAD:
                单部件路径 = 要素类.要素创建_通过多部件至单部件(拓扑导出后要素2路径)
                要素类.转换_到CAD(单部件路径, r"AA_拓扑_线.dwg")

        if 要素类.属性获取_几何数量(拓扑导出后要素1路径) > 0:
            输入输出类.输出消息(f"拓扑检查存在点错误")
            if 是否导出到CAD:
                单部件路径 = 要素类.要素创建_通过多部件至单部件(拓扑导出后要素1路径)
                要素类.转换_到CAD(单部件路径, r"AA_拓扑_点.dwg")

        if 要素类.属性获取_几何数量(拓扑导出后要素3路径) <= 0 and 要素类.属性获取_几何数量(拓扑导出后要素2路径) <= 0 and 要素类.属性获取_几何数量(拓扑导出后要素1路径) <= 0:
            输入输出类.输出消息(f"拓扑检查没有错误")
        要素类.要素删除(拓扑导出后要素1路径)
        要素类.要素删除(拓扑导出后要素2路径)
        要素类.要素删除(拓扑导出后要素3路径)

    @staticmethod
    def 拓扑检查范围(输入要素路径, 范围要素路径, 是否导出到CAD=None):
        要素类.拓扑检查范围_通过要素名称列表([输入要素路径], 范围要素路径, 是否导出到CAD)

    @staticmethod
    def 拓扑检查范围_通过要素名称列表(输入要素路径列表, 范围要素路径, 是否导出到CAD=None):
        for x in 输入要素路径列表:
            范围要素路径_复制后 = 要素类.要素创建_通过复制(范围要素路径)

            已填色要素名称 = 要素类.属性获取_要素名称(x)
            已填色要素路径_复制后 = 要素类.要素创建_通过复制(x)
            from bxarcpy.环境包 import 输入输出类

            擦除后要素路径 = 要素类.要素创建_通过擦除(范围要素路径_复制后, 已填色要素路径_复制后)
            需填未填要素路径 = 要素类.要素创建_通过多部件至单部件(擦除后要素路径)

            if 要素类.属性获取_几何数量(需填未填要素路径) > 0:
                输入输出类.输出消息(f"【{已填色要素名称}】【{范围要素路径}】之间存在空隙（需填未填）")
                要素类.要素创建_通过复制并重命名重名要素(需填未填要素路径, f"AA_空隙_{已填色要素名称}_{范围要素路径}")
                if 是否导出到CAD:
                    要素类.转换_到CAD(需填未填要素路径, rf"AA_空隙_{已填色要素名称}_{范围要素路径}.dwg")

            擦除后要素路径2 = 要素类.要素创建_通过擦除(已填色要素路径_复制后, 范围要素路径_复制后)
            不需填但被填路径 = 要素类.要素创建_通过多部件至单部件(擦除后要素路径2)
            if 要素类.属性获取_几何数量(不需填但被填路径) > 0:
                输入输出类.输出消息(f"【{已填色要素名称}】【{范围要素路径}】之间存在多余（不需填但被填）")
                要素类.要素创建_通过复制并重命名重名要素(不需填但被填路径, f"AA_多余_{已填色要素名称}_{范围要素路径}")
                if 是否导出到CAD:
                    要素类.转换_到CAD(不需填但被填路径, rf"AA_多余_{已填色要素名称}_{范围要素路径}.dwg")

            if 要素类.属性获取_几何数量(需填未填要素路径) <= 0 and 要素类.属性获取_几何数量(不需填但被填路径) <= 0:
                输入输出类.输出消息(f"【{已填色要素名称}】【{范围要素路径}】之间契合")


class 字段类:
    @staticmethod
    def 属性获取_名称(字段对象):
        return 字段对象.name

    @staticmethod
    def 属性获取_类型(字段对象):
        from bxarcpy.基本对象包 import 枚举类

        return 枚举类.字段类型.名称获取(字段对象.type)

    @staticmethod
    def 属性获取_长度(字段对象):
        return 字段对象.length

    @staticmethod
    def 属性获取_别称(字段对象):
        return 字段对象.aliasName

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
    from bxarcpy.环境包 import 环境管理器类
    from bxpy.基本对象包 import 字类

    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\J江东区临江控规\临江控规_数据库.gdb"
    # 道路中线要素名称 = bxarcpy.环境.输入参数获取_以字符串形式(0, "DL_道路中线", True)
    with 环境管理器类.环境管理器类创建(工作空间):
        # pass
        # 要素1 = 要素类.要素创建_通过复制("KZX_城镇集建区")
        # 要素2 = 要素类.要素创建_通过复制("JX_街坊范围线")
        # 要素类.要素创建_通过分割(要素1, 要素2, "AA_test333")
        print(要素类.要素创建_通过复制("CZ_基本农田"))
        # 返回值 = 要素类.转换_到numpy("DIST_用地规划图1", ["OID@", "地类编号"], 返回字典形式=False)
        # 返回值[0] = (1, "070303333")
        # print(返回值.dtype.keys())  # type: ignore
        # 要素类.转换_从numpy(
        #     "DIST_用地规划图1",
        #     返回值,
        #     ["OID@", "OID@"],
        #     False,
        # )
        # print(返回值)
