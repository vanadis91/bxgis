# *-* coding:utf8 *-*
class 配置类:
    @staticmethod
    def 获取工作空间():
        import toml
        from bxpy.路径包 import 路径类

        toml文件 = 路径类.连接(路径类.属性获取_目录(__file__), "项目信息.toml")
        with open(toml文件, "r", encoding="utf-8") as f:
            配置文件 = toml.load(f)
        return 配置文件["项目基本信息"]["工作空间"]
