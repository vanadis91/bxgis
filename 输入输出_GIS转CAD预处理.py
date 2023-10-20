# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-09-18 17:28:35
"""
from sys import argv
import bxpy
import bxarcpy

# cd C:\Program Files (x86)\ArcGIS\Pro\bin\Python\Scripts


def main(工作空间="C:\\Users\\common\\project\\J江东区临江控规\\临江控规_数据库.gdb", 输入要素名称="AA_规划道路", 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg", 裁剪范围要素名称=None, 需融合地类编号列表=None, 切分阈值=None):
    with bxarcpy.类.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        # 输入输出_GIS转CAD预处理_PY3
        # To allow overwriting outputs change overwriteOutput option to True.
        bxarcpy.类.配置.是否覆盖输出要素 = True
        # arcpy.env.overwriteOutput = False

        # Process: 导出为 CAD (要素转 CAD) (conversion)
        # test111_dwg = "C:\\Users\\beixiao\\Desktop\\test111.dwg"
        # arcpy.conversion.ExportCAD(in_features=[], Output_Type="DWG_R2010", Output_File=test111_dwg,
        #                            Ignore_FileNames="Ignore_Filenames_in_Tables", Append_To_Existing="Overwrite_Existing_Files", Seed_File="")

        # Process: 复制要素 (2) (复制要素) (management)
        输入要素 = bxarcpy.类.要素类.要素读取_通过名称(输入要素名称)
        # 输出要素 = bxarcpy.数据管理.要素复制(输入要素=输入路径)
        输入要素 = 输入要素.要素创建_通过复制()

        # 删除字段 = ["dkbmgk", "地块性", "单元名", "TBYBH", "FID_DLTB", "GKXZ", "Layer", "CZCSXM", "三调地类名称", "三调地类编号", "ORIG_FID", "a", "镇街名称", "名称", "FID_4去除", "Shape_Leng", "三调稳", "二调永", "三调恢", "三调耕", "二调耕", "街道", "村名称", "组名", "序号", "FID_规划范围线_2303070850", "FWDGDHRLY", "SFWYYJJBNT", "WDGD", "BZ", "ZRSYX", "SJMC", "SJBH", "BHJSSJ", "BHKSSJ", "JZDZ", "LXDH", "ZRRMC", "ZRRZJHM", "ZZRR", "ZMC", "CFZR", "SJNF", "FRDBS", "ZLFLDM", "GDDJ", "GDDB", "ZZSXMC", "ZZSXDM", "TBXHMC", "TBXHDM", "GGBZL", "GDPDJB", "GDLX", "YJJBNTMJ", "KCMJ", "KCXS", "KCDLBM", "YJJBNTTBMJ", "ZLDWMC", "ZLDWDM", "QSDWMC", "QSDWDM", "QSXZ", "DLMC", "DLBM", "TBBH", "YJJBNTTBBH", "XZQMC", "XZQDM", "YSDM", "BSM", "FID_YJJBNTBHTB", "mj", "RefName", "LineWt", "Elevation", "Linetype", "Color", "Entity", "地块性质", "实体类型", "基数转换关系", "用途管制分区", "综合耕地N", "面积", "处理方向", "综合净面积", "基期代码", "基期名称", "基期CZCSXM", "基期类型", "基期大类", "基期城乡统计", "基期KCXS"]
        # Process: 删除字段 (2) (删除字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段删除(输入要素=输出要素, 删除字段列表=删除字段)
        输入要素.字段删除(保留字段名称列表=["地类编号"])

        # Process: 添加字段 (添加字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="Layer", 字段类型="字符串", 字段长度=100)

        # # Process: 计算字段 (计算字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="Layer", 表达式="\"YDGIS-\" + !地类编号!.replace('/','／')", 字段类型="字符串")
        # Process: 添加字段 (2) (添加字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="地块性质", 字段类型="字符串", 字段长度=100)

        # Process: 计算字段 (2) (计算字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="地块性质", 表达式="!地类编号!.replace('／','/')", 字段类型="字符串")

        # Process: 添加字段 (3) (添加字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="实体类型", 字段类型="字符串", 字段长度=100)

        # Process: 计算字段 (3) (计算字段) (management)
        # 输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="实体类型", 表达式='"控规地块"', 字段类型="字符串")

        # Process: 裁剪 (裁剪) (analysis)
        if 裁剪范围要素名称:
            裁剪后要素 = 输入要素.要素创建_通过裁剪(裁剪范围要素名称)
            bxpy.调试.输出调试(f"裁剪要素成功")
        else:
            裁剪后要素 = 输入要素
        # 输出要素 = bxarcpy.分析.裁剪(输入要素=输出要素, 裁剪要素=裁剪范围)
        if 需融合地类编号列表:
            for x in 需融合地类编号列表:
                SQL语句 = f"地类编号 = '{x}'"
                bxpy.调试.输出调试(f"SQL语句是：{SQL语句}")
                选择集 = 裁剪后要素.选择集创建_通过属性(SQL语句=SQL语句)
                融合后要素 = 选择集.要素创建_通过融合(融合字段列表=["地类编号"])
                裁剪后要素 = 裁剪后要素.要素创建_通过更新并合并字段(融合后要素.名称)
            融合后要素 = 裁剪后要素
        else:
            融合后要素 = 裁剪后要素
        # Process: 多部件至单部件 (多部件至单部件) (management)
        # 输出要素 = bxarcpy.数据管理.要素多部件至单部件(输入要素=输出要素)
        融合后要素.字段添加("是否切分")
        if 切分阈值:
            # {"折点数量": 1500, "孔洞数量": 3, "面积": 1500000}
            with bxarcpy.类.游标类_用于更新(融合后要素.名称, ["_形状", "是否切分"]) as 游标:
                for 行 in 游标:
                    图形: "bxarcpy.类.游标类_用于更新.形状" = 行.数据_列表格式[0]
                    # print(行.数据_列表格式[0])
                    # print(type(行.数据_列表格式[0]))
                    if 图形.孔洞数量 > 切分阈值["孔洞数量"] and 图形.折点数量 > 切分阈值["折点数量"] and 图形.面积 > 切分阈值["面积"]:
                        行.数据_列表格式[1] = "1"
                        行.行更新_列表格式()
                        bxpy.调试.输出调试(f"孔洞数量：{str(图形.孔洞数量)}, 折点数量：{str(图形.折点数量)}，面积：{str(图形.面积)}")
        选择集 = 融合后要素.选择集创建_通过属性(SQL语句=f"是否切分 = '1'")
        切分后要素 = 选择集.要素创建_通过切分()
        更新后要素 = 融合后要素.要素创建_通过更新并合并字段(更新要素名称=切分后要素.名称)

        转单部件后要素 = 更新后要素.要素创建_通过多部件至单部件()
        # Process: 修复几何 (修复几何) (management)
        # 输出要素 = bxarcpy.数据管理.要素几何修复(输入要素=输出要素)
        转单部件后要素.要素几何修复()

        # 输出要素 = bxarcpy.数据管理.字段删除(输入要素=输出要素, 删除字段列表=["ORIG_FID", "地类编号"])
        转单部件后要素.字段添加("Layer").字段计算("Layer", "\"YDGIS-\" + !地类编号!.replace('/','／')")
        转单部件后要素.字段添加("地块性质").字段计算("地块性质", "!地类编号!.replace('／','/')")
        转单部件后要素.字段添加("实体类型").字段计算("实体类型", '"控规地块"')
        转单部件后要素.字段删除(["ORIG_FID", "地类编号", "是否切分"])

        # Process: 复制要素 (复制要素) (management)
        # print("输入要素是：" + 输出要素)
        # print("输出要素是：" + 工作空间 + 输出路径)
        转单部件后要素.导出到CAD(输出CAD路径)
        转单部件后要素.要素创建_通过复制并重命名重名要素("AA_导出到CAD前预处理")
        # 输出要素 = bxarcpy.数据管理.要素复制(输入要素=输出要素, 输出要素=工作空间 + 输出路径)
        # bxarcpy.转换.GEO导出到CAD(输入要素列表=[输出要素], 输出路径=输出CAD路径)


if __name__ == "__main__":
    import bxpy

    bxpy.调试.开启()
    # Global Environment settings
    # main(*argv[1:])
    # main(
    #     工作空间="C:\\Users\\common\\project\\J江东区临江控规\\临江控规_数据库.gdb",
    #     输入路径="\\DIST_用地规划图1",
    #     裁剪范围="\\JX_规划范围线",
    #     输出路径="\\AA_导出到CAD前预处理6",
    #     输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg",
    # )
    main(
        工作空间=r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb",
        输入要素名称="DIST_用地现状图",
        输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg",
        裁剪范围要素名称="JX_规划范围线",
        需融合地类编号列表=["0703"],
        切分阈值={"折点数量": 1500, "孔洞数量": 3, "面积": 1500000},
    )
