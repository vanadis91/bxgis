import bxarcpy
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 用地创建_通过根据地类名称生成编号(输入要素名称, 地类名称字段名称="地类名称", 输出要素名称="in_memory\\AA_计算地类编号"):
    if 输出要素名称 == "in_memory\\AA_计算地类编号":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()
    from bxpandas.数据框架包 import 数据框架类

    a = 数据框架类.转换_从excel文件(r"C:\Users\beixiao\AppConfig\Bxcad\Config\设计配置\设计参数\地块_指标测算表.xlsx", 要读取的列=[1, 3, 4], 指定数据类型={"性质名称": str, "地块性质": str, "地类标准": str})
    基数转换映射表 = 数据框架类.转换_到字典(a)  # type: ignore

    输入要素 = 要素类.要素创建_通过复制(输入要素名称)
    要素类.字段添加(输入要素, "地类编号")
    with 游标类.游标创建("更新", 输入要素, [地类名称字段名称, "地类编号"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [地类名称字段名称, "地类编号"]):
            对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["性质名称"] == x[地类名称字段名称] and 基数转换映射表1["地类标准"] == "国空"]
            if 对应的对象列表:
                x["地类编号"] = 对应的对象列表[0]["地块性质"]
                游标类.行更新_字典形式(游标, x)
            else:
                print(f"未找到该 地类名称 对应的 地类编号：{x[地类名称字段名称]}")

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        用地创建_通过根据地类名称生成编号("DIST_用地规划图", 地类名称字段名称="地类名称", 输出要素名称="in_memory\\AA_计算地类编号")
