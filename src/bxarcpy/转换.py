from .拓扑类 import 拓扑类
from .要素类 import 要素类
from .要素数据集类 import 要素数据集类
from .布局类 import 布局类


class 转换:
    @staticmethod
    def 拓扑导出到要素(拓扑对象: 拓扑类, 输出要素名称="AA_拓扑导出后要素"):
        return 拓扑对象.导出到要素(输出要素名称)

    @staticmethod
    def 要素导出到CAD(要素对象: 要素类, 输出路径):
        return 要素对象.导出到CAD(输出路径)

    @staticmethod
    def 要素导出到要素(要素对象: 要素类, 输出目录=None, 输出文件名=None):
        return 要素对象.导出到要素(输出目录, 输出文件名)

    @staticmethod
    def 要素数据集导入从CAD(CAD路径列表, 输出要素数据集名称):
        return 要素数据集类.导入从CAD(CAD路径列表, 输出要素数据集名称)

    @staticmethod
    def 布局导出到PDF(布局对象: 布局类, PDF路径):
        return 布局对象.导出到PDF(PDF路径)
