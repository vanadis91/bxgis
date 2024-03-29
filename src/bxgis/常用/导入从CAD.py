import bxarcpy
from bxpy import 日志
from bxgis import 配置


def 导入从CAD(输入CAD数据集中的要素类=r"C:\Users\beixiao\Desktop\01.dwg\控规地块", 是否拓扑检查=False, 是否范围检查=True, 是否转曲=True, 输出要素名称=r"YD_CAD色块"):
    # if 输入CAD图层名称 in ["点", "线", "面"]:
    #     输入CAD图层名称 = bxarcpy.常量._要素类型映射[输入CAD图层名称]

    # 日志.输出调试(f"当前工作空间{bxarcpy.配置.当前工作空间}")
    # 输出要素集 = bxarcpy.要素数据集类.导入从CAD(输入CAD路径列表, r"AA_CAD导入GEO1")
    # 日志.输出调试("输出的要素集是：" + 输出要素集.名称 + rf"\{输入CAD图层名称}")

    # 输入要素 = bxarcpy.要素类.要素读取_通过名称(输出要素集.名称 + rf"\{输入CAD图层名称}")

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入CAD数据集中的要素类).要素创建_通过复制().要素几何修复()

    # 输出要素集.要素数据集删除()

    if 是否转曲:
        输入要素 = 输入要素.要素创建_通过增密()

    if 输入要素.名称_无路径 == "控规地块":
        输入要素 = 输入要素.字段添加(字段名称=配置.地块要素字段映射.地类编号字段名称).字段计算(配置.地块要素字段映射.地类编号字段名称, "!Layer!.split('#')[0].split('-')[1].replace('／','/')")

    输入要素.字段删除(["Entity", "Handle", "Layer", "Color", "Linetype", "Elevation", "LineWt", "RefName", "LyrColor", "LyrLnType", "LyrLineWt", "Angle", "LyrFrzn", "LyrLock", "LyrOn", "LyrVPFrzn", "LyrHandle", "EntColor", "BlkColor", "EntLinetype", "BlkLinetype", "Thickness", "EntLineWt", "BlkLineWt", "LTScale", "ExtX", "ExtY", "ExtZ", "DocName", "DocPath", "DocType", "DocVer", "DocUpdate", "DocId"])

    if 是否拓扑检查:
        输入要素.拓扑检查重叠()

    if 是否范围检查:
        from bxarcpy import 数据库类
        from bxarcpy import 配置 as arcpy配置

        当前数据库 = 数据库类.数据库读取_通过路径(arcpy配置.当前工作空间)
        if 配置.项目信息.JX_规划范围线要素名称 in 当前数据库.要素名称列表获取():
            输入要素.拓扑检查范围(配置.项目信息.JX_规划范围线要素名称)
        else:
            from bxarcpy import 环境

            环境.输出消息(f"当前工作空间中尚不存在范围要素：{配置.项目信息.JX_规划范围线要素名称}")

    输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        导入从CAD(输入CAD数据集中的要素类=r"C:\Users\beixiao\Desktop\01.dwg\控规地块", 是否拓扑检查=True, 是否范围检查=True, 是否转曲=True, 输出要素名称=r"YD_CAD色块")
