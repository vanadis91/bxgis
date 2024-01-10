import bxarcpy


def 设施_移动至正确位置(输入要素名称):
    设施要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()

    需操作的字段名称列表 = ["SHAPE@XY", "设施坐标"]
    with bxarcpy.游标类.游标创建_通过名称("更新", 设施要素.名称, 需操作的字段名称列表) as 游标:
        for x in 游标:
            import re

            设施坐标 = re.split(r"[()\s]", x["设施坐标"])
            x["SHAPE@XY"] = (float(设施坐标[1]), float(设施坐标[2]))

            游标.行更新(x)
    设施要素 = 设施要素.要素创建_通过复制并重命名重名要素(输入要素名称)
    return 设施要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        设施_移动至正确位置("SS_配套设施")
