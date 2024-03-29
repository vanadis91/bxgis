import bxarcpy


def 入库_局调入库(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 输入要素="\\AA_规划工业用地"):  # 用地_格式化_修改为入库格式
    with bxarcpy.环境.环境管理器(临时工作空间=工作空间, 工作空间=工作空间):
        # To allow overwriting outputs change overwriteOutput option to True.
        bxarcpy.配置.是否覆盖输出要素 = True
        # arcpy.env.overwriteOutput = False

        删除字段 = ["Entity", "Color", "Linetype", "Elevation", "LineWt", "RefName", "mj", "FID_YJJBNTBHTB", "BSM", "YSDM", "XZQDM", "XZQMC", "YJJBNTTBBH", "TBBH", "DLBM", "DLMC", "QSXZ", "QSDWDM", "QSDWMC", "ZLDWDM", "ZLDWMC", "YJJBNTTBMJ", "KCDLBM", "KCXS", "KCMJ", "YJJBNTMJ", "GDLX", "GDPDJB", "GGBZL", "TBXHDM", "TBXHMC", "ZZSXDM", "ZZSXMC", "GDDB", "GDDJ", "ZLFLDM", "FRDBS", "SJNF", "CFZR", "ZMC", "ZZRR", "ZRRZJHM", "ZRRMC", "LXDH", "JZDZ", "BHKSSJ", "BHJSSJ", "SJBH", "SJMC", "ZRSYX", "BZ", "WDGD", "SFWYYJJBNT", "FWDGDHRLY", "FID_规划范围线_2303070850", "序号", "组名", "村名称", "街道", "二调耕", "三调耕", "三调恢", "二调永", "三调稳", "Shape_Leng", "FID_4去除", "名称", "镇街名称", "a", "ORIG_FID", "三调地类编号", "三调地类名称", "CZCSXM", "Layer", "地块性质", "实体类型", "GKXZ", "FID_DLTB", "TBYBH", "单元名", "地块性", "dkbmgk"]

        地类转换路径 = "C:\\Users\\common\\AppConfig\\ArcGIS\\020.地类转换\\地类转换_国空与城乡地类转换.xls\\Sheet1$"

        # Process: 添加字段 (4) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输入要素, 字段名称="GHDY", 字段类型="字符串", 字段长度=50, 字段别称="规划编制单元名称")

        # Process: 计算字段 (4) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="GHDY", 表达式="'临江单元'", 字段类型="字符串")

        # Process: 添加字段 (2) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="PFSJ", 字段类型="日期", 字段长度=100, 字段别称="批复时间")

        # Process: 添加字段 (5) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="YDXZMC", 字段类型="字符串", 字段长度=50, 字段别称="用地性质名称")

        # Process: 计算字段 (5) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="YDXZMC", 表达式="!性质名称!", 字段类型="字符串")

        # Process: 添加字段 (7) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="PFWH", 字段类型="字符串", 字段长度=50, 字段别称="批复文号")

        # Process: 添加字段 (8) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="DKBH", 字段类型="字符串", 字段长度=50, 字段别称="地块编号")

        # Process: 计算字段 (2) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="DKBH", 表达式="!地块编号!", 字段类型="字符串")

        # Process: 添加字段 (9) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="MJ", 字段类型="双精度", 字段长度=10, 字段别称="面积")

        # Process: 计算字段 (7) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="MJ", 表达式="!面积公顷!", 字段类型="字符串")

        # Process: 添加字段 (10) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="RJL", 字段类型="单精度", 字段长度=10, 字段别称="容积率")

        # Process: 计算字段 (8) (计算字段) (management)
        容积率计算 = """
        def test(x):
            if x:
                return float(x)
        """
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="RJL", 表达式="test(!容积率!)", 字段类型="字符串", 代码块=容积率计算)

        # Process: 添加字段 (11) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="RJL_XX", 字段类型="单精度", 字段长度=10, 字段别称="容积率下限")

        # Process: 添加字段 (12) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="LDL", 字段类型="单精度", 字段长度=10, 字段别称="绿地率")

        # Process: 计算字段 (9) (计算字段) (management)
        绿地率计算 = """
        def test(x):
            if x:
                return float(x)
        """
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="LDL", 表达式="test(!绿地率!)", 字段类型="字符串", 代码块=绿地率计算)

        # Process: 添加字段 (13) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="LDL_SX", 字段类型="单精度", 字段长度=10, 字段别称="绿地率上限")

        # Process: 添加字段 (14) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="JZMD", 字段类型="单精度", 字段长度=10, 字段别称="建筑密度")

        # Process: 计算字段 (10) (计算字段) (management)
        建筑密度计算 = """
        def test(x):
            if x and x != "方案阶段名称":
                return float(x)
        """
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="JZMD", 表达式="test(!建筑密度!)", 字段类型="字符串", 代码块=建筑密度计算)

        # Process: 添加字段 (15) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="JZMD_XX", 字段类型="单精度", 字段长度=10, 字段别称="建筑密度下限")

        # Process: 添加字段 (16) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="JZXG", 字段类型="单精度", 字段长度=10, 字段别称="建筑限高")

        # Process: 计算字段 (11) (计算字段) (management)
        建筑限高计算 = """
        def test(x):
            x = x.split('-')[0]
            if x:
                return float(x)
        """
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="JZXG", 表达式="test(!建筑限高!)", 字段类型="字符串", 代码块=建筑限高计算)

        # Process: 添加字段 (17) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="JZXG_XX", 字段类型="单精度", 字段长度=10, 字段别称="建筑限高下限")

        # Process: 添加字段 (18) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="JDCW", 字段类型="短整型", 字段长度=10, 字段别称="机动车位")

        # Process: 添加字段 (19) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="JDCW_SX", 字段类型="短整型", 字段长度=10, 字段别称="机动车位上限")

        # Process: 添加字段 (20) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="FJDCW", 字段类型="短整型", 字段长度=10, 字段别称="非机动车位")

        # Process: 添加字段 (21) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="FJDCW_SX", 字段类型="短整型", 字段长度=10, 字段别称="非机动车位上限")

        # Process: 添加字段 (22) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="TDM", 字段类型="字符串", 字段长度=50, 字段别称="土地码")

        # Process: 添加字段 (23) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="BZ", 字段类型="字符串", 字段长度=255, 字段别称="备注")

        # Process: 计算字段 (12) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="BZ", 表达式="!备注说明!", 字段类型="字符串")

        # Process: 添加字段 (3) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="YDXZ_N", 字段类型="字符串", 字段长度=50, 字段别称="用地性质代码_新地类")

        # Process: 计算字段 (3) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="YDXZ_N", 表达式="!地类编号!", 字段类型="字符串")

        # Process: 添加字段 (24) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="YDXZ", 字段类型="字符串", 字段长度=50, 字段别称="用地性质代码")

        # Process: 添加连接 (添加连接) (management)
        输出要素 = bxarcpy.数据管理.连接创建(输入要素=输出要素, 输入要素连接字段="YDXZ_N", 连接要素=地类转换路径, 连接要素连接字段="新地类编号")

        # Process: 计算字段 (14) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="YDXZ", 表达式="!Sheet1$.旧地类编号!", 字段类型="字符串")

        # Process: 移除连接 (移除连接) (management)
        bxarcpy.数据管理.连接取消(输入要素=输出要素, 连接要素=地类转换路径)

        # Process: 添加字段 (6) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="ZYDXZ_N", 字段类型="字符串", 字段长度=10, 字段别称="主用地性质代码_新地类")

        # Process: 计算字段 (6) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="ZYDXZ_N", 表达式='!地类编号!.split("(")[0].split("/")[0]', 字段类型="字符串")

        # Process: 添加字段 (25) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="ZYDXZ", 字段类型="字符串", 字段长度=10, 字段别称="主用地性质代码")

        # Process: 添加连接 (添加连接) (management)
        输出要素 = bxarcpy.数据管理.连接创建(输入要素=输出要素, 输入要素连接字段="ZYDXZ_N", 连接要素=地类转换路径, 连接要素连接字段="新地类编号")

        # Process: 计算字段 (14) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="ZYDXZ", 表达式="!Sheet1$.旧地类编号!", 字段类型="字符串")

        # Process: 移除连接 (移除连接) (management)
        bxarcpy.数据管理.连接取消(输入要素=输出要素, 连接要素=地类转换路径)

        # Process: 添加字段 (26) (添加字段) (management)
        输出要素 = bxarcpy.数据管理.字段添加(输入要素=输出要素, 字段名称="TDLX", 字段类型="字符串", 字段长度=255, 字段别称="土地类型")

        # Process: 添加连接 (3) (添加连接) (management)
        输出要素 = bxarcpy.数据管理.连接创建(输入要素=输出要素, 输入要素连接字段="YDXZ_N", 连接要素=地类转换路径, 连接要素连接字段="新地类编号")

        # Process: 计算字段 (16) (计算字段) (management)
        输出要素 = bxarcpy.数据管理.字段计算(输入要素=输出要素, 字段名称="TDLX", 表达式="!Sheet1$.地类大类!", 字段类型="字符串")

        # Process: 移除连接 (3) (移除连接) (management)
        bxarcpy.数据管理.连接取消(输入要素=输出要素, 连接要素=地类转换路径)


if __name__ == "__main__":
    入库_局调入库(工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 输入要素="\\AA_规划工业用地")
