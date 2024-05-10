import bxarcpy
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 入库_局调入库(输入要素="AA_规划工业用地"):  # 用地_格式化_修改为入库格式
    # To allow overwriting outputs change overwriteOutput option to True.
    # arcpy.env.overwriteOutput = False

    删除字段 = ["Entity", "Color", "Linetype", "Elevation", "LineWt", "RefName", "mj", "FID_YJJBNTBHTB", "BSM", "YSDM", "XZQDM", "XZQMC", "YJJBNTTBBH", "TBBH", "DLBM", "DLMC", "QSXZ", "QSDWDM", "QSDWMC", "ZLDWDM", "ZLDWMC", "YJJBNTTBMJ", "KCDLBM", "KCXS", "KCMJ", "YJJBNTMJ", "GDLX", "GDPDJB", "GGBZL", "TBXHDM", "TBXHMC", "ZZSXDM", "ZZSXMC", "GDDB", "GDDJ", "ZLFLDM", "FRDBS", "SJNF", "CFZR", "ZMC", "ZZRR", "ZRRZJHM", "ZRRMC", "LXDH", "JZDZ", "BHKSSJ", "BHJSSJ", "SJBH", "SJMC", "ZRSYX", "BZ", "WDGD", "SFWYYJJBNT", "FWDGDHRLY", "FID_规划范围线_2303070850", "序号", "组名", "村名称", "街道", "二调耕", "三调耕", "三调恢", "二调永", "三调稳", "Shape_Leng", "FID_4去除", "名称", "镇街名称", "a", "ORIG_FID", "三调地类编号", "三调地类名称", "CZCSXM", "Layer", "地块性质", "实体类型", "GKXZ", "FID_DLTB", "TBYBH", "单元名", "地块性", "dkbmgk"]

    地类转换路径 = "C:\\Users\\common\\AppConfig\\ArcGIS\\020.地类转换\\地类转换_国空与城乡地类转换.xls\\Sheet1$"
    输出要素 = 要素类.字段添加(输入要素, 字段名称="GHDY", 字段类型="字符串", 字段长度=50, 字段别称="规划编制单元名称")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="GHDY", 表达式="'临江单元'", 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="PFSJ", 字段类型="日期", 字段长度=100, 字段别称="批复时间")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="YDXZMC", 字段类型="字符串", 字段长度=50, 字段别称="用地性质名称")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="YDXZMC", 表达式="!性质名称!", 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="PFWH", 字段类型="字符串", 字段长度=50, 字段别称="批复文号")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="DKBH", 字段类型="字符串", 字段长度=50, 字段别称="地块编号")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="DKBH", 表达式="!地块编号!", 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="MJ", 字段类型="双精度", 字段长度=10, 字段别称="面积")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="MJ", 表达式="!面积公顷!", 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="RJL", 字段类型="单精度", 字段长度=10, 字段别称="容积率")
    容积率计算 = """
        def test(x):
            if x:
                return float(x)
        """
    输出要素 = 要素类.字段计算(输出要素, 字段名称="RJL", 表达式="test(!容积率!)", 字段类型="字符串", 代码块=容积率计算)
    输出要素 = 要素类.字段添加(输出要素, 字段名称="RJL_XX", 字段类型="单精度", 字段长度=10, 字段别称="容积率下限")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="LDL", 字段类型="单精度", 字段长度=10, 字段别称="绿地率")
    绿地率计算 = """
        def test(x):
            if x:
                return float(x)
        """
    输出要素 = 要素类.字段计算(输出要素, 字段名称="LDL", 表达式="test(!绿地率!)", 字段类型="字符串", 代码块=绿地率计算)
    输出要素 = 要素类.字段添加(输出要素, 字段名称="LDL_SX", 字段类型="单精度", 字段长度=10, 字段别称="绿地率上限")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="JZMD", 字段类型="单精度", 字段长度=10, 字段别称="建筑密度")
    建筑密度计算 = """
        def test(x):
            if x and x != "方案阶段名称":
                return float(x)
        """
    输出要素 = 要素类.字段计算(输出要素, 字段名称="JZMD", 表达式="test(!建筑密度!)", 字段类型="字符串", 代码块=建筑密度计算)
    输出要素 = 要素类.字段添加(输出要素, 字段名称="JZMD_XX", 字段类型="单精度", 字段长度=10, 字段别称="建筑密度下限")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="JZXG", 字段类型="单精度", 字段长度=10, 字段别称="建筑限高")
    建筑限高计算 = """
        def test(x):
            x = x.split('-')[0]
            if x:
                return float(x)
        """
    输出要素 = 要素类.字段计算(输出要素, 字段名称="JZXG", 表达式="test(!建筑限高!)", 字段类型="字符串", 代码块=建筑限高计算)
    输出要素 = 要素类.字段添加(输出要素, 字段名称="JZXG_XX", 字段类型="单精度", 字段长度=10, 字段别称="建筑限高下限")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="JDCW", 字段类型="短整型", 字段长度=10, 字段别称="机动车位")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="JDCW_SX", 字段类型="短整型", 字段长度=10, 字段别称="机动车位上限")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="FJDCW", 字段类型="短整型", 字段长度=10, 字段别称="非机动车位")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="FJDCW_SX", 字段类型="短整型", 字段长度=10, 字段别称="非机动车位上限")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="TDM", 字段类型="字符串", 字段长度=50, 字段别称="土地码")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="BZ", 字段类型="字符串", 字段长度=255, 字段别称="备注")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="BZ", 表达式="!备注说明!", 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="YDXZ_N", 字段类型="字符串", 字段长度=50, 字段别称="用地性质代码_新地类")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="YDXZ_N", 表达式="!地类编号!", 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="YDXZ", 字段类型="字符串", 字段长度=50, 字段别称="用地性质代码")
    输出要素 = 要素类.连接创建(输出要素, "YDXZ_N", 地类转换路径, "新地类编号")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="YDXZ", 表达式="!Sheet1$.旧地类编号!", 字段类型="字符串")
    要素类.连接取消(输出要素, 地类转换路径)
    输出要素 = 要素类.字段添加(输出要素, 字段名称="ZYDXZ_N", 字段类型="字符串", 字段长度=10, 字段别称="主用地性质代码_新地类")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="ZYDXZ_N", 表达式='!地类编号!.split("(")[0].split("/")[0]', 字段类型="字符串")
    输出要素 = 要素类.字段添加(输出要素, 字段名称="ZYDXZ", 字段类型="字符串", 字段长度=10, 字段别称="主用地性质代码")
    输出要素 = 要素类.连接创建(输出要素, "ZYDXZ_N", 地类转换路径, "新地类编号")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="ZYDXZ", 表达式="!Sheet1$.旧地类编号!", 字段类型="字符串")
    要素类.连接取消(输出要素, 地类转换路径)
    输出要素 = 要素类.字段添加(输出要素, 字段名称="TDLX", 字段类型="字符串", 字段长度=255, 字段别称="土地类型")
    输出要素 = 要素类.连接创建(输出要素, "YDXZ_N", 地类转换路径, "新地类编号")
    输出要素 = 要素类.字段计算(输出要素, 字段名称="TDLX", 表达式="!Sheet1$.地类大类!", 字段类型="字符串")
    要素类.连接取消(输出要素, 地类转换路径)


if __name__ == "__main__":
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间=工作空间):
        入库_局调入库(输入要素="\\AA_规划工业用地")
