from bxarcpy.要素包 import 要素类
from bxpy.日志包 import 日志生成器
from bxpy.元数据包 import 追踪元数据类
from bxarcpy.环境包 import 环境管理器类, 环境类
from bxgis.配置 import 基本信息


def 导入从CAD(输入CAD数据集中的要素类路径=r"C:\Users\beixiao\Desktop\01.dwg\控规地块", 是否拓扑检查=False, 是否范围检查=True, 是否转曲=True, 输出要素路径=r"CZ_CAD色块"):
    日志生成器.临时关闭日志()
    # if 输入CAD图层名称 in ["点", "线", "面"]:
    #     输入CAD图层名称 = bxarcpy.常量._要素类型映射[输入CAD图层名称]

    # 日志类.输出调试(f"当前工作空间{bxarcpy.配置.当前工作空间}")
    # 输出要素集 = bxarcpy.要素数据集类.导入从CAD(输入CAD路径列表, r"AA_CAD导入GEO1")
    # 日志类.输出调试("输出的要素集是：" + 输出要素集.名称 + rf"\{输入CAD图层名称}")

    # 输入要素 = bxarcpy.要素类.要素读取_通过名称(输出要素集.名称 + rf"\{输入CAD图层名称}")

    输入要素名称 = 要素类.属性获取_要素名称(输入CAD数据集中的要素类路径)
    try:
        输入要素路径 = 要素类.要素创建_通过复制(输入CAD数据集中的要素类路径)
    except:
        追踪元数据类.追踪信息获取()
        raise Exception("可能是因为在GIS软件中打开过该文件，所以跳错了，建议关闭GIS软件后再次运行")
    日志生成器.输出调试(f"输入要素名称：{输入要素名称}")
    是否为控规地块flag = True if 输入要素名称 == "控规地块" else False
    输入要素路径 = 要素类.要素创建_通过几何修复(输入要素路径, 是否打印被删除的要素=True)
    输入要素类型 = 要素类.属性获取_几何类型(输入要素路径)

    # 输出要素集.要素数据集删除()
    if 是否转曲 and 输入要素类型 in ["面", "线"]:
        输入要素路径 = 要素类.要素创建_通过增密(输入要素路径)
    if 是否为控规地块flag:
        要素类.字段添加(输入要素路径, 基本信息.地块要素字段映射.地类编号字段名称)
        要素类.字段计算(输入要素路径, 基本信息.地块要素字段映射.地类编号字段名称, "!Layer!.split('#')[0].split('-')[1].replace('／','/')")

    要素类.字段删除(输入要素路径, ["Entity", "Handle", "Layer", "Color", "Linetype", "Elevation", "LineWt", "RefName", "LyrColor", "LyrLnType", "LyrLineWt", "Angle", "LyrFrzn", "LyrLock", "LyrOn", "LyrVPFrzn", "LyrHandle", "EntColor", "BlkColor", "EntLinetype", "BlkLinetype", "Thickness", "EntLineWt", "BlkLineWt", "LTScale", "ExtX", "ExtY", "ExtZ", "DocName", "DocPath", "DocType", "DocVer", "DocUpdate", "DocId", "ScaleX", "ScaleY", "ScaleZ"])

    if 是否拓扑检查 and 输入要素类型 in ["面", "线"]:
        要素类.拓扑检查重叠(输入要素路径)

    if 是否范围检查 and 输入要素类型 in ["面"]:
        from bxarcpy.数据库包 import 数据库类

        当前数据库 = 环境类.属性获取_当前工作空间()
        if 基本信息.项目信息.JX_规划范围线要素名称 in 数据库类.属性获取_要素名称列表(当前数据库):
            要素类.拓扑检查范围(输入要素路径, 基本信息.项目信息.JX_规划范围线要素名称)
        else:
            from bxarcpy.环境包 import 输入输出类

            输入输出类.输出消息(f"当前工作空间中尚不存在范围要素：{基本信息.项目信息.JX_规划范围线要素名称}")
    要素投影后 = 要素类.要素创建_通过投影定义(输入要素路径)
    ret = 要素类.要素创建_通过复制并重命名重名要素(要素投影后, 输出要素路径)
    return ret


class 界面类:
    @staticmethod
    def 函数参数定义():
        from bxarcpy.参数包 import 参数类

        输入CAD数据集中的要素类 = 参数类.参数创建("输入CAD数据集中的要素类", "要素类", 参数必要性="必填")

        是否拓扑检查 = 参数类.参数创建("是否拓扑检查", "布尔值", 默认值=False)

        是否范围检查 = 参数类.参数创建("是否范围检查", "布尔值", 默认值=False)

        是否转曲 = 参数类.参数创建("是否转曲", "布尔值", 默认值=False)

        输出要素名称 = 参数类.参数创建("输出要素名称", "要素类", 参数类型="输出参数", 默认值="YD_CAD色块")

        return [输入CAD数据集中的要素类, 是否拓扑检查, 是否范围检查, 是否转曲, 输出要素名称]

    @staticmethod
    def 函数运行(参数列表, 消息):
        from bxarcpy.参数包 import 参数类

        参数字典 = 参数类.参数列表转换_到字典_参数对象转换为值(参数列表)
        导入从CAD(
            输入CAD数据集中的要素类路径=参数字典["输入CAD数据集中的要素类"],
            是否拓扑检查=参数字典["是否拓扑检查"],
            是否范围检查=参数字典["是否范围检查"],
            是否转曲=参数字典["是否转曲"],
            输出要素路径=参数字典["输出要素名称"],
        )
        return None


if __name__ == "__main__":
    from bxpy.日志包 import 日志生成器

    日志生成器.开启()
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        # Polyline Polygon
        # 导入从CAD(输入CAD数据集中的要素类路径=r"AA_test", 是否拓扑检查=True, 是否范围检查=False, 是否转曲=True, 输出要素路径=r"AA_村庄界线")
        导入从CAD(输入CAD数据集中的要素类路径=r"C:\Users\beixiao\Desktop\01.dwg\控规地块", 是否拓扑检查=True, 是否范围检查=False, 是否转曲=True, 输出要素路径=r"AA_现状用地拓扑检查")
        # 导入从CAD(输入CAD数据集中的要素类路径=r"C:\Users\beixiao\Desktop\01.dwg\道路中心线", 是否拓扑检查=True, 是否范围检查=False, 是否转曲=True, 输出要素路径=r"CZ_CAD导入_道路中心线")
        # 导入从CAD(输入CAD数据集中的要素类路径=r"C:\Users\beixiao\Desktop\02.dwg\Point", 是否拓扑检查=True, 是否范围检查=True, 是否转曲=True, 输出要素路径=r"AA_地块指标1")
