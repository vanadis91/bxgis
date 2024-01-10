import bxarcpy


def 用地创建_通过计算所属区域(输入要素名称, 区域要素名称="JX_街区范围线", 字段映射列表=[["所属街区", "街区编号"]], 输出要素名称="in_memory\\AA_计算所属区域"):
    if 输出要素名称 == "in_memory\\AA_计算所属区域":
        输出要素名称 = 输出要素名称 + "_" + bxarcpy.常量.当前时间()
    输入要素 = bxarcpy.要素类.要素读取_通过名称(输入要素名称).要素创建_通过复制()
    赋值后要素 = 输入要素.要素创建_通过联合并赋值字段(区域要素名称, 字段映射列表)
    输出要素 = 赋值后要素.要素创建_通过复制并重命名重名要素(输出要素名称, 重名要素后缀="计算所属区域前")
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        用地创建_通过计算所属区域("DIST_用地规划图", 区域要素名称="JX_街区范围线", 字段映射列表=[["所属街区", "街区编号"]], 输出要素名称="in_memory\\AA_计算所属区域")
