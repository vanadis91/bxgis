# *-* coding:utf8 *-*
def 用地合规性检查(
    用地要素路径,
    检查字段是否存在缺失=True,
    检查字段类型是否正确=True,
    检查地类编号是否存在空值=True,
    输出要素路径="内存临时",
):
    import bxarcpy.工具包 as 工具包
    from bxarcpy.要素包 import 要素类, 字段类
    from bxgis.配置.配置包 import 配置类

    基本信息 = 配置类.项目信息对象获取()
    from bxarcpy.环境包 import 环境管理器类, 输入输出类

    输出要素路径 = 工具包.输出路径生成_当采用内存临时时(["用地更新"]) if 输出要素路径 == "内存临时" else 输出要素路径
    用地要素名称 = 要素类.属性获取_要素名称(用地要素路径)
    用地要素 = 要素类.要素创建_通过复制(用地要素路径)

    if 检查字段是否存在缺失:
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
        部分字段不存在flag = False
        for 字段x in 需要存在的字段名称列表:
            if 字段x not in 字段名称列表:
                输入输出类.输出消息(f"【{用地要素名称}】中缺少【{字段x}】字段，已新建该字段")
                要素类.字段添加(用地要素, 字段x)
                部分字段不存在flag = True
        # if 部分字段不存在flag:
        #     raise Exception(f"【{用地要素名称}】中缺少部分必须要存在的字段。")
        要素类.字段排序(用地要素, [基本信息.地块要素字段映射.地类编号字段名称])

    if 检查字段类型是否正确:
        # 检查字段的数据类型是否正确
        from bxpy.基本对象包 import 字典类
        from bxpy.路径包 import 路径类
        from bxgis.配置.配置包 import 配置类

        基本信息 = 配置类.项目信息对象获取()

        地块属性表 = 基本信息.应用信息.地块属性表获取()
        字段类型不准确flag = False
        字段列表 = 要素类.字段列表获取(用地要素)
        for 字段x in 字段列表:
            指定的地块属性表列表 = [地块属性表x for 地块属性表x in 地块属性表 if 字段类.属性获取_名称(字段x) == 地块属性表x["属性名称"]]
            if 字段类.属性获取_名称(字段x).upper() in ["OBJECTID", "SHAPE", "SHAPE_LENGTH", "SHAPE_AREA"]:
                continue
            if len(指定的地块属性表列表) == 0:
                输入输出类.输出消息(f"未在地块属性表中找到{字段类.属性获取_名称(字段x)}的定义")
                continue
            指定的地块属性表 = 指定的地块属性表列表[0]
            if 字段类.属性获取_类型(字段x) != 指定的地块属性表["字段类型"] and not (字段类.属性获取_类型(字段x) == "定长字符串" and 指定的地块属性表["字段类型"] == "字符串"):
                字段类型不准确flag = True
                输入输出类.输出消息(f"{用地要素名称}的{字段类.属性获取_名称(字段x)}字段类型与配置文件不一致，请修改为{指定的地块属性表['字段类型']}")
        if 字段类型不准确flag:
            raise Exception(f"部分字段的类型不准确。")

    if 检查地类编号是否存在空值:
        # 检查地类编号是否存在空值
        地类编号存在空值的要素 = 要素类.要素创建_通过筛选(用地要素, f"{基本信息.地块要素字段映射.地类编号字段名称} IS NULL OR {基本信息.地块要素字段映射.地类编号字段名称} = ''")
        if 要素类.属性获取_几何数量(地类编号存在空值的要素) > 0:
            输入输出类.输出消息(f"{用地要素路径}部分地块的地类编号为空")
            raise Exception(f"{用地要素路径}部分地块的地类编号为空")

    输出要素路径 = 要素类.要素创建_通过复制并重命名重名要素(用地要素, 输出要素路径)
    return 输出要素路径


if __name__ == "__main__":
    from bxarcpy.环境包 import 输入输出类, 环境管理器类

    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    # 工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        用地合规性检查(用地要素路径="DIST_用地规划图", 输出要素路径="DIST_用地规划图")
