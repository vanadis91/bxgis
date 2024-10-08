import bxarcpy
from bxgis import 常用
from bxgis import 配置
import bxarcpy.工具包 as 工具包
from bxpy.日志包 import 日志类
from bxpy.时间包 import 时间类
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息
from bxgis.常用 import 属性更新


@时间类.装饰器_运行时长
def 设施更新(
    输入要素路径="SS_配套设施",
    是否根据坐标字段移动设施坐标=True,
    规划范围线要素名称="JX_规划范围线",
    工业片区范围线要素名称="JX_工业片区范围线",
    用地规划要素名称="DIST_用地规划图",
    城镇集建区要素名称="KZX_城镇集建区",
    城镇弹性区要素名称="KZX_城镇弹性区",
    输出要素名称="内存临时",
):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_设施更新" + "_" + 工具包.生成短GUID()
    设施要素路径 = 要素类.要素创建_通过复制(输入要素路径)

    日志类.输出调试("开始计算类别代码")
    设施要素路径 = _计算类别代码(设施要素路径)

    日志类.输出调试("开始计算位置精确度")
    设施要素路径 = _计算位置精确度(设施要素路径)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(设施要素路径, "AA_计算类别代码")
        日志类.输出调试并暂停("已计算类别代码")

    if 是否根据坐标字段移动设施坐标:
        日志类.输出调试("开始将设施的点移动到正确的位置")
        设施要素路径 = _移动至正确位置(设施要素路径)
    if 规划范围线要素名称:
        日志类.输出调试("开始清理规划范围线以外的设施")
        设施要素路径 = _清理范围外设施(设施要素路径, 规划范围线要素名称)

    if 工业片区范围线要素名称:
        日志类.输出调试("开始计算设施所属工业片区")
        设施要素路径 = 属性更新.要素创建_通过更新_根据面(设施要素路径, 工业片区范围线要素名称, 字段映射列表=[[基本信息.设施要素字段映射.所属工业片区字段名称, 基本信息.区域要素字段映射.区域编号字段名称]], 计算方式="内点在区域要素内")

    if 用地规划要素名称:
        日志类.输出调试("开始计算设施所属地块")
        设施要素路径 = _计算设施所属地块(设施要素路径, 用地规划要素名称)

    if 城镇集建区要素名称 and 城镇弹性区要素名称:
        日志类.输出调试("开始计算设施是否为远期预留")
        设施要素路径 = _计算远期预留(输入要素名称=设施要素路径, 城镇集建区要素名称=城镇集建区要素名称, 城镇弹性区要素名称=城镇弹性区要素名称)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(设施要素路径, "AA_计算远期预留")
        日志类.输出调试并暂停("已计算远期预留")

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(设施要素路径, 输出要素名称)
    return 输出要素
    # task: 计算开发动态字段


def _移动至正确位置(输入要素名称, 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_移动至正确位置" + "_" + 工具包.生成短GUID()

    设施要素 = 要素类.要素创建_通过复制(输入要素名称)
    if 基本信息.设施要素字段映射.设施坐标字段名称 not in 要素类.字段名称列表获取(设施要素):
        raise Exception(f"【{输入要素名称}】缺少【{基本信息.设施要素字段映射.设施坐标字段名称}】字段，无法移动设施坐标。字段的值的格式为：(x坐标 y坐标 z坐标)")
    with 游标类.游标创建("更新", 设施要素, ["SHAPE@XY", 基本信息.设施要素字段映射.设施坐标字段名称]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, ["SHAPE@XY", 基本信息.设施要素字段映射.设施坐标字段名称]):
            坐标字段内容: str = x[基本信息.设施要素字段映射.设施坐标字段名称]
            if 坐标字段内容[0] == "(":
                坐标字段内容 = 坐标字段内容[1:]
            if 坐标字段内容[-1] == ")":
                坐标字段内容 = 坐标字段内容[:-1]
            坐标字段内容 = 坐标字段内容.strip()
            if "," in 坐标字段内容:
                坐标字段内容列表 = 坐标字段内容.split(",")
            elif " " in 坐标字段内容:
                坐标字段内容列表 = 坐标字段内容.split(" ")
            # 设施坐标 = re.split(r"[()\s]", x[基本信息.设施要素字段映射.设施坐标字段名称])
            x["SHAPE@XY"] = (float(坐标字段内容列表[0]), float(坐标字段内容列表[1]))

            游标类.行更新_字典形式(游标, x)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(设施要素, 输出要素名称)
    return 输出要素


def _清理范围外设施(输入要素名称, 范围要素名称="JX_规划范围线", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_清理范围外设施" + "_" + 工具包.生成短GUID()

    设施要素 = 要素类.要素创建_通过复制(输入要素名称)
    范围要素 = 要素类.要素创建_通过复制(范围要素名称)

    相交后要素 = 要素类.要素创建_通过相交_原始([设施要素, 范围要素])
    要素类.字段删除(相交后要素, 保留字段名称列表=要素类.字段名称列表获取(设施要素))

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(相交后要素, 输出要素名称)
    return 输出要素


def _计算远期预留(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_计算远期预留" + "_" + 工具包.生成短GUID()

    设施要素 = 要素类.要素创建_通过复制(输入要素名称)
    集建区要素 = 要素类.要素创建_通过复制(城镇集建区要素名称)
    弹性区要素 = 要素类.要素创建_通过复制(城镇弹性区要素名称)
    开发边界要素 = 要素类.要素创建_通过合并([集建区要素, 弹性区要素])

    if 基本信息.控制线要素字段映射.控制线名称字段名称 not in 要素类.字段名称列表获取(开发边界要素):
        raise Exception(f"【{城镇集建区要素名称}】和【{城镇弹性区要素名称}】中未包括【{基本信息.控制线要素字段映射.控制线名称字段名称}】字段")

    要素类.字段添加(设施要素, "所属三线")
    设施要素 = 属性更新.要素创建_通过更新_根据面(设施要素, 开发边界要素, 字段映射列表=[["所属三线", 基本信息.控制线要素字段映射.控制线名称字段名称]], 计算方式="内点在区域要素内")
    要素类.字段添加(设施要素, 基本信息.设施要素字段映射.远期预留字段名称)

    需操作字段列表 = [基本信息.设施要素字段映射.远期预留字段名称, "所属三线", 基本信息.设施要素字段映射.开发动态字段名称]
    with 游标类.游标创建("更新", 设施要素, 需操作字段列表) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, 需操作字段列表):
            if x["所属三线"] in ["", " ", None] and x[基本信息.设施要素字段映射.开发动态字段名称] not in ["现状", "现状已实施", "现状保留"]:
                x[基本信息.设施要素字段映射.远期预留字段名称] = "是"
            else:
                x[基本信息.设施要素字段映射.远期预留字段名称] = "否"
            游标类.行更新_字典形式(游标, x)
    要素类.字段删除(设施要素, ["所属三线"])
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(设施要素, 输出要素名称)
    return 输出要素


def _计算设施所属地块(输入要素路径, 用地要素路径, 输出要素路径="内存临时"):
    if 输出要素路径 == "内存临时":
        输出要素路径 = "in_memory\\AA_计算设施所属地块" + "_" + 工具包.生成短GUID()
    设施要素 = 要素类.要素创建_通过复制(输入要素路径)

    用地要素 = 要素类.要素创建_通过复制(用地要素路径)
    用地要素 = 要素类.字段删除(用地要素, 保留字段名称列表=[基本信息.地块要素字段映射.地块编号字段名称])

    空间连接后要素 = 要素类.要素创建_通过空间连接(设施要素, 用地要素, "在连接要素内")
    要素类.字段计算(空间连接后要素, 基本信息.设施要素字段映射.设施所在地块编号字段名称, f"!{基本信息.地块要素字段映射.地块编号字段名称}!")
    要素类.字段删除(空间连接后要素, [基本信息.地块要素字段映射.地块编号字段名称, "Join_Count", "TARGET_FID"])

    输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(空间连接后要素, 输出要素路径)
    return 输出要素路径


def _计算类别代码(输入要素路径, 输出要素路径="内存临时"):
    if 输出要素路径 == "内存临时":
        输出要素路径 = "in_memory\\AA_计算设施所属地块" + "_" + 工具包.生成短GUID()
    设施要素 = 要素类.要素创建_通过复制(输入要素路径)

    from bxpy.基本对象包 import 字典类
    from bxpy.路径包 import 路径类

    excel路径 = 路径类.转绝对("..\\配置\\配套_指标测算表_杭州新.xlsx", 路径类.属性获取_目录(__file__))
    设施名称 = 基本信息.设施要素字段映射.设施名称字段名称
    类别代码 = 基本信息.设施要素字段映射.类别代码字段名称

    类别代码映射表 = 字典类.转换_从excel(excel路径, "Sheet2", 要读取的列=["设施名称", "类型代码"], 指定数据类型={"设施名称": str, "类别代码": str})

    要素类.字段添加(设施要素, 类别代码)
    未找到类别代码的设施名称集 = set()
    from bxpy.基本对象包 import 字类

    with 游标类.游标创建("更新", 设施要素, [设施名称, 类别代码]) as 游标:
        for 游标x in 游标类.属性获取_数据_字典形式(游标, [设施名称, 类别代码]):
            类别代码映射 = [映射 for 映射 in 类别代码映射表 if 游标x[设施名称] == 映射["设施名称"]]
            if len(类别代码映射) == 0:
                未找到类别代码的设施名称集.add(游标x[设施名称])
            else:
                游标x[类别代码] = 字类.格式_补位(类别代码映射[0]["类型代码"], 4)
                游标类.行更新_字典形式(游标, 游标x)
    if len(list(未找到类别代码的设施名称集)) > 0:
        raise Exception(f"以下设施名称未找到类别代码：{list(未找到类别代码的设施名称集)}")

    输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(设施要素, 输出要素路径)
    return 输出要素路径


def _计算位置精确度(输入要素路径, 输出要素路径="内存临时"):
    if 输出要素路径 == "内存临时":
        输出要素路径 = "in_memory\\AA_计算设施所属地块" + "_" + 工具包.生成短GUID()
    设施要素 = 要素类.要素创建_通过复制(输入要素路径)

    from bxpy.基本对象包 import 字典类
    from bxpy.路径包 import 路径类

    位置精确度 = 基本信息.设施要素字段映射.位置精确度字段名称

    要素类.字段添加(设施要素, 位置精确度)
    要素类.字段计算(设施要素, 位置精确度, "'地块级'")

    输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(设施要素, 输出要素路径)
    return 输出要素路径


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 日志类.开启()
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        设施更新(
            输入要素路径="SS_配套设施",
            规划范围线要素名称="JX_规划范围线",
            工业片区范围线要素名称="JX_工业片区范围线",
            用地规划要素名称="DIST_用地规划图",
            城镇集建区要素名称="KZX_城镇集建区",
            城镇弹性区要素名称="KZX_城镇弹性区",
            输出要素名称="SS_配套设施",
        )
