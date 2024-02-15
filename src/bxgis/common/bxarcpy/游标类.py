from ast import If
from sre_constants import IN
from bxpy import 日志
import arcpy
from .常量 import _要素类型反映射


class 游标类:
    _需操作的字段名称列表映射表 = {
        "SHAPE@": "SHAPE@",
        "_形状": "SHAPE@",
        "OID@": "OID@",
        "_ID": "OID@",
        "_面积": "SHAPE@AREA",
        "SHAPE@AREA": "SHAPE@AREA",
        "_长度": "SHAPE@LENGTH",
        "SHAPE@LENGTH": "SHAPE@LENGTH",
        "_质心": "SHAPE@CENTROID",
        "SHAPE@CENTROID": "SHAPE@CENTROID",
        "_外接矩形": "SHAPE@EXTENT",
        "SHAPE@EXTENT": "SHAPE@EXTENT",
        "_外接矩形": "SHAPE@EXTENT",
        "SHAPE@EXTENT": "SHAPE@EXTENT",
        "_坐标": "SHAPE@XY",
        "SHAPE@XY": "SHAPE@XY",
    }

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

    class 形状类:
        def __init__(self, 内嵌对象) -> None:
            # print(f"形状类：{内嵌对象.__class__}")
            self._内嵌对象 = 内嵌对象

        @property
        def 类型(self):
            类型 = self._内嵌对象.type
            return _要素类型反映射[类型.upper()]

        @property
        def 点表(self):
            return self._内嵌对象.getPart()

        @property
        def json格式(self):
            import json

            return json.loads(self._内嵌对象.JSON)

        def 交集(self, 相交要素形状: "游标类.形状类", 类型="面"):
            _交集类型映射表 = {4: 4, "面": 4, 2: 2, "线": 2, 1: 1, "点": 1}
            ret = self._内嵌对象.intersect(相交要素形状._内嵌对象, _交集类型映射表[类型])
            if ret:
                return 游标类.形状类(ret)
            else:
                return ret

        def 差集(self, 擦除要素形状: "游标类.形状类"):
            ret = self._内嵌对象.difference(擦除要素形状._内嵌对象)
            if ret:
                return 游标类.形状类(ret)
            else:
                return ret
            
        def 并集(self, 合并要素形状: "游标类.形状类"):
            ret = self._内嵌对象.union(合并要素形状._内嵌对象)
            if ret:
                return 游标类.形状类(ret)
            else:
                return ret

        # def 转线(self, 输出要素名称):
        #     arcpy.PolygonToLine_management(self._内嵌对象, neighbor_option="IGNORE_NEIGHBORS")

        @property
        def 内点(self):
            return self._内嵌对象.labelPoint

        @property
        def 部件数量(self):
            return self._内嵌对象.partCount

        @property
        def 折点数量(self):
            return self._内嵌对象.pointCount

        @property
        def 面积(self):
            return self._内嵌对象.area

        def 边界获取(self):
            return 游标类.形状类(self._内嵌对象.boundary())

        def 是否具有孔洞(self):
            return self._内嵌对象.hasOmittedBoundary

        def 是否为多部件要素(self):
            return self._内嵌对象.isMultipart

        def 是否包含曲线(self):
            ret = [x for x in self.json格式.keys() if "curve" in x]
            if len(ret) > 0:
                return True
            return False

        @property
        def 孔洞数量(self):
            折点和孔洞数量总数 = 0
            for 每个部件x in self._内嵌对象.getPart():
                折点和孔洞数量 = len(每个部件x)
                折点和孔洞数量总数 += 折点和孔洞数量
            return 折点和孔洞数量总数 - self.折点数量

        # @property
        # def 孔洞数量(self):
        #     return self._内嵌对象.interiorRingCount()

        # def 边界部件获取(self, 索引):
        #     return self._内嵌对象[索引]

        # def 边界组成数量(self):
        #     return self._内嵌对象.getPartCount()

    @staticmethod
    def 游标创建_通过名称(游标类型, 输入要素名称, 需操作的字段名称列表):
        return 游标类(游标类型, 输入要素名称, 需操作的字段名称列表)

    def __init__(self, 游标类型, 输入要素名称, 需操作的字段名称列表: list):
        for x in 需操作的字段名称列表:
            if x == "*":
                from bxarcpy import 要素类

                要素 = 要素类.要素读取_通过名称(输入要素名称)
                所有字段名称列表 = 要素.字段名称列表获取()
                需操作的字段名称列表.extend(所有字段名称列表)
                需操作的字段名称列表.remove("*")

        self.字段名称列表 = 需操作的字段名称列表
        self.游标类型 = 游标类型
        需更新的字段名称列表temp = []
        for x in 需操作的字段名称列表:
            if x in 游标类._需操作的字段名称列表映射表:
                需更新的字段名称列表temp.append(游标类._需操作的字段名称列表映射表[x])
            else:
                需更新的字段名称列表temp.append(x)
        需操作的字段名称列表 = 需更新的字段名称列表temp
        # print(需操作的字段名称列表)
        if 游标类型 in ["更新"]:
            self._内嵌对象 = arcpy.da.UpdateCursor(输入要素名称, 需操作的字段名称列表)  # type: ignore
        elif 游标类型 in ["插入", "新增"]:
            self._内嵌对象 = arcpy.da.InsertCursor(输入要素名称, 需操作的字段名称列表)  # type: ignore
        elif 游标类型 in ["查找", "读取", "查询"]:
            self._内嵌对象 = arcpy.da.SearchCursor(输入要素名称, 需操作的字段名称列表)  # type: ignore

    def __enter__(self):
        self._内嵌对象 = self._内嵌对象.__enter__()
        return self

    def __exit__(self, 异常类型, 异常值, 追溯信息):
        # 如果__exit__返回值为True,代表吞掉了异常，继续运行
        # 如果__exit__返回值不为True,代表吐出了异常
        return self._内嵌对象.__exit__(异常类型, 异常值, 追溯信息)

    def __iter__(self):
        return self

    def __next__(self):
        行数据 = self._内嵌对象.__next__()
        # 行对象 = 游标类.行对象类(行数据, self)
        行数据temp = []
        for k, v in zip(self.字段名称列表, 行数据):
            if k == "_形状":
                行数据temp.append(游标类.形状类(v))
            else:
                行数据temp.append(v)
        行数据temp = {k: v for k, v in zip(self.字段名称列表, 行数据temp)}
        # print(f"行数据temp：{行数据temp}")
        return 行数据temp

    def 下一个(self):
        return self.__next__()

    def 重置(self):
        # self._内嵌对象.reset()
        # print(f"行数据：{self._内嵌对象[0]}")
        # 行数据temp = []
        # for k, v in zip(self.字段名称列表, 行数据):
        #     if k == "_形状":
        #         行数据temp.append(游标类.形状类(v))
        #     else:
        #         行数据temp.append(v)
        # 行对象 = 游标类.行对象类(行数据, self)
        self._内嵌对象.reset()
        return

    def 行删除(self):
        return self._内嵌对象.deleteRow()

    def 行更新(self, 行数据):
        行数据 = [行数据[y] for y in self.字段名称列表]
        用于更新的列表 = []
        for k, v in zip(self.字段名称列表, 行数据):
            if k == "_形状" and v.__class__.__name__ == "形状类":
                用于更新的列表.append(v._内嵌对象)
            else:
                用于更新的列表.append(v)
        return self._内嵌对象.updateRow(用于更新的列表)

    def 行插入(self, 行数据):
        # print(f"行数据为：{行数据}")
        行数据 = [行数据[y] for y in self.字段名称列表]
        用于插入的列表 = []
        for k, v in zip(self.字段名称列表, 行数据):
            if k == "_形状" and v.__class__.__name__ == "形状类":
                用于插入的列表.append(v._内嵌对象)
            else:
                用于插入的列表.append(v)
        return self._内嵌对象.insertRow(用于插入的列表)


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
