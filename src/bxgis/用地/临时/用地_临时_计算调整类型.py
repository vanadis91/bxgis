import bxarcpy
import bxarcpy.工具包 as 工具包
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.数据库包 import 数据库类
from bxarcpy.要素数据集包 import 要素数据集类
from bxarcpy.环境包 import 环境管理器类, 输入输出类
from bxgis.配置 import 基本信息


def 用地_计算调整类型(用地调整要素名称, 输出要素名称="in_memory\\AA_计算调整类型"):
    if 输出要素名称 == "in_memory\\AA_计算调整类型":
        输出要素名称 = 输出要素名称 + "_" + 工具包.生成短GUID()
    输入要素 = 要素类.要素创建_通过复制(用地调整要素名称)
    要素类.字段添加(输入要素, "调整类型")
    要素类.字段添加(输入要素, "调整类型1")
    with 游标类.游标创建("更新", 输入要素, ["地类编号_现状", "地类编号_规划", "地类差异", "调整类型", "调整类型1", "所属三区三线", "开发动态", "Shape_Area", "容积率"]) as 游标:
        from bxpy.基本对象包 import 字类

        开发边界内_未建设空间_住宅 = 0
        开发边界内_未建设空间_工业 = 0
        开发边界内_未建设空间_商服 = 0
        开发边界内_未建设空间_其他 = 0
        开发边界内_未建设空间_道路河道绿地 = 0
        开发边界内_已建设空间_改住宅 = 0
        开发边界内_已建设空间_改工业 = 0
        开发边界内_已建设空间_改商服 = 0
        开发边界内_住宅建筑面积 = 0
        开发边界内_住宅用地面积 = 0
        开发边界内_工业建筑面积 = 0
        开发边界内_工业用地面积 = 0
        开发边界内_商服建筑面积 = 0
        开发边界内_商服用地面积 = 0
        for x in 游标:
            x["调整类型1"] = ""
            if x["所属三区三线"] in ["城镇集中建设区", "城镇弹性发展区"]:
                x["调整类型1"] = x["调整类型1"] + "-开发边界内"
            else:
                x["调整类型1"] = x["调整类型1"] + "-开发边界外"
            if x["地类编号_规划"][0:2] in ["01", "02", "03", "04", "05", "06", "17"] and x["地类编号_规划"][0:6] not in ["060102"]:
                x["调整类型1"] = x["调整类型1"] + "-非建设用地"
            else:
                x["调整类型1"] = x["调整类型1"] + "-建设用地"

            x["调整类型"] = ""
            if x["所属三区三线"] in ["城镇集中建设区", "城镇弹性发展区"]:
                x["调整类型"] = x["调整类型"] + "-开发边界内"
            else:
                x["调整类型"] = x["调整类型"] + "-开发边界外"

            if (((x["地类编号_现状"][0:2] in ["01", "02", "03", "04", "05", "06", "17"] and x["地类编号_现状"][0:6] not in ["060102"]) or x["地类编号_规划"][0:9] in ["120802/07", "120802/08", "120802/14"]) and (x["地类编号_规划"][0:2] in ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16"] or x["地类编号_规划"][0:6] in ["060102"]) and x["开发动态"] not in ["现状已实施", "拟建", "已批未建"]) or x["开发动态"] in ["规划未实施"]:
                x["调整类型"] = x["调整类型"] + "-未建设空间"
            else:
                x["调整类型"] = x["调整类型"] + "-已建设空间"

            if x["地类编号_规划"][0:4] in ["0701", "0702"] or x["地类编号_规划"][0:9] in ["120802/07"]:
                x["调整类型"] = x["调整类型"] + "-住宅"
                if "-开发边界内" in x["调整类型"]:
                    开发边界内_住宅建筑面积 += float(x["容积率"]) * x["Shape_Area"]
                    开发边界内_住宅用地面积 += x["Shape_Area"]
                    if float(x["容积率"]) <= 0:
                        print("有住宅容积率是0")
            elif x["地类编号_规划"][0:4] in ["1001", "1101"]:
                x["调整类型"] = x["调整类型"] + "-工业"
                if "-开发边界内" in x["调整类型"]:
                    开发边界内_工业建筑面积 += float(x["容积率"]) * x["Shape_Area"]
                    开发边界内_工业用地面积 += x["Shape_Area"]
                    if float(x["容积率"]) <= 0:
                        print("有工业容积率是0")
            elif x["地类编号_规划"][0:2] in ["09"]:
                x["调整类型"] = x["调整类型"] + "-商服"
                if "-开发边界内" in x["调整类型"]:
                    开发边界内_商服建筑面积 += float(x["容积率"]) * x["Shape_Area"]
                    开发边界内_商服用地面积 += x["Shape_Area"]
                    if float(x["容积率"]) <= 0:
                        print("有商服容积率是0")
            elif x["地类编号_规划"][0:2] in ["08", "13"] or x["地类编号_规划"] in ["120802", "120802/120803", "120803", "120803v"] or x["地类编号_规划"][0:9] in ["120802/08"]:
                x["调整类型"] = x["调整类型"] + "-公服"
            elif x["地类编号_规划"][0:4] in ["1202", "1207"] or x["地类编号_规划"][0:2] in ["17", "14"] or x["地类编号_规划"][0:6] in ["060102"] or x["地类编号_规划"][0:9] in ["120802/14"]:
                x["调整类型"] = x["调整类型"] + "-道路河道绿地"
            else:
                x["调整类型"] = x["调整类型"] + "-其他"

            if x["地类编号_现状"][0:4] not in ["0701", "0702"] and x["地类编号_现状"][0:9] not in ["120802/07"] and (x["地类编号_规划"][0:4] in ["0701", "0702"] or x["地类编号_规划"][0:9] in ["120802/07"]):
                x["调整类型"] = x["调整类型"] + "-其他用地更新为住宅用地"
            if x["地类编号_现状"][0:2] not in ["09"] and x["地类编号_规划"][0:2] in ["09"]:
                x["调整类型"] = x["调整类型"] + "-其他用地更新为商服用地"
            if x["地类编号_现状"][0:4] in ["1001", "1101"] and x["地类编号_规划"][0:4] in ["1001", "1101"] and x["开发动态"] not in ["现状已实施", "拟建", "已批未建"]:
                x["调整类型"] = x["调整类型"] + "-工业用地更新为工业用地"

            if "-开发边界内" in x["调整类型"] and "-未建设空间" in x["调整类型"] and "-住宅" in x["调整类型"]:
                开发边界内_未建设空间_住宅 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-未建设空间" in x["调整类型"] and "-工业" in x["调整类型"]:
                开发边界内_未建设空间_工业 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-未建设空间" in x["调整类型"] and "-商服" in x["调整类型"]:
                开发边界内_未建设空间_商服 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-未建设空间" in x["调整类型"] and ("-公服" in x["调整类型"] or "-其他" in x["调整类型"]):
                开发边界内_未建设空间_其他 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-未建设空间" in x["调整类型"] and "-道路河道绿地" in x["调整类型"]:
                开发边界内_未建设空间_道路河道绿地 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-已建设空间" in x["调整类型"] and "-其他用地更新为住宅用地" in x["调整类型"]:
                开发边界内_已建设空间_改住宅 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-已建设空间" in x["调整类型"] and "-工业用地更新为工业用地" in x["调整类型"]:
                开发边界内_已建设空间_改工业 += x["Shape_Area"]
            if "-开发边界内" in x["调整类型"] and "-已建设空间" in x["调整类型"] and "-其他用地更新为商服用地" in x["调整类型"]:
                开发边界内_已建设空间_改商服 += x["Shape_Area"]

            游标.行更新(x)
    print(f"开发边界内_未建设空间_住宅：{开发边界内_未建设空间_住宅}")
    print(f"开发边界内_未建设空间_工业：{开发边界内_未建设空间_工业}")
    print(f"开发边界内_未建设空间_商服：{开发边界内_未建设空间_商服}")
    print(f"开发边界内_未建设空间_其他：{开发边界内_未建设空间_其他}")
    print(f"开发边界内_未建设空间_道路河道绿地：{开发边界内_未建设空间_道路河道绿地}")
    print(f"开发边界内_已建设空间_改住宅：{开发边界内_已建设空间_改住宅}")
    print(f"开发边界内_已建设空间_改工业：{开发边界内_已建设空间_改工业}")
    print(f"开发边界内_已建设空间_改商服：{开发边界内_已建设空间_改商服}")
    print(f"开发边界内_住宅平均容积率：{开发边界内_住宅建筑面积/开发边界内_住宅用地面积}")
    print(f"开发边界内_工业平均容积率：{开发边界内_工业建筑面积/开发边界内_工业用地面积}")
    print(f"开发边界内_商服平均容积率：{开发边界内_商服建筑面积/开发边界内_商服用地面积}")
    输出要素 = 要素类.要素创建_通过复制并重命名重名要素(输入要素, 输出要素名称)
    return 输出要素


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        用地_计算调整类型("DIST_用地调整图", "DIST_用地调整图")
