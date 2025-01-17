# *-* coding:utf8 *-*
class 配置类:
    @staticmethod
    def 获取工作空间():
        from bxpy.路径包 import 路径类
        from bxpy.基本对象包 import 字典类

        配置文件 = 字典类.转换_从文件(路径类.连接(路径类.属性获取_目录(__file__), "项目信息.yml"))

        return 配置文件["项目基本信息"]["工作空间"]
