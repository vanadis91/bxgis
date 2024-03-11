from bxpy import 日志

try:
    import arcpy
except Exception as e:
    pass


class 环境:
    class 环境管理器(object):
        def __init__(self, 工作空间, 临时工作空间=None, 输出包含M值="Disabled", 输出包含Z值="Disabled", XY分辨率=0.0001, XY容差=0.001, 是否覆盖输出要素=True, **kwargs):
            _参数映射 = {"临时工作空间": "scratchWorkspace", "scratchWorkspace": "scratchWorkspace", "工作空间": "workspace", "workspace": "workspace", "输出包含M值": "outputMFlag", "outputMFlag": "outputMFlag", "输出包含Z值": "outputZFlag", "outputZFlag": "outputZFlag", "XYResolution": "XYResolution", "XY分辨率": "XYResolution", "XYTolerance": "XYTolerance", "XY容差": "XYTolerance"}
            kwargsTemp = {}
            for key, value in kwargs.items():
                kwargsTemp[_参数映射[key]] = value
            kwargs = kwargsTemp
            kwargs["outputMFlag"] = 输出包含M值
            kwargs["outputZFlag"] = 输出包含Z值
            kwargs["XYResolution"] = XY分辨率
            kwargs["XYTolerance"] = XY容差
            if 临时工作空间 is None:
                kwargs["scratchWorkspace"] = 工作空间
            else:
                kwargs["scratchWorkspace"] = 临时工作空间
            kwargs["workspace"] = 工作空间
            from .配置类 import 配置

            配置.是否覆盖输出要素 = 是否覆盖输出要素

            self._original_envs = {}
            self._environments = kwargs

        def __enter__(self):
            envs = list(arcpy.env._environments) + ["autoCancelling", "overwriteOutput"]

            # Handle invalid keys and read-only environments
            for k in self._environments.keys():
                if k not in envs:
                    msg = arcpy.GetIDMessage(87059).replace("%1", "%s") % k
                    raise AttributeError(msg)
                elif k in ["scratchGDB", "scratchFolder"]:
                    msg = arcpy.GetIDMessage(87064).replace("%1", "%s") % k
                    raise AttributeError(msg)

            for k, v in self._environments.items():
                if k in envs:
                    self._original_envs[k] = getattr(arcpy.env, k)
                    setattr(arcpy.env, k, v)

        def __exit__(self, exc_type, exc_value, traceback):
            self.reset()

        def reset(self):
            for k, v in self._original_envs.items():
                setattr(arcpy.env, k, v)

    @staticmethod
    def 输入参数获取_以字符串形式(索引, 默认值="", 是否去除路径=False):
        x = arcpy.GetParameterAsText(索引)
        if x == "":
            x = 默认值
        if 是否去除路径:
            x = x.split("\\")[-1]
        环境.输出消息(f"参数{索引}为：{x}")
        return x

    @staticmethod
    def 输出消息(x):
        arcpy.AddMessage(x)
        # print(x)
