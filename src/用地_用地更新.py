import bxarcpy
from bxpy import 字
import 配置
from typing import Union, Literal


class 用地类:
    @staticmethod
    def 用地创建_通过融合部分地类(输入要素名称, 输出要素名称="in_memory\\AA_融合部分地类"):
        # 需要保证所有地块都具有所属街区和所属街坊两个字段并赋值
        if 输出要素名称 == "in_memory\\AA_融合部分地类":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        地类编号字段名称 = 配置.地块要素字段映射.地类编号字段名称

        输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

        # 公路编号
        公路要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '1202%'")
        公路要素 = 公路要素.要素创建_通过融合([地类编号字段名称])
        输入要素 = 输入要素.要素创建_通过更新并合并字段(公路要素.名称)

        # 道路编号
        道路要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '1207%'")
        道路要素 = 道路要素.要素创建_通过融合([地类编号字段名称])
        输入要素 = 输入要素.要素创建_通过更新并合并字段(道路要素.名称)

        # 非建设用地编号
        非建设用地要素 = 输入要素.要素创建_通过筛选(f"{地类编号字段名称} LIKE '01%' Or {地类编号字段名称} LIKE '02%' Or {地类编号字段名称} LIKE '03%' Or {地类编号字段名称} LIKE '04%' Or {地类编号字段名称} LIKE '05%' Or {地类编号字段名称} LIKE '06%' Or {地类编号字段名称} LIKE '17%'")
        非建设用地要素 = 非建设用地要素.要素创建_通过融合([地类编号字段名称])
        输入要素 = 输入要素.要素创建_通过更新并合并字段(非建设用地要素.名称)

        # 输出
        输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    @staticmethod
    def 用地创建_通过计算所属区域(输入要素名称, 区域要素名称="JX_街区范围线", 字段映射列表=[["所属街区", "街区编号"]], 计算方式: Literal["分割输入要素", "按输入要素内点"] = "分割输入要素", 输出要素名称="in_memory\\AA_计算所属区域"):
        if 输出要素名称 == "in_memory\\AA_计算所属区域":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
        区域要素 = bxarcpy.要素类.要素读取_通过名称(区域要素名称).要素创建_通过复制()

        需要添加的字段列表 = [x[0] for x in 字段映射列表]
        for x in 需要添加的字段列表:
            输入要素.字段添加(x)

        if 计算方式 == "分割输入要素":
            赋值后要素 = 输入要素.要素创建_通过联合并赋值字段(区域要素.名称, 字段映射列表)

            输出要素 = 赋值后要素.要素创建_通过复制并重命名重名要素(输出要素名称, 重名要素后缀="计算所属区域前")

        elif 计算方式 == "按输入要素内点":
            区域要素保留字段列表 = [x[1] for x in 字段映射列表]
            区域要素.字段删除(保留字段名称列表=区域要素保留字段列表)

            赋值后要素 = 输入要素.要素创建_通过空间连接(区域要素.名称, "内点在连接要素内")
            for x in 字段映射列表:
                赋值后要素.字段计算(x[0], f"!{x[1]}!")

            赋值后要素.字段删除([x[1] for x in 字段映射列表])

            输出要素 = 赋值后要素.要素创建_通过复制并重命名重名要素(输出要素名称)

        return 输出要素

    @staticmethod
    def 用地创建_通过所属街坊生成所属街区(输入要素名称, 输出要素名称="in_memory\\AA_根据所属街坊生成所属街区"):
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

    @staticmethod
    def 用地创建_通过计算地块编号(输入要素名称, 输出要素名称="in_memory\\AA_计算地块编号"):
        # 需要保证所有地块都具有所属街区和所属街坊两个字段并赋值
        if 输出要素名称 == "in_memory\\AA_计算地块编号":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        地块要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

        需操作的字段名称列表 = ["地类编号", "地块编号"]
        地块编号最大值字典 = {}
        with bxarcpy.游标类.游标创建_通过名称("查找", 地块要素.名称, 需操作的字段名称列表) as 游标:
            for x in 游标:
                if x["地块编号"] not in ["", " ", None] and x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"]:
                    地块编号序号 = int(x["地块编号"].split("-")[-1])
                    地块所属街坊 = x["地块编号"].split("-")[0]
                    if 地块所属街坊 in 地块编号最大值字典:
                        地块编号最大值字典[地块所属街坊] = max(地块编号最大值字典[地块所属街坊], 地块编号序号)
                    else:
                        地块编号最大值字典[地块所属街坊] = 地块编号序号

        print(f"地块编号最大值字典：{地块编号最大值字典}")

        # 公路编号
        公路要素 = 地块要素.要素创建_通过筛选("地类编号 LIKE '1202%'")
        公路要素 = 公路要素.要素创建_通过融合(["地类编号", "所属街坊", "所属街区"])
        公路要素.字段添加("地块编号")
        需操作的字段名称列表 = ["地块编号", "所属街坊"]
        with bxarcpy.游标类.游标创建_通过名称("更新", 公路要素.名称, 需操作的字段名称列表) as 游标:
            for x in 游标:
                地块编号最大值字典[x["所属街坊"]] += 1

                x["地块编号"] = x["所属街坊"] + "-" + 字.格式_补位(str(地块编号最大值字典[x["所属街坊"]]), 2)

                游标.行更新(x)
        地块要素 = 地块要素.要素创建_通过更新并合并字段(公路要素.名称)

        # 道路编号
        道路要素 = 地块要素.要素创建_通过筛选("地类编号 LIKE '1207%'")
        道路要素 = 道路要素.要素创建_通过融合(["地类编号", "所属街坊", "所属街区"], 是否单部件=False)
        道路要素.字段添加("地块编号")
        需操作的字段名称列表 = ["地类编号", "地块编号", "所属街坊"]
        with bxarcpy.游标类.游标创建_通过名称("更新", 道路要素.名称, 需操作的字段名称列表) as 游标:
            for x in 游标:
                if x["地类编号"] == "1207":
                    x["地块编号"] = x["所属街坊"] + "-" + "SS1"
                elif x["地类编号"] == "1207v":
                    x["地块编号"] = x["所属街坊"] + "-" + "XS1"

                游标.行更新(x)
        地块要素 = 地块要素.要素创建_通过更新并合并字段(道路要素.名称)

        # 非建设用地编号
        非建设用地要素 = 地块要素.要素创建_通过筛选("地类编号 LIKE '01%' Or 地类编号 LIKE '02%' Or 地类编号 LIKE '03%' Or 地类编号 LIKE '04%' Or 地类编号 LIKE '05%' Or 地类编号 LIKE '06%' Or 地类编号 LIKE '17%'")
        非建设用地要素 = 非建设用地要素.要素创建_通过融合(["地类编号"])
        非建设用地要素.字段添加("地块编号")
        需操作的字段名称列表 = ["地块编号"]
        非建设用地编号 = 0
        with bxarcpy.游标类.游标创建_通过名称("更新", 非建设用地要素.名称, 需操作的字段名称列表) as 游标:
            for x in 游标:
                非建设用地编号 += 1
                x["地块编号"] = "QT12" + "-" + 字.格式_补位(str(非建设用地编号), 2)  # type: ignore

                游标.行更新(x)
        地块要素 = 地块要素.要素创建_通过更新并合并字段(非建设用地要素.名称)

        地块要素 = 地块要素.字段删除(["ORIG_FID", "扣除地类系数", "耕地保有量"])
        输出要素 = 地块要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    @staticmethod
    def 用地创建_通过计算耕保量(输入要素名称, 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 输出要素名称="in_memory\\AA_计算耕保量"):
        if 输出要素名称 == "in_memory\\AA_计算耕保量":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        用地要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
        用地要素.字段删除(["扣除地类系数", "耕地保有量"])

        仅有耕地的要素 = 用地要素.要素创建_通过筛选("地类编号 LIKE '01%'")
        仅有耕地的要素.字段删除(保留字段名称列表=["地类编号"])

        带有扣除系数的耕地要素 = 仅有耕地的要素.要素创建_通过相交([有扣除地类系数的要素名称])
        带有扣除系数的耕地要素.字段删除(保留字段名称列表=["扣除地类系数"])

        合并扣除系数后要素 = 用地要素.要素创建_通过联合([带有扣除系数的耕地要素.名称], 是否保留FID=False)
        合并扣除系数后要素.字段删除(["Shape_Length_1", "Shape_Area_1", "耕地保有量"])
        合并扣除系数后要素.字段添加(字段名称="耕地保有量", 字段类型="双精度", 字段长度=10)

        from bxpy import 字

        耕地保有量汇总 = 0
        with bxarcpy.游标类.游标创建_通过名称("更新", 合并扣除系数后要素.名称, ["地类编号", "扣除地类系数", "SHAPE@AREA", "耕地保有量"]) as 游标:
            for x in 游标:
                if 字.匹配正则(x["地类编号"], "^01"):
                    耕地保有量 = (1 - x["扣除地类系数"]) * x["SHAPE@AREA"]
                    耕地保有量汇总 += 耕地保有量
                    x["耕地保有量"] = 耕地保有量
                    游标.行更新(x)
        bxarcpy.环境.输出消息(f"耕地保有量总和为：{耕地保有量汇总}")

        仅有耕地的要素 = 合并扣除系数后要素.要素创建_通过筛选("地类编号 LIKE '01%'")
        仅有耕地的要素 = 仅有耕地的要素.要素创建_通过融合(["地块编号", "地类编号"], [["耕地保有量", "SUM"]])

        合并扣除系数后要素 = 合并扣除系数后要素.要素创建_通过更新并合并字段(仅有耕地的要素.名称)
        合并扣除系数后要素.字段删除(["扣除地类系数", "耕地保有量"])
        合并扣除系数后要素.字段修改("SUM_耕地保有量", "耕地保有量", "耕地保有量", 清除字段别称=False)

        输出要素 = 合并扣除系数后要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    @staticmethod
    def 用地创建_通过根据地类编号生成名称(输入要素名称, 地类编号字段名称="地类编号", 性质名称字段名称="性质名称", 地块性质别称字段名称="地块性质别称", 用地构成字段名称="用地构成", 输出要素名称="in_memory\\AA_根据地类编号生成名称"):
        if 输出要素名称 == "in_memory\\AA_根据地类编号生成名称":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

        import bxpandas as pd

        a = pd.转换.excel文件转数据框架(r"C:\Users\beixiao\AppConfig\Bxcad\Config\设计配置\设计参数\地块_指标测算表.xlsx", 要读取的列=[1, 3, 4, 5, 86], 数据类型={"性质名称": str, "地块性质": str, "地类标准": str, "地块性质别称": str, "用地构成": str})
        基数转换映射表 = pd.转换.数据框架转字典(a)  # type: ignore

        输入要素.字段添加(性质名称字段名称).字段添加(地块性质别称字段名称).字段添加(用地构成字段名称)
        with bxarcpy.游标类.游标创建_通过名称("更新", 输入要素.名称, [地类编号字段名称, 性质名称字段名称, 地块性质别称字段名称, 用地构成字段名称]) as 游标:
            for x in 游标:
                对应的对象列表 = [基数转换映射表1 for 基数转换映射表1 in 基数转换映射表 if 基数转换映射表1["地块性质"] == x[地类编号字段名称] and 基数转换映射表1["地类标准"] == "国空"]
                if 对应的对象列表:
                    x[性质名称字段名称] = 对应的对象列表[0]["性质名称"]
                    x[地块性质别称字段名称] = 对应的对象列表[0]["地块性质别称"]
                    x[用地构成字段名称] = 对应的对象列表[0]["用地构成"]
                    游标.行更新(x)
                else:
                    print(f"未找到该 地类编号 对应的 名称：{x[地类编号字段名称]}")

        输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    @staticmethod
    def 用地创建_通过计算土地码(输入要素名称, 地籍要素名称="CZ_三调筛选_坐落单位名称", 输出要素名称="in_memory\\AA_计算土地码"):
        # 需要保证该编号的地块都已经编号
        if 输出要素名称 == "in_memory\\AA_计算土地码":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        地块要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
        地籍要素 = bxarcpy.要素类.要素读取_通过名称(地籍要素名称).要素创建_通过复制()

        地块要素.字段添加("土地码")
        地籍要素.字段删除(保留字段名称列表=["坐落单位代码"])

        有地籍地块要素 = 地块要素.要素创建_通过空间连接(地籍要素.名称, "内点在连接要素内")

        需操作的字段名称列表 = ["地块编号", "地类编号", "土地码", "坐落单位代码"]
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

                if x["地块编号"] not in ["", " ", None] and len(x["地块编号"].split("-")) == 2 and x["地类编号"][0:2] not in ["01", "02", "03", "04", "05", "06", "17"]:
                    地籍代码 = "H" + x["坐落单位代码"][4:12]
                    主地类编号 = x["地类编号"].split("(")[0].split("/")[0].replace("v", "")
                    兼容性质数量 = len(x["地类编号"].split("(")[0].split("/"))
                    街区编号 = x["地块编号"][4:6]
                    街坊编号 = x["地块编号"][6:8]
                    地块编号 = 字.格式_补位(x["地块编号"].split("-")[-1], 3)
                    # print(地籍代码 + 主地类编号.ljust(8, "0") + f"X{兼容性质数量}" + 街区编号 + 街坊编号 + 地块编号 + "0")

                    土地码 = 地籍代码 + 字.格式_补位(主地类编号, 8, "后方") + f"X{兼容性质数量}" + 街区编号 + 街坊编号 + 地块编号 + "0"
                    x["土地码"] = 土地码

                游标_地块.行更新(x)

        输出要素 = 有地籍地块要素.字段删除(["坐落单位代码"]).要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素

    @staticmethod
    def 用地创建_通过计算开发动态(输入要素名称, 输出要素名称="in_memory\\AA_计算开发动态"):
        if 输出要素名称 == "in_memory\\AA_计算开发动态":
            输出要素名称 = 输出要素名称 + "_" + bxarcpy.工具集.生成短GUID()

        输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

        用地要素 = 用地类.用地创建_通过计算所属区域(输入要素.名称, 区域要素名称="KZX_城镇开发边界", 字段映射列表=[["所属三线", "控制线名称"]], 计算方式="按输入要素内点")
        with bxarcpy.游标类.游标创建_通过名称("更新", 用地要素.名称, ["所属三线", "地类编号", "开发动态"]) as 游标:
            for x in 游标:
                if x["所属三线"] not in ["", " ", None]:
                    x["所属三线"] = "开发边界内"

                if x["开发动态"] in ["现状已实施", "现状保留", "保留"]:
                    x["开发动态"] = "保留"
                elif x["开发动态"] in ["改/扩建", "改扩建"] and x["所属三线"] == "开发边界内":
                    x["开发动态"] = "改/扩建"
                elif x["开发动态"] in ["盘活"] and x["所属三线"] != "开发边界内":
                    x["开发动态"] = "盘活"
                elif x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"] and x["所属三线"] == "开发边界内":
                    x["开发动态"] = "新建"
                elif x["地类编号"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] and x["地类编号"][0:4] not in ["1207", "1202"] and x["所属三线"] != "开发边界内":
                    x["开发动态"] = "新增"

                游标.行更新(x)

        输出要素 = 用地要素.要素创建_通过复制并重命名重名要素(输出要素名称)
        return 输出要素


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地要素 = 用地类.用地创建_通过融合部分地类("DIST_用地规划图")
        用地要素 = 用地类.用地创建_通过计算所属区域(用地要素.名称, 区域要素名称="JX_街坊范围线", 字段映射列表=[["所属街坊", "区域编号"]], 计算方式="分割输入要素")
        用地要素 = 用地类.用地创建_通过所属街坊生成所属街区(用地要素.名称)
        用地要素 = 用地类.用地创建_通过计算地块编号(用地要素.名称)
        用地要素 = 用地类.用地创建_通过计算耕保量(用地要素.名称)
        用地要素 = 用地类.用地创建_通过根据地类编号生成名称(用地要素.名称)
        用地要素 = 用地类.用地创建_通过计算土地码(用地要素.名称)
        用地要素 = 用地类.用地创建_通过计算开发动态(用地要素.名称)
