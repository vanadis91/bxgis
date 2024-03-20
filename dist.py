def 生成esri路径下文件():
    import os
    import sys

    # 添加支持路径
    项目根目录 = os.path.dirname(__file__)
    sys.path.append(项目根目录 + "\\src")
    sys.path.append(项目根目录 + "\\src\\bxgis\\common")
    from bxpy.系统包 import 系统类
    from bxpy.路径包 import 路径类
    from bxpy.进程包 import 子进程类

    # 重新生成esri路径下文件
    esri目录路径 = 路径类.连接(项目根目录, "src\\bxgis\\esri")
    # 路径类.删除(esri目录路径)
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{esri目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))

    import arcpy

    pyt文件路径 = 路径类.连接(项目根目录, "src\\bxgis\\bxgis.pyt")
    arcpy.gp.createtoolboxsupportfiles(pyt文件路径)  # type: ignore

    # 将pyt文件复制到toolboxes目录下
    toolboxes目录路径 = 路径类.连接(项目根目录, "src\\bxgis\\esri\\toolboxes")
    路径类.复制(pyt文件路径, toolboxes目录路径)

    # 将xml文件移动到toolboxes目录下
    bxgis目录路径 = 路径类.连接(项目根目录, "src\\bxgis")
    子路径下文件列表 = 路径类.子路径(bxgis目录路径)[2]
    for x in 子路径下文件列表:
        if len(x) >= 8 and x[0:5] == "bxgis" and x[-4:] == ".xml":
            子路径下文件完整路径_移动前 = 路径类.连接(项目根目录, "src\\bxgis", x)
            子路径下文件完整路径_移动后 = 路径类.连接(toolboxes目录路径, x)
            路径类.修改(子路径下文件完整路径_移动前, 子路径下文件完整路径_移动后)

    # 运行setuptools
    系统类.属性设置_当前工作目录(项目根目录)
    当前运行的解释器路径 = sys.executable

    子程序 = 子进程类.子进程创建(f'"{当前运行的解释器路径}" setup.py sdist bdist_wheel')
    print(子进程类.输出获取_阻塞(子程序))

    eggInfo目录路径 = 路径类.连接(项目根目录, "bxgis.egg-info")
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{eggInfo目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))

    build目录路径 = 路径类.连接(项目根目录, "build")
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{build目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))


def 生成次要的包():
    import os
    import sys

    # 添加支持路径
    项目根目录 = os.path.dirname(__file__)
    sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy")
    from bxpy.系统包 import 系统类
    from bxpy.路径包 import 路径类
    from bxpy.进程包 import 子进程类

    # 删除pyarmor
    pyarmor目录路径 = 路径类.连接(项目根目录, "src\\bxgis\\common\\pyarmor_runtime_005556")
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{pyarmor目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))
    # 路径类.删除(bxgeo目录路径)

    # 删除bxgeo
    bxgeo目录路径 = 路径类.连接(项目根目录, "src\\bxgis\\common\\bxgeo")
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{bxgeo目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))
    # 路径类.删除(bxgeo目录路径)

    系统类.属性设置_当前工作目录("C:\\Users\\beixiao\\Project\\bxgeo")
    子程序 = 子进程类.子进程创建(f'"C:\\Program Files\\Python39\\Scripts\\pyarmor.exe" gen -O ..\\bxgis\\src\\bxgis\\common bxgeo')
    print(子进程类.输出获取_阻塞(子程序))

    # 删除bxpandas
    bxpandas目录路径 = 路径类.连接(项目根目录, "src\\bxgis\\common\\bxpandas")
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{bxpandas目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))

    系统类.属性设置_当前工作目录("C:\\Users\\beixiao\\Project\\bxpandas")
    子程序 = 子进程类.子进程创建(f'"C:\\Program Files\\Python39\\Scripts\\pyarmor.exe" gen -O ..\\bxgis\\src\\bxgis\\common bxpandas')
    print(子进程类.输出获取_阻塞(子程序))

    # 删除bxpy
    bxpy目录路径 = 路径类.连接(项目根目录, "src\\bxgis\\common\\bxpy")
    子程序 = 子进程类.子进程创建(f'rmdir /s /q "{bxpy目录路径}"')
    print(子进程类.输出获取_阻塞(子程序))

    系统类.属性设置_当前工作目录("C:\\Users\\beixiao\\Project\\bxpy")
    子程序 = 子进程类.子进程创建(f'"C:\\Program Files\\Python39\\Scripts\\pyarmor.exe" gen -O ..\\bxgis\\src\\bxgis\\common bxpy')
    print(子进程类.输出获取_阻塞(子程序))


def 包构建setuptools():
    import os
    from setuptools import setup, find_packages

    # def read(fname):
    #     return open(os.path.join(os.path.dirname(__file__), fname)).read()
    # print(find_packages(where="src").extend(find_packages(where="src/bxgis/common")))
    # print(find_packages(where="src/bxgis/common"))
    包名称列表 = find_packages(where="src")
    包名称列表.extend(find_packages(where="src/bxgis/common"))
    包路径字典 = {}
    for 包名称x in 包名称列表:
        if len(包名称x) >= 5 and 包名称x[0:5] == "bxgis":
            包路径字典[包名称x] = "src/bxgis"
        elif len(包名称x) >= 7 and 包名称x[0:7] == "bxarcpy":
            包路径字典[包名称x] = "src/bxgis/common/bxarcpy"
        elif len(包名称x) >= 5 and 包名称x[0:5] == "bxgeo":
            包路径字典[包名称x] = "src/bxgis/common/bxgeo"
        elif len(包名称x) >= 8 and 包名称x[0:8] == "bxpandas":
            包路径字典[包名称x] = "src/bxgis/common/bxpandas"
        elif len(包名称x) >= 4 and 包名称x[0:4] == "bxpy":
            包路径字典[包名称x] = "src/bxgis/common/bxpy"
        elif len(包名称x) >= 22 and 包名称x[0:22] == "pyarmor_runtime_005556":
            包路径字典[包名称x] = "src/bxgis/common/pyarmor_runtime_005556"
    print(包名称列表)
    print(包路径字典)

    setup(
        name="bxgis",
        version="0.0.1",
        description=("一个近期用于实现杭州详规入库数据库构建，远期用于协助国土空间规划编制的包。"),
        author="beixiao",
        author_email="vanadis91@163.com",
        url="https://github.com/vanadis91/bxgis",
        license="GPLv3",
        # long_description=read("Readme.txt"),
        python_requires="~=3.9",
        install_requires=[
            "shapely",
            "numpy",
            "pandas",
            "pypiwin32",
            "psutil",
            "setuptools",
            "pytest",
            "tinydb",
            "shortuuid",
            "tqdm",
            "colorama",
            "flask",
            "flask_login",
            "pymongo",
        ],
        packages=包名称列表,
        package_dir=包路径字典,
        package_data={
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
        script_args=["sdist", "bdist_wheel"],
    )


if __name__ == "__main__":
    # 生成次要的包()
    生成esri路径下文件()
    包构建setuptools()
