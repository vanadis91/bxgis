import arcpy


class 环境管理器(object):
    def __init__(self, 输出包含M值="Disabled", 输出包含Z值="Disabled", **kwargs):
        参数映射 = {"临时工作空间": "scratchWorkspace", "scratchWorkspace": "scratchWorkspace", "工作空间": "workspace", "workspace": "workspace", "输出包含M值": "outputMFlag", "outputMFlag": "outputMFlag", "输出包含Z值": "outputZFlag", "outputZFlag": "outputZFlag"}
        kwargsTemp = {}
        for key, value in kwargs.items():
            kwargsTemp[参数映射[key]] = value
        kwargs = kwargsTemp
        kwargs["outputMFlag"] = 输出包含M值
        kwargs["outputZFlag"] = 输出包含Z值

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
