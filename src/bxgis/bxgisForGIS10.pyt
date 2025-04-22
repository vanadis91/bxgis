# -- coding:cp936 �C
import arcpy
# -*- coding: gbk -*-

data_type_map = {
    u"Ҫ��ͼ��".encode('gbk'): "GPFeatureLayer",
    u"Ҫ����".encode('gbk'): "DEFeatureClass",
    u"����ֵ".encode('gbk'): "GPBoolean",
    u"˫����".encode('gbk'): "GPDouble",
    u"�ֶ�".encode('gbk'): "Field",
    u"������".encode('gbk'): "GPLong",
    u"�ַ���".encode('gbk'): "GPString",
    u"��".encode('gbk'): "DETable",
    u"�����ռ�".encode('gbk'): "DEWorkspace",
    u"ֵ��".encode('gbk'): "GPValueTable",
    u"�ļ�".encode('gbk'): "DEFile",
    u"�ļ���".encode('gbk'): "DEFolder",
    u"�����ļ�".encode('gbk'): "GPDataFile",
    u"CAD���ݼ�".encode('gbk'): "DECadDrawingDataset",
    u"����".encode('gbk'): "GPVariant",
    u"�κ�ֵ".encode('gbk'): "GPType",
}
required_map = {
    u"����".encode('gbk'): "Required",
    u"ѡ��".encode('gbk'): "Optional",
    u"���ص��������".encode('gbk'): "Derived",
}
args_type_map = {
    u"�������".encode('gbk'): "Input",
    u"�������".encode('gbk'): "Output",
}

# def get_prj_info():
#     # ��ȡ��Ŀ��Ϣ
#     import os
#     import yaml
#     toml_file_path = os.path.join(os.path.dirname(__file__),u'����',u'��Ŀ��Ϣ.toml')
#     with open(toml_file_path,mode='r')as f:
#         return yaml.load(f)
def get_registry_value(key_path, value_name):
    import _winreg as winreg
    # ��ע�����
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        # ��ȡָ�����Ƶ�ֵ
        value, regtype = winreg.QueryValueEx(key, value_name)
        # �ر�ע�����
        winreg.CloseKey(key)
        return value
    
    except WindowsError as e:
        raise Exception(u"�޷��ҵ�arcgis_pro�İ�װ·��".encode('gbk'))

def add_search_path():
    # Ϊpy3�İ�����·������ӱ���Ŀ
    import os
    import shutil
    arcgis_pro_install_dir = get_registry_value(r"SOFTWARE\ESRI\ArcGISPro",'InstallDir')
    pkg_search_path = os.path.join(arcgis_pro_install_dir,'bin','Python','envs','arcgispro-py3','Lib','site-packages')
    com_pth_path_from = os.path.join(os.path.dirname(__file__),u'com.pth')
    com_pth_path_to = os.path.join(pkg_search_path,u'com.pth')
    if not os.path.isfile(com_pth_path_to):
        shutil.copy2(com_pth_path_from, com_pth_path_to)
    else:
        try:
            os.remove(com_pth_path_to)
            shutil.copy2(com_pth_path_from, com_pth_path_to)
        except Exception as e:
            print(u"�޷�ɾ��ԭ�е�com.pth".encode('gbk'))

add_search_path()

def fun_run(module_name, function_name, args_list):
    import subprocess
    import json
    import os
    import arcpy

    args_dict = ParameterCls.convert_to_dictRawValue(args_list)
    args_dict_str = json.dumps(args_dict,ensure_ascii=False)

    run_cli_dict={
        u'ģ������'.encode('gbk'): module_name.encode('gbk'),
        u'��������'.encode('gbk'): function_name.encode('gbk'),
        u'�����ֵ�'.encode('gbk'): args_dict_str,
        u'��ǰ�����ռ�'.encode('gbk'): arcpy.env.workspace.encode('gbk'),
    }

    args_path = os.path.join(os.path.dirname(__file__),u'������',u'�����в���.json')
    with open(args_path,mode='w')as f:
        json.dump(run_cli_dict, f, ensure_ascii=False, indent=4)

    arcgis_pro_install_dir = get_registry_value(r"SOFTWARE\ESRI\ArcGISPro",'InstallDir')
    interpreter_path = os.path.join(arcgis_pro_install_dir,'bin','Python','envs','arcgispro-py3','python.exe')
    str = u"\"{}\" -m bxgis.������.�����а�".format(interpreter_path)
    process = subprocess.Popen(str.encode('gbk'))
    return None

class ParameterCls:
    @staticmethod
    def parameterCreate_muti(args_dict_list):
        ret_list = []
        for args_dict in args_dict_list:
            a = ParameterCls.parameterCreate(**args_dict)
            ret_list.append(a)
        return ret_list

    @staticmethod
    def parameterCreate(
        name=u'δָ��',
        dataType=u'Ҫ��ͼ��',
        discription=None,
        required=u"ѡ��",
        argsDirction=u"�������",
        multiValue=False,
        enabled=True,
        default=None,
        dependenciesParameterNameList=None,
        parameterOptionType=None,
        parameterOptionList=None,
    ):
        name = name.encode('gbk')
        dataTypeRaw = data_type_map.get(dataType.encode('gbk'),dataType)
        requiredRaw = required_map.get(required.encode('gbk'),required) 
        directionRaw = args_type_map.get(argsDirction.encode('gbk'),argsDirction) 
        discription = name if discription is None else discription
        ret = arcpy.Parameter(
            name=name,
            displayName=discription,
            direction=directionRaw,
            datatype=dataTypeRaw,
            parameterType=requiredRaw,
            enabled=enabled,
            multiValue=multiValue,
        )

        if default:
            ParameterCls.attrSet_value(ret, default)

        if dependenciesParameterNameList:
            ParameterCls.attrGet_dependencies(ret, dependenciesParameterNameList)

        if parameterOptionType == "ValueList":
            ret.filter.type = "ValueList"
        elif parameterOptionType == "Range":
            ret.filter.type = "Range"
        if parameterOptionType and parameterOptionList:
            valueRaw = [x for x in parameterOptionList]
            ret.filter.list = valueRaw
        return ret

    @staticmethod
    def attrGet_value(parameterObject):
        return parameterObject.value

    @staticmethod
    def attrSet_value(parameterObject, value):
        parameterObject.value = value  # type: ignore

    @staticmethod
    def attrGet_valueAsText(parameterObject):
        return parameterObject.valueAsText

    @staticmethod
    def attrGet_name(parameterObject):
        return parameterObject.name

    @staticmethod
    def attrGet_enabled(parameterObject, boolen):
        parameterObject.enabled = boolen  # type: ignore

    @staticmethod
    def attrGet_dependencies(parameterObject, parameterNameList):
        parameterObject.parameterDependencies = parameterNameList  # type: ignore

    @staticmethod
    def attrGet_filter(parameterObject):
        return parameterObject.filter  # type: ignore

    class FilterCls:
        @staticmethod
        def attrSet_type(filterObject, type):
            typeRaw = type
            filterObject.type = typeRaw  # type: ignore

        @staticmethod
        def attrSet_value(filterObject, value):
            valueRaw = [x for x in value]
            filterObject.list = valueRaw

    @staticmethod
    def convert_to_listRawValue(parameterList):
        def getRawValue(parameterObject):
            if type(ParameterCls.attrGet_value(parameterObject)) in [int, float, str, bool]:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif ParameterCls.attrGet_value(parameterObject) is None:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif type(ParameterCls.attrGet_value(parameterObject)) is list:
                ret = [getRawValue(x) for x in parameterObject]
            else:
                ret = ParameterCls.attrGet_valueAsText(parameterObject)
            return ret
        
        patameterListTemp = []
        for x in parameterList:
            patameterListTemp.append(getRawValue(x))
        return patameterListTemp
    
    @staticmethod
    def convert_to_dictRawValue(parameterList):
        parameterNameList = [ParameterCls.attrGet_name(x).encode('gbk') for x in parameterList]
        parameterDict = {k: v for k, v in zip(parameterNameList, parameterList)}
        patameterDictTemp = {}

        def getRawValue(parameterObject):
            if type(ParameterCls.attrGet_value(parameterObject)) in [int, float, bool]:
                ret = ParameterCls.attrGet_value(parameterObject)
            elif type(ParameterCls.attrGet_value(parameterObject)) is str:
                ret = ParameterCls.attrGet_value(parameterObject).encode('gbk')
            elif type(ParameterCls.attrGet_value(parameterObject)) is list:
                ret = [getRawValue(x) for x in parameterObject]
            elif ParameterCls.attrGet_value(parameterObject) is None:
                ret = ParameterCls.attrGet_value(parameterObject)
            else:
                ret = ParameterCls.attrGet_valueAsText(parameterObject).encode('gbk')
            return ret

        for k, v in parameterDict.items():
            patameterDictTemp[k] = getRawValue(v)
        return patameterDictTemp

    @staticmethod
    def convert_to_dict(parameterList):
        parameterNameList = [ParameterCls.attrGet_name(x) for x in parameterList]
        parameterDict = {k: v for k, v in zip(parameterNameList, parameterList)}
        return parameterDict


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file) �����˹����������"""
        self.label = "BXGIS������"  # �����ǩ
        self.alias = "BXGIS������"  # �������

        # List of tool classes associated with this toolbox
        self.tools = [ru_ku_dan_yuan, ru_ku_tu_ze, ru_ku_ju_diao_ru_ku, ru_ku_gong_ye_pian_qu, ru_ku_kong_zhi_xian, ru_ku_cun_zhuang_jian_she_bian_jie, ru_ku_yong_tu_fen_qu, ru_ku_jie_qu_jie_fang_fen_cun, ru_ku_gui_hua_di_kuai, ru_ku_she_shi, ru_ku_dan_yuan_de_qing, ru_ku_kong_zhi_xian_de_qing_di_kuai_hou_tui_xian, ru_ku_kong_zhi_xian_de_qing_te_shu_fan_wei_xian, ru_ku_kong_zhi_xian_de_qing_dao_lu_zhong_xian, ru_ku_kong_zhi_xian_de_qing_dao_lu_bian_xian, ru_ku_gui_hua_di_kuai_de_qing, ru_ku_gui_hua_di_kuai_de_qing_shui_yu, ru_ku_gui_hua_di_kuai_de_qing_dao_lu, ru_ku_she_shi_de_qing, yong_tu_fen_qu_bian_hao_sheng_cheng, yong_tu_fen_qu_gui_hua_tu_sheng_cheng, yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_fen_qu, qu_chu_zi_duan_zhong_suo_you_kong_ge, qu_yu_geng_xin, qu_yu_jian_cha, qu_yu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_qu_yu, dao_ru_shu_xing_biao, shu_xing_dui_bi, zuo_biao_xi_tong_yi, zi_duan_ming_cheng_xiao_xie_gai_da_xie, dao_ru_cong_CAD, dao_chu_dao_CAD, shu_xing_yu_xiu_fu, yao_su_chuang_jian_tong_guo_geng_xin_gen_ju_mian, shu_ju_jian_cha, qu_zhuan_zhe, qing_li_li_shi_yao_su, tong_ji, yao_su_lian_he, yong_di_die_he_tu_sheng_cheng, yong_di_ji_qi_tu_sheng_cheng, yong_di_geng_xin, yong_di_xian_zhuang_tu_sheng_cheng, yong_di_gui_hua_tu_sheng_cheng, yong_di_chuang_jian_sheng_cheng_yong_di_tiao_zheng_tu, kai_fa_bian_jie_nei_gong_ye_yong_di, yong_di_ji_suan_tiao_zheng_lei_xing, jian_cha_di_kuai_bian_hao_he_tu_di_ma_shi_fou_you_wen_ti, di_lei_bian_hao_ming_cheng_bie_cheng_pi_pei_jian_cha, ji_ben_nong_tian_shi_fou_bei_zhan, kai_fa_bian_jie_wai_cheng_zhen_jian_she_yong_di_jian_cha, yong_di_he_gui_xing_jian_cha, chu_bu_ji_shu_zhuan_huan_san_diao, chu_bu_ji_shu_zhuan_huan_er_diao, zi_duan_chu_li_bing_sheng_cheng_fen_xiang_san_diao, zi_duan_chu_li_bing_sheng_cheng_fen_xiang_er_diao, di_lei_zhuan_huan_cheng_xiang_di_lei_zhuan_guo_kong_di_lei, di_lei_zhuan_huan_jiu_ban_guo_kong_di_lei_zhuan_xin_ban_guo_kong_di_lei, yong_di_gong_ju_ji_geng_xin_dui_xiang_shu_xing, yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_yong_di, yong_di_chuang_jian_tong_guo_gen_ju_di_lei_ming_cheng_sheng_cheng_bian_hao, yong_di_gong_ju_ji_yong_di_shu_ju_tong_ji, tong_ji_kai_fa_bian_jie_wai_ji_qi_203_yong_di, yong_di_chuang_jian_tong_guo_ji_suan_liang_ke_yong_di, ji_suan_wen_ben_lian_jie_yong_shu_ju, she_shi_geng_xin, she_shi_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_she_shi, he_dao_bian_xian_sheng_cheng, dao_lu_bian_xian_sheng_cheng, dao_lu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_kong_zhi_xian, dao_lu_hong_xian_ti_qu, di_kuai_zhi_biao_ce_suan_biao_huo_qu, huo_qu_gong_zuo_kong_jian, xiang_mu_chu_shi_hua,]

# class common_importFromCAD(object): 
#     def __init__(self):
#         self.label = u"�����CAD"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"����"

#     def getParameterInfo(self):
#         args_dict_list = [
#             {"name": u"����CAD���ݼ��е�Ҫ����·��", "dataType": u"Ҫ����", "required": u'����', "argsDirction": u"�������",'multiValue': False},
#             {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':False},
#             {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':False},
#             {"name": u"�Ƿ�ת��", "dataType": u"����ֵ", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':False},
#             {"name": u"���Ҫ��·��", "dataType": u"Ҫ����", "required": u'����', "argsDirction": u"�������",'multiValue': False,'default':u'YD_CADɫ��'},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.����.�����CAD',u'�����CAD',parameterList)

# class common_curveToPolyline(object): 
#     # "��ת��"
#     def __init__(self):
#         self.label = u"��ת��"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"����"

#     def getParameterInfo(self):
#         # init_addSearchPath()
#         # from bxgis.���� import ������Ϣ
#         args_dict_list = [
#             {"name": u"����Ҫ��·���б�", "dataType": u"Ҫ����", "required": u'����', "argsDirction": u"�������",'multiValue': True},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     # def isLicensed(self):
#     #     """Set whether tool is licensed to execute."""
#     #     return True

#     # def updateParameters(self, �����б�):
#     #     init_addSearchPath()
#     #     import bxgis.����.������CAD as ������CAD

#     #     return ������CAD.������.������������(�����б�)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.����.��ת��',u'��ת��',parameterList)

#     # def updateMessages(self, parameters):
#     #     """Modify the messages created by internal validation for each tool
#     #     parameter.  This method is called after internal validation."""
#     #     return

# class config_projectInit(object): 
#     def __init__(self):
#         self.label = u"��Ŀ��ʼ��"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"����"

#     def getParameterInfo(self):
#         args_dict_list = [
#             {"name": u"��Ŀ�ļ���·��", "dataType": u"�ļ���", "required": u'����', "argsDirction": u"�������",'multiValue': False},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.����.��Ŀ��ʼ��',u'��Ŀ��ʼ��',parameterList)

class ru_ku_dan_yuan(object):
    # ���_��Ԫ
    def __init__(self):
        self.label = u"���_��Ԫ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"��Ԫ���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���Ƶ�λ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�˿ڹ�ģ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�絥Ԫƽ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHFW'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_��Ԫ", u"���_��Ԫ", parameterList)
    
class ru_ku_tu_ze(object):
    # ���_ͼ��
    def __init__(self):
        self.label = u"���_ͼ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"ͼ�����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [{'���ʹ���': 'JZHTX-GC', '��������': '����������-�߲�', 'Ҫ��·��': 'TZ_�����߲������', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'JZHTX-DC', '��������': '����������-���', 'Ҫ��·��': 'TZ_������������', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'JKKD', '��������': '�����ڶ�', 'Ҫ��·��': 'TZ_��ֹ������������', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'JDCCRK', '��������': '�����������', 'Ҫ��·��': 'TZ_���������ڷ���', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'JGLDKZX', '��������': '�����ȵ�������', 'Ҫ��·��': 'TZ_�����ȵ�������', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'ZYJM', '��������': '��Ҫ����', 'Ҫ��·��': 'TZ_��Ҫ����', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'DKLTD', '��������': '�ؿ���ͨ��', 'Ҫ��·��': 'TZ_�ؿ���ͨ��', '�ֶ�ӳ��': [['ͨ�����', 'GKYQ'], ['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'QTTZX', '��������': '����ͼ����', 'Ҫ��·��': 'TZ_����ͼ����', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}]},
            {"name": u"ͼ�����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [{'���ʹ���': 'DKGDFQ', '��������': '�ؿ�߶ȷ���', 'Ҫ��·��': 'TZ_�ؿ�߶ȷ���', '�ֶ�ӳ��': [['�����߶�', 'GKYQ'], ['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'GGKCKJ', '��������': '���������ռ�', 'Ҫ��·��': 'TZ_���������ռ�', '�ֶ�ӳ��': [['�ܿ�Ҫ��', 'GKYQ'], ['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'DXKJGKM', '��������': '���¿ռ�ܿ���', 'Ҫ��·��': 'TZ_���¿ռ�ܿ���', '�ֶ�ӳ��': [['�ܿ�Ҫ��', 'GKYQ'], ['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'QTTZM', '��������': '����ͼ����', 'Ҫ��·��': 'TZ_����ͼ����', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}]},
            {"name": u"ͼ����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [{'���ʹ���': 'DBJZ', '��������': '�ر꽨��', 'Ҫ��·��': 'TZ_�ر꽨��', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'ZYSD', '��������': '��Ҫ�ӵ�', 'Ҫ��·��': 'TZ_��Ҫ�ӵ�', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}, {'���ʹ���': 'QTTZD', '��������': '����ͼ���', 'Ҫ��·��': 'TZ_����ͼ���', '�ֶ�ӳ��': [['�ܿ�����', 'GKLD'], ['��ע', 'BZ']]}]},
            {"name": u"���Ҫ�������ֵ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"{'��': 'XG_TZX', '��': 'XG_TZM', '��': 'XG_TZD'}"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_ͼ��", u"���_ͼ��", parameterList)
    
class ru_ku_ju_diao_ru_ku(object):
    # ���_�ֵ����
    def __init__(self):
        self.label = u"���_�ֵ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AA_�滮��ҵ�õ�'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_�ֵ�", u"���_�ֵ����", parameterList)
    
class ru_ku_gong_ye_pian_qu(object):
    # ���_��ҵƬ��
    def __init__(self):
        self.label = u"���_��ҵƬ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��ҵƬ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_��ҵƬ����Χ��'},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GYPQ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_��ҵƬ��", u"���_��ҵƬ��", parameterList)
    
class ru_ku_kong_zhi_xian(object):
    # ���_������
    def __init__(self):
        self.label = u"���_������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�ؿ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"��·����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DL_��·����'},
            {"name": u"��·����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DL_��·����'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_KZX'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_������", u"���_������", parameterList)
    
class ru_ku_cun_zhuang_jian_she_bian_jie(object):
    # ���_��ׯ����߽�
    def __init__(self):
        self.label = u"���_��ׯ����߽�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��ׯ����߽�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_��ׯ����߽�'},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"��Ԫ���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'QT12'},
            {"name": u"�Ƿ��ںϲ��ಿ���䵥����", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�ܿ�Ҫ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'���ա����õ��ߡ��������ۡ���Ԫͳ�Ԥ�����ԡ�������������ԭ����п��ƣ��ۺϿ��Ǵ�ׯ�ּ������뽨���õ�ָ�갲�ţ��������ռ��ʶȼ���'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_JSBJ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_��ׯ����߽�", u"���_��ׯ����߽�", parameterList)
    
class ru_ku_yong_tu_fen_qu(object):
    # ���_��;����
    def __init__(self):
        self.label = u"���_��;����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_��;����ͼ'},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"��Ԫ���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'QT12'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_YTFQ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_��;����", u"���_��;����", parameterList)
    
class ru_ku_jie_qu_jie_fang_fen_cun(object):
    # ���_�����ַ��ִ�
    def __init__(self):
        self.label = u"���_�����ַ��ִ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ�������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['JX_������Χ��', 'JX_�ַ���Χ��']},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"�㼶�б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['����', '�ַ�']},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'������'},
            {"name": u"�������������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'������������'},
            {"name": u"�ܳ����ס�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܳ����ס����'},
            {"name": u"�ܽ�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܽ������'},
            {"name": u"��סլ��������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'��סլ�������'},
            {"name": u"�ܹ�ҵ��������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܹ�ҵ�������'},
            {"name": u"���̷���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'���̷��������'},
            {"name": u"�ܴ�ׯ���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܴ�ׯ��������'},
            {"name": u"�ܴ�ׯ��ס�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܴ�ׯ��ס����'},
            {"name": u"�ܸ��ر������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܸ��ر�����'},
            {"name": u"�����û���ũ���õ�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�����û���ũ���õ����'},
            {"name": u"����̬���������õ�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'����̬���������õ����'},
            {"name": u"�ܴ�ׯ����߽��õ�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܴ�ׯ����߽��õ����'},
            {"name": u"�ܳ��罨���õ�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܳ��罨���õ����'},
            {"name": u"�ܴ�ׯ�����õ�����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ܴ�ׯ�����õ����'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_JQJF'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_�����ַ��ִ�", u"���_�����ַ��ִ�", parameterList)
    
class ru_ku_gui_hua_di_kuai(object):
    # ���_�滮�ؿ�
    def __init__(self):
        self.label = u"���_�滮�ؿ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"�������ʩ�����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": u"������Ϣ.��Ŀ��Ϣ.�������ʩ�����б�"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_�滮�ؿ�", u"���_�滮�ؿ�", parameterList)
    
class ru_ku_she_shi(object):
    # ���_��ʩ
    def __init__(self):
        self.label = u"���_��ʩ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��ʩҪ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'SS_������ʩ'},
            {"name": u"��Ԫ����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ٽ���Ԫ'},
            {"name": u"����ʱ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�����ĺ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_PTSS'},
            {"name": u"�������ʩ�����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": u"������Ϣ.��Ŀ��Ϣ.�������ʩ�����б�"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_��ʩ", u"���_��ʩ", parameterList)
    
class ru_ku_dan_yuan_de_qing(object):
    # ���_��Ԫ_����
    def __init__(self):
        self.label = u"���_��Ԫ_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��ԪҪ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_�ع浥Ԫ'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_�ع浥Ԫ1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_��Ԫ_����", u"���_��Ԫ_����", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_di_kuai_hou_tui_xian(object):
    # ���_������_����_�ؿ������
    def __init__(self):
        self.label = u"���_������_����_�ؿ������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_������_���'},
            {"name": u"�߲������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_������_�߲�'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_�ؿ������'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_�ؿ������1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_������_����_�ؿ������", u"���_������_����_�ؿ������", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_te_shu_fan_wei_xian(object):
    # ���_������_����_���ⷶΧ��
    def __init__(self):
        self.label = u"���_������_����_���ⷶΧ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"������Ҫ��·���б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['GZW_��λ�����̵�', 'GZW_��λ���Ƶ�·', 'GZW_�õع�������', 'GZW_�߶ȷ�����']},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_���ⷶΧ��'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_���ⷶΧ��1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_������_����_���ⷶΧ��", u"���_������_����_���ⷶΧ��", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_dao_lu_zhong_xian(object):
    # ���_������_����_��·����
    def __init__(self):
        self.label = u"���_������_����_��·����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��·Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DL_��·����'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_��·������'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_��·������1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_������_����_��·����", u"���_������_����_��·����", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_dao_lu_bian_xian(object):
    # ���_������_����_��·����
    def __init__(self):
        self.label = u"���_������_����_��·����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_��·����'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_��·����1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_������_����_��·����", u"���_������_����_��·����", parameterList)
    
class ru_ku_gui_hua_di_kuai_de_qing(object):
    # ���_�滮�ؿ�_����
    def __init__(self):
        self.label = u"���_�滮�ؿ�_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_�ع�ؿ�'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_�ع�ؿ�1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_�滮�ؿ�_����", u"���_�滮�ؿ�_����", parameterList)
    
class ru_ku_gui_hua_di_kuai_de_qing_shui_yu(object):
    # ���_�滮�ؿ�_����_ˮ��
    def __init__(self):
        self.label = u"���_�滮�ؿ�_����_ˮ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�Ƿ�������ˮ������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_ˮ��'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_ˮ��1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_�滮�ؿ�_����_ˮ��", u"���_�滮�ؿ�_����_ˮ��", parameterList)
    
class ru_ku_gui_hua_di_kuai_de_qing_dao_lu(object):
    # ���_�滮�ؿ�_����_��·
    def __init__(self):
        self.label = u"���_�滮�ؿ�_����_��·"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_��·��'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_��·��1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_�滮�ؿ�_����_��·", u"���_�滮�ؿ�_����_��·", parameterList)
    
class ru_ku_she_shi_de_qing(object):
    # ���_��ʩ_����
    def __init__(self):
        self.label = u"���_��ʩ_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"���\\���_����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��ʩҪ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'SS_������ʩ'},
            {"name": u"���Ҫ��ģ��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_������ʩ'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AC_RK_������ʩ1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.���.���_����.���_��ʩ_����", u"���_��ʩ_����", parameterList)
    
class yong_tu_fen_qu_bian_hao_sheng_cheng(object):
    # ��;�����������
    def __init__(self):
        self.label = u"��;�����������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_��;����ͼ'},
            {"name": u"���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.����Ҫ���ֶ�ӳ��.���������ֶ�����"},
            {"name": u"��������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.����Ҫ���ֶ�ӳ��.��������ֶ�����"},
            {"name": u"��Ԫ���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'FY07'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.��;�����������", u"��;�����������", parameterList)
    
class yong_tu_fen_qu_gui_hua_tu_sheng_cheng(object):
    # ��;�����滮ͼ����
    def __init__(self):
        self.label = u"��;�����滮ͼ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õص���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õص���ͼ'},
            {"name": u"ũ������Ҫ�������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['YD_��λ_��ʳ����������', 'YD_��λũ�õ���ʵ_������������']},
            {"name": u"���򼯽���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���򼯽���'},
            {"name": u"��������Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_��������'},
            {"name": u"���û���ũ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���û���ũ��'},
            {"name": u"���򿪷��߽��⼯�����޸�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YT_���򿪷��߽��⼯�����޸�'},
            {"name": u"������Ҫ���ϵ�Ҫ�������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": []},
            {"name": u"�������������滻�б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [['½����̬������', 'һ��ũҵ��'], ['��ҵ��չ��', 'һ��ũҵ��']]},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_��;�����滮ͼ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.��;�����滮ͼ����", u"��;�����滮ͼ����", parameterList)
    
class yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_fen_qu(object):
    # �õ�_���߼�_�������Ҫ�����ɷ���
    def __init__(self):
        self.label = u"�õ�_���߼�_�������Ҫ�����ɷ���"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_YTFQ'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.���߼�.�������Ҫ�����ɷ���", u"�õ�_���߼�_�������Ҫ�����ɷ���", parameterList)
    
class qu_chu_zi_duan_zhong_suo_you_kong_ge(object):
    # ȥ���ֶ������пո�
    def __init__(self):
        self.label = u"ȥ���ֶ������пո�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����\\�ֶ�ֵ���"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"ȥ���ֶ�ֵ��ǰ��Ŀո�", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"ȥ���ֶ�ֵ�ڵĿո�", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.�ֶ�ֵ���.ȥ���ֶ������пո�", u"ȥ���ֶ������пո�", parameterList)
    
class qu_yu_geng_xin(object):
    # �������
    def __init__(self):
        self.label = u"�������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�ַ���Χ��'},
            {"name": u"����Ҫ���б���ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'������'},
            {"name": u"�õ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�õ�Ҫ�������������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'��������'},
            {"name": u"��ʩҪ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'SS_������ʩ'},
            {"name": u"��ʩҪ�������������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'��������'},
            {"name": u"�п۳�����ϵ����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����ɸѡ_�۳�����ϵ��'},
            {"name": u"�Ƿ񲻻��ܲ�����ʩ", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"��������ʩ�����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": u"������Ϣ.��Ŀ��Ϣ.�������ʩ�����б�"},
            {"name": u"��������ʩ���ڵؿ�����б�", "dataType": u"�κ�ֵ", "required": u"ѡ��", "argsDirction": u"�������", "multiValue": True, "default": None},
            {"name": u"�Ƿ�����õغ���ʩ����������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�������õؽ��зָ�", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�ͳ�Ƹ��ر�����", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�ͳ�����û���ũ��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���û���ũ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.KZX_���û���ũ��Ҫ������"},
            {"name": u"�Ƿ�ͳ����̬��������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"��̬��������Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.KZX_��̬��������Ҫ������"},
            {"name": u"�Ƿ�ͳ�ƴ�ׯ����߽�", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"��ׯ����߽�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.KZX_��ׯ����߽�Ҫ������"},
            {"name": u"�Ƿ�ͳ����ʩ", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.�������", u"�������", parameterList)
    
class qu_yu_jian_cha(object):
    # ������
    def __init__(self):
        self.label = u"������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"��Χ���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"���˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.����.������", u"������", parameterList)
    
class qu_yu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_qu_yu(object):
    # ����_���߼�_�������Ҫ����������
    def __init__(self):
        self.label = u"����_���߼�_�������Ҫ����������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�ִ巶Χ��'},
            {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�����ַ��ִ�'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.���߼�.�������Ҫ����������", u"����_���߼�_�������Ҫ����������", parameterList)
    
class dao_ru_shu_xing_biao(object):
    # �������Ա�
    def __init__(self):
        self.label = u"�������Ա�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"EXCEL�ļ�·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\1-�˶Ի�����λ.xlsx'},
            {"name": u"EXCEL�ļ��б������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'sheet1'},
            {"name": u"ӳ���ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'ʵ��GUID'},
            {"name": u"������ֶ������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['*']},
            {"name": u"������ֶ������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['*']},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.�������Ա�", u"�������Ա�", parameterList)
    
class shu_xing_dui_bi(object):
    # ���ԶԱ�
    def __init__(self):
        self.label = u"���ԶԱ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��1", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"����Ҫ��·��2", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"ӳ���ֶ������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['_ID', '_ID']},
            {"name": u"�Ƿ񵼳������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ա��ֶ������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [['��������', '��������'], ['�����ִ�', '�����ִ�']]},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.���ԶԱ�", u"���ԶԱ�", parameterList)
    
class zuo_biao_xi_tong_yi(object):
    # ����ϵͳһ
    def __init__(self):
        self.label = u"����ϵͳһ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·���б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['YD_���ڳ�ת��']},
            {"name": u"����ϵ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"PROJCS['CGCS2000_3_Degree_GK_CM_120E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',120.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.����ϵͳһ", u"����ϵͳһ", parameterList)
    
class zi_duan_ming_cheng_xiao_xie_gai_da_xie(object):
    # �ֶ�����Сд�Ĵ�д
    def __init__(self):
        self.label = u"�ֶ�����Сд�Ĵ�д"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·���б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['JX_�滮��Χ��']},
            {"name": u"���Ҫ��·���б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['�ڴ���ʱ']},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.�ֶ�����Сд�Ĵ�д", u"�ֶ�����Сд�Ĵ�д", parameterList)
    
class dao_ru_cong_CAD(object):
    # �����CAD
    def __init__(self):
        self.label = u"�����CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����CAD���ݼ��е�Ҫ����·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg\\�ع�ؿ�'},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�ת��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_CADɫ��'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.�����CAD", u"�����CAD", parameterList)
    
class dao_chu_dao_CAD(object):
    # ������CAD
    def __init__(self):
        self.label = u"������CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"���ں��ֶ�����", "dataType": u"�ַ���", "required": u"ѡ��", "argsDirction": u"�������", "multiValue": False, "default": None},
            {"name": u"���ں��ֶ������ںϵ�ֵ���б�", "dataType": u"�κ�ֵ", "required": u"ѡ��", "argsDirction": u"�������", "multiValue": True, "default": None},
            {"name": u"�з���ֵ", "dataType": u"�ַ���", "required": u"ѡ��", "argsDirction": u"�������", "multiValue": False, "default": None},
            {"name": u"�Ƿ�ȥ��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"CAD��ͼ����õ��ֶε�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'������'},
            {"name": u"���CAD·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.������CAD", u"������CAD", parameterList)
    
class shu_xing_yu_xiu_fu(object):
    # �������޸�
    def __init__(self):
        self.label = u"�������޸�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·���б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['YD_���ڳ�ת��']},
            {"name": u"���Ҫ��·���б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['�ڴ���ʱ']},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.�������޸�", u"�������޸�", parameterList)
    
class yao_su_chuang_jian_tong_guo_geng_xin_gen_ju_mian(object):
    # Ҫ�ش���_ͨ������_������
    def __init__(self):
        self.label = u"Ҫ�ش���_ͨ������_������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_������Χ��'},
            {"name": u"�ֶ�ӳ���б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [['��������', '�������']]},
            {"name": u"���㷽ʽ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ָ�����Ҫ��'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.���Ը���", u"Ҫ�ش���_ͨ������_������", parameterList)
    
class shu_ju_jian_cha(object):
    # ���ݼ��
    def __init__(self):
        self.label = u"���ݼ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg\\�ع�ؿ�'},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����߼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ񼸺��޸�", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�ಿ�����", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"���߼����ֵ", "dataType": u"�ַ���", "required": u"ѡ��", "argsDirction": u"�������", "multiValue": False, "default": None},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.���ݼ��", u"���ݼ��", parameterList)
    
class qu_zhuan_zhe(object):
    # ��ת��
    def __init__(self):
        self.label = u"��ת��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·���б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['YD_���ڳ�ת��']},
            {"name": u"�ֶ�ȷ���Ƿ�ת��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.��ת��", u"��ת��", parameterList)
    
class qing_li_li_shi_yao_su(object):
    # ������ʷҪ��
    def __init__(self):
        self.label = u"������ʷҪ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�������ݿ�·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\common\\Project\\D�������������嵥Ԫ�ع�\\03�����ļ�\\24.11.27������\\D�������������嵥Ԫ�ع�_���ݿ�.gdb'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.������ʷҪ��", u"������ʷҪ��", parameterList)
    
class tong_ji(object):
    # ͳ��
    def __init__(self):
        self.label = u"ͳ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YD_���ڳ�ת��'},
            {"name": u"��ͳ���ֶμ�ͳ�Ʒ�ʽ�б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": [{'�ֶ�����': '', 'ͳ�Ʒ�ʽ': '���'}]},
            {"name": u"�����ֶ��б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['����1']},
            {"name": u"ɸѡ���ʽ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�Ƿ���ʾ������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.ͳ��", u"ͳ��", parameterList)
    
class yao_su_lian_he(object):
    # Ҫ������
    def __init__(self):
        self.label = u"Ҫ������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.Ҫ������", u"Ҫ������", parameterList)
    
class yong_di_die_he_tu_sheng_cheng(object):
    # �õص���ͼ����
    def __init__(self):
        self.label = u"�õص���ͼ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ�������б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['DIST_�õ���״ͼ', 'YD_������Ϣ����δ��', 'YD_��λ_��ʳ����������', 'YD_��λ����ũ����ʵ', 'YD_��λũ�õ���ʵ_������������', 'YD_��λũ�õ���ʵ_����ˮ', 'YD_��λũ�õ���ʵ_�������', 'YD_��λũ�õ���ʵ_������ʩũ�õ�']},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ����߼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õص���ͼ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.�õص���ͼ����", u"�õص���ͼ����", parameterList)
    
class yong_di_ji_qi_tu_sheng_cheng(object):
    # �õػ���ͼ����
    def __init__(self):
        self.label = u"�õػ���ͼ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ�������б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['YD_����ϸ��', 'YD_ũת��20�꼰��ǰ']},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ����߼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õػ���ͼ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.�õػ���ͼ����", u"�õػ���ͼ����", parameterList)
    
class yong_di_geng_xin(object):
    # �õظ���
    def __init__(self):
        self.label = u"�õظ���"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�ֲ�����SQL���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u''},
            {"name": u"�ַ���Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�ַ���Χ��'},
            {"name": u"�ִ巶Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�ִ巶Χ��'},
            {"name": u"���򼯽���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���򼯽���'},
            {"name": u"��������Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_��������'},
            {"name": u"�п۳�����ϵ����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����ɸѡ_�۳�����ϵ��'},
            {"name": u"�����䵥λ��Ϣ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����ɸѡ_���䵥λ����'},
            {"name": u"��ʩҪ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'SS_������ʩ'},
            {"name": u"�Ƿ���кϹ��Լ��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ���õر߽���е���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����¼������������ַ��ͷִ�", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����¼��������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ���ݵ��������ɵ�������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����ؿ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�����߽��ڷǽ����õ��Ƿ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"��·�Ƿ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�����߽���ǽ����õ��Ƿ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ���㿪����̬", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����ؿ�����ʩ��ģ", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ���㽨����ģ������ģ����������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�������������", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���ڷ���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YD_TZ_���������ڷ�λ'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.�õظ���", u"�õظ���", parameterList)
    
class yong_di_xian_zhuang_tu_sheng_cheng(object):
    # �õ���״ͼ����
    def __init__(self):
        self.label = u"�õ���״ͼ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ�������б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['DIST_�õػ���ͼ', 'YD_��״�޸�1', 'YD_ũת��21�꼰�Ժ�', 'YD_������Ϣ��ʵʩ', 'YD_�ؼ���Ϣ', 'YD_��״�޸�2']},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"�Ƿ����߼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õ���״ͼ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.�õ���״ͼ����", u"�õ���״ͼ����", parameterList)
    
class yong_di_gui_hua_tu_sheng_cheng(object):
    # �õع滮ͼ����
    def __init__(self):
        self.label = u"�õع滮ͼ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ�������б�", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['DIST_�õص���ͼ', 'YD_GIS����_ũ�õ����']},
            {"name": u"CAD����ɫ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_CAD����_�õع滮'},
            {"name": u"CAD����ɫ���п�϶�ĵ���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'00'},
            {"name": u"CAD����ɫ������Ч�ĵ����б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['07%', '08%', '09%', '10%', '11%', '12%', '13%', '14%', '15%', '16%', '1701%', '1702%', '1703%', '23%']},
            {"name": u"CAD����ɫ������Ч���ֵ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YD_CAD����'},
            {"name": u"CAD����ɫ������������Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YD_GIS����_�����õ��޸�'},
            {"name": u"GIS���Ѵ����ϸС��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YD_GIS����_ϸС�洦��'},
            {"name": u"����ϲ���ϸС����������б�", "dataType": u"�κ�ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": True, "default": ['01%', '02%', '03%', '04%', '05%', '06%', '1207%', '17%']},
            {"name": u"ϸС�������ֵ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'10'},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.JX_�滮��Χ��Ҫ������"},
            {"name": u"�Ƿ����˼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ�Χ���", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�Ƿ����߼��", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.�õع滮ͼ����", u"�õع滮ͼ����", parameterList)
    
class yong_di_chuang_jian_sheng_cheng_yong_di_tiao_zheng_tu(object):
    # �õش���_�����õص���ͼ
    def __init__(self):
        self.label = u"�õش���_�����õص���ͼ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õض���ͼ'},
            {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õػ���ͼ'},
            {"name": u"�滮Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"��ֲ����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_����_��ֲ��������"},
            {"name": u"���䵥λҪ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_����_���䵥λ����"},
            {"name": u"�����õص���ͼ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õص���ͼ'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.�õص���ͼ����", u"�õش���_�����õص���ͼ", parameterList)
    
class kai_fa_bian_jie_nei_gong_ye_yong_di(object):
    # �����߽��ڹ�ҵ�õ�
    def __init__(self):
        self.label = u"�����߽��ڹ�ҵ�õ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\��ʱ"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"������_���򿪷��߽�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���򿪷��߽�'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AA_�����߽��ڹ�ҵ�õ�'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.��ʱ.�õ�_��ʱ_�����߽��ڹ�ҵ�õ�", u"�����߽��ڹ�ҵ�õ�", parameterList)
    
class yong_di_ji_suan_tiao_zheng_lei_xing(object):
    # �õ�_�����������
    def __init__(self):
        self.label = u"�õ�_�����������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\��ʱ"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õص���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'in_memory\\AA_�����������'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.��ʱ.�õ�_��ʱ_�����������", u"�õ�_�����������", parameterList)
    
class jian_cha_di_kuai_bian_hao_he_tu_di_ma_shi_fou_you_wen_ti(object):
    # ���ؿ��ź��������Ƿ�������
    def __init__(self):
        self.label = u"���ؿ��ź��������Ƿ�������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�ؿ����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�ؿ����ֶ�����"},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.�ؿ��ź���������", u"���ؿ��ź��������Ƿ�������", parameterList)
    
class di_lei_bian_hao_ming_cheng_bie_cheng_pi_pei_jian_cha(object):
    # ���������Ʊ��ƥ����
    def __init__(self):
        self.label = u"���������Ʊ��ƥ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.���������ֶ�����"},
            {"name": u"���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.���������ֶ�����"},
            {"name": u"�ؿ����ʱ���ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�ؿ����ʱ���ֶ�����"},
            {"name": u"�õع����ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�õش����ֶ�����"},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.���������Ʊ��ƥ����", u"���������Ʊ��ƥ����", parameterList)
    
class ji_ben_nong_tian_shi_fou_bei_zhan(object):
    # ����ũ���Ƿ�ռ
    def __init__(self):
        self.label = u"����ũ���Ƿ�ռ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"����ũ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���û���ũ��'},
            {"name": u"�Ƿ������CAD", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": False},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.����ũ���Ƿ�ռ", u"����ũ���Ƿ�ռ", parameterList)
    
class kai_fa_bian_jie_wai_cheng_zhen_jian_she_yong_di_jian_cha(object):
    # �����߽���������õؼ��
    def __init__(self):
        self.label = u"�����߽���������õؼ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"���򼯽���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���򼯽���'},
            {"name": u"��������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_��������'},
            {"name": u"���Ҫ������_�����߽���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            {"name": u"���Ҫ������_�����߽���", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            {"name": u"���Ҫ������_�����߽��⽨���õ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            {"name": u"���Ҫ������_�����߽��ڷǽ����õ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.�����߽������õؼ��", u"�����߽���������õؼ��", parameterList)
    
class yong_di_he_gui_xing_jian_cha(object):
    # �õغϹ��Լ��
    def __init__(self):
        self.label = u"�õغϹ��Լ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"����ֶ��Ƿ����ȱʧ", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"����ֶ������Ƿ���ȷ", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���������Ƿ���ڿ�ֵ", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.�õغϹ��Լ��", u"�õغϹ��Լ��", parameterList)
    
class chu_bu_ji_shu_zhuan_huan_san_diao(object):
    # ��������ת��_����
    def __init__(self):
        self.label = u"��������ת��_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'YD_����_�ֶκ���'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.��������ת��_����", u"��������ת��_����", parameterList)
    
class chu_bu_ji_shu_zhuan_huan_er_diao(object):
    # ��������ת��_����
    def __init__(self):
        self.label = u"��������ת��_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����_�ֶκ���'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.��������ת��_����", u"��������ת��_����", parameterList)
    
class zi_duan_chu_li_bing_sheng_cheng_fen_xiang_san_diao(object):
    # �ֶδ������ɷ���_����
    def __init__(self):
        self.label = u"�ֶδ������ɷ���_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����'},
            {"name": u"�۳�����ϵ��Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_����_�۳�����ϵ��"},
            {"name": u"��ֲ��������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_����_��ֲ��������"},
            {"name": u"�����������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_����_�����������"},
            {"name": u"���䵥λ����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_����_���䵥λ����"},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.�ֶδ������ɷ���_����", u"�ֶδ������ɷ���_����", parameterList)
    
class zi_duan_chu_li_bing_sheng_cheng_fen_xiang_er_diao(object):
    # �ֶδ������ɷ���_����
    def __init__(self):
        self.label = u"�ֶδ������ɷ���_����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\����"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.����.�ֶδ������ɷ���_����", u"�ֶδ������ɷ���_����", parameterList)
    
class di_lei_zhuan_huan_cheng_xiang_di_lei_zhuan_guo_kong_di_lei(object):
    # ����ת��_�������ת���յ���
    def __init__(self):
        self.label = u"����ת��_�������ת���յ���"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.����ת��_�������ת���յ���", u"����ת��_�������ת���յ���", parameterList)
    
class di_lei_zhuan_huan_jiu_ban_guo_kong_di_lei_zhuan_xin_ban_guo_kong_di_lei(object):
    # ����ת��_�ɰ���յ���ת�°���յ���
    def __init__(self):
        self.label = u"����ת��_�ɰ���յ���ת�°���յ���"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.����ת��_�ɰ���յ���ת�°���յ���", u"����ת��_�ɰ���յ���ת�°���յ���", parameterList)
    
class yong_di_gong_ju_ji_geng_xin_dui_xiang_shu_xing(object):
    # �õ�_���߼�_���¶�������
    def __init__(self):
        self.label = u"�õ�_���߼�_���¶�������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"��������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'AA_����ָ��'},
            {"name": u"���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'Text'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.���¶�������", u"�õ�_���߼�_���¶�������", parameterList)
    
class yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_yong_di(object):
    # �õ�_���߼�_�������Ҫ�������õ�
    def __init__(self):
        self.label = u"�õ�_���߼�_�������Ҫ�������õ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ؿ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.�������Ҫ�������õ�", u"�õ�_���߼�_�������Ҫ�������õ�", parameterList)
    
class yong_di_chuang_jian_tong_guo_gen_ju_di_lei_ming_cheng_sheng_cheng_bian_hao(object):
    # �õش���_ͨ�����ݵ����������ɱ��
    def __init__(self):
        self.label = u"�õش���_ͨ�����ݵ����������ɱ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'��������'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'in_memory\\AA_���������'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.���ݵ����������ɱ��", u"�õش���_ͨ�����ݵ����������ɱ��", parameterList)
    
class yong_di_gong_ju_ji_yong_di_shu_ju_tong_ji(object):
    # �õ�_���߼�_�õ�����ͳ��
    def __init__(self):
        self.label = u"�õ�_���߼�_�õ�����ͳ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õ�Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.�õ�����ͳ��", u"�õ�_���߼�_�õ�����ͳ��", parameterList)
    
class tong_ji_kai_fa_bian_jie_wai_ji_qi_203_yong_di(object):
    # ͳ�ƿ����߽������203�õ�
    def __init__(self):
        self.label = u"ͳ�ƿ����߽������203�õ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���򼯽���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"��������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"�滮��Χ��Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���䵥λҪ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.ͳ�ƿ����߽������203�õ�", u"ͳ�ƿ����߽������203�õ�", parameterList)
    
class yong_di_chuang_jian_tong_guo_ji_suan_liang_ke_yong_di(object):
    # �õش���_ͨ�����������õ�
    def __init__(self):
        self.label = u"�õش���_ͨ�����������õ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ������", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False},
            {"name": u"����ֲ���Ե�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'CZ_����ɸѡ_��ֲ��������'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'in_memory\\AA_���������õ�'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.���������õ�", u"�õش���_ͨ�����������õ�", parameterList)
    
class ji_suan_wen_ben_lian_jie_yong_shu_ju(object):
    # �����ı�����������
    def __init__(self):
        self.label = u"�����ı�����������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"�õ�\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õع滮Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.YD_�õ�_�滮Ҫ������"},
            {"name": u"�õص���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.YD_�õ�_����Ҫ������"},
            {"name": u"��;����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.FQ_��;����_�滮Ҫ������"},
            {"name": u"���򼯽���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.KZX_���򼯽���Ҫ������"},
            {"name": u"��������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.KZX_��������Ҫ������"},
            {"name": u"���û���ũ��Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.KZX_���û���ũ��Ҫ������"},
            {"name": u"�滮��Χ��Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.JX_�滮��Χ��Ҫ������"},
            {"name": u"��λ������������Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.��Ŀ��Ϣ.CZ_��λ�滮_������������"},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'��������'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.�õ�.���߼�.�����ı�����������", u"�����ı�����������", parameterList)
    
class she_shi_geng_xin(object):
    # ��ʩ����
    def __init__(self):
        self.label = u"��ʩ����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"��ʩ"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"����Ҫ��·��", "dataType": u"Ҫ����", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'SS_������ʩ'},
            {"name": u"�Ƿ���������ֶ��ƶ���ʩ����", "dataType": u"����ֵ", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": True},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"��ҵƬ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_��ҵƬ����Χ��'},
            {"name": u"����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_������Χ��'},
            {"name": u"�ַ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�ַ���Χ��'},
            {"name": u"�ִ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�ִ巶Χ��'},
            {"name": u"�õع滮Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"���õع滮Ҫ����������ʩ���ͳһ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'����ʩ���õ�'},
            {"name": u"���򼯽���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_���򼯽���'},
            {"name": u"��������Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'KZX_��������'},
            {"name": u"���Ҫ��·��_�õ�", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            {"name": u"���Ҫ��·��_��ʩ", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.��ʩ.��ʩ����", u"��ʩ����", parameterList)
    
class she_shi_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_she_shi(object):
    # ��ʩ_���߼�_�������Ҫ��������ʩ
    def __init__(self):
        self.label = u"��ʩ_���߼�_�������Ҫ��������ʩ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"��ʩ\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��ʩҪ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_PTSS'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.��ʩ.���߼�.�������Ҫ��������ʩ", u"��ʩ_���߼�_�������Ҫ��������ʩ", parameterList)
    
class he_dao_bian_xian_sheng_cheng(object):
    # �ӵ���������
    def __init__(self):
        self.label = u"�ӵ���������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"��·"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�ӵ�����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DL_�ӵ�����'},
            {"name": u"�õ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�ӵ��õ�����Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DL_�ӵ��õ�����'},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"����Ҫ��·��", "dataType": u"�ַ���", "required": u"ѡ��", "argsDirction": u"�������", "multiValue": False, "default": None},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.��·.�ӵ���������", u"�ӵ���������", parameterList)
    
class dao_lu_bian_xian_sheng_cheng(object):
    # ��·��������
    def __init__(self):
        self.label = u"��·��������"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"��·"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��·����Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DL_��·����'},
            {"name": u"�õ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�滮��Χ��Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'JX_�滮��Χ��'},
            {"name": u"���Ҫ��·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.��·.��·��������", u"��·��������", parameterList)
    
class dao_lu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_kong_zhi_xian(object):
    # ��·_���߼�_�������Ҫ�����ɿ�����
    def __init__(self):
        self.label = u"��·_���߼�_�������Ҫ�����ɿ�����"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"��·\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"������Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'XG_KZX'},
            {"name": u"���Ҫ�����ƺ�׺", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.��·.���߼�.�������Ҫ�����ɿ�����", u"��·_���߼�_�������Ҫ�����ɿ�����", parameterList)
    
class dao_lu_hong_xian_ti_qu(object):
    # ��·������ȡ
    def __init__(self):
        self.label = u"��·������ȡ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"��·\\���߼�"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"�õ�Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'DIST_�õع滮ͼ'},
            {"name": u"�������ֶ�����", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u"������Ϣ.�ؿ�Ҫ���ֶ�ӳ��.�������ֶ�����"},
            {"name": u"������CAD·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg'},
            {"name": u"���Ҫ������", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'�ڴ���ʱ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.��·.���߼�.��·������ȡ", u"��·������ȡ", parameterList)
    
class di_kuai_zhi_biao_ce_suan_biao_huo_qu(object):
    # �ؿ�ָ�������ȡ
    def __init__(self):
        self.label = u"�ؿ�ָ�������ȡ"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.������Ϣ", u"�ؿ�ָ�������ȡ", parameterList)
    
class huo_qu_gong_zuo_kong_jian(object):
    # ��ȡ�����ռ�
    def __init__(self):
        self.label = u"��ȡ�����ռ�"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"����"

    def getParameterInfo(self):
        args_dict_list = [
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.���ð�", u"��ȡ�����ռ�", parameterList)
    
class xiang_mu_chu_shi_hua(object):
    # ��Ŀ��ʼ��
    def __init__(self):
        self.label = u"��Ŀ��ʼ��"
        self.description = ""
        self.canRunInBackground = False
        self.category = u""

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"��Ŀ�ļ���·��", "dataType": u"�ַ���", "required": u"����", "argsDirction": u"�������", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.����.��Ŀ��ʼ��", u"��Ŀ��ʼ��", parameterList)
    