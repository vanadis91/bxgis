# -*- coding: utf-8 -*-
import bxarcpy


def main(工作空间, 输入要素名称, 地类名称字段名称="地类名称"):
    with bxarcpy.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        bxarcpy.配置.是否覆盖输出要素 = True
        from bxpandas import 类 as pd

        a = pd.转换.excel转数据框架(r"C:\Users\beixiao\AppConfig\Bxcad\Config\设计配置\设计参数\地块_指标测算表.xlsx", 要读取的列=(1, 3, 4), 列数据类型={"性质名称": str, "地块性质": str, "地类标准": str})
        基数转换映射表 = pd.转换.数据框架转json(a)

        输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称)
        输入要素 = 输入要素.要素创建_通过复制()
        输入要素.字段添加("地类编号")
        with bxarcpy.游标类.游标创建_通过名称("更新", 输入要素.名称, [地类名称字段名称, "地类编号"]) as 游标:
            for x in 游标:
                对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["性质名称"] == x[地类名称字段名称] and 基数转换映射表1["地类标准"] == "国空"]
                if 对应的对象列表:
                    x["地类编号"] = 对应的对象列表[0]["地块性质"]
                    游标.行更新(x)
                else:
                    print(f"未找到该 地类名称 对应的 地类编号：{x[地类名称字段名称]}")

        输入要素.要素创建_通过复制并重命名重名要素(输入要素名称)


if __name__ == "__main__":
    # Global Environment settings
    # main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 输入要素名称="YD_GIS方案")
    main(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 输入要素名称="AA_test", 地类名称字段名称="JQXZYD")
