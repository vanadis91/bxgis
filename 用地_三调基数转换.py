# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2023-09-23 15:58:06
"""
import arcpy
import bxarcpy


def main(工作空间=None, 输入要素名称=None):
    with bxarcpy.类.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        # 用地_三调基数转换
        # To allow overwriting outputs change overwriteOutput option to True.
        # arcpy.env.overwriteOutput = False
        bxarcpy.类.配置.是否覆盖输出要素 = True

        # 地类转换表格 = "C:\\Users\\common\\AppConfig\\ArcGIS\\020.地类转换\\地类转换_三调与国空基数转换.xls\\Sheet1$"

        from bxpandas import 类 as pd

        a = pd.转换.excel转数据框架(r"C:\Users\common\AppConfig\ArcGIS\020.地类转换\地类转换_三调与国空基数转换.xls", 要读取的列=range(0, 5, 1), 列数据类型={"三调编码": str, "国空代码": str})
        基数转换映射表 = pd.转换.数据框架转json(a)

        输入要素 = bxarcpy.类.要素类.要素读取_通过名称(输入要素名称)
        输入要素 = 输入要素.要素创建_通过复制()
        输入要素.字段添加("地类编号_国空")
        输入要素.字段添加("基数转换关系")
        with bxarcpy.类.游标类_用于更新(输入要素.名称, ["地类编号", "地类编号_国空", "基数转换关系"]) as cur:
            for cur1 in cur:
                对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["三调编码"] == cur1.数据_列表格式[0]]
                if 对应的对象列表:
                    cur1.数据_列表格式[1] = 对应的对象列表[0]["国空代码"]
                    cur1.数据_列表格式[2] = 对应的对象列表[0]["转换类型"]
                    cur1.行更新_列表格式()
                else:
                    print(f"未找到该 三调地类编号 对应的 国空地类编号：{cur1.数据_列表格式[0]}")

        # try:
        #     输入要素.连接取消("Sheet1$")
        # except Exception as res:
        #     raise Exception(f"错误信息: {res}")
        # 输入要素.连接创建("地类编号", 地类转换表格, "三调编码")

        # 输入要素.字段计算(字段名称=输入要素名称 + ".地类编号_国空", 表达式="!Sheet1$.国空代码!")
        # 输入要素.字段计算(字段名称=输入要素名称 + ".基数转换关系", 表达式="!Sheet1$.转换类型!")

        选择集 = 输入要素.选择集创建_通过属性(SQL语句=f"城镇村属性码 LIKE '203%' AND 地类编号_国空 LIKE '1207%'")
        选择集.字段计算(字段名称="地类编号_国空", 表达式="'060102'")

        选择集 = 输入要素.选择集创建_通过属性(SQL语句=f"城镇村属性码 LIKE '203%' AND 地类编号_国空 LIKE '08%'")
        选择集.字段计算(字段名称="地类编号_国空", 表达式="'0704'")

        选择集 = 输入要素.选择集创建_通过属性(SQL语句=f"城镇村属性码 LIKE '203%' AND 地类编号_国空 NOT LIKE '060102%' AND 地类编号_国空 NOT LIKE '0703%' AND 地类编号_国空 NOT LIKE '0704%'")
        选择集.字段计算(字段名称="地类编号_国空", 表达式="!地类编号_国空!+'v'")
        输入要素.字段修改("地类编号", "地类编号_三调")
        输入要素.字段修改("地类名称", "地类名称_三调")
        输入要素.字段删除(保留字段名称列表=["地类编号_三调", "地类名称_三调", "地类编号_国空", "基数转换关系"])
        输入要素.字段修改("地类编号_国空", "地类编号")
        输入要素.要素创建_通过复制并重命名重名要素("YD_基期初转换")

        # 输入要素.连接取消("Sheet1$")


if __name__ == "__main__":
    # Global Environment settings
    main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 输入要素名称="CZ_三调")
