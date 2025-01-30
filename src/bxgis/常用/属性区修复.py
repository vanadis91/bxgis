# *-* coding:utf8 *-*
import bxarcpy
from bxarcpy.要素包 import 要素类
from bxarcpy.游标包 import 游标类
from bxarcpy.几何包 import 几何类
from bxarcpy.环境包 import 输入输出类, 环境管理器类
from bxarcpy.工具包 import 临时路径生成


def 属性域修复(输入要素路径列表=["YD_基期初转换"], 输出要素路径列表=["内存临时"]):
    for i, 输入要素路径x in enumerate(输入要素路径列表):
        输入要素 = 要素类.要素创建_通过复制(输入要素路径x)
        输出要素路径 = 临时路径生成([输入要素路径x]) if 输出要素路径列表[i] == "内存临时" else 输出要素路径列表[i]
        输出要素 = 要素类.要素创建_通过属性域修复(输入要素)
        要素类.要素创建_通过复制并重命名重名要素(输出要素, 输出要素路径)


if __name__ == "__main__":
    # 工作空间 = r"C:\Users\common\project\F富阳受降控规\受降北_数据库.gdb"
    工作空间 = r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"
    # 工作空间 = r"C:\Users\beixiao\Project\F富阳受降控规\0.资料\7.流程_24.06.13_质检\富阳区受降北单元入库数据.gdb"
    # 工作空间 = r"C:\Users\common\Project\D德清洛舍杨树湾单元控规\03过程文件\24.11.27报批稿\D德清洛舍杨树湾单元控规_数据库.gdb"
    with 环境管理器类.环境管理器类创建(工作空间):
        属性域修复(输入要素路径列表=["CZ_审批信息_农转用"], 输出要素路径列表=["CZ_审批信息_农转用1"])
