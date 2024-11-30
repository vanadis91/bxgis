from bxpy.路径包 import 路径类
from bxpy.进程包 import 子进程类


class 配置:
    nssmEXE路径 = None


def _获取nssmEXE路径():
    if 配置.nssmEXE路径 == None:
        本文件所在目录 = 路径类.属性获取_目录(__file__)
        nssmEXE路径 = 路径类.连接(本文件所在目录, "otherAPP", "nssm", "nssm.exe")
        配置.nssmEXE路径 = nssmEXE路径  # type: ignore
    return 配置.nssmEXE路径


class 服务类:
    @staticmethod
    def 服务创建(服务名称="bx-", 执行程序路径=""):
        命令行 = f'"{_获取nssmEXE路径()}" install "{服务名称}" "{执行程序路径}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 服务删除(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" remove "{服务名称}" confirm'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 属性设置_开机启动(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" set "{服务名称}" Start SERVICE_AUTO_START'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 属性设置_停止后自动重启(服务名称="bx-", 停止后重启延迟_毫秒=0):
        命令行 = f'"{_获取nssmEXE路径()}" set "{服务名称}" AppExit Default Restart && "{_获取nssmEXE路径()}" set "{服务名称}" AppRestartDelay {str(停止后重启延迟_毫秒)}'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 属性设置_收到停止命令后进行强制停止延迟(服务名称="bx-", 强制停止延迟_毫秒=0):
        命令行 = f'"{_获取nssmEXE路径()}" set "{服务名称}" AppStopTimeout {str(强制停止延迟_毫秒)}'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 属性设置_显示名称(服务名称="bx-", 显示名称=""):
        命令行 = f'"{_获取nssmEXE路径()}" set "{服务名称}" DisplayName "{显示名称}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 属性设置_描述(服务名称="bx-", 描述文字=""):
        命令行 = f'"{_获取nssmEXE路径()}" set "{服务名称}" Description "{描述文字}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 服务编辑_GUI(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" edit "{服务名称}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 服务启动(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" start "{服务名称}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 服务停止(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" stop "{服务名称}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 服务重启(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" restart "{服务名称}"'
        子进程 = 子进程类.子进程创建(命令行)
        return 子进程类.交互_输入关闭等待结束并输出获取(子进程)

    @staticmethod
    def 服务状态查询(服务名称="bx-"):
        命令行 = f'"{_获取nssmEXE路径()}" status "{服务名称}"'
        子进程 = 子进程类.子进程创建(命令行)
        ret = 子进程类.交互_输入关闭等待结束并输出获取(子进程)
        ret = [x.strip() for x in ret.split("\n") if x.strip() != ""]  # type: ignore
        # print(ret)
        状态 = "空"
        for x in ret:
            if "未安装" in x:
                状态 = "未安装"
                break
            if "SERVICE_RUNNING" in x:
                状态 = "运行"
                break
            if "SERVICE_STOPPED" in x:
                状态 = "停止"
                break
        return 状态

    @staticmethod
    def 服务是否已存在(服务名称):
        from bxpy.基本对象包 import 模块加载

        模块加载("win32service", "pywin32")
        import win32service
        import win32api

        try:
            # 打开服务控制管理器
            服务管理器 = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)

            # 打开指定的服务
            服务对象 = win32service.OpenService(服务管理器, 服务名称, win32service.SERVICE_QUERY_STATUS)

            # 关闭服务句柄
            win32service.CloseServiceHandle(服务对象)

            # 关闭服务控制管理器
            win32service.CloseServiceHandle(服务管理器)

            # 如果能打开服务, 则说明服务存在
            return True

        except win32api.error as e:
            # 如果出现错误, 说明服务不存在
            return False


if __name__ == "__main__":
    print(服务类.服务状态查询("camsvc"))
