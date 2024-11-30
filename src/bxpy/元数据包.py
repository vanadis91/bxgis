class 变量元数据类:
    @staticmethod
    def 默认值设置(变量名, 默认值):
        import inspect

        a = inspect.currentframe()
        if not a:
            return None
        a = a.f_back
        if not a:
            return None
        outer_locals = a.f_locals
        if 变量名 not in outer_locals:
            return 默认值
        else:
            return outer_locals[变量名]


class 调用元数据类:
    @staticmethod
    def 调用栈帧获取_当前():
        import inspect

        # return inspect.currentframe().f_back  # type: ignore
        return inspect.stack()[1]

    @staticmethod
    def 调用栈帧获取_所有():
        import inspect

        return inspect.stack()[1:]

    class 调用栈帧:
        @staticmethod
        def 属性获取_代码(栈帧):
            return 栈帧.f_code

        @staticmethod
        def 属性获取_局部变量字典(栈帧):
            return 栈帧.f_locals

        @staticmethod
        def 属性获取_行号(栈帧):
            import inspect

            if type(栈帧) is inspect.FrameInfo:
                return 栈帧.frame.f_lineno
            else:
                return 栈帧.f_lineno

        @staticmethod
        def 属性获取_所在文件路径(栈帧):
            import inspect

            if type(栈帧) is inspect.FrameInfo:
                return 栈帧.filename
            else:
                return 栈帧.filename

        @staticmethod
        def 属性获取_函数名称(栈帧):
            import inspect

            if type(栈帧) is inspect.FrameInfo:
                return 栈帧.function
            else:
                return 栈帧.f_code.co_name
            # return 栈帧.f_code.co_name

        @staticmethod
        def 属性获取_全局变量字典(栈帧):
            return 栈帧.f_globals

        @staticmethod
        def 上一级调用栈帧获取(栈帧):
            import inspect

            if type(栈帧) is inspect.FrameInfo:
                return 栈帧.frame.f_back
            else:
                return 栈帧.f_back


class 对象元数据类:
    @staticmethod
    def 对象所属包(obj):
        import inspect

        return inspect.getmodule(obj)

    @staticmethod
    def 对象所在文件位置(obj):
        import inspect

        return inspect.getsourcefile(obj)

    @staticmethod
    def 对象源码(obj):
        import inspect

        return inspect.getsource(obj)

    @staticmethod
    def 属性设置(对象, 属性, 值):
        return setattr(对象, 属性, 值)

    @staticmethod
    def 属性获取(对象, 属性):
        return getattr(对象, 属性)

    @staticmethod
    def 动态创建类(类名称, 父类元祖: tuple, 属性和方法字典: dict):
        return type(类名称, 父类元祖, 属性和方法字典)


class 追踪元数据类:
    @staticmethod
    def 追踪信息打印并暂停():
        import traceback

        traceback.print_exc()
        input("按任意键继续……")

    @staticmethod
    def 追踪信息获取():
        import traceback

        return traceback.format_exc()


if __name__ == "__main__":
    # print(调用栈帧类.调用栈帧获取_当前())
    pass
