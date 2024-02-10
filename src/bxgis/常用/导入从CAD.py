import bxarcpy
from bxpy import 日志


def 导入从CAD(输入CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"], 输入CAD图层名称="控规地块", 是否拓扑检查=False, 是否范围检查=True, 是否转曲=True, 输出要素名称=r"YD_CAD色块"):
    if 输入CAD图层名称 in ["点", "线", "面"]:
        输入CAD图层名称 = bxarcpy.常量._要素类型映射[输入CAD图层名称]

    日志.输出调试(f"当前工作空间{bxarcpy.配置.当前工作空间}")
    输出要素集 = bxarcpy.要素数据集类.导入从CAD(输入CAD路径列表, r"AA_CAD导入GEO1")
    日志.输出调试("输出的要素集是：" + 输出要素集.名称 + rf"\{输入CAD图层名称}")

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输出要素集.名称 + rf"\{输入CAD图层名称}")

    复制后要素 = 输入要素.要素创建_通过复制().要素几何修复()
    输出要素集.要素数据集删除()

    if 是否转曲:
        复制后要素 = 复制后要素.要素创建_通过增密()

    if 输入CAD图层名称 == "控规地块":
        复制后要素 = 复制后要素.字段添加("地类编号").字段计算("地类编号", "!Layer!.split(\"#\")[0].split(\"-\")[1].replace('／','/')")

    复制后要素.字段删除(["Entity", "Handle", "Layer", "Color", "Linetype", "Elevation", "LineWt", "RefName", "LyrColor", "LyrLnType", "LyrLineWt", "Angle", "LyrFrzn", "LyrLock", "LyrOn", "LyrVPFrzn", "LyrHandle", "EntColor", "BlkColor", "EntLinetype", "BlkLinetype", "Thickness", "EntLineWt", "BlkLineWt", "LTScale", "ExtX", "ExtY", "ExtZ", "DocName", "DocPath", "DocType", "DocVer", "DocUpdate", "DocId"])

    if 是否拓扑检查:
        复制后要素.拓扑检查重叠()

    if 是否范围检查:
        复制后要素.拓扑检查范围("JX_规划范围线")

    复制后要素 = 复制后要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 复制后要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        导入从CAD(输入CAD路径列表=[r"C:\Users\beixiao\Desktop\001.dwg"], 输入CAD图层名称="控规地块", 输出要素名称=r"YD_CAD色块", 是否拓扑检查=True, 是否范围检查=True, 是否转曲=True)
