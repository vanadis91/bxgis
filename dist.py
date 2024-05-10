from typing import Literal


def 生成esri路径下文件():
    import os
    import sys

    # 添加支持路径
    项目根目录 = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(项目根目录, "src"))
    from bxpy.路径包 import 路径类

    # 重新生成esri路径下文件
    esri目录路径 = 路径类.连接(项目根目录, "src", "bxgis", "esri")
    路径类.删除(esri目录路径)

    import arcpy

    pyt文件路径 = 路径类.连接(项目根目录, "src", "bxgis", "bxgis.pyt")
    arcpy.gp.createtoolboxsupportfiles(pyt文件路径)  # type: ignore

    # 将pyt文件复制到toolboxes目录下
    toolboxes目录路径 = 路径类.连接(项目根目录, "src", "bxgis", "esri", "toolboxes")
    路径类.复制(pyt文件路径, toolboxes目录路径)

    # 将xml文件移动到toolboxes目录下
    bxgis目录路径 = 路径类.连接(项目根目录, "src", "bxgis")
    子路径下文件列表 = 路径类.子路径(bxgis目录路径)[2]  # type: ignore
    for x in 子路径下文件列表:
        if len(x) >= 8 and x[0:5] == "bxgis" and x[-4:] == ".xml":
            子路径下文件完整路径_移动前 = 路径类.连接(项目根目录, "src", "bxgis", x)
            子路径下文件完整路径_移动后 = 路径类.连接(toolboxes目录路径, x)
            路径类.修改(子路径下文件完整路径_移动前, 子路径下文件完整路径_移动后)


def 生成次要的包(次要包是否源码=True):
    import os
    import sys

    # 添加支持路径
    项目根目录 = os.path.dirname(__file__)
    sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy\\src")
    sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy\\.venv\\Lib\\site-packages")
    from bxpy.路径包 import 路径类
    from bxpy.构建发布包 import 加密类pyarmor

    所有项目根目录 = 路径类.转绝对("..", 项目根目录)
    # 删除bxshapely
    bxshapely目录路径 = 路径类.连接(项目根目录, "src", "bxshapely")

    路径类.删除(bxshapely目录路径)
    if 次要包是否源码:
        路径类.链接_新增(
            路径类.连接(所有项目根目录, "bxshapely", "src", "bxshapely"),
            路径类.属性获取_目录(bxshapely目录路径),
        )
    else:
        加密类pyarmor.加密包(
            准备加密的包或文件的路径=路径类.连接(所有项目根目录, "bxshapely", "src", "bxshapely"),
            加密后存放的目录=路径类.属性获取_目录(bxshapely目录路径),
        )

    # 删除bxpandas
    bxpandas目录路径 = 路径类.连接(项目根目录, "src", "bxpandas")
    路径类.删除(bxpandas目录路径)
    if 次要包是否源码:
        路径类.链接_新增(
            路径类.连接(所有项目根目录, "bxpandas", "src", "bxpandas"),
            路径类.属性获取_目录(bxpandas目录路径),
        )
    else:
        加密类pyarmor.加密包(
            准备加密的包或文件的路径=路径类.连接(所有项目根目录, "bxpandas", "src", "bxpandas"),
            加密后存放的目录=路径类.属性获取_目录(bxpandas目录路径),
        )

    # 删除bxpy
    bxpy目录路径 = 路径类.连接(项目根目录, "src", "bxpy")
    路径类.删除(bxpy目录路径)
    if 次要包是否源码:
        路径类.链接_新增(
            路径类.连接(所有项目根目录, "bxpy", "src", "bxpy"),
            路径类.属性获取_目录(bxpy目录路径),
        )
    else:
        加密类pyarmor.加密包(
            准备加密的包或文件的路径=路径类.连接(所有项目根目录, "bxpy", "src", "bxpy"),
            加密后存放的目录=路径类.属性获取_目录(bxpy目录路径),
        )

    # 删除bxarcpy
    bxarcpy目录路径 = 路径类.连接(项目根目录, "src", "bxarcpy")
    路径类.删除(bxarcpy目录路径)
    路径类.链接_新增(
        路径类.连接(所有项目根目录, "bxarcpy", "src", "bxarcpy"),
        路径类.属性获取_目录(bxarcpy目录路径),
    )


def 包构建():
    from bxpy.构建发布包 import 构建类setuptools, 工具集
    from bxpy.路径包 import 路径类

    包名称列表 = 工具集.查找所有包("src")
    print(f"包名称列表: {包名称列表}")
    包路径字典 = {}
    for 包名称x in 包名称列表:
        if len(包名称x) >= 5 and 包名称x[0:5] == "bxgis":
            包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
        elif len(包名称x) >= 7 and 包名称x[0:7] == "bxarcpy":
            包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
        elif len(包名称x) >= 9 and 包名称x[0:9] == "bxshapely":
            包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
        elif len(包名称x) >= 8 and 包名称x[0:8] == "bxpandas":
            包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
        elif len(包名称x) >= 4 and 包名称x[0:4] == "bxpy":
            包路径字典[包名称x] = f'src/{包名称x.replace(".","/")}'
    print(f"包路径字典: {包路径字典}")
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
            "pandas",
            "psutil",
            "setuptools",
            "tinydb",
            "shortuuid",
            "tqdm",
            "colorama",
        ],
        包名称列表=包名称列表,
        包路径字典=包路径字典,
        包额外数据字典={
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


def main(功能: Literal["作者开发环境初始化", "作者打包", "打包"] = "作者开发环境初始化"):
    if 功能 == "作者开发环境初始化":
        生成次要的包(次要包是否源码=True)  # type: ignore
    elif 功能 == "作者打包":
        生成次要的包(次要包是否源码=False)
        生成esri路径下文件()
        包构建()
        生成次要的包(次要包是否源码=True)
    elif 功能 == "打包":
        生成esri路径下文件()
        包构建()


if __name__ == "__main__":
    main(功能="作者开发环境初始化")
