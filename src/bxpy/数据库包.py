from bxpy.日志包 import 日志类
from bxpy.时间包 import 时间类
from typing import Literal, Union
from bxpy.基本对象包 import 模块加载

模块加载("pymongo")
import pymongo

# import logging
# from bxpy import 系统
# import mongoengine as odm


class 工具集:
    @staticmethod
    def 创建唯一标识对象(唯一标识字符串=""):
        from bson.objectid import ObjectId

        if 唯一标识字符串 == "":
            return ObjectId()
        else:
            return ObjectId(唯一标识字符串)


class 数据库类mongodb:
    @staticmethod
    def 服务创建(主机地址="cloud.beixiao.top", 用户名="vanadis91", 密码="Txdsjsbx-01", 端口号=57017, 连接超时=5000, 数据库名="bxroot"):
        uri = f"mongodb://{用户名}:{密码}@{主机地址}:{端口号}/{数据库名}"
        return pymongo.MongoClient(uri, serverSelectionTimeoutMS=连接超时)

    @staticmethod
    def 属性获取_连接信息(服务: pymongo.MongoClient):
        return 服务.server_info()

    @staticmethod
    def 服务关闭(服务: pymongo.MongoClient):
        return 服务.close()

    class 库类:
        @staticmethod
        def 库打开(服务: pymongo.MongoClient, 库名称):
            return 服务[库名称]

        @staticmethod
        def 属性获取_表名称列表(库):
            return 库.list_collection_names()

    class 表类:
        def __init__(self, 库对象):
            self.内嵌对象 = 库对象
            self.表_列表 = self.内嵌对象.list_collection_names()

        @staticmethod
        def 表打开(库, 表名称):
            return 库[表名称]

        @staticmethod
        def 表删除(库, 表名称):
            try:
                ret = 库[表名称].drop()
                日志类.输出信息(表名称 + " 表删除成功")
                return ret
            except Exception as e:
                日志类.输出信息(f"执行 表_删除 失败，错误信息{str(e)}")

    class 项类:
        @staticmethod
        def 项新增(表, 新增项列表, 返回数据形式: Literal["操作项列表", "原始"] = "操作项列表", id输入类型: Literal["字符串", "对象"] = "对象", id输出类型: Literal["字符串", "对象"] = "字符串"):
            if type(新增项列表) == dict:
                新增项列表 = [新增项列表]
            if id输入类型 == "字符串":
                新增项列表Temp = []
                for x in 新增项列表:
                    if type(x) is dict and "_id" in x and type(x["_id"]) is not str:
                        x["_id"] = str(x["_id"])
                    新增项列表Temp.append(x)
                新增项列表 = 新增项列表Temp
            elif id输入类型 == "对象":
                新增项列表Temp = []
                for x in 新增项列表:
                    if type(x) is dict and "_id" in x and type(x["_id"]) is str:
                        x["_id"] = 工具集.创建唯一标识对象(x["_id"])
                    新增项列表Temp.append(x)
                新增项列表 = 新增项列表Temp
            try:
                result = 表.insert_many(新增项列表)
                ID列表 = 数据库类mongodb.项集合类_新增操作.属性获取_ID列表(result)
                日志类.输出信息(f"数据插入成功:{str(ID列表)}")
                if 返回数据形式 == "原始":
                    return result
                if 返回数据形式 == "操作项列表":
                    if result:
                        retList = [数据库类mongodb.项类.项查询(表, {"_id": x})[0] for x in ID列表]
                    else:
                        retList = []
                    if id输出类型 == "字符串":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is not str:
                                x["_id"] = str(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    elif id输出类型 == "对象":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is str:
                                x["_id"] = 工具集.创建唯一标识对象(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    return retList
            except Exception as e:
                日志类.输出警告(f"执行 项新增 失败，错误信息{str(e)}")

        @staticmethod
        def 项查询(表, 查询条件={}, 返回格式={}, 返回数据形式: Literal["操作项列表", "原始"] = "操作项列表", id输入类型: Literal["字符串", "对象"] = "对象", id输出类型: Literal["字符串", "对象"] = "字符串") -> list:
            if id输入类型 == "字符串":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is not str:
                    查询条件["_id"] = str(查询条件["_id"])
            elif id输入类型 == "对象":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is str:
                    查询条件["_id"] = 工具集.创建唯一标识对象(查询条件["_id"])
            try:
                ret = 表.find(查询条件, 返回格式)
                # 日志类.输出调试("全部数据查询成功")
                if 返回数据形式 == "原始":
                    return ret
                if 返回数据形式 == "操作项列表":
                    retList = list(ret)
                    if id输出类型 == "字符串":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is not str:
                                x["_id"] = str(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    elif id输出类型 == "对象":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is str:
                                x["_id"] = 工具集.创建唯一标识对象(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    return retList
            except Exception as e:
                from bxpy.元数据包 import 追踪元数据类

                日志类.输出错误(f"数据库类mongodb/项查询，错误，{追踪元数据类.追踪信息获取()}")
                return []

        @staticmethod
        def 项修改(表, 查询条件=None, 修改内容=None, 返回数据形式: Literal["操作项列表", "原始"] = "操作项列表", id输入类型: Literal["字符串", "对象"] = "对象", id输出类型: Literal["字符串", "对象"] = "字符串", **kw):
            if 修改内容 is None:
                修改内容 = {}
            if 查询条件 is None:
                查询条件 = {}
            if id输入类型 == "字符串":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is not str:
                    查询条件["_id"] = str(查询条件["_id"])
                if type(修改内容) is dict and "_id" in 修改内容 and type(修改内容["_id"]) is not str:
                    修改内容["_id"] = str(修改内容["_id"])
            elif id输入类型 == "对象":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is str:
                    查询条件["_id"] = 工具集.创建唯一标识对象(查询条件["_id"])
                if type(修改内容) is dict and "_id" in 修改内容 and type(修改内容["_id"]) is str:
                    修改内容["_id"] = 工具集.创建唯一标识对象(修改内容["_id"])
            try:
                ret = 表.update_many(查询条件, 修改内容, **kw)
                日志类.输出信息("全部数据修改成功")
                if 返回数据形式 == "原始":
                    return ret
                if 返回数据形式 == "操作项列表":
                    retList = 数据库类mongodb.项类.项查询(表, 查询条件)
                    if id输出类型 == "字符串":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is not str:
                                x["_id"] = str(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    elif id输出类型 == "对象":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is str:
                                x["_id"] = 工具集.创建唯一标识对象(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    return retList
            except Exception as e:
                日志类.输出信息(f"执行 项修改 失败，错误信息{e}")

        @staticmethod
        def 项替换(表, 查询条件=None, 替换内容=None, 返回数据形式: Literal["操作项列表", "原始"] = "操作项列表", id输入类型: Literal["字符串", "对象"] = "对象", id输出类型: Literal["字符串", "对象"] = "字符串", **kw):
            if 替换内容 is None:
                替换内容 = {}
            if 查询条件 is None:
                查询条件 = {}
            if id输入类型 == "字符串":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is not str:
                    查询条件["_id"] = str(查询条件["_id"])
                if type(替换内容) is dict and "_id" in 替换内容 and type(替换内容["_id"]) is not str:
                    替换内容["_id"] = str(替换内容["_id"])
            elif id输入类型 == "对象":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is str:
                    查询条件["_id"] = 工具集.创建唯一标识对象(查询条件["_id"])
                if type(替换内容) is dict and "_id" in 替换内容 and type(替换内容["_id"]) is str:
                    替换内容["_id"] = 工具集.创建唯一标识对象(替换内容["_id"])
            try:
                ret = 表.replace_one(查询条件, 替换内容, **kw)
                日志类.输出信息("全部数据替换成功")
                if 返回数据形式 == "原始":
                    return ret
                if 返回数据形式 == "操作项列表":
                    retList = 数据库类mongodb.项类.项查询(表, 查询条件)
                    if id输出类型 == "字符串":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is not str:
                                x["_id"] = str(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    elif id输出类型 == "对象":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is str:
                                x["_id"] = 工具集.创建唯一标识对象(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    return retList
            except Exception as e:
                日志类.输出信息(f"执行函数：项_替换 失败，错误信息{e}")

        @staticmethod
        def 项删除(表, 查询条件=None, 返回数据形式: Literal["操作项列表", "原始"] = "操作项列表", id输入类型: Literal["字符串", "对象"] = "对象", id输出类型: Literal["字符串", "对象"] = "字符串"):
            if 查询条件 is None:
                查询条件 = {}
            if id输入类型 == "字符串":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is not str:
                    查询条件["_id"] = str(查询条件["_id"])
            elif id输入类型 == "对象":
                if type(查询条件) is dict and "_id" in 查询条件 and type(查询条件["_id"]) is str:
                    查询条件["_id"] = 工具集.创建唯一标识对象(查询条件["_id"])
            try:
                ret = 表.delete_many(查询条件)
                日志类.输出信息("数据删除成功")
                if 返回数据形式 == "原始":
                    return ret
                if 返回数据形式 == "操作项列表":
                    retList = list(ret)
                    if id输出类型 == "字符串":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is not str:
                                x["_id"] = str(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    elif id输出类型 == "对象":
                        retListTemp = []
                        for x in retList:
                            if type(x) is dict and "_id" in x and type(x["_id"]) is str:
                                x["_id"] = 工具集.创建唯一标识对象(x["_id"])
                            retListTemp.append(x)
                        retList = retListTemp
                    return retList
            except Exception as e:
                日志类.输出信息(f"执行函数：项_删除_多个 失败，错误信息{e}")

    class 项集合类_新增操作:
        @staticmethod
        def 属性获取_ID列表(集合):
            return 集合.inserted_ids

    class 项集合类_查询操作:
        @staticmethod
        def 输出指定数量(集合, 数量):
            return 集合.limit(数量)

        @staticmethod
        def 排序(集合, 列名, 排序方式="正序"):
            排序方式字典 = {"正序": 1, "倒序": 0}
            return 集合.sort(列名, 排序方式字典[排序方式])

    class 项集合类_修改操作:
        @staticmethod
        def 属性获取_查询到的数量(集合):
            return 集合.matched_count

        @staticmethod
        def 属性获取_被修改的数量(集合):
            return 集合.modified_count

    class 项集合类_删除操作:
        @staticmethod
        def 属性获取_被删除的数量(集合):
            return 集合.deleted_count

    # @staticmethod
    # def 连接_启动(路径):
    #     子进程("mongod --dbpath" + 路径)


# class odm服务:
#     def __init__(self, 服务对象=None):
#         if 服务对象:
#             self.内嵌对象 = 服务对象
#         else:
#             self.内嵌对象 = None

#     @staticmethod
#     def 服务_启动(路径):
#         子进程("mongod --dbpath" + 路径)

#     def 服务_连接(self):
#         return self

#     @staticmethod
#     def 库_打开(库名称str, uri="mongodb://localhost:27017/test"):
#         return _odm库(odm.connect(db=库名称str, host=uri))


# class _odm库:
#     def __init__(self, 库对象):
#         self.内嵌对象 = 库对象

#     @staticmethod
#     def 表_建立映射(映射类的名称, 父类tup, 属性和方法dict):
#         return type(映射类的名称, 父类tup, 属性和方法dict)


# # class _odm表:
# #     def __init__(self, 表对象):
# #         self.内嵌对象 = 表对象


# class odm表映射_常规表(odm.Document):
#     def __init__(self, *args, 通过字典生成=None, **kwargs):
#         if 通过字典生成:
#             super().__init__(*args, **通过字典生成, **kwargs)
#         else:
#             super().__init__(*args, **kwargs)

#     meta = {"abstract": True}

#     @classmethod
#     def 项_新增(cls, *args, 通过字典生成=None, **kwargs):
#         return cls(*args, 通过字典生成=通过字典生成, **kwargs).save()

#     @classmethod
#     def 项_删除(cls, *args, 查询函数=None, **kwargs):
#         return _odm项查询集合(cls.objects).查询(*args, 查询函数=查询函数, **kwargs).删除()

#     @classmethod
#     def 项_修改(cls, *args, 修改函数=None, **kwargs):
#         return _odm项查询集合(cls.objects).修改(*args, 修改函数=修改函数, **kwargs)

#     @classmethod
#     def 项_查询(cls, *args, 查询函数=None, **kwargs):
#         return _odm项查询集合(cls.objects).查询(*args, 查询函数=查询函数, **kwargs)

#     # @classmethod
#     # def 项_列表(cls):
#     #     return _odm项查询集合(cls.objects)

#     # @classmethod
#     # def 项_查询(cls, 查询单个结果=False):
#     #     if 查询单个结果:
#     #         return cls.objects.first()
#     #     else:
#     #         return cls.objects.all()


# class odm表映射_动态表(odm.DynamicDocument):
#     meta = {"abstract": True}


# class odm表映射_配置:
#     def __init__(self):
#         self.映射的表 = None
#         self.是否允许继承 = False
#         self.是否为抽象类 = False
#         self.项排序 = None

#     def 渲染(self):
#         render = {}
#         if self.映射的表:
#             render["collection"] = self.映射的表
#         if self.是否允许继承:
#             render["allow_inheritance"] = self.是否允许继承
#         if self.是否为抽象类:
#             render["abstract"] = self.是否为抽象类
#         if self.项排序:
#             """

#             :param 列名及排序方式列表:
#             :return:
#             :test: 列名及排序方式列表 = [{'列名':'123', '排序方式':'正序'}]
#             """
#             temp = []
#             for x in self.项排序:
#                 if x["排序方式"] == "正序":
#                     temp.append("+" + x["列名"])
#                 elif x["排序方式"] == "倒序":
#                     temp.append("-" + x["列名"])
#             render["ordering"] = temp
#         return render


# class _odm项查询集合:
#     def __init__(self, 内嵌对象):
#         if type(内嵌对象) == odm.queryset.queryset.QuerySet:
#             self.内嵌对象queryset = 内嵌对象
#             self.内嵌对象 = None
#         else:
#             self.内嵌对象queryset = None
#             self.内嵌对象 = 内嵌对象

#     def __str__(self):
#         if self.内嵌对象queryset:
#             return "<class QuerySet>" + str(self.内嵌对象queryset)
#         else:
#             return str(self.内嵌对象.__class__) + str(self.内嵌对象)

#     def __iter__(self):
#         if self.内嵌对象queryset:
#             return self.内嵌对象queryset.__iter__()
#         else:
#             return self.内嵌对象.__iter__()

#     def __next__(self):
#         if self.内嵌对象queryset:
#             return self.内嵌对象queryset.__next__()
#         else:
#             return self.内嵌对象.__next__()

#     def __getitem__(self, item):
#         if self.内嵌对象queryset:
#             return self.内嵌对象queryset.__getitem__(item)
#         else:
#             return self.内嵌对象.__getitem__(item)

#     def 新增(self):
#         if self.内嵌对象queryset:
#             for xx in self.内嵌对象queryset:
#                 xx.save()
#         else:
#             for xx in self.内嵌对象:
#                 xx.save()

#     def 删除(self):
#         if self.内嵌对象queryset:
#             return self.内嵌对象queryset.delete()
#         else:
#             for x in self.内嵌对象:
#                 x.delete()

#     def 修改(self, *args, 修改函数=None, **kwargs):
#         if 修改函数:
#             self.__init__(map(修改函数, self, **kwargs))
#             for xx in self.内嵌对象:
#                 xx.save()
#             return self
#         if self.内嵌对象queryset:
#             self.__init__(self.内嵌对象queryset.update(*args, **kwargs))
#             return self
#         日志类.输出警告("修改 未执行")

#     def 查询(self, *args, 查询函数=None, **kwargs):
#         if 查询函数:
#             self.__init__(filter(查询函数, self))
#             return self
#         if self.内嵌对象queryset:
#             self.__init__(self.内嵌对象queryset.filter(*args, **kwargs))
#             return self
#         日志类.输出警告("查询 未执行")

#     # def 输出指定数量(self, 数量):
#     #     if self.内嵌对象queryset:
#     #         if 数量 == 1:
#     #             return self.内嵌对象queryset.first()
#     #     else:
#     #         if 数量 == 1:
#     #             return self.内嵌对象[0]


# class odm字典映射(odm.EmbeddedDocument):
#     meta = {"abstract": True}


# class odm数据类型_字符串(odm.StringField):
#     def __init__(self, 是否必须=False, 最大长度=255, 选项=None, 主键=False, **kwargs):
#         super().__init__(required=是否必须, max_length=最大长度, choices=选项, primary_key=主键, **kwargs)


# class odm数据类型_整数(odm.IntField):
#     def __init__(self, 是否必须=False, 默认=0, **kwargs):
#         super().__init__(required=是否必须, default=默认, **kwargs)


# class odm数据类型_浮点(odm.FloatField):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)


# class odm数据类型_日期(odm.DateTimeField):
#     def __init__(self, 默认=时间类.时间创建_当前()._内嵌对象, **kwargs):
#         super().__init__(default=默认, **kwargs)


# class odm数据类型_列表(odm.ListField):
#     def __init__(self, 项数据类型, **kwargs):
#         super().__init__(项数据类型, **kwargs)


# class odm数据类型_字典(odm.EmbeddedDocumentField):
#     def __init__(self, 字典名称, **kwargs):
#         super().__init__(字典名称, **kwargs)


if __name__ == "__main__":
    # a = 创建唯一标识对象()
    # b = 创建唯一标识对象("131234567891452145235145")
    # print(a)
    # if a == b:
    #     print("相同")
    # else:
    #     print("不相同")
    pass
    # 库 = mongo服务().服务_连接().库_打开('test')
    # 表 = 库.表_打开('testexcel')
    # mydict = [{"name": "Bill2", "address": "Highway 37"},
    #           {"name": "Bill1", "address": "Highway 37"}]
    # mydict1 = {"name": "Bill", "address": "Highway 37"}
    # # 表.项_新增(mydict)
    # test = 表.项_查询({"name": "Bill2"}, {}).内嵌对象
    # del test[0]
    # print(test[0])
    # print(type(test))
    # aa = 表.项_查询({"name": "Bill"}, {"name": 1, "_id": 0}).指定输出数量(3)
    # bb = [x for x in aa]
    # print(bb)
    # print(表.项_查询())
    # aa = 表.项_修改({"name": "Bill"}, {'$inc': {'x': 3}})
    # aa = 表.项_删除({"name": "Bill1"})
    # print(aa.内嵌对象)
    # print(aa.查询到的数量)
    # print(aa.被修改的数量)
    # 库 = odm服务().服务_连接().库_打开('test')

    # 测试excel = 库.表_建立映射('测试excel', (odm表映射_常规表,), dict(
    #     meta=odm表映射_配置().映射的表('testexcel'),
    #     名称=odm数据类型_字符串(),
    #     name=odm数据类型_字符串(),
    #     address=odm数据类型_字符串(),
    #     地址=odm数据类型_字符串(),
    #     啊啊啊=odm数据类型_字符串(),
    #     x=odm数据类型_整数()))

    # class 成绩(odm字典映射):
    #     科目 = odm数据类型_字符串()
    #     分数 = odm数据类型_整数()

    # class 测试excel(odm表映射_常规表):
    #     meta = odm表映射_配置().映射的表('testexcel')
    #     名称 = odm数据类型_字符串()
    #     name = odm数据类型_字符串()
    #     address = odm数据类型_字符串()
    #     地址 = odm数据类型_字符串()
    #     啊啊啊 = odm数据类型_字符串()
    #     x = odm数据类型_整数()
    #     成绩 = odm数据类型_列表(odm数据类型_字典(成绩))

    #
    #
    # aa = 测试excel.项_查询()
    # aa.删除()

    # def temp(x):
    #     x['啊啊啊'] = '测试5'
    #     return 测试excel.项_新增(id=x['id'], name=x['name'], 啊啊啊=x['啊啊啊'])
    #
    # for y in aa:
    #     temp(y)

    # aa = aa.修改(修改函数=temp)
    # print(aa[17].id)
    # print([x['啊啊啊'] for x in aa])

    # print([x for x in aa])
    # bb = filter(lambda x: x['name'] == '测试3', aa)
    # print(list(bb))
    # print(type(aa.内嵌对象queryset))
    # cj1 = 成绩(科目='语文', 分数=98)
    # cj2 = 成绩(科目='数学', 分数=97)
    # aa = 测试excel.项_新增(x=13)
    # aa = 测试excel(名称='测试4', 地址='地址4', 成绩=[cj1, cj2])
    # aa.保存()
    # print(aa.pk)
