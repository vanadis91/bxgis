# *-* coding:utf8 *-*
from bxpy.日志包 import 日志生成器
from bxpy.进度条包 import 进度条类
from bxpy.路径包 import 路径类
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.基本对象包 import 数组类
from bxarcpy.几何包 import 几何类
from bxarcpy.几何包 import 点类 as arc点类
from bxarcpy.几何包 import 线类 as arc线类
from bxarcpy.环境包 import 环境管理器类
from bxshapely.线包 import 环类, 线类
from bxgis.配置 import 基本信息
from typing import Union, Literal


def 导出到CAD(输入要素路径="DIST_用地规划图", 规划范围线要素名称: Union[str, None] = "JX_规划范围线", 需融合字段名称=None, 需融合字段中需融合的值的列表=None, 切分阈值=None, 是否去孔=True, CAD中图层采用的字段的名称='地类编号', 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg"):
    # {"折点数量": 10, "孔洞数量": 2, "面积": 1000, "地类编号列表": ["1207"]}
    输入要素路径_复制后 = 要素类.要素创建_通过复制(输入要素路径)
    日志生成器.输出控制台(f"几何数量：{要素类.属性获取_几何数量(输入要素路径_复制后)}")

    # 日志类.输出控制台(输入要素)
    # 输入要素.字段删除(保留字段名称列表=["地类编号"])

    if 规划范围线要素名称:
        裁剪后要素 = 要素类.要素创建_通过裁剪(输入要素路径_复制后, 规划范围线要素名称)
        日志生成器.输出调试(f"裁剪要素成功")
    else:
        裁剪后要素 = 输入要素路径_复制后
    日志生成器.输出控制台(f"几何数量：{要素类.属性获取_几何数量(裁剪后要素)}")

    if 需融合字段名称:
        if 需融合字段中需融合的值的列表:
            for 需融合字段中需融合的值x in 需融合字段中需融合的值的列表:
                SQL语句 = f"{需融合字段名称} = '{需融合字段中需融合的值x}'"
                日志生成器.输出调试(f"SQL语句是：{SQL语句}")
                选择集 = 要素类.选择集创建_通过属性(裁剪后要素, SQL语句=SQL语句)
                融合后要素 = 要素类.要素创建_通过融合(选择集, 融合字段列表=[需融合字段名称])
                裁剪后要素 = 要素类.要素创建_通过更新(裁剪后要素, 融合后要素)
            融合后要素 = 裁剪后要素
        else:
            融合后要素 = 裁剪后要素
    else:
        融合后要素 = 裁剪后要素
    日志生成器.输出控制台(f"几何数量：{要素类.属性获取_几何数量(融合后要素)}")

    融合后要素 = 要素类.要素创建_通过多部件至单部件(融合后要素)

    if 切分阈值:
        # {"折点数量": 1500, "孔洞数量": 3, "面积": 1500000, '地类编号列表': ['1207']}
        融合后要素操作字段列表 = ["_形状", "是否切分", "_ID", "地类编号"]
        要素类.字段添加(融合后要素, "是否切分")
        with 游标类.游标创建("更新", 融合后要素, 融合后要素操作字段列表) as 游标:
            for 需融合字段中需融合的值x in 游标类.属性获取_数据_字典形式(游标, 融合后要素操作字段列表):
                图形 = 需融合字段中需融合的值x["_形状"]
                # print(行.数据_列表格式[0])
                # print(type(行.数据_列表格式[0]))
                if 几何类.属性获取_孔洞数量(图形) >= 切分阈值["孔洞数量"] and 几何类.属性获取_折点数量(图形) >= 切分阈值["折点数量"] and 几何类.属性获取_面积(图形) >= 切分阈值["面积"] and 需融合字段中需融合的值x["地类编号"] in 切分阈值["地类编号列表"]:
                    需融合字段中需融合的值x["是否切分"] = "1"
                    游标.行更新(需融合字段中需融合的值x)
                    日志生成器.输出信息(f"ID：{str(需融合字段中需融合的值x['_ID'])}，孔洞数量：{str(几何类.属性获取_孔洞数量(图形))}, 折点数量：{str(几何类.属性获取_折点数量(图形))}，面积：{str(几何类.属性获取_面积(图形))}，地类：{需融合字段中需融合的值x['地类编号']}")

        选择集 = 要素类.选择集创建_通过属性(融合后要素, SQL语句=f"是否切分 = '1'")
        切分后要素 = 要素类.要素创建_通过切分(选择集)
        切分后要素 = 要素类.要素创建_通过更新(融合后要素, 更新要素路径=切分后要素)
    else:
        切分后要素 = 融合后要素
    日志生成器.输出控制台(f"几何数量：{要素类.属性获取_几何数量(切分后要素)}")
    if 是否去孔:
        DIST_用地规划图线 = 要素类.要素创建_通过名称("DIST_用地规划图线", "线", 切分后要素)
        线要素字段名称列表 = 要素类.字段名称列表获取(DIST_用地规划图线, 含系统字段=False)
        # 线要素字段名称列表.remove("OBJECTID")
        # 线要素字段名称列表.remove("Shape")
        # 线要素字段名称列表.remove("Shape_Length")
        # 线要素字段名称列表.remove("Shape_Area")
        操作字段名称列表 = [*线要素字段名称列表, "_形状"]
        with 游标类.游标创建("插入", DIST_用地规划图线, 操作字段名称列表) as 游标_线:
            with 游标类.游标创建("查询", 切分后要素, 操作字段名称列表) as 游标_面:
                for 需融合字段中需融合的值x in 进度条类.进度条创建(游标类.属性获取_数据_字典形式(游标_面, 操作字段名称列表), 总进度=要素类.属性获取_几何数量(切分后要素)):
                    partList = []
                    for part in 几何类.属性获取_折点列表(需融合字段中需融合的值x["_形状"]):
                        ptList = []
                        shapeList = []
                        for pt in part:
                            if pt is not None:
                                ptList.append((arc点类.属性获取_x坐标(pt), arc点类.属性获取_y坐标(pt)))
                            else:
                                shapeList.append(ptList)
                                ptList = []
                        shapeList.append(ptList)
                        partList.append(shapeList)

                    扁平List = []
                    for part in partList:
                        扁平List.extend(part)

                    a = 环类.环创建_通过点表(扁平List[0])
                    if len(扁平List) > 1:
                        for shape in 扁平List[1:]:
                            b = 环类.环创建_通过点表(shape)
                            a = 环类.多部件连接(a, b)  # type: ignore
                    点表 = 线类.坐标获取(a)  # type: ignore
                    # import bxpy

                    # bxpy.日志类.输出控制台(点表)
                    array = 数组类.数组创建()
                    part_array = 数组类.数组创建()
                    for pt in 点表:
                        点 = arc点类.点创建(*pt)
                        数组类.项插入(part_array, 点)  # type: ignore
                    数组类.项插入(array, part_array)  # type: ignore
                    需融合字段中需融合的值x["_形状"] = arc线类.线创建(array)
                    游标类.行插入_字典形式(游标_线, 需融合字段中需融合的值x, 操作字段名称列表)
        去孔后要素 = DIST_用地规划图线
    else:
        去孔后要素 = 切分后要素
    if CAD中图层采用的字段的名称:
        要素类.字段添加(去孔后要素, "Layer")
        要素类.字段计算(去孔后要素, "Layer", f"'YDGIS-' + !{CAD中图层采用的字段的名称}!.replace('/','／')")

        要素类.字段添加(去孔后要素, "地块性质")
        要素类.字段计算(去孔后要素, "地块性质", f"!{CAD中图层采用的字段的名称}!.replace('／','/')")

        要素类.字段添加(去孔后要素, "实体类型")
        要素类.字段计算(去孔后要素, "实体类型", '"控规地块"')

        要素类.字段删除(去孔后要素, ["ORIG_FID", CAD中图层采用的字段的名称, "是否切分"])
    # 去孔后要素.要素创建_通过复制并重命名重名要素("DIST_用地规划图2")
    # with bxarcpy.游标类.游标创建_通过名称("查询", 去孔后要素.名称, ["_形状"]) as 游标:
    #     for x in 游标:
    #         日志类.输出控制台(f"{bxarcpy.几何对象类.折点数量获取(x['_形状'])}")
    # 去孔后要素.要素创建_通过复制并重命名重名要素("AA_123")
    要素类.转换_到CAD(去孔后要素, 输出CAD路径)
    目录 = 路径类.属性获取_目录(输出CAD路径)
    文件名 = 路径类.属性获取_文件名(输出CAD路径)
    xml文件路径 = 路径类.连接(目录, 文件名, ".xml")
    路径类.删除(xml文件路径)


class 界面类:
    参数定义列表 = [
        {"参数名称": "输入要素路径", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "要素类", "是否多选": False, "默认值": "DIST_用地规划图"},
        {"参数名称": "规划范围线要素名称", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "要素类", "是否多选": False, "默认值": "JX_规划范围线"},
        {"参数名称": "需融合字段名称", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "字符串", "是否多选": False, "默认值": None},
        {"参数名称": "需融合字段中需融合的值的列表", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "字符串", "是否多选": True, "默认值": None},
        {"参数名称": "切分阈值", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "字符串", "是否多选": False, "默认值": None},
        {"参数名称": "是否去孔", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "字符串", "是否多选": False, "默认值": True},
        {"参数名称": "CAD中图层采用的字段的名称", "参数类型": "输入参数", "是否必须": "必填", "数据类型": "字符串", "是否多选": False, "默认值": None},
        {"参数名称": "输出CAD路径", "参数类型": "输出参数", "是否必须": "必填", "数据类型": "字符串", "是否多选": False, "默认值": r"C:\Users\beixiao\Desktop\01.dwg"},
    ]

    @staticmethod
    def 函数参数定义():
        from bxgis.配置 import 基本信息
        from bxarcpy.参数包 import 参数类

        输入要素 = 参数类.参数创建("输入要素", "要素类", 参数必要性="必填")

        是否将要素按范围裁剪 = 参数类.参数创建("是否将要素按范围裁剪", "布尔值", 默认值=False)

        规划范围线要素名称 = 参数类.参数创建("规划范围线要素名称", "要素类", 默认值=基本信息.项目信息.JX_规划范围线要素名称, 是否可用=False)

        是否对要素进行融合 = 参数类.参数创建("是否对要素进行融合", "布尔值", 默认值=False)

        需融合字段名称 = 参数类.参数创建("需融合字段名称", "字符串", 是否多个值=False, 是否可用=False, 默认值=基本信息.地块要素字段映射.地类编号字段名称)

        需融合字段中需融合的值的列表 = 参数类.参数创建("需融合字段中需融合的值的列表", "字符串", 是否多个值=True, 是否可用=False, 默认值=["1207"])

        是否对要素进行切分 = 参数类.参数创建("是否对要素进行切分", "布尔值", 默认值=False)

        切分时折点数量阈值 = 参数类.参数创建("切分时折点数量阈值", "长整型", 是否可用=False, 默认值=15000)

        切分时孔洞数量阈值 = 参数类.参数创建("切分时孔洞数量阈值", "长整型", 是否可用=False, 默认值=3)

        切分时面积阈值 = 参数类.参数创建("切分时面积阈值", "双精度", 是否可用=False, 默认值=500000)

        切分时地类编号限制列表 = 参数类.参数创建("切分时地类编号限制列表", "字符串", 是否多个值=True, 是否可用=False, 默认值=["1207"])

        是否去孔 = 参数类.参数创建("是否去孔", "布尔值", 默认值=False)

        输出CAD路径 = 参数类.参数创建("输出CAD路径", "CAD数据集", 参数类型="输出参数")

        return [输入要素, 是否将要素按范围裁剪, 规划范围线要素名称, 是否对要素进行融合, 需融合字段名称, 需融合字段中需融合的值的列表, 是否对要素进行切分, 切分时折点数量阈值, 切分时孔洞数量阈值, 切分时面积阈值, 切分时地类编号限制列表, 是否去孔, 输出CAD路径]

    @staticmethod
    def 函数参数更新(参数列表):
        from bxarcpy.参数包 import 参数类

        参数字典 = 参数类.参数列表转换_到字典(参数列表)
        if 参数类.属性获取_值(参数字典["是否将要素按范围裁剪"]):
            参数类.属性设置_是否可用(参数字典["规划范围线要素名称"], True)
        else:
            参数类.属性设置_是否可用(参数字典["规划范围线要素名称"], False)

        if 参数类.属性获取_值(参数字典["是否对要素进行融合"]):
            参数类.属性设置_是否可用(参数字典["需融合字段名称"], True)
            参数类.属性设置_是否可用(参数字典["需融合字段中需融合的值的列表"], True)
        else:
            参数类.属性设置_是否可用(参数字典["需融合字段名称"], False)
            参数类.属性设置_是否可用(参数字典["需融合字段中需融合的值的列表"], False)

        if 参数类.属性获取_值(参数字典["是否对要素进行切分"]):
            参数类.属性设置_是否可用(参数字典["切分时折点数量阈值"], True)
            参数类.属性设置_是否可用(参数字典["切分时孔洞数量阈值"], True)
            参数类.属性设置_是否可用(参数字典["切分时面积阈值"], True)
            参数类.属性设置_是否可用(参数字典["切分时地类编号限制列表"], True)
        else:
            参数类.属性设置_是否可用(参数字典["切分时折点数量阈值"], False)
            参数类.属性设置_是否可用(参数字典["切分时孔洞数量阈值"], False)
            参数类.属性设置_是否可用(参数字典["切分时面积阈值"], False)
            参数类.属性设置_是否可用(参数字典["切分时地类编号限制列表"], False)

        if str(参数类.属性获取_值(参数字典["输出CAD路径"]))[-4:] != ".dwg":
            参数类.属性设置_值(参数字典["输出CAD路径"], str(参数类.属性获取_值(参数字典["输出CAD路径"])) + ".dwg")
        return None

    @staticmethod
    def 函数运行(参数列表, 消息):
        from bxarcpy.参数包 import 参数类

        参数字典 = 参数类.参数列表转换_到字典_参数对象转换为值(参数列表)
        # 日志类.输出控制台(参数字典)
        规划范围线要素名称 = 参数字典["规划范围线要素名称"] if 参数字典["是否将要素按范围裁剪"] else None
        需融合字段中需融合的值的列表 = 参数字典["需融合字段中需融合的值的列表"] if 参数字典["是否对要素进行融合"] else None
        需融合字段名称 = 参数字典["需融合字段名称"] if 参数字典["是否对要素进行融合"] else None
        切分阈值 = {"折点数量": 参数字典["切分时折点数量阈值"], "孔洞数量": 参数字典["切分时孔洞数量阈值"], "面积": 参数字典["切分时面积阈值"], "地类编号列表": 参数字典["切分时地类编号限制列表"]} if 参数字典["是否对要素进行切分"] else None

        导出到CAD(
            输入要素路径=参数字典["输入要素"],
            规划范围线要素名称=规划范围线要素名称,
            需融合字段名称=需融合字段名称,
            需融合字段中需融合的值的列表=需融合字段中需融合的值的列表,
            切分阈值=切分阈值,
            是否去孔=参数字典["是否去孔"],
            输出CAD路径=参数字典["输出CAD路径"],
        )
        return None


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        # 导出到CAD(输入要素名称="XG_GHDK", 规划范围线要素名称=None, 需融合地类编号列表=None, 切分阈值=None, 是否去孔=True, CAD中图层采用的字段的名称="dldm", 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg")
        # 导出到CAD(输入要素名称="AA_开发边界内", 规划范围线要素名称=None, 需融合字段中需融合的值的列表=["1207", "1207v"], 切分阈值=None, 是否去孔=False, CAD中图层采用的字段的名称="dldm", 输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg")
        # 导出到CAD(输入要素路径="AA_开发边界内", 规划范围线要素名称=None, 需融合字段中需融合的值的列表=None, 切分阈值=None, 是否去孔=True, CAD中图层采用的字段的名称="地类编号", 输出CAD路径=r"C:\Users\beixiao\Desktop\AA_开发边界内.dwg")
        # 导出到CAD(输入要素路径="AA_开发边界外", 规划范围线要素名称=None, 需融合字段中需融合的值的列表=None, 切分阈值=None, 是否去孔=True, CAD中图层采用的字段的名称="地类编号", 输出CAD路径=r"C:\Users\beixiao\Desktop\AA_开发边界外.dwg")
        # 导出到CAD(
        #     输入要素路径="DIST_用地规划图",
        #     规划范围线要素名称=基本信息.项目信息.JX_规划范围线要素名称,
        #     需融合字段名称=None,
        #     需融合字段中需融合的值的列表=None,
        #     切分阈值=None,
        #     是否去孔=True,
        #     CAD中图层采用的字段的名称="地类编号",
        #     输出CAD路径=r"C:\Users\beixiao\Desktop\01.dwg",
        # )
        导出到CAD(
            输入要素路径="DIST_用地规划图",
            规划范围线要素名称=None,
            需融合字段名称=None,
            需融合字段中需融合的值的列表=None,
            切分阈值=None,
            是否去孔=True,
            CAD中图层采用的字段的名称="地类编号",
            输出CAD路径=r"C:\Users\beixiao\Desktop\02.dwg",
        )
