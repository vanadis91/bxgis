class 测试类:
    @staticmethod
    def 测试启动_doctest():
        import doctest

        doctest.testmod()

    @staticmethod
    def 测试启动_pytest(路径列表=None):
        from bxpy.基本对象包 import 模块加载

        模块加载("pytest")

        import pytest
        from bxpy.系统包 import 系统类
        from bxpy.路径包 import 路径类

        当前工作目录 = 系统类.属性获取_当前工作目录()
        ini文件目录 = 路径类.连接(当前工作目录, "pytest.ini")
        if 路径类.是否存在(ini文件目录):
            pytest.main(路径列表)
            return

        路径类.新增(ini文件目录)
        with open("pytest.ini", mode="w") as f:
            f.writelines(
                [
                    "[pytest]\n",
                    "python_files = *_test.py test_*\n",
                    "python_classes = Test* test_* *_test\n",
                    "python_functions = test_* *_test\n",
                ]
            )
        pytest.main(路径列表)
        # 路径类.删除(ini文件目录)
        return


if __name__ == "__main__":
    print(测试类.测试启动_pytest())
