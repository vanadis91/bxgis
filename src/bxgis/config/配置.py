from typing import Union, Literal


class 计算机信息:
    CAD输出目录 = r"C:\Users\beixiao\Desktop"


class 项目信息:
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    单元名称 = "临江单元"
    单元类型: Literal["城镇单元", "乡村单元"] = "城镇单元"
    单元编号 = "QT12"
    批复时间 = "2023/12/18"
    批复文号 = "杭政函〔2023〕109号"
    编制单位 = "浙江大学建筑设计研究院有限公司"
    单元功能 = "以打造中国先进制造业的重要窗口为使命，以新材料产业为主导，生物医药和装备制造产业为特色，融高端智造、产业服务、现代物流于一体的一流示范产业园区。"
    人口规模 = "3.1809"
    跨单元平衡情况 = ""
    CZ_三调筛选_扣除地类系数 = "CZ_三调筛选_扣除地类系数"
    JX_规划范围线要素名称 = "JX_规划范围线"
    JX_工业片区范围线要素名称 = "JX_工业片区范围线"
    JX_街区范围线要素名称 = "JX_街区范围线"
    JX_街坊范围线要素名称 = "JX_街坊范围线"
    JX_分村范围线要素名称 = "JX_分村范围线"
    YD_用地_规划要素名称 = "DIST_用地规划图"
    YD_用地_现状要素名称 = "DIST_用地现状图"
    TY_用途分区_规划要素名称 = "DIST_用途分区图"
    SS_配套设施_规划要素名称 = "SS_配套设施"
    DL_道路中线要素名称 = "DL_道路中线"
    DL_道路边线要素名称 = "DL_道路边线"
    DL_河道中线要素名称 = "DL_河道中线"
    DL_河道边线要素名称 = "DL_河道边线"
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
    KZX_永久基本农田要素名称 = "KZX_永久基本农田"
    KZX_城镇集建区要素名称 = "KZX_城镇集建区"
    KZX_城镇弹性区要素名称 = "KZX_城镇弹性区"
    KZX_村庄建设边界要素名称 = "KZX_村庄建设边界"


class 区域要素字段映射:
    区域编号字段名称 = "区域编号"
    区域名称字段名称 = "区域名称"
    区域类型字段名称: Literal["街区", "街坊", "分村", "工业片区"] = "街坊"
    总工业用地面积字段名称 = "总工业用地面积"
    总耕地用地面积字段名称 = "总耕地用地面积"
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


class 控制线要素字段映射:
    控制线名称字段名称 = "控制线名称"


class 地块要素字段映射:
    地块编号字段名称 = "地块编号"
    地类编号字段名称 = "地类编号"  # 即：070102等数字形式的性质
    性质名称字段名称 = "性质名称"  # 即：二类城镇住宅用地等文字形式的性质
    地块性质别称字段名称 = "地块性质别称"  # 即：R2等代码形式的性质
    兼容比例字段名称 = "兼容比例"
    容积率字段名称 = "容积率"
    绿地率字段名称 = "绿地率"
    耕地保有量字段名称 = "耕地保有量"
    建筑密度字段名称 = "建筑密度"
    建筑高度字段名称 = "建筑限高"
    限高类型字段名称 = "限高类型"
    配套设施规模字段名称 = "配套设施规模"
    城市设计刚性要求字段名称 = "城市设计刚性要求"
    城市设计弹性要求字段名称 = "城市设计弹性要求"
    开发动态字段名称 = "开发动态"
    土地码字段名称 = "土地码"
    用地大类字段名称 = "用地构成"
    选择用地字段名称 = "选择用地"
    备注字段名称 = "备注"
    所属街区字段名称 = "所属街区"
    所属街坊字段名称 = "所属街坊"
    所属分村字段名称 = "所属分村"
    配套设施规模字段名称 = "配套设施规模"


class 设施要素字段映射:
    所属工业片区字段名称 = "所属工业片区"
    类别代码字段名称 = "类别代码"
    远期预留字段名称 = "远期预留"
    开发动态字段名称 = "开发动态"
    设施名称字段名称 = "设施名称"
    设施代码字段名称 = "设施代码"
    设施规模字段名称 = "设施规模"
    设施级别字段名称 = "设施级别"
    设施所在地块编号字段名称 = "设施所在地块编号"
    位置精确度字段名称 = "位置精确度"
    设施坐标字段名称 = "设施坐标"
    备注说明字段名称 = "备注说明"

class 分区要素字段映射:
    分区名称字段名称 = '分区名称'
    分区编号字段名称 = '分区编号'
    
