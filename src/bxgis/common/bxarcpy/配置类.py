from bxpy import 日志
try:
    import arcpy
except Exception as e:
    pass


class _配置类:
    _单例对象 = None

    def __new__(cls, *args, **kwargs):
        if cls._单例对象 is None:
            cls._单例对象 = super().__new__(cls)
        return cls._单例对象

    def __init__(self) -> None:
        pass

    @property
    def 是否覆盖输出要素(self):
        return arcpy.env.overwriteOutput

    @是否覆盖输出要素.setter
    def 是否覆盖输出要素(self, boolen):
        arcpy.env.overwriteOutput = boolen

    @property
    def 当前工作空间(self):
        return arcpy.env.workspace

    @当前工作空间.setter
    def 当前工作空间(self, 工作空间路径=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"):
        arcpy.env.workspace = 工作空间路径


配置 = _配置类()
