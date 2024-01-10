import bxarcpy


def 用地创建_通过计算用地构成(输入要素名称, 输出要素名称="in_memory\\AA_计算用地构成"):
    if 输出要素名称 == "in_memory\\AA_计算用地构成":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.常量.当前时间()
    from bxpandas import 类 as pd

    a = pd.转换.excel转数据框架(r"C:\Users\beixiao\AppConfig\Bxcad\Config\设计配置\设计参数\地块_指标测算表.xlsx", 要读取的列=(3, 4, 86), 列数据类型={"地块性质": str, "地类标准": str, "用地构成": str})
    用地构成映射表 = pd.转换.数据框架转json(a)  # type: ignore

    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    输入要素.字段添加("用地构成")
    with bxarcpy.游标类.游标创建_通过名称("更新", 输入要素.名称, ["地类编号", "用地构成"]) as 游标:
        for x in 游标:
            对应的对象列表 = [用地构成映射表1 for 用地构成映射表1 in 用地构成映射表 if 用地构成映射表1["地块性质"] == x["地类编号"] and 用地构成映射表1["地类标准"] == "国空"]
            if 对应的对象列表:
                x["用地构成"] = 对应的对象列表[0]["用地构成"]
                游标.行更新(x)
            else:
                print(f"未找到该 地类编号 对应的 用地构成：{x['地类编号']}")
    输出要素 = 输入要素.要素创建_通过复制并重命名重名要素(输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地创建_通过计算用地构成("DIST_用地规划图", 输出要素名称="in_memory\\AA_计算用地构成")
