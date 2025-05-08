# *-* coding:utf8 *-*
def 初始化_添加搜索路径():
    import os
    import sys

    # 添加src目录
    该文件的目录 = os.path.dirname(__file__)

    while 该文件的目录.split(os.sep)[-1] != "bxgis":
        try:
            该文件的目录 = os.path.dirname(该文件的目录)
        except Exception as e:
            raise Exception(f"添加搜索路径失败。\n{e}")

    项目src目录 = os.path.dirname(该文件的目录)
    if 项目src目录 not in sys.path:
        sys.path.insert(0, 项目src目录)

    # 添加utils目录
    通用工具目录 = os.path.join(项目src目录, "bxgis", "utils")
    if 通用工具目录 not in sys.path:
        sys.path.insert(0, 通用工具目录)

    # 添加bxgis的第三方包搜索路径
    项目根目录 = os.path.dirname(项目src目录)
    第三方包目录 = os.path.join(项目根目录, ".venv", "Lib", "site-packages")
    if 第三方包目录 not in sys.path:
        sys.path.insert(0, 第三方包目录)

    # 移除10.8的搜索路径
    from bxpy.基本对象包 import 表类

    表类.项删除(sys.path, "c:\\program files (x86)\\arcgis\\desktop10.8\\bin", 索引或值不存在时是否提示=False)
    表类.项删除(sys.path, "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcPy", 索引或值不存在时是否提示=False)
    表类.项删除(sys.path, "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcToolbox\\Scripts", 索引或值不存在时是否提示=False)


if __name__ == "__main__":
    try:
        # 参数列表 = 系统类.属性获取_当前进程参数()
        # print(f"获取到的参数列表：{参数列表}")

        # 命令行文件路径 = 参数列表[0]
        # 模块名称 = 参数列表[1]
        # 函数名称 = 参数列表[2]
        # 函数参数列表 = 参数列表[3:] if len(参数列表) >= 4 else None
        # print(f"模块名称：{模块名称}")
        # print(f"函数名称：{函数名称}")
        # if 函数参数列表:
        #     import json

        #     键列表 = 函数参数列表[::2]
        #     值列表 = 函数参数列表[1::2]
        #     参数字典 = {}
        #     for 键, 值 in zip(键列表, 值列表):
        #         if 值[0] in ["[", "{"] and 值[-1] in ["]", "}"]:
        #             参数字典[键] = json.loads(值)
        #         else:
        #             参数字典[键] = 值
        #     print(f"参数字典：{参数字典}")
        初始化_添加搜索路径()
        from bxpy.路径包 import 路径类
        from bxgis.配置.配置包 import 配置类
        import json

        命令行参数文件路径 = 路径类.连接(路径类.属性获取_目录(__file__), "命令行参数.json")
        with open(命令行参数文件路径, "r", encoding="gbk") as f:
            运行命令字典 = json.load(f)
        模块名称 = 运行命令字典["模块名称"]
        函数名称 = 运行命令字典["函数名称"]
        print(f"模块名称：{模块名称}")
        print(f"函数名称：{函数名称}")
        if "参数列表" in 运行命令字典:
            参数列表字符串 = 运行命令字典["参数列表"]
            参数列表 = json.loads(参数列表字符串)

            参数列表temp = []
            for x in 参数列表:
                if isinstance(x, str) and ";" in x:
                    参数列表temp.append([y.strip() for y in x.split(";")])
                else:
                    参数列表temp.append(x)
            参数列表 = 参数列表temp
            print(f"参数列表：{参数列表}")

        if "参数字典" in 运行命令字典:
            参数字典字符串 = 运行命令字典["参数字典"]
            参数字典 = json.loads(参数字典字符串)

            参数字典temp = {}
            for k, v in 参数字典.items():
                if isinstance(v, str) and ";" in v:
                    参数字典temp[k] = [y.strip() for y in v.split(";")]
                else:
                    参数字典temp[k] = v
            参数字典 = 参数字典temp
            print(f"参数字典：{参数字典}")

        from bxarcpy.环境包 import 环境管理器类

        import importlib

        模块 = importlib.import_module(模块名称)
        函数 = getattr(模块, 函数名称)
        if 函数名称 == "项目初始化":
            if "参数列表" in 运行命令字典 and "参数字典" in 运行命令字典:
                函数(*参数列表, **参数字典)
            elif "参数列表" in 运行命令字典 and "参数字典" not in 运行命令字典:
                函数(*参数列表)
            elif "参数列表" not in 运行命令字典 and "参数字典" in 运行命令字典:
                函数(**参数字典)
            else:
                函数()
        else:
            工作空间 = 配置类.工作空间路径获取()
            with 环境管理器类.环境管理器类创建(工作空间):
                if "参数列表" in 运行命令字典 and "参数字典" in 运行命令字典:
                    函数(*参数列表, **参数字典)
                elif "参数列表" in 运行命令字典 and "参数字典" not in 运行命令字典:
                    函数(*参数列表)
                elif "参数列表" not in 运行命令字典 and "参数字典" in 运行命令字典:
                    函数(**参数字典)
                else:
                    函数()
        input(f"按任意键继续...")
    except Exception as e:
        from bxpy.元数据包 import 追踪元数据类

        追踪元数据类.追踪信息打印并暂停()
