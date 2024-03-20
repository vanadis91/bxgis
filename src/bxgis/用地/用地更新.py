import bxarcpy
from bxpy.基本对象包 import 字类, 字典类
from bxgis import 配置
from typing import Union, Literal
from bxgis import 常用


def 用地更新(输入要素名称="DIST_用地规划图", 街坊范围线要素名称="JX_街坊范围线", 分村范围线要素名称="JX_分村范围线", 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 有坐落单位信息的要素名称="CZ_三调筛选_坐落单位名称", 设施要素名称="SS_配套设施", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_用地更新" + "_" + bxarcpy.工具集.生成短GUID()
    if 街坊范围线要素名称 is None and 分村范围线要素名称 is None:
        bxarcpy.环境.输出消息(f"因不存在街坊范围线或者分村范围线，所以无法自动生成地块编号。")
    用地要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    用地要素 = 用地数据合规性检查(用地要素.名称)
    用地要素 = 融合部分地类(用地要素.名称, 城镇集建区要素名称=城镇集建区要素名称, 城镇弹性区要素名称=城镇弹性区要素名称)
    if 街坊范围线要素名称:
        用地要素 = 常用.计算所属区域.计算所属区域(用地要素.名称, 区域要素名称=街坊范围线要素名称, 字段映射列表=[[配置.地块要素字段映射.所属街坊字段名称, 配置.区域要素字段映射.区域编号字段名称]], 计算方式="分割输入要素")
        用地要素 = 根据所属街坊生成所属街区(用地要素.名称)
    if 分村范围线要素名称:
        用地要素 = 常用.计算所属区域.计算所属区域(用地要素.名称, 区域要素名称=分村范围线要素名称, 字段映射列表=[[配置.地块要素字段映射.所属分村字段名称, 配置.区域要素字段映射.区域编号字段名称]], 计算方式="分割输入要素")
    用地要素 = 计算地块编号(用地要素.名称)
    用地要素 = 计算耕保量(用地要素.名称, 有扣除地类系数的要素名称=有扣除地类系数的要素名称)
    用地要素 = 根据地类编号生成名称(用地要素.名称)
    用地要素 = 计算土地码(用地要素.名称, 地籍要素名称=有坐落单位信息的要素名称)
    用地要素 = 计算开发动态(用地要素.名称)
    用地要素 = 计算地块内设施规模(用地要素.名称, 设施要素名称)
    输出要素 = 用地要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    # task: 计算配套设施规模字段
    return 输出要素


def 用地数据合规性检查(用地要素名称):
    用地要素 = bxarcpy.要素类.要素读取_通过名称(用地要素名称).要素创建_通过复制()

    # 检查字段名称是否都包含
    字段名称列表 = 用地要素.字段名称列表获取()
    需要存在的字段名称列表 = [
        配置.地块要素字段映射.地块编号字段名称,
        配置.地块要素字段映射.地类编号字段名称,
        配置.地块要素字段映射.兼容比例字段名称,
        配置.地块要素字段映射.容积率字段名称,
        配置.地块要素字段映射.绿地率字段名称,
        配置.地块要素字段映射.建筑密度字段名称,
        配置.地块要素字段映射.建筑高度字段名称,
        配置.地块要素字段映射.城市设计刚性要求字段名称,
        配置.地块要素字段映射.城市设计弹性要求字段名称,
        配置.地块要素字段映射.开发动态字段名称,
        配置.地块要素字段映射.选择用地字段名称,
        配置.地块要素字段映射.备注字段名称,
    ]
    部分字段不存在flag = False
    for x in 需要存在的字段名称列表:
        if x not in 字段名称列表:
            部分字段不存在flag = True
            bxarcpy.环境.输出消息(f"{用地要素名称}中缺少{x}字段")
    if 部分字段不存在flag:
        raise ValueError(f"{用地要素名称}中缺少{x}字段。")

    # 检查字段的数据类型是否正确
    字段类型不准确flag = False
    字段列表 = 用地要素.字段列表获取()
    for x in 字段列表:
        if x.名称 in [
            配置.地块要素字段映射.容积率字段名称,
            配置.地块要素字段映射.绿地率字段名称,
            配置.地块要素字段映射.建筑密度字段名称,
            配置.地块要素字段映射.建筑高度字段名称,
        ]:
            if x.类型 != "String":
                字段类型不准确flag = True
                bxarcpy.环境.输出消息(f"{用地要素名称}的{x.名称}字段请采用定长字符串形式")
    if 字段类型不准确flag:
        raise ValueError(f"部分字段的类型不准确。")

    # 检查地类编号是否存在空值
    地类编号存在空值的要素 = 用地要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} IS NULL")
    if 地类编号存在空值的要素.几何数量 > 0:
        bxarcpy.环境.输出消息(f"{用地要素名称}部分地块的地类编号为空")
        raise ValueError(f"{用地要素名称}部分地块的地类编号为空")
    return 用地要素


def 融合部分地类(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_融合部分地类"):
    # 需要保证所有地块都具有所属街区和所属街坊两个字段并赋值
    if 输出要素名称 == "in_memory\\AA_融合部分地类":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    地类编号字段名称 = 配置.地块要素字段映射.地类编号字段名称

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

    # # 公路编号
    # 公路要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '1202%'")
    # 公路要素 = 公路要素.要素创建_通过融合([地类编号字段名称])
    # 输入要素 = 输入要素.要素创建_通过更新并合并字段(公路要素.名称)

    # 道路编号
    道路要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '1207%'")
    道路要素 = 道路要素.要素创建_通过融合([地类编号字段名称])
    输入要素 = 输入要素.要素创建_通过更新并合并字段(道路要素.名称)

    # 非建设用地编号
    非建设用地要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '01%' Or {地类编号字段名称} LIKE '02%' Or {地类编号字段名称} LIKE '03%' Or {地类编号字段名称} LIKE '04%' Or {地类编号字段名称} LIKE '05%' Or {地类编号字段名称} LIKE '06%' Or {地类编号字段名称} LIKE '17%'")
    非建设用地要素 = 非建设用地要素.要素创建_通过融合([地类编号字段名称])
    输入要素 = 输入要素.要素创建_通过更新并合并字段(非建设用地要素.名称)

    # 将河道根据开发边界进行了切分
    输入要素字段名称列表 = 输入要素.字段名称列表获取()
    仅河道要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '17%'")
    temp1 = 仅河道要素.要素创建_通过相交([城镇集建区要素名称]).字段删除(保留字段名称列表=输入要素字段名称列表)
    仅河道要素 = 仅河道要素.要素创建_通过更新并合并字段(temp1.名称)
    temp1 = 仅河道要素.要素创建_通过相交([城镇弹性区要素名称]).字段删除(保留字段名称列表=输入要素字段名称列表)
    仅河道要素 = 仅河道要素.要素创建_通过更新并合并字段(temp1.名称)
    输入要素 = 仅河道要素.要素创建_通过更新并合并字段(仅河道要素.名称)

    # 输出
    输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 根据所属街坊生成所属街区(输入要素名称, 输出要素名称="in_memory\\AA_根据所属街坊生成所属街区"):
    if 输出要素名称 == "in_memory\\AA_根据所属街坊生成所属街区":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    输入要素.字段添加(配置.地块要素字段映射.所属街区字段名称)
    with bxarcpy.游标类.游标创建_通过名称("更新", 输入要素.名称, [配置.地块要素字段映射.所属街坊字段名称, 配置.地块要素字段映射.所属街区字段名称]) as 游标:
        for x in 游标:
            x[配置.地块要素字段映射.所属街区字段名称] = x[配置.地块要素字段映射.所属街坊字段名称][0:-2]
            游标.行更新(x)

    输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 计算地块编号(输入要素名称, 输出要素名称="in_memory\\AA_计算地块编号"):
    # 需要保证所有地块都具有所属街区和所属街坊两个字段并赋值
    if 输出要素名称 == "in_memory\\AA_计算地块编号":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    地块要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

    # 汇总已编号的地块情况
    需操作的字段名称列表 = [配置.地块要素字段映射.地类编号字段名称, 配置.地块要素字段映射.地块编号字段名称]
    地块编号字典 = {}
    编号存在重复flag = False
    with bxarcpy.游标类.游标创建_通过名称("查找", 地块要素.名称, 需操作的字段名称列表) as 游标:
        for x in 游标:
            if x[配置.地块要素字段映射.地块编号字段名称] not in ["", " ", None] and x[配置.地块要素字段映射.地类编号字段名称][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x[配置.地块要素字段映射.地类编号字段名称][0:4] not in ["1207"]:
                地块编号序号 = int(x[配置.地块要素字段映射.地块编号字段名称].split("-")[-1])
                地块所属区域 = x[配置.地块要素字段映射.地块编号字段名称].split("-")[0]
                if 地块所属区域 in 地块编号字典 and 地块编号序号 not in 地块编号字典[地块所属区域]:
                    地块编号字典[地块所属区域].append(地块编号序号)
                elif 地块所属区域 in 地块编号字典 and 地块编号序号 in 地块编号字典[地块所属区域]:
                    编号存在重复flag = True
                    bxarcpy.环境.输出消息(f"{x[配置.地块要素字段映射.地块编号字段名称]}存在重复")
                else:
                    地块编号字典[地块所属区域] = [地块编号序号]
    if 编号存在重复flag:
        raise ValueError(f"部分地块的地块编号存在重复。")
    # print(f"地块编号字典：{地块编号字典}")

    # 对未编号的建设用地进行编号
    是否有地块所属街坊和分村都为空flag = False
    with bxarcpy.游标类.游标创建_通过名称("更新", 地块要素.名称, [配置.地块要素字段映射.地类编号字段名称, 配置.地块要素字段映射.地块编号字段名称, 配置.地块要素字段映射.所属街坊字段名称, 配置.地块要素字段映射.所属分村字段名称, "_ID"]) as 游标:
        for x in 游标:
            地块编号序号 = 1
            if x[配置.地块要素字段映射.地块编号字段名称] in ["", " ", None] and x[配置.地块要素字段映射.地类编号字段名称][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x[配置.地块要素字段映射.地类编号字段名称][0:4] not in ["1207"]:
                if x[配置.地块要素字段映射.所属街坊字段名称] not in ["", " ", None]:
                    字典类.默认值设置(地块编号字典, [配置.地块要素字段映射.所属街坊字段名称], [])
                    while 地块编号序号 in 地块编号字典[配置.地块要素字段映射.所属街坊字段名称]:
                        地块编号序号 += 1
                    地块编号字典[配置.地块要素字段映射.所属街坊字段名称].append(地块编号序号)
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属街坊字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                    游标.行更新(x)
                elif x[配置.地块要素字段映射.所属分村字段名称] not in ["", " ", None]:
                    字典类.默认值设置(地块编号字典, [配置.地块要素字段映射.所属分村字段名称], [])
                    while 地块编号序号 in 地块编号字典[配置.地块要素字段映射.所属分村字段名称]:
                        地块编号序号 += 1
                    地块编号字典[配置.地块要素字段映射.所属分村字段名称].append(地块编号序号)
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属分村字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                    游标.行更新(x)
                else:
                    是否有地块所属街坊和分村都为空flag = True
                    bxarcpy.环境.输出消息(f"ID为{x['_ID']}的地块所属街坊和所属分村都为空，无法生成编号。")
    if 是否有地块所属街坊和分村都为空flag:
        raise ValueError("似乎有地块所属街坊和所属分村均为空。")

    # 对开发边界内的河道进行编号
    仅河道要素 = 地块要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} LIKE '17%'")
    是否有河道所属街坊和分村都为空flag = False
    with bxarcpy.游标类.游标创建_通过名称("更新", 仅河道要素.名称, [配置.地块要素字段映射.地类编号字段名称, 配置.地块要素字段映射.地块编号字段名称, 配置.地块要素字段映射.所属街坊字段名称, 配置.地块要素字段映射.所属分村字段名称, "_ID"]) as 游标:
        for x in 游标:
            地块编号序号 = 1
            if x[配置.地块要素字段映射.地块编号字段名称] in ["", " ", None] and x[配置.地块要素字段映射.地类编号字段名称][0:2] in ["17"]:
                if x[配置.地块要素字段映射.所属街坊字段名称] not in ["", " ", None]:
                    字典类.默认值设置(地块编号字典, [配置.地块要素字段映射.所属街坊字段名称], [])
                    while 地块编号序号 in 地块编号字典[配置.地块要素字段映射.所属街坊字段名称]:
                        地块编号序号 += 1
                    地块编号字典[配置.地块要素字段映射.所属街坊字段名称].append(地块编号序号)
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属街坊字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                    游标.行更新(x)
                elif x[配置.地块要素字段映射.所属分村字段名称] not in ["", " ", None]:
                    字典类.默认值设置(地块编号字典, [配置.地块要素字段映射.所属分村字段名称], [])
                    while 地块编号序号 in 地块编号字典[配置.地块要素字段映射.所属分村字段名称]:
                        地块编号序号 += 1
                    地块编号字典[配置.地块要素字段映射.所属分村字段名称].append(地块编号序号)
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属分村字段名称] + "-" + 字类.格式_补位(str(地块编号序号), 2)
                    游标.行更新(x)
                else:
                    是否有河道所属街坊和分村都为空flag = True
                    bxarcpy.环境.输出消息(f"ID为{x['_ID']}的河道所属街坊和所属分村都为空，无法生成编号。")
    if 是否有河道所属街坊和分村都为空flag:
        raise ValueError("似乎有河道所属街坊和所属分村均为空")
    地块要素 = 地块要素.要素创建_通过更新并合并字段(仅河道要素.名称)

    # 道路编号
    道路要素 = 地块要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} LIKE '1207%'")
    是否有道路所属街坊和分村都为空flag = False
    with bxarcpy.游标类.游标创建_通过名称("更新", 道路要素.名称, [配置.地块要素字段映射.地类编号字段名称, 配置.地块要素字段映射.地块编号字段名称, 配置.地块要素字段映射.所属街坊字段名称, 配置.地块要素字段映射.所属分村字段名称, "_ID"]) as 游标:
        for x in 游标:
            if x[配置.地块要素字段映射.所属街坊字段名称] not in ["", " ", None]:
                if x[配置.地块要素字段映射.地类编号字段名称] == "1207":
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属街坊字段名称] + "-" + "SS1"
                elif x[配置.地块要素字段映射.地类编号字段名称] == "1207v":
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属街坊字段名称] + "-" + "XS1"
            elif x[配置.地块要素字段映射.所属分村字段名称] not in ["", " ", None]:
                if x[配置.地块要素字段映射.地类编号字段名称] == "1207":
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属分村字段名称] + "-" + "SS1"
                elif x[配置.地块要素字段映射.地类编号字段名称] == "1207v":
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属分村字段名称] + "-" + "XS1"
            else:
                是否有道路所属街坊和分村都为空flag = True
                bxarcpy.环境.输出消息(f"ID为{x['_ID']}的道路所属街坊和所属分村都为空，无法生成编号。")
            游标.行更新(x)
    if 是否有道路所属街坊和分村都为空flag:
        raise ValueError("似乎有道路所属街区和所属分村均为空")
    地块要素 = 地块要素.要素创建_通过更新并合并字段(道路要素.名称)

    # 非建设用地编号
    非建设用地要素 = 地块要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} LIKE '01%' Or {配置.地块要素字段映射.地类编号字段名称} LIKE '02%' Or {配置.地块要素字段映射.地类编号字段名称} LIKE '03%' Or {配置.地块要素字段映射.地类编号字段名称} LIKE '04%' Or {配置.地块要素字段映射.地类编号字段名称} LIKE '05%' Or {配置.地块要素字段映射.地类编号字段名称} LIKE '06%' Or {配置.地块要素字段映射.地类编号字段名称} LIKE '17%'")
    非建设用地编号 = 0
    是否有非建设用地所属街坊和分村都为空flag = False
    with bxarcpy.游标类.游标创建_通过名称("更新", 非建设用地要素.名称, [配置.地块要素字段映射.地块编号字段名称, 配置.地块要素字段映射.所属街坊字段名称, 配置.地块要素字段映射.所属分村字段名称, "_ID"]) as 游标:
        for x in 游标:
            if x[配置.地块要素字段映射.所属街坊字段名称] not in ["", " ", None]:
                if x[配置.地块要素字段映射.地块编号字段名称] in ["", " ", None]:
                    非建设用地编号 += 1
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属街坊字段名称][0:4] + "-" + 字.格式_补位(str(非建设用地编号), 2)  # type: ignore
            elif x[配置.地块要素字段映射.所属分村字段名称] not in ["", " ", None]:
                if x[配置.地块要素字段映射.地块编号字段名称] in ["", " ", None]:
                    非建设用地编号 += 1
                    x[配置.地块要素字段映射.地块编号字段名称] = x[配置.地块要素字段映射.所属分村字段名称][0:4] + "-" + 字.格式_补位(str(非建设用地编号), 2)  # type: ignore
            else:
                是否有非建设用地所属街坊和分村都为空flag = True
                bxarcpy.环境.输出消息(f"ID为{x['_ID']}的非建设用地所属街坊和所属分村都为空，无法生成编号。")
            游标.行更新(x)
    if 是否有非建设用地所属街坊和分村都为空flag:
        raise ValueError("似乎有非建设用地所属街区和所属分村均为空")
    地块要素 = 地块要素.要素创建_通过更新并合并字段(非建设用地要素.名称)

    地块要素 = 地块要素.字段删除(["ORIG_FID", "扣除地类系数", "耕地保有量"])
    输出要素 = 地块要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 计算耕保量(输入要素名称, 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 输出要素名称="in_memory\\AA_计算耕保量"):
    if 输出要素名称 == "in_memory\\AA_计算耕保量":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    用地要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    用地要素.字段删除(["扣除地类系数", 配置.地块要素字段映射.耕地保有量字段名称])

    有扣除地类系数的要素 = bxarcpy.要素类.要素读取_通过名称(有扣除地类系数的要素名称).要素创建_通过复制()
    if "扣除地类系数" not in 有扣除地类系数的要素.字段名称列表获取():
        raise ValueError(f"{有扣除地类系数的要素名称}中未包括 扣除地类系数 字段，建议通过 用地/基期/字段处理并生成分项 来创建带有该字段的要素。")

    仅有耕地的要素 = 用地要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} LIKE '01%'")
    仅有耕地的要素.字段删除(保留字段名称列表=[配置.地块要素字段映射.地类编号字段名称])

    带有扣除系数的耕地要素 = 仅有耕地的要素.要素创建_通过相交([有扣除地类系数的要素名称])
    带有扣除系数的耕地要素.字段删除(保留字段名称列表=["扣除地类系数"])

    合并扣除系数后要素 = 用地要素.要素创建_通过联合([带有扣除系数的耕地要素.名称], 是否保留FID=False)
    合并扣除系数后要素.字段删除(["Shape_Length_1", "Shape_Area_1"])
    合并扣除系数后要素.字段添加(字段名称=配置.地块要素字段映射.耕地保有量字段名称, 字段类型="双精度", 字段长度=10)

    from bxpy.基本对象包 import 字类

    耕地保有量汇总 = 0
    with bxarcpy.游标类.游标创建_通过名称("更新", 合并扣除系数后要素.名称, [配置.地块要素字段映射.地类编号字段名称, "扣除地类系数", "SHAPE@AREA", 配置.地块要素字段映射.耕地保有量字段名称]) as 游标:
        for x in 游标:
            if 字类.匹配正则(x[配置.地块要素字段映射.地类编号字段名称], "^01"):
                耕地保有量 = (1 - x["扣除地类系数"]) * x["SHAPE@AREA"]
                耕地保有量汇总 += 耕地保有量
                x[配置.地块要素字段映射.耕地保有量字段名称] = 耕地保有量
                游标.行更新(x)
    bxarcpy.环境.输出消息(f"耕地保有量总和为：{耕地保有量汇总}")

    仅有耕地的要素 = 合并扣除系数后要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地类编号字段名称} LIKE '01%'")
    仅有耕地的要素 = 仅有耕地的要素.要素创建_通过融合([配置.地块要素字段映射.地块编号字段名称, 配置.地块要素字段映射.地类编号字段名称], [[配置.地块要素字段映射.耕地保有量字段名称, "SUM"]])

    合并扣除系数后要素 = 合并扣除系数后要素.要素创建_通过更新并合并字段(仅有耕地的要素.名称)
    合并扣除系数后要素.字段删除(["扣除地类系数", 配置.地块要素字段映射.耕地保有量字段名称])
    合并扣除系数后要素.字段修改("SUM_" + 配置.地块要素字段映射.耕地保有量字段名称, 配置.地块要素字段映射.耕地保有量字段名称, 配置.地块要素字段映射.耕地保有量字段名称, 清除字段别称=False)

    输出要素 = 合并扣除系数后要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 根据地类编号生成名称(输入要素名称, 地类编号字段名称=配置.地块要素字段映射.地类编号字段名称, 性质名称字段名称=配置.地块要素字段映射.性质名称字段名称, 地块性质别称字段名称=配置.地块要素字段映射.地块性质别称字段名称, 用地构成字段名称=配置.地块要素字段映射.用地大类字段名称, 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_根据地类编号生成名称" + "_" + bxarcpy.工具集.生成短GUID()

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    from bxpy.路径包 import 路径类

    当前文件所在目录 = 路径类.属性获取_目录(__file__)
    转换文件路径 = 路径类.转绝对("..\\", 当前文件所在目录)
    import bxpandas as pd

    a = pd.转换.excel文件转数据框架(转换文件路径 + r"\config\地块_指标测算表.xlsx", 要读取的列=[1, 3, 4, 5, 86], 数据类型={"性质名称": str, "地块性质": str, "地类标准": str, "地块性质别称": str, "用地构成": str})
    基数转换映射表 = pd.转换.数据框架转字典(a)  # type: ignore

    输入要素.字段添加(性质名称字段名称).字段添加(地块性质别称字段名称).字段添加(用地构成字段名称)
    部分地类未找到名称flag = False
    with bxarcpy.游标类.游标创建_通过名称("更新", 输入要素.名称, [地类编号字段名称, 性质名称字段名称, 地块性质别称字段名称, 用地构成字段名称]) as 游标:
        for x in 游标:
            对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["地块性质"] == x[地类编号字段名称] and 基数转换映射表1["地类标准"] == "国空"]
            if 对应的对象列表:
                x[性质名称字段名称] = 对应的对象列表[0]["性质名称"]
                x[地块性质别称字段名称] = 对应的对象列表[0]["地块性质别称"]
                x[用地构成字段名称] = 对应的对象列表[0]["用地构成"]
                游标.行更新(x)
            else:
                bxarcpy.环境.输出消息(f"未找到 {x[地类编号字段名称]} 对应的 性质名称。")
                部分地类未找到名称flag = True
    if 部分地类未找到名称flag:
        raise ValueError("部分地类编号没有找到对应的性质名称，请通过bxgis/config/地块_指标测算表.xlsx添加地类。")
    输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 计算土地码(输入要素名称, 地籍要素名称="CZ_三调筛选_坐落单位名称", 输出要素名称="in_memory\\AA_计算土地码"):
    # 需要保证该编号的地块都已经编号
    if 输出要素名称 == "in_memory\\AA_计算土地码":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

    地块要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    地籍要素 = bxarcpy.要素类.要素读取_通过名称(地籍要素名称).要素创建_通过复制()
    if "坐落单位代码" not in 地籍要素.字段名称列表获取():
        raise ValueError(f"{地籍要素名称}中未包括 坐落单位代码 字段，建议通过 用地/基期/字段处理并生成分项 来创建带有该字段的要素。")
    地块要素.字段添加(配置.地块要素字段映射.土地码字段名称).字段删除(["坐落单位代码"])
    地籍要素.字段删除(保留字段名称列表=["坐落单位代码"])

    有地籍地块要素 = 地块要素.要素创建_通过空间连接(地籍要素.名称, "内点在连接要素内")

    需操作的字段名称列表 = [配置.地块要素字段映射.地块编号字段名称, 配置.地块要素字段映射.地类编号字段名称, 配置.地块要素字段映射.土地码字段名称, "坐落单位代码"]

    地块编号存在空值的要素 = 有地籍地块要素.要素创建_通过筛选(f"{配置.地块要素字段映射.地块编号字段名称} IS NULL")
    if 地块编号存在空值的要素.几何数量 > 0:
        raise ValueError(f"部分地块的地块编号为空，影响土地码生成。")
    with bxarcpy.游标类.游标创建_通过名称("更新", 有地籍地块要素.名称, 需操作的字段名称列表) as 游标_地块:
        for x in 游标_地块:
            地籍代码 = "H00000000"
            主地类编号 = "00000000"
            兼容性质数量 = 1
            街区编号 = "00"
            街坊编号 = "00"
            地块编号 = "000"

            # print(x["地块编号"])
            # print(len(x["地块编号"].split("-")))
            # print(x["地类编号"][0:2])

            if x[配置.地块要素字段映射.地块编号字段名称] not in ["", " ", None] and len(x[配置.地块要素字段映射.地块编号字段名称].split("-")) == 2 and len(x[配置.地块要素字段映射.地块编号字段名称].split("-")[0]) == 8:
                地籍代码 = "H" + x["坐落单位代码"][4:12]
                主地类编号 = x[配置.地块要素字段映射.地类编号字段名称].split("(")[0].split("/")[0].replace("v", "")
                兼容性质数量 = len(x[配置.地块要素字段映射.地类编号字段名称].split("(")[0].split("/"))
                街区编号 = x[配置.地块要素字段映射.地块编号字段名称][4:6]
                街坊编号 = x[配置.地块要素字段映射.地块编号字段名称][6:8]
                地块编号 = 字类.格式_补位(x[配置.地块要素字段映射.地块编号字段名称].split("-")[-1], 3)
                # print(地籍代码 + 主地类编号.ljust(8, "0") + f"X{兼容性质数量}" + 街区编号 + 街坊编号 + 地块编号 + "0")

                土地码 = 地籍代码 + 字类.格式_补位(主地类编号, 8, "后方") + f"X{兼容性质数量}" + 街区编号 + 街坊编号 + 地块编号 + "0"
                x[配置.地块要素字段映射.土地码字段名称] = 土地码

            游标_地块.行更新(x)

    输出要素 = 有地籍地块要素.字段删除(["坐落单位代码"]).要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 计算开发动态(输入要素名称, 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 输出要素名称="in_memory\\AA_计算开发动态"):
    if 输出要素名称 == "in_memory\\AA_计算开发动态":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()
    from bxgis import 配置

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    集建区要素 = bxarcpy.要素类.要素读取_通过名称(城镇集建区要素名称).要素创建_通过复制()
    弹性区要素 = bxarcpy.要素类.要素读取_通过名称(城镇弹性区要素名称).要素创建_通过复制()
    开发边界要素 = 集建区要素.要素创建_通过合并([弹性区要素.名称])
    if 配置.控制线要素字段映射.控制线名称字段名称 not in 开发边界要素.字段名称列表获取():
        raise ValueError(f"{城镇集建区要素名称}和{城镇弹性区要素名称}中未包括 {配置.控制线要素字段映射.控制线名称字段名称} 字段。")
    用地要素 = 常用.计算所属区域.计算所属区域(输入要素名称=输入要素.名称, 区域要素名称=开发边界要素.名称, 字段映射列表=[["所属三线", "控制线名称"]], 计算方式="内点在区域要素内")
    with bxarcpy.游标类.游标创建_通过名称("更新", 用地要素.名称, ["所属三线", 配置.地块要素字段映射.地类编号字段名称, 配置.地块要素字段映射.开发动态字段名称]) as 游标:
        for x in 游标:
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

            游标.行更新(x)
    用地要素.字段删除(["所属三线"])

    输出要素 = 用地要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


def 计算地块内设施规模(输入要素名称="DIST_用地规划图", 设施要素名称="SS_配套设施", 输出要素名称="内存临时"):
    if 输出要素名称 == "内存临时":
        输出要素名称 = "in_memory\\AA_计算地块内设施规模" + "_" + bxarcpy.工具集.生成短GUID()

    if 设施要素名称 is None:
        用地要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
        输出要素 = 用地要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    用地要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    设施要素 = bxarcpy.要素类.要素读取_通过名称(设施要素名称).要素创建_通过复制()

    设施字段名称列表 = 设施要素.字段名称列表获取()
    if 配置.设施要素字段映射.设施名称字段名称 not in 设施字段名称列表 or 配置.设施要素字段映射.设施规模字段名称 not in 设施字段名称列表:
        raise ValueError(f"{输入要素名称}缺少了{配置.设施要素字段映射.设施名称字段名称}或者{配置.设施要素字段映射.设施规模字段名称}字段。")

    用地要素.字段添加(配置.地块要素字段映射.配套设施规模字段名称).字段添加(配置.地块要素字段映射.配套设施规模字段名称 + "2").字段添加(配置.地块要素字段映射.配套设施规模字段名称 + "3")
    使用到了配套设施规模2字段 = False
    使用到了配套设施规模3字段 = False
    with bxarcpy.游标类.游标创建_通过名称("更新", 用地要素.名称, ["_ID", "_形状", 配置.地块要素字段映射.配套设施规模字段名称, 配置.地块要素字段映射.配套设施规模字段名称 + "2", 配置.地块要素字段映射.配套设施规模字段名称 + "3"]) as 用地游标:
        with bxarcpy.游标类.游标创建_通过名称("查询", 设施要素.名称, ["_形状", 配置.设施要素字段映射.设施名称字段名称, 配置.设施要素字段映射.设施规模字段名称]) as 设施游标:
            for 用地x in 用地游标:
                地块设施规模内容 = []
                for 设施x in 设施游标:
                    if bxarcpy.几何对象类.关系_包含(用地x["_形状"], 设施x["_形状"]):
                        设施名称 = 设施x[配置.设施要素字段映射.设施名称字段名称]
                        设施规模 = 设施x[配置.设施要素字段映射.设施规模字段名称]
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
                设施游标.重置()
                地块设施规模内容_字符串形式 = ""
                for x in 地块设施规模内容:
                    if x["设施规模"] not in ["", " ", None]:
                        地块设施规模内容_字符串形式 = 地块设施规模内容_字符串形式 + x["设施名称"] + "-" + x["设施数量"] + "-" + x["设施规模"] + "/"
                    else:
                        地块设施规模内容_字符串形式 = 地块设施规模内容_字符串形式 + x["设施名称"] + "-" + x["设施数量"] + "/"
                地块设施规模内容_字符串形式 = 地块设施规模内容_字符串形式[:-1]
                if len(地块设施规模内容_字符串形式) > 765:
                    raise ValueError(f"ID为{用地x['_ID']}的地块的配套设施规模字符串长度超过了765。")
                elif len(地块设施规模内容_字符串形式) > 510:
                    用地x[配置.地块要素字段映射.配套设施规模字段名称] = 地块设施规模内容_字符串形式[0:255]
                    用地x[配置.地块要素字段映射.配套设施规模字段名称 + "2"] = 地块设施规模内容_字符串形式[255:510]
                    用地x[配置.地块要素字段映射.配套设施规模字段名称 + "3"] = 地块设施规模内容_字符串形式[510:]
                    使用到了配套设施规模2字段 = True
                    使用到了配套设施规模3字段 = True
                elif len(地块设施规模内容_字符串形式) > 255:
                    用地x[配置.地块要素字段映射.配套设施规模字段名称] = 地块设施规模内容_字符串形式[0:255]
                    用地x[配置.地块要素字段映射.配套设施规模字段名称 + "2"] = 地块设施规模内容_字符串形式[255:]
                    使用到了配套设施规模2字段 = True
                else:
                    用地x[配置.地块要素字段映射.配套设施规模字段名称] = 地块设施规模内容_字符串形式
                用地游标.行更新(用地x)
    if 使用到了配套设施规模3字段 == False:
        用地要素.字段删除([配置.地块要素字段映射.配套设施规模字段名称 + "3"])
    if 使用到了配套设施规模2字段 == False:
        用地要素.字段删除([配置.地块要素字段映射.配套设施规模字段名称 + "2"])
    输出要素 = 用地要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地更新(输入要素名称="DIST_用地规划图", 街坊范围线要素名称="JX_街坊范围线", 分村范围线要素名称="JX_分村范围线", 城镇集建区要素名称="KZX_城镇集建区", 城镇弹性区要素名称="KZX_城镇弹性区", 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 有坐落单位信息的要素名称="CZ_三调筛选_坐落单位名称", 设施要素名称="SS_配套设施", 输出要素名称="DIST_用地规划图_更新后")
