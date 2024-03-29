import bxarcpy
from bxpy import 日志
from typing import Union, Literal


def 导出到CAD(输入要素名称="DIST_用地规划图", 规划范围线要素名称: Union[str, None] = "JX_规划范围线", 需融合地类编号列表=None, 切分阈值=None, 是否去孔=True, CAD中图层采用的字段的名称=None, 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg"):
    # {"折点数量": 10, "孔洞数量": 2, "面积": 1000, "地类编号列表": ["1207"]}
    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    # 日志.输出控制台(输入要素)
    # 输入要素.字段删除(保留字段名称列表=["地类编号"])

    if 规划范围线要素名称:
        裁剪后要素 = 输入要素.要素创建_通过裁剪(规划范围线要素名称)
        日志.输出调试(f"裁剪要素成功")
    else:
        裁剪后要素 = 输入要素

    if 需融合地类编号列表:
        for 面x in 需融合地类编号列表:
            SQL语句 = f"地类编号 = '{面x}'"
            日志.输出调试(f"SQL语句是：{SQL语句}")
            选择集 = 裁剪后要素.选择集创建_通过属性(SQL语句=SQL语句)
            融合后要素 = 选择集.要素创建_通过融合(融合字段列表=["地类编号"])
            裁剪后要素 = 裁剪后要素.要素创建_通过更新(融合后要素.名称)
        融合后要素 = 裁剪后要素
    else:
        融合后要素 = 裁剪后要素

    融合后要素 = 融合后要素.要素创建_通过多部件至单部件()

    if 切分阈值:
        # {"折点数量": 1500, "孔洞数量": 3, "面积": 1500000, '地类编号列表': ['1207']}
        融合后要素.字段添加("是否切分")
        with bxarcpy.游标类.游标创建_通过名称("更新", 融合后要素.名称, ["_形状", "是否切分", "_ID", "地类编号"]) as 游标:
            for 面x in 游标:
                图形 = 面x["_形状"]
                # print(行.数据_列表格式[0])
                # print(type(行.数据_列表格式[0]))
                if bxarcpy.几何对象类.孔洞数量获取(图形) >= 切分阈值["孔洞数量"] and bxarcpy.几何对象类.折点数量获取(图形) >= 切分阈值["折点数量"] and bxarcpy.几何对象类.面积获取(图形) >= 切分阈值["面积"] and 面x["地类编号"] in 切分阈值["地类编号列表"]:
                    面x["是否切分"] = "1"
                    游标.行更新(面x)
                    日志.输出信息(f"ID：{str(面x['_ID'])}，孔洞数量：{str(bxarcpy.几何对象类.孔洞数量获取(图形))}, 折点数量：{str(bxarcpy.几何对象类.折点数量获取(图形))}，面积：{str(bxarcpy.几何对象类.面积获取(图形))}，地类：{面x['地类编号']}")
        选择集 = 融合后要素.选择集创建_通过属性(SQL语句=f"是否切分 = '1'")
        切分后要素 = 选择集.要素创建_通过切分()
        切分后要素 = 融合后要素.要素创建_通过更新(更新要素名称=切分后要素.名称)
    else:
        切分后要素 = 融合后要素

    if 是否去孔:
        import bxgeo

        DIST_用地规划图线 = bxarcpy.要素类.要素创建_通过名称("DIST_用地规划图线", "线", 切分后要素.名称)
        线要素字段名称列表 = DIST_用地规划图线.字段名称列表获取(含系统字段=False)
        # 线要素字段名称列表.remove("OBJECTID")
        # 线要素字段名称列表.remove("Shape")
        # 线要素字段名称列表.remove("Shape_Length")
        # 线要素字段名称列表.remove("Shape_Area")
        with bxarcpy.游标类.游标创建_通过名称("插入", DIST_用地规划图线.名称, [*线要素字段名称列表, "_形状"]) as 游标_线:
            with bxarcpy.游标类.游标创建_通过名称("查询", 切分后要素.名称, [*线要素字段名称列表, "_形状"]) as 游标_面:
                import bxpy

                for 面x in bxpy.进度条(游标_面, 总进度=切分后要素.几何数量):
                    partList = []
                    for part in bxarcpy.几何对象类.点表获取(面x["_形状"]):
                        ptList = []
                        shapeList = []
                        for pt in part:
                            if pt is not None:
                                ptList.append((bxarcpy.点.X坐标获取(pt), bxarcpy.点.Y坐标获取(pt)))
                            else:
                                shapeList.append(ptList)
                                ptList = []
                        shapeList.append(ptList)
                        partList.append(shapeList)

                    扁平List = []
                    for part in partList:
                        扁平List.extend(part)

                    a = bxgeo.环.环创建_通过点表(扁平List[0])._内嵌对象
                    if len(扁平List) > 1:
                        for shape in 扁平List[1:]:
                            b = bxgeo.环.环创建_通过点表(shape)._内嵌对象
                            a = bxgeo.环.多部件连接(a, b)._内嵌对象  # type: ignore
                    点表 = bxgeo.线.坐标获取(a)  # type: ignore
                    # import bxpy

                    # bxpy.日志.输出控制台(点表)
                    array = bxarcpy.数组.数组创建()._内嵌对象
                    part_array = bxarcpy.数组.数组创建()._内嵌对象
                    for pt in 点表:
                        点 = bxarcpy.点.点创建(*pt)._内嵌对象
                        bxarcpy.数组.项插入(part_array, 点)  # type: ignore
                    bxarcpy.数组.项插入(array, part_array)  # type: ignore
                    面x["_形状"] = bxarcpy.线.线创建(array)._内嵌对象
                    游标_线.行插入(面x)
        去孔后要素 = DIST_用地规划图线
    else:
        去孔后要素 = 切分后要素
    if CAD中图层采用的字段的名称:
        去孔后要素.字段添加("Layer").字段计算("Layer", f"'YDGIS-' + !{CAD中图层采用的字段的名称}!.replace('/','／')")
        去孔后要素.字段添加("地块性质").字段计算("地块性质", f"!{CAD中图层采用的字段的名称}!.replace('／','/')")
        去孔后要素.字段添加("实体类型").字段计算("实体类型", '"控规地块"')
        去孔后要素.字段删除(["ORIG_FID", CAD中图层采用的字段的名称, "是否切分"])
    # 去孔后要素.要素创建_通过复制并重命名重名要素("DIST_用地规划图2")
    # with bxarcpy.游标类.游标创建_通过名称("查询", 去孔后要素.名称, ["_形状"]) as 游标:
    #     for x in 游标:
    #         日志.输出控制台(f"{bxarcpy.几何对象类.折点数量获取(x['_形状'])}")
    # 去孔后要素.要素创建_通过复制并重命名重名要素("AA_123")
    去孔后要素.导出到CAD(输出CAD路径)


if __name__ == "__main__":
    import bxarcpy

    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        导出到CAD(输入要素名称="XG_GHDK", 规划范围线要素名称=None, 需融合地类编号列表=None, 切分阈值=None, 是否去孔=True, CAD中图层采用的字段的名称="dldm", 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg")
