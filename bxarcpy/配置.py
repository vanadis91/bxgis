import arcpy


def 是否覆盖输出要素(是否覆盖输出要素):
    arcpy.env.overwriteOutput = 是否覆盖输出要素


def 设置当前工作空间(工作空间路径=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"):
    arcpy.env.workspace = 工作空间路径


def 获取参数_字符串形式(索引):
    return arcpy.GetParameterAsText(索引)


# class 配置:
#     def __init__(self) -> None:
#         self.内嵌对象 = arcpy.env

#     @property
#     def 覆盖输出要素(self):
#         return self.内嵌对象.overwriteOutput

#     @覆盖输出要素.setter
#     def 覆盖输出要素(self, boolen):
#         self.内嵌对象.overwriteOutput = boolen
