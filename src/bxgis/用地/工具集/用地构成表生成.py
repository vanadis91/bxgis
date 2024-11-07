import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.路径包 import 路径类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 用地_工具集_用地构成表生成(
    用地要素路径,
    地类编号字段名称=基本信息.地块要素字段映射.地类编号字段名称,
    输出要素路径="内存临时",
):
    输出要素路径 = 工具包.输出路径生成_当采用内存临时时(["用地构成表生成"]) if 输出要素路径 == "内存临时" else 输出要素路径

    from bxpandas.数据框架包 import 数据框架类

    配置文件路径 = 路径类.连接(基本信息.计算机信息.bxgis根目录, "配置", "地块_指标测算表.xlsx")
    a = 数据框架类.转换_从excel文件(配置文件路径, 要读取的列=["性质名称", "地块性质", "地类标准"], 指定数据类型={"性质名称": str, "地块性质": str, "地类标准": str})
    基数转换映射表 = 数据框架类.转换_到字典(a)  # type: ignore

    用地要素 = 要素类.要素创建_通过复制(用地要素路径)
    用地汇总字典 = {}
    with 游标类.游标创建("查询", 用地要素, [地类编号字段名称, "_面积"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [地类编号字段名称, "_面积"]):
            用地汇总字典.setdefault(x[地类编号字段名称], 0)
            用地汇总字典[x[地类编号字段名称]] += x["_面积"]

    from bxpy.基本对象包 import 表类, 字类

    用地汇总字典_转表后 = []
    for k, v in 用地汇总字典.items():
        用地汇总字典_转表后.append([k, round(v, 2)])

    用地汇总字典_转表后 = 表类.排序(None, 用地汇总字典_转表后)
    print(用地汇总字典_转表后)

    return None


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        print("总的")
        用地_工具集_用地构成表生成("DIST_用地规划图")
        print("银湖村")
        用地_工具集_用地构成表生成("AA_用地规划图_银湖村")
        print("东坞山村")
        用地_工具集_用地构成表生成("AA_用地规划图_东坞山村")
        print("大庄村")
        用地_工具集_用地构成表生成("AA_用地规划图_大庄村")
