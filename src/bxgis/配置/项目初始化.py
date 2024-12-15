# *-* coding:utf8 *-*


def 项目初始化(项目文件夹路径=r"C:\Users\beixiao\Desktop"):
    from bxpy.路径包 import 路径类
    from bxpy.基本对象包 import 字典类, 字类
    from bxpy.日志包 import 日志生成器
    import toml

    项目名称 = 路径类.属性获取_文件名(项目文件夹路径)
    子路径列表 = 路径类.子路径(项目文件夹路径)

    是否已存在数据库 = False
    if len(子路径列表[1]) > 0:
        for 文件夹名称x in 子路径列表[1]:
            if 文件夹名称x[-4:] == ".gdb" and "临时" not in 文件夹名称x and "Default" not in 文件夹名称x:
                数据库路径 = 路径类.连接(项目文件夹路径, 文件夹名称x)
                是否已存在数据库 = True
                break
    if not 是否已存在数据库:
        from bxarcpy.数据库包 import 数据库类

        数据库路径 = 数据库类.数据库创建(项目文件夹路径, f"{项目名称}_数据库.gdb")
        日志生成器.输出控制台(f"未在 项目根目录 找到数据库，因此自动创建了数据库：{数据库路径}")

    toml文件路径 = 路径类.连接(项目文件夹路径, ".bxgis", "项目信息.toml")
    if not 路径类.是否存在(toml文件路径):
        项目信息 = {"项目基本信息": {"工作空间": 数据库路径, "项目目录": 项目文件夹路径}}
        路径类.新增文件(toml文件路径)
        with open(toml文件路径, "w", encoding="utf-8") as f:
            toml.dump(项目信息, f)
        日志生成器.输出控制台(f"未在 项目根目录/.bxgis 找到 项目信息.toml，因此自动创建了该文件")
    with open(toml文件路径, "r", encoding="utf-8") as f:
        当前项目配置 = toml.load(f)

    默认项目信息文件路径 = 路径类.连接(路径类.属性获取_目录(__file__), "项目信息_默认.toml")
    with open(默认项目信息文件路径, "r", encoding="utf-8") as f:
        默认配置 = toml.load(f)

    最终配置 = 字典类.解包合并(默认配置, 当前项目配置)
    日志生成器.输出控制台(f"最终配置为：{字类.转换_到字(最终配置,json缩进=2)}", 内容长度=20000)

    当前项目信息文件路径 = 路径类.连接(路径类.属性获取_目录(__file__), "项目信息.toml")
    with open(toml文件路径, "w", encoding="utf-8") as f:
        toml.dump(最终配置, f)
    with open(当前项目信息文件路径, "w", encoding="utf-8") as f:
        toml.dump(最终配置, f)
    日志生成器.输出控制台(f"可通过修改 {toml文件路径} 中内容来进一步完善配置")


if __name__ == "__main__":
    项目初始化(r"C:\Users\common\Project\J江东区临江控规")
