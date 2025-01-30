# *-* coding:utf8 *-*

import sys

# 添加支持路径
sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy\\src")
sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy\\.venv\\Lib\\site-packages")


def 创建发布版本():
    from bxpy.路径包 import 路径类
    from bxpy.构建发布包 import 加密类pyarmor

    项目根目录 = 路径类.属性获取_目录(__file__)
    发布版本路径 = 路径类.连接(项目根目录, "dist", "bxgis")
    路径类.删除(发布版本路径)
    路径类.复制(路径类.连接(项目根目录, "src"), 发布版本路径)
    路径类.复制(路径类.连接(项目根目录, ".venv"), 发布版本路径)

    需要加密的包路径 = 路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis")
    加密类pyarmor.加密包(准备加密的包或文件的路径=需要加密的包路径, 加密后存放的目录=路径类.属性获取_目录(需要加密的包路径))

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


def 生成次要的包():
    from bxpy.路径包 import 路径类
    from bxpy.构建发布包 import 加密类pyarmor

    项目根目录 = 路径类.属性获取_目录(__file__)
    所有项目根目录 = 路径类.属性获取_目录(__file__, 2)

    需要加密的包列表 = ["bxshapely", "bxpandas", "bxpy"]
    for 包x in 需要加密的包列表:
        bxshapely源码路径 = 路径类.连接(所有项目根目录, 包x, "src", 包x)
        bxshapely目标路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", 包x)
        路径类.删除(bxshapely目标路径)
        路径类.复制(bxshapely源码路径, 路径类.属性获取_目录(bxshapely目标路径))
        加密类pyarmor.加密包(准备加密的包或文件的路径=bxshapely目标路径, 加密后存放的目录=路径类.属性获取_目录(bxshapely目标路径))
        子路径列表的列表 = 路径类.子路径(bxshapely目标路径, 单一层次=False, 链接处理方式="向下探索")
        for 子路径列表x in 子路径列表的列表:
            if "#历史版本" in 子路径列表x[1]:
                路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))


def main():
    生成次要的包()
    创建发布版本()


if __name__ == "__main__":
    main()
