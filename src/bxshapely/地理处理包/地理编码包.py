from typing import Union, Literal, Any
from bxpy.网络会话包 import 会话类
from bxpy.时间包 import 时间类
from bxpy.基本对象包 import 表类
from bxpy.进度条包 import 进度条类
from bxpandas.数据框架包 import 数据框架类
from bxshapely.地理处理包.坐标系转换包 import 加密坐标系转换工具


def 经纬度获取_根据地址(
    地址列表=["上城区见仁里17号"],
    输出格式: Literal["json", "xml"] = "json",
    所在城市="杭州市",
    输出结果采用的坐标系: Literal["gcj02", "bd09mc", "bd09ll"] = "bd09ll",
):
    密钥 = "0giDJ7mmGCmNFiq70cYVHOWe3qyGUsuw"
    网址 = "https://api.map.baidu.com/geocoding/v3"
    地址列表按29个一组修改后列表 = 表类.表分隔成子表(地址列表, 29)
    ret = []
    for 地址列表 in 进度条类.进度条创建(地址列表按29个一组修改后列表, 前置信息="大组进度", 位置固定=0):
        时间类.等待(1)
        for 地址 in 进度条类.进度条创建(地址列表, 前置信息="小组进度", 位置固定=1, 进度条结束后保留=False):
            数据 = {
                "address": 地址,
                "output": 输出格式,
                "ak": 密钥,
                "city": 所在城市,
                "ret_coordtype": 输出结果采用的坐标系,
            }
            响应 = 会话类.会话创建(网址=网址, 数据_args=数据)
            if 响应:
                返回值 = 会话类.响应类.属性获取_内容_json(响应)
                if 返回值["status"] != 0:
                    返回值格式化后 = {
                        "经度": 0,
                        "纬度": 0,
                        "是否准确打点": 0,
                        "地图自身打点精度": "大于10000m",
                        "地址与打点相关性": "50-",
                        "地址类型": "UNKNOWN",
                    }
                    ret.append(返回值格式化后)
                if 返回值["status"] == 0:
                    if 输出结果采用的坐标系 == "bd09ll":
                        百度经度 = 返回值["result"]["location"]["lng"]
                        百度纬度 = 返回值["result"]["location"]["lat"]
                        经度, 纬度 = 加密坐标系转换工具().BD09_to_WGS84(百度经度, 百度纬度)
                    else:
                        经度 = 返回值["result"]["location"]["lng"]
                        纬度 = 返回值["result"]["location"]["lat"]
                    返回值格式化后 = {
                        "经度": 经度,
                        "纬度": 纬度,
                        "是否准确打点": 返回值["result"]["precise"],
                        "地图自身打点精度": 打点精度转换(返回值["result"]["confidence"]),
                        "地址与打点相关性": 打点相关性转换(返回值["result"]["comprehension"]),
                        "地址类型": 返回值["result"]["level"],
                    }
                    ret.append(返回值格式化后)
    数据框架 = 数据框架类.数据框架创建_通过字典列表(ret)
    数据框架类.转换_到excel文件(数据框架, r"C:\Users\beixiao\Desktop\经纬度.xlsx")


def 打点精度转换(误差):
    误差 = float(误差)
    if 误差 >= 100:
        return "小于20m"
    elif 误差 >= 90:
        return "小于50m"
    elif 误差 >= 80:
        return "小于100m"
    elif 误差 >= 75:
        return "小于200m"
    elif 误差 >= 70:
        return "小于300m"
    elif 误差 >= 60:
        return "小于500m"
    elif 误差 >= 50:
        return "小于1000m"
    elif 误差 >= 40:
        return "小于2000m"
    elif 误差 >= 30:
        return "小于5000m"
    elif 误差 >= 25:
        return "小于8000m"
    elif 误差 >= 20:
        return "小于10000m"
    else:
        return "大于10000m"


def 打点相关性转换(相关性):
    相关性 = float(相关性)
    if 相关性 >= 100:
        return "100，误差100m内概率91%，误差500m内概率96%"
    elif 相关性 >= 90:
        return "90+，误差100m内概率89%，误差500m内概率96%"
    elif 相关性 >= 80:
        return "80+，误差100m内概率为88%，误差500m内概率为95%"
    elif 相关性 >= 70:
        return "70+，误差100m内概率为84%，误差500m内概率为93%"
    elif 相关性 >= 60:
        return "60+，误差100m内概率为81%，误差500m内概率为91%"
    elif 相关性 >= 50:
        return "50+，误差100m内概率为79%，误差500m内概率为90%"
    else:
        return "50-"


def 地址列表获取(excel文件路径=r"C:\Users\beixiao\Desktop\test.xlsx"):
    数据框架 = 数据框架类.转换_从excel文件(excel文件路径, 要读取的列=["序号", "详细地址"])
    数据 = 数据框架类.转换_到字典(数据框架)
    return [x["详细地址"] for x in 数据]


if __name__ == "__main__":
    地址列表 = 地址列表获取()
    经纬度获取_根据地址(地址列表)
