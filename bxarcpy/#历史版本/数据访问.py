import arcpy

# cursor = arcpy.da.SearchCursor(要素类, ["地类编号"])
# print(cursor.fields)
# print("Next 1: {}".format(cursor.next()))
# with arcpy.da.SearchCursor(要素类, ["地类编号"]) as cursor:
#     print(cursor.fields)
#     print("Next 1: {}".format(cursor.next()))


class 更新游标:
    def __init__(self, 输入要素, 字段列表):
        self.内嵌对象 = arcpy.da.UpdateCursor(输入要素, 字段列表)
        self.字段列表 = self.内嵌对象.fields

    def __enter__(self):
        self.内嵌对象 = self.内嵌对象.__enter__()
        return self

    def __exit__(self, 异常类型, 异常值, 追溯信息):
        # 如果__exit__返回值为True,代表吞掉了异常，继续运行
        # 如果__exit__返回值不为True,代表吐出了异常
        return self.内嵌对象.__exit__(异常类型, 异常值, 追溯信息)

    def __iter__(self):
        return self

    def __next__(self):
        return self.内嵌对象.__next__()

    def 下一个(self):
        return self.内嵌对象.__next__()

    def 重置(self):
        return self.内嵌对象.reset()

    def 当前行删除(self):
        return self.内嵌对象.deleteRow()

    def 当前行更新(self, 列表):
        return self.内嵌对象.updateRow(列表)


if __name__ == "__main__":
    import bxarcpy

    with bxarcpy.环境.环境管理器(临时工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb", 工作空间=r"C:\Users\common\project\J江东区临江控规\临江控规_数据库.gdb"):
        要素类 = "DIST_用地规划图"
        with 更新游标(要素类, ["地类编号"]) as 游标:
            # print(游标.字段列表)
            # print(type(游标.内嵌对象.next()))
            print(游标.下一个())
            # for x in cursor:
            #     print(f"Next：{x}")
        pass
