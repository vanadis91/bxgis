# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-09-25 16:31:40
"""
import bxarcpy


def main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 村庄建设边界要素名称="KZX_村庄建设边界", 单元名称="临江单元", 批复时间="", 批复文号="", 单元编号="QT12"):
    with bxarcpy.类.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        bxarcpy.类.配置.是否覆盖输出要素 = True

        村庄建设边界要素 = bxarcpy.要素类.要素读取_通过名称(村庄建设边界要素名称)
        村庄建设边界要素 = 村庄建设边界要素.要素创建_通过复制()

        融合后要素 = 村庄建设边界要素.要素创建_通过融合(None).要素创建_通过多部件至单部件().要素几何修复()
        融合后要素.字段添加("建设边界编号")
        需操作的字段名称列表 = ["建设边界编号"]
        编号 = 1
        with bxarcpy.游标类.游标创建_通过名称("更新", 融合后要素.名称, 需操作的字段名称列表) as 游标:
            for x in 游标:
                x["建设边界编号"] = 单元编号 + "-" + "JSBJ" + str(编号).zfill(2)
                编号 += 1
                游标.行更新(x)
        融合后要素.字段删除(["ORIG_FID", "ORIG_FID_1"])

        村庄建设边界要素 = 融合后要素.要素创建_通过复制并重命名重名要素("XG_JSBJ")
        村庄建设边界要素.字段添加("DYMC", "字符串", 50, "规划编制单元名称").字段计算("DYMC", f"'{单元名称}'")
        村庄建设边界要素.字段添加("PFSJ", "日期", None, "批复时间").字段计算("PFSJ", f"'{批复时间}'")
        村庄建设边界要素.字段添加("PFWH", "字符串", 50, "批复文号").字段计算("PFWH", f"'{批复文号}'")
        村庄建设边界要素.字段添加("JSBM", "字符串", 20, "建设边界编码").字段计算("JSBM", "!建设边界编号!")
        村庄建设边界要素.字段添加("JSMJ", "双精度", 50, "建设边界面积").字段计算("JSMJ", "round(!Shape_Area!/10000, 2)")

        村庄建设边界要素.字段添加("GKYQ", "字符串", 255, "管控要求")
        需操作的字段名称列表 = ["GKYQ"]
        with bxarcpy.游标类.游标创建_通过名称("更新", 村庄建设边界要素.名称, 需操作的字段名称列表) as 游标:
            for x in 游标:
                x["GKYQ"] = "按照“避让底线、引导集聚、单元统筹、预留弹性、界限清晰”的原则进行控制，综合考虑村庄分级分类与建设用地指标安排，引导乡村空间适度集聚"
                游标.行更新(x)

        村庄建设边界要素.字段添加("BZ", "字符串", 255, "备注")

        村庄建设边界要素.字段删除(["建设边界编号"])


if __name__ == "__main__":
    main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 村庄建设边界要素名称="KZX_村庄建设边界", 单元名称="临江单元", 批复时间="", 批复文号="", 单元编号="QT12")
