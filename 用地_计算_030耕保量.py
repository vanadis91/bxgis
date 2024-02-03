import bxarcpy


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


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地创建_通过计算耕保量("DIST_用地规划图_街坊街区_编号", 有扣除地类系数的要素名称="CZ_三调筛选_扣除地类系数", 输出要素名称="DIST_用地规划图_街坊街区_编号_耕保")
