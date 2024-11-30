import bxarcpy
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxpy.日志包 import 日志生成器
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 统计开发边界外基期203用地(基期要素路径, 城镇集建区要素路径, 城镇弹性区要素路径, 规划范围线要素路径, 坐落单位要素路径, 输出要素路径="内存临时"):
    日志生成器.临时开启日志()
    from bxarcpy.工具包 import 输出路径生成_当采用内存临时时
    from bxgis.配置.基本信息 import 地块要素字段映射, 项目信息

    输出要素路径 = 输出路径生成_当采用内存临时时([基期要素路径]) if 输出要素路径 == "内存临时" else 输出要素路径

    基期要素路径 = 要素类.要素创建_通过复制(基期要素路径)
    城镇集建区要素路径 = 要素类.要素创建_通过复制(城镇集建区要素路径)
    城镇弹性区要素路径 = 要素类.要素创建_通过复制(城镇弹性区要素路径)

    基期要素路径 = 要素类.要素创建_通过擦除(基期要素路径, 城镇集建区要素路径)
    基期要素路径 = 要素类.要素创建_通过擦除(基期要素路径, 城镇弹性区要素路径)
    基期要素路径 = 要素类.要素创建_通过筛选(基期要素路径, f"{地块要素字段映射.地类编号字段名称} LIKE '0703%' OR {地块要素字段映射.地类编号字段名称} LIKE '0704%' OR {地块要素字段映射.地类编号字段名称} LIKE '%v%'")
    基期要素路径 = 要素类.要素创建_通过裁剪(基期要素路径, 规划范围线要素路径)

    if 日志生成器.属性获取_当前函数内日志开启状态():
        输出要素 = 要素类.要素创建_通过复制并重命名重名要素(基期要素路径, "AA_裁剪后的基期要素")
        日志生成器.输出调试并暂停("输出了裁剪后的基期要素")

    坐落单位要素路径 = 要素类.要素创建_通过复制(坐落单位要素路径)
    坐落单位要素路径 = 要素类.要素创建_通过裁剪(坐落单位要素路径, 规划范围线要素路径)

    if 日志生成器.属性获取_当前函数内日志开启状态():
        输出要素 = 要素类.要素创建_通过复制并重命名重名要素(坐落单位要素路径, "AA_裁剪后的坐落单位要素")
        日志生成器.输出调试并暂停("输出了裁剪后的坐落单位要素")

    基期要素路径 = 要素类.要素创建_通过联合并赋值字段(基期要素路径, 坐落单位要素路径, [["坐落单位名称", "坐落单位名称"]], 是否去除输入无联合有的部分=True)

    面积统计字典 = {}
    操作字段列表 = ["坐落单位名称", "_面积"]
    with 游标类.游标创建("查询", 基期要素路径, 操作字段列表) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, 操作字段列表):
            面积统计字典.setdefault(x["坐落单位名称"], 0)
            面积统计字典[x["坐落单位名称"]] += x["_面积"]

    from bxarcpy.环境包 import 输入输出类

    输入输出类.输出消息(f"开发边界外基期203用地统计：{面积统计字典}")
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(基期要素路径, 输出要素路径)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        统计开发边界外基期203用地(
            "DIST_用地基期图",
            "KZX_城镇集建区",
            "KZX_城镇弹性区",
            "JX_规划范围线",
            "CZ_三调筛选_坐落单位名称",
            "AC_开发边界外基期203用地",
        )
