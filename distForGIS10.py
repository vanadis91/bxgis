# *-* coding:utf8 *-*

from typing import Literal
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
    路径类.复制(路径类.连接(项目根目录, "src", "bxgis"), 路径类.连接(项目根目录, "dist", "bxgis", "src"))
    加密类pyarmor.加密包(
        准备加密的包或文件的路径=路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis"),
        加密后存放的目录=路径类.连接(项目根目录, "dist", "bxgis", "src"),
    )
    子路径列表的列表 = 路径类.子路径(路径类.连接(项目根目录, "dist", "bxgis", "src", "bxgis"), 单一层次=False, 链接处理方式="向下探索")
    for 子路径列表x in 子路径列表的列表:
        if "#历史版本" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))
        if "_gsdata_" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "_gsdata_"))


def 生成次要的包():

    from bxpy.路径包 import 路径类
    from bxpy.构建发布包 import 加密类pyarmor

    项目根目录 = 路径类.属性获取_目录(__file__)
    所有项目根目录 = 路径类.属性获取_目录(__file__, 2)

    # 删除bxshapely
    bxshapely目录路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", "bxshapely")
    路径类.删除(bxshapely目录路径)
    加密类pyarmor.加密包(
        准备加密的包或文件的路径=路径类.连接(所有项目根目录, "bxshapely", "src", "bxshapely"),
        加密后存放的目录=路径类.属性获取_目录(bxshapely目录路径),
    )
    子路径列表的列表 = 路径类.子路径(bxshapely目录路径, 单一层次=False, 链接处理方式="向下探索")
    for 子路径列表x in 子路径列表的列表:
        if "#历史版本" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))

    # 删除bxpandas
    bxpandas目录路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", "bxpandas")
    路径类.删除(bxpandas目录路径)
    加密类pyarmor.加密包(
        准备加密的包或文件的路径=路径类.连接(所有项目根目录, "bxpandas", "src", "bxpandas"),
        加密后存放的目录=路径类.属性获取_目录(bxpandas目录路径),
    )
    子路径列表的列表 = 路径类.子路径(bxpandas目录路径, 单一层次=False, 链接处理方式="向下探索")
    for 子路径列表x in 子路径列表的列表:
        if "#历史版本" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))

    # 删除bxpy
    bxpy目录路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", "bxpy")
    路径类.删除(bxpy目录路径)
    加密类pyarmor.加密包(
        准备加密的包或文件的路径=路径类.连接(所有项目根目录, "bxpy", "src", "bxpy"),
        加密后存放的目录=路径类.属性获取_目录(bxpy目录路径),
    )
    子路径列表的列表 = 路径类.子路径(bxpy目录路径, 单一层次=False, 链接处理方式="向下探索")
    for 子路径列表x in 子路径列表的列表:
        if "#历史版本" in 子路径列表x[1]:
            路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))

    # # 删除bxarcpy
    # bxarcpy目录路径 = 路径类.连接(项目根目录, "src", "bxgis", "utils", "bxarcpy")
    # 路径类.删除(源路径=bxarcpy目录路径)
    # 路径类.复制(
    #     路径类.连接(所有项目根目录, "bxarcpy", "src", "bxarcpy"),
    #     路径类.连接(项目根目录, "src", "bxgis", "utils"),
    # )
    # 子路径列表的列表 = 路径类.子路径(bxarcpy目录路径, 单一层次=False, 链接处理方式="向下探索")
    # for 子路径列表x in 子路径列表的列表:
    #     if "#历史版本" in 子路径列表x[1]:
    #         路径类.删除(路径类.连接(子路径列表x[0], "#历史版本"))


def 包构建():
    from bxpy.构建发布包 import 构建类setuptools, 工具集
    from bxpy.路径包 import 路径类

    包名称列表 = 工具集.查找所有包("src")
    包路径字典 = 工具集.查找所有包路径("src")
    print(f"包名称列表: {包名称列表}")
    print(f"包路径字典: {包路径字典}")
    # 包路径字典 = {}
    # for 包名称x in 包名称列表:
    #     if len(包名称x) >= 5 and 包名称x[0:5] == "bxgis":
    #         包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
    #     elif len(包名称x) >= 7 and 包名称x[0:7] == "bxarcpy":
    #         包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
    #     elif len(包名称x) >= 9 and 包名称x[0:9] == "bxshapely":
    #         包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
    #     elif len(包名称x) >= 8 and 包名称x[0:8] == "bxpandas":
    #         包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
    #     elif len(包名称x) >= 4 and 包名称x[0:4] == "bxpy":
    #         包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
    # print(f"包路径字典: {包路径字典}")
    构建类setuptools.构建(
        包名称="bxgis",
        包版本="0.0.1",
        包描述="一个近期用于实现杭州详规入库数据库构建，远期用于协助国土空间规划编制的包。",
        包作者="beixiao",
        包作者邮箱="vanadis91@163.com",
        包主页="https://github.com/vanadis91/bxgis",
        包许可证="GPLv3",
        Python版本="~=3.9",
        第三方包列表=[
            "shapely",
            "numpy",
            "pandas",
            "pypiwin32",
            "psutil",
            "setuptools",
            "tinydb",
            "shortuuid",
            "tqdm",
            "colorama",
        ],
        包名称列表=包名称列表,
        包路径字典=包路径字典,
        手动指定包额外数据={
            "bxgis": [
                "esri/arcpy/*",
                "esri/help/gp/*",
                "esri/help/gp/toolboxes/*",
                "esri/help/gp/messages/*",
                "esri/toolboxes/*",
                "config/*",
            ],
            "bxshapely": [
                "pyarmor_runtime_005556/pyarmor_runtime.pyd",
            ],
            "bxpandas": [
                "pyarmor_runtime_005556/pyarmor_runtime.pyd",
            ],
            "bxpy": [
                "pyarmor_runtime_005556/pyarmor_runtime.pyd",
            ],
        },
        运行参数列表=["sdist", "bdist_wheel"],
    )
    项目根目录 = 路径类.属性获取_目录(__file__)
    eggInfo目录路径 = 路径类.连接(项目根目录, "bxgis.egg-info")
    路径类.删除(eggInfo目录路径)
    build目录路径 = 路径类.连接(项目根目录, "build")
    路径类.删除(build目录路径)


def main():
    创建发布版本()


if __name__ == "__main__":
    main()
