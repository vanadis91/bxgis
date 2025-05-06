# *-* coding:utf8 *-*

import sys

# 添加支持路径
sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy\\src")
sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy\\.venv\\Lib\\site-packages")


def 创建发布版本(是否更新辅助包=True):
    from bxpy.路径包 import 路径类
    from bxpy.系统包 import 系统类
    from bxpy.构建发布包 import 加密类pyarmor
    from bxpy.进程包 import 子进程类

    if 是否更新辅助包:
        项目根目录 = 路径类.属性获取_目录(__file__)
        所有项目根目录 = 路径类.属性获取_目录(__file__, 2)

        需要加密的包列表 = ["bxshapely", "bxpandas", "bxpy"]
        for 包x in 需要加密的包列表:
            源码路径 = 路径类.连接(所有项目根目录, 包x, "src", 包x)
            目标路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", 包x)
            路径类.删除(目标路径)
            路径类.复制(源码路径, 路径类.属性获取_目录(目标路径))
            加密类pyarmor.加密包(准备加密的包或文件的路径=目标路径, 加密后存放的目录=路径类.属性获取_目录(目标路径))
            系统类.属性设置_当前工作目录(路径类.连接(所有项目根目录, 包x))
            子进程实例 = 子进程类.子进程创建(f"pdm export --without-hashes --pyproject -o requirements_{包x}.txt")
            print(子进程类.交互_输入关闭等待结束并输出获取(子进程实例))
            路径类.复制(f"requirements_{包x}.txt", 项目根目录)
            路径类.删除(f"requirements_{包x}.txt")
            系统类.属性设置_当前工作目录(项目根目录)
            子进程实例 = 子进程类.子进程创建(f"pdm import requirements_{包x}.txt")
            print(子进程类.交互_输入关闭等待结束并输出获取(子进程实例))
            路径类.删除(f"requirements_{包x}.txt")

    项目根目录 = 路径类.属性获取_目录(__file__)
    发布版本路径 = 路径类.连接(项目根目录, "dist", "bxgis")
    路径类.删除(发布版本路径)
    路径类.复制(路径类.连接(项目根目录, "src"), 发布版本路径)
    路径类.复制(路径类.连接(项目根目录, ".venv"), 发布版本路径)

    需要加密的包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis", "utils", "bxarcpy")
    加密类pyarmor.加密包(准备加密的包或文件的路径=需要加密的包路径, 加密后存放的目录=路径类.连接(项目根目录, "dist"))

    需要加密的包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis")
    加密类pyarmor.加密包(准备加密的包或文件的路径=需要加密的包路径, 加密后存放的目录=路径类.属性获取_目录(需要加密的包路径))

    被两次加密的包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis", "utils", "bxarcpy")
    路径类.删除(被两次加密的包路径)
    只被加密一次的包路径 = 路径类.连接(项目根目录, "dist", "bxarcpy")
    辅助包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis", "utils")
    路径类.复制(只被加密一次的包路径, 辅助包路径)
    路径类.删除(只被加密一次的包路径)

    原先就加密的包列表 = ["bxshapely", "bxpandas", "bxpy"]
    for x in 原先就加密的包列表:
        被两次加密的包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis", "utils", x)
        路径类.删除(被两次加密的包路径)
        只被加密一次的包路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", x)
        辅助包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis", "utils")
        路径类.复制(只被加密一次的包路径, 辅助包路径)

    子路径列表的列表 = 路径类.子路径(需要加密的包路径, 单一层次=False, 链接处理方式="向下探索")
    for 子路径列表x in 子路径列表的列表:
        if "#历史版本" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))
        if "_gsdata_" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "_gsdata_"))


# 子进程实例 = 子进程类.子进程创建("pdm export -o requirements_bxdingding.txt")
# print(子进程类.交互_输入关闭等待结束并输出获取(子进程实例))
# 路径类.复制("requirements_bxdingding.txt", "..\\appBXRoot\\docker-bxroot\\com")
# 路径类.删除("requirements_bxdingding.txt")


def main():
    创建发布版本()


if __name__ == "__main__":
    main()
