from bxpy.日志包 import 日志生成器
import arcpy
from typing import Union, Literal, Any, List, Dict, Optional, TypedDict

# from pydantic import BaseModel


class 环境类:
    @staticmethod
    def 属性获取_是否覆盖输出要素():
        return arcpy.env.overwriteOutput

    @staticmethod
    def 属性设置_是否覆盖输出要素(boolen):
        arcpy.env.overwriteOutput = boolen

    @staticmethod
    def 属性获取_当前工作空间():
        return arcpy.env.workspace  # type: ignore

    @staticmethod
    def 属性设置_当前工作空间(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"):
        arcpy.env.workspace = 工作空间  # type: ignore

    @staticmethod
    def 属性获取_当前临时工作空间():
        return arcpy.env.scratchWorkspace  # type: ignore


class 环境管理器类:
    @staticmethod
    def 环境管理器类创建(工作空间, 临时工作空间="默认", 输出包含M值="Disabled", 输出包含Z值="Disabled", XY分辨率=0.0001, XY容差=0.001, 是否覆盖输出要素=True, **kwargs):
        _参数映射 = {
            "临时工作空间": "scratchWorkspace",
            "工作空间": "workspace",
            "输出包含M值": "outputMFlag",
            "输出包含Z值": "outputZFlag",
            "XY分辨率": "XYResolution",
            "XY容差": "XYTolerance",
        }

        kwargsTemp = {}
        for key, value in kwargs.items():
            if key in _参数映射:
                kwargsTemp[_参数映射[key]] = value
            else:
                kwargsTemp[key] = value
        kwargs = kwargsTemp

        kwargs["workspace"] = 工作空间

        if 临时工作空间 == "默认":
            from bxpy.路径包 import 路径类
            from bxarcpy.数据库包 import 数据库类

            目录 = 路径类.属性获取_目录(工作空间)
            文件名 = 路径类.属性获取_文件名_去扩展名(工作空间)

            临时工作空间路径 = 路径类.连接(目录, f"{文件名}_临时.gdb")
            if not 路径类.是否存在(临时工作空间路径):
                kwargs["scratchWorkspace"] = 数据库类.数据库创建(目录, f"{文件名}_临时.gdb")
            else:
                kwargs["scratchWorkspace"] = 临时工作空间路径
        else:
            kwargs["scratchWorkspace"] = 临时工作空间

        kwargs["outputMFlag"] = 输出包含M值
        kwargs["outputZFlag"] = 输出包含Z值
        kwargs["XYResolution"] = XY分辨率
        kwargs["XYTolerance"] = XY容差
        环境类.属性设置_是否覆盖输出要素(是否覆盖输出要素)

        return arcpy.EnvManager(**kwargs)


class 输入输出类:
    @staticmethod
    def 输入参数获取_以字符串形式(索引, 默认值="", 是否去除路径=False):
        from bxarcpy.环境包 import 输入输出类

        x: str = arcpy.GetParameterAsText(索引)  # type: ignore
        if x == "":
            x = 默认值
        if 是否去除路径:
            x = x.split("\\")[-1]
        输入输出类.输出消息(f"参数{索引}为：{x}")
        return x

    @staticmethod
    def 输出消息(x, 级别: Literal["调试", "信息", "警告", "错误", "危险"] = "信息"):
        if 日志生成器.属性获取_当前函数内日志开启状态():
            日志生成器.输出(级别=级别, 内容=x)
        else:
            内容 = 日志生成器.输出("信息", x, 是否开启=True, 输出是否着色=False, 输出流对象=None)
            arcpy.AddMessage(内容)
        # print(x)


if __name__ == "__main__":
    from bxpy.路径包 import 路径类

    目录 = 路径类.属性获取_目录(r"C:\Users\beixiao\Project\J江东区临江控规\临江控规_数据库.gdb")
    文件名 = 路径类.属性获取_文件名_去扩展名(r"C:\Users\beixiao\Project\J江东区临江控规\临江控规_数据库.gdb")
    print(文件名)
