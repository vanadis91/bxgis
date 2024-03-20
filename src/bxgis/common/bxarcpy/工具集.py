def 生成当前时间():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")


def 生成当前时间_微秒():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%f")


def 生成短GUID():
    from bxpy.基本对象包 import 字类

    return 字类.字符串生成_短GUID()
