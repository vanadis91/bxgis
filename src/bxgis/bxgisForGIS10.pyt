# -- coding:cp936 –
import arcpy
# -*- coding: gbk -*-

data_type_map = {
    u"要素图层".encode('gbk'): "GPFeatureLayer",
    u"要素类".encode('gbk'): "DEFeatureClass",
    u"布尔值".encode('gbk'): "GPBoolean",
    u"双精度".encode('gbk'): "GPDouble",
    u"字段".encode('gbk'): "Field",
    u"长整型".encode('gbk'): "GPLong",
    u"字符串".encode('gbk'): "GPString",
    u"表".encode('gbk'): "DETable",
    u"工作空间".encode('gbk'): "DEWorkspace",
    u"值表".encode('gbk'): "GPValueTable",
    u"文件".encode('gbk'): "DEFile",
    u"文件夹".encode('gbk'): "DEFolder",
    u"数据文件".encode('gbk'): "GPDataFile",
    u"CAD数据集".encode('gbk'): "DECadDrawingDataset",
    u"变量".encode('gbk'): "GPVariant",
    u"任何值".encode('gbk'): "GPType",
}
required_map = {
    u"必填".encode('gbk'): "Required",
    u"选填".encode('gbk'): "Optional",
    u"隐藏的输出参数".encode('gbk'): "Derived",
}
args_type_map = {
    u"输入参数".encode('gbk'): "Input",
    u"输出参数".encode('gbk'): "Output",
}

# def get_prj_info():
#     # 获取项目信息
#     import os
#     import yaml
#     toml_file_path = os.path.join(os.path.dirname(__file__),u'配置',u'项目信息.toml')
#     with open(toml_file_path,mode='r')as f:
#         return yaml.load(f)
def get_registry_value(key_path, value_name):
    import _winreg as winreg
    # 打开注册表项
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        # 获取指定名称的值
        value, regtype = winreg.QueryValueEx(key, value_name)
        # 关闭注册表项
        winreg.CloseKey(key)
        return value
    
    except WindowsError as e:
        raise Exception(u"无法找到arcgis_pro的安装路径".encode('gbk'))

def add_search_path():
    # 为py3的包搜索路径中添加本项目
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
            print(u"无法删除原有的com.pth".encode('gbk'))

add_search_path()

def fun_run(module_name, function_name, args_list):
    import subprocess
    import json
    import os
    import arcpy

    args_dict = ParameterCls.convert_to_dictRawValue(args_list)
    args_dict_str = json.dumps(args_dict,ensure_ascii=False)

    run_cli_dict={
        u'模块名称'.encode('gbk'): module_name.encode('gbk'),
        u'函数名称'.encode('gbk'): function_name.encode('gbk'),
        u'参数字典'.encode('gbk'): args_dict_str,
        u'当前工作空间'.encode('gbk'): arcpy.env.workspace.encode('gbk'),
    }

    args_path = os.path.join(os.path.dirname(__file__),u'命令行',u'命令行参数.json')
    with open(args_path,mode='w')as f:
        json.dump(run_cli_dict, f, ensure_ascii=False, indent=4)

    arcgis_pro_install_dir = get_registry_value(r"SOFTWARE\ESRI\ArcGISPro",'InstallDir')
    interpreter_path = os.path.join(arcgis_pro_install_dir,'bin','Python','envs','arcgispro-py3','python.exe')
    str = u"\"{}\" -m bxgis.命令行.命令行包".format(interpreter_path)
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
        name=u'未指定',
        dataType=u'要素图层',
        discription=None,
        required=u"选填",
        argsDirction=u"输入参数",
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
        .pyt file) 定义了工具箱的属性"""
        self.label = "BXGIS工具箱"  # 定义标签
        self.alias = "BXGIS工具箱"  # 定义别名

        # List of tool classes associated with this toolbox
        self.tools = [ru_ku_dan_yuan, ru_ku_tu_ze, ru_ku_ju_diao_ru_ku, ru_ku_gong_ye_pian_qu, ru_ku_kong_zhi_xian, ru_ku_cun_zhuang_jian_she_bian_jie, ru_ku_yong_tu_fen_qu, ru_ku_jie_qu_jie_fang_fen_cun, ru_ku_gui_hua_di_kuai, ru_ku_she_shi, ru_ku_dan_yuan_de_qing, ru_ku_kong_zhi_xian_de_qing_di_kuai_hou_tui_xian, ru_ku_kong_zhi_xian_de_qing_te_shu_fan_wei_xian, ru_ku_kong_zhi_xian_de_qing_dao_lu_zhong_xian, ru_ku_kong_zhi_xian_de_qing_dao_lu_bian_xian, ru_ku_gui_hua_di_kuai_de_qing, ru_ku_gui_hua_di_kuai_de_qing_shui_yu, ru_ku_gui_hua_di_kuai_de_qing_dao_lu, ru_ku_she_shi_de_qing, yong_tu_fen_qu_bian_hao_sheng_cheng, yong_tu_fen_qu_gui_hua_tu_sheng_cheng, yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_fen_qu, qu_chu_zi_duan_zhong_suo_you_kong_ge, qu_yu_geng_xin, qu_yu_jian_cha, qu_yu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_qu_yu, dao_ru_shu_xing_biao, shu_xing_dui_bi, zuo_biao_xi_tong_yi, zi_duan_ming_cheng_xiao_xie_gai_da_xie, dao_ru_cong_CAD, dao_chu_dao_CAD, shu_xing_yu_xiu_fu, yao_su_chuang_jian_tong_guo_geng_xin_gen_ju_mian, shu_ju_jian_cha, qu_zhuan_zhe, qing_li_li_shi_yao_su, tong_ji, yao_su_lian_he, yong_di_die_he_tu_sheng_cheng, yong_di_ji_qi_tu_sheng_cheng, yong_di_geng_xin, yong_di_xian_zhuang_tu_sheng_cheng, yong_di_gui_hua_tu_sheng_cheng, yong_di_chuang_jian_sheng_cheng_yong_di_tiao_zheng_tu, kai_fa_bian_jie_nei_gong_ye_yong_di, yong_di_ji_suan_tiao_zheng_lei_xing, jian_cha_di_kuai_bian_hao_he_tu_di_ma_shi_fou_you_wen_ti, di_lei_bian_hao_ming_cheng_bie_cheng_pi_pei_jian_cha, ji_ben_nong_tian_shi_fou_bei_zhan, kai_fa_bian_jie_wai_cheng_zhen_jian_she_yong_di_jian_cha, yong_di_he_gui_xing_jian_cha, chu_bu_ji_shu_zhuan_huan_san_diao, chu_bu_ji_shu_zhuan_huan_er_diao, zi_duan_chu_li_bing_sheng_cheng_fen_xiang_san_diao, zi_duan_chu_li_bing_sheng_cheng_fen_xiang_er_diao, di_lei_zhuan_huan_cheng_xiang_di_lei_zhuan_guo_kong_di_lei, di_lei_zhuan_huan_jiu_ban_guo_kong_di_lei_zhuan_xin_ban_guo_kong_di_lei, yong_di_gong_ju_ji_geng_xin_dui_xiang_shu_xing, yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_yong_di, yong_di_chuang_jian_tong_guo_gen_ju_di_lei_ming_cheng_sheng_cheng_bian_hao, yong_di_gong_ju_ji_yong_di_shu_ju_tong_ji, tong_ji_kai_fa_bian_jie_wai_ji_qi_203_yong_di, yong_di_chuang_jian_tong_guo_ji_suan_liang_ke_yong_di, ji_suan_wen_ben_lian_jie_yong_shu_ju, she_shi_geng_xin, she_shi_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_she_shi, he_dao_bian_xian_sheng_cheng, dao_lu_bian_xian_sheng_cheng, dao_lu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_kong_zhi_xian, dao_lu_hong_xian_ti_qu, di_kuai_zhi_biao_ce_suan_biao_huo_qu, huo_qu_gong_zuo_kong_jian, xiang_mu_chu_shi_hua,]

# class common_importFromCAD(object): 
#     def __init__(self):
#         self.label = u"导入从CAD"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"常用"

#     def getParameterInfo(self):
#         args_dict_list = [
#             {"name": u"输入CAD数据集中的要素类路径", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False},
#             {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
#             {"name": u"是否范围检查", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
#             {"name": u"是否转曲", "dataType": u"布尔值", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False,'default':False},
#             {"name": u"输出要素路径", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输出参数",'multiValue': False,'default':u'YD_CAD色块'},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.常用.导入从CAD',u'导入从CAD',parameterList)

# class common_curveToPolyline(object): 
#     # "曲转折"
#     def __init__(self):
#         self.label = u"曲转折"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"常用"

#     def getParameterInfo(self):
#         # init_addSearchPath()
#         # from bxgis.配置 import 基本信息
#         args_dict_list = [
#             {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u'必填', "argsDirction": u"输入参数",'multiValue': True},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     # def isLicensed(self):
#     #     """Set whether tool is licensed to execute."""
#     #     return True

#     # def updateParameters(self, 参数列表):
#     #     init_addSearchPath()
#     #     import bxgis.常用.导出到CAD as 导出到CAD

#     #     return 导出到CAD.界面类.函数参数更新(参数列表)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.常用.曲转折',u'曲转折',parameterList)

#     # def updateMessages(self, parameters):
#     #     """Modify the messages created by internal validation for each tool
#     #     parameter.  This method is called after internal validation."""
#     #     return

# class config_projectInit(object): 
#     def __init__(self):
#         self.label = u"项目初始化"
#         self.description = ""
#         self.canRunInBackground = False
#         self.category = u"配置"

#     def getParameterInfo(self):
#         args_dict_list = [
#             {"name": u"项目文件夹路径", "dataType": u"文件夹", "required": u'必填', "argsDirction": u"输入参数",'multiValue': False},
#         ]
#         return ParameterCls.parameterCreate_muti(args_dict_list)

#     def execute(self, parameterList, message):
#         fun_run(u'bxgis.配置.项目初始化',u'项目初始化',parameterList)

class ru_ku_dan_yuan(object):
    # 入库_单元
    def __init__(self):
        self.label = u"入库_单元"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"单元编号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"单元类型", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"编制单位", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"单元功能", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"人口规模", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"跨单元平衡情况", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_GHFW'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_单元", u"入库_单元", parameterList)
    
class ru_ku_tu_ze(object):
    # 入库_图则
    def __init__(self):
        self.label = u"入库_图则"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"图则线列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [{'类型代码': 'JZHTX-GC', '类型名称': '建筑后退线-高层', '要素路径': 'TZ_建筑高层后退线', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'JZHTX-DC', '类型名称': '建筑后退线-多层', '要素路径': 'TZ_建筑多层后退线', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'JKKD', '类型名称': '禁开口段', '要素路径': 'TZ_禁止机动车开口线', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'JDCCRK', '类型名称': '机动车出入口', '要素路径': 'TZ_机动车开口符号', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'JGLDKZX', '类型名称': '景观廊道控制线', '要素路径': 'TZ_景观廊道控制线', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'ZYJM', '类型名称': '重要界面', '要素路径': 'TZ_重要界面', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'DKLTD', '类型名称': '地块连通道', '要素路径': 'TZ_地块连通道', '字段映射': [['通道宽度', 'GKYQ'], ['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'QTTZX', '类型名称': '其他图则线', '要素路径': 'TZ_其他图则线', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}]},
            {"name": u"图则面列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [{'类型代码': 'DKGDFQ', '类型名称': '地块高度分区', '要素路径': 'TZ_地块高度分区', '字段映射': [['分区高度', 'GKYQ'], ['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'GGKCKJ', '类型名称': '公共开敞空间', '要素路径': 'TZ_公共开敞空间', '字段映射': [['管控要求', 'GKYQ'], ['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'DXKJGKM', '类型名称': '地下空间管控面', '要素路径': 'TZ_地下空间管控面', '字段映射': [['管控要求', 'GKYQ'], ['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'QTTZM', '类型名称': '其他图则面', '要素路径': 'TZ_其他图则面', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}]},
            {"name": u"图则点列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [{'类型代码': 'DBJZ', '类型名称': '地标建筑', '要素路径': 'TZ_地标建筑', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'ZYSD', '类型名称': '重要视点', '要素路径': 'TZ_重要视点', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}, {'类型代码': 'QTTZD', '类型名称': '其他图则点', '要素路径': 'TZ_其他图则点', '字段映射': [['管控力度', 'GKLD'], ['备注', 'BZ']]}]},
            {"name": u"输出要素名称字典", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u"{'线': 'XG_TZX', '面': 'XG_TZM', '点': 'XG_TZD'}"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_图则", u"入库_图则", parameterList)
    
class ru_ku_ju_diao_ru_ku(object):
    # 入库_局调入库
    def __init__(self):
        self.label = u"入库_局调入库"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AA_规划工业用地'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_局调", u"入库_局调入库", parameterList)
    
class ru_ku_gong_ye_pian_qu(object):
    # 入库_工业片区
    def __init__(self):
        self.label = u"入库_工业片区"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"工业片区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_工业片区范围线'},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_GYPQ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_工业片区", u"入库_工业片区", parameterList)
    
class ru_ku_kong_zhi_xian(object):
    # 入库_控制线
    def __init__(self):
        self.label = u"入库_控制线"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"地块要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"道路中线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DL_道路中线'},
            {"name": u"道路边线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DL_道路边线'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_KZX'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_控制线", u"入库_控制线", parameterList)
    
class ru_ku_cun_zhuang_jian_she_bian_jie(object):
    # 入库_村庄建设边界
    def __init__(self):
        self.label = u"入库_村庄建设边界"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"村庄建设边界要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_村庄建设边界'},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"单元编号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'QT12'},
            {"name": u"是否融合并多部件变单部件", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"管控要求", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'按照“避让底线、引导集聚、单元统筹、预留弹性、界限清晰”的原则进行控制，综合考虑村庄分级分类与建设用地指标安排，引导乡村空间适度集聚'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_JSBJ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_村庄建设边界", u"入库_村庄建设边界", parameterList)
    
class ru_ku_yong_tu_fen_qu(object):
    # 入库_用途分区
    def __init__(self):
        self.label = u"入库_用途分区"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"分区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用途分区图'},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"单元编号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'QT12'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_YTFQ'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_用途分区", u"入库_用途分区", parameterList)
    
class ru_ku_jie_qu_jie_fang_fen_cun(object):
    # 入库_街区街坊分村
    def __init__(self):
        self.label = u"入库_街区街坊分村"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"区域要素名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['JX_街区范围线', 'JX_街坊范围线']},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"层级列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['街区', '街坊']},
            {"name": u"区域编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'区域编号'},
            {"name": u"区域主导属性字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'区域主导属性'},
            {"name": u"总城镇居住人数字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总城镇居住人数'},
            {"name": u"总建筑面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总建筑面积'},
            {"name": u"总住宅建筑面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总住宅建筑面积'},
            {"name": u"总工业建筑面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总工业建筑面积'},
            {"name": u"总商服建筑面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总商服建筑面积'},
            {"name": u"总村庄户籍人数字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总村庄户籍人数'},
            {"name": u"总村庄居住人数字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总村庄居住人数'},
            {"name": u"总耕地保有量字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总耕地保有量'},
            {"name": u"总永久基本农田用地面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总永久基本农田用地面积'},
            {"name": u"总生态保护红线用地面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总生态保护红线用地面积'},
            {"name": u"总村庄建设边界用地面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总村庄建设边界用地面积'},
            {"name": u"总城乡建设用地面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总城乡建设用地面积'},
            {"name": u"总村庄建设用地面积字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'总村庄建设用地面积'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_JQJF'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_街区街坊分村", u"入库_街区街坊分村", parameterList)
    
class ru_ku_gui_hua_di_kuai(object):
    # 入库_规划地块
    def __init__(self):
        self.label = u"入库_规划地块"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"不入库设施名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": u"基本信息.项目信息.不入库设施名称列表"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_规划地块", u"入库_规划地块", parameterList)
    
class ru_ku_she_shi(object):
    # 入库_设施
    def __init__(self):
        self.label = u"入库_设施"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"设施要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'SS_配套设施'},
            {"name": u"单元名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'临江单元'},
            {"name": u"批复时间", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"批复文号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'XG_PTSS'},
            {"name": u"不入库设施名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": u"基本信息.项目信息.不入库设施名称列表"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_设施", u"入库_设施", parameterList)
    
class ru_ku_dan_yuan_de_qing(object):
    # 入库_单元_德清
    def __init__(self):
        self.label = u"入库_单元_德清"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"单元要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_控规单元'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_控规单元1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_单元_德清", u"入库_单元_德清", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_di_kuai_hou_tui_xian(object):
    # 入库_控制线_德清_地块后退线
    def __init__(self):
        self.label = u"入库_控制线_德清_地块后退线"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"多层后退线要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_后退线_多层'},
            {"name": u"高层后退线要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_后退线_高层'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_地块后退线'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_地块后退线1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_控制线_德清_地块后退线", u"入库_控制线_德清_地块后退线", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_te_shu_fan_wei_xian(object):
    # 入库_控制线_德清_特殊范围线
    def __init__(self):
        self.label = u"入库_控制线_德清_特殊范围线"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"控制线要素路径列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['GZW_虚位控制绿地', 'GZW_虚位控制道路', 'GZW_用地功能引导', 'GZW_高度分区线']},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_特殊范围线'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_特殊范围线1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_控制线_德清_特殊范围线", u"入库_控制线_德清_特殊范围线", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_dao_lu_zhong_xian(object):
    # 入库_控制线_德清_道路中线
    def __init__(self):
        self.label = u"入库_控制线_德清_道路中线"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"道路要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DL_道路中线'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_道路中心线'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_道路中心线1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_控制线_德清_道路中线", u"入库_控制线_德清_道路中线", parameterList)
    
class ru_ku_kong_zhi_xian_de_qing_dao_lu_bian_xian(object):
    # 入库_控制线_德清_道路边线
    def __init__(self):
        self.label = u"入库_控制线_德清_道路边线"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_道路红线'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_道路红线1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_控制线_德清_道路边线", u"入库_控制线_德清_道路边线", parameterList)
    
class ru_ku_gui_hua_di_kuai_de_qing(object):
    # 入库_规划地块_德清
    def __init__(self):
        self.label = u"入库_规划地块_德清"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_控规地块'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_控规地块1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_规划地块_德清", u"入库_规划地块_德清", parameterList)
    
class ru_ku_gui_hua_di_kuai_de_qing_shui_yu(object):
    # 入库_规划地块_德清_水域
    def __init__(self):
        self.label = u"入库_规划地块_德清_水域"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"是否已输入水体名称", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_水域'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_水域1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_规划地块_德清_水域", u"入库_规划地块_德清_水域", parameterList)
    
class ru_ku_gui_hua_di_kuai_de_qing_dao_lu(object):
    # 入库_规划地块_德清_道路
    def __init__(self):
        self.label = u"入库_规划地块_德清_道路"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_道路面'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_道路面1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_规划地块_德清_道路", u"入库_规划地块_德清_道路", parameterList)
    
class ru_ku_she_shi_de_qing(object):
    # 入库_设施_德清
    def __init__(self):
        self.label = u"入库_设施_德清"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"入库\\入库_德清"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"设施要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'SS_配套设施'},
            {"name": u"入库要素模板", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AC_RK_配套设施'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AC_RK_配套设施1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.入库.入库_德清.入库_设施_德清", u"入库_设施_德清", parameterList)
    
class yong_tu_fen_qu_bian_hao_sheng_cheng(object):
    # 用途分区编号生成
    def __init__(self):
        self.label = u"用途分区编号生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"分区"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"分区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用途分区图'},
            {"name": u"分区名称字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.分区要素字段映射.分区名称字段名称"},
            {"name": u"分区编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.分区要素字段映射.分区编号字段名称"},
            {"name": u"单元编号", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'FY07'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.分区.用途分区编号生成", u"用途分区编号生成", parameterList)
    
class yong_tu_fen_qu_gui_hua_tu_sheng_cheng(object):
    # 用途分区规划图生成
    def __init__(self):
        self.label = u"用途分区规划图生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"分区"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地调整要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地调整图'},
            {"name": u"农田整备要素名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['YD_上位_粮食生产功能区', 'YD_上位农用地落实_耕地质量提升']},
            {"name": u"城镇集建区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇集建区'},
            {"name": u"城镇弹性区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇弹性区'},
            {"name": u"永久基本农田要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_永久基本农田'},
            {"name": u"城镇开发边界外集建区修改要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YT_城镇开发边界外集建区修改'},
            {"name": u"其他需要叠合的要素名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": []},
            {"name": u"批量分区名称替换列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [['陆域生态控制区', '一般农业区'], ['林业发展区', '一般农业区']]},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'DIST_用途分区规划图'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.分区.用途分区规划图生成", u"用途分区规划图生成", parameterList)
    
class yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_fen_qu(object):
    # 用地_工具集_根据入库要素生成分区
    def __init__(self):
        self.label = u"用地_工具集_根据入库要素生成分区"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"分区\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"分区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_YTFQ'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.分区.工具集.根据入库要素生成分区", u"用地_工具集_根据入库要素生成分区", parameterList)
    
class qu_chu_zi_duan_zhong_suo_you_kong_ge(object):
    # 去除字段中所有空格
    def __init__(self):
        self.label = u"去除字段中所有空格"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"分析\\字段值检查"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"去除字段值中前后的空格", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"去除字段值内的空格", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.分析.字段值检查.去除字段中所有空格", u"去除字段中所有空格", parameterList)
    
class qu_yu_geng_xin(object):
    # 区域更新
    def __init__(self):
        self.label = u"区域更新"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"区域"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"区域要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_街坊范围线'},
            {"name": u"区域要素中编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'区域编号'},
            {"name": u"用地要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"用地要素中所属区域字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'所属街区'},
            {"name": u"设施要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'SS_配套设施'},
            {"name": u"设施要素中所属区域字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'所属街区'},
            {"name": u"有扣除地类系数的要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_三调筛选_扣除地类系数'},
            {"name": u"是否不汇总部分设施", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"不汇总设施名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": u"基本信息.项目信息.不入库设施名称列表"},
            {"name": u"不汇总设施所在地块地类列表", "dataType": u"任何值", "required": u"选填", "argsDirction": u"输入参数", "multiValue": True, "default": None},
            {"name": u"是否计算用地和设施的所属区域", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否按区域对用地进行分割", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否统计耕地保有量", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否统计永久基本农田", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"永久基本农田要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.KZX_永久基本农田要素名称"},
            {"name": u"是否统计生态保护红线", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"生态保护红线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.KZX_生态保护红线要素名称"},
            {"name": u"是否统计村庄建设边界", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"村庄建设边界要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.KZX_村庄建设边界要素名称"},
            {"name": u"是否统计设施", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.区域.区域更新", u"区域更新", parameterList)
    
class qu_yu_jian_cha(object):
    # 区域检查
    def __init__(self):
        self.label = u"区域检查"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"区域\\分析"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"区域要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"范围检查要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.区域.分析.区域检查", u"区域检查", parameterList)
    
class qu_yu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_qu_yu(object):
    # 区域_工具集_根据入库要素生成区域
    def __init__(self):
        self.label = u"区域_工具集_根据入库要素生成区域"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"区域\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"区域要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_分村范围线'},
            {"name": u"区域要素类型", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'街区街坊分村'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.区域.工具集.根据入库要素生成区域", u"区域_工具集_根据入库要素生成区域", parameterList)
    
class dao_ru_shu_xing_biao(object):
    # 导入属性表
    def __init__(self):
        self.label = u"导入属性表"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"属性"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"EXCEL文件路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\1-核对机动车位.xlsx'},
            {"name": u"EXCEL文件中表格名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'sheet1'},
            {"name": u"映射字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'实体GUID'},
            {"name": u"需更新字段名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['*']},
            {"name": u"需更新字段类型列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['*']},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.属性.导入属性表", u"导入属性表", parameterList)
    
class shu_xing_dui_bi(object):
    # 属性对比
    def __init__(self):
        self.label = u"属性对比"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"属性"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径1", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"输入要素路径2", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"映射字段名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['_ID', '_ID']},
            {"name": u"是否导出变更项", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"对比字段名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [['所属街区', '所属街区'], ['所属分村', '所属分村']]},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.属性.属性对比", u"属性对比", parameterList)
    
class zuo_biao_xi_tong_yi(object):
    # 坐标系统一
    def __init__(self):
        self.label = u"坐标系统一"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['YD_基期初转换']},
            {"name": u"坐标系", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"PROJCS['CGCS2000_3_Degree_GK_CM_120E',GEOGCS['GCS_China_Geodetic_Coordinate_System_2000',DATUM['D_China_2000',SPHEROID['CGCS2000',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',120.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.坐标系统一", u"坐标系统一", parameterList)
    
class zi_duan_ming_cheng_xiao_xie_gai_da_xie(object):
    # 字段名称小写改大写
    def __init__(self):
        self.label = u"字段名称小写改大写"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['JX_规划范围线']},
            {"name": u"输出要素路径列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输出参数", "multiValue": True, "default": ['内存临时']},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.字段名称小写改大写", u"字段名称小写改大写", parameterList)
    
class dao_ru_cong_CAD(object):
    # 导入从CAD
    def __init__(self):
        self.label = u"导入从CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入CAD数据集中的要素类路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg\\控规地块'},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否转曲", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'CZ_CAD色块'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.导入从CAD", u"导入从CAD", parameterList)
    
class dao_chu_dao_CAD(object):
    # 导出到CAD
    def __init__(self):
        self.label = u"导出到CAD"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"需融合字段名称", "dataType": u"字符串", "required": u"选填", "argsDirction": u"输入参数", "multiValue": False, "default": None},
            {"name": u"需融合字段中需融合的值的列表", "dataType": u"任何值", "required": u"选填", "argsDirction": u"输入参数", "multiValue": True, "default": None},
            {"name": u"切分阈值", "dataType": u"字符串", "required": u"选填", "argsDirction": u"输入参数", "multiValue": False, "default": None},
            {"name": u"是否去孔", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"CAD中图层采用的字段的名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'地类编号'},
            {"name": u"输出CAD路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.导出到CAD", u"导出到CAD", parameterList)
    
class shu_xing_yu_xiu_fu(object):
    # 属性域修复
    def __init__(self):
        self.label = u"属性域修复"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['YD_基期初转换']},
            {"name": u"输出要素路径列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输出参数", "multiValue": True, "default": ['内存临时']},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.属性域修复", u"属性域修复", parameterList)
    
class yao_su_chuang_jian_tong_guo_geng_xin_gen_ju_mian(object):
    # 要素创建_通过更新_根据面
    def __init__(self):
        self.label = u"要素创建_通过更新_根据面"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"区域要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_街区范围线'},
            {"name": u"字段映射列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [['所属街区', '街区编号']]},
            {"name": u"计算方式", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'分割输入要素'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.属性更新", u"要素创建_通过更新_根据面", parameterList)
    
class shu_ju_jian_cha(object):
    # 数据检查
    def __init__(self):
        self.label = u"数据检查"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg\\控规地块'},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否曲线检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否几何修复", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否多部件检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"碎线检查阈值", "dataType": u"字符串", "required": u"选填", "argsDirction": u"输入参数", "multiValue": False, "default": None},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.数据检查", u"数据检查", parameterList)
    
class qu_zhuan_zhe(object):
    # 曲转折
    def __init__(self):
        self.label = u"曲转折"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['YD_基期初转换']},
            {"name": u"手动确认是否转换", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.曲转折", u"曲转折", parameterList)
    
class qing_li_li_shi_yao_su(object):
    # 清理历史要素
    def __init__(self):
        self.label = u"清理历史要素"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入数据库路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'C:\\Users\\common\\Project\\D德清洛舍杨树湾单元控规\\03过程文件\\24.11.27报批稿\\D德清洛舍杨树湾单元控规_数据库.gdb'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.清理历史要素", u"清理历史要素", parameterList)
    
class tong_ji(object):
    # 统计
    def __init__(self):
        self.label = u"统计"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YD_基期初转换'},
            {"name": u"需统计字段及统计方式列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": [{'字段名称': '', '统计方式': '求和'}]},
            {"name": u"分组字段列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['分组1']},
            {"name": u"筛选表达式", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"是否显示进度条", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.统计", u"统计", parameterList)
    
class yao_su_lian_he(object):
    # 要素联合
    def __init__(self):
        self.label = u"要素联合"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"常用"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"联合要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.常用.要素联合", u"要素联合", parameterList)
    
class yong_di_die_he_tu_sheng_cheng(object):
    # 用地叠合图生成
    def __init__(self):
        self.label = u"用地叠合图生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['DIST_用地现状图', 'YD_审批信息已批未建', 'YD_上位_粮食生产功能区', 'YD_上位基本农田落实', 'YD_上位农用地落实_耕地质量提升', 'YD_上位农用地落实_旱改水', 'YD_上位农用地落实_垦造耕地', 'YD_上位农用地落实_新增设施农用地']},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否曲线检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'DIST_用地叠合图'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.用地叠合图生成", u"用地叠合图生成", parameterList)
    
class yong_di_ji_qi_tu_sheng_cheng(object):
    # 用地基期图生成
    def __init__(self):
        self.label = u"用地基期图生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['YD_基期细化', 'YD_农转用20年及以前']},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否曲线检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'DIST_用地基期图'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.用地基期图生成", u"用地基期图生成", parameterList)
    
class yong_di_geng_xin(object):
    # 用地更新
    def __init__(self):
        self.label = u"用地更新"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"局部更新SQL语句", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u''},
            {"name": u"街坊范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_街坊范围线'},
            {"name": u"分村范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_分村范围线'},
            {"name": u"城镇集建区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇集建区'},
            {"name": u"城镇弹性区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇弹性区'},
            {"name": u"有扣除地类系数的要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_三调筛选_扣除地类系数'},
            {"name": u"有坐落单位信息的要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_三调筛选_坐落单位名称'},
            {"name": u"设施要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'SS_配套设施'},
            {"name": u"是否进行合规性检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否对用地边界进行调整", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否重新计算所属街区街坊和分村", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否重新计算耕保量", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否根据地类编号生成地类名称", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否计算地块编号", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"开发边界内非建设用地是否编号", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"道路是否编号", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"开发边界外非建设用地是否编号", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否计算土地码", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否计算开发动态", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否计算地块内设施规模", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否计算建筑规模市政规模等其他属性", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否计算机动车开口", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"开口符号要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YD_TZ_机动车开口方位'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.用地更新", u"用地更新", parameterList)
    
class yong_di_xian_zhuang_tu_sheng_cheng(object):
    # 用地现状图生成
    def __init__(self):
        self.label = u"用地现状图生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['DIST_用地基期图', 'YD_现状修改1', 'YD_农转用21年及以后', 'YD_审批信息已实施', 'YD_地籍信息', 'YD_现状修改2']},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": False},
            {"name": u"是否曲线检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'DIST_用地现状图'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.用地现状图生成", u"用地现状图生成", parameterList)
    
class yong_di_gui_hua_tu_sheng_cheng(object):
    # 用地规划图生成
    def __init__(self):
        self.label = u"用地规划图生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称列表", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['DIST_用地叠合图', 'YD_GIS方案_农用地设计']},
            {"name": u"CAD导出色块要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_CAD导入_用地规划'},
            {"name": u"CAD导出色块中空隙的地类", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'00'},
            {"name": u"CAD导出色块中有效的地类列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['07%', '08%', '09%', '10%', '11%', '12%', '13%', '14%', '15%', '16%', '1701%', '1702%', '1703%', '23%']},
            {"name": u"CAD导出色块中有效部分的要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YD_CAD方案'},
            {"name": u"CAD导出色块以外地类调整要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YD_GIS方案_建设用地修改'},
            {"name": u"GIS中已处理的细小面要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YD_GIS方案_细小面处理'},
            {"name": u"允许合并的细小面地类名称列表", "dataType": u"任何值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": True, "default": ['01%', '02%', '03%', '04%', '05%', '06%', '1207%', '17%']},
            {"name": u"细小面面积阈值", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'10'},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.JX_规划范围线要素名称"},
            {"name": u"是否拓扑检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否范围检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"是否曲线检查", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'DIST_用地规划图'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.用地规划图生成", u"用地规划图生成", parameterList)
    
class yong_di_chuang_jian_sheng_cheng_yong_di_tiao_zheng_tu(object):
    # 用地创建_生成用地调整图
    def __init__(self):
        self.label = u"用地创建_生成用地调整图"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"二调要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地二调图'},
            {"name": u"基期要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地基期图'},
            {"name": u"规划要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"种植属性要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_三调_种植属性名称"},
            {"name": u"坐落单位要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_三调_坐落单位名称"},
            {"name": u"既有用地调整图", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地调整图'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.用地调整图生成", u"用地创建_生成用地调整图", parameterList)
    
class kai_fa_bian_jie_nei_gong_ye_yong_di(object):
    # 开发边界内工业用地
    def __init__(self):
        self.label = u"开发边界内工业用地"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\临时"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"控制线_城镇开发边界", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇开发边界'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'AA_开发边界内工业用地'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.临时.用地_临时_开发边界内工业用地", u"开发边界内工业用地", parameterList)
    
class yong_di_ji_suan_tiao_zheng_lei_xing(object):
    # 用地_计算调整类型
    def __init__(self):
        self.label = u"用地_计算调整类型"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\临时"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地调整要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'in_memory\\AA_计算调整类型'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.临时.用地_临时_计算调整类型", u"用地_计算调整类型", parameterList)
    
class jian_cha_di_kuai_bian_hao_he_tu_di_ma_shi_fou_you_wen_ti(object):
    # 检查地块编号和土地码是否有问题
    def __init__(self):
        self.label = u"检查地块编号和土地码是否有问题"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\分析"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"地块编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地块编号字段名称"},
            {"name": u"土地码字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.土地码字段名称"},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地类编号字段名称"},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.分析.地块编号和土地码检查", u"检查地块编号和土地码是否有问题", parameterList)
    
class di_lei_bian_hao_ming_cheng_bie_cheng_pi_pei_jian_cha(object):
    # 地类编号名称别称匹配检查
    def __init__(self):
        self.label = u"地类编号名称别称匹配检查"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\分析"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地类编号字段名称"},
            {"name": u"主地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.主地类编号字段名称"},
            {"name": u"性质名称字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.性质名称字段名称"},
            {"name": u"地块性质别称字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地块性质别称字段名称"},
            {"name": u"用地构成字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.用地大类字段名称"},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.分析.地类编号名称别称匹配检查", u"地类编号名称别称匹配检查", parameterList)
    
class ji_ben_nong_tian_shi_fou_bei_zhan(object):
    # 基本农田是否被占
    def __init__(self):
        self.label = u"基本农田是否被占"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\分析"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"基本农田要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_永久基本农田'},
            {"name": u"是否输出到CAD", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": False},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.分析.基本农田是否被占", u"基本农田是否被占", parameterList)
    
class kai_fa_bian_jie_wai_cheng_zhen_jian_she_yong_di_jian_cha(object):
    # 开发边界外城镇建设用地检查
    def __init__(self):
        self.label = u"开发边界外城镇建设用地检查"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\分析"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"城镇集建区", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇集建区'},
            {"name": u"城镇弹性区", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇弹性区'},
            {"name": u"输出要素名称_开发边界内", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            {"name": u"输出要素名称_开发边界外", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            {"name": u"输出要素名称_开发边界外建设用地", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            {"name": u"输出要素名称_开发边界内非建设用地", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.分析.开发边界内外用地检查", u"开发边界外城镇建设用地检查", parameterList)
    
class yong_di_he_gui_xing_jian_cha(object):
    # 用地合规性检查
    def __init__(self):
        self.label = u"用地合规性检查"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\分析"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"检查字段是否存在缺失", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"检查字段类型是否正确", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"检查地类编号是否存在空值", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.分析.用地合规性检查", u"用地合规性检查", parameterList)
    
class chu_bu_ji_shu_zhuan_huan_san_diao(object):
    # 初步基数转换_三调
    def __init__(self):
        self.label = u"初步基数转换_三调"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\基期"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'YD_三调_字段汉化'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.基期.初步基数转换_三调", u"初步基数转换_三调", parameterList)
    
class chu_bu_ji_shu_zhuan_huan_er_diao(object):
    # 初步基数转换_二调
    def __init__(self):
        self.label = u"初步基数转换_二调"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\基期"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_二调_字段汉化'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.基期.初步基数转换_二调", u"初步基数转换_二调", parameterList)
    
class zi_duan_chu_li_bing_sheng_cheng_fen_xiang_san_diao(object):
    # 字段处理并生成分项_三调
    def __init__(self):
        self.label = u"字段处理并生成分项_三调"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\基期"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_三调'},
            {"name": u"扣除地类系数要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_三调_扣除地类系数"},
            {"name": u"种植属性名称要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_三调_种植属性名称"},
            {"name": u"城镇村属性码要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_三调_城镇村属性码"},
            {"name": u"坐落单位名称要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_三调_坐落单位名称"},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.基期.字段处理并生成分项_三调", u"字段处理并生成分项_三调", parameterList)
    
class zi_duan_chu_li_bing_sheng_cheng_fen_xiang_er_diao(object):
    # 字段处理并生成分项_二调
    def __init__(self):
        self.label = u"字段处理并生成分项_二调"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\基期"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_二调'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.基期.字段处理并生成分项_二调", u"字段处理并生成分项_二调", parameterList)
    
class di_lei_zhuan_huan_cheng_xiang_di_lei_zhuan_guo_kong_di_lei(object):
    # 地类转换_城乡地类转国空地类
    def __init__(self):
        self.label = u"地类转换_城乡地类转国空地类"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地类编号字段名称"},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.地类转换_城乡地类转国空地类", u"地类转换_城乡地类转国空地类", parameterList)
    
class di_lei_zhuan_huan_jiu_ban_guo_kong_di_lei_zhuan_xin_ban_guo_kong_di_lei(object):
    # 地类转换_旧版国空地类转新版国空地类
    def __init__(self):
        self.label = u"地类转换_旧版国空地类转新版国空地类"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地类编号字段名称"},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.地类转换_旧版国空地类转新版国空地类", u"地类转换_旧版国空地类转新版国空地类", parameterList)
    
class yong_di_gong_ju_ji_geng_xin_dui_xiang_shu_xing(object):
    # 用地_工具集_更新对象属性
    def __init__(self):
        self.label = u"用地_工具集_更新对象属性"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"属性所在要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'AA_户数指标'},
            {"name": u"属性所在字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'Text'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.更新对象属性", u"用地_工具集_更新对象属性", parameterList)
    
class yong_di_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_yong_di(object):
    # 用地_工具集_根据入库要素生成用地
    def __init__(self):
        self.label = u"用地_工具集_根据入库要素生成用地"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"地块要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_GHDK'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.根据入库要素生成用地", u"用地_工具集_根据入库要素生成用地", parameterList)
    
class yong_di_chuang_jian_tong_guo_gen_ju_di_lei_ming_cheng_sheng_cheng_bian_hao(object):
    # 用地创建_通过根据地类名称生成编号
    def __init__(self):
        self.label = u"用地创建_通过根据地类名称生成编号"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"地类名称字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'地类名称'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'in_memory\\AA_计算地类编号'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.根据地类名称生成编号", u"用地创建_通过根据地类名称生成编号", parameterList)
    
class yong_di_gong_ju_ji_yong_di_shu_ju_tong_ji(object):
    # 用地_工具集_用地数据统计
    def __init__(self):
        self.label = u"用地_工具集_用地数据统计"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地类编号字段名称"},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.用地数据统计", u"用地_工具集_用地数据统计", parameterList)
    
class tong_ji_kai_fa_bian_jie_wai_ji_qi_203_yong_di(object):
    # 统计开发边界外基期203用地
    def __init__(self):
        self.label = u"统计开发边界外基期203用地"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"基期要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"城镇集建区要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"城镇弹性区要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"规划范围线要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"坐落单位要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.统计开发边界外基期203用地", u"统计开发边界外基期203用地", parameterList)
    
class yong_di_chuang_jian_tong_guo_ji_suan_liang_ke_yong_di(object):
    # 用地创建_通过计算两可用地
    def __init__(self):
        self.label = u"用地创建_通过计算两可用地"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素名称", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False},
            {"name": u"有种植属性的要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'CZ_三调筛选_种植属性名称'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'in_memory\\AA_计算两可用地'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.计算两可用地", u"用地创建_通过计算两可用地", parameterList)
    
class ji_suan_wen_ben_lian_jie_yong_shu_ju(object):
    # 计算文本链接用数据
    def __init__(self):
        self.label = u"计算文本链接用数据"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"用地\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地规划要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.YD_用地_规划要素名称"},
            {"name": u"用地调整要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.YD_用地_调整要素名称"},
            {"name": u"用途分区要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.FQ_用途分区_规划要素名称"},
            {"name": u"城镇集建区要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.KZX_城镇集建区要素名称"},
            {"name": u"城镇弹性区要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.KZX_城镇弹性区要素名称"},
            {"name": u"永久基本农田要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.KZX_永久基本农田要素名称"},
            {"name": u"规划范围线要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.JX_规划范围线要素名称"},
            {"name": u"上位耕地质量提升要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.项目信息.CZ_上位规划_耕地质量提升"},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'地类名称'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.用地.工具集.计算文本链接用数据", u"计算文本链接用数据", parameterList)
    
class she_shi_geng_xin(object):
    # 设施更新
    def __init__(self):
        self.label = u"设施更新"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"设施"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"输入要素路径", "dataType": u"要素类", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'SS_配套设施'},
            {"name": u"是否根据坐标字段移动设施坐标", "dataType": u"布尔值", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": True},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"工业片区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_工业片区范围线'},
            {"name": u"街区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_街区范围线'},
            {"name": u"街坊要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_街坊范围线'},
            {"name": u"分村要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_分村范围线'},
            {"name": u"用地规划要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"与用地规划要素中配套设施如何统一", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'从设施到用地'},
            {"name": u"城镇集建区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇集建区'},
            {"name": u"城镇弹性区要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'KZX_城镇弹性区'},
            {"name": u"输出要素路径_用地", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            {"name": u"输出要素路径_设施", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.设施.设施更新", u"设施更新", parameterList)
    
class she_shi_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_she_shi(object):
    # 设施_工具集_根据入库要素生成设施
    def __init__(self):
        self.label = u"设施_工具集_根据入库要素生成设施"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"设施\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"设施要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_PTSS'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.设施.工具集.根据入库要素生成设施", u"设施_工具集_根据入库要素生成设施", parameterList)
    
class he_dao_bian_xian_sheng_cheng(object):
    # 河道边线生成
    def __init__(self):
        self.label = u"河道边线生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"道路"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"河道中线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DL_河道中线'},
            {"name": u"用地要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"河道用地修正要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DL_河道用地修正'},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"修正要素路径", "dataType": u"字符串", "required": u"选填", "argsDirction": u"输入参数", "multiValue": False, "default": None},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.道路.河道边线生成", u"河道边线生成", parameterList)
    
class dao_lu_bian_xian_sheng_cheng(object):
    # 道路边线生成
    def __init__(self):
        self.label = u"道路边线生成"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"道路"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"道路中线要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DL_道路中线'},
            {"name": u"用地要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"规划范围线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'JX_规划范围线'},
            {"name": u"输出要素路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.道路.道路边线生成", u"道路边线生成", parameterList)
    
class dao_lu_gong_ju_ji_gen_ju_ru_ku_yao_su_sheng_cheng_kong_zhi_xian(object):
    # 道路_工具集_根据入库要素生成控制线
    def __init__(self):
        self.label = u"道路_工具集_根据入库要素生成控制线"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"道路\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"控制线要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'XG_KZX'},
            {"name": u"输出要素名称后缀", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'1'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.道路.工具集.根据入库要素生成控制线", u"道路_工具集_根据入库要素生成控制线", parameterList)
    
class dao_lu_hong_xian_ti_qu(object):
    # 道路红线提取
    def __init__(self):
        self.label = u"道路红线提取"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"道路\\工具集"

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"用地要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'DIST_用地规划图'},
            {"name": u"地类编号字段名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u"基本信息.地块要素字段映射.地类编号字段名称"},
            {"name": u"导出到CAD路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop\\01.dwg'},
            {"name": u"输出要素名称", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输出参数", "multiValue": False, "default": u'内存临时'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.道路.工具集.道路红线提取", u"道路红线提取", parameterList)
    
class di_kuai_zhi_biao_ce_suan_biao_huo_qu(object):
    # 地块指标测算表获取
    def __init__(self):
        self.label = u"地块指标测算表获取"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"配置"

    def getParameterInfo(self):
        args_dict_list = [
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.配置.基本信息", u"地块指标测算表获取", parameterList)
    
class huo_qu_gong_zuo_kong_jian(object):
    # 获取工作空间
    def __init__(self):
        self.label = u"获取工作空间"
        self.description = ""
        self.canRunInBackground = False
        self.category = u"配置"

    def getParameterInfo(self):
        args_dict_list = [
        ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.配置.配置包", u"获取工作空间", parameterList)
    
class xiang_mu_chu_shi_hua(object):
    # 项目初始化
    def __init__(self):
        self.label = u"项目初始化"
        self.description = ""
        self.canRunInBackground = False
        self.category = u""

    def getParameterInfo(self):
        args_dict_list = [
        {"name": u"项目文件夹路径", "dataType": u"字符串", "required": u"必填", "argsDirction": u"输入参数", "multiValue": False, "default": u'C:\\Users\\beixiao\\Desktop'},
            ]
        return ParameterCls.parameterCreate_muti(args_dict_list)

    def execute(self, parameterList, message):
        fun_run(u"bxgis.配置.项目初始化", u"项目初始化", parameterList)
    