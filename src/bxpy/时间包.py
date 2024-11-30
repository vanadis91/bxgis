import time
import datetime

# __all__ = ["时间", "时间间隔"]


class 时间格式化映射:
    年 = r"%y"  # %y	去掉世纪的年份（00 - 99）
    年完整 = r"%Y"  # %Y	完整的年份
    月 = r"%m"  # %m	显示月份
    月名称 = r"%b"  # %b	显示简化月份名称
    月名称完整 = r"%B"  # %B	显示完整月份名称
    周年序号 = r"%U"  # %U	一年中的星期数 %W	和%U基本相同
    日 = r"%d"  # %d	显示当月第几天
    日年序号 = r"%j"  # %j	显示当年第几天
    日周序号 = r"%w"  # %w	显示在星期中的第几天，默认从0开始表示周一
    日星期名称 = r"%a"  # %a	显示简化星期名称
    日星期名称完整 = r"%A"  # %A	显示完整星期名称
    时 = r"%H"  # %H	按24小时制显示小时
    时12小时制 = r"%I"  # %I	按12小时制显示小时
    时上下午符号 = r"%p"  # %p	本地am或者pm的相应符
    分 = r"%M"  # %M	显示分钟数
    秒 = r"%S"  # %S	显示秒数
    微秒 = r"%f"
    时差 = r"%z"  # %z	时区的名字（如果不存在为空字符）

    # %c	本地相应的日期和时间表示
    # %x	本地相应日期
    # %X	本地相应时间
    # %%	‘%’字符


class 时间间隔类:
    @staticmethod
    def 时间间隔创建(日=0, 时=0, 分=0, 秒=0, 毫秒=0, 微秒=0, 星期=0):
        return datetime.timedelta(days=日, seconds=秒, microseconds=毫秒, milliseconds=微秒, minutes=分, hours=时, weeks=星期)

    @staticmethod
    def 属性获取_总秒数(时间间隔: datetime.timedelta):
        return 时间间隔.total_seconds()


class 时间类:
    @staticmethod
    def 时间创建_通过年月日(年, 月, 日, 时=0, 分=0, 秒=0, 微秒=0):
        return datetime.datetime(年, 月, 日, 时, 分, 秒, 微秒)

    @staticmethod
    def 时间创建_通过时间戳(时间戳):
        return datetime.datetime.fromtimestamp(时间戳)

    @staticmethod
    def 时间创建_通过时间戳_毫秒为整数(时间戳):
        return datetime.datetime.fromtimestamp(int(时间戳 / 1000))

    @staticmethod
    def 时间创建_通过格式化字符串(格式化字符串="2022-11-26 07:55:55", 字符串格式=rf"{时间格式化映射.年完整}-{时间格式化映射.月}-{时间格式化映射.日} {时间格式化映射.时}:{时间格式化映射.分}:{时间格式化映射.秒}"):
        return datetime.datetime.strptime(格式化字符串, 字符串格式)

    @staticmethod
    def 时间创建_当前(是否带时区信息=True):
        if 是否带时区信息:
            # 是否带时区信息 = datetime.timezone(datetime.timedelta(hours=0))
            时区 = datetime.datetime.now().astimezone().tzinfo
        return datetime.datetime.now(时区)

    @staticmethod
    def 时间合并_静态(*值):
        return datetime.datetime.combine(*值)

    @staticmethod
    def 时间替换(时间对象: datetime.datetime, 年=None, 月=None, 日=None, 时=None, 分=None, 秒=None, 微秒=None):
        return 时间对象.replace(year=年, month=月, day=日, hour=时, minute=分, second=秒, microsecond=微秒)  # type: ignore

    @staticmethod
    def 等待(秒):
        return time.sleep(秒)

    @staticmethod
    def 属性获取_年(时间对象: datetime.datetime):
        return 时间对象.year

    @staticmethod
    def 属性获取_月(时间对象: datetime.datetime):
        return 时间对象.month

    @staticmethod
    def 属性获取_日(时间对象: datetime.datetime):
        return 时间对象.day

    @staticmethod
    def 属性获取_时(时间对象: datetime.datetime):
        return 时间对象.hour

    @staticmethod
    def 属性获取_分(时间对象: datetime.datetime):
        return 时间对象.minute

    @staticmethod
    def 属性获取_秒(时间对象: datetime.datetime):
        return 时间对象.second

    @staticmethod
    def 属性获取_微秒(时间对象: datetime.datetime):
        return 时间对象.microsecond

    @staticmethod
    def 属性获取_星期_周一为0(时间对象: datetime.datetime):
        return 时间对象.weekday()

    @staticmethod
    def 属性获取_星期_周一为1(时间对象: datetime.datetime):
        return 时间对象.isoweekday()

    @staticmethod
    def 属性获取_年月日(时间对象: datetime.datetime):
        return datetime.datetime.isocalendar(时间对象)

    @staticmethod
    def 属性获取_本地时区(时间对象: datetime.datetime):
        return 时间对象.astimezone().tzinfo

    @staticmethod
    def 属性获取_时差(时间对象: datetime.datetime):
        return 时间对象.utcoffset()

    @staticmethod
    def 属性设置_时差(时间对象: datetime.datetime, 小时=8):
        时差 = datetime.timezone(datetime.timedelta(hours=小时))
        return 时间对象.astimezone(时差)

    @staticmethod
    def 转换_到时间戳_毫秒为整数(时间对象: datetime.datetime):
        """
        :test:
        >>> a = 时间().表达_通过时间戳()
        >>> print(a > 16000)
        True
        """
        # time库通过time.mktime(结构化时间)
        return int(时间对象.timestamp() * 1000)

    @staticmethod
    def 转换_到时间戳(时间对象: datetime.datetime):
        """
        :test:
        >>> a = 时间().表达_通过时间戳()
        >>> print(a > 16000)
        True
        """
        # time库通过time.mktime(结构化时间)
        # return time.mktime(self.内嵌对象.timetuple())
        return 时间对象.timestamp()

    @staticmethod
    def 转到_到时间戳_14位(时间对象: datetime.datetime) -> int:
        # time库通过time.mktime(结构化时间)
        # return time.mktime(self.内嵌对象.timetuple())
        """
        :test:
        >>> a = 时间().表达_通过时间戳_14位()
        >>> print(str(a)[0:4])
        2024
        """
        ret = 时间类.转换_到格式化字符串(时间对象, rf"{时间格式化映射.年完整}{时间格式化映射.月}{时间格式化映射.日}{时间格式化映射.时}{时间格式化映射.分}{时间格式化映射.秒}")
        return int(ret)

    @staticmethod
    def 转换_到ISO公历序数(时间对象: datetime.datetime):
        return 时间对象.toordinal()

    @staticmethod
    def 转换_到结构化对象(时间对象: datetime.datetime):
        # time库通过time.localtime(时间戳)
        return 时间对象.timetuple()

    @staticmethod
    def 转换_到格式化字符串(时间对象: datetime.datetime, 格式化字符串=rf"{时间格式化映射.年完整}-{时间格式化映射.月}-{时间格式化映射.日} {时间格式化映射.时}:{时间格式化映射.分}:{时间格式化映射.秒}"):
        """
        >>> a = 时间().表达_通过格式化字符串(r"%年完整%-%月%-%日% %时%:%分%:%秒%")
        >>> print(a[4:5])
        -
        """
        # time库通过time.strftime(格式化字符串, 结构化时间)
        return 时间对象.strftime(格式化字符串)

    @staticmethod
    def 装饰器_运行时长(func):
        def 运行时长(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            runtime = end_time - start_time
            print(f"函数【{func.__name__}】运行时间为{runtime}秒。")
            return result

        return 运行时长

    @staticmethod
    def 系统时间修改(修改后时间字符串="2024-12-12 12:12:12"):
        from bxpy.进程包 import 子进程类

        年月日 = 修改后时间字符串.strip().split(" ")[0]
        时分秒 = 修改后时间字符串.strip().split(" ")[1]
        暂停WindowsTime服务子进程 = 子进程类.子进程创建("net stop w32time")
        子进程类.等待_阻塞(暂停WindowsTime服务子进程)
        修改日期子进程 = 子进程类.子进程创建(f"date {年月日}")
        子进程类.等待_阻塞(修改日期子进程)
        修改时间子进程 = 子进程类.子进程创建(f"time {时分秒}")
        子进程类.等待_阻塞(修改时间子进程)

    @staticmethod
    def 系统时间重置():
        from bxpy.进程包 import 子进程类

        启动WindowsTime服务子进程 = 子进程类.子进程创建("net start w32time")
        子进程类.等待_阻塞(启动WindowsTime服务子进程)
        恢复为默认时间子进程 = 子进程类.子进程创建("w32tm /config /syncfromflags:domhier /update")
        子进程类.等待_阻塞(恢复为默认时间子进程)


# class 日期:
#     def __init__(self, 内嵌对象):
#         self.内嵌对象 = 内嵌对象

#     @staticmethod
#     def 创建_指定日期_通过年月日(年, 月, 日):
#         return 日期(datetime.date(年, 月, 日))


# class 时间:
#     def __init__(self, 内嵌对象):
#         self.内嵌对象 = 内嵌对象

#     @staticmethod
#     def 创建_指定时间_通过时分秒(时, 分, 秒):
#         return 时间(datetime.time(时, 分, 秒))


if __name__ == "__main__":
    # tz = datetime.timezone(datetime.timedelta(hours=8))
    # 时区 = datetime.datetime.now().astimezone().tzinfo
    # 时差 = datetime.timedelta(hours=8)
    a = 时间类.时间创建_当前()
    b = 时间类.属性获取_本地时区(a)
    c = 时间类.属性获取_时差(a)
    d = 时间类.属性设置_时差(a, 10)
    e = 时间类.转换_到格式化字符串(d, f"{时间格式化映射.日星期名称} {时间格式化映射.月名称} {时间格式化映射.日} {时间格式化映射.年完整} {时间格式化映射.时}:{时间格式化映射.分}:{时间格式化映射.秒} GMT{时间格式化映射.时差} ({时间类.属性获取_本地时区(d)})")
    # print(时区)
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    # from bxpy import 测试类

    # 测试类.测试启动_doctest()
