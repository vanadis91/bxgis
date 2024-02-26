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
    # script_args=["sdist", "bdist_wheel"],
)
# if __name__ == "__main__":
#     print(find_packages(where="src"))
