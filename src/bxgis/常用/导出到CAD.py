import bxarcpy
from bxpy import 日志
from typing import Union, Literal


def 导出到CAD(输入要素名称="DIST_用地规划图", 范围要素名称: Union[str, None] = "JX_规划范围线", 需融合地类编号列表=None, 切分阈值=None, 是否去孔=True, 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg"):
    # {"折点数量": 10, "孔洞数量": 2, "面积": 1000, "地类编号列表": ["1207"]}
    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    # 日志.输出控制台(输入要素)
    # 输入要素.字段删除(保留字段名称列表=["地类编号"])

    if 范围要素名称:
        裁剪后要素 = 输入要素.要素创建_通过裁剪(范围要素名称)
        日志.输出调试(f"裁剪要素成功")
    else:
        裁剪后要素 = 输入要素

    if 需融合地类编号列表:
        for x in 需融合地类编号列表:
            SQL语句 = f"地类编号 = '{x}'"
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
            for x in 游标:
                图形: "bxarcpy.游标类.形状类" = x["_形状"]
                # print(行.数据_列表格式[0])
                # print(type(行.数据_列表格式[0]))
                if 图形.孔洞数量 >= 切分阈值["孔洞数量"] and 图形.折点数量 >= 切分阈值["折点数量"] and 图形.面积 >= 切分阈值["面积"] and x["地类编号"] in 切分阈值["地类编号列表"]:
                    x["是否切分"] = "1"
                    游标.行更新(x)
                    日志.输出信息(f"ID：{str(x['_ID'])}，孔洞数量：{str(图形.孔洞数量)}, 折点数量：{str(图形.折点数量)}，面积：{str(图形.面积)}，地类：{x['地类编号']}")
        选择集 = 融合后要素.选择集创建_通过属性(SQL语句=f"是否切分 = '1'")
        切分后要素 = 选择集.要素创建_通过切分()
        切分后要素 = 融合后要素.要素创建_通过更新(更新要素名称=切分后要素.名称)
    else:
        切分后要素 = 融合后要素

    if 是否去孔:
        import sys

        sys.path.append(r"C:\Users\beixiao\Project\bxgeo")
        sys.path.append(r"C:\Users\beixiao\Project\bxgeo\.venv\Lib\site-packages")
        import bxgeo

        DIST_用地规划图线 = bxarcpy.要素类.要素创建_通过名称("DIST_用地规划图线", "线", 切分后要素.名称)
        线要素字段名称列表 = DIST_用地规划图线.字段名称列表获取()
        线要素字段名称列表.remove("OBJECTID")
        线要素字段名称列表.remove("Shape")
        线要素字段名称列表.remove("Shape_Length")
        线要素字段名称列表.remove("Shape_Area")
        with bxarcpy.游标类.游标创建_通过名称("插入", DIST_用地规划图线.名称, [*线要素字段名称列表, "_形状"]) as 游标_线:
            with bxarcpy.游标类.游标创建_通过名称("查询", 切分后要素.名称, [*线要素字段名称列表, "_形状"]) as 游标_面:
                for x in 游标_面:
                    partList = []
                    for part in x["_形状"].点表:
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

                    a = bxgeo.环.环创建_通过点表(扁平List[0])
                    if len(扁平List) > 1:
                        for shape in 扁平List[1:]:
                            b = bxgeo.环.环创建_通过点表(shape)
                            a = bxgeo.环.多部件连接(a, b)  # type: ignore
                    点表 = bxgeo.线.坐标获取(a)  # type: ignore

                    array = bxarcpy.数组.数组创建()._内嵌对象
                    part_array = bxarcpy.数组.数组创建()._内嵌对象
                    for pt in 点表:
                        点 = bxarcpy.点.点创建(*pt)._内嵌对象
                        bxarcpy.数组.项插入(part_array, 点)  # type: ignore
                    bxarcpy.数组.项插入(array, part_array)  # type: ignore
                    polyline = bxarcpy.线.线创建(array)._内嵌对象
                    x["_形状"] = bxarcpy.游标类.形状类(polyline)

                    游标_线.行插入(x)
        去孔后要素 = DIST_用地规划图线
    else:
        去孔后要素 = 切分后要素

    去孔后要素.字段添加("Layer").字段计算("Layer", "\"YDGIS-\" + !地类编号!.replace('/','／')")
    去孔后要素.字段添加("地块性质").字段计算("地块性质", "!地类编号!.replace('／','/')")
    去孔后要素.字段添加("实体类型").字段计算("实体类型", '"控规地块"')
    去孔后要素.字段删除(["ORIG_FID", "地类编号", "是否切分"])
    # 去孔后要素.要素创建_通过复制并重命名重名要素("DIST_用地规划图2")

    去孔后要素.导出到CAD(输出CAD路径)


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        导出到CAD("DIST_用地规划图", 范围要素名称="JX_规划范围线", 需融合地类编号列表=None, 切分阈值=None, 是否去孔=True, 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg")
