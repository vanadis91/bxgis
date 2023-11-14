# -*- coding: utf-8 -*-
import bxarcpy
from bxpy import 日志
import arcpy


def main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 图层名称="DIST_用地规划图"):  # 表达_设置符号系统
    with bxarcpy.环境.环境管理器(工作空间=工作空间, 临时工作空间=工作空间):
        # To allow overwriting outputs change overwriteOutput option to True.
        bxarcpy.配置.是否覆盖输出要素 = True
        # Process: 将图层符号系统与样式匹配 (将图层符号系统与样式匹配) (management)
        文档 = bxarcpy.文档类.文档读取_通过名称("Current")
        # 文档 = bxarcpy.文档类.文档读取_通过名称(文档路径=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.aprx")
        地图 = 文档.地图列表读取("*")[0]
        bxarcpy.环境.输出消息(f"选取到的地图是：{地图}")
        # 日志.输出调试(地图)
        图层名称1 = 图层名称.split("\\")[-1]
        图层 = 地图.图层列表读取(图层名称1)[0]
        bxarcpy.环境.输出消息(f"选取到的图层是：{图层}")
        # 日志.输出调试(图层)
        # 图层对象 = 图层.getDefinition("V3")
        # symLvl2 = 图层对象.renderer.symbol.symbol.symbolLayers[1]
        # symLvl2.color.values = [140, 70, 20, 20]
        # 图层.setDefinition(图层对象)

        # 样式1 = r"C:\Users\beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.lyrx"
        # 样式图层 = arcpy.mp.LayerFile(样式1).listLayers()[0]
        # 样式图层的符号 = 样式图层.listLayers()[0].symbology
        # 图层.symbology = 样式图层的符号

        # 样式2 = r"C:\Users\common\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.lyr"
        # 图层.符号系统设置_通过lyr图层文件(图层文件路径=样式2, 映射关系=[["VALUE_FIELD", "", "JQYDDM"]])

        # 图层 = bxarcpy.图层类(名称=图层名称)
        样式文件 = r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx"
        # 图层._内嵌对象.symbology.applySymbologyFromStyle(样式文件)
        # 图层.符号系统设置_通过stylx样式文件(样式文件路径=r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx", 映射关系="$feature.地类编号")
        # arcpy.management.MatchLayerSymbologyToAStyle(in_layer=r"DIST_输出\DIST_用地规划图", match_values="地类编号", in_style=样式文件)
        # arcpy.management.MatchLayerSymbologyToAStyle(in_layer=r"DIST_输出\DIST_用地规划图", match_values="$feature.地类编号", in_style=样式文件)
        # arcpy.management.MatchLayerSymbologyToAStyle(in_layer=r"DIST_用地规划图", match_values="地类编号", in_style=样式文件)
        # arcpy.management.MatchLayerSymbologyToAStyle(in_layer=r"DIST_用地规划图", match_values="$feature.地类编号", in_style=样式文件)
        # arcpy.management.MatchLayerSymbologyToAStyle(in_layer=图层._内嵌对象, match_values="$feature.地类编号", in_style=样式文件)
        # arcpy.management.MatchLayerSymbologyToAStyle(in_layer=图层._内嵌对象, match_values="地类编号", in_style=样式文件)
        # 文档.文档另存为(r"C:\Users\beixiao\Desktop\003.aprx")
        # 文档._内嵌对象.refresh()
        # arcpy.management.MatchLayerSymbologyToAStyle(r"DIST_输出\DIST_用地规划图", "地类编号", r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx")

        # 样式文件路径 = r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx"
        # 图层._内嵌对象.updateConnectionProperties(None, None, 样式文件路径)
        # 图层.符号系统.符号系统设置_通过stylx样式文件(样式文件路径)


if __name__ == "__main__":
    工作空间 = bxarcpy.环境.输入参数获取_以字符串形式(0, r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb")
    图层名称 = bxarcpy.环境.输入参数获取_以字符串形式(1, r"DIST_用地规划图", False)
    arcpy.management.MatchLayerSymbologyToAStyle(r"DIST_用地规划图", "地类编号", r"C:\Users\Beixiao\AppConfig\ArcGIS\010.符号系统\符号系统_省国空地类_根据编号.stylx")

    # 日志.开启()
    # main(工作空间=工作空间, 图层名称=图层名称)
