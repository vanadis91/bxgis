# *-* coding:utf8 *-*
# from .config import 配置
# from . import 常用
# from . import 道路
# from . import 用地
# from . import 区域
# from . import 分区
# from . import 设施
# from . import 入库
def 初始化_添加搜索路径():
    import os
    import sys

    # 添加src目录
    该文件的目录 = os.path.dirname(__file__)
    if 该文件的目录.split(os.sep)[-1] == "bxgis":
        项目src目录 = os.path.dirname(该文件的目录)
    elif 该文件的目录.split(os.sep)[-1] == "toolboxes":
        该文件的目录 = os.path.dirname(该文件的目录)
        该文件的目录 = os.path.dirname(该文件的目录)
        项目src目录 = os.path.dirname(该文件的目录)
    else:
        raise ValueError("添加搜索路径失败。")
    if 项目src目录 not in sys.path:
        sys.path.insert(0, 项目src目录)

    # 添加utils目录
    通用工具目录 = os.path.join(项目src目录, "bxgis", "utils")
    if 通用工具目录 not in sys.path:
        sys.path.insert(0, 通用工具目录)

    # 添加bxgis的第三方包搜索路径
    if 项目src目录.split(os.sep)[-1] == "src":
        项目根目录 = os.path.dirname(项目src目录)
        第三方包目录 = os.path.join(项目根目录, ".venv", "Lib", "site-packages")
        if 第三方包目录 not in sys.path:
            sys.path.insert(0, 第三方包目录)

    # 移除10.8的搜索路径
    from bxpy.基本对象包 import 表类

    表类.项删除(sys.path, "c:\\program files (x86)\\arcgis\\desktop10.8\\bin", 索引或值不存在时是否提示=False)
    表类.项删除(sys.path, "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcPy", 索引或值不存在时是否提示=False)
    表类.项删除(sys.path, "c:\\program files (x86)\\arcgis\\desktop10.8\\ArcToolbox\\Scripts", 索引或值不存在时是否提示=False)


初始化_添加搜索路径()
