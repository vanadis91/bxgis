class common_importFromCAD(object):
    def __init__(self):
        self.label = "�����CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = "����"

    def getParameterInfo(self):
        args_dict_list = [
            {"name": "����CAD���ݼ��е�Ҫ����·��", "dataType": "Ҫ����", "required": "����", "argsDirction": "�������", "multiValue": False},
            {"name": "�Ƿ����˼��", "dataType": "����ֵ", "required": "����", "argsDirction": "�������", "multiValue": False, "default": False},
            {"name": "�Ƿ�Χ���", "dataType": "����ֵ", "required": "����", "argsDirction": "�������", "multiValue": False, "default": False},
            {"name": "�Ƿ�ת��", "dataType": "����ֵ", "required": "����", "argsDirction": "�������", "multiValue": False, "default": False},
            {"name": "���Ҫ��·��", "dataType": "Ҫ����", "required": "����", "argsDirction": "�������", "multiValue": False, "default": "YD_CADɫ��"},
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run("bxgis.����.�����CAD", "�����CAD", parameterList)
