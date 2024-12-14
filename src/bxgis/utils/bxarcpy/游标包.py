# *-* coding:utf8 *-*
from bxpy.日志包 import 日志生成器
import arcpy
from typing import Union, Literal, Any
from collections import OrderedDict

枚举_特殊字段 = {
    "_形状": "SHAPE@",
    "_ID": "OID@",
    "_面积": "SHAPE@AREA",
    "_长度": "SHAPE@LENGTH",
    "_质心": "SHAPE@CENTROID",
    "_外接矩形": "SHAPE@EXTENT",
    "_坐标": "SHAPE@XY",
    "_坐标X": "SHAPE@X",
    "_坐标Y": "SHAPE@Y",
    "_坐标Z": "SHAPE@Z",
    "_WKT格式": "SHAPE@WKT",
    "_WKB格式": "SHAPE@WKB",
    "_JSON格式": "SHAPE@JSON",
}


class 游标类:

    # class 行对象类:
    #     def __init__(self, 行数据, 游标对象: "游标类") -> None:
    #         self.数据_字典格式 = {}
    #         self.数据_列表格式 = []
    #         self._内嵌对象_游标对象 = 游标对象
    #         for k, v in zip(游标对象.字段名称列表, 行数据):
    #             if k == "_形状":
    #                 self.数据_列表格式.append(游标类.形状类(v))
    #                 self.数据_字典格式[k] = 游标类.形状类(v)
    #             else:
    #                 self.数据_列表格式.append(v)
    #                 self.数据_字典格式[k] = v
    #         # self.数据_字典格式 = {k: v for k, v in zip(self._内嵌对象_游标对象.字段名称列表, 行数据)}

    #     def 行删除(self):
    #         return self._内嵌对象_游标对象._内嵌对象.deleteRow()

    #     def 行更新_列表格式(self):
    #         用于更新的列表 = []
    #         for k, v in zip(self._内嵌对象_游标对象.字段名称列表, self.数据_列表格式):
    #             if k == "_形状":
    #                 用于更新的列表.append(v._内嵌对象)
    #             else:
    #                 用于更新的列表.append(v)
    #         return self._内嵌对象_游标对象._内嵌对象.updateRow(用于更新的列表)

    #     def 行更新_字典格式(self):
    #         用于更新的列表 = []
    #         for k in self._内嵌对象_游标对象.字段名称列表:
    #             if k == "_形状":
    #                 用于更新的列表.append(self.数据_字典格式[k]._内嵌对象)
    #             else:
    #                 用于更新的列表.append(self.数据_字典格式[k])
    #         return self._内嵌对象_游标对象._内嵌对象.updateRow(用于更新的列表)

    #     def 行插入_列表格式(self):
    #         用于更新的列表 = []
    #         for k, v in zip(self._内嵌对象_游标对象.字段名称列表, self.数据_列表格式):
    #             if k == "_形状":
    #                 用于更新的列表.append(v._内嵌对象)
    #             else:
    #                 用于更新的列表.append(v)
    #         return self._内嵌对象_游标对象._内嵌对象.insertRow(用于更新的列表)

    # class 形状类:
    #     def __init__(self, 内嵌对象) -> None:
    #         # print(f"形状类：{内嵌对象.__class__}")
    #         self._内嵌对象 = 内嵌对象

    #     @property
    #     def 类型(self):
    #         类型 = self._内嵌对象.type
    #         return _要素类型反映射[类型.upper()]

    #     @property
    #     def 点表(self):
    #         return self._内嵌对象.getPart()

    #     @property
    #     def json格式(self):
    #         import json

    #         return json.loads(self._内嵌对象.JSON)

    #     def 交集(self, 相交要素形状: "游标类.形状类", 类型="面"):
    #         _交集类型映射表 = {4: 4, "面": 4, 2: 2, "线": 2, 1: 1, "点": 1}
    #         ret = self._内嵌对象.intersect(相交要素形状._内嵌对象, _交集类型映射表[类型])
    #         if ret:
    #             return 游标类.形状类(ret)
    #         else:
    #             return ret

    #     def 差集(self, 擦除要素形状: "游标类.形状类"):
    #         ret = self._内嵌对象.difference(擦除要素形状._内嵌对象)
    #         if ret:
    #             return 游标类.形状类(ret)
    #         else:
    #             return ret

    #     def 并集(self, 合并要素形状: "游标类.形状类"):
    #         ret = self._内嵌对象.union(合并要素形状._内嵌对象)
    #         if ret:
    #             return 游标类.形状类(ret)
    #         else:
    #             return ret

    #     # def 转线(self, 输出要素名称):
    #     #     arcpy.PolygonToLine_management(self._内嵌对象, neighbor_option="IGNORE_NEIGHBORS")

    #     @property
    #     def 内点(self):
    #         return self._内嵌对象.labelPoint

    #     @property
    #     def 部件数量(self):
    #         return self._内嵌对象.partCount

    #     @property
    #     def 折点数量(self):
    #         return self._内嵌对象.pointCount

    #     @property
    #     def 面积(self):
    #         return self._内嵌对象.area

    #     def 边界获取(self):
    #         return 游标类.形状类(self._内嵌对象.boundary())

    #     def 是否具有孔洞(self):
    #         return self._内嵌对象.hasOmittedBoundary

    #     def 是否为多部件要素(self):
    #         return self._内嵌对象.isMultipart

    #     def 是否包含曲线(self):
    #         ret = [x for x in self.json格式.keys() if "curve" in x]
    #         if len(ret) > 0:
    #             return True
    #         return False

    #     @property
    #     def 孔洞数量(self):
    #         折点和孔洞数量总数 = 0
    #         for 每个部件x in self._内嵌对象.getPart():
    #             折点和孔洞数量 = len(每个部件x)
    #             折点和孔洞数量总数 += 折点和孔洞数量
    #         return 折点和孔洞数量总数 - self.折点数量

    #     # @property
    #     # def 孔洞数量(self):
    #     #     return self._内嵌对象.interiorRingCount()

    #     # def 边界部件获取(self, 索引):
    #     #     return self._内嵌对象[索引]

    #     # def 边界组成数量(self):
    #     #     return self._内嵌对象.getPartCount()

    @staticmethod
    def 游标创建(游标类型: Literal["插入", "查询", "更新"], 输入要素路径, 需操作的字段名称列表: list, 自动创建缺失的字段=True):
        from bxarcpy.要素包 import 要素类

        if "*" in 需操作的字段名称列表:
            所有字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
            需操作的字段名称列表.extend(所有字段名称列表)
            需操作的字段名称列表.remove("*")

        所有字段名称列表 = 要素类.字段名称列表获取(输入要素路径)
        缺失的字段 = [字段名称 for 字段名称 in 需操作的字段名称列表 if 字段名称 not in 所有字段名称列表 and 字段名称 not in 枚举_特殊字段.keys() and 字段名称 not in 枚举_特殊字段.values()]
        if len(缺失的字段) > 0:
            if 自动创建缺失的字段:
                from bxarcpy.环境包 import 输入输出类

                输入输出类.输出消息(f"{输入要素路径}缺少以下字段：{缺失的字段}，将自动创建", 级别="警告")

                for 缺失的字段x in 缺失的字段:
                    要素类.字段添加(输入要素路径, 缺失的字段x)
            else:
                raise Exception(f"{输入要素路径}缺少以下字段：{缺失的字段}")

        需操作的字段名称列表temp = []
        for x in 需操作的字段名称列表:
            if x in 枚举_特殊字段:
                需操作的字段名称列表temp.append(枚举_特殊字段[x])
            else:
                需操作的字段名称列表temp.append(x)
        需操作的字段名称列表 = 需操作的字段名称列表temp
        # print(需操作的字段名称列表)
        if 游标类型 in ["更新"]:
            return arcpy.da.UpdateCursor(输入要素路径, 需操作的字段名称列表)  # type: ignore
        elif 游标类型 in ["插入", "新增"]:
            return arcpy.da.InsertCursor(输入要素路径, 需操作的字段名称列表)  # type: ignore
        elif 游标类型 in ["查找", "读取", "查询"]:
            return arcpy.da.SearchCursor(输入要素路径, 需操作的字段名称列表)  # type: ignore
        return arcpy.da.SearchCursor(输入要素路径, 需操作的字段名称列表)  # type: ignore

    @staticmethod
    def 属性获取_数据_字典形式(游标对象, 需操作的字段名称列表):
        for 行对象 in 游标对象:
            有序字典 = OrderedDict()
            for 字段索引i, 字段名称x in enumerate(需操作的字段名称列表):
                有序字典[字段名称x] = 行对象[字段索引i]
            yield 有序字典

    @staticmethod
    def 项迭代器获取(输入要素路径, 需操作的字段名称列表, 自动创建缺失的字段=True):
        with 游标类.游标创建(游标类型="查询", 输入要素路径=输入要素路径, 需操作的字段名称列表=需操作的字段名称列表, 自动创建缺失的字段=自动创建缺失的字段) as 游标实例:
            for 游标x in 游标类.属性获取_数据_字典形式(游标实例, 需操作的字段名称列表):
                yield 游标x

    @staticmethod
    def 项列表获取(输入要素路径, 需操作的字段名称列表, 自动创建缺失的字段=True):
        项列表 = []
        with 游标类.游标创建(游标类型="查询", 输入要素路径=输入要素路径, 需操作的字段名称列表=需操作的字段名称列表, 自动创建缺失的字段=自动创建缺失的字段) as 游标实例:
            for 游标x in 游标类.属性获取_数据_字典形式(游标实例, 需操作的字段名称列表):
                项列表.append(游标x)
        return 项列表

    @staticmethod
    def 项更新(输入要素路径, 项列表, 需操作的字段名称列表, 主键名称="_ID"):
        if 主键名称 not in 需操作的字段名称列表:
            raise Exception("主键名称必须存在于需操作的字段名称列表中")
        with 游标类.游标创建(游标类型="更新", 输入要素路径=输入要素路径, 需操作的字段名称列表=需操作的字段名称列表, 自动创建缺失的字段=True) as 游标实例:
            for 游标x in 游标类.属性获取_数据_字典形式(游标实例, 需操作的字段名称列表):
                匹配项列表 = [项x for 项x in 项列表 if 游标x[主键名称] == 项x[主键名称]]
                if len(匹配项列表) == 1:
                    匹配项 = 匹配项列表[0]
                    for 字段名称x in 需操作的字段名称列表:
                        游标x[字段名称x] = 匹配项[需操作的字段名称列表]
                    游标类.行更新_字典形式(游标实例, 游标x)

    @staticmethod
    def 重置(游标对象):
        # self._内嵌对象.reset()
        # print(f"行数据：{self._内嵌对象[0]}")
        # 行数据temp = []
        # for k, v in zip(self.字段名称列表, 行数据):
        #     if k == "_形状":
        #         行数据temp.append(游标类.形状类(v))
        #     else:
        #         行数据temp.append(v)
        # 行对象 = 游标类.行对象类(行数据, self)
        return 游标对象.reset()

    @staticmethod
    def 行删除(游标对象):
        return 游标对象.deleteRow()

    @staticmethod
    def 行更新_列表形式(游标对象, 行数据):
        return 游标对象.updateRow(行数据)

    @staticmethod
    def 行更新_字典形式(游标对象, 行数据: Union[OrderedDict, dict], 操作字段列表=None, 输入操作要素进行数据验证=None):
        if type(行数据) is dict and not 操作字段列表:
            raise Exception("行数据为字典时, 参数 操作字段列表 不能为空")
        行数据temp = []
        if 操作字段列表:
            for x in 操作字段列表:
                行数据temp.append(行数据[x])
        else:
            for k, v in 行数据.items():
                行数据temp.append(v)
            # 日志类.输出控制台(行数据)
        if 输入操作要素进行数据验证:
            from bxarcpy.要素包 import 要素类, 字段类

            字段列表 = 要素类.字段列表获取(输入操作要素进行数据验证)

            字段长度字典 = {}
            for 字段x in 字段列表:
                字段长度字典[字段类.属性获取_名称(字段x)] = 字段类.属性获取_长度(字段x)

            if not 操作字段列表:
                操作字段列表 = [k for k, v in 行数据.items()]
            for 操作字段x in 操作字段列表:
                if isinstance(行数据[操作字段x], str) and len(行数据[操作字段x]) > 字段长度字典[操作字段x]:
                    raise Exception(f"{行数据}中字段{操作字段x}的长度不能超过{字段长度字典[操作字段x]}")

        return 游标对象.updateRow(行数据temp)

    @staticmethod
    def 行插入_列表形式(游标对象, 行数据):
        # print(f"行数据为：{行数据}")
        # 日志类.输出控制台(行数据)
        return 游标对象.insertRow(行数据)

    @staticmethod
    def 行插入_字典形式(游标对象, 行数据: Union[OrderedDict, dict], 操作字段列表=None):
        if isinstance(行数据, dict) and not 操作字段列表:
            raise Exception("行数据为字典时, 参数 操作字段列表 不能为空")
        行数据temp = []
        if 操作字段列表:
            for x in 操作字段列表:
                行数据temp.append(行数据[x])
        else:
            for k, v in 行数据:
                行数据temp.append(v)
        # 日志类.输出控制台(行数据)
        return 游标对象.insertRow(行数据temp)


# class 数据访问类:
#     @staticmethod
#     def
# class 游标类_用于更新(游标类):
#     class 行对象:
#         def __init__(self, 行数据, 游标对象: "游标类_用于更新") -> None:
#             self.数据_字典格式 = {}
#             self.数据_列表格式 = []
#             self._内嵌对象_游标对象 = 游标对象
#             for k, v in zip(游标对象.字段名称列表, 行数据):
#                 if k == "_形状":
#                     self.数据_列表格式.append(游标类_用于更新.形状(v))
#                     self.数据_字典格式[k] = 游标类_用于更新.形状(v)
#                 else:
#                     self.数据_列表格式.append(v)
#                     self.数据_字典格式[k] = v
#             # self.数据_字典格式 = {k: v for k, v in zip(self._内嵌对象_游标对象.字段名称列表, 行数据)}

#         def 行删除(self):
#             return self._内嵌对象_游标对象._内嵌对象.deleteRow()

#         def 行更新_列表格式(self):
#             用于更新的列表 = []
#             for k, v in zip(self._内嵌对象_游标对象.字段名称列表, self.数据_列表格式):
#                 if k == "_形状":
#                     用于更新的列表.append(v._内嵌对象)
#                 else:
#                     用于更新的列表.append(v)
#             return self._内嵌对象_游标对象._内嵌对象.updateRow(用于更新的列表)

#         def 行更新_字典格式(self):
#             用于更新的列表 = []
#             for k in self._内嵌对象_游标对象.字段名称列表:
#                 if k == "_形状":
#                     用于更新的列表.append(self.数据_字典格式[k]._内嵌对象)
#                 else:
#                     用于更新的列表.append(self.数据_字典格式[k])
#             return self._内嵌对象_游标对象._内嵌对象.updateRow(用于更新的列表)

#     class 形状:
#         _类型映射表 = {"polyline": "线", "polygon": "面"}

#         def __init__(self, 内嵌对象) -> None:
#             # print(f"形状类：{内嵌对象.__class__}")
#             self._内嵌对象 = 内嵌对象

#         @property
#         def 类型(self):
#             类型 = self._内嵌对象.type
#             return 游标类_用于更新.形状._类型映射表[类型]

#         @property
#         def 点表(self):
#             return self._内嵌对象.getPart()

#         @property
#         def 折点数量(self):
#             return self._内嵌对象.pointCount

#         @property
#         def 面积(self):
#             return self._内嵌对象.area

#         def 是否具有孔洞(self):
#             return self._内嵌对象.hasOmittedBoundary

#         @property
#         def 孔洞数量(self):
#             折点和孔洞数量总数 = 0
#             for 每个部件x in self._内嵌对象.getPart():
#                 折点和孔洞数量 = len(每个部件x)
#                 折点和孔洞数量总数 += 折点和孔洞数量
#             return 折点和孔洞数量总数 - self.折点数量

#         # @property
#         # def 孔洞数量(self):
#         #     return self._内嵌对象.interiorRingCount()

#         def 是否为多部件要素(self):
#             return self._内嵌对象.isMultipart

#         @property
#         def 部件数量(self):
#             return self._内嵌对象.partCount

#         # def 边界部件获取(self, 索引):
#         #     return self._内嵌对象[索引]

#         # def 边界组成数量(self):
#         #     return self._内嵌对象.getPartCount()

#     def __init__(self, 输入要素名称, 需更新的字段名称列表):
#         self.字段名称列表 = 需更新的字段名称列表
#         需更新的字段名称列表temp = []
#         for x in 需更新的字段名称列表:
#             if x in 游标类_用于更新._需更新的字段名称列表映射表:
#                 需更新的字段名称列表temp.append(游标类_用于更新._需更新的字段名称列表映射表[x])
#             else:
#                 需更新的字段名称列表temp.append(x)
#         需更新的字段名称列表 = 需更新的字段名称列表temp

#         self._内嵌对象 = arcpy.da.UpdateCursor(输入要素名称, 需更新的字段名称列表)

#     def __enter__(self):
#         self._内嵌对象 = self._内嵌对象.__enter__()
#         return self

#     def __exit__(self, 异常类型, 异常值, 追溯信息):
#         # 如果__exit__返回值为True,代表吞掉了异常，继续运行
#         # 如果__exit__返回值不为True,代表吐出了异常
#         return self._内嵌对象.__exit__(异常类型, 异常值, 追溯信息)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         行数据 = self._内嵌对象.__next__()
#         行对象 = 游标类_用于更新.行对象(行数据, self)
#         return 行对象

#     def 下一个(self):
#         return self.__next__()

#     def 重置(self):
#         行数据 = self._内嵌对象.reset()
#         行对象 = 游标类_用于更新.行对象(行数据, self._内嵌对象)
#         return 行对象
