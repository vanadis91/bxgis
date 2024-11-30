from bxpy.进程包 import 子进程类
from bxpy.日志包 import 日志类
from typing import Union, Literal


class 工具集:
    @staticmethod
    def 查找所有包(路径="src"):
        from bxpy.基本对象包 import 模块加载

        模块加载("setuptools")
        from setuptools import find_packages

        return find_packages(where="src")

    @staticmethod
    def 硬件信息获取():
        子进程命令 = f"python -m pyarmor.cli.hdinfo"
        子进程 = 子进程类.子进程创建(子进程命令)
        输出内容 = 子进程类.输出获取_阻塞(子进程)
        print(输出内容)


class 构建类pyinstaller:
    @staticmethod
    def 构建(
        入口文件路径=".\\src\\main.py",
        打包输出路径=".\\dist",
        build文件路径=".\\build",
        清除此前生成的文件=True,
        清除此前缓存的文件=True,
        生成格式: Literal["常规", "单文件"] = "常规",
        spec文件路径="默认",
        exe文件名称="默认",
        exe文件以外文件的目录形式: Literal["默认", "旧版本"] = "默认",
        额外数据路径列表=[
            {"源路径": "", "目标路径": ""},
        ],
        额外代码路径列表=[
            {"源路径": "", "目标路径": ""},
        ],
        额外包搜索路径列表=[],
        额外调用的包列表=[],
        额外排除的包列表=[],
        收集包中子包的包列表=[],
        收集包中数据的包列表=[],
        收集包中代码的包列表=[],
        收集包中所有内容的包列表=[],
        调试模式={
            "启用所有选项": False,
            "模块初始化时显示加载位置": False,
            "打包初始化时显示进度消息，用于诊断缺少的模块": False,
            "将源码作为文件存储，而非打包到exe内": False,
        },
        python解释器参数="",
        程序界面类型: Literal["显示终端", "隐藏终端", "从终端启动则隐藏", "从终端启动则最小化"] = "显示终端",
        图标="None",
    ):
        from bxpy.基本对象包 import 模块加载

        模块加载("PyInstaller", "pyinstaller")
        子进程命令 = ""
        子进程命令 += f" --distpath {打包输出路径}"
        子进程命令 += f" --workpath {build文件路径}"

        if 清除此前缓存的文件:
            子进程命令 += " --clean"

        if 清除此前生成的文件:
            子进程命令 += " -y"

        if 生成格式 == "常规":
            子进程命令 += " -D"
        elif 生成格式 == "单文件":
            子进程命令 += " -F"

        if spec文件路径 != "默认":
            子进程命令 += f" --specpath {spec文件路径}"
        else:
            子进程命令 += f" --specpath spec"

        if exe文件名称 != "默认":
            子进程命令 += f" --name {exe文件名称}"

        if exe文件以外文件的目录形式 == "旧版本":
            子进程命令 += f' --contents-directory "."'
        elif exe文件以外文件的目录形式 != "默认":
            子进程命令 += f" --contents-directory {exe文件以外文件的目录形式}"

        if 额外数据路径列表 != [{"源路径": "", "目标路径": ""}]:
            for x in 额外数据路径列表:
                子进程命令 += f' --add-data "{x["源路径"]}":"{x["目标路径"]}"'

        if 额外代码路径列表 != [{"源路径": "", "目标路径": ""}]:
            for x in 额外代码路径列表:
                子进程命令 += f' --add-binary "{x["源路径"]}":"{x["目标路径"]}"'

        if 额外包搜索路径列表 != []:
            for x in 额外包搜索路径列表:
                子进程命令 += f' -p "{x}"'

        if 额外调用的包列表 != []:
            for x in 额外调用的包列表:
                子进程命令 += f" --hidden-import {x}"

        if 额外排除的包列表 != []:
            for x in 额外排除的包列表:
                子进程命令 += f" --exclude-module {x}"

        if 收集包中子包的包列表 != []:
            for x in 收集包中子包的包列表:
                子进程命令 += f" --collect-submodules {x}"

        if 收集包中数据的包列表 != []:
            for x in 收集包中数据的包列表:
                子进程命令 += f" --collect-data {x}"

        if 收集包中代码的包列表 != []:
            for x in 收集包中代码的包列表:
                子进程命令 += f" --collect-binaries {x}"

        if 收集包中所有内容的包列表 != []:
            for x in 收集包中所有内容的包列表:
                子进程命令 += f" --collect-all {x}"

        if 调试模式["启用所有选项"]:
            子进程命令 += f" --debug all"
        if 调试模式["模块初始化时显示加载位置"]:
            子进程命令 += f" --debug imports"
        if 调试模式["打包初始化时显示进度消息，用于诊断缺少的模块"]:
            子进程命令 += f" --debug bootloader"
        if 调试模式["将源码作为文件存储，而非打包到exe内"]:
            子进程命令 += f" --debug noarchive"

        if python解释器参数 != "":
            for x in python解释器参数:
                子进程命令 += f" --python-option {python解释器参数}"

        if 程序界面类型 == "显示终端":
            子进程命令 += f" -c"
        elif 程序界面类型 == "隐藏终端":
            子进程命令 += f" -w"
        elif 程序界面类型 == "从终端启动则隐藏":
            子进程命令 += f" --hide-console hide-early"
        elif 程序界面类型 == "从终端启动则最小化":
            子进程命令 += f" --hide-console minimize-early"

        if 图标 != "None":
            子进程命令 += f" --icon {图标}"

        子进程命令 = f'pdm run pyinstaller {子进程命令} "{入口文件路径}"'
        日志类.输出调试(f"子进程命令：{子进程命令}")
        子进程 = 子进程类.子进程创建(子进程命令, 编码="gbk")
        子进程类.输出显示_阻塞_逐行(子进程)


class 构建类setuptools:
    @staticmethod
    def 构建(
        包名称="bxgis",
        包版本="0.0.1",
        包描述=("一个近期用于实现杭州详规入库数据库构建，远期用于协助国土空间规划编制的包。"),
        包作者="beixiao",
        包作者邮箱="vanadis91@163.com",
        包主页="https://github.com/vanadis91/bxgis",
        包许可证="GPLv3",
        包长描述="",
        Python版本="~=3.9",
        第三方包列表=["shapely", "numpy", "pandas", "pypiwin32", "psutil", "setuptools", "pytest", "tinydb", "shortuuid", "tqdm", "colorama", "flask", "flask_login", "pymongo"],
        包名称列表=[
            "bxgis",
            "bxgis.bxarcpy",
            "bxarcpy",
        ],
        包路径字典={
            "bxgis": "src/bxgis",
            "bxgis.bxarcpy": "src/bxgis",
            "bxarcpy": "src/bxgis/common/bxarcpy",
        },
        包额外数据字典={
            "bxgis": [
                "esri/arcpy/*",
                "esri/help/gp/*",
                "esri/help/gp/toolboxes/*",
                "esri/help/gp/messages/*",
                "esri/toolboxes/*",
                "config/*",
            ],
            "pyarmor_runtime_005556": [
                "pyarmor_runtime.pyd",
            ],
        },
        运行参数列表=["sdist", "bdist_wheel"],
    ):
        from bxpy.基本对象包 import 模块加载

        模块加载("setuptools")
        from setuptools import setup

        setup(
            name=包名称,
            version=包版本,
            description=包描述,
            author=包作者,
            author_email=包作者邮箱,
            url=包主页,
            license=包许可证,
            long_description=包长描述,
            python_requires=Python版本,
            install_requires=第三方包列表,
            packages=包名称列表,
            package_dir=包路径字典,
            package_data=包额外数据字典,
            script_args=运行参数列表,
        )


class 加密类pyarmor:
    @staticmethod
    def 许可证注册(注册文件路径):
        子进程命令 = f'python -m pyarmor.cli reg "{注册文件路径}"'
        子进程 = 子进程类.子进程创建(子进程命令)
        子进程类.输出显示_阻塞_逐行(子进程)

    @staticmethod
    def 加密包(
        准备加密的包或文件的路径,
        加密源类型: Literal["文件", "包"] = "包",
        加密后存放的目录=".\\dist",
        是否递归搜索子目录=True,
        辅助包保存到包目录内部=True,
        有效期: Literal[None, "30", "2024-12-31"] = None,
        时间来源: Literal["本地", "网络"] = "本地",
        是否绑定硬盘序列号: Literal["", "HXS2000CN2A"] = "",
        是否绑定网卡地址: Literal["", "00:16:3e:35:19:3d"] = "",
        是否绑定IP地址: Literal["", "128.16.4.10"] = "",
    ):
        子进程命令 = ""
        子进程命令列表 = []
        from bxpy.基本对象包 import 模块加载

        模块加载("pyarmor")
        import sys
        from pyarmor.cli.__main__ import main_entry

        当前解释器路径 = sys.executable
        if 加密后存放的目录 != ".\\dist":
            子进程命令 += f' -O "{加密后存放的目录}"'
            子进程命令列表.append("-O")
            子进程命令列表.append(str(加密后存放的目录))
        if 是否递归搜索子目录:
            子进程命令 += f" -r"
            子进程命令列表.append("-r")
        if 加密源类型 == "包" and 辅助包保存到包目录内部:
            子进程命令 += f" -i"
            子进程命令列表.append("-i")
        if 时间来源 == "网络":
            # 子进程命令2 = f'"{当前解释器路径}" -m pyarmor.cli cfg nts=http://worldtimeapi.org/api'
            # 子进程 = 子进程类.子进程创建(子进程命令)
            # 输出内容 = 子进程类.输出获取_阻塞(子进程)
            # print(输出内容)
            子进程命令列表2 = ["cfg", "nts=http://worldtimeapi.org/api"]
            main_entry(子进程命令列表2)
        if 有效期:
            子进程命令 += f" -e {有效期}"
            子进程命令列表.append("-e")
            子进程命令列表.append(str(有效期))
        if 是否绑定硬盘序列号 != "" or 是否绑定网卡地址 != "" or 是否绑定IP地址 != "":
            strTemp = ""
            strTemp = strTemp + 是否绑定网卡地址 if 是否绑定网卡地址 != "" else strTemp
            strTemp = strTemp + " " + 是否绑定硬盘序列号 if 是否绑定硬盘序列号 != "" else strTemp
            strTemp = strTemp + " " + 是否绑定IP地址 if 是否绑定IP地址 != "" else strTemp
            子进程命令 += f' -b "{strTemp}"'
            子进程命令列表.append("-b")
            子进程命令列表.append(str(strTemp))
        # 子进程命令 = f'"{当前解释器路径}" -m pyarmor.cli gen {子进程命令} {准备加密的包或文件的路径}'
        # 子进程 = 子进程类.子进程创建(子进程命令)
        # print(子进程类.输出获取_阻塞(子进程))
        子进程命令列表.insert(0, "gen")
        子进程命令列表.append(准备加密的包或文件的路径)
        main_entry(子进程命令列表)


if __name__ == "__main__":
    构建类pyinstaller.构建(入口文件路径=".\\src\\main.py", exe文件名称="Datalink")
