# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-09-24 17:43:33
"""
import bxarcpy
from bxpy import 日志

# from sys import argv


def main(
    工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb",
    CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"],
    输入图层名称="控规地块",
    输出要素名称=r"YD_CAD色块",
    是否拓扑检查=False,
):
    with bxarcpy.类.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        bxarcpy.类.配置.是否覆盖输出要素 = True
        if 输入图层名称 in ["点", "线", "面"]:
            输入图层名称 = bxarcpy.类._要素类型映射[输入图层名称]
        # arcpy.env.overwriteOutput = False
        输出要素集 = bxarcpy.类.要素数据集类.导入从CAD(CAD路径列表, r"AA_CAD导入GEO1")
        # 输出要素集 = bxarcpy.转换.CAD导入到GEO(CAD路径列表=CAD路径列表, 输出数据库=工作空间, 输出要素集名称=r"AA_CAD导入GEO1")
        日志.输出调试("输出的要素集是：" + 输出要素集.名称 + rf"\{输入图层名称}")

        输入要素 = bxarcpy.类.要素类.要素读取_通过名称(输出要素集.名称 + rf"\{输入图层名称}")

        复制后要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        输出要素集.要素数据集删除()
        # bxarcpy.数据管理.要素删除(输入要素列表=[输出要素集])
        复制后要素 = 复制后要素.要素几何修复()
        # Process: 修复几何 (修复几何) (management)
        if 输入图层名称 == "控规地块":
            复制后要素 = 复制后要素.字段添加("地类编号").字段计算("地类编号", "!Layer!.split(\"#\")[0].split(\"-\")[1].replace('／','/')")

        复制后要素.字段删除(["Entity", "Handle", "Layer", "Color", "Linetype", "Elevation", "LineWt", "RefName", "LyrColor", "LyrLnType", "LyrLineWt", "Angle", "LyrFrzn", "LyrLock", "LyrOn", "LyrVPFrzn", "LyrHandle", "EntColor", "BlkColor", "EntLinetype", "BlkLinetype", "Thickness", "EntLineWt", "BlkLineWt", "LTScale", "ExtX", "ExtY", "ExtZ", "DocName", "DocPath", "DocType", "DocVer", "DocUpdate", "DocId"])

        if 是否拓扑检查:
            复制后要素.拓扑创建()


if __name__ == "__main__":
    # Global Environment settings
    # main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"], 输入图层名称="控规地块", 输出要素名称=r"YD_CAD色块", 是否拓扑检查=True)
    # main(工作空间=r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\01.dwg"], 输入图层名称="控规地块", 输出要素=r"YD_CAD色块", 是否拓扑检查=True)
    # main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\002.dwg"], 输入图层名称="面", 输出要素名称=r"JX_工业片区范围线", 是否拓扑检查=True)
    日志.开启()
    # main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\002.dwg"], 输入图层名称="道路中心线", 输出要素名称=r"DL_道路中线", 是否拓扑检查=True)
    main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\002.dwg"], 输入图层名称="河道中线", 输出要素名称=r"DL_河道中线", 是否拓扑检查=True)
    # main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", CAD路径列表=[r"C:\Users\beixiao\Desktop\新111块.dwg"], 输入图层名称="面", 输出要素名称=r"KZX_村庄建设边界", 是否拓扑检查=True)
