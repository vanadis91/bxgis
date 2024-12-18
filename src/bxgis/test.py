class common_importFromCAD(object):
    def __init__(self):
        self.label = "导入从CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = "常用"

    def getParameterInfo(self):
        args_dict_list = [
            {"name": "输入CAD数据集中的要素类路径", "dataType": "要素类", "required": "必填", "argsDirction": "输入参数", "multiValue": False},
            {"name": "是否拓扑检查", "dataType": "布尔值", "required": "必填", "argsDirction": "输入参数", "multiValue": False, "default": False},
            {"name": "是否范围检查", "dataType": "布尔值", "required": "必填", "argsDirction": "输入参数", "multiValue": False, "default": False},
            {"name": "是否转曲", "dataType": "布尔值", "required": "必填", "argsDirction": "输入参数", "multiValue": False, "default": False},
            {"name": "输出要素路径", "dataType": "要素类", "required": "必填", "argsDirction": "输出参数", "multiValue": False, "default": "YD_CAD色块"},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run("bxgis.常用.导入从CAD", "导入从CAD", parameterList)
