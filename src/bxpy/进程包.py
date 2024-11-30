# *-* coding:utf8 *-*
import subprocess
from typing import Union, Literal

import threading as td
import multiprocessing as mp
import concurrent.futures

# import psutil
# from pathlib import Path
# from bxpy import 字
from bxpy.日志包 import 日志类
from bxpy.时间包 import 时间类


class 子进程类:
    @staticmethod
    def 子进程创建(要执行的进程, 输入=subprocess.PIPE, 输出=subprocess.PIPE, 跳错=subprocess.PIPE, 是否通过终端运行=True, 编码="utf-8", 配置: Literal[0, "创建新控制台来运行子进程", "子进程不打开任何窗口"] = 0, 作为新的主进程运行=False):
        """

        :param 要执行的命令: 可以用字符串或者命令序列，如果用字符串则必须将 通过终端运行 改为True
        :param 输入:
        :param 输出:其值可以是subprocess.PIPE、subprocess.DEVNULL、一个已经存在的文件描述符、已经打开的文件对象或者None
        :param 跳错:
        :param 是否通过终端运行:
        :param 编码:
        :return:
        :test:
        """
        # proc = subprocess.run(要执行的命令, stdin=输入, stdout=输出, stderr=跳错, shell=是否通过终端运行, encoding=编码)
        if 是否通过终端运行 and type(要执行的进程) is str and 编码 == "utf-8":
            要执行的进程 = "chcp 65001 && " + 要执行的进程
        elif 是否通过终端运行 and type(要执行的进程) is not str and 编码 == "utf-8":
            转换编码 = ["chcp", "65001", "&&"]
            转换编码.extend(要执行的进程)
            要执行的进程 = 转换编码
        elif 是否通过终端运行 and 编码 == "gbk":
            要执行的进程 = 要执行的进程
        if 配置 == "创建新控制台来运行子进程":
            配置 = subprocess.CREATE_NEW_CONSOLE  # type: ignore
        elif 配置 == "子进程不打开任何窗口":
            配置 = subprocess.CREATE_NO_WINDOW  # type: ignore
        proc = subprocess.Popen(要执行的进程, stdin=输入, stdout=输出, stderr=跳错, shell=是否通过终端运行, encoding=编码, creationflags=配置, start_new_session=作为新的主进程运行)  # type: ignore
        # f = subprocess.check_output(要执行的命令, shell=是否通过终端运行)
        # t = f.decode(encoding='gbk')
        # print(t)
        # print(f'结果：{stdout_value[0]}，错误：{stdout_value[1]}')
        # print('ret.returncode: ', ret.returncode)
        # print('ret.stdout: ', ret.stdout)
        return proc

    @staticmethod
    def 子进程终止(子进程: subprocess.Popen):
        return 子进程.kill()  # type: ignore

    @staticmethod
    def 交互_输入(子进程: subprocess.Popen, 内容: str):
        try:
            子进程.stdin.write(内容 + "\n")  # type: ignore
        except Exception as e:
            print(e)
            子进程.stdin.write(内容.encode() + b"\n")  # type: ignore
        return 子进程.stdin.flush()  # type: ignore

    @staticmethod
    def 交互_输入关闭(子进程: subprocess.Popen):
        return 子进程.stdin.close()  # type: ignore

    @staticmethod
    def 交互_输入关闭等待结束并输出获取(子进程: subprocess.Popen, 输入=None, 超时=None, 输出形式: Literal["合并为字符串", "合并为列表"] = "合并为字符串"):
        内容 = 子进程.communicate(input=输入, timeout=超时)  # type: ignore
        输出内容 = str(内容[0]).strip()
        错误内容 = str(内容[1]).strip()
        if 输出形式 == "合并为字符串":
            内容 = ""
            if 输出内容 not in [None, "", " "]:
                内容 = 内容 + 输出内容
            if 错误内容 not in [None, "", " "] and 内容 in [None, "", " "]:
                内容 = 内容 + 错误内容
            elif 错误内容 not in [None, "", " "] and 内容 not in [None, "", " "]:
                内容 = 内容 + "\n" + 错误内容
            return 内容
        elif 输出形式 == "合并为列表":
            内容 = [输出内容, 错误内容]
            return 内容

    @staticmethod
    def 交互_信号发送(子进程: subprocess.Popen, 信号):
        return 子进程.send_signal(信号)  # type: ignore

    @staticmethod
    def 等待结束(子进程: subprocess.Popen):
        return 子进程.wait()  # type: ignore

    @staticmethod
    def 输出显示_阻塞_逐行(子进程: subprocess.Popen):
        def read_stdout():
            for line in iter(子进程.stdout.readline, ""):  # type: ignore
                if line not in ["", b"", None, " "]:
                    print(line.strip())
                # if 子进程.poll() is not None:
                #     break
                # stdout_buffer.append(line.strip())

        def read_stderr():
            for line in iter(子进程.stderr.readline, ""):  # type: ignore
                if line not in ["", b"", None, " "]:
                    print(line.strip())
                # if 子进程.poll() is not None:
                #     break
                # stderr_buffer.append(line.strip())

        stdout_thread = 多线程类.多线程创建(read_stdout, 是否随主程序结束=True)
        stderr_thread = 多线程类.多线程创建(read_stderr, 是否随主程序结束=True)

        多线程类.运行(stdout_thread)  # type: ignore
        多线程类.运行(stderr_thread)  # type: ignore

        # 检查并打印缓冲区内容
        # while stdout_buffer or stderr_buffer:
        #     if stdout_buffer:
        #         print("标准输出:", stdout_buffer.pop(0))
        #     if stderr_buffer:
        #         print("错误输出:", stderr_buffer.pop(0))

        # 多线程类.阻塞主程序(stdout_thread)  # type: ignore
        # 多线程类.阻塞主程序(stderr_thread)  # type: ignore

        # 检查子进程是否结束
        while True:
            if 子进程.poll() is not None:
                break
            else:
                时间类.等待(0.1)

    @staticmethod
    def 输出显示_非阻塞(子进程: subprocess.Popen):
        def read_stdout():
            for line in iter(子进程.stdout.readline, ""):  # type: ignore
                if line not in ["", b"", None, " "]:
                    print(line.strip())
                # if 子进程.poll() is not None:
                #     break
                # stdout_buffer.append(line.strip())

        def read_stderr():
            for line in iter(子进程.stderr.readline, ""):  # type: ignore
                if line not in ["", b"", None, " "]:
                    print(line.strip())
                # if 子进程.poll() is not None:
                #     break
                # stderr_buffer.append(line.strip())

        stdout_thread = 多线程类.多线程创建(read_stdout)
        stderr_thread = 多线程类.多线程创建(read_stderr)

        多线程类.运行(stdout_thread)  # type: ignore
        多线程类.运行(stderr_thread)  # type: ignore

        # 检查并打印缓冲区内容
        # while stdout_buffer or stderr_buffer:
        #     if stdout_buffer:
        #         print("标准输出:", stdout_buffer.pop(0))
        #     if stderr_buffer:
        #         print("错误输出:", stderr_buffer.pop(0))

        # 多线程类.阻塞主程序(stdout_thread)  # type: ignore
        # 多线程类.阻塞主程序(stderr_thread)  # type: ignore

        # 检查子进程是否结束

    @staticmethod
    def 属性获取_退出状态码(子进程: subprocess.Popen):
        # 0 表示正常完成，其他表示跳错
        return 子进程.returncode  # type: ignore

    @staticmethod
    def 属性获取_状态(子进程: subprocess.Popen):
        # 如果poll函数返回None，表示子进程尚未结束；如果poll函数返回一个整数值，表示子进程已经结束，并且返回的整数值即为子进程的退出状态码。
        return 子进程.poll()  # type: ignore


class 多线程类:
    @staticmethod
    def 多线程创建(子程序, 子程序参数=(), 是否随主程序结束=False):
        ret = td.Thread(target=子程序, args=子程序参数)
        if 是否随主程序结束:
            ret.setDaemon(是否随主程序结束)
        return ret

    @staticmethod
    def 属性获取_当前运行线程列表():
        return td.enumerate()

    @staticmethod
    def 运行(多线程对象: td.Thread):
        return 多线程对象.start()

    @staticmethod
    def 阻塞主程序(多线程对象: td.Thread, 最多阻塞时间=None):
        return 多线程对象.join(最多阻塞时间)


class 多线程池类:
    @staticmethod
    def 多线程池创建():
        return []

    @staticmethod
    def 运行(多线程池对象: list, 子程序, 子程序参数=(), 是否随主程序结束=False):
        """
        :param 子程序:
        :param 子程序参数: 子程序参数如果只有一个需要写成(arg, )
        """
        x = td.Thread(target=子程序, args=子程序参数)
        if 是否随主程序结束:
            x.setDaemon(是否随主程序结束)
        多线程池对象.append(x)
        return x.start()

    @staticmethod
    def 阻塞主程序(多线程池对象: list, 最多阻塞时间=None):
        for x in 多线程池对象:
            x.join(最多阻塞时间)


class 多进程类:
    class 锁类:
        @staticmethod
        def 锁创建():
            return mp.Manager().Lock()

    class 变量类:
        @staticmethod
        def 变量创建(类型, 初始值):
            return mp.Manager().Value(类型, 初始值)

        @staticmethod
        def 变量值获取(变量):
            return 变量.value

        @staticmethod
        def 变量值设置(变量, x):
            变量.value = x

    class 队列类:
        @staticmethod
        def 队列创建():
            return mp.Manager().Queue()

        @staticmethod
        def 放入(队列, 参数):
            return 队列.put(参数)

        @staticmethod
        def 取出(队列):
            return 队列.get()

    @staticmethod
    def 多进程创建(子程序, 子程序参数=()):
        """
        :param 子程序:
        :param 子程序参数: 子程序参数如果只有一个需要写成(arg, )
        """
        return mp.Process(target=子程序, args=子程序参数)

    @staticmethod
    def 运行(多进程对象: mp.Process):
        return 多进程对象.start()

    @staticmethod
    def 阻塞主程序(多进程对象: mp.Process, 最多阻塞时间=None):
        return 多进程对象.join(最多阻塞时间)

    @staticmethod
    def 允许windows进入子进程():
        return mp.freeze_support()


class 多进程池类:
    @staticmethod
    def 多进程池创建(最大数量=None):
        return mp.Pool(processes=最大数量)

    @staticmethod
    def 运行_异步(多进程池对象, 子程序, 子程序参数=(), 子程序回调=None, 跳错回调=None):
        """
        :param 子程序:
        :param 子程序参数: 子程序参数如果只有一个需要写成(arg, )，参数需要从队列中取
        :param 子程序回调:
        :param 跳错回调:
        """
        return 多进程池对象.apply_async(func=子程序, args=子程序参数, callback=子程序回调, error_callback=跳错回调)

    @staticmethod
    def 关闭(多进程池对象):
        return 多进程池对象.close()

    @staticmethod
    def 阻塞主程序(多进程池对象):
        return 多进程池对象.join()


class 并发器:
    @staticmethod
    def 并发器创建(并发类型: Literal["线程", "进程"] = "线程", 最大数量=None):
        if 并发类型 == "线程":
            return concurrent.futures.ThreadPoolExecutor(max_workers=最大数量)
        elif 并发类型 == "进程":
            return concurrent.futures.ProcessPoolExecutor(max_workers=最大数量)

    @staticmethod
    def 运行(并发器对象: Union[concurrent.futures.ThreadPoolExecutor, concurrent.futures.ProcessPoolExecutor], 函数, *值):
        执行结果对象Future = 并发器对象.submit(函数, *值)
        return 执行结果对象Future

    @staticmethod
    def 运行_按顺序(并发器对象: Union[concurrent.futures.ThreadPoolExecutor, concurrent.futures.ProcessPoolExecutor], 函数, *可迭代对象, 等待超时=None, 分段大小=1):
        执行结果对象Future = 并发器对象.map(函数, *可迭代对象, timeout=等待超时, chunksize=分段大小)
        return 执行结果对象Future

    @staticmethod
    def 执行结果获取(执行结果对象Future, 等待超时=None):
        return 执行结果对象Future.result(timeout=等待超时)

    @staticmethod
    def 执行结果取消(执行结果对象Future):
        return 执行结果对象Future.cancel()

    @staticmethod
    def 阻塞主程序(执行结果对象列表FutureList, 等待超时=None, 返回条件="ALL_COMPLETED"):
        已完成执行结果列表, 未完成执行结果列表 = concurrent.futures.wait(执行结果对象列表FutureList, timeout=等待超时, return_when=返回条件)
        return 已完成执行结果列表, 未完成执行结果列表


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

if __name__ == "__main__":
    子进程 = 子进程类.子进程创建("diskpart")
    子进程类.交互_输入(子进程, "list volume")
    # 子进程类.交互_输入(子进程, "select volume E")
    # 子进程类.交互_输入(子进程, "remove letter=E")
    子进程类.交互_输入(子进程, "exit")
    ret = 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    print(ret)
    # subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE) as proc:
    #         for cmd in commands:
    #             proc.stdin.write(cmd.encode() + b"\n")  # type: ignore
    #             proc.stdin.flush()  # type: ignore
    #         proc.stdin.close()  # type: ignore
    #         output, error = proc.communicate()
    #         if proc.returncode != 0:
    #             print(f"Error occurred: {error.decode()}")
    #         else:
    #             print("Drive letter removed successfully.")
