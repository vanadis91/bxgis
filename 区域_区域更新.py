# -*- coding: utf-8 -*-

import bxarcpy
from typing import Union, Literal
from 用地_用地更新_010所属区域 import 用地创建_通过计算所属区域 as 计算用地所属区域
from 设施_设施更新_020所属区域 import 设施创建_通过计算所属区域 as 计算设施所属区域


def 区域更新(区域要素名称, 地块要素名称="DIST_用地规划图", 地块要素中所属区域字段名称="所属街区", 区域要素中编号字段名称="区域编号", 永久基本农田要素名称="KZX_基本农田", 生态保护红线要素名称="KZX_生态保护红线", 村庄建设边界要素名称="KZX_村庄建设边界", 设施要素名称="SS_配套设施", 设施要素中所属区域字段名称="所属街区"):
    区域要素 = bxarcpy.要素类.要素读取_通过名称(区域要素名称).要素创建_通过复制()
    地块要素 = bxarcpy.要素类.要素读取_通过名称(地块要素名称).要素创建_通过复制()
    设施要素 = bxarcpy.要素类.要素读取_通过名称(设施要素名称).要素创建_通过复制()

    地块要素 = 计算用地所属区域(地块要素.名称, 区域要素.名称, [[地块要素中所属区域字段名称, 区域要素中编号字段名称]], "分割输入要素")
    设施要素 = 计算设施所属区域(设施要素.名称, 区域要素.名称, [[设施要素中所属区域字段名称, 区域要素中编号字段名称]])

    from bxpy import 字典, 字, 转浮

    统计数据 = {}
    需操作的字段名称列表 = ["地类编号", 地块要素中所属区域字段名称, "居住人数", "Shape_Area", "绿地面积指定", "地块建筑面积", "住宅建筑面积", "公服建筑面积", "商服建筑面积", "工业建筑面积", "用地构成"]
    with bxarcpy.游标类.游标创建_通过名称("查找", 地块要素.名称, 需操作的字段名称列表) as 游标:
        for x in 游标:
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总居住人数"], 0)
            统计数据[x[地块要素中所属区域字段名称]]["总居住人数"] += 转浮(x["居住人数"])
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总城镇居住人数"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总村庄居住人数"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总村庄户籍人数"], 0)

            if x["用地构成"] in ["城镇建设用地"]:
                统计数据[x[地块要素中所属区域字段名称]]["总城镇居住人数"] += 转浮(x["居住人数"])
            elif x["用地构成"] in ["村庄建设用地"]:
                统计数据[x[地块要素中所属区域字段名称]]["总村庄居住人数"] += 转浮(x["居住人数"])
            统计数据[x[地块要素中所属区域字段名称]]["总村庄户籍人数"] += 转浮(x["户籍人数"])

            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总填色面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总建设用地"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总非建设用地"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总城乡建设用地面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总村庄建设用地面积"], 0)

            统计数据[x[地块要素中所属区域字段名称]]["总填色面积"] += 转浮(x["Shape_Area"])
            if x["用地构成"] in ["城镇建设用地", "村庄建设用地", "其他建设用地", "区域基础设施用地"]:
                统计数据[x[地块要素中所属区域字段名称]]["总建设用地"] += 转浮(x["Shape_Area"])
            elif x["用地构成"] in ["林草地", "农业设施建设用地", "农园地", "其他土地", "水域"]:
                统计数据[x[地块要素中所属区域字段名称]]["总非建设用地"] += 转浮(x["Shape_Area"])
            elif x["用地构成"] in ["城镇建设用地", "村庄建设用地"]:
                统计数据[x[地块要素中所属区域字段名称]]["总城乡建设用地面积"] += 转浮(x["Shape_Area"])
            elif x["用地构成"] in ["村庄建设用地"]:
                统计数据[x[地块要素中所属区域字段名称]]["总村庄建设用地面积"] += 转浮(x["Shape_Area"])

            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总工业用地面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总绿地用地面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总公园绿地用地面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总公园绿地用地面积_扣除配套"], 0)

            if 字.匹配正则(x["地类编号"], "^1001.*"):
                统计数据[x[地块要素中所属区域字段名称]]["总工业用地面积"] += 转浮(x["Shape_Area"])
            elif 字.匹配正则(x["地类编号"], "^(1401|1402|1403).*"):
                统计数据[x[地块要素中所属区域字段名称]]["总绿地用地面积"] += 转浮(x["Shape_Area"])
            if 字.匹配正则(x["地类编号"], ".*(1401).*"):
                统计数据[x[地块要素中所属区域字段名称]]["总公园绿地用地面积"] += 转浮(x["Shape_Area"])
                统计数据[x[地块要素中所属区域字段名称]]["总公园绿地用地面积_扣除配套"] += 转浮(x["绿地面积指定"])

            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总耕地用地面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总林地用地面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总河流水面用地面积"], 0)

            if 字.匹配正则(x["地类编号"], "^01.*"):
                统计数据[x[地块要素中所属区域字段名称]]["总耕地用地面积"] += 转浮(x["Shape_Area"])
            elif 字.匹配正则(x["地类编号"], "^03.*"):
                统计数据[x[地块要素中所属区域字段名称]]["总林地用地面积"] += 转浮(x["Shape_Area"])
            elif 字.匹配正则(x["地类编号"], "^1701.*"):
                统计数据[x[地块要素中所属区域字段名称]]["总河流水面用地面积"] += 转浮(x["Shape_Area"])

            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总建筑面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总住宅建筑面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总公服建筑面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总商服建筑面积"], 0)
            字典.默认值设置(统计数据, [x[地块要素中所属区域字段名称], "总工业建筑面积"], 0)

            统计数据[x[地块要素中所属区域字段名称]]["总建筑面积"] += 转浮(x["地块建筑面积"])
            统计数据[x[地块要素中所属区域字段名称]]["总住宅建筑面积"] += 转浮(x["住宅建筑面积"])
            统计数据[x[地块要素中所属区域字段名称]]["总公服建筑面积"] += 转浮(x["公服建筑面积"])
            统计数据[x[地块要素中所属区域字段名称]]["总商服建筑面积"] += 转浮(x["商服建筑面积"])
            统计数据[x[地块要素中所属区域字段名称]]["总工业建筑面积"] += 转浮(x["工业建筑面积"])

    # 永久基本农田统计
    永久基本农田要素 = bxarcpy.要素类.要素读取_通过名称(永久基本农田要素名称).要素创建_通过复制()
    区域要素拷贝 = 区域要素.要素创建_通过复制()
    区域和永久基本农田相交后 = 区域要素拷贝.要素创建_通过相交([永久基本农田要素.名称])
    with bxarcpy.游标类.游标创建_通过名称("查找", 区域和永久基本农田相交后.名称, [区域要素中编号字段名称, "Shape_Area"]) as 游标:
        from bxpy import 字, 字典, 转浮

        for x in 游标:
            字典.默认值设置(统计数据, [x[区域要素中编号字段名称], "总永久基本农田用地面积"], 0)
            统计数据[x[区域要素中编号字段名称]]["总永久基本农田用地面积"] += 转浮(x["Shape_Area"])

    # 生态保护红线统计
    生态保护红线要素 = bxarcpy.要素类.要素读取_通过名称(生态保护红线要素名称).要素创建_通过复制()
    区域要素拷贝 = 区域要素.要素创建_通过复制()
    区域和生态保护红线相交后 = 区域要素拷贝.要素创建_通过相交([生态保护红线要素.名称])
    with bxarcpy.游标类.游标创建_通过名称("查找", 区域和生态保护红线相交后.名称, [区域要素中编号字段名称, "Shape_Area"]) as 游标:
        from bxpy import 字, 字典, 转浮

        for x in 游标:
            字典.默认值设置(统计数据, [x[区域要素中编号字段名称], "总生态保护红线用地面积"], 0)
            统计数据[x[区域要素中编号字段名称]]["总生态保护红线用地面积"] += 转浮(x["Shape_Area"])

    # 村庄建设边界统计
    村庄建设边界要素 = bxarcpy.要素类.要素读取_通过名称(村庄建设边界要素名称).要素创建_通过复制()
    区域要素拷贝 = 区域要素.要素创建_通过复制()
    区域和村庄建设边界相交后 = 区域要素拷贝.要素创建_通过相交([村庄建设边界要素.名称])
    with bxarcpy.游标类.游标创建_通过名称("查找", 区域和村庄建设边界相交后.名称, [区域要素中编号字段名称, "Shape_Area"]) as 游标:
        from bxpy import 字, 字典, 转浮

        for x in 游标:
            字典.默认值设置(统计数据, [x[区域要素中编号字段名称], "总村庄建设边界用地面积"], 0)
            统计数据[x[区域要素中编号字段名称]]["总村庄建设边界用地面积"] += 转浮(x["Shape_Area"])

    # 计算设施相关的内容
    需操作的字段名称列表 = ["设施类型", "设施名称", "设施数量", "设施规模", 设施要素中所属区域字段名称]
    with bxarcpy.游标类.游标创建_通过名称("查找", 设施要素.名称, 需操作的字段名称列表) as 游标:
        from bxpy import 转浮, 字典

        for x in 游标:
            if x[设施要素中所属区域字段名称] not in ["", None]:
                字典.默认值设置(统计数据, [x[设施要素中所属区域字段名称]], {})
                if x["设施类型"] in ["教育", "商服", "社会福利", "社区治理", "生态环境", "体育", "文化", "医疗"]:
                    设施大类名称 = "配套设施汇总"
                elif x["设施类型"] in ["市政交通"]:
                    设施大类名称 = "交通设施汇总"
                elif x["设施类型"] in ["市政防灾", "市政公用", "市政环卫", "市政人防", "市政消防"]:
                    设施大类名称 = "市政设施汇总"
                else:
                    设施大类名称 = "其他设施汇总"

                字典.默认值设置(统计数据, [x[设施要素中所属区域字段名称], 设施大类名称], {})
                if x["设施名称"] not in 统计数据[x[设施要素中所属区域字段名称]][设施大类名称]:
                    统计数据[x[设施要素中所属区域字段名称]][设施大类名称][x["设施名称"]] = [转浮(x["设施数量"]), x["设施规模"]]
                else:
                    统计数据[x[设施要素中所属区域字段名称]][设施大类名称][x["设施名称"]][0] += 转浮(x["设施数量"])
                    if x["设施规模"] not in ["", " ", None] and 统计数据[x[设施要素中所属区域字段名称]][设施大类名称][x["设施名称"]][1] not in ["", " ", None]:
                        统计数据[x[设施要素中所属区域字段名称]][设施大类名称][x["设施名称"]][1] += "、" + x["设施规模"]
                    elif x["设施规模"] not in ["", " ", None] and 统计数据[x[设施要素中所属区域字段名称]][设施大类名称][x["设施名称"]][1] in ["", " ", None]:
                        统计数据[x[设施要素中所属区域字段名称]][设施大类名称][x["设施名称"]][1] += x["设施规模"]

    # 开始正式赋值区域要素
    区域要素.字段添加("区域名称", 删除既有字段=False).字段添加("区域主导属性", 删除既有字段=False)
    区域要素.字段添加("配套设施汇总弹性", 删除既有字段=False).字段添加("交通设施汇总弹性", 删除既有字段=False).字段添加("市政设施汇总弹性", 删除既有字段=False).字段添加("其他设施汇总弹性", 删除既有字段=False)
    区域要素.字段添加("总居住人数").字段添加("总城镇居住人数").字段添加("总村庄居住人数").字段添加("总村庄户籍人数")
    区域要素.字段添加("总填色面积").字段添加("总建设用地").字段添加("总城乡建设用地面积").字段添加("总村庄建设用地面积")
    区域要素.字段添加("总工业用地面积").字段添加("总绿地用地面积").字段添加("总公园绿地用地面积").字段添加("总公园绿地用地面积_扣除配套")
    区域要素.字段添加("总非建设用地").字段添加("总耕地用地面积").字段添加("总林地用地面积").字段添加("总河流水面用地面积")
    区域要素.字段添加("总建筑面积").字段添加("总住宅建筑面积").字段添加("总公服建筑面积").字段添加("总商服建筑面积").字段添加("总工业建筑面积")
    区域要素.字段添加("总永久基本农田用地面积").字段添加("总生态保护红线用地面积").字段添加("总村庄建设边界用地面积")
    区域要素.字段添加("允许提高幅度").字段添加("备注")
    区域要素.字段添加("配套设施汇总1", 字段长度=255).字段添加("配套设施汇总2", 字段长度=255).字段添加("配套设施汇总3", 字段长度=255)
    区域要素.字段添加("交通设施汇总1", 字段长度=255).字段添加("交通设施汇总2", 字段长度=255).字段添加("交通设施汇总3", 字段长度=255)
    区域要素.字段添加("市政设施汇总1", 字段长度=255).字段添加("市政设施汇总2", 字段长度=255).字段添加("市政设施汇总3", 字段长度=255)
    区域要素.字段添加("其他设施汇总1", 字段长度=255).字段添加("其他设施汇总2", 字段长度=255).字段添加("其他设施汇总3", 字段长度=255)

    需操作的字段名称列表 = [区域要素中编号字段名称, "总居住人数", "总城镇居住人数", "总村庄居住人数", "总村庄户籍人数", "总填色面积", "总建设用地", "总城乡建设用地面积", "总村庄建设用地面积", "总工业用地面积", "总绿地用地面积", "总公园绿地用地面积", "总公园绿地用地面积_扣除配套", "总非建设用地", "总耕地用地面积", "总林地用地面积", "总河流水面用地面积", "总建筑面积", "总住宅建筑面积", "总公服建筑面积", "总商服建筑面积", "总工业建筑面积", "总永久基本农田用地面积", "总生态保护红线用地面积", "总村庄建设边界用地面积", "允许提高幅度", "备注", "配套设施汇总1", "配套设施汇总2", "配套设施汇总3", "配套设施汇总弹性", "交通设施汇总1", "交通设施汇总2", "交通设施汇总3", "交通设施汇总弹性", "市政设施汇总1", "市政设施汇总2", "市政设施汇总3", "市政设施汇总弹性", "其他设施汇总1", "其他设施汇总2", "其他设施汇总3", "其他设施汇总弹性"]

    with bxarcpy.游标类.游标创建_通过名称("更新", 区域要素.名称, 需操作的字段名称列表) as 游标:
        from bxpy import 转字

        for x in 游标:
            if x[区域要素中编号字段名称] in 统计数据:
                x["总居住人数"] = 转字(统计数据[x[区域要素中编号字段名称]]["总居住人数"])
                x["总城镇居住人数"] = 转字(统计数据[x[区域要素中编号字段名称]]["总城镇居住人数"])
                x["总村庄居住人数"] = 转字(统计数据[x[区域要素中编号字段名称]]["总村庄居住人数"])
                x["总村庄户籍人数"] = 转字(统计数据[x[区域要素中编号字段名称]]["总村庄户籍人数"])

                x["总填色面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总填色面积"])
                x["总建设用地"] = 转字(统计数据[x[区域要素中编号字段名称]]["总建设用地"])
                x["总城乡建设用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总城乡建设用地面积"])
                x["总村庄建设用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总村庄建设用地面积"])

                x["总工业用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总工业用地面积"])
                x["总绿地用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总绿地用地面积"])
                x["总公园绿地用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总公园绿地用地面积"])
                x["总公园绿地用地面积_扣除配套"] = 转字(统计数据[x[区域要素中编号字段名称]]["总公园绿地用地面积_扣除配套"])

                x["总非建设用地"] = 转字(统计数据[x[区域要素中编号字段名称]]["总非建设用地"])
                x["总耕地用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总耕地用地面积"])
                x["总林地用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总林地用地面积"])
                x["总河流水面用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总河流水面用地面积"])

                x["总建筑面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总建筑面积"])
                x["总住宅建筑面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总住宅建筑面积"])
                x["总公服建筑面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总公服建筑面积"])
                x["总商服建筑面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总商服建筑面积"])
                x["总工业建筑面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总工业建筑面积"])

                x["总永久基本农田用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总永久基本农田用地面积"])
                x["总生态保护红线用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总生态保护红线用地面积"])
                x["总村庄建设边界用地面积"] = 转字(统计数据[x[区域要素中编号字段名称]]["总村庄建设边界用地面积"])
                x["允许提高幅度"] = 转字(5)

                for 设施大类名称 in ["配套设施汇总", "交通设施汇总", "市政设施汇总", "其他设施汇总"]:
                    if 设施大类名称 in 统计数据[x[区域要素中编号字段名称]]:
                        设施汇总字符串 = "刚性管控：配置"
                        for k, v in 统计数据[x[区域要素中编号字段名称]][设施大类名称].items():
                            if v[1] in ["", " ", None]:
                                设施汇总字符串 += k + str(int(v[0])) + "处；"
                            else:
                                设施汇总字符串 += k + str(int(v[0])) + "处，规模分别为" + v[1] + "；"
                        设施汇总字符串 = 设施汇总字符串[0:-1]
                        if x[设施大类名称 + "弹性"] not in ["", " ", None]:
                            设施汇总字符串 += "；弹性引导："
                            设施汇总字符串 += x[设施大类名称 + "弹性"]
                        if len(设施汇总字符串) > 765:
                            x[设施大类名称 + "1"] = 设施汇总字符串[0:255]
                            x[设施大类名称 + "2"] = 设施汇总字符串[255:510]
                            x[设施大类名称 + "3"] = 设施汇总字符串[510:765]
                            from bxarcpy import 环境

                            环境.输出消息(f"{x[区域要素中编号字段名称]} 区域中 {设施大类名称} 字符串长度过长")
                        if len(设施汇总字符串) > 510:
                            x[设施大类名称 + "1"] = 设施汇总字符串[0:255]
                            x[设施大类名称 + "2"] = 设施汇总字符串[255:510]
                            x[设施大类名称 + "3"] = 设施汇总字符串[510:]
                        elif len(设施汇总字符串) > 255:
                            x[设施大类名称 + "1"] = 设施汇总字符串[0:255]
                            x[设施大类名称 + "2"] = 设施汇总字符串[255:]
                        else:
                            x[设施大类名称 + "1"] = 设施汇总字符串

            游标.行更新(x)

    区域要素 = 区域要素.要素创建_通过复制并重命名重名要素(区域要素名称)


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with bxarcpy.环境.环境管理器(工作空间):
        区域更新("JX_街坊范围线", "DIST_用地规划图", "所属街坊", "区域编号", 永久基本农田要素名称="KZX_基本农田", 生态保护红线要素名称="KZX_生态保护红线", 村庄建设边界要素名称="KZX_村庄建设边界", 设施要素名称="SS_配套设施", 设施要素中所属区域字段名称="所属街区")
