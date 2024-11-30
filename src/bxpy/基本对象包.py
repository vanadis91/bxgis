from typing import Union, Literal, Any


_全局变量_唯一ID = None


class 基本对象类:
    @staticmethod
    def 深拷贝(对象):
        import copy

        return copy.deepcopy(对象)

    @staticmethod
    def 属性获取(对象, 属性名称, 默认值=None):
        return getattr(对象, 属性名称, 默认值)

    @staticmethod
    def 是否具有属性(对象, 属性名称):
        return hasattr(对象, 属性名称)

    @staticmethod
    def 属性获取_所有(对象):
        return vars(对象)


class 枚举类_正则:
    任意字符_除换行符号 = "."


class 正则类(基本对象类):
    def __init__(self, 内嵌对象) -> None:
        self._内嵌对象 = 内嵌对象

    def 匹配字符串(self, 字符串, 模式: Literal["从任意位置匹配一个", "从头匹配一个", "查找所有匹配并返回列表", "查找所有匹配并返回迭代器", "替换匹配项"] = "从任意位置匹配一个", 替换内容=""):
        return 字类.匹配正则(字符串, self._内嵌对象, 模式, 替换内容)  # type: ignore


class 浮类(基本对象类):
    @staticmethod
    def 转换_到浮(x):
        if x in ["", None]:
            return 0.0
        return float(x)


class 整类(基本对象类):
    @staticmethod
    def 转换_到整(x):
        try:
            return int(x)
        except Exception as e:
            if isinstance(x, str):
                print(e)
                字符串列表 = list(x)
                字符串列表 = [x for x in 字符串列表 if x.isdigit() or x == "." or x == "-"]
                try:
                    ret = int(float("".join(字符串列表).lstrip("0")))
                    return ret
                except Exception as e:
                    print(e)
                    ret = int(float("".join(字符串列表).lstrip("0").replace("-", "")))
                    return ret
            else:
                raise e


class 表类(基本对象类):
    @staticmethod
    def 是否包含项(表, item):
        """
        如果定义了该方法，那么在执行item in container 或者 item not in container时该方法就会被调用。
        如果没有定义，那么Python会迭代容器中的元素来一个一个比较，从而决定返回True或者False。

        :param item:
        :return:

        >>> Object = ["123", "321", 正则表达式("^33")]

        >>> if  表.是否包含项(Object, "3333"):
        ...     assert True
        ... else:
        ...     assert False
        """
        if item in 表:
            return True
        for x1 in 表:  # type: ignore
            if type(x1) is 正则类 and type(item) is str and x1.匹配字符串(item):
                return True
        return False

    @staticmethod
    def 项增加(表, 元素, 索引=None) -> list:
        if 索引 is None:
            表.append(元素)  # type: ignore
        else:
            表.insert(索引, 元素)  # type: ignore
        return 表

    @staticmethod
    def 项删除(表, 索引或值=None, 判断是值还是索引: Literal["自动", "值", "索引"] = "自动"):
        if 索引或值 is None:
            表.pop()  # type: ignore
        elif (type(索引或值) is str and 判断是值还是索引 == "自动") or 判断是值还是索引 == "值":
            if 索引或值 in 表:  # type: ignore
                表.remove(索引或值)  # type: ignore
            else:
                print(f"值{索引或值}不在列表{self._内嵌对象}中，无法删除")  # type: ignore
        elif (type(索引或值) is int and 判断是值还是索引 == "自动") or 判断是值还是索引 == "索引":
            表.pop(索引或值)  # type: ignore
        return 表

    @staticmethod
    def 项替换(表: list, 旧元素, 新元素) -> list:
        表[表.index(旧元素)] = 新元素
        return 表

    @staticmethod
    def 表扩展(表, 值):
        表.extend(值)  # type: ignore
        return 表

    @staticmethod
    def 表粘接(表, 索引: int, 删除个数=0, 插入值的列表=[]):
        for x1 in range(索引, 索引 + 删除个数):
            表 = 表类.项删除(表, 索引)  # type: ignore

        插入值的列表.reverse()

        for x1 in 插入值的列表:
            表 = 表类.项增加(表, x1, 索引)  # type: ignore

        return 表  # type: ignore

    @staticmethod
    def 表反转(表):
        表.reverse()  # type: ignore
        return 表

    @staticmethod
    def 表分隔成子表(表: list, 子表长度):
        return [表[i : i + 子表长度] for i in range(0, len(表), 子表长度)]

    @staticmethod
    def 数学_最大值(表):
        return max(表)  # type: ignore

    @staticmethod
    def 数学_最小值(表):
        return min(表)  # type: ignore

    @staticmethod
    def 数学_汇总值(表):
        return sum(表)  # type: ignore

    @staticmethod
    def 项对应索引(表, 项):
        return 表.index(项)  # type: ignore

    @staticmethod
    def 项出现次数(表, 项):
        return 表.count(项)  # type: ignore

    @staticmethod
    def 查询(表, 查找语句):
        模块加载("tinydb")
        from tinydb import TinyDB
        from tinydb.storages import MemoryStorage

        _内嵌对象_数据库格式 = TinyDB(storage=MemoryStorage).table(字类.字符串生成_GUID())
        _内嵌对象_数据库格式.insert_multiple(表)  # type: ignore
        result = _内嵌对象_数据库格式.search(查找语句)
        return result

    @staticmethod
    def 排序(函数, x, 排序: Literal["升序", "降序"] = "升序"):
        排序映射 = {"升序": False, False: False, "降序": True, True: True}
        排序temp: bool = 排序映射[排序]
        return sorted(x, key=函数, reverse=排序temp)  # type: ignore

    @staticmethod
    def 映射(函数, *x: list):
        map对象 = map(函数, *x)
        return list(map对象)

    @staticmethod
    def 过滤(函数, *x: list):
        some对象 = filter(函数, *x)
        return list(some对象)

    @staticmethod
    def 查询游标():
        模块加载("tinydb")
        from tinydb import Query

        return Query()

    @staticmethod
    def 转换_到表(x):
        return list(x)


class 字类(基本对象类):
    @staticmethod
    def 替换(字, 旧字, 新字):
        字 = 字.replace(旧字, 新字)  # type: ignore
        return 字

    @staticmethod
    def 格式_去空格(字, 类型: Literal["去左去右", "去左", "去右"] = "去左去右"):
        if 类型 == "去左去右":
            字.strip()  # type: ignore
        elif 类型 == "去左":
            字.lstrip()  # type: ignore
        elif 类型 == "去右":
            字.rstrip()  # type: ignore
        return 字

    @staticmethod
    def 分隔成表(字, 分隔字符串):
        return 字.split(分隔字符串)  # type: ignore

    @staticmethod
    def 格式_大小写(字, 转换类型: Literal["大写", "小写", "首字母大写", "每个单词首字母大写"] = "大写"):
        if 转换类型 == "大写":
            字 = 字.upper()  # type: ignore
        elif 转换类型 == "小写":
            字 = 字.lower()  # type: ignore
        elif 转换类型 == "首字母大写":
            字 = 字.capitalize()  # type: ignore
        elif 转换类型 == "每个单词首字母大写":
            字 = 字.title()  # type: ignore
        return 字

    @staticmethod
    def 格式_补位(字, 补位后长度, 补位位置: Literal["前方", "后方"] = "前方", 补位字符="0") -> Union[str, "字类"]:
        if 补位位置 == "前方":
            字 = 字类.转换_到字(字).rjust(补位后长度, 补位字符)  # type: ignore
        elif 补位位置 == "后方":
            字 = 字类.转换_到字(字).ljust(补位后长度, 补位字符)  # type: ignore
        return 字

    @staticmethod
    def 匹配正则(字, 正则: str, 模式: Literal["从任意位置匹配一个", "从头匹配一个", "查找所有匹配并返回列表", "查找所有匹配并返回迭代器", "替换匹配项"] = "从任意位置匹配一个", 替换内容=""):
        import re

        if 模式 == "从任意位置匹配一个":
            return re.search(正则, 字)  # type: ignore
        elif 模式 == "从头匹配一个":
            return re.match(正则, 字)  # type: ignore
        elif 模式 == "查找所有匹配并返回列表":
            return list(re.findall(正则, 字))  # type: ignore
        elif 模式 == "查找所有匹配并返回迭代器":
            return re.finditer(正则, 字)  # type: ignore
        elif 模式 == "替换匹配项":
            return re.sub(正则, 替换内容, 字)  # type: ignore

    @staticmethod
    def 匹配正则列表(字, 正则列表: list, 模式: Literal["从任意位置匹配一个", "从头匹配一个", "查找所有匹配并返回列表", "查找所有匹配并返回迭代器", "替换匹配项"] = "从任意位置匹配一个", 替换内容=""):
        import re

        if 模式 == "从任意位置匹配一个":
            for 正则 in 正则列表:
                ret = re.search(正则, 字)
                if ret:
                    return ret
        elif 模式 == "从头匹配一个":
            for 正则 in 正则列表:
                ret = re.match(正则, 字)
                if ret:
                    return ret
        elif 模式 == "查找所有匹配并返回列表":
            retlist = []
            for 正则 in 正则列表:
                ret = list(re.findall(正则, 字))
                if len(ret) > 0:
                    retlist.extend(ret)
            return retlist
        elif 模式 == "查找所有匹配并返回迭代器":
            正则 = "|".join(正则列表)
            return re.finditer(正则, 字)  # type: ignore
        elif 模式 == "替换匹配项":
            for 正则 in 正则列表:
                字 = re.sub(正则, 替换内容, 字)
            return 字  # type: ignore

    @staticmethod
    def 字符串生成_GUID():
        """
        >>> type(str(字.字符串生成_GUID())).__name__
        'str'
        """
        import uuid

        return str(uuid.uuid1())

    @staticmethod
    def 字符串生成_短GUID_方式2():
        # import sys
        # from bxpy import 日志

        # 日志类.输出调试(sys.path)
        # 日志类.输出调试(sys.executable)
        模块加载("shortuuid")
        import shortuuid

        return str(shortuuid.uuid(pad_length=22))

    @staticmethod
    def 字符串生成_短GUID():
        import time
        import base64

        """生成唯一ID标记, 由大写字母和数字组成, 形如:AGEPAW5WOM"""
        global _全局变量_唯一ID

        def _Tmp() -> str:
            """根据毫秒数生成唯一ID"""
            # 获取当前时间的时间戳（毫秒级）
            milliseconds = int(time.time() * 1000)
            # 将整数转换为字节串
            num_bytes = milliseconds.to_bytes((milliseconds.bit_length() + 7) // 8, "big")
            # 生成唯一ID, 由大写字母和数字组成
            short_uid = base64.b32encode(num_bytes).decode("utf-8").rstrip("=")
            if len(short_uid) < 10:  # 确保生成的ID长度不超过10个字符
                short_uid = short_uid + short_uid
            return short_uid[0:10]

        short_uid = _Tmp()
        # 如果生成的ID和上次相同, 则等待一段时间重新生成
        if _全局变量_唯一ID != None and short_uid == _全局变量_唯一ID:
            time.sleep(0.001)  # 等待1毫秒, 肯定没有问题了
            short_uid = _Tmp()
        _全局变量_唯一ID = short_uid
        return short_uid

    @staticmethod
    def 字符串生成_14位时间戳():
        from bxpy.时间包 import 时间类

        return 时间类.转到_到时间戳_14位(时间类.时间创建_当前())

    @staticmethod
    def 字符串生成_ObjectId(唯一标识字符串=""):
        from bson.objectid import ObjectId

        if 唯一标识字符串 == "":
            return ObjectId()
        else:
            return ObjectId(唯一标识字符串)

    @staticmethod
    def 转换_到ObjectId(x):
        from bson.objectid import ObjectId

        if x == "":
            return ObjectId()
        else:
            return ObjectId(x)

    @staticmethod
    def 筛选相似字符串(x, 字符串列表, 返回列表长度=3, 相似度=0.6):
        import difflib

        similar_words = difflib.get_close_matches(x, 字符串列表, n=返回列表长度, cutoff=相似度)
        return similar_words

    @staticmethod
    def 是否可以转换为正整数(x):
        return x.isdigit()

    @staticmethod
    def 转换_到文件(x: str, 路径):
        with open(路径, "w", encoding="utf-8") as f:
            ret = f.write(x)
            return ret

    @staticmethod
    def 转换_从文件(路径, 编码格式: Literal["utf-8"] = "utf-8"):
        with open(路径, "r", encoding=编码格式) as f:
            ret = f.readlines()
            return ret

    @staticmethod
    def 转换_到字(x, 小数点后位数=2, json缩进=None):
        """
        >>> 字.转换_到str({1: 1, 2: 2})
        '{"1": 1, "2": 2}'
        """
        import json
        from bson.objectid import ObjectId

        if type(x) in [dict, list]:
            return json.dumps(x, ensure_ascii=False, indent=json缩进)
        elif type(x) is ObjectId:
            return str(x)
        elif type(x) is str:
            return x
        elif type(x) is tuple:
            return str(x)
        elif type(x) is int:
            return str(x)
        elif type(x) is float:
            a = format(x, f".{小数点后位数}f")
            # a = str(round(x, 小数点后位数))
            # if 小数点后位数 == 0:
            #     a = a.split(".")[0]
            # elif len(a.split(".")[1]) < 小数点后位数:
            #     a.
            return a
        else:
            print(f"该类型无法转换为字符串: {type(x)}")
            return str(x)


class 字典类(基本对象类):
    @staticmethod
    def 默认值设置(字典: dict, 键名称列表, 默认值=None):
        b = 字典
        for 键名称 in 键名称列表[0:-1]:
            try:
                b = b.__getitem__(键名称)
            except Exception as e:
                b.__setitem__(键名称, {})
                b = b.__getitem__(键名称)
        try:
            b = b.__getitem__(键名称列表[-1])
        except Exception as e:
            b.__setitem__(键名称列表[-1], 默认值)
            # b = b.__getitem__(键名称列表[-1])
        return 字典

    @staticmethod
    def 是否存在键(字典: dict, 键名称列表):
        b = 字典
        for x in 键名称列表:
            try:
                b = b[x]
            except Exception as e:
                return False
        return True

    @staticmethod
    def 解包合并(字典1: dict, 字典2: dict, 键删除列表=None):  # type: ignore
        """
        >>> dict1 = {"a": 1, "b": {"x": 2, "y": {"m": 3, "n": 4}}, "c": 5}
        >>> dict2 = {"b": {"y": {"p": 6}}, "d": 7}
        >>> c = 字典.解包合并(dict1, dict2)
        >>> print(c)
        {'a': 1, 'b': {'x': 2, 'y': {'m': 3, 'n': 4, 'p': 6}}, 'c': 5, 'd': 7}
        """
        from bxpy.日志包 import 日志类

        日志类.临时关闭日志()
        字典1 = 字典1.copy()  # type: ignore
        if 键删除列表:
            字典1Temp = 字典1
            for 嵌套的键 in 键删除列表:
                键列表 = 嵌套的键.split(".")
                最后一个键 = 键列表[-1]
                除了最后一个键的列表 = 键列表[0:-1]
                for 键 in 除了最后一个键的列表:
                    字典1Temp = 字典1Temp.get(键)  # type: ignore
                del 字典1Temp[最后一个键]  # type: ignore
                字典1Temp = 字典1
        日志类.输出调试(f"字典1：{字典1}")
        for key, value in 字典2.items():
            if key in 字典1 and isinstance(字典1[key], dict) and isinstance(value, dict):
                字典1[key] = 字典类.解包合并(字典1[key], value)
            elif isinstance(value, dict):
                字典1[key] = 字典类.解包合并({}, value)  # type: ignore
            else:
                字典1[key] = value
        return 字典1

    @staticmethod
    def 转换_到文件(x: dict, 路径, 编码格式: Literal["utf-8"] = "utf-8", 缩进=4):
        import json

        with open(路径, "w", encoding=编码格式) as f:
            json.dump(x, f, ensure_ascii=False, indent=缩进)
        return json.dumps(x)

    @staticmethod
    def 转换_从文件(路径, 编码格式: Literal["utf-8"] = "utf-8"):
        import json

        with open(路径, "r", encoding=编码格式) as f:
            # 从文件中读取 JSON 数据并转换为 Python 对象
            内容 = f.read()
            if 内容 != "":
                data = json.loads(内容)
            else:
                data = {}
        return data

    @staticmethod
    def 转换_从excel(excel路径, excel表名称="Sheet1", 指定行标签所在行的索引=0, 指定列标签所在列的索引=None, 要读取的列: Union[list, tuple, None] = None, 要读取的行: Union[list, tuple, None] = None, 要跳过的行: Union[list, None] = None, 指定数据类型=None, 被视为缺失值的值=None):
        from bxpandas.数据框架包 import 数据框架类

        a = 数据框架类.转换_从excel文件(excel路径=excel路径, excel表名称=excel表名称, 指定行标签所在行的索引=指定行标签所在行的索引, 指定列标签所在列的索引=指定列标签所在列的索引, 要读取的列=要读取的列, 要读取的行=要读取的行, 要跳过的行=要跳过的行, 指定数据类型=指定数据类型, 被视为缺失值的值=被视为缺失值的值)
        ret = 数据框架类.转换_到字典(a)
        return ret

    @staticmethod
    def 转换_到字典(x):
        import json

        return json.loads(x)


class 文件类:
    @staticmethod
    def 文件打开(路径, 模式: Literal["覆盖", "追加", "读取"] = "覆盖", 编码: Literal["utf-8", "gbk"] = "utf-8"):
        _模式映射 = {"覆盖": "w", "追加": "a", "读取": "r"}
        模式raw = _模式映射[模式] if 模式 in _模式映射 else 模式
        return open(路径, 模式raw, encoding=编码)

    @staticmethod
    def 文件写入(文件标识符, 内容):
        内容 = 字类.转换_到字(内容)
        文件标识符.write(内容)
        return 文件标识符

    @staticmethod
    def 文件写入_多行(文件标识符, 内容):
        # 内容 = 字类.转换_到字(内容)
        文件标识符.writelines(内容)
        return 文件标识符

    @staticmethod
    def 文件读取(文件标识符):
        return 文件标识符.read()

    @staticmethod
    def 文件读取_多行(文件标识符):
        return 文件标识符._内嵌对象.readlines


class 转换:
    @staticmethod
    def 转浮(x):
        return 浮类.转换_到浮(x)

    @staticmethod
    def 转整(x):
        return 整类.转换_到整(x)

    @staticmethod
    def 转表(x):
        return 表类.转换_到表(x)

    @staticmethod
    def 转字(x, 小数点后位数=2, json缩进=None):
        return 字类.转换_到字(x, 小数点后位数=小数点后位数, json缩进=json缩进)

    @staticmethod
    def 转字典(x):
        return 字典类.转换_到字典(x)


class IO流类:
    from io import StringIO

    @staticmethod
    def IO流创建():
        from io import StringIO

        return StringIO()

    @staticmethod
    def 写入(IO流对象, 内容):
        return IO流对象.write(内容)

    @staticmethod
    def 游标位置设置(IO流对象, 偏移量, 基点: Literal["开头", "当前位置", "末尾"] = "开头"):
        基点映射字典 = {"开头": 0, "当前位置": 1, "末尾": 2}
        基点raw = 基点映射字典[基点] if 基点 in 基点映射字典 else 基点
        return IO流对象.seek(偏移量, 基点raw)

    @staticmethod
    def 游标位置获取(IO流对象):
        return IO流对象.tell()

    @staticmethod
    def 缓冲区刷新(IO流对象):
        return IO流对象.flush()

    @staticmethod
    def 关闭(IO流对象):
        from bxpy.时间包 import 时间类

        # 时间类.等待(5)  # 为了便于读取输入的input函数的循环能够捕捉到所有的值
        IO流对象.close()

    @staticmethod
    def 属性获取_是否已关闭(IO流对象):
        return IO流对象.closed

    @staticmethod
    def 读取(IO流对象, 数量=-1):
        return IO流对象.read(数量)

    @staticmethod
    def 截断(IO流对象, 数量=None):
        return IO流对象.truncate(size=数量)

    @staticmethod
    def 读取_所有(IO流对象):
        return IO流对象.getvalue()

    @staticmethod
    def 清空(IO流对象: StringIO):
        IO流对象.truncate(0)
        IO流对象.seek(0)

    @staticmethod
    def 读取_一行(IO流对象, 数量=-1):
        return IO流对象.readline(数量)

    @staticmethod
    def 读取_按表输出(IO流对象):
        return IO流对象.readlines()


class IO函数配置:
    import sys

    上一次输入的值字典 = {}
    记录等待输入状态的值 = None
    输入流对象 = sys.stdin
    输出流对象 = sys.stdout


def 输出(内容, 结尾符号="\n", 输出流对象="默认"):
    输出流对象raw = IO函数配置.输出流对象 if 输出流对象 == "默认" else 输出流对象
    if 输出流对象raw:
        print(内容, end=结尾符号, file=输出流对象raw)  # type: ignore


def 输入(内容, 输出流对象="默认", 输入流对象="默认"):
    输入流对象raw = IO函数配置.输入流对象 if 输入流对象 == "默认" else 输入流对象
    import sys
    from bxpy.时间包 import 时间类

    if 输出流对象:
        输出(内容, 结尾符号="", 输出流对象=输出流对象)  # type: ignore
    if 输入流对象raw == sys.stdin:
        return input()
    elif 输入流对象raw:
        获取到的值 = IO流类.读取_所有(输入流对象raw)
        while 获取到的值 in ["", None] or (len(获取到的值) > 0 and 获取到的值[-1] != "\n"):  # type: ignore
            时间类.等待(1)
            获取到的值 = IO流类.读取_所有(输入流对象raw)
        IO流类.清空(输入流对象raw)  # type: ignore
        # 输出(f"输入函数获取到的值：{获取到的值}")
        return 获取到的值[:-1]


def 输入_带选项(提示信息, 存储上一次输入的变量=None, 变量的默认值="", 输入内容映射表=[], 输出流对象="默认", 输入流对象="默认") -> str:
    输入流对象raw = IO函数配置.输入流对象 if 输入流对象 == "默认" else 输入流对象
    输出流对象raw = IO函数配置.输出流对象 if 输出流对象 == "默认" else 输出流对象

    # 接收真实提示信息的对象 需要具有 控制台当前提示信息 属性
    if len(输入内容映射表) > 0:
        预选项字符串 = " ["
        for 预选项列表x in 输入内容映射表:
            预选项字符串 = 预选项字符串 + 预选项列表x[0] + "(" + 预选项列表x[1] + ")/"
        预选项字符串 = 预选项字符串[0:-1] + "]"
    else:
        预选项字符串 = ""

    if 存储上一次输入的变量:
        if 存储上一次输入的变量 not in IO函数配置.上一次输入的值字典.keys():
            if 变量的默认值[0:2] == "{{" and 变量的默认值[-2:] == "}}":
                IO函数配置.上一次输入的值字典[存储上一次输入的变量] = eval(变量的默认值[2:-2])
            else:
                IO函数配置.上一次输入的值字典[存储上一次输入的变量] = 变量的默认值
        提示字符串 = 提示信息 + 预选项字符串 + "：<" + IO函数配置.上一次输入的值字典[存储上一次输入的变量] + "> "
    else:
        提示字符串 = 提示信息 + 预选项字符串 + ": "

    IO函数配置.记录等待输入状态的值 = 提示字符串
    输入内容 = 输入(提示字符串, 输出流对象raw, 输入流对象raw)  # type: ignore
    IO函数配置.记录等待输入状态的值 = None
    if 输入内容 == "" and 存储上一次输入的变量:
        输入内容 = IO函数配置.上一次输入的值字典[存储上一次输入的变量]

    if len(输入内容映射表) > 0:
        允许的输入选项 = list(zip(*输入内容映射表))[1]
        while 输入内容 not in 允许的输入选项 and "*" not in 允许的输入选项:
            IO函数配置.记录等待输入状态的值 = 提示字符串
            输入内容 = 输入(提示字符串, 输出流对象raw, 输入流对象raw)  # type: ignore
            IO函数配置.记录等待输入状态的值 = None
            if 输入内容 == "":
                输入内容 = IO函数配置.上一次输入的值字典[存储上一次输入的变量]
        if 存储上一次输入的变量:
            IO函数配置.上一次输入的值字典[存储上一次输入的变量] = 输入内容
        for 输入内容_真实值, 输入内容_映射值 in 输入内容映射表:
            if 输入内容 == 输入内容_映射值:
                输入内容 = 输入内容_真实值
                break
    else:
        if 存储上一次输入的变量:
            IO函数配置.上一次输入的值字典[存储上一次输入的变量] = 输入内容

    return 输入内容  # type: ignore


def 模块加载(包名称: str, 下载时包名称=None, 包版本: Union[str, None, Literal["==3.9.0", ">=3.9.*"]] = None, 包管理工具="pdm"):
    常用包名称映射字典 = {
        "win32": ("win32api", "pywin32"),
        "win32api": ("win32api", "pywin32"),
        "pywin32": ("win32api", "pywin32"),
    }
    包名称, 下载时包名称 = 常用包名称映射字典[包名称] if 包名称 in 常用包名称映射字典 else (包名称, 下载时包名称)
    下载时包名称 = 包名称 if 下载时包名称 is None else 下载时包名称
    import importlib
    from bxpy.日志包 import 日志类

    try:
        importlib.import_module(包名称)
        return None
    except Exception as e:
        if "No module named" not in str(e):
            raise e
        import urllib.request
        from bxpy.基本对象包 import 输出
        from bxpy.元数据包 import 调用元数据类
        import subprocess
        import os

        当前帧 = 调用元数据类.调用栈帧获取_当前()
        上一帧 = 调用元数据类.调用栈帧.上一级调用栈帧获取(当前帧)
        上一帧所在文件路径 = 调用元数据类.调用栈帧.属性获取_所在文件路径(上一帧)
        from bxpy.路径包 import 路径类

        文件所在目录原始 = 路径类.属性获取_目录(上一帧所在文件路径)
        文件所在目录 = 文件所在目录原始
        while not 路径类.是否存在(路径类.连接(文件所在目录, "pyproject.toml")):
            try:
                文件所在目录 = 路径类.属性获取_目录(文件所在目录)
            except Exception as e:
                raise Exception(f"似乎一直无法找到存在pyproject.toml的目录，最开始查找的路径是{文件所在目录原始}")

        输出(f"{文件所在目录}所在包中，{包名称}不存在，开始尝试下载{下载时包名称}")
        if urllib.request.urlopen(f"https://pypi.org/pypi/{下载时包名称}/json").getcode() != 200:
            raise Exception(f"pypi中不存在名称为{下载时包名称}的包")

        输出(f"开始下载{下载时包名称}")

        当前工作目录 = os.getcwd()
        os.chdir(文件所在目录)
        if 包管理工具 == "pdm":
            带有具体版本的包名称 = f"{下载时包名称}{包版本}" if 包版本 else 下载时包名称
            result = subprocess.Popen(f"pdm add {带有具体版本的包名称}", stdout=subprocess.PIPE)
            输出(result.communicate())  # type: ignore
        os.chdir(当前工作目录)
        try:
            importlib.import_module(包名称)
            输出(f"{包名称}下载并加载成功")
            return True
        except Exception as e:
            输出(f"{包名称}下载失败")
            raise (e)


# def 模块检测(模块名称: str, 包管理工具="pdm"):
#     try:
#         exec(模块名称)
#     except Exception as e:
#         if "from " in 模块名称:
#             包名称 = 模块名称.split("from ")[1].split(" import ")[0].split(".")[0]
#         else:
#             包名称 = 模块名称.split("import ")[1].split(" ")[0].split(".")[0]
#         if "No module named" not in str(e):
#             print(f"{包名称}加载失败")
#             raise e
#         from bxpy.网络会话包 import 会话类

#         print(f"{包名称}不存在，开始尝试下载")
#         if 会话类.响应类.属性获取_状态码(会话类.会话创建(f"https://pypi.org/pypi/{包名称}/json")) != 200:
#             raise Exception(f"pypi中不存在名称为{包名称}的包")

#         from bxpy.进程包 import 子进程类

#         print(f"开始下载{包名称}")
#         子进程 = 子进程类.子进程创建(f"pdm add {包名称}")
#         子进程类.输出获取_阻塞_逐行获取(子进程)
#         try:
#             exec(模块名称)
#             print(f"{包名称}下载并加载成功")
#         except Exception as e:
#             print(f"{包名称}下载失败")
#             raise (e)


if __name__ == "__main__":
    # from bxpy.元数据包 import 调用元数据类

    # 当前帧 = 调用元数据类.调用栈帧获取_当前()
    # 文件名称 = 调用元数据类.调用栈帧.上一级调用栈帧获取(当前帧)
    # print(文件名称)
    # import shortuuid
    # from io import StringIO

    # 输入输出流 = StringIO()
    # 输入输出流.write("测试1\n")
    # 输入输出流.write("测试2")
    # while 输入输出流.closed == False:
    # 输入输出流.seek(0)
    # a = 输入输出流.readline()
    # 输入输出流.truncate()

    # a = 输入输出流.getvalue()
    # b = 输入输出流.getvalue()
    # print(f"a:{a}")
    # print(f"b:{b}")
    # print(shortuuid.uuid(pad_length=22))
    # print(shortuuid.get_alphabet())
    # 模块加载("bs4", "beautifulsoup4")
    # target_word = "applyes"
    # word_list = ["ape", "apples", "banana", "apply", "pineapple"]
    # ret = 字类.筛选相似字符串(target_word, word_list, 返回列表长度=1)
    # print(ret)
    # while True:
    # 测试变量 = 输入("测试内容", "测试变量", "0", [["啊啊", "0"], ["版本", "1"]])
    # print(f"测试变量：{测试变量}")
    # 测试变量 = 输入("测试内容", "测试变量", "0", [["啊啊", "0"], ["版本", "1"], ["仓储", "*"]])
    # print(f"测试变量：{测试变量}")
    # 测试变量 = 输入("测试内容", "测试变量", "0")
    # print(f"测试变量：{测试变量}")
    # 测试变量 = 输入("测试内容")
    # print(f"测试变量：{测试变量}")
    # 测试变量 = 输入("测试内容", 输入内容映射表=[["啊啊", "0"], ["版本", "1"], ["仓储", "*"]])
    # print(f"测试变量：{测试变量}")
    # 测试变量 = 输入("测试内容", 输入内容映射表=[["啊啊", "0"], ["版本", "1"]])
    # print(f"测试变量：{测试变量}")
    # print(整类.转换_到整("123.156a"))3
    # a = [1, 2, 3]
    # b = 表(a).项增加(4)
    # print(b._内嵌对象)
    # print(type(b))
    # print(getattr(字, "去掉空格")(" 123132 "))
    # from bxpy import 测试

    # 测试.测试启动_doctest()
    pass
