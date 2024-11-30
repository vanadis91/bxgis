# *-* coding:utf8 *-*

import os
import shutil
from typing import Union, Literal, AnyStr

# import psutil
# from pathlib import Path
# from bxpy import 字
from bxpy.日志包 import 日志类

# from bxpy import 进程
from bxpy.时间包 import 时间类


# import time
# import stat

# from concurrent.futures import ThreadPoolExecutor

# import win32gui
# import win32con
# import time
# from tkinter import messagebox
# import win32api

# from bxpy import 对象


# class bxpath(os.PathLike, bxobj):
#     def __init__(self, 内嵌对象) -> None:
#         if type(内嵌对象) is str:
#             self._内嵌对象: str = 路径.规范化(内嵌对象, None, "反斜杠", True)
#         elif type(内嵌对象) is bxpath:
#             self._内嵌对象 = 内嵌对象._内嵌对象
#         else:
#             self._内嵌对象 = 路径.规范化(内嵌对象, None, "反斜杠", True)

#     def __fspath__(self):
#         return self._内嵌对象

#     def __repr__(self) -> str:
#         return self._内嵌对象

#     def 新增(self, 强制明确路径的类型=None, 是否覆盖=False):
#         return 路径.新增(self._内嵌对象, 强制明确路径的类型=强制明确路径的类型, 是否覆盖=是否覆盖)

#     def 连接(self, *连接路径):
#         self._内嵌对象 = os.path.join(self._内嵌对象, *连接路径)
#         return self

#     def 复制(self, 目标路径, 链接处理方式="保持原样", 多进程=False):
#         return 路径.复制(self._内嵌对象, 目标路径, 链接处理方式=链接处理方式, 多进程=多进程)

#     def 删除(self):
#         return 路径.删除(self._内嵌对象)

#     def 修改(self, 目标路径):
#         return 路径.修改(self._内嵌对象, 目标路径)

#     def 分隔为部件(self, 返回形式="列表"):
#         return 路径.分隔为部件(self._内嵌对象, 返回形式=返回形式)

#     @property
#     def 部件_目录(self):
#         return self.分隔为部件()[0]

#     @property
#     def 部件_文件名_去扩展名(self):
#         return self.分隔为部件()[1]

#     @property
#     def 部件_扩展名(self):
#         return self.分隔为部件()[2]

#     @property
#     def 部件_驱动器(self):
#         return self.分隔为部件()[3]

#     @property
#     def 部件_文件名_有扩展名(self):
#         return self.分隔为部件()[4]

#     def 链接_新增(self, 目标路径, 链接类型="符号链接"):
#         return 路径.链接_新增(self._内嵌对象, 目标路径, 链接类型)

#     def 链接_真实路径(self):
#         return 路径.链接_真实路径(self._内嵌对象)

#     def 规范化(self, 转换大小写="小写", 转换斜杠="反斜杠", 删除末尾的路径分隔符=False):
#         self._内嵌对象 = 路径.规范化(self._内嵌对象, 转换大小写=转换大小写, 转换斜杠=转换斜杠, 删除末尾的路径分隔符=删除末尾的路径分隔符)
#         return self

#     def 是否存在(self, 链接处理方式="保持原样"):
#         return 路径.是否存在(self._内嵌对象, 链接处理方式=链接处理方式)

#     def 是否为文件(self):
#         return 路径.是否为文件(self._内嵌对象)

#     def 是否为目录(self):
#         return 路径.是否为目录(self._内嵌对象)

#     def 是否为链接(self):
#         return 路径.是否为链接(self._内嵌对象)

#     def 是否为绝对路径(self):
#         return 路径.是否为绝对路径(self._内嵌对象)

#     def 子路径(self, 单一层次=True, 链接处理方式="保持原样"):
#         return 路径.子路径(self._内嵌对象, 单一层次=单一层次, 链接处理方式=链接处理方式)

#     def 转绝对(self, 待转换路径=".\\"):
#         self._内嵌对象 = 路径.转绝对(待转换路径=待转换路径, 基点路径=self._内嵌对象)
#         return self

#     def 转相对(self, 基点路径):
#         self._内嵌对象 = 路径.转相对(self._内嵌对象, 基点路径)
#         return self

#     @staticmethod
#     def 盘符获取():
#         """

#         >>> 路径.盘符获取()[0]
#         {'盘符': 'C:\\\\', '文件类型': 'NTFS'}
#         """
#         import psutil

#         partitions = psutil.disk_partitions()
#         return [{"盘符": partition.device, "文件类型": partition.fstype} for partition in partitions]

#     @staticmethod
#     def 属性_获取(源路径, 属性名称):
#         if 属性名称 == "类型":
#             if 路径.是否为文件(源路径):
#                 return "文件"
#             elif 路径.是否为目录(源路径):
#                 return "目录"
#             elif 路径.是否为链接(源路径):
#                 return "链接"
#         # return win32api.GetFileAttributes(源路径)
#         elif 属性名称 == "容量":
#             if 源路径[-1:] == ":" or 源路径[-2:] == ":\\" or len(源路径) == 1:
#                 if len(源路径) == 1:
#                     源路径 = 源路径 + ":"
#                 if 路径.是否存在(源路径):
#                     import psutil

#                     temp = psutil.disk_usage(源路径)
#                     temp = {
#                         "总容量": psutil._common.bytes2human(temp.total),
#                         "已用容量": psutil._common.bytes2human(temp.used),
#                         "剩余容量": psutil._common.bytes2human(temp.free),
#                         "已用百分比": psutil._common.bytes2human(temp.percent),
#                     }
#                     return temp
#                 else:
#                     temp = {"总容量": "0", "已用容量": "0", "剩余容量": "0", "已用百分比": "0"}
#                     return temp
#             else:
#                 return os.path.getsize(源路径)
#         elif 属性名称 == "修改时间":
#             return os.path.getmtime(源路径)
#         elif 属性名称 == "访问时间":
#             return os.path.getatime(源路径)
#         elif 属性名称 == "创建时间":
#             return os.path.getctime(源路径)

#     @staticmethod
#     def 属性_设置(源路径, 属性名称, 属性值):
#         pass
#         # FILE_ATTRIBUTE_READONLY = 1 (0x1)  只读
#         # FILE_ATTRIBUTE_HIDDEN = 2 (0x2) 隐藏
#         # FILE_ATTRIBUTE_SYSTEM = 4 (0x4) 系统文件
#         # FILE_ATTRIBUTE_DIRECTORY = 16 (0x10) 目录
#         # FILE_ATTRIBUTE_ARCHIVE = 32 (0x20)
#         # FILE_ATTRIBUTE_NORMAL = 128 (0x80) 常规
#         # FILE_ATTRIBUTE_TEMPORARY = 256 (0x100)
#         # FILE_ATTRIBUTE_SPARSE_FILE = 512 (0x200)
#         # FILE_ATTRIBUTE_REPARSE_POINT = 1024 (0x400)
#         # FILE_ATTRIBUTE_COMPRESSED = 2048 (0x800)
#         # FILE_ATTRIBUTE_OFFLINE = 4096 (0x1000)
#         # FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192 (0x2000)
#         # FILE_ATTRIBUTE_ENCRYPTED = 16384 (0x4000)
#         # return win32api.SetFileAttributes(源路径, 属性)


# 定义复制文件的函数, 如果是闭包，则多进程无法执行该函数
def _多进程复制_复制文件(源路径列表x, 源目录, 目标目录, 复制的对象, 链接处理方式):
    # 源路径x = list(源路径列表x.keys())[0]
    目标路径x = list(源路径列表x.keys())[0].replace(源目录, 路径类.连接(目标目录, 复制的对象))
    # 文件数量 = len(list(源路径列表x.values())[0])
    if not 路径类.是否存在(目标路径x):
        路径类.新增(目标路径x, 路径类型="目录")
    for i, j in 源路径列表x.items():
        for nn in [路径类.连接(i, k) for k in j]:
            日志类.输出调试(f"从源{nn}复制到目标{目标路径x}")
            路径类.复制(nn, 目标路径x, 链接处理方式=链接处理方式)
    文件数量 = len(路径类.子路径(目标路径x, 单一层次=True)[2])  # type: ignore
    日志类.输出调试(f"路径下文件列表{路径类.子路径(目标路径x, 单一层次=True)}")
    return 文件数量


def _多进程复制(源路径, 目标路径, 链接处理方式="保持原样"):
    日志类.临时关闭日志()
    from bxpy.进程包 import 多进程类, 多进程池类

    源目录 = 源路径  # 这个函数从 路径.复制 转过来，所以源路径一定是目录类型，并且目标路径已经创建好了
    目标目录 = 目标路径

    复制的对象 = 路径类.属性获取_文件名(路径类.链接_真实路径(源路径))
    日志类.输出调试("正式开始复制了1")
    队列 = 多进程类.队列类.队列创建()
    文件计数 = 0
    文件总数 = 0
    目录计数 = -1  # 不包括源路径本身
    目录总数 = -1  # 不包括源路径本身
    日志类.输出调试("正式开始复制了2")
    # 读取文件列表
    for root, dirs, files in 路径类.子路径(源目录, 单一层次=False, 链接处理方式=链接处理方式):
        路径类.新增(root.replace(源目录, 路径类.连接(目标目录, 复制的对象)), 路径类型="目录")
        多进程类.队列类.放入(队列, {root: files})
        文件总数 += len(files)
        目录总数 += 1
    多进程类.队列类.放入(队列, False)

    # 定义计数的函数
    def 计数(文件数量):
        nonlocal 文件计数, 目录计数
        日志类.输出调试(f"文件数量{文件数量}文件计数{文件计数}目录计数{目录计数}")
        文件计数 += 文件数量
        目录计数 += 1
        cls = round(文件计数 / 文件总数 * 100)
        # print(f'\r文件数: {文件计数}/{文件总数} 目录数: {目录计数}/{目录总数} 百分比: {cls}% {"*" * round(cls/2)}', end='')
        print(f"\r文件数: {文件计数}/{文件总数} 目录数: {目录计数}/{目录总数} 百分比: {cls}%", end="")

    # 定义出错后函数
    def 跳错(err):
        print(f"多线程跳错：{err}")

    # 正式开始复制
    print(f"正在从 {源目录} 复制所有文件到 {目标目录}")
    日志类.输出调试("正式开始复制了")
    开始时间戳 = 时间类.转换_到时间戳(时间类.时间创建_当前())
    p = 多进程池类.多进程池创建()
    while True:
        t = 多进程类.队列类.取出(队列)
        if not t:
            break
        多进程池类.运行_异步(p, _多进程复制_复制文件, 子程序参数=(t, 源目录, 目标目录, 复制的对象, 链接处理方式), 子程序回调=计数, 跳错回调=跳错)

    多进程池类.关闭(p)
    多进程池类.阻塞主程序(p)
    耗时 = round(时间类.转换_到时间戳(时间类.时间创建_当前()) - 开始时间戳, 2)  # type: ignore
    print(f"\r共复制文件{文件计数}/{文件总数}个，目录{目录计数}/{目录总数}个，耗时{耗时}秒")
    # print(f'文件计数有没有少：{(文件计数 == 文件总数)}，目录计数有没有少：{(目录计数 == 目录总数)}')
    if (文件计数 == 文件总数) and (目录计数 == 目录总数):
        return True
    else:
        return False


class 路径类:
    @staticmethod
    def 属性获取_目录(x, 获取次数=1):
        for i in range(获取次数):
            x = 路径类.分隔为部件(x)[0]
        return x

    @staticmethod
    def 属性获取_文件名(x):
        return 路径类.分隔为部件(x)[4]

    @staticmethod
    def 属性获取_文件名_去扩展名(x):
        return 路径类.分隔为部件(x)[1]

    @staticmethod
    def 属性获取_扩展名(x):
        return 路径类.分隔为部件(x)[2]

    @staticmethod
    def 属性获取_驱动器(x):
        return 路径类.分隔为部件(x)[3]

    @staticmethod
    def 属性获取_类型(源路径):
        if 路径类.是否为文件(源路径):
            return "文件"
        elif 路径类.是否为目录(源路径):
            return "目录"
        elif 路径类.是否为链接(源路径):
            return "链接"

    @staticmethod
    def 属性获取_容量(源路径, 单一层次=True, 链接处理方式="保持原样") -> Union[dict, float]:  # type: ignore
        if 源路径[-1:] == ":" or 源路径[-2:] == ":\\" or len(源路径) == 1:
            if len(源路径) == 1:
                源路径 = 源路径 + ":"
            if 路径类.是否存在(源路径, 链接处理方式="向下探索"):
                from bxpy.基本对象包 import 模块加载

                模块加载("psutil")
                import psutil

                temp = psutil.disk_usage(源路径)  # type: ignore
                temp = {
                    "总容量": psutil._common.bytes2human(temp.total),  # type: ignore
                    "已用容量": psutil._common.bytes2human(temp.used),  # type: ignore
                    "剩余容量": psutil._common.bytes2human(temp.free),  # type: ignore
                    "已用百分比": psutil._common.bytes2human(temp.percent),  # type: ignore
                }
                return temp
            else:
                temp = {"总容量": "0", "已用容量": "0", "剩余容量": "0", "已用百分比": "0"}
                return temp
        elif 路径类.是否为文件(源路径):
            return os.path.getsize(源路径)
        elif 路径类.是否为目录(源路径) and 单一层次:
            子路径列表 = 路径类.子路径(源路径, 单一层次=单一层次, 链接处理方式=链接处理方式)
            ret = 0
            for 文件名x in 子路径列表[2]:
                文件路径x = 路径类.连接(子路径列表[0], 文件名x)
                ret += 路径类.属性获取_容量(文件路径x)  # type: ignore
            return ret
        elif 路径类.是否为目录(源路径) and not 单一层次:
            from bxpy.进度条包 import 进度条类

            子路径列表 = 路径类.子路径(源路径, 单一层次=单一层次, 链接处理方式=链接处理方式, 返回形式="生成器")
            ret = 0
            for 子路径列表x in 进度条类.进度条创建(子路径列表, 前置信息="开始统计文件夹的容量"):
                for 文件名x in 子路径列表x[2]:
                    文件路径x = 路径类.连接(子路径列表x[0], 文件名x)
                    ret += 路径类.属性获取_容量(文件路径x)  # type: ignore
            return ret
        elif 路径类.是否为链接(源路径) and 链接处理方式 == "向下探索":
            return 路径类.属性获取_容量(路径类.链接_真实路径(源路径), 单一层次=单一层次, 链接处理方式=链接处理方式)
        elif 路径类.是否为链接(源路径) and 链接处理方式 == "保持原样":
            return os.path.getsize(源路径)

    @staticmethod
    def 属性获取_修改时间(源路径):
        return os.path.getmtime(源路径)

    @staticmethod
    def 属性获取_访问时间(源路径):
        return os.path.getatime(源路径)

    @staticmethod
    def 属性获取_创建时间(源路径):
        return os.path.getctime(源路径)

    @staticmethod
    def 属性获取_md5(源路径):
        import hashlib

        md5 = hashlib.md5()
        with open(源路径, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()

    @staticmethod
    def 属性获取_分隔符():
        return os.sep

    @staticmethod
    def 属性设置(源路径, 属性名称, 属性值):
        pass
        # FILE_ATTRIBUTE_READONLY = 1 (0x1)  只读
        # FILE_ATTRIBUTE_HIDDEN = 2 (0x2) 隐藏
        # FILE_ATTRIBUTE_SYSTEM = 4 (0x4) 系统文件
        # FILE_ATTRIBUTE_DIRECTORY = 16 (0x10) 目录
        # FILE_ATTRIBUTE_ARCHIVE = 32 (0x20)
        # FILE_ATTRIBUTE_NORMAL = 128 (0x80) 常规
        # FILE_ATTRIBUTE_TEMPORARY = 256 (0x100)
        # FILE_ATTRIBUTE_SPARSE_FILE = 512 (0x200)
        # FILE_ATTRIBUTE_REPARSE_POINT = 1024 (0x400)
        # FILE_ATTRIBUTE_COMPRESSED = 2048 (0x800)
        # FILE_ATTRIBUTE_OFFLINE = 4096 (0x1000)
        # FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192 (0x2000)
        # FILE_ATTRIBUTE_ENCRYPTED = 16384 (0x4000)
        # return win32api.SetFileAttributes(源路径, 属性)

    @staticmethod
    def 新增(源路径, 路径类型: Literal["自动", "文件", "目录"] = "自动", 是否覆盖=False, 已存在时是否提示=False):
        日志类.临时关闭日志()
        """简单的单行注释。
        :param 强制明确路径的类型: '文件'|'目录'
        >>> 路径.新增(r"C:\\Users\\beixiao\\Desktop\\123.txt")
        True
        >>> 路径.新增(r"C:\\Users\\beixiao\\Desktop\\123.txt")
        C:\\Users\\beixiao\\Desktop\\123.txt已存在，新增路径失败
        False
        >>> 路径.删除(r"C:\\Users\\beixiao\\Desktop\\123.txt")
        True
        """
        源路径 = 路径类.规范化(源路径.strip())  # 删掉开头和末尾的空格符，然后删除末尾的\\
        扩展名 = 路径类.属性获取_扩展名(源路径)
        if 路径类.是否存在(源路径):
            if 是否覆盖:
                路径类.删除(源路径)
                路径类.新增(源路径, 路径类型=路径类型)
                if 已存在时是否提示:
                    print(f"{源路径}已存在，已删除并重新新建")
            else:
                if 已存在时是否提示:
                    print(f"{源路径}已存在，已跳过新建")
        else:
            if (扩展名 and 路径类型 == "自动") or (路径类型 == "文件"):
                if not 路径类.是否存在(路径类.属性获取_目录(源路径)):
                    try:
                        os.makedirs(路径类.属性获取_目录(源路径))  # 必须有路径的上级目录，否则跳错
                    except Exception as err:
                        print(f"创建上一级目录失败，上一级目录为{路径类.属性获取_目录(源路径)}，{err}")
                try:
                    fo = open(源路径, mode="x")
                    fo.close()
                except Exception as err:
                    print(f"新增文件失败，路径为{源路径}，{err}")
            elif (扩展名 == "" and 路径类型 == "自动") or (路径类型 == "目录"):
                try:
                    os.makedirs(源路径)
                except Exception as err:
                    print(f"新增目录失败，路径为{源路径}，{err}")
        if not 路径类.是否存在(源路径):
            print(f"新增路径失败，路径为，{源路径}")
        else:
            日志类.输出调试(f"新增路径成功，路径为，{源路径}")
            return True

    @staticmethod
    def 新增文件(源路径, 是否覆盖=False, 已存在时是否提示=False):
        return 路径类.新增(源路径, "文件", 是否覆盖, 已存在时是否提示=已存在时是否提示)

    @staticmethod
    def 新增目录(源路径, 是否覆盖=False):
        return 路径类.新增(源路径, "目录", 是否覆盖)

    @staticmethod
    def 连接(源路径, *连接路径):
        return 路径类.规范化(os.path.join(源路径, *连接路径))

    @staticmethod
    def 复制(源路径, 目标目录, 链接处理方式="保持原样", 多进程=False):
        日志类.临时关闭日志()
        """将源路径的文件或者目录，复制到目标路径的下一个层次

        :param 源路径:
        :param 目标路径:目标路径必须是目录，如果要重命名需要用 路径.修改 函数
        :param 链接处理方式:
        :param 多进程:
        :return:
        :test:
        aa = "L:\\Beixiao\\Sync\\030.办公室电脑\\Database\\2.法规\\G拱墅区关于进一步加强拱墅区学校（幼儿园）建设标准的实施意见.pdf"
        bb = "I:\\Beixiao\\Database\\2.法规\\G拱墅区关于进一步加强拱墅区学校（幼儿园）建设标准的实施意见.pdf"
        shutil.copytree(aa, bb, symlinks=False)
        路径.新增(路径.分隔为部件(bb)[0], 强制明确路径的类型='目录')
        路径.新增(bb, 强制明确路径的类型='文件', 是否覆盖=True)
        shutil.copy2(aa, bb, follow_symlinks=False)
        """
        源路径_真实 = 路径类.链接_真实路径(路径类.规范化(源路径))  # 添加真实路径是为了避免因为大小写导致复制失败
        目标目录_真实 = 路径类.链接_真实路径(路径类.规范化(目标目录))  # 添加真实路径是为了避免因为大小写导致复制失败
        复制的对象 = 路径类.属性获取_文件名(源路径_真实)
        结果 = None
        日志类.输出调试(f"源路径为{源路径}")
        日志类.输出调试(f"源路径类型为{路径类.属性获取_类型(源路径)}")
        日志类.输出调试(f"复制的对象为: {复制的对象}")
        if not 路径类.是否存在(目标目录_真实):
            路径类.新增(目标目录_真实, 路径类型="目录")  # 必须有路径的上级目录，否则shutil.copy2跳错
        if 路径类.是否为目录(源路径_真实):
            if 链接处理方式 == "保持原样" and not 多进程:
                日志类.输出调试("进入到了单线程保持原样复制")
                shutil.copytree(源路径, 路径类.连接(目标目录_真实, 复制的对象), symlinks=True, dirs_exist_ok=True)  # 添加真实路径是为了避免因为大小写导致复制失败
            elif 链接处理方式 == "向下探索" and not 多进程:
                日志类.输出调试("进入到了单线程向下探索复制")
                shutil.copytree(源路径, 路径类.连接(目标目录_真实, 复制的对象), symlinks=False, dirs_exist_ok=True)
            elif 多进程:
                日志类.输出调试("进入到了多线程复制")
                结果 = _多进程复制(源路径, 目标目录_真实, 链接处理方式=链接处理方式)
                日志类.输出调试(f"返回的结果是：{结果}")
        elif 路径类.是否为文件(路径类.链接_真实路径(源路径)):
            if 链接处理方式 == "保持原样":
                shutil.copy2(源路径, 路径类.连接(目标目录_真实, 复制的对象), follow_symlinks=False)
            elif 链接处理方式 == "向下探索":
                shutil.copy2(源路径, 路径类.连接(目标目录_真实, 复制的对象), follow_symlinks=True)
        if (路径类.是否存在(路径类.连接(目标目录_真实, 复制的对象)) and 多进程 and 结果) or (路径类.是否存在(路径类.连接(目标目录_真实, 复制的对象)) and (not 多进程)):
            日志类.输出调试(f"结果：{结果}，是否存在：{路径类.是否存在(路径类.连接(目标目录_真实, 复制的对象))}")
            # print(f'从 {源路径_真实} 复制到 {目标路径_真实} 成功')
            return True
        else:
            print(f"从 {源路径_真实} 复制到 {目标目录_真实} 失败")
            # 当前只检测第一层文件或目录是否存在，没有匹配复制的文件或目录是否所有成功
            return False

    @staticmethod
    def 删除(源路径):
        """

        :param 源路径:
        :return:
        :test:路径.删除('H:\\Beixiao\\Database\\4.资料\\H杭州市钱塘区城镇社区建设专项规划')
        """
        from bxpy.进程包 import 子进程类

        日志类.临时关闭日志()

        源路径 = 路径类.规范化(源路径)

        def 第一次删除失败时改权属(func, path, execinfo):
            import stat

            os.chmod(path, stat.S_IWUSR)
            func(path)

        if 路径类.是否为链接(源路径):
            日志类.输出调试(f"{源路径}识别为链接")
            try:
                os.remove(源路径)
            except Exception as e:
                import sys

                if sys.platform.startswith("win"):
                    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{源路径}"', 编码="gbk")
                    ret = 子进程类.交互_输入关闭等待结束并输出获取(子程序)
                    日志类.输出调试(ret)
                elif sys.platform.startswith("linux"):
                    子程序 = 子进程类.子进程创建(f'rm -rf "{源路径}"')
                    ret = 子进程类.交互_输入关闭等待结束并输出获取(子程序)
                    日志类.输出调试(ret)
                else:
                    print(f"{源路径}删除失败")
        elif 路径类.是否为文件(源路径):
            日志类.输出调试(f"{源路径}识别为文件")
            try:
                os.remove(源路径)
            except Exception as e:
                import sys

                if sys.platform.startswith("win"):
                    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{源路径}"', 编码="gbk")
                    ret = 子进程类.交互_输入关闭等待结束并输出获取(子程序)
                    日志类.输出调试(ret)
                elif sys.platform.startswith("linux"):
                    子程序 = 子进程类.子进程创建(f'rm -rf "{源路径}"')
                    ret = 子进程类.交互_输入关闭等待结束并输出获取(子程序)
                    日志类.输出调试(ret)
                else:
                    print(f"{源路径}删除失败")
        elif 路径类.是否为目录(源路径):
            日志类.输出调试(f"{源路径}识别为目录")
            shutil.rmtree(源路径, onerror=第一次删除失败时改权属)
        if 路径类.是否存在(源路径):
            print(f"{源路径}删除失败")
            return False
        else:
            日志类.输出调试(f"{源路径}删除成功")
            return True

    @staticmethod
    def 修改(源路径, 目标路径):
        源路径 = 路径类.规范化(源路径)
        目标路径 = 路径类.规范化(目标路径)
        os.rename(源路径, 目标路径)
        if not 路径类.是否存在(源路径, 链接处理方式="向下探索") and 路径类.是否存在(目标路径, 链接处理方式="向下探索"):
            日志类.输出调试(f"{源路径}修改成功")
            return True
        else:
            print(f"{源路径}修改失败")
            return False

    @staticmethod
    def 分隔为部件(源路径, 返回形式="列表") -> Union[list, dict]:
        ret = []
        源路径 = 路径类.规范化(源路径)
        源路径列表 = os.path.splitext(源路径)
        扩展名 = 源路径列表[1]
        源路径_去扩展名 = 路径类.规范化(源路径列表[0].strip())
        # temp = os.path.split(源路径_去扩展名)
        目录 = os.path.dirname(源路径_去扩展名)
        去扩展名文件名 = os.path.basename(源路径_去扩展名)
        驱动器 = os.path.splitdrive(目录)[0]
        文件名 = 去扩展名文件名 + 扩展名
        if 返回形式 == "列表":
            ret = [目录, 去扩展名文件名, 扩展名, 驱动器, 文件名]
        elif 返回形式 == "字典":
            ret = {"驱动器": 驱动器, "目录": 目录, "文件名": 文件名, "扩展名": 扩展名, "去扩展名文件名": 去扩展名文件名}
        return ret

    @staticmethod
    def 链接_新增(源路径, 目标目录, 链接类型: Literal["符号链接", "硬链接", "目录连接点"] = "符号链接", 目标文件名称: Union[Literal["等同于源"], AnyStr] = "等同于源"):
        """将源路径的文件或者目录，链接到目标路径的下一个层次

        :param 源路径:
        :param 目标路径:目标路径必须是目录，如果要重命名需要用 路径.修改 函数
        :param 链接类型:'符号链接'|'目录连接点'|'硬链接'
        :return:路径.是否为目录(路径.链接_真实路径('C:\\Users\\beixiao\\Database\\4.资料\\H杭州市钱塘区城镇社区建设专项规划'))
        :test:
        """
        from bxpy.进程包 import 子进程类

        源路径 = 路径类.规范化(源路径)
        目标目录 = 路径类.规范化(目标目录)
        源路径_真实 = 路径类.链接_真实路径(源路径)
        目标目录_真实 = 路径类.链接_真实路径(目标目录)
        链接的对象 = 路径类.属性获取_文件名(源路径_真实)
        目标文件名称 = 链接的对象 if 目标文件名称 == "等同于源" else 目标文件名称
        if not 路径类.是否存在(目标目录_真实):
            路径类.新增(目标目录_真实, 路径类型="目录")  # 必须有路径的上级目录，否则跳错
        if 链接类型 == "符号链接":
            if 路径类.是否为目录(源路径_真实):
                return os.symlink(源路径, 路径类.连接(目标目录_真实, 目标文件名称), target_is_directory=True)
            elif 路径类.是否为文件(源路径_真实):
                return os.symlink(源路径, 路径类.连接(目标目录_真实, 目标文件名称), target_is_directory=False)
        elif 链接类型 == "硬链接":
            if 路径类.是否为目录(源路径_真实):
                # print("无法对目录创建硬链接")
                print(f"无法对{源路径_真实}创建硬链接，因为源路径是目录")
            elif 路径类.是否为文件(源路径_真实):
                return os.link(源路径, 路径类.连接(目标目录_真实, 目标文件名称))
        elif 链接类型 == "目录连接点":
            if 路径类.是否为目录(源路径_真实):
                需运行的字符串 = ["mklink", "/J", 路径类.连接(目标目录_真实, 目标文件名称), 源路径]
                子进程 = 子进程类.子进程创建(需运行的字符串, 编码="gbk")
                消息 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
            elif 路径类.是否为文件(源路径_真实):
                print(f"无法对{源路径_真实}创建目录连接点，因为源路径是文件")
                # print("无法对文件创建目录连接点")
        if not 路径类.是否存在(路径类.连接(目标目录_真实, 目标文件名称)):
            print(f"从{源路径_真实}链接到{目标目录_真实}失败")
            return False
        else:
            日志类.输出调试(f"从{源路径_真实}链接到{目标目录_真实}成功")
            return True

    @staticmethod
    def 链接_真实路径(链接路径):
        链接路径 = 路径类.规范化(链接路径)
        return os.path.realpath(链接路径)

    @staticmethod
    def 规范化(x, 转换大小写: Literal["小写", "大写", "首字母大写", "每个单词首字母大写", "windows则小写", None] = None, 转换斜杠: Literal["跟随系统", "反斜杠", "斜杠", None] = "跟随系统", 删除末尾的路径分隔符=True) -> str:
        """

        :param 删除末尾的路径分隔符:
        :param 待转换路径:
        :param 转换大小写:
        :param 转换斜杠:
        :return:
        :test:路径.规范化('c:\\abCc\\abCc/啊啊啊\\', 转换大小写='每个单词首字母大写', 转换斜杠='反斜杠', 删除末尾的路径分隔符=True)
        """
        # os.path.normcase(待转换路径)
        # print(f"-------------------待转换路径{待转换路径}")
        import os

        if x is None:
            return ""

        if 转换大小写 in ["小写", "大写", "首字母大写", "每个单词首字母大写"]:
            from bxpy.基本对象包 import 字类

            临时路径 = 字类.格式_大小写(x, 转换大小写)  # type: ignore
        elif 转换大小写 in ["windows则小写"] and os.name == "nt":
            # 临时路径_真实 = os.path.realpath(临时路径)
            # if 临时路径_真实.upper() == 临时路径.upper():
            临时路径 = x.lower()
        else:
            临时路径 = x
        if 转换斜杠 == "跟随系统":
            转换斜杠 = "斜杠" if os.path.sep == "/" else "反斜杠"
        if 转换斜杠 == "反斜杠":
            临时路径 = 临时路径.replace("/", "\\")  # type: ignore
        elif 转换斜杠 == "斜杠":
            临时路径 = 临时路径.replace("\\", "/")  # type: ignore
        else:
            临时路径 = 临时路径
        if 删除末尾的路径分隔符 and len(临时路径) > 0:
            while 临时路径[-1] == os.path.sep:  # type: ignore
                临时路径 = 临时路径[0:-1:1]  # type: ignore

        # print(f"-------------------临时路径{临时路径}")

        return 临时路径  # type: ignore

    @staticmethod
    def 是否相等(源路径, 目标路径):
        源路径 = 路径类.规范化(源路径, 转换大小写="windows则小写")
        目标路径 = 路径类.规范化(目标路径, 转换大小写="windows则小写")
        return 源路径 == 目标路径

    @staticmethod
    def 是否存在(源路径, 链接处理方式: Literal["保持原样", "向下探索"] = "向下探索"):
        源路径 = 路径类.规范化(源路径)
        源路径_临时改名 = 源路径 + "_临时改名"
        if 链接处理方式 == "保持原样":
            try:
                os.rename(源路径, 源路径_临时改名)
                os.rename(源路径_临时改名, 源路径)
                return True
            except:
                return False
            # if 路径类.是否为链接(源路径):
            #     return True
            # else:
            #     return os.path.exists(源路径)
        elif 链接处理方式 == "向下探索":
            return os.path.exists(源路径)

    @staticmethod
    def 是否为文件(源路径):
        """

        :param 源路径:
        :return:
        :test:路径.是否为文件('H:\\Beixiao\\Database\\4.资料\\H杭州市钱塘区城镇社区建设专项规划')
        :test:路径.是否为文件('C:\\Users\\beixiao\\Project\\AAE学习')
        :test:路径.是否为文件('C:\\Users\\beixiao\\Sync\\010.共享盘\\Database\\2.法规\\F富阳区建设用地选址论证工作流程与要求.pdf')
        """
        源路径 = 路径类.规范化(源路径)
        if 路径类.是否为链接(源路径):
            return False
        else:
            return os.path.isfile(源路径)

    @staticmethod
    def 是否为目录(源路径):
        """

        :param 源路径:
        :return:
        :test:路径.是否为目录('C:\\Users\\beixiao\\Project\\AAE学习')
        :test:路径.是否为目录('C:\\Users\\beixiao\\Sync\\010.共享盘\\Database\\2.法规\\F富阳区建设用地选址论证工作流程与要求.pdf')
        :test:路径.是否为目录('C:\\Users\\Beixiao\\Sync\\010.共享盘\\Database\\4.资料\\H杭州市钱塘区城镇社区建设专项规划')
        """
        源路径 = 路径类.规范化(源路径)
        if 路径类.是否为链接(源路径):
            return False
        else:
            return os.path.isdir(源路径)

    @staticmethod
    def 是否为链接(源路径):
        """

        :param 源路径:
        :return:
        :test:路径.是否为链接('H:\\Beixiao\\Database\\4.资料\\H杭州市钱塘区城镇社区建设专项规划')
        :test:路径.是否为链接('C:\\Users\\beixiao\\Project\\AAE学习')
        :test:路径.是否为链接('C:\\Users\\beixiao\\Sync\\010.共享盘\\Database\\2.法规\\F富阳区建设用地选址论证工作流程与要求.pdf')
        """
        源路径 = 路径类.规范化(源路径)
        if os.name == "nt" and os.path.islink(源路径):
            return True
        elif os.name == "nt" and os.path.islink(源路径) is False:
            try:
                from bxpy.基本对象包 import 模块加载

                模块加载("win32api")
                import win32api

                attr = win32api.GetFileAttributes(源路径)
                # attributes = os.stat(源路径).st_file_attributes
                # print(attr)
                return (attr & 1024) == 1024
            except Exception:
                return False
        else:
            return os.path.islink(源路径)
        # 源路径_临时改名 = 源路径 + "_临时改名"
        # 源路径_真实 = 路径类.规范化(路径类.链接_真实路径(源路径))
        # try:
        #     os.rename(源路径, 源路径_临时改名)
        #     os.rename(源路径_临时改名, 源路径)
        # except:
        #     return False
        # if 源路径 != 源路径_真实:
        #     return True
        # else:
        #     return os.path.islink(源路径)

    @staticmethod
    def 是否为符号链接(源路径):
        源路径 = 路径类.规范化(源路径)
        try:
            return os.path.islink(源路径)
        except Exception:
            return False

    @staticmethod
    def 是否为目录连接点(源路径):
        源路径 = 路径类.规范化(源路径)
        try:
            if os.name != "nt":
                return False
            from bxpy.基本对象包 import 模块加载

            模块加载("win32api", "pywin32")
            import win32api

            attr = win32api.GetFileAttributes(源路径)
            # attributes = os.stat(源路径).st_file_attributes
            # print(attr)
            是否是链接 = (attr & 1024) == 1024
            if 是否是链接 and os.path.islink(源路径) is False:
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def 是否为绝对路径(源路径):
        源路径 = 路径类.规范化(源路径)
        return os.path.isabs(源路径)

    @staticmethod
    def 子路径(源路径, 单一层次=True, 链接处理方式="保持原样", 返回形式: Literal["字典", "列表", "生成器"] = "列表") -> list:
        """

        :param 源路径:
        :param 单一层次:
        :param 链接处理方式:保持原样||向下探索||忽略
        :return:返回列表，列表里每个元素是元祖，元祖有3个元素，分别是：当前的子路径, 子路径下文件夹，子路径下文件
        :task:需要梳理清楚junc和sym在非单一层次下的处理逻辑，包括link的对象不存在和存在的两种情况

        >>> aa = 路径.子路径(r"C:\\Users")
        >>> 'All Users' in aa[1]
        True
        """
        源路径 = 路径类.规范化(源路径)
        路径列表 = []
        if 单一层次:
            子路径中的文件 = []
            子路径中的目录 = []
            for i in os.listdir(源路径):
                if 路径类.是否为目录(路径类.链接_真实路径(路径类.连接(源路径, i))):
                    子路径中的目录.append(i)
                elif 路径类.是否为文件(路径类.链接_真实路径(路径类.连接(源路径, i))):
                    子路径中的文件.append(i)
            if 返回形式 == "字典":
                return {"路径": 源路径, "目录": 子路径中的目录, "文件": 子路径中的文件}  # type: ignore
            return [源路径, 子路径中的目录, 子路径中的文件]
        else:
            if 链接处理方式 == "向下探索":
                路径列表 = os.walk(源路径, followlinks=True)
            else:
                路径列表 = os.walk(源路径, followlinks=False)
            if 返回形式 == "字典":
                return [{"路径": 路径, "目录": 目录, "文件": 文件} for 路径, 目录, 文件 in 路径列表]
            elif 返回形式 == "列表":
                return list(路径列表)
            else:
                return 路径列表  # type: ignore

    @staticmethod
    def 转绝对(待转换路径, 基点路径):
        from bxpy.系统包 import 系统类

        待转换路径 = 路径类.规范化(待转换路径)
        基点路径 = 路径类.规范化(基点路径)
        当前工作目录 = 系统类.属性获取_当前工作目录()
        系统类.属性设置_当前工作目录(基点路径)
        转换后路径 = os.path.abspath(待转换路径)
        系统类.属性设置_当前工作目录(当前工作目录)
        return 路径类.规范化(转换后路径)

    @staticmethod
    def 转相对(待转换路径, 基点路径):
        待转换路径 = 路径类.规范化(待转换路径)
        基点路径 = 路径类.规范化(基点路径)
        return os.path.relpath(待转换路径, 基点路径)


# class 文件:
#     @staticmethod
#     def txt_写入(路径x, 内容):
#         with open(路径x, "w", encoding="utf-8") as f:
#             ret = f.write(内容)
#         return ret

#     @staticmethod
#     def txt_读取(路径x, 编码格式="utf-8"):
#         with open(路径x, "r", encoding=编码格式) as f:
#             ret = f.readlines()
#         return ret

#     @staticmethod
#     def json_写入(json数据, 路径, 编码格式="utf-8", 缩进=4):
#         import json

#         return json.dump(json数据, open(路径, "w", encoding=编码格式), ensure_ascii=False, indent=缩进)

#     @staticmethod
#     def json_读取(路径x, 编码格式="utf-8"):
#         import json

#         return json.load(open(路径x, "r", encoding=编码格式))


# class 右下角提醒:
#     __single = None
#     __firstinit = False
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.__single:
#             cls.__single = super().__new__(cls)
#         return cls.__single
#
#     def __init__(self):
#         if not 右下角提醒.__firstinit:
#             # 注册一个窗口类
#             wc = win32gui.WNDCLASS()
#             hinst = wc.hInstance = win32gui.GetModuleHandle(None)
#             wc.lpszClassName = "PythonTaskbarDemo"
#             wc.lpfnWndProc = {win32con.WM_DESTROY: self.当删除时, }
#             classAtom = win32gui.RegisterClass(wc)
#             style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
#             self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
#                                               0, 0, win32con.CW_USEDEFAULT,
#                                               win32con.CW_USEDEFAULT,
#                                               0, 0, hinst, None)
#             hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
#             nid = (self.hwnd, 0, win32gui.NIF_ICON,
#                    win32con.WM_USER + 20, hicon, "Demo")
#             win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
#             右下角提醒.__firstinit = True
#
#     def 显示信息(self, title, msg):
#         # 原作者使用Shell_NotifyIconA方法代替包装后的Shell_NotifyIcon方法
#         # 据称是不能win32gui structure, 我稀里糊涂搞出来了.
#         # 具体对比原代码.
#         nid = (self.hwnd,  # 句柄
#                0,  # 托盘图标ID
#                win32gui.NIF_INFO,  # 标识
#                0,  # 回调消息ID
#                0,  # 托盘图标句柄
#                "TestMessage",  # 图标字符串
#                msg,  # 气球提示字符串
#                5,  # 提示的显示时间
#                title,  # 提示标题
#                win32gui.NIIF_INFO  # 提示用到的图标
#                )
#         win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
#         # time.sleep(2)
#         # win32gui.DestroyWindow(self.hwnd)
#
#     def 当删除时(self, hwnd, msg, wparam, lparam):
#         nid = (self.hwnd, 0)
#         win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
#         win32gui.PostQuitMessage(0)  # Terminate the app.
class 路径监视类:
    # class 枚举类:
    #     import watchdog

    #     修改事件 = watchdog.events.EVENT_TYPE_MODIFIED  # type: ignore

    @staticmethod
    def 处理器创建(
        包含路径列表=["*.txt", "*.md", "README.*"],
        排除路径列表=[".git/*", "*.tmp", "cache/*", "*.log"],
        是否忽略目录监控=False,
        是否大小写区分=False,
    ):
        from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler

        处理器实例 = PatternMatchingEventHandler(patterns=包含路径列表, ignore_patterns=排除路径列表, ignore_directories=是否忽略目录监控, case_sensitive=是否大小写区分)
        return 处理器实例

    @staticmethod
    def 处理器事件回调函数绑定_修改事件(处理器, 回调函数):
        处理器.on_modified = 回调函数

    @staticmethod
    def 处理器事件回调函数绑定_创建事件(处理器, 回调函数):
        处理器.on_created = 回调函数

    @staticmethod
    def 处理器事件回调函数绑定_删除事件(处理器, 回调函数):
        处理器.on_deleted = 回调函数

    @staticmethod
    def 处理器事件回调函数绑定_移动事件(处理器, 回调函数):
        处理器.on_moved = 回调函数

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件类型(事件参数1):
        return 事件参数1.event_type

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件路径是否为目录(事件参数1):
        return 事件参数1.is_directory

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件发生时路径(事件参数1):
        return 事件参数1.src_path

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件发生后路径(事件参数1):
        # 在重命名或移动操作中，表示目标文件或目录的路径（仅适用于如FileMovedEvent这样的特定事件类型）
        return 事件参数1.dest_path

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件发生时间戳(事件参数1):
        return 事件参数1.timestamp

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件路径容量(事件参数1):
        return 事件参数1.file_size

    @staticmethod
    def 处理器事件回调函数参数1_属性获取_事件路径是否为符号链接(事件参数1):
        return 事件参数1.is_symlink

    @staticmethod
    def 触发器创建():
        from watchdog.observers import Observer

        return Observer()

    @staticmethod
    def 触发器挂载处理器(触发器, 处理器, 监视路径列表, 是否递归=True):
        for 监视路径x in 监视路径列表:
            触发器.schedule(处理器, 监视路径x, recursive=是否递归)
        return 触发器

    @staticmethod
    def 触发器创建并挂载处理器(处理器, 监视路径列表, 是否递归=True):
        from watchdog.observers import Observer

        触发器 = Observer()
        for 监视路径x in 监视路径列表:
            触发器.schedule(处理器, 监视路径x, recursive=是否递归)
        return 触发器

    @staticmethod
    def 触发器启动(触发器):
        return 触发器.start()

    @staticmethod
    def 触发器停止(触发器):
        return 触发器.stop()

    @staticmethod
    def 触发器阻塞主程序(触发器):
        return 触发器.join()


if __name__ == "__main__":
    # 路径 = r"C:\Users\beixiao\Desktop\X下沙中心区单元JS0403-26地块_成果_22.07.10_送审稿.pdf"
    print(路径类.是否存在(r"C:\Users\beixiao\Project\appBXRoot\bxroot-flask-server\log\debug.log"))
    # print(路径类.属性获取_扩展名(路径))
    # print(路径类.属性获取_容量(路径))
    # print(路径类.属性获取_md5(路径))
    # print(路径类.属性获取_容量(r"C"))
    # print(路径类.属性获取_容量(r"C"))
    # print(路径类.属性获取_文件所在路径())
    # print(路径类.连接(r"C:\\", r"Users\beixiao\Project\T桃源单元土储七块地"))
    # print(路径类.是否为链接(r"C:\Users\beixiao\Project\F富阳受降控规"))
    # print(路径类.是否为链接(r"C:\Users\beixiao\Project\aaatest"))
    # print(路径类.是否为链接(r"C:\Users\beixiao\Project\aaatest1"))
    # print(路径类.是否为链接(r"C:\Users\beixiao\Project\aaatest2"))
    # print(路径类.是否为链接(r"C:\Users\beixiao\Project\aaatest3"))
    # print(路径类.属性获取_类型(r"C:\Users\beixiao\Project\AAAtest"))
    # print(os.path.islink(r"C:\Users\beixiao\Project\AAAtest3"))
    # print(路径类.规范化(r"C:\Users\beixiao\Project\AAAtest"))
    # from bxpy.测试包 import 测试类

    # 测试类.测试启动_doctest()
    pass
