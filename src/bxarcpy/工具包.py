def 生成当前时间():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")


def 生成当前时间_微秒():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%f")


def 生成短GUID():
    from bxpy.基本对象包 import 字类

    return 字类.字符串生成_短GUID()


def 输出路径生成_当采用内存临时时(输入要素路径列表):
    from bxpy.基本对象包 import 字类
    from bxpy.路径包 import 路径类

    要素名称列表 = [路径类.属性获取_文件名(路径类.规范化(x)) for x in 输入要素路径列表]
    要素名称 = "_".join(要素名称列表)

    要素名称列表 = 要素名称.split("_")
    要素名称列表 = [x for x in 要素名称列表 if not 字类.匹配正则(x, r"^[A-Za-z0-9]{10}$") and not 字类.匹配正则(x, r"^[A-Za-z0-9]{22}$") and x.upper() not in ["AA", "KZX", "DIST", "YD", "GZW", "CZ", "AC", "DL", "JX", "SS", "TK", "YT"]]
    要素名称 = "_".join(要素名称列表)
    if len(要素名称) > 15:
        要素名称 = 要素名称[0:15]
    输出要素路径 = "in_memory\\AA_" + 要素名称 + "_" + 生成短GUID()
    return 输出要素路径
