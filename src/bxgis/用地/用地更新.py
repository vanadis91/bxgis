# *-* coding:utf8 *-*

from bxpy.日志包 import 日志类
from bxpy.基本对象包 import 字类, 字典类
from typing import Union, Literal, Optional
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类, 字段类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息
from bxgis.常用 import 属性更新


def 用地更新(
    输入要素名称="DIST_用地规划图",
    街坊范围线要素名称: Optional[str] = "JX_街坊范围线",
    分村范围线要素名称: Optional[str] = "JX_分村范围线",
    城镇集建区要素名称="KZX_城镇集建区",
    城镇弹性区要素名称="KZX_城镇弹性区",
    有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数",
    有坐落单位信息的要素名称="CZ_三调筛选_坐落单位名称",
    设施要素名称: Union[str, None] = "SS_配套设施",
    输出要素名称="内存临时",
):
    日志类.临时关闭日志()
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_用地更新" + "_" + 工具包.生成短GUID()
    if 街坊范围线要素名称 is None and 分村范围线要素名称 is None:
        输入输出类.输出消息(f"因街坊范围线和分村范围线均不存在，所以无法自动生成地块编号。")
    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    输入输出类.输出消息("开始合规性检查")
    用地要素 = 用地数据合规性检查(用地要素)
    输入输出类.输出消息("通过了数据合规性检查")

    输入输出类.输出消息("开始融合部分地类")
    用地要素 = 融合部分地类(用地要素, 城镇集建区要素名称=城镇集建区要素名称, 城镇弹性区要素名称=城镇弹性区要素名称)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了部分地类的融合")
    输入输出类.输出消息("完成了部分地类的融合")

    输入输出类.输出消息("开始将地块根据扣除地类系数、开发边界、街坊、分村进行分割")
    用地要素 = 对用地进行分割(用地要素, [街坊范围线要素名称, 分村范围线要素名称])
    用地要素 = 对用地进行分割_按扣除地类系数分割耕地(用地要素, 有扣除地类系数的要素名称)
    用地要素 = 对用地进行分割_按开发边界分割非建设用地(用地要素, 城镇集建区要素名称, 城镇弹性区要素名称)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了根据开发边界_扣除地类系数_街区街坊线的分割")
    输入输出类.输出消息("完成了根据开发边界、扣除地类系数、街坊、分村的分割")

    if 街坊范围线要素名称:
        用地要素 = 属性更新.要素创建_通过更新_根据面(用地要素, 区域要素名称=街坊范围线要素名称, 字段映射列表=[[基本信息.地块要素字段映射.所属街坊字段名称, 基本信息.区域要素字段映射.区域编号字段名称]], 计算方式="分割输入要素")
        用地要素 = 根据所属街坊生成所属街区(用地要素)
    else:
        要素类.字段添加(用地要素, 基本信息.地块要素字段映射.所属街坊字段名称)

    if 分村范围线要素名称:
        用地要素 = 属性更新.要素创建_通过更新_根据面(用地要素, 区域要素名称=分村范围线要素名称, 字段映射列表=[[基本信息.地块要素字段映射.所属分村字段名称, 基本信息.区域要素字段映射.区域编号字段名称]], 计算方式="分割输入要素")
    else:
        要素类.字段添加(用地要素, 基本信息.地块要素字段映射.所属分村字段名称)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了根据街坊分村界线分割")
    输入输出类.输出消息("完成了根据街坊分村界线分割")

    用地要素 = 将道路根据街坊分村合并成多部件(用地要素)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了道路的融合_进行到这里地块界线稳定了")
    输入输出类.输出消息("完成了道路的融合_进行到这里地块界线稳定了")

    用地要素 = 计算耕保量(用地要素, 有扣除地类系数的要素名称=有扣除地类系数的要素名称)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了耕保量的计算")
    输入输出类.输出消息("完成了耕保量的计算")

    用地要素 = 根据地类编号生成名称(用地要素)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了根据地类编号生成名称")
    输入输出类.输出消息("完成了根据地类编号生成名称")

    用地要素 = 计算地块编号(用地要素, 城镇集建区要素名称, 城镇弹性区要素名称)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了地块编号的计算")
    输入输出类.输出消息("完成了地块编号的计算")

    用地要素 = 根据地类编号生成名称(用地要素)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了地类名称等的计算")
    输入输出类.输出消息("完成了地类名称等的计算")

    用地要素 = 计算土地码(用地要素, 地籍要素名称=有坐落单位信息的要素名称)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了土地码的计算")
    输入输出类.输出消息("完成了土地码的计算")

    用地要素 = 计算开发动态(用地要素)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了开发动态的计算")
    输入输出类.输出消息("完成了开发动态的计算")

    if 设施要素名称:
        用地要素 = 计算地块内设施规模(用地要素, 设施要素名称)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_完成了配套设施的计算")
    输入输出类.输出消息("完成了配套设施的计算")

    from bxgis.常用 import 数据检查

    用地要素 = 数据检查.数据检查(用地要素)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(用地要素, 输出要素名称)
    # task: 计算配套设施规模字段
    return 输出要素


def 用地数据合规性检查(用地要素路径):
    用地要素名称 = 要素类.属性获取_要素名称(用地要素路径)
    用地要素 = 要素类.要素创建_通过复制(用地要素路径)

    # 检查字段名称是否都包含
    字段名称列表 = 要素类.字段名称列表获取(用地要素)
    需要存在的字段名称列表 = [
        基本信息.地块要素字段映射.地块编号字段名称,
        基本信息.地块要素字段映射.地类编号字段名称,
        基本信息.地块要素字段映射.兼容比例字段名称,
        基本信息.地块要素字段映射.容积率字段名称,
        基本信息.地块要素字段映射.绿地率字段名称,
        基本信息.地块要素字段映射.建筑密度字段名称,
        基本信息.地块要素字段映射.建筑高度字段名称,
        基本信息.地块要素字段映射.城市设计刚性要求字段名称,
        基本信息.地块要素字段映射.城市设计弹性要求字段名称,
        基本信息.地块要素字段映射.开发动态字段名称,
        基本信息.地块要素字段映射.选择用地字段名称,
        基本信息.地块要素字段映射.备注字段名称,
        基本信息.地块要素字段映射.所属工业片区字段名称,
        基本信息.地块要素字段映射.户籍人数字段名称,
    ]
    # 部分字段不存在flag = False
    for x in 需要存在的字段名称列表:
        if x not in 字段名称列表:
            输入输出类.输出消息(f"【{用地要素名称}】中缺少【{x}】字段，已新建该字段")
            要素类.字段添加(用地要素, x)
    要素类.字段排序(用地要素, [基本信息.地块要素字段映射.地类编号字段名称])
    # if 部分字段不存在flag:
    #     raise Exception(f"【{用地要素路径}】中缺少部分必须要存在的字段。")

    # 检查字段的数据类型是否正确
    字段类型不准确flag = False
    字段列表 = 要素类.字段列表获取(用地要素)
    for x in 字段列表:
        if 字段类.属性获取_名称(x) in [
            基本信息.地块要素字段映射.容积率字段名称,
            基本信息.地块要素字段映射.绿地率字段名称,
            基本信息.地块要素字段映射.建筑密度字段名称,
            基本信息.地块要素字段映射.建筑高度字段名称,
        ]:
            if 字段类.属性获取_类型(x) != "String":
                字段类型不准确flag = True
                输入输出类.输出消息(f"{用地要素路径}的{字段类.属性获取_名称(x)}字段请采用定长字符串形式")
    if 字段类型不准确flag:
        raise Exception(f"部分字段的类型不准确。")

    # 检查地类编号是否存在空值
    地类编号存在空值的要素 = 要素类.要素创建_通过筛选(用地要素, f"{基本信息.地块要素字段映射.地类编号字段名称} IS NULL OR {基本信息.地块要素字段映射.地类编号字段名称} = ''")
    if 要素类.属性获取_几何数量(地类编号存在空值的要素) > 0:
        输入输出类.输出消息(f"{用地要素路径}部分地块的地类编号为空")
        raise Exception(f"{用地要素路径}部分地块的地类编号为空")
    return 用地要素


def 融合部分地类(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="内存临时"):
    # 需要保证所有地块都具有所属街区和所属街坊两个字段并赋值
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_融合部分地类" + "_" + 工具包.生成短GUID()

    地类编号字段名称 = 基本信息.地块要素字段映射.地类编号字段名称

    输入要素 = 要素类.要素创建_通过复制(输入要素名称)

    # # 公路编号
    # 公路要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '1202%'")
    # 公路要素 = 公路要素.要素创建_通过融合([地类编号字段名称])
    # 输入要素 = 输入要素.要素创建_通过更新并合并字段(公路要素.名称)

    # 道路编号
    道路要素 = 要素类.要素创建_通过筛选(输入要素, f"{地类编号字段名称} LIKE '1207%'")
    道路要素 = 要素类.要素创建_通过融合(道路要素, [地类编号字段名称])
    输入要素 = 要素类.要素创建_通过更新并合并字段(输入要素, 道路要素)

    # 非建设用地编号
    非建设用地要素 = 要素类.要素创建_通过筛选(输入要素, f"{地类编号字段名称} LIKE '01%' Or {地类编号字段名称} LIKE '02%' Or {地类编号字段名称} LIKE '03%' Or {地类编号字段名称} LIKE '04%' Or {地类编号字段名称} LIKE '05%' Or {地类编号字段名称} LIKE '06%' Or {地类编号字段名称} LIKE '17%'")
    非建设用地要素 = 要素类.要素创建_通过融合(非建设用地要素, [地类编号字段名称])
    输入要素 = 要素类.要素创建_通过更新并合并字段(输入要素, 非建设用地要素)

    # 输出
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素名称)
    return 输出要素


def 对用地进行分割_按扣除地类系数分割耕地(输入要素名称, 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 输出要素名称="in_memory\\AA_根据扣除地类系数分割"):
    日志类.临时关闭日志()
    if 输出要素名称 == "in_memory\\AA_根据扣除地类系数分割":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()

    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    有扣除地类系数的要素 = 要素类.要素创建_通过复制(有扣除地类系数的要素名称)
    if "扣除地类系数" not in 要素类.字段名称列表获取(有扣除地类系数的要素):
        raise Exception(f"{有扣除地类系数的要素名称}中未包括【扣除地类系数】字段，建议通过【用地/基期/字段处理并生成分项】来创建带有该字段的要素。")

    仅有耕地的要素 = 要素类.要素创建_通过筛选(用地要素, f"{基本信息.地块要素字段映射.地类编号字段名称} LIKE '01%'")

    既是耕地又带有扣除地类系数 = 要素类.要素创建_通过裁剪(输入要素路径=有扣除地类系数的要素名称, 裁剪要素路径=仅有耕地的要素)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(既是耕地又带有扣除地类系数, "AA_去除非耕地后有扣除地类系数的要素")
        日志类.输出调试并暂停("去除非耕地后有扣除地类系数的要素")

    分割后要素 = 要素类.要素创建_通过分割(用地要素, 既是耕地又带有扣除地类系数)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(分割后要素, "AA_分割后要素")
        日志类.输出调试并暂停("分割后要素")

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(分割后要素, 输出要素名称)
    return 输出要素


def 对用地进行分割_按开发边界分割非建设用地(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_按开发边界分割非建设用地" + "_" + 工具包.生成短GUID()

    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    城镇集建区 = 要素类.要素创建_通过复制(城镇集建区要素名称)
    城镇弹性区 = 要素类.要素创建_通过复制(城镇弹性区要素名称)

    地类编号字段名称 = 基本信息.地块要素字段映射.地类编号字段名称

    非建设用地 = 要素类.要素创建_通过筛选(用地要素, f"{地类编号字段名称} LIKE '01%' OR {地类编号字段名称} LIKE '02%' OR {地类编号字段名称} LIKE '03%' OR {地类编号字段名称} LIKE '04%' OR {地类编号字段名称} LIKE '05%' OR {地类编号字段名称} LIKE '06%' OR {地类编号字段名称} LIKE '17%' OR {地类编号字段名称} LIKE '1207%'")

    分割后要素 = 要素类.要素创建_通过分割(非建设用地, 城镇集建区)
    分割后要素 = 要素类.要素创建_通过分割(分割后要素, 城镇弹性区)
    用地要素 = 要素类.要素创建_通过更新(用地要素, 分割后要素)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(用地要素, "AA_分割后用地要素")
        日志类.输出调试并暂停("分割后用地要素")

    输出要素名称 = 要素类.要素创建_通过复制并重命名重名要素(用地要素, 输出要素名称)
    return 输出要素名称


def 对用地进行分割(输入要素路径, 分割要素列表, 输出要素路径="内存临时"):
    if 输出要素路径 == "内存临时":
        输出要素路径 = "in_memory\\AA_根据所属街坊生成所属街区" + "_" + 工具包.生成短GUID()
    用地 = 要素类.要素创建_通过复制(输入要素路径)
    for 分割要素路径x in 分割要素列表:
        if 分割要素路径x:
            分割要素 = 要素类.要素创建_通过复制(分割要素路径x)
            用地 = 要素类.要素创建_通过分割(用地, 分割要素)
    输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(用地, 输出要素路径)
    return 输出要素路径


def 根据所属街坊生成所属街区(输入要素名称, 输出要素名称="in_memory\\AA_根据所属街坊生成所属街区"):
    if 输出要素名称 == "in_memory\\AA_根据所属街坊生成所属街区":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()

    输入要素 = 要素类.要素创建_通过复制(输入要素名称)
    要素类.字段添加(输入要素, 基本信息.地块要素字段映射.所属街区字段名称)
    with 游标类.游标创建("更新", 输入要素, [基本信息.地块要素字段映射.所属街坊字段名称, 基本信息.地块要素字段映射.所属街区字段名称]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [基本信息.地块要素字段映射.所属街坊字段名称, 基本信息.地块要素字段映射.所属街区字段名称]):
            x[基本信息.地块要素字段映射.所属街区字段名称] = x[基本信息.地块要素字段映射.所属街坊字段名称][0:-2]
            游标类.行更新_字典形式(游标, x)

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素名称)
    return 输出要素


def 将道路根据街坊分村合并成多部件(输入要素名称, 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_道路合并成多部件" + "_" + 工具包.生成短GUID()
    地块要素 = 要素类.要素创建_通过复制(输入要素名称)
    道路要素 = 要素类.要素创建_通过筛选(地块要素, f"{基本信息.地块要素字段映射.地类编号字段名称} LIKE '1207%'")
    道路要素 = 要素类.要素创建_通过融合(
        道路要素,
        融合字段列表=[
            基本信息.地块要素字段映射.地类编号字段名称,
            基本信息.地块要素字段映射.所属街区字段名称,
            基本信息.地块要素字段映射.所属街坊字段名称,
            基本信息.地块要素字段映射.所属分村字段名称,
        ],
        是否单部件=False,
    )
    地块要素 = 要素类.要素创建_通过更新(地块要素, 道路要素)
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(地块要素, 输出要素名称)
    return 输出要素


def 计算地块编号(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_计算地块编号"):
    日志类.临时关闭日志()
    # 需要保证所有地块都具有所属街区和所属街坊两个字段并赋值
    if 输出要素名称 == "in_memory\\AA_计算地块编号":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()

    地块要素 = 要素类.要素创建_通过复制(输入要素名称)

    地类编号字段名称 = 基本信息.地块要素字段映射.地类编号字段名称
    地块编号字段名称 = 基本信息.地块要素字段映射.地块编号字段名称
    所属街坊字段名称 = 基本信息.地块要素字段映射.所属街坊字段名称
    所属分村字段名称 = 基本信息.地块要素字段映射.所属分村字段名称
    # 汇总已编号的地块情况
    需操作的字段名称列表 = [地类编号字段名称, 地块编号字段名称]
    地块编号字典 = {}
    编号存在重复flag = False
    with 游标类.游标创建("查询", 地块要素, 需操作的字段名称列表) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, 需操作的字段名称列表):
            if x[基本信息.地块要素字段映射.地块编号字段名称] not in ["", " ", None] and x[基本信息.地块要素字段映射.地类编号字段名称][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x[基本信息.地块要素字段映射.地类编号字段名称][0:4] not in ["1207"]:
                地块编号序号 = int(x[基本信息.地块要素字段映射.地块编号字段名称].split("-")[-1])
                地块所属区域 = x[基本信息.地块要素字段映射.地块编号字段名称].split("-")[0]
                if 地块所属区域 in 地块编号字典 and 地块编号序号 not in 地块编号字典[地块所属区域]:
                    地块编号字典[地块所属区域].append(地块编号序号)
                elif 地块所属区域 in 地块编号字典 and 地块编号序号 in 地块编号字典[地块所属区域]:
                    编号存在重复flag = True
                    输入输出类.输出消息(f"{x[基本信息.地块要素字段映射.地块编号字段名称]}存在重复")
                else:
                    地块编号字典[地块所属区域] = [地块编号序号]
    if 编号存在重复flag:
        raise Exception(f"部分地块的地块编号存在重复。")
    # print(f"地块编号字典：{地块编号字典}")
    日志类.输出调试并暂停(f"既有的地块编号字典：{地块编号字典}", 内容长度=20000)

    # 对未编号的建设用地进行编号
    是否有地块所属街坊和分村都为空flag = False
    操作字段 = [基本信息.地块要素字段映射.地类编号字段名称, 基本信息.地块要素字段映射.地块编号字段名称, 基本信息.地块要素字段映射.所属街坊字段名称, 基本信息.地块要素字段映射.所属分村字段名称, "_ID"]
    日志类.输出调试(f"地块要素字段列表：{要素类.字段名称列表获取(地块要素)}")
    with 游标类.游标创建("更新", 地块要素, 操作字段) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, 操作字段):
            地块编号序号 = 1
            if x[基本信息.地块要素字段映射.地块编号字段名称] in ["", " ", None] and x[基本信息.地块要素字段映射.地类编号字段名称][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x[基本信息.地块要素字段映射.地类编号字段名称][0:4] not in ["1207"]:
                if x[基本信息.地块要素字段映射.所属街坊字段名称] not in ["", " ", None]:
                    字典类.默认值设置(地块编号字典, [x[基本信息.地块要素字段映射.所属街坊字段名称]], [])
                    while 地块编号序号 in 地块编号字典[x[基本信息.地块要素字段映射.所属街坊字段名称]]:
                        地块编号序号 += 1
                    地块编号字典[x[基本信息.地块要素字段映射.所属街坊字段名称]].append(地块编号序号)
                    x[基本信息.地块要素字段映射.地块编号字段名称] = x[基本信息.地块要素字段映射.所属街坊字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                    游标类.行更新_字典形式(游标, x)
                elif x[基本信息.地块要素字段映射.所属分村字段名称] not in ["", " ", None]:
                    字典类.默认值设置(地块编号字典, [x[基本信息.地块要素字段映射.所属分村字段名称]], [])
                    while 地块编号序号 in 地块编号字典[x[基本信息.地块要素字段映射.所属分村字段名称]]:
                        地块编号序号 += 1
                    地块编号字典[x[基本信息.地块要素字段映射.所属分村字段名称]].append(地块编号序号)
                    x[基本信息.地块要素字段映射.地块编号字段名称] = x[基本信息.地块要素字段映射.所属分村字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                    游标类.行更新_字典形式(游标, x)
                else:
                    是否有地块所属街坊和分村都为空flag = True
                    输入输出类.输出消息(f"ID为{x['_ID']}的地块所属街坊和所属分村都为空，无法生成编号。")
    if 是否有地块所属街坊和分村都为空flag:
        raise Exception("似乎有地块所属街坊和所属分村均为空。")
    日志类.输出调试并暂停(f"建设用地编号结束后的编号字典：{地块编号字典}", 内容长度=20000)

    # 对开发边界内的非建设用地（含河道、耕地等）进行编号
    非建设用地 = 要素类.要素创建_通过筛选(地块要素, f"{地类编号字段名称} LIKE '01%' Or {地类编号字段名称} LIKE '02%' Or {地类编号字段名称} LIKE '03%' Or {地类编号字段名称} LIKE '04%' Or {地类编号字段名称} LIKE '05%' Or {地类编号字段名称} LIKE '06%' Or {地类编号字段名称} LIKE '17%'")
    要素类.字段计算(非建设用地, 地块编号字段名称, "''")  # 清空所有非建设用地编号
    地块要素 = 要素类.要素创建_通过更新(地块要素, 非建设用地)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(地块要素, "AA_已完成非建设用地编号清除")
        日志类.输出调试并暂停("已完成非建设用地编号清除")

    非建设用地_边界外 = 要素类.要素创建_通过擦除(非建设用地, 城镇集建区要素名称)
    非建设用地_边界外 = 要素类.要素创建_通过擦除(非建设用地_边界外, 城镇弹性区要素名称)
    非建设用地_边界内 = 要素类.要素创建_通过擦除(非建设用地, 非建设用地_边界外)

    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(非建设用地_边界内, "AA_已完成边界内非建设用地提取")
        日志类.输出调试并暂停("已完成边界内非建设用地提取")

    是否有河道所属街坊和分村都为空flag = False
    with 游标类.游标创建("更新", 非建设用地_边界内, [地类编号字段名称, 地块编号字段名称, 所属街坊字段名称, 所属分村字段名称, "_ID"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [地类编号字段名称, 地块编号字段名称, 所属街坊字段名称, 所属分村字段名称, "_ID"]):
            地块编号序号 = 1
            if x[所属街坊字段名称] not in ["", " ", None]:
                字典类.默认值设置(地块编号字典, [x[所属街坊字段名称]], [])
                日志类.输出调试(f"当前{x[所属街坊字段名称]}编号列表是：{地块编号字典[x[所属街坊字段名称]]}")
                while 地块编号序号 in 地块编号字典[x[所属街坊字段名称]]:
                    地块编号序号 += 1
                地块编号字典[x[所属街坊字段名称]].append(地块编号序号)
                x[地块编号字段名称] = x[所属街坊字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                日志类.输出调试(f"开发边界内非建设用地被编号为：{x[地块编号字段名称]}")
                游标类.行更新_字典形式(游标, x)
            elif x[所属分村字段名称] not in ["", " ", None]:
                字典类.默认值设置(地块编号字典, [x[所属分村字段名称]], [])
                while 地块编号序号 in 地块编号字典[x[所属分村字段名称]]:
                    地块编号序号 += 1
                地块编号字典[x[所属分村字段名称]].append(地块编号序号)
                x[地块编号字段名称] = x[所属分村字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                游标类.行更新_字典形式(游标, x)
            else:
                是否有河道所属街坊和分村都为空flag = True
                输入输出类.输出消息(f"ID为{x['_ID']}的非建设用地所属街坊和所属分村都为空，无法生成编号。")
    if 是否有河道所属街坊和分村都为空flag:
        raise Exception("似乎有河道所属街坊和所属分村均为空")
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(非建设用地_边界内, "AA_已完成边界内非建设用地的编号")
        日志类.输出调试并暂停("已完成边界内非建设用地的编号")

    地块要素 = 要素类.要素创建_通过更新并合并字段(地块要素, 非建设用地_边界内, 是否多部件转单部件=False)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(地块要素, "AA_已完成非建设用地编号的合并")
        日志类.输出调试并暂停("已完成非建设用地编号的合并")
    日志类.输出调试并暂停(f"开发边界内非建设用地编号结束后的编号字典：{地块编号字典}", 内容长度=20000)

    # 道路编号
    道路要素 = 要素类.要素创建_通过筛选(地块要素, f"{地类编号字段名称} LIKE '1207%'")
    是否有道路所属街坊和分村都为空flag = False
    with 游标类.游标创建("更新", 道路要素, [地类编号字段名称, 地块编号字段名称, 所属街坊字段名称, 所属分村字段名称, "_ID"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [地类编号字段名称, 地块编号字段名称, 所属街坊字段名称, 所属分村字段名称, "_ID"]):
            if x[所属街坊字段名称] not in ["", " ", None]:
                if x[地类编号字段名称] == "1207":
                    x[地块编号字段名称] = x[所属街坊字段名称] + "-" + "CZ"
                elif x[地类编号字段名称] == "1207v":
                    x[地块编号字段名称] = x[所属街坊字段名称] + "-" + "XC"
            elif x[所属分村字段名称] not in ["", " ", None]:
                if x[地类编号字段名称] == "1207":
                    x[地块编号字段名称] = x[所属分村字段名称] + "-" + "CZ"
                elif x[地类编号字段名称] == "1207v":
                    x[地块编号字段名称] = x[所属分村字段名称] + "-" + "XC"
            else:
                是否有道路所属街坊和分村都为空flag = True
                输入输出类.输出消息(f"ID为{x['_ID']}的道路所属街坊和所属分村都为空，无法生成编号。")
            游标类.行更新_字典形式(游标, x)
    if 是否有道路所属街坊和分村都为空flag:
        raise Exception("似乎有道路所属街区和所属分村均为空")
    地块要素 = 要素类.要素创建_通过更新并合并字段(地块要素, 道路要素, 是否多部件转单部件=False)
    日志类.输出调试并暂停(f"道路编号结束后的编号字典：{地块编号字典}", 内容长度=20000)
    # 非建设用地编号
    非建设用地要素 = 要素类.要素创建_通过筛选(地块要素, f"{地类编号字段名称} LIKE '01%' Or {地类编号字段名称} LIKE '02%' Or {地类编号字段名称} LIKE '03%' Or {地类编号字段名称} LIKE '04%' Or {地类编号字段名称} LIKE '05%' Or {地类编号字段名称} LIKE '06%' Or {地类编号字段名称} LIKE '17%'")
    非建设用地编号 = 0
    是否有非建设用地所属街坊和分村都为空flag = False
    with 游标类.游标创建("更新", 非建设用地要素, [地块编号字段名称, 所属街坊字段名称, 所属分村字段名称, "_ID"]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, [地块编号字段名称, 所属街坊字段名称, 所属分村字段名称, "_ID"]):
            if x[所属街坊字段名称] not in ["", " ", None]:
                if x[地块编号字段名称] in ["", " ", None]:
                    非建设用地编号 += 1
                    x[地块编号字段名称] = x[所属街坊字段名称][0:4] + "-" + 字类.格式_补位(str(非建设用地编号), 2)  # type: ignore
            elif x[所属分村字段名称] not in ["", " ", None]:
                if x[地块编号字段名称] in ["", " ", None]:
                    非建设用地编号 += 1
                    x[地块编号字段名称] = x[所属分村字段名称][0:4] + "-" + 字类.格式_补位(str(非建设用地编号), 2)  # type: ignore
            else:
                是否有非建设用地所属街坊和分村都为空flag = True
                输入输出类.输出消息(f"ID为{x['_ID']}的非建设用地所属街坊和所属分村都为空，无法生成编号。")
            游标类.行更新_字典形式(游标, x)
    if 是否有非建设用地所属街坊和分村都为空flag:
        raise ValueError("似乎有非建设用地所属街区和所属分村均为空")
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(地块要素, "AA_已完成所有非建设用地编号")
        日志类.输出调试并暂停("已完成所有非建设用地编号")
    地块要素 = 要素类.要素创建_通过更新并合并字段(地块要素, 非建设用地要素, 是否多部件转单部件=False)
    日志类.输出调试并暂停(f"开发边界外非建设用地编号后字典：{地块编号字典}", 内容长度=20000)
    要素类.字段删除(地块要素, ["ORIG_FID", "扣除地类系数"])
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(地块要素, 输出要素名称)
    return 输出要素


def 计算耕保量(输入要素名称, 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 输出要素名称="in_memory\\AA_计算耕保量"):
    日志类.临时关闭日志()
    if 输出要素名称 == "in_memory\\AA_计算耕保量":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()

    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    要素类.字段删除(用地要素, ["扣除地类系数", 基本信息.地块要素字段映射.耕地保有量字段名称])

    有扣除地类系数的要素 = 要素类.要素创建_通过复制(有扣除地类系数的要素名称)
    if "扣除地类系数" not in 要素类.字段名称列表获取(有扣除地类系数的要素):
        raise Exception(f"{有扣除地类系数的要素名称}中未包括【扣除地类系数】字段，建议通过【用地/基期/字段处理并生成分项】来创建带有该字段的要素。")

    仅有耕地的要素 = 要素类.要素创建_通过筛选(用地要素, f"{基本信息.地块要素字段映射.地类编号字段名称} LIKE '01%'")
    带有扣除系数的耕地要素 = 要素类.要素创建_通过裁剪(有扣除地类系数的要素名称, 仅有耕地的要素)
    带有扣除系数的耕地要素 = 要素类.要素创建_通过多部件至单部件(带有扣除系数的耕地要素)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(带有扣除系数的耕地要素, "AA_带有扣除系数的耕地要素")
        日志类.输出调试并暂停("带有扣除系数的耕地要素")

    合并扣除系数后要素 = 要素类.要素创建_通过联合并赋值字段(用地要素, 带有扣除系数的耕地要素, [["扣除地类系数", "扣除地类系数"]], 要素被分割时提示信息中包括的字段=[基本信息.地块要素字段映射.地类编号字段名称], 是否多部件转单部件=False)
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(合并扣除系数后要素, "AA_合并扣除系数后的要素")
        日志类.输出调试并暂停("合并扣除系数后")
    # 要素类.字段删除(合并扣除系数后要素, ["Shape_Length_1", "Shape_Area_1"])
    要素类.字段添加(合并扣除系数后要素, 字段名称=基本信息.地块要素字段映射.耕地保有量字段名称, 字段类型="双精度", 字段长度=10)

    from bxpy.基本对象包 import 字类

    耕地保有量汇总 = 0
    操作字段列表 = [基本信息.地块要素字段映射.地类编号字段名称, "扣除地类系数", "SHAPE@AREA", 基本信息.地块要素字段映射.耕地保有量字段名称]
    with 游标类.游标创建("更新", 合并扣除系数后要素, 操作字段列表) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, 操作字段列表):
            if 字类.匹配正则(x[基本信息.地块要素字段映射.地类编号字段名称], "^01"):
                if x["扣除地类系数"] in ["", None, " "]:
                    x["扣除地类系数"] = 0.0
                耕地保有量 = (1.0 - float(x["扣除地类系数"])) * x["SHAPE@AREA"]
                耕地保有量汇总 += 耕地保有量
                x[基本信息.地块要素字段映射.耕地保有量字段名称] = 耕地保有量
                游标类.行更新_字典形式(游标, x)
    输入输出类.输出消息(f"耕地保有量总和为：{耕地保有量汇总}")

    要素类.字段删除(合并扣除系数后要素, ["扣除地类系数"])
    # 不同扣除系数的耕地最终还是根据地块编号进行了合并
    # 仅有耕地的要素 = 要素类.要素创建_通过筛选(合并扣除系数后要素, f"{基本信息.地块要素字段映射.地类编号字段名称} LIKE '01%'")
    # 仅有耕地的要素 = 要素类.要素创建_通过融合(仅有耕地的要素, [基本信息.地块要素字段映射.地块编号字段名称, 基本信息.地块要素字段映射.地类编号字段名称], [[基本信息.地块要素字段映射.耕地保有量字段名称, "SUM"]])

    # 合并扣除系数后要素 = 要素类.要素创建_通过更新并合并字段(合并扣除系数后要素, 仅有耕地的要素)
    # 要素类.字段删除(合并扣除系数后要素, ["扣除地类系数", 基本信息.地块要素字段映射.耕地保有量字段名称])
    # 要素类.字段修改(合并扣除系数后要素, "SUM_" + 基本信息.地块要素字段映射.耕地保有量字段名称, 基本信息.地块要素字段映射.耕地保有量字段名称, 基本信息.地块要素字段映射.耕地保有量字段名称, 清除字段别称=False)

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(合并扣除系数后要素, 输出要素名称)
    return 输出要素


def 根据地类编号生成名称(
    输入要素名称,
    地类编号字段名称=基本信息.地块要素字段映射.地类编号字段名称,
    性质名称字段名称=基本信息.地块要素字段映射.性质名称字段名称,
    地块性质别称字段名称=基本信息.地块要素字段映射.地块性质别称字段名称,
    用地构成字段名称=基本信息.地块要素字段映射.用地大类字段名称,
    输出要素名称="内存临时",
):
    日志类.临时关闭日志()
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_根据地类编号生成名称" + "_" + 工具包.生成短GUID()

    输入要素 = 要素类.要素创建_通过复制(输入要素名称)
    from bxpy.路径包 import 路径类

    当前文件所在目录 = 路径类.属性获取_目录(__file__)
    转换文件路径 = 路径类.转绝对(f"..", 当前文件所在目录)
    from bxpandas.数据框架包 import 数据框架类

    a = 数据框架类.转换_从excel文件(转换文件路径 + r"\配置\地块_指标测算表.xlsx", 要读取的列=["性质名称", "地块性质", "地类标准", "地块性质别称", "用地构成"], 指定数据类型={"性质名称": str, "地块性质": str, "地类标准": str, "地块性质别称": str, "用地构成": str})
    基数转换映射表 = 数据框架类.转换_到字典(a)  # type: ignore
    日志类.输出调试(f"基数转换映射表为：{基数转换映射表}", 文件输出路径=r"C:\Users\beixiao\Desktop\01.txt", 内容长度=100000)
    要素类.字段添加(输入要素, 性质名称字段名称)
    要素类.字段添加(输入要素, 地块性质别称字段名称)
    要素类.字段添加(输入要素, 用地构成字段名称)
    部分地类未找到名称flag = False
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(输入要素, "AA_TEST2")
        日志类.输出调试(f"输入要素已导出")
    with 游标类.游标创建("更新", 输入要素, [地类编号字段名称, 性质名称字段名称, 地块性质别称字段名称, 用地构成字段名称]) as 游标:
        try:
            for x in 游标类.属性获取_数据_字典形式(游标, [地类编号字段名称, 性质名称字段名称, 地块性质别称字段名称, 用地构成字段名称]):
                日志类.输出调试(f"当前性质为：{x}")
                对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["地块性质"] == x[地类编号字段名称] and 基数转换映射表1["地类标准"] == "国空"]
                日志类.输出调试(f"基数转换映射表中获取到的对应项为：{对应的对象列表}")
                if 对应的对象列表:
                    x[性质名称字段名称] = 对应的对象列表[0]["性质名称"]
                    x[地块性质别称字段名称] = 对应的对象列表[0]["地块性质别称"]
                    x[用地构成字段名称] = 对应的对象列表[0]["用地构成"]
                    游标类.行更新_字典形式(游标, x)
                else:
                    输入输出类.输出消息(f"未找到 {x[地类编号字段名称]} 对应的 性质名称。")
                    部分地类未找到名称flag = True
        except Exception as e:
            from bxpy.元数据包 import 追踪元数据类

            strrrr = 追踪元数据类.追踪信息获取()
            print(strrrr)
            # 日志类.输出调试(f"追踪到的错误：{strrrr}", 文件输出路径=r"C:\Users\beixiao\Desktop\01.txt")
    if 部分地类未找到名称flag:
        raise Exception("部分地类编号没有找到对应的性质名称，请通过bxgis/配置/地块_指标测算表.xlsx添加地类。")
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素名称)
    return 输出要素


def 计算土地码(输入要素名称, 地籍要素名称="CZ_三调筛选_坐落单位名称", 输出要素名称="in_memory\\AA_计算土地码"):
    # 需要保证该编号的地块都已经编号
    日志类.临时关闭日志()
    if 输出要素名称 == "in_memory\\AA_计算土地码":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()

    地块要素 = 要素类.要素创建_通过复制(输入要素名称)
    地籍要素 = 要素类.要素创建_通过复制(地籍要素名称)
    if "坐落单位代码" not in 要素类.字段名称列表获取(地籍要素):
        raise Exception(f"{地籍要素名称}中未包括 坐落单位代码 字段，建议通过 用地/基期/字段处理并生成分项 来创建带有该字段的要素。")
    要素类.字段添加(地块要素, 基本信息.地块要素字段映射.土地码字段名称)
    要素类.字段删除(地块要素, ["坐落单位代码"])
    要素类.字段删除(地籍要素, 保留字段名称列表=["坐落单位代码"])
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(地籍要素, "AA_清理字段后的地籍要素")
        日志类.输出调试并暂停("清理字段后的地籍要素")

    有地籍地块要素 = 要素类.要素创建_通过空间连接(地块要素, 地籍要素, "内点在连接要素内")

    需操作的字段名称列表 = [基本信息.地块要素字段映射.地块编号字段名称, 基本信息.地块要素字段映射.地类编号字段名称, 基本信息.地块要素字段映射.土地码字段名称, "坐落单位代码"]

    地块编号存在空值的要素 = 要素类.要素创建_通过筛选(有地籍地块要素, f"{基本信息.地块要素字段映射.地块编号字段名称} IS NULL")
    if 要素类.属性获取_几何数量(地块编号存在空值的要素) > 0:
        raise Exception(f"部分地块的地块编号为空，影响土地码生成。")
    if 日志类.属性获取_当前函数内日志开启状态():
        要素类.要素创建_通过复制并重命名重名要素(有地籍地块要素, "AA_将地块和地籍空间连接后")
        日志类.输出调试并暂停("导出了地块和地籍空间连接后要素")
    with 游标类.游标创建("更新", 有地籍地块要素, 需操作的字段名称列表) as 游标_地块:
        for x in 游标类.属性获取_数据_字典形式(游标_地块, 需操作的字段名称列表):
            地籍代码 = "H00000000"
            主地类编号 = "00000000"
            兼容性质数量 = 1
            街区编号 = "00"
            街坊编号 = "00"
            地块编号 = "000"

            # print(x["地块编号"])
            # print(len(x["地块编号"].split("-")))
            # print(x["地类编号"][0:2])

            if x[基本信息.地块要素字段映射.地块编号字段名称] not in ["", " ", None] and len(x[基本信息.地块要素字段映射.地块编号字段名称].split("-")) == 2 and len(x[基本信息.地块要素字段映射.地块编号字段名称].split("-")[0]) == 8:
                地籍代码 = "H" + x["坐落单位代码"][4:12]
                主地类编号 = x[基本信息.地块要素字段映射.地类编号字段名称].split("(")[0].split("/")[0].replace("v", "")
                兼容性质数量 = len(x[基本信息.地块要素字段映射.地类编号字段名称].split("(")[0].split("/"))
                街区编号 = x[基本信息.地块要素字段映射.地块编号字段名称][4:6]
                街坊编号 = x[基本信息.地块要素字段映射.地块编号字段名称][6:8]
                地块编号 = 字类.格式_补位(x[基本信息.地块要素字段映射.地块编号字段名称].split("-")[-1], 3)
                # print(地籍代码 + 主地类编号.ljust(8, "0") + f"X{兼容性质数量}" + 街区编号 + 街坊编号 + 地块编号 + "0")

                土地码 = 地籍代码 + 字类.格式_补位(主地类编号, 8, "后方") + f"X{兼容性质数量}" + 街区编号 + 街坊编号 + 地块编号 + "0"
                x[基本信息.地块要素字段映射.土地码字段名称] = 土地码

            游标类.行更新_字典形式(游标_地块, x)

    要素类.字段删除(有地籍地块要素, ["坐落单位代码"])
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(有地籍地块要素, 输出要素名称)
    return 输出要素


def 计算开发动态(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_计算开发动态"):
    if 输出要素名称 == "in_memory\\AA_计算开发动态":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()
    from bxgis import 配置
    from bxgis.常用 import 属性更新

    输入要素 = 要素类.要素创建_通过复制(输入要素名称)
    集建区要素 = 要素类.要素创建_通过复制(城镇集建区要素名称)
    弹性区要素 = 要素类.要素创建_通过复制(城镇弹性区要素名称)
    开发边界要素 = 要素类.要素创建_通过合并([集建区要素, 弹性区要素])
    if 基本信息.控制线要素字段映射.控制线名称字段名称 not in 要素类.字段名称列表获取(开发边界要素):
        raise Exception(f"{城镇集建区要素名称}和{城镇弹性区要素名称}中未包括 {基本信息.控制线要素字段映射.控制线名称字段名称} 字段。")
    用地要素 = 属性更新.要素创建_通过更新_根据面(输入要素, 开发边界要素, 字段映射列表=[["所属三线", "控制线名称"]], 计算方式="内点在区域要素内")
    with 游标类.游标创建("更新", 用地要素, ["所属三线", 基本信息.地块要素字段映射.地类编号字段名称, 基本信息.地块要素字段映射.开发动态字段名称]) as 游标:
        for x in 游标类.属性获取_数据_字典形式(游标, ["所属三线", 基本信息.地块要素字段映射.地类编号字段名称, 基本信息.地块要素字段映射.开发动态字段名称]):
            if x["所属三线"] not in ["", " ", None]:
                x["所属三线"] = "开发边界内"

            if x["开发动态"] in ["现状已实施", "现状保留", "保留"]:
                x["开发动态"] = "保留"
            elif x["开发动态"] in ["改/扩建", "改扩建", "盘活"] and x["所属三线"] == "开发边界内":
                x["开发动态"] = "改/扩建"
            elif x["开发动态"] in ["改/扩建", "改扩建", "盘活"] and x["所属三线"] != "开发边界内":
                x["开发动态"] = "盘活"
            elif x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"] and x["所属三线"] == "开发边界内":
                x["开发动态"] = "新建"
            elif x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"] and x["所属三线"] != "开发边界内":
                x["开发动态"] = "新增"
            else:
                x["开发动态"] = None

            游标类.行更新_字典形式(游标, x)
    要素类.字段删除(用地要素, ["所属三线"])

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(用地要素, 输出要素名称)
    return 输出要素


def 计算地块内设施规模(输入要素名称="DIST_用地规划图", 设施要素名称="SS_配套设施", 输出要素名称="内存临时"):
    日志类.临时关闭日志()
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_计算地块内设施规模" + "_" + 工具包.生成短GUID()

    用地要素 = 要素类.要素创建_通过复制(输入要素名称)
    设施要素 = 要素类.要素创建_通过复制(设施要素名称)

    设施字段名称列表 = 要素类.字段名称列表获取(设施要素)
    日志类.输出调试(f"设施字段名称列表：{设施字段名称列表}")
    if 基本信息.设施要素字段映射.设施名称字段名称 not in 设施字段名称列表 or 基本信息.设施要素字段映射.设施规模字段名称 not in 设施字段名称列表:
        raise Exception(f"{输入要素名称}缺少了{基本信息.设施要素字段映射.设施名称字段名称}或者{基本信息.设施要素字段映射.设施规模字段名称}字段。")

    要素类.字段添加(用地要素, 基本信息.地块要素字段映射.配套设施规模字段名称, 字段长度=255)
    要素类.字段添加(用地要素, 基本信息.地块要素字段映射.配套设施规模字段名称 + "2", 字段长度=255)
    要素类.字段添加(用地要素, 基本信息.地块要素字段映射.配套设施规模字段名称 + "3", 字段长度=255)
    使用到了配套设施规模2字段 = False
    使用到了配套设施规模3字段 = False
    用地游标操作字段 = ["_ID", "_形状", 基本信息.地块要素字段映射.配套设施规模字段名称, 基本信息.地块要素字段映射.配套设施规模字段名称 + "2", 基本信息.地块要素字段映射.配套设施规模字段名称 + "3"]
    设施游标操作字段 = ["_ID", "_形状", 基本信息.设施要素字段映射.设施名称字段名称, 基本信息.设施要素字段映射.设施规模字段名称]
    with 游标类.游标创建("更新", 用地要素, 用地游标操作字段) as 用地游标:
        with 游标类.游标创建("查询", 设施要素, 设施游标操作字段) as 设施游标:
            for 用地x in 游标类.属性获取_数据_字典形式(用地游标, 用地游标操作字段):
                地块设施规模内容 = []
                if 日志类.属性获取_当前函数内日志开启状态():
                    if int(用地x["_ID"]) == 300:
                        日志类.输出调试并暂停("开始ID300对象")
                for 设施x in 游标类.属性获取_数据_字典形式(设施游标, 设施游标操作字段):
                    if 几何类.关系_包含(用地x["_形状"], 设施x["_形状"]):
                        设施名称 = 设施x[基本信息.设施要素字段映射.设施名称字段名称]
                        设施规模 = 设施x[基本信息.设施要素字段映射.设施规模字段名称]
                        retList = [x for x in 地块设施规模内容 if x["设施名称"] == 设施名称]
                        if len(retList) > 0:
                            if 设施规模 not in ["", " ", None]:
                                newRet = {"设施名称": 设施名称, "设施数量": retList[0]["设施数量"] + 1, "设施规模": retList[0]["设施规模"] + "," + 设施规模}
                            else:
                                newRet = {"设施名称": 设施名称, "设施数量": retList[0]["设施数量"] + 1, "设施规模": retList[0]["设施规模"]}
                            地块设施规模内容.remove(retList[0])
                            地块设施规模内容.append(newRet)
                        else:
                            if 设施规模 not in ["", " ", None]:
                                newRet = {"设施名称": 设施名称, "设施数量": 1, "设施规模": 设施规模}
                            else:
                                newRet = {"设施名称": 设施名称, "设施数量": 1, "设施规模": ""}
                            地块设施规模内容.append(newRet)
                游标类.重置(设施游标)
                if 日志类.属性获取_当前函数内日志开启状态():
                    if int(用地x["_ID"]) == 300:
                        日志类.输出调试(f"地块设施规模内容为：{地块设施规模内容}")
                地块设施规模内容_字符串形式 = ""
                for x in 地块设施规模内容:
                    if x["设施规模"] not in ["", " ", None]:
                        地块设施规模内容_字符串形式 = f'{地块设施规模内容_字符串形式}{x["设施名称"]}-{str(x["设施数量"])}-{str(x["设施规模"])}/'
                    else:
                        地块设施规模内容_字符串形式 = f'{地块设施规模内容_字符串形式}{x["设施名称"]}-{str(x["设施数量"])}/'
                地块设施规模内容_字符串形式 = 地块设施规模内容_字符串形式[:-1]
                if 日志类.属性获取_当前函数内日志开启状态():
                    if int(用地x["_ID"]) == 300:
                        日志类.输出调试(f"地块设施规模内容_字符串形式为：{地块设施规模内容_字符串形式}")
                if len(地块设施规模内容_字符串形式) > 765:
                    raise Exception(f"ID为{用地x['_ID']}的地块的配套设施规模字符串长度超过了765。")
                elif len(地块设施规模内容_字符串形式) > 510:
                    用地x[基本信息.地块要素字段映射.配套设施规模字段名称] = 地块设施规模内容_字符串形式[0:255]
                    用地x[基本信息.地块要素字段映射.配套设施规模字段名称 + "2"] = 地块设施规模内容_字符串形式[255:510]
                    用地x[基本信息.地块要素字段映射.配套设施规模字段名称 + "3"] = 地块设施规模内容_字符串形式[510:]
                    使用到了配套设施规模2字段 = True
                    使用到了配套设施规模3字段 = True
                elif len(地块设施规模内容_字符串形式) > 255:
                    用地x[基本信息.地块要素字段映射.配套设施规模字段名称] = 地块设施规模内容_字符串形式[0:255]
                    用地x[基本信息.地块要素字段映射.配套设施规模字段名称 + "2"] = 地块设施规模内容_字符串形式[255:]
                    使用到了配套设施规模2字段 = True
                else:
                    用地x[基本信息.地块要素字段映射.配套设施规模字段名称] = 地块设施规模内容_字符串形式
                游标类.行更新_字典形式(用地游标, 用地x)
    if 使用到了配套设施规模3字段 == False:
        要素类.字段删除(用地要素, [基本信息.地块要素字段映射.配套设施规模字段名称 + "3"])
    if 使用到了配套设施规模2字段 == False:
        要素类.字段删除(用地要素, [基本信息.地块要素字段映射.配套设施规模字段名称 + "2"])
    用地要素 = 要素类.字段排序(用地要素, [基本信息.地块要素字段映射.地类编号字段名称])

    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(用地要素, 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    日志类.开启()
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        用地更新(
            输入要素名称="DIST_用地规划图",
            街坊范围线要素名称="JX_街坊范围线",
            分村范围线要素名称=None,
            城镇集建区要素名称="KZX_城镇集建区",
            城镇弹性区要素名称="KZX_城镇弹性区",
            有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数",
            有坐落单位信息的要素名称="CZ_三调筛选_坐落单位名称",
            设施要素名称="SS_配套设施",
            输出要素名称="DIST_用地规划图",
        )
        # 根据地类编号生成名称(
        #     "XG_GHDK",
        #     "dldm",
        #     "dlmc",
        #     "dlbm",
        #     基本信息.地块要素字段映射.用地大类字段名称,
        #     "XG_GHDK1",
        # )
