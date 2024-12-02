import bxarcpy
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息
from bxarcpy.工具包 import 输出路径生成_当采用内存临时时


def 初步基数转换(输入要素路径="YD_三调_字段汉化", 输出要素路径="内存临时"):
    输出要素路径 = 输出路径生成_当采用内存临时时([输入要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

    from bxpy.路径包 import 路径类
    import os

    当前文件所在目录 = 路径类.属性获取_目录(__file__)

    转换文件路径 = 路径类.连接(基本信息.计算机信息.bxgis根目录, "配置", "地类转换_三调与国空基数转换.xls")

    from bxpandas.数据框架包 import 数据框架类

    a = 数据框架类.转换_从excel文件(转换文件路径, 要读取的列=list(range(0, 5, 1)), 指定数据类型={"三调编码": str, "国空代码": str})
    基数转换映射表 = 数据框架类.转换_到字典(a)  # type: ignore

    输入要素 = 要素类.要素创建_通过复制(输入要素路径)
    要素类.字段添加(输入要素, "地类编号")
    要素类.字段添加(输入要素, "基数转换关系")
    if "地类编号_三调" not in 要素类.字段名称列表获取(输入要素):
        raise Exception("当前输入要素不存在 地类编号_三调 字段，需通过 bxgis/用地/基期/字段处理并生成分项 或者 手动 来将 DLBM 字段重命名为 地类编号_三调。")

    是否有三调地类未找到了对应的国空地类flag = False
    操作字段名称列表 = ["地类编号_三调", "地类编号", "基数转换关系", "城镇村属性码"]
    with 游标类.游标创建("更新", 输入要素, 操作字段名称列表) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, 操作字段名称列表):
            对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["三调编码"] == x["地类编号_三调"]]
            if 对应的对象列表:
                x["地类编号"] = 对应的对象列表[0]["国空代码"]
                x["基数转换关系"] = 对应的对象列表[0]["转换类型"]
                if x["城镇村属性码"] and x["城镇村属性码"].startswith("203") and x["地类编号"].startswith("1207"):
                    x["地类编号"] = "1207v"
                elif x["城镇村属性码"] and x["城镇村属性码"].startswith("203") and x["地类编号"].startswith("08"):
                    x["地类编号"] = "0704"
                elif x["城镇村属性码"] and x["城镇村属性码"].startswith("203") and not x["地类编号"].startswith("1207") and not x["地类编号"].startswith("08") and not x["地类编号"].startswith("0703") and not x["地类编号"].startswith("0704"):
                    if x["地类编号"].startswith("07") or x["地类编号"].startswith("08") or x["地类编号"].startswith("09") or x["地类编号"].startswith("1001") or x["地类编号"].startswith("11") or x["地类编号"].startswith("1208") or x["地类编号"].startswith("1209") or (x["地类编号"].startswith("13") and not x["地类编号"].startswith("1311")) or x["地类编号"].startswith("14") or x["地类编号"].startswith("16") or x["地类编号"].startswith("2301"):
                        x["地类编号"] = x["地类编号"] + "v"
                    else:
                        x["基数转换关系"] = x["基数转换关系"] + "，在203中"
                        输入输出类.输出消息(f'在203中存在{x["地类编号"]}，地类没有加v')
                游标类.行更新_字典形式(游标, x)
            else:
                是否有三调地类未找到了对应的国空地类flag = True
                输入输出类.输出消息(f"未找到三调地类 {x['地类编号_三调']} 对应的 国空地类，请在 bxgis/配置/地类转换_三调与国空基数转换.xls 中添加相应的地类。")

    if 是否有三调地类未找到了对应的国空地类flag:
        raise Exception("存在部分三调地类未找到对应的国空地类。")

    # 输入要素.字段修改("地类编号", "地类编号_三调")
    # 输入要素.字段修改("地类名称", "地类名称_三调")
    要素类.字段删除(输入要素, 保留字段名称列表=["地类编号_三调", "地类名称_三调", "地类编号", "基数转换关系"])
    # 输入要素.字段修改("地类编号_国空", "地类编号")
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        初步基数转换("CZ_三调", 输出要素路径="YD_基数初转换")
