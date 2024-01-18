def 生成当前时间():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")


def 生成当前时间_微秒():
    import datetime

    return datetime.datetime.now().strftime(r"%Y%m%d%H%M%f")


def 生成SUUID():
    from bxpy import 字

    return 字.字符串生成_SUUID()
