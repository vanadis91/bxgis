# *-* coding:utf8 *-*

import os
import sys
from typing import Literal

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


class 系统类:
    @staticmethod
    def 程序退出():
        os._exit(0)

    @staticmethod
    def 属性获取_网卡情况() -> list:
        # [
        #     {"网卡状态": "Enabled", "网络状态": "Connected", "网络类型": "Dedicated", "网络名称": "ZeroTier One [41d49af6c2378696]"},
        #     {"网卡状态": "Disabled", "网络状态": "Disconnected", "网络类型": "Dedicated", "网络名称": "VMware Network Adapter VMnet1"},
        #     {"网卡状态": "Disabled", "网络状态": "Disconnected", "网络类型": "Dedicated", "网络名称": "VMware Network Adapter VMnet8"},
        #     {"网卡状态": "Enabled", "网络状态": "Connected", "网络类型": "Dedicated", "网络名称": "以太网"},
        #     {"网卡状态": "Enabled", "网络状态": "Connected", "网络类型": "Dedicated", "网络名称": "vEthernet (Default Switch)"},
        # ]
        from bxpy.进程包 import 子进程类

        进程 = 子进程类.子进程创建("netsh interface show interface")
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(进程)
        输出 = 输出.split("\n")  # type: ignore
        输出 = [x for x in 输出 if x.strip().startswith("Enabled") or x.strip().startswith("Disabled") or x.strip().startswith("已启用") or x.strip().startswith("已禁用")]
        日志类.输出调试(输出)
        输出temp = []
        for x in 输出:
            x1 = x.split(" ")
            x1 = [x for x in x1 if x != ""]
            日志类.输出调试(x1)
            网卡状态 = "Enabled" if x1[0] in ["Enabled", "已启用"] else "Disabled"
            网络状态 = "Connected" if x1[1] in ["Connected", "已连接"] else "Disconnected"
            网络类型 = "Dedicated" if x1[2] in ["Dedicated", "专用"] else "Unknown"
            网络名称 = " ".join(x1[3:])
            构造后数据 = {
                "网卡状态": 网卡状态,
                "网络状态": 网络状态,
                "网络类型": 网络类型,
                "网络名称": 网络名称,
            }
            输出temp.append(构造后数据)
        输出 = 输出temp
        return 输出

    @staticmethod
    def 网卡禁用(网络名称="以太网"):
        from bxpy.进程包 import 子进程类

        cli = f'netsh interface set interface "{网络名称}" admin=disable'
        日志类.输出调试(f"禁用网卡的命令：{cli}")
        子进程 = 子进程类.子进程创建(cli)
        内容 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
        if 子进程类.属性获取_退出状态码(子进程) != 0:
            print(内容)

    @staticmethod
    def 网卡启用(网络名称="以太网"):
        from bxpy.进程包 import 子进程类

        cli = f'netsh interface set interface "{网络名称}" admin=enable'
        日志类.输出调试(f"启用网卡的命令：{cli}")
        进程 = 子进程类.子进程创建(cli)
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(进程)
        if 子进程类.属性获取_退出状态码(进程) != 0:
            print(输出)

    @staticmethod
    def 网络是否畅通(host="1.1.1.1", port=80, timeout=3):
        import socket

        try:
            # 创建一个socket对象
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置超时
            sock.settimeout(timeout)
            # 尝试连接
            sock.connect((host, port))
            # 连接成功后关闭socket
            sock.close()
            return True
        except socket.error as e:
            # print(f"网络连接检测失败: {e}")
            return False

    @staticmethod
    def 属性获取_网络情况() -> list:
        # [
        #     {"网络名称": "ZeroTier One [41d49af6c2378696]", "DHCP": "No", "IP": "172.25.0.100", "子网前缀": "172.25.0.0/16", "子网掩码": "255.255.0.0", "默认网关": "25.255.255.254", "网关跃点数": "9999"},
        #     {"网络名称": "以太网", "DHCP": "Yes", "IP": "192.168.31.110", "子网前缀": "192.168.31.0/24", "子网掩码": "255.255.255.0", "默认网关": "192.168.31.201", "网关跃点数": "2"},
        #     {"网络名称": "蓝牙网络连接 2", "DHCP": "Yes"},
        #     {"网络名称": "Loopback Pseudo-Interface 1", "DHCP": "No", "IP": "127.0.0.1", "子网前缀": "127.0.0.0/8", "子网掩码": "255.0.0.0"},
        #     {"网络名称": "vEthernet (Default Switch)", "DHCP": "No", "IP": "172.31.240.1", "子网前缀": "172.31.240.0/20", "子网掩码": "255.255.240.0"},
        # ]
        from bxpy.进程包 import 子进程类

        进程 = 子进程类.子进程创建("netsh interface ip show address")
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(进程)
        输出 = 输出.split("\n")  # type: ignore
        输出temp = []
        网络对象 = {}
        for x in 输出:
            if "接口" in x or "Configuration" in x:
                if 网络对象 != {}:
                    输出temp.append(网络对象)
                网络对象 = {}
                网络对象["网络名称"] = x.split('"')[1]
            if "DHCP" in x:
                内容 = x.split(":")[1].strip()
                内容 = "Yes" if 内容 in ["是", "Yes"] else "No"
                网络对象["DHCP"] = 内容
            if "IP" in x:
                内容 = x.split(":")[1].strip()
                网络对象["IP"] = 内容
            if "子网前缀" in x or "Subnet Prefix" in x:
                网络对象["子网前缀"] = x.split(":")[1].split("(")[0].strip()
            if "子网掩码" in x:
                网络对象["子网掩码"] = x.split("掩码")[1].strip()[:-1]
            elif "掩码" in x:
                网络对象["子网掩码"] = x.split("掩码")[1].strip()[:-1]
            elif "mask" in x:
                网络对象["子网掩码"] = x.split("mask")[1].strip()[:-1]
            if "默认网关" in x or "Default Gateway" in x:
                网络对象["默认网关"] = x.split(":")[1].strip()
            if "网关跃点数" in x or "Gateway Metric" in x:
                网络对象["网关跃点数"] = x.split(":")[1].strip()
        输出temp.append(网络对象)
        输出 = 输出temp
        return 输出

    @staticmethod
    def 属性获取_进程情况(包含的属性列表=["pid", "name"], 返回形式: Literal["列表", "生成器"] = "列表"):
        import psutil

        if 返回形式 == "列表":
            return [process.info for process in psutil.process_iter(包含的属性列表)]  # type: ignore
        else:
            psutil.process_iter(包含的属性列表)

    @staticmethod
    def 属性获取_卷情况() -> list:
        """

        >>> 路径.盘符获取()[0]
        {'盘符': 'C:\\\\', '文件类型': 'NTFS'}
        """
        import psutil

        partitions = psutil.disk_partitions(all=True)
        ret = [{"盘符": partition.device, "文件类型": partition.fstype} for partition in partitions]
        from bxpy.进程包 import 子进程类

        子进程 = 子进程类.子进程创建("diskpart", 编码="gbk")
        子进程类.交互_输入(子进程, "list volume")
        子进程类.交互_输入(子进程, "exit")
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
        输出 = [x.strip() for x in 输出.split("\n") if (x.strip().startswith("Volume") and not x.strip().startswith("Volume ###"))]  # type: ignore
        输出 = [[y.strip() for y in x.split("  ") if y != ""] for x in 输出]
        for x in ret:
            for y in 输出:
                if x["盘符"][0:1] in y:
                    x["卷号"] = y[0].split(" ")[-1]
                    break
        return ret

    @staticmethod
    def 卷盘符删除(盘符="E:\\"):
        from bxpy.进程包 import 子进程类

        卷信息 = 系统类.属性获取_卷情况()
        try:
            卷号 = [x for x in 卷信息 if x["盘符"] == 盘符][0]["卷号"]
        except Exception as e:
            raise Exception(f"没有找到{盘符}的卷号")
        子进程 = 子进程类.子进程创建("diskpart")
        子进程类.交互_输入(子进程, f"select volume {盘符[0:1]}")
        子进程类.交互_输入(子进程, f"remove letter={盘符[0:1]}")
        子进程类.交互_输入(子进程, "exit")
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
        print(输出)
        return 卷号

    @staticmethod
    def 卷盘符添加(卷号="10", 盘符="E:\\"):
        from bxpy.进程包 import 子进程类

        子进程 = 子进程类.子进程创建("diskpart", 是否通过终端运行=False)
        子进程类.交互_输入(子进程, f"select volume {卷号}")
        子进程类.交互_输入(子进程, f"assign letter={盘符[0:1]}")
        子进程类.交互_输入(子进程, "exit")
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
        return 输出

    @staticmethod
    def 属性获取_磁盘情况():
        from bxpy.进程包 import 子进程类

        进程 = 子进程类.子进程创建("wmic DISKDRIVE GET Name, InterfaceType, MediaType, Model, PNPDeviceID, SerialNumber, Size")
        输出 = 子进程类.交互_输入关闭等待结束并输出获取(进程)
        输出 = 输出.split("\n")  # type: ignore
        输出 = [x for x in 输出 if "PHYSICALDRIVE" in x]
        输出 = [[y for y in x.split("  ") if y != ""] for x in 输出]
        输出temp = []
        for x in 输出:
            构造后数据 = {
                "接口类型": x[0],  # USB SCSI IDE
                "介质类型": x[1],
                # Removable Media
                # External hard disk media
                # Fixed hard disk media
                "介质名称": x[2],
                # Kingston DataTraveler 3.0 USB Device
                # WDC WD40 EZRZ-00GXCB0 SCSI Disk Device
                # External USB3.0 SCSI Disk Device
                # KINGSTON SA400S37480G
                # External USB3.0 SCSI Disk Device
                # WDC WD10EADX-00TDHB0
                # WDC WD40 EZRZ-00GXCB0 SCSI Disk Device
                "驱动ID": x[4],
                # USBSTOR\DISK&VEN_KINGSTON&PROD_DATATRAVELER_3.0&REV_0000\E0D55E6CE7A71620A85605E8&0
                # SCSI\DISK&VEN_WDC_WD40&PROD_EZRZ-00GXCB0\8&EB13AAF&0&000000
                # SCSI\DISK&VEN_WDC_WD20&PROD_EZRX-00D8PB0\8&233294AD&0&000000
                # SCSI\DISK&VEN_WDC_WD40&PROD_EZAX-00C8UB0\8&240CC9D&0&000000
                # SCSI\DISK&VEN_EXTERNAL&PROD_USB3.0\6&28C9CAD&0&000001
                # SCSI\DISK&VEN_&PROD_KINGSTON_SA400S3\4&7042F81&0&000000
                # SCSI\DISK&VEN_EXTERNAL&PROD_USB3.0\6&28C9CAD&0&000000
                # SCSI\DISK&VEN_WDC&PROD_WD10EADX-00TDHB0\4&7042F81&0&010000
                # SCSI\DISK&VEN_WDC_WD40&PROD_EZRZ-00GXCB0\8&1078E408&0&000000
                "序列号": x[5],
                # 0000000005
                # 000000004BA8
                # 000000004BA8
                # 000000004BA8
                # DD564198838B4
                # 50026B7682E28FE4
                # DD564198838B4
                # WD-WCAV5N402766
                # 000000004BA8
                "容量": x[6],
                # 30992855040
                # 4000784417280
            }
            输出temp.append(构造后数据)
        输出 = 输出temp
        return 输出

    @staticmethod
    def 属性获取_当前工作目录():
        return os.getcwd()

    @staticmethod
    def 属性设置_当前工作目录(源路径):
        return os.chdir(源路径)

    @staticmethod
    def 属性获取_当前进程参数():
        return sys.argv

    @staticmethod
    def 属性获取_当前进程路径():
        """获取当前可执行文件所在的目录"""
        return sys.executable

    @staticmethod
    def 属性获取_当前进程是否冻结():
        return getattr(sys, "frozen", False)

    @staticmethod
    def 属性获取_环境变量(变量名):
        return os.getenv(变量名)

    @staticmethod
    def 属性设置_环境变量(变量名, 值):
        return os.putenv(变量名, 值)

    @staticmethod
    def 属性获取_特殊路径(名称: Literal["桌面"]):
        import os

        if 名称 == "桌面":
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return False

    @staticmethod
    def 属性获取_换行符():
        return os.linesep

    @staticmethod
    def 属性获取_分隔符():
        return os.sep

    @staticmethod
    def 属性获取_操作系统():
        return os.name

    @staticmethod
    def 属性获取_计算机名称():
        import socket

        return socket.gethostname()

    @staticmethod
    def 属性获取_默认输出流():
        import sys

        return sys.stdout

    @staticmethod
    def 属性设置_默认输出流(StringIO对象):
        import sys

        sys.stdout = StringIO对象

    @staticmethod
    def 属性获取_计算机唯一标识():
        """
        >>> print(环境变量.计算机唯一标识)
        4CCC6A8F5AC3-GA16021772
        """
        # import uuid
        import psutil
        from bxpy.进程包 import 子进程类

        try:
            子进程 = 子进程类.子进程创建("wmic baseboard get serialnumber")
            主板序列号 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
            主板序列号 = 主板序列号.split("\n")[2].strip()  # type: ignore
        except Exception as e:
            主板序列号 = "0000000000"
        if 主板序列号 in [None, ""]:
            主板序列号 = "0000000000"
        主板序列号 = 主板序列号.replace("/", "")

        try:
            interfaces = psutil.net_if_addrs()
            for interface in interfaces:
                if interfaces[interface][0].family == psutil.AF_LINK:
                    网卡物理地址 = interfaces[interface][0].address
                    break
        except Exception as e:
            网卡物理地址 = "000000000000"
        if 网卡物理地址 in [None, ""]:
            网卡物理地址 = "0000000000"
        网卡物理地址 = 网卡物理地址.replace("-", "")

        try:
            子进程 = 子进程类.子进程创建("wmic diskdrive where index=0 get SerialNumber")
            磁盘序列号 = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
            磁盘序列号 = 磁盘序列号.split("\n")[1].strip()  # type: ignore
        except Exception as e:
            磁盘序列号 = "0000000000"
        if 磁盘序列号 in [None, ""]:
            磁盘序列号 = "0000000000"
        磁盘序列号 = 磁盘序列号.replace("/", "")

        return 网卡物理地址 + "-" + 主板序列号 + "-" + 磁盘序列号

    # @staticmethod
    # def 运行(输入内容):
    #     a = 'chcp 65001 && ' + 输入内容
    #     os.system(a)
    #     # os.system('chcp 936')
    #     # os.system('chcp 65001 && ping www.baidu.com')


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
    # print(系统类.卷盘符删除("E:\\"))
    # print(系统类.卷盘符添加("10", "E:\\"))
    print(系统类.网络是否畅通())
