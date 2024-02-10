import os
from setuptools import setup


# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="bxgis",
    version="0.0.1",
    author="beixiao",
    author_email="vanadis91@163.com",
    description=("一个用于便捷实现杭州详规入库数据库构建的包。"),
    # long_description=read("Readme.txt"),
    python_requires="~=3.9",
    install_requires=[
        "requests",
    ],
    packages=["bxgis"],
    package_data={"bxgis": ["esri/toolboxes/*", "esri/arcpy/*", "esri/help/gp/*", "esri/help/gp/toolboxes/*", "esri/help/gp/messages/*"]},
)
