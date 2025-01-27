# *-* coding:utf8 *-*
from typing import Union, Literal


class 计算机信息:
    CAD输出目录 = r"C:\Users\beixiao\Desktop"
    环境: Literal["生产环境", "开发环境"] = "开发环境"
    bxgis根目录 = r"C:\Users\beixiao\Project\appBXGis\src\bxgis"


class 应用信息:
    _地块指标测算表 = None
    _地块属性表 = None
    _配套指标测算表 = None

    @staticmethod
    def 地块指标测算表获取():
        if 应用信息._地块指标测算表:
            return 应用信息._地块指标测算表
        from bxpy.路径包 import 路径类
        from bxpy.基本对象包 import 字典类

        配置文件路径 = 路径类.连接(计算机信息.bxgis根目录, "配置", "地块_指标测算表.xlsx")
        应用信息._地块指标测算表 = 字典类.转换_从excel(配置文件路径, excel表名称="Sheet3", 指定数据类型={"地块性质": str, "地块性质别称": str})
        return 应用信息._地块指标测算表

    @staticmethod
    def 地块属性表获取():
        if 应用信息._地块属性表:
            return 应用信息._地块属性表
        from bxpy.路径包 import 路径类
        from bxpy.基本对象包 import 字典类

        配置文件路径 = 路径类.连接(计算机信息.bxgis根目录, "配置", "地块_属性表.xlsx")
        应用信息._地块属性表 = 字典类.转换_从excel(配置文件路径, excel表名称="Sheet1", 指定数据类型={"小数位数": str, "字段长度": str})
        return 应用信息._地块属性表

    @staticmethod
    def 配套指标测算表获取():
        if 应用信息._配套指标测算表:
            return 应用信息._配套指标测算表
        from bxpy.路径包 import 路径类
        from bxpy.基本对象包 import 字典类

        配置文件路径 = 路径类.连接(计算机信息.bxgis根目录, "配置", "配套_指标测算表_杭州新.xlsx")
        应用信息._配套指标测算表 = 字典类.转换_从excel(配置文件路径, excel表名称="Sheet3", 指定数据类型={"设施类型": str})
        return 应用信息._配套指标测算表


class 项目信息:
    # 基本信息
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    项目目录 = r"C:\Users\common\project\J江东区临江控规"
    单元名称 = "临江单元"
    单元类型: Literal["城镇单元", "乡村单元"] = "城镇单元"
    单元编号 = "QT12"
    批复时间 = "2023/12/18"
    批复文号 = "杭政函[2023]109号"
    编制单位 = "浙江大学建筑设计研究院有限公司"
    单元功能 = "以打造中国先进制造业的重要窗口为使命，以新材料产业为主导，生物医药和装备制造产业为特色，融高端智造、产业服务、现代物流于一体的一流示范产业园区。"
    人口规模 = "3.1956"
    跨单元平衡情况 = ""
    不入库设施名称列表 = [
        "移动通信基站",
        "开闭所",
        "公共交通停靠站",
        "人防警报器",
        "综合接入局",
        "人防物资库",
        "应急物资储备仓库",
        "战时救护站",
        "社区固定避难场所",
        "社区应急避难场所",
        "防灾医疗设施（街坊级）",
        "防空专业队工程",
        "一等人员掩蔽工程",
        "区域供水站",
        "防灾指挥设施",
        "食品站",
        "能源站",
        "专科医院（市）",
        "综合医院（区）",
        "边防派出所",
        "防灾医疗设施",
        "气象站",
        "热电厂",
        "有线电视分前端中心",
        "通信机房",
        "公交停保场",
    ]
    地类标准: Literal["国空", "城规"] = "国空"

    # 参照
    CZ_三调_扣除地类系数 = "CZ_三调筛选_扣除地类系数"  # 将三调中拥有扣除地类系数的图斑单独提取出来，可使用 用地/基期/字段处理并生成分项 工具来生成。
    CZ_三调_种植属性名称 = "CZ_三调筛选_种植属性名称"  # 将三调中两可用地提取出来，方式同上。
    CZ_三调_城镇村属性码 = "CZ_三调筛选_城镇村属性码"  # 将三调中城镇村属性码提取出来，方式同上。
    CZ_三调_坐落单位名称 = "CZ_三调筛选_坐落单位名称"  # 将三调中行政界线提取出来，方式同上。

    # 上位规划
    CZ_上位规划_耕地质量提升 = "YD_上位农用地落实_耕地质量提升"
    CZ_上位规划_旱改水 = "YD_上位农用地落实_旱改水"
    CZ_上位规划_垦造耕地 = "YD_上位农用地落实_垦造耕地"
    CZ_上位规划_新增设施农用地 = "YD_上位农用地落实_新增设施农用地"

    # 区域
    JX_规划范围线要素名称 = "JX_规划范围线"
    JX_工业片区范围线要素名称 = "JX_工业片区范围线"
    JX_街区范围线要素名称 = "JX_街区范围线"
    JX_街坊范围线要素名称 = "JX_街坊范围线"
    JX_分村范围线要素名称 = "JX_分村范围线"

    # 用地
    YD_用地_规划要素名称 = "DIST_用地规划图"
    YD_用地_现状要素名称 = "DIST_用地现状图"
    YD_用地_调整要素名称 = "DIST_用地调整图"

    # 分区
    FQ_用途分区_规划要素名称 = "DIST_用途分区规划图"

    # 设施
    SS_配套设施_规划要素名称 = "SS_配套设施"

    # 道路
    DL_道路中线要素名称 = "DL_道路中线"
    DL_道路边线要素名称 = "DL_道路边线"
    DL_河道中线要素名称 = "DL_河道中线"
    DL_河道边线要素名称 = "DL_河道边线"

    # 构筑物
    GZW_高架桥要素名称 = "GZW_高架桥"
    GZW_隧道要素名称 = None
    GZW_铁路线要素名称 = "GZW_铁路线"
    GZW_输油管要素名称 = None
    GZW_原水输水要素名称 = None
    GZW_高压线要素名称 = "GZW_高压线"
    GZW_天然气要素名称 = "GZW_天然气"
    GZW_综合管廊要素名称 = None
    GZW_市政管线要素名称 = None
    GZW_微波通道要素名称 = None
    GZW_高度分区要素名称 = None
    GZW_共用通道要素名称 = None
    GZW_远景道路要素名称 = None
    GZW_虚位控制河道要素名称 = "GZW_虚位控制河道"
    GZW_虚位控制道路要素名称 = "GZW_虚位控制道路"
    GZW_绿化控制线要素名称 = "GZW_绿化控制线"
    GZW_景观廊道要素名称 = None
    GZW_其他要素名称 = None

    # 控制线
    KZX_永久基本农田要素名称 = "KZX_永久基本农田"
    KZX_生态保护红线要素名称 = "KZX_生态保护红线"
    KZX_城镇集建区要素名称 = "KZX_城镇集建区"
    KZX_城镇弹性区要素名称 = "KZX_城镇弹性区"
    KZX_城镇开发边界要素名称 = "KZX_城镇开发边界"
    KZX_村庄建设边界要素名称 = "KZX_村庄建设边界"

    # 图则
    TZ_后退界线多层要素名称 = "YD_TZ_后退界线_多层"
    TZ_后退界线高层要素名称 = "YD_TZ_后退界线_高层"
    TZ_禁止开口线要素名称 = "TZ_禁止开口线"
    TZ_机动车出入口要素名称 = "YD_TZ_机动车出入口"
    TZ_景观廊道要素名称 = "TZ_景观廊道"
    TZ_重要界面要素名称 = "TZ_重要界面"
    TZ_连通道要素名称 = "TZ_连通道"
    TZ_其他图则线要素名称 = "TZ_其他图则线"
    TZ_高度分区要素名称 = "TZ_高度分区"
    TZ_开敞空间要素名称 = "TZ_开敞空间"
    TZ_地下空间要素名称 = "TZ_地下空间"
    TZ_其他图则面要素名称 = "TZ_其他图则面"
    TZ_地标建筑要素名称 = "TZ_地标建筑"
    TZ_重要视点要素名称 = "TZ_重要视点"
    TZ_其他图则点要素名称 = "TZ_其他图则点"


class 项目信息_受降:
    # 基本信息
    工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    单元名称 = "受降北单元"
    单元类型: Literal["城镇单元", "乡村单元"] = "城镇单元"
    单元编号 = "FY07"
    批复时间 = "2023/11/28"
    批复文号 = "杭政函[2023]104号"
    编制单位 = "浙江大学建筑设计研究院有限公司"
    单元功能 = "依托数字经济时代背景、银湖科技城产业平台、受降区位优势，打造以高品质生态居住区与创新产业联动平台为主导的“个性化、生态化、创新化”富阳未来宜居宜业新组团，“生态品质居住+创新智慧生产”的产城人融合活力新单元。"
    人口规模 = "6.8628"
    跨单元平衡情况 = "本单元为受降南单元解决18班小学、35班初中的缺口平衡问题。"
    不入库设施名称列表 = []
    地类标准: Literal["国空", "城规"] = "国空"

    # 参照
    CZ_三调_扣除地类系数 = "CZ_三调筛选_扣除地类系数"  # 将三调中拥有扣除地类系数的图斑单独提取出来，可使用 用地/基期/字段处理并生成分项 工具来生成。
    CZ_三调_种植属性名称 = "CZ_三调筛选_种植属性名称"  # 将三调中两可用地提取出来，方式同上。
    CZ_三调_城镇村属性码 = "CZ_三调筛选_城镇村属性码"  # 将三调中城镇村属性码提取出来，方式同上。
    CZ_三调_坐落单位名称 = "CZ_三调筛选_坐落单位名称"  # 将三调中行政界线提取出来，方式同上。

    # 上位规划
    CZ_上位规划_耕地质量提升 = "YD_上位农用地落实_耕地质量提升"
    CZ_上位规划_旱改水 = "YD_上位农用地落实_旱改水"
    CZ_上位规划_垦造耕地 = "YD_上位农用地落实_垦造耕地"
    CZ_上位规划_新增设施农用地 = "YD_上位农用地落实_新增设施农用地"

    # 区域
    JX_规划范围线要素名称 = "JX_规划范围线"
    JX_工业片区范围线要素名称 = "JX_工业片区范围线"
    JX_街区范围线要素名称 = "JX_街区范围线"
    JX_街坊范围线要素名称 = "JX_街坊范围线"
    JX_分村范围线要素名称 = "JX_分村范围线"

    # 用地
    YD_用地_规划要素名称 = "DIST_用地规划图"
    YD_用地_现状要素名称 = "DIST_用地现状图"
    YD_用地_调整要素名称 = "DIST_用地调整图"

    # 分区
    FQ_用途分区_规划要素名称 = "DIST_用途分区规划图"

    # 设施
    SS_配套设施_规划要素名称 = "SS_配套设施"

    # 道路
    DL_道路中线要素名称 = "DL_道路中线"
    DL_道路边线要素名称 = "DL_道路边线"
    DL_河道中线要素名称 = "DL_河道中线"
    DL_河道边线要素名称 = "DL_河道边线"

    # 构筑物
    GZW_高架桥要素名称 = "GZW_高架桥"
    GZW_隧道要素名称 = None
    GZW_铁路线要素名称 = "GZW_铁路线"
    GZW_输油管要素名称 = None
    GZW_原水输水要素名称 = None
    GZW_高压线要素名称 = "GZW_高压线"
    GZW_天然气要素名称 = "GZW_天然气"
    GZW_综合管廊要素名称 = None
    GZW_市政管线要素名称 = None
    GZW_微波通道要素名称 = None
    GZW_高度分区要素名称 = None
    GZW_共用通道要素名称 = None
    GZW_远景道路要素名称 = None
    GZW_虚位控制河道要素名称 = "GZW_虚位控制河道"
    GZW_虚位控制道路要素名称 = "GZW_虚位控制道路"
    GZW_绿化控制线要素名称 = "GZW_绿化控制线"
    GZW_景观廊道要素名称 = None
    GZW_其他要素名称 = None

    # 控制线
    KZX_永久基本农田要素名称 = "KZX_永久基本农田"
    KZX_生态保护红线要素名称 = None
    KZX_城镇集建区要素名称 = "KZX_城镇集建区"
    KZX_城镇弹性区要素名称 = "KZX_城镇弹性区"
    KZX_城镇开发边界要素名称 = "KZX_城镇开发边界"
    KZX_村庄建设边界要素名称 = "KZX_村庄建设边界"

    # 图则
    TZ_后退界线多层要素名称 = "TZ_后退界线多层"
    TZ_后退界线高层要素名称 = "TZ_后退界线高层"
    TZ_禁止开口线要素名称 = "TZ_禁止开口线"
    TZ_机动车出入口要素名称 = "TZ_机动车出入口"
    TZ_景观廊道要素名称 = "TZ_景观廊道"
    TZ_重要界面要素名称 = "TZ_重要界面"
    TZ_连通道要素名称 = "TZ_连通道"
    TZ_其他图则线要素名称 = "TZ_其他图则线"
    TZ_高度分区要素名称 = "TZ_高度分区"
    TZ_开敞空间要素名称 = "TZ_开敞空间"
    TZ_地下空间要素名称 = "TZ_地下空间"
    TZ_其他图则面要素名称 = "TZ_其他图则面"
    TZ_地标建筑要素名称 = "TZ_地标建筑"
    TZ_重要视点要素名称 = "TZ_重要视点"
    TZ_其他图则点要素名称 = "TZ_其他图则点"


class 区域要素字段映射:
    区域编号字段名称 = "区域编号"
    区域名称字段名称 = "区域名称"
    # 区域类型字段名称: Literal["街区", "街坊", "分村", "工业片区"] = "街坊"
    区域类型字段名称 = "区域类型"
    总工业用地面积字段名称 = "总工业用地面积"
    总耕地用地面积字段名称 = "总耕地用地面积"
    总永久基本农田用地面积字段名称 = "总耕地保有量"
    总永久基本农田用地面积字段名称 = "总永久基本农田用地面积"
    总生态保护红线用地面积字段名称 = "总生态保护红线用地面积"
    总村庄建设边界用地面积字段名称 = "总村庄建设边界用地面积"
    总城乡建设用地面积字段名称 = "总城乡建设用地面积"
    总村庄建设用地面积字段名称 = "总村庄建设用地面积"
    总城镇居住人数字段名称 = "总城镇居住人数"
    总村庄户籍人数字段名称 = "总村庄户籍人数"
    总村庄居住人数字段名称 = "总村庄居住人数"
    总建筑面积字段名称 = "总建筑面积"
    总住宅建筑面积字段名称 = "总住宅建筑面积"
    总工业建筑面积字段名称 = "总工业建筑面积"
    总商服建筑面积字段名称 = "总商服建筑面积"
    区域主导属性字段名称 = "区域主导属性"
    配套设施汇总字段名称 = "配套设施汇总"
    交通设施汇总字段名称 = "交通设施汇总"
    市政设施汇总字段名称 = "市政设施汇总"
    其他设施汇总字段名称 = "其他设施汇总"
    备注字段名称 = "备注"


class 控制线要素字段映射:
    控制线名称字段名称 = "控制线名称"
    控制线类型字段名称 = "控制线类型"
    控制线开发动态字段名称 = "控制线开发动态"
    控制线备注字段名称 = "控制线备注"


class 地块要素字段映射:
    地块编号字段名称 = "地块编号"
    地类编号字段名称 = "地类编号"  # 即：070102等数字形式的性质
    性质名称字段名称 = "性质名称"  # 即：二类城镇住宅用地等文字形式的性质
    地块性质别称字段名称 = "地块性质别称"  # 即：R2等代码形式的性质
    主地类编号字段名称 = "主地类编号"  # 即：070102等数字形式的性质
    兼容比例字段名称 = "兼容比例"
    容积率字段名称 = "容积率"
    绿地率字段名称 = "绿地率"
    开口方位字段名称 = "开口方位"
    耕地保有量字段名称 = "耕地保有量"
    建筑密度字段名称 = "建筑密度"
    建筑高度字段名称 = "建筑限高"
    限高类型字段名称 = "限高类型"
    配套设施字段名称 = "配套设施"
    配套设施代码字段名称 = "配套设施代码"
    配套设施规模字段名称 = "配套设施规模"
    配套设施规模1字段名称 = "配套设施规模1"
    配套设施规模2字段名称 = "配套设施规模2"
    配套设施规模3字段名称 = "配套设施规模3"
    城市设计刚性要求字段名称 = "城市设计刚性要求"
    城市设计弹性要求字段名称 = "城市设计弹性要求"
    开发动态字段名称 = "开发动态"
    土地码字段名称 = "土地码"
    用地大类字段名称 = "用地构成"
    选择用地字段名称 = "选择用地"
    备注字段名称 = "备注说明"
    所属街区字段名称 = "所属街区"
    所属街坊字段名称 = "所属街坊"
    所属分村字段名称 = "所属分村"
    所属工业片区字段名称 = "所属工业片区"
    所属单元字段名称 = "所属单元"
    户籍人数字段名称 = "户籍人数"
    配套设施规模字段名称 = "配套设施规模"
    面积字段名称 = "面积"
    面积公顷字段名称 = "面积公顷"
    限高类型字段名称 = "限高类型"
    用地权属字段名称 = "用地权属"


class 开发动态状态_枚举:
    开发边界内保留 = "保留"
    开发边界外保留 = "保留"
    开发边界内改造 = "改/扩建"
    开发边界外改造 = "盘活"
    开发边界内新建 = "新建"
    开发边界外新建 = "新增"
    # 开发边界内保留 = "保留"
    # 开发边界外保留 = "保留"
    # 开发边界内改造 = "改造"
    # 开发边界外改造 = "改造"
    # 开发边界内新建 = "新建"
    # 开发边界外新建 = "新建"


class 地块编号部件正则_枚举:
    单元序号正则 = r"^[A-Za-z]{2}-\d{2}"
    街区序号正则 = r"(?<=-\d{2}-)\d{2}(?=-)"
    街坊序号正则 = r""
    分村序号正则 = r""
    地块序号正则 = r"-([0-9]+)$"
    地块编号格式 = r"{所属街坊}-{地块序号:02}"
    地块编号格式_开发边界内非建设用地 = r"{所属单元}-{所属街区}-{地块序号}"
    地块编号格式_开发边界外非建设用地 = r"{所属单元}-{地块序号}"
    地块编号格式_城镇道路 = r"{所属单元}-{所属街区}-CZ"
    地块编号格式_村庄道路 = r"{所属单元}-{所属街区}-XC"


class 设施要素字段映射:
    句柄字段名称 = "句柄"
    实体GUID字段名称 = "实体GUID"
    实体ID字段名称 = "实体ID"
    实体类型字段名称 = "实体类型"
    所属工业片区字段名称 = "所属工业片区"
    所属单元字段名称 = "所属单元"
    所属街区字段名称 = "设施所在街区"
    所属街坊字段名称 = "设施所在街坊"
    所属分村字段名称 = "设施所在分村"
    类别代码字段名称 = "类别代码"
    远期预留字段名称 = "远期预留"
    开发动态字段名称 = "开发动态"
    设施名称字段名称 = "设施名称"
    设施代码字段名称 = "设施代码"
    设施数量字段名称 = "设施数量"
    设施规模字段名称 = "设施规模"
    设施类型字段名称 = "设施类型"
    设施级别字段名称 = "设施级别"
    设施所在地块编号字段名称 = "设施所在地块编号"
    位置精确度字段名称 = "位置精确度"
    设施坐标字段名称 = "设施坐标"
    控制方式字段名称 = "控制方式"
    设置形式字段名称 = "设置形式"
    设置形式指定字段名称 = "设置形式指定"
    位置精确度字段名称 = "位置精确度"
    位置精确度指定字段名称 = "位置精确度指定"
    设施图标坐标字段名称 = "设施图标坐标"
    设施坐标字段名称 = "设施坐标"
    设施坐标锁定字段名称 = "设施坐标锁定"
    备注说明字段名称 = "备注说明"
    开发动态字段名称 = "开发动态"
    开发动态锁定字段名称 = "开发动态锁定"
    缩放比例字段名称 = "缩放比例"


class 分区要素字段映射:
    分区名称字段名称 = "分区名称"
    分区编号字段名称 = "分区编号"
    分区编码字段名称 = "分区编码"
    分区要求字段名称 = "分区要求"
    备注说明字段名称 = "备注说明"


if __name__ == "__main__":
    字符串 = 地块编号部件正则_枚举.地块编号格式

    print("".format(单元编号="1", 街区编号="2", 地块序号="3", 测试="54"))
