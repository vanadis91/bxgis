def main():
    import os
    import sys

    # 添加支持路径
    项目根目录 = os.path.dirname(__file__)
    sys.path.append(项目根目录 + "\\src")
    sys.path.append(项目根目录 + "\\src\\bxgis\\common")
    from bxpy import 系统

    # 重新生成esri路径下文件
    esri目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\esri")
    # 系统.路径.删除(esri目录路径)
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{esri目录路径}"')
    print(子程序.输出获取_阻塞())

    import arcpy

    pyt文件路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\bxgis.pyt")
    arcpy.gp.createtoolboxsupportfiles(pyt文件路径)  # type: ignore

    # 将pyt文件复制到toolboxes目录下
    toolboxes目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\esri\\toolboxes")
    系统.路径.复制(pyt文件路径, toolboxes目录路径)

    # 将xml文件移动到toolboxes目录下
    bxgis目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis")
    子路径下文件列表 = 系统.路径.子路径(bxgis目录路径)[2]
    for x in 子路径下文件列表:
        if len(x) >= 8 and x[0:5] == "bxgis" and x[-4:] == ".xml":
            子路径下文件完整路径_移动前 = 系统.路径.连接(项目根目录, "src\\bxgis", x)
            子路径下文件完整路径_移动后 = 系统.路径.连接(toolboxes目录路径, x)
            系统.路径.修改(子路径下文件完整路径_移动前, 子路径下文件完整路径_移动后)

    # 运行setuptools
    系统.终端.当前工作目录_修改(项目根目录)
    当前运行的解释器路径 = sys.executable

    子程序 = 系统.终端.子进程(f'"{当前运行的解释器路径}" setup.py sdist bdist_wheel')
    print(子程序.输出获取_阻塞())

    eggInfo目录路径 = 系统.路径.连接(项目根目录, "bxgis.egg-info")
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{eggInfo目录路径}"')
    print(子程序.输出获取_阻塞())

    build目录路径 = 系统.路径.连接(项目根目录, "build")
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{build目录路径}"')
    print(子程序.输出获取_阻塞())


def 生成次要的包():
    import os
    import sys

    # 添加支持路径
    项目根目录 = os.path.dirname(__file__)
    sys.path.insert(0, "C:\\Users\\beixiao\\Project\\bxpy")
    from bxpy import 系统

    # 删除pyarmor
    pyarmor目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\common\\pyarmor_runtime_005556")
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{pyarmor目录路径}"')
    print(子程序.输出获取_阻塞())
    # 系统.路径.删除(bxgeo目录路径)

    # 删除bxgeo
    bxgeo目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\common\\bxgeo")
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{bxgeo目录路径}"')
    print(子程序.输出获取_阻塞())
    # 系统.路径.删除(bxgeo目录路径)

    系统.终端.当前工作目录_修改("C:\\Users\\beixiao\\Project\\bxgeo")
    子程序 = 系统.终端.子进程(f'"C:\\Program Files\\Python39\\Scripts\\pyarmor.exe" gen -O ..\\bxgis\\src\\bxgis\\common bxgeo')
    print(子程序.输出获取_阻塞())

    # 删除bxpandas
    bxpandas目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\common\\bxpandas")
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{bxpandas目录路径}"')
    print(子程序.输出获取_阻塞())

    系统.终端.当前工作目录_修改("C:\\Users\\beixiao\\Project\\bxpandas")
    子程序 = 系统.终端.子进程(f'"C:\\Program Files\\Python39\\Scripts\\pyarmor.exe" gen -O ..\\bxgis\\src\\bxgis\\common bxpandas')
    print(子程序.输出获取_阻塞())

    # 删除bxpy
    bxpy目录路径 = 系统.路径.连接(项目根目录, "src\\bxgis\\common\\bxpy")
    子程序 = 系统.终端.子进程(f'rmdir /s /q "{bxpy目录路径}"')
    print(子程序.输出获取_阻塞())

    系统.终端.当前工作目录_修改("C:\\Users\\beixiao\\Project\\bxpy")
    子程序 = 系统.终端.子进程(f'"C:\\Program Files\\Python39\\Scripts\\pyarmor.exe" gen -O ..\\bxgis\\src\\bxgis\\common bxpy')
    print(子程序.输出获取_阻塞())


if __name__ == "__main__":
    # 生成次要的包()
    main()
