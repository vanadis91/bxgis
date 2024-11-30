import tkinter
from tkinter import messagebox
import tkinterdnd2 as tkdnd
from typing import Union, Literal, Any


class 枚举类:
    class 字符串换行方式:
        不在单词中间换行 = tkinter.WORD

    class 字符串操作:
        末端 = tkinter.END
        最后一行 = "end-1c linestart"

    class 组件布局填充方式:
        沿X和Y轴填充 = tkinter.BOTH
        沿Y轴填充 = tkinter.Y
        沿X轴填充 = tkinter.X

    class 组件位置:
        顶部 = tkinter.TOP
        左侧 = tkinter.LEFT
        右侧 = tkinter.RIGHT
        底部 = tkinter.BOTTOM

    class 边框样式:
        扁平 = tkinter.FLAT
        凸起 = tkinter.RAISED
        凹陷 = tkinter.SUNKEN
        沟槽 = tkinter.GROOVE
        脊 = tkinter.RIDGE


class 界面类:
    @staticmethod
    def 界面创建(标题=None, 尺寸=None):
        # ret = tkinter.Tk()
        ret = tkdnd.TkinterDnD.Tk()
        if 标题:
            ret.title(标题)
        if 尺寸:
            ret.geometry(尺寸)
        return ret

    @staticmethod
    def 属性设置_标题(界面对象, 标题内容):
        return 界面对象.title(标题内容)

    @staticmethod
    def 属性设置_图标(界面对象, 图标路径):
        return 界面对象.iconbitmap(图标路径)

    @staticmethod
    def 属性设置_尺寸(界面对象, 尺寸="300x200"):
        return 界面对象.geometry(尺寸)

    @staticmethod
    def 属性设置_状态(界面对象):
        # "iconic" 代表最小化
        return 界面对象.state()

    @staticmethod
    def 界面隐藏(界面对象):
        return 界面对象.withdraw()

    @staticmethod
    def 界面销毁(界面对象):
        return 界面对象.destroy()

    @staticmethod
    def 界面最小化(界面对象):
        return 界面对象.iconify()

    @staticmethod
    def 界面尺寸锁定(界面对象):
        return 界面对象.resizable(0, 0)

    @staticmethod
    def 系统触发器绑定处理器(界面对象, 触发器: Literal["关闭窗口"], 函数):
        if 触发器 == "关闭窗口":
            触发器raw = "WM_DELETE_WINDOW"
        return 界面对象.protocol(触发器raw, 函数)

    @staticmethod
    def 界面显示(界面对象):
        return 界面对象.deiconify()

    @staticmethod
    def 界面事件循环(界面对象: tkinter.Tk):
        界面对象.mainloop()

    @staticmethod
    def 组件显示(组件对象, 跟随主窗口变化=False, 填充=枚举类.组件布局填充方式.沿X和Y轴填充, 位置=None, 在目标组件前=None, 在目标组件后=None):
        # 枚举类.组件位置.底部
        组件对象.pack(expand=跟随主窗口变化, fill=填充, side=位置, before=在目标组件前, after=在目标组件后)

    @staticmethod
    def 组件隐藏(组件对象):
        组件对象.pack_forget()

    @staticmethod
    def 提示框创建_模态(界面对象, 标题="标题", 内容="这里是提示框的内容"):
        messagebox.showinfo(标题, 内容)

    @staticmethod
    def 提示框创建_模态_win32ui(标题="标题", 内容="这里是提示框的内容"):
        import win32con
        import win32ui  # type: ignore

        result = win32ui.MessageBox(内容, 标题, win32con.MB_OK)
        # print(f"用户点击了按钮: {result}")

    @staticmethod
    def 提示框创建_非模态(标题="标题", 内容="这里是提示框的内容"):
        from tkinter import ttk

        root = tkinter.Tk()
        # root.withdraw()
        root.title(标题)
        root.geometry("+{}+{}".format(100, 100))  # 设置提示框初始位置
        # root.transient(界面对象)  # 设置为父窗口的临时窗口
        # root.grab_set()  # 确保输入聚焦于此窗口，但不阻止与父窗口的交互（非模态的关键）
        label = ttk.Label(root, text=内容)
        label.pack(padx=20, pady=20)
        close_button = ttk.Button(root, text="关闭", command=root.destroy)
        close_button.pack(pady=(0, 10))
        root.mainloop()
        # return root
        # root.deiconify()

    # @staticmethod
    # def 系统托盘图标创建(界面对象, 图标路径="", 名称="name", 标题="title"):
    #     from PIL import Image
    #     import pystray

    #     image = Image.open(图标路径)
    #     menu = (
    #         pystray.MenuItem("打开", lambda icon, item: 界面类.界面显示(界面对象)),
    #         pystray.MenuItem("退出", lambda icon, item: icon.stop()),
    #     )
    #     icon = pystray.Icon(名称, image, 标题, menu)
    #     icon.run()


class 托盘图标类(object):
    def __init__(self, 图标路径, 鼠标悬停提示, 菜单项列表, 回调函数_图标销毁整个程序结束, 回调函数_图标销毁窗口重新出现, 菜单栏是否添加预设退出按钮=True, 不显示的菜单项ID=None, 托盘图标类名称=None):
        import win32api, win32con, win32gui_struct, win32gui

        """
        icon         需要显示的图标文件路径
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: [['a', None, callback], ['b', None, [['b1', None, callback]]]]
        on_quit      传递退出函数，在退出码不是0的退出时，一并运行
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        default_menu_index 不显示的右键菜单序号
        window_class_name  窗口类名
        """
        self.图标路径 = 图标路径
        self.鼠标悬停提示 = 鼠标悬停提示
        self.回调函数_图标销毁整个程序结束 = 回调函数_图标销毁整个程序结束
        self.回调函数_图标销毁窗口重新出现 = 回调函数_图标销毁窗口重新出现
        self.托盘图标实例标识符 = None
        self.提醒消息ID = None

        if 菜单栏是否添加预设退出按钮:
            菜单项列表.append(["退出", None, self.菜单栏预设退出事件回调函数])

        回调函数ID初始值 = 5320
        菜单项ID与回调函数间映射字典 = {}
        self.菜单项列表_添加ID后, 回调函数ID, 菜单项ID与回调函数间映射字典 = self._菜单项增加回调函数ID(
            菜单项列表,
            回调函数ID初始值,
            菜单项ID与回调函数间映射字典,
        )
        self.菜单项回调函数ID字典 = 菜单项ID与回调函数间映射字典
        from bxpy.日志包 import 日志类

        # 日志类.临时开启日志()
        日志类.输出调试(f"菜单项列表_添加ID后：{self.菜单项列表_添加ID后}")
        日志类.输出调试(f"菜单项回调函数ID字典：{self.菜单项回调函数ID字典}")

        self.不显示的菜单项ID = 不显示的菜单项ID or 0
        self.托盘图标类名称 = 托盘图标类名称 or "e6ef93a7-de65-4183-b681-3234e47f2996"

        message_map = {
            win32gui.RegisterWindowMessage("TaskbarCreated"): self.回调函数_图标被创建,
            win32con.WM_DESTROY: self.回调函数_图标被销毁,
            win32con.WM_COMMAND: self.回调函数_菜单项被点击,
            win32con.WM_USER + 20: self.回调函数_图标被点击,
        }

        # 注册窗口类。
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = self.托盘图标类名称
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # 也可以指定wndproc.
        self.托盘图标类 = win32gui.RegisterClass(wc)

    @staticmethod
    def 托盘图标创建(图标路径, 鼠标悬停提示, 菜单项列表, 回调函数_图标销毁整个程序结束, 回调函数_图标销毁窗口重新出现, 菜单栏是否添加预设退出按钮=True, 不显示的菜单项ID=None, 托盘图标类名称=None):
        return 托盘图标类(
            图标路径,
            鼠标悬停提示,
            菜单项列表,
            回调函数_图标销毁整个程序结束,
            回调函数_图标销毁窗口重新出现,
            菜单栏是否添加预设退出按钮,
            不显示的菜单项ID,
            托盘图标类名称,
        )

    def 托盘图标激活(self):
        """激活任务栏图标，不用每次都重新创建新的托盘图标"""
        import win32api, win32con, win32gui_struct, win32gui

        hinst = win32gui.GetModuleHandle(None)  # 创建窗口。
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.托盘图标实例标识符 = win32gui.CreateWindow(self.托盘图标类, self.托盘图标类名称, style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        win32gui.UpdateWindow(self.托盘图标实例标识符)
        self.提醒消息ID = None
        self.托盘图标发送提醒消息(消息标题="软件已最小化到托盘", 消息内容="点击托盘图标重新打开。", 提示显示时间=500)

        win32gui.PumpMessages()

    def 托盘图标发送提醒消息(self, 消息标题="", 消息内容="", 提示显示时间=500):
        """刷新托盘图标
        title 标题
        msg   内容，为空的话就不显示提示
        time  提示显示时间"""
        from bxpy.路径包 import 路径类
        import win32api, win32con, win32gui_struct, win32gui

        hinst = win32gui.GetModuleHandle(None)
        if 路径类.是否为文件(路径类.链接_真实路径(self.图标路径)):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, self.图标路径, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        提醒消息 = win32gui.NIM_MODIFY if self.提醒消息ID else win32gui.NIM_ADD

        self.提醒消息ID = (self.托盘图标实例标识符, 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO, win32con.WM_USER + 20, hicon, self.鼠标悬停提示, 消息内容, 提示显示时间, 消息标题, win32gui.NIIF_INFO)  # 句柄、托盘图标ID  # 托盘图标可以使用的功能的标识  # 回调消息ID、托盘图标句柄、图标字符串  # 提示内容、提示显示时间、提示标题  # 提示用到的图标
        win32gui.Shell_NotifyIcon(提醒消息, self.提醒消息ID)
        return 0

    def 回调函数_图标被创建(self, hwnd, msg, wparam, lparam):
        self.托盘图标发送提醒消息()

    def 回调函数_图标被点击(self, hwnd, msg, wparam, lparam):
        """鼠标事件"""
        import win32api, win32con, win32gui_struct, win32gui

        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            self.回调函数_菜单显示()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            self.回调函数_图标被销毁(退出码=2)
        return 0
        """
        可能的鼠标事件：
          WM_MOUSEMOVE      #光标经过图标
          WM_LBUTTONDOWN    #左键按下
          WM_LBUTTONUP      #左键弹起
          WM_LBUTTONDBLCLK  #双击左键
          WM_RBUTTONDOWN    #右键按下
          WM_RBUTTONUP      #右键弹起
          WM_RBUTTONDBLCLK  #双击右键
          WM_MBUTTONDOWN    #滚轮按下
          WM_MBUTTONUP      #滚轮弹起
          WM_MBUTTONDBLCLK  #双击滚轮
        """

    def 回调函数_菜单项被点击(self, hwnd, msg, wparam, lparam):
        import win32api, win32con, win32gui_struct, win32gui

        id = win32gui.LOWORD(wparam)
        ret = self._运行菜单项回调函数(id)
        return ret

    def _运行菜单项回调函数(self, id):
        菜单项回调函数 = self.菜单项回调函数ID字典[id]  # type: ignore
        ret = 菜单项回调函数(self)
        return ret

    def 回调函数_图标被销毁(self, hwnd=None, msg=None, wparam=None, lparam=None, 退出码=1):
        import win32api, win32con, win32gui_struct, win32gui

        nid = (self.托盘图标实例标识符, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 终止应用程序。
        from bxpy.日志包 import 日志类

        # 日志类.临时开启日志()
        日志类.输出调试(f"当前图标销毁的退出码：{退出码}")
        if 退出码 == 1 and self.回调函数_图标销毁整个程序结束:
            # 1代表程序正常结束了
            self.回调函数_图标销毁整个程序结束()  # 需要传递自身过去时用 s.on_quit(s)
        elif 退出码 == 2:
            # 2代表程序窗口复现了
            self.回调函数_图标销毁窗口重新出现()
        else:
            # 3代表程序跳出异常了
            self.回调函数_图标销毁整个程序结束()
        return 0

    def 回调函数_菜单显示(self):
        import win32api, win32con, win32gui_struct, win32gui

        """显示右键菜单"""
        菜单栏 = win32gui.CreatePopupMenu()
        self.菜单栏创建(菜单栏, self.菜单项列表_添加ID后)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.托盘图标实例标识符)
        win32gui.TrackPopupMenu(菜单栏, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.托盘图标实例标识符, None)
        win32gui.PostMessage(self.托盘图标实例标识符, win32con.WM_NULL, 0, 0)

    def _菜单项增加回调函数ID(self, 菜单项元祖, 回调函数ID, 菜单项ID与回调函数间映射字典):
        添加ID后的菜单项元祖 = []
        for 菜单项x in 菜单项元祖:
            项内容, 项图标路径, 项点击回调函数或子菜单项元祖 = 菜单项x
            if callable(项点击回调函数或子菜单项元祖):  # 如果是回调函数
                菜单项ID与回调函数间映射字典[回调函数ID] = 项点击回调函数或子菜单项元祖  # type: ignore
                菜单项x.append(回调函数ID)
                添加ID后的菜单项元祖.append(菜单项x)
            else:  # 如果是子菜单
                x1, x2, x3 = self._菜单项增加回调函数ID(
                    项点击回调函数或子菜单项元祖,
                    回调函数ID,
                    菜单项ID与回调函数间映射字典,
                )
                回调函数ID = x2
                添加ID后的菜单项元祖.append([项内容, 项图标路径, x1, 回调函数ID])
            回调函数ID += 1
        return 添加ID后的菜单项元祖, 回调函数ID, 菜单项ID与回调函数间映射字典

    def 菜单栏预设退出事件回调函数(self, 回调参数1):
        import win32api, win32con, win32gui_struct, win32gui

        # win32gui.DestroyWindow(self.托盘图标实例标识符)
        self.回调函数_图标被销毁(退出码=1)
        return 0

    def 菜单栏创建(self, 菜单栏对象, 菜单项元祖_带ID):
        import win32api, win32con, win32gui_struct, win32gui

        for 项内容, 项图标路径, 项点击回调函数或子菜单项元祖, 项ID in 菜单项元祖_带ID[::-1]:
            if 项图标路径:
                项图标路径 = self.菜单项图标设置(项图标路径)

            if 项ID in self.菜单项回调函数ID字典:  # 如果没有子菜单
                菜单项, extras = win32gui_struct.PackMENUITEMINFO(text=项内容, hbmpItem=项图标路径, wID=项ID)
                win32gui.InsertMenuItem(菜单栏对象, 0, 1, 菜单项)
            else:
                子菜单栏对象 = win32gui.CreatePopupMenu()
                self.菜单栏创建(子菜单栏对象, 项点击回调函数或子菜单项元祖)
                菜单项, extras = win32gui_struct.PackMENUITEMINFO(text=项内容, hbmpItem=项图标路径, hSubMenu=子菜单栏对象)
                win32gui.InsertMenuItem(菜单栏对象, 0, 1, 菜单项)

    def 菜单项图标设置(self, 图标路径):
        import win32api, win32con, win32gui_struct, win32gui

        # 加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, 图标路径, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm


class 组件类:
    @staticmethod
    def 取得焦点(组件对象):
        return 组件对象.focus_set()

    @staticmethod
    def 属性设置(组件对象, 文字内容=None):
        字典 = {}
        if 文字内容:
            字典["text"] = 文字内容
        return 组件对象.config(**字典)

    @staticmethod
    def 组件触发器绑定处理器(组件对象, 触发器: Literal["回车", "鼠标左键单击", "首次显示时", "不可见时", "拖放", "键盘输入"], 函数):
        触发器映射字典 = {"回车": "<Return>", "鼠标左键单击": "<Button-1>", "首次显示时": "<Map>", "不可见时": "<Unmap>", "拖放": "<<Drop>>", "键盘输入": "<Key>"}
        触发器raw = 触发器映射字典[触发器] if 触发器 in 触发器映射字典 else 触发器
        if 触发器raw == "<<Drop>>":
            from tkinterdnd2 import DND_FILES

            组件对象.drop_target_register(DND_FILES)
            ret = 组件对象.dnd_bind(触发器raw, 函数)
        else:
            ret = 组件对象.bind(触发器raw, 函数)
        return ret

    @staticmethod
    def 组件创建_滚动文本框(界面对象, 状态: Literal["不可编辑", "常规"] = "不可编辑", 高度=10):
        from tkinter import scrolledtext

        if 状态 == "不可编辑":
            状态raw = "disabled"
        elif 状态 == "常规":
            状态raw = "normal"
        return scrolledtext.ScrolledText(界面对象, state=状态raw, height=高度)

    @staticmethod
    def 组件创建_输入框(界面对象):
        from tkinter import Entry

        return Entry(界面对象)

    @staticmethod
    def 组件创建_多行文本框(界面对象, 换行方式=枚举类.字符串换行方式.不在单词中间换行):
        from tkinter import Text

        return Text(界面对象, wrap=换行方式)  # type: ignore

    @staticmethod
    def 组件创建_框架(界面对象, 宽度=200, 高度=100, 边框宽度=2, 边框样式=枚举类.边框样式.扁平):
        from tkinter import Frame

        return Frame(界面对象, width=宽度, height=高度, borderwidth=边框宽度, relief=边框样式)  # type: ignore

    @staticmethod
    def 组件创建_标签(界面对象, 内容="", 边框宽度=2, 边框样式=枚举类.边框样式.脊):
        from tkinter import Label

        return Label(界面对象, text=内容, borderwidth=边框宽度, relief=边框样式)  # type: ignore

    @staticmethod
    def 组件创建_按钮(界面对象, 标签, 命令函数):
        from tkinter import Button

        return Button(界面对象, text=标签, command=命令函数)


class 输入框类(组件类):
    @staticmethod
    def 输入框内容获取(输入框组件对象):
        return 输入框组件对象.get()

    @staticmethod
    def 输入框内容删除(输入框组件对象, 起点=0, 终点="end"):
        return 输入框组件对象.delete(起点, 终点)


if __name__ == "__main__":
    pass
    # def 子线程_创建提示():
    #     界面类.提示框创建_模态_win32ui("监测到硬盘变更", "在应用打开期间请不要变更硬盘，10秒后将强制卸载硬盘，硬盘相关信息将发送至管理员处备案")

    # 线程 = 多线程类.多线程创建(子线程_创建提示, 是否随主程序结束=True)
    # 多线程类.运行(线程)
    # 时间类.等待(2)
    # print(2)
