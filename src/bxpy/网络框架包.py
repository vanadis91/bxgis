from bxpy.基本对象包 import 模块加载

模块加载("flask")
模块加载("flask_cors")
模块加载("flask_login")
# from bxpy import 转换
from bxpy.时间包 import 时间间隔类, 时间类
from flask import Flask, session, Response, Blueprint
from flask_cors import CORS
from typing import Union, Literal, Any, TypeVar
import flask_login

框架或蓝图 = TypeVar("框架或蓝图", Blueprint, Flask)
# import os
# from flask import Flask, Blueprint, request, session, url_for, redirect, render_template, render_template_string, abort, flash, get_flashed_messages, make_response, Response


# from werkzeug.routing import BaseConverter
# from werkzeug.utils import secure_filename


class 配置:
    class 枚举_内容类型:
        text = "text/plain"
        html = "text/html"
        json = "application/json"
        xml = "text/xml"


class 工具集:
    class 密码处理:
        @staticmethod
        def 密码生成_HASH方式(字符串):
            from werkzeug.security import generate_password_hash

            return generate_password_hash(字符串)

        @staticmethod
        def 密码验证_HASH方式(正确的密码HASH值, 输入值):
            from werkzeug.security import check_password_hash

            return check_password_hash(正确的密码HASH值, 输入值)

    class 令牌处理:
        @staticmethod
        def Token生成(data, 有效时间=6000):
            模块加载("jwt", "pyjwt")
            import jwt

            会话密钥 = b"\x1c\x9c\x8bl\x1d`\xe5ai\x85\xd6\xe9\x8bLFg"
            expInt = 时间类.转换_到时间戳_毫秒为整数(时间类.时间创建_当前()) + 有效时间
            payload = {"exp": expInt, "data": data}
            token = jwt.encode(payload, key=会话密钥, algorithm="HS256")
            print(f"token: {token}")
            return token

        @staticmethod
        def Token验证(tokenStr):
            模块加载("jwt", "pyjwt")
            import jwt

            会话密钥 = b"\x1c\x9c\x8bl\x1d`\xe5ai\x85\xd6\xe9\x8bLFg"

            try:
                # tokenBytes = tokenStr.encode('utf-8')
                # print(f"tokenStr: {tokenStr}")
                payload = jwt.decode(tokenStr, key=会话密钥, algorithms=["HS256"])
                return payload
            except jwt.PyJWTError as e:
                print(f"jwt验证失败: {e}")
                return None

    @staticmethod
    def 链接构建(*值, **参):
        """
        url_for('page', num=1, q='welcome to w3c 15%2')。URL 构建会转义特殊字符和 Unicode 数据，免去你很多麻烦。如果你的应用不位于 URL 的根路径（比如，在 /myapplication 下，而不是 / ）， url_for() 会妥善处理这个问题。
        :param 值:
        :param 参:如果key不是预设值，那么key+value将作为数据集getArgs。
        :return:
        """
        from flask import url_for

        return url_for(*值, **参)


class 插件集:
    class 登录管理器类:
        # import flask_login

        # 类模版_用户类 = flask_login.UserMixin
        # 装饰器_登录检测 = flask_login.login_required
        # 当前用户 = flask_login.current_user
        @staticmethod
        def 登录管理器创建():
            return flask_login.LoginManager()

        @staticmethod
        def 登录管理器挂载(登陆管理器, 应用):
            return 登陆管理器.init_app(应用)

        @staticmethod
        def 属性获取_登录视图(登陆管理器):
            return 登陆管理器.login_view

        @staticmethod
        def 属性设置_登录视图(登陆管理器, x):
            登陆管理器.login_view = x

        @staticmethod
        def 属性获取_当前用户():
            return flask_login.current_user

        @staticmethod
        def 属性获取_用户类模版():
            return flask_login.UserMixin

        @staticmethod
        def 装饰器_定义未授权处理函数(登陆管理器: flask_login.LoginManager):
            return 登陆管理器.unauthorized_handler

        @staticmethod
        def 装饰器_定义获取用户函数_通过唯一标识(登陆管理器: flask_login.LoginManager):
            return 登陆管理器.user_loader

        @staticmethod
        def 装饰器_定义获取用户函数_通过请求(登陆管理器: flask_login.LoginManager):
            return 登陆管理器.request_loader

        @staticmethod
        def 装饰器_检测是否登录():
            return flask_login.login_required

        @staticmethod
        def 用户登录(登陆管理器, 用户对象):
            # return flask_login.login_user(用户对象, remember=True)
            return flask_login.login_user(用户对象, remember=True)

        @staticmethod
        def 用户登出(登陆管理器):
            return flask_login.logout_user()


class _框架及蓝图类模版:
    @staticmethod
    def 路由(框架: 框架或蓝图, 路径, 请求方法=["GET", "POST", "OPTIONS", "PUT"]):
        """

        :param 路径: 路径中可以包括变量和限制变量类型，如'/page/<int:num>'，变量将作为被装饰函数的形参。flask添加路由的尾部带有/：访问时加/和不加/效果是一样的。flask添加路由的尾部没有/：访问时加/会报错，只能不加/才能访问成功
        :param 请求方法:
        :return:
        """
        options = {"methods": 请求方法}

        def decorator(f):
            endpoint = options.pop("endpoint", None)
            框架.add_url_rule(路径, endpoint, f, **options)
            return f

        return decorator

    class 请求类:
        from flask import make_response
        from flask import request, Request

        @staticmethod
        def 请求读取(请求实例=request):
            return 请求实例

        @staticmethod
        def 属性获取_请求头(请求: Request):
            return 请求.headers

        class 请求头:
            from werkzeug.datastructures.headers import Headers

            @staticmethod
            def 获取指定键的值_单个(请求头: Headers, 键, 获取不到时返回的值="") -> str:
                return 请求头.get(键, 获取不到时返回的值)

            @staticmethod
            def 获取指定键的值_多个(请求头: Headers, 键) -> list:
                return 请求头.getlist(键)

            @staticmethod
            def 获取所有键值(请求头: Headers):
                return dict(请求头)

        @staticmethod
        def 属性获取_请求方式(请求: Request):
            return 请求.method

        @staticmethod
        def 属性获取_请求网址(请求: Request):
            return 请求.url

        @staticmethod
        def 属性获取_请求域名(请求: Request):
            return 请求.host

        @staticmethod
        def 属性获取_路径(请求: Request):
            return 请求.path

        @staticmethod
        def 属性获取_路径_完整(请求: Request):
            return 请求.full_path

        @staticmethod
        def 属性获取_临时存储cookies(请求: Request):
            return 请求.cookies

        @staticmethod
        def 属性获取_内容_args(请求: Request):
            return 请求.args

        @staticmethod
        def 属性获取_内容_args_按键值(请求: Request, 键名称="", 获取不到时返回的值="", 方式: Literal["获取指定键的值_单个", "获取指定键的值_多个", "获取所有键值"] = "获取指定键的值_单个"):
            if 方式 == "获取指定键的值_单个":
                return 请求.args.get(键名称, 获取不到时返回的值)
            elif 方式 == "获取指定键的值_多个":
                return 请求.args.getlist(键名称)
            elif 方式 == "获取所有键值":
                return dict(请求.args)

        @staticmethod
        def 属性获取_内容_json(请求: Request) -> dict:
            # 如果将content-type指定为application/json， flask就会将接收到的请求体数据做一次json编码转换，将字符串转换为字典对象，赋值给属性json
            return 请求.json  # type: ignore

        @staticmethod
        def 属性获取_内容_data(请求: Request):
            # 发送的请求体中，当content-type不是multipart/form-data、application/x-www-form-urlencoded 这两种类型时，data才会有值，例如我现在用postman指定的content-type是text/plain
            return 请求.data

        @staticmethod
        def 属性获取_内容_form(请求: Request):
            # form 顾名思义是表单数据，当请求头content-type 是 application/x-www-form-urlencoded 或者是 multipart/form-data 时，请求体的数据才会被解析为form属性。
            return 请求.form

        @staticmethod
        def 属性获取_内容_files(请求: Request):
            # 当浏览器上传文件时，form表单需要指定 enctype为 multipart/form-data。意味着当请求头content-type是multipart/form-data，而且请求体中的字段中还有content-type属性时（说明是文件上传），flask会把它当做文件来处理，所以这时候 files 这个属性就有值了。
            return 请求.files

        @staticmethod
        def 属性获取_内容_stream(请求: Request):
            # 当浏览器上传文件时，form表单需要指定 enctype为 multipart/form-data。意味着当请求头content-type是multipart/form-data，而且请求体中的字段中还有content-type属性时（说明是文件上传），flask会把它当做文件来处理，所以这时候 files 这个属性就有值了。
            return 请求.stream

        class 内容_args:
            @staticmethod
            def 获取指定键的值_单个(内容, 键, 获取不到时返回的值="") -> str:
                return 内容.get(键, 获取不到时返回的值)

            @staticmethod
            def 获取指定键的值_多个(内容, 键) -> list:
                return 内容.getlist(键)

            @staticmethod
            def 获取所有键值(内容):
                return dict(内容)

        class 内容_json:
            @staticmethod
            def 获取指定键的值_单个(内容, 键, 获取不到时返回的值="") -> str:
                return 内容.get(键, 获取不到时返回的值)

            @staticmethod
            def 获取指定键的值_多个(内容, 键) -> list:
                return 内容.getlist(键)

            @staticmethod
            def 获取所有键值(内容):
                return dict(内容)

        class 内容_data:
            @staticmethod
            def 获取指定键的值_单个(内容, 键, 获取不到时返回的值="") -> str:
                return 内容.get(键, 获取不到时返回的值)

            @staticmethod
            def 获取指定键的值_多个(内容, 键) -> list:
                return 内容.getlist(键)

            @staticmethod
            def 获取所有键值(内容):
                return dict(内容)

        class 内容_form:
            @staticmethod
            def 获取指定键的值_单个(内容, 键, 获取不到时返回的值="") -> str:
                return 内容.get(键, 获取不到时返回的值)

            @staticmethod
            def 获取指定键的值_多个(内容, 键) -> list:
                return 内容.getlist(键)

            @staticmethod
            def 获取所有键值(内容):
                return dict(内容)

        class 内容_files:
            class 文件:
                @staticmethod
                def 属性获取_文件名(文件):
                    return 文件.filename  # type: ignore

                @staticmethod
                def 属性获取_数据stream(文件):
                    return 文件.stream  # type: ignore

                @staticmethod
                def 保存(文件, 路径):
                    """
                    保存路径可以是相对路径也可以是绝对路径。保存路径要精确到文件名称。保存的目录必须是已存在的。
                    :param 路径:可以写成os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                    :return:
                    """
                    return 文件.save(路径)  # type: ignore

            @staticmethod
            def 数量(内容):
                return 内容.Count  # type: ignore

        class 内容_stream:
            @staticmethod
            def 读取(内容):
                return 内容.read()

    class 响应类(Response):
        @staticmethod
        def 响应创建_通过元祖(响应内容, 状态码=None, 响应头=None, 响应内容类型=None):
            from bxpy.基本对象包 import 字类, 字典类, 基本对象类
            from flask import make_response

            if 响应内容类型 == "application/json":
                响应内容 = 字类.转换_到字(响应内容)
            # print(f'响应内容是: {响应内容}')
            # print(f'响应内容类型是: {type(响应内容)}')
            if 状态码 is None and 响应头 is None:
                resp = make_response(响应内容)
            elif 状态码 is None:
                resp = make_response(响应内容, 响应头)
            elif 响应头 is None:
                resp = make_response(响应内容, 状态码)
            else:
                resp = make_response(响应内容, 状态码, 响应头)

            if 响应内容类型 is not None:
                _框架及蓝图类模版.响应类.属性设置_响应内容类型(resp, 响应内容类型)
            return resp

        def 响应创建_通过渲染网页_通过模板(self, 模板路径, **其他变量):
            # noinspection PyArgumentList
            from flask import make_response
            from flask import render_template

            return make_response(render_template(模板路径, **其他变量))

        def 响应创建_通过渲染网页_通过字符串(self, 字符串):
            from flask import make_response
            from flask import render_template_string

            return make_response(render_template_string(字符串))

        def 响应创建_中断函数并返回错误(self, 错误代码, 错误内容=""):
            from flask import make_response
            from flask import abort

            resp = make_response(错误内容, 错误代码)
            abort(resp)

        def 响应创建_重定向(self, 网址):
            from flask import redirect

            return redirect(网址)

        def 响应创建_从目录发送(self, 文件路径, 是否作为文件发送=True):
            from flask import send_from_directory

            return send_from_directory("static", 文件路径, as_attachment=是否作为文件发送)

        @staticmethod
        def 属性获取_响应内容(响应: Response):
            return 响应.data

        @staticmethod
        def 属性设置_响应内容(响应: Response, 值):
            响应.data = 值

        @staticmethod
        def 属性获取_响应头(响应: Response):
            return 响应.headers

        @staticmethod
        def 属性获取_响应内容类型(响应: Response):
            return 响应.mimetype

        @staticmethod
        def 属性设置_响应内容类型(响应: Response, 值=配置.枚举_内容类型.text):
            响应.mimetype = 值

        @staticmethod
        def 属性获取_状态码(响应: Response):
            return 响应.status

        @staticmethod
        def 属性设置_状态码(响应: Response, 值=配置.枚举_内容类型.text):
            响应.status = 值

        class 响应头:
            from werkzeug.datastructures.headers import Headers

            @staticmethod
            def 属性获取_单个(响应头: Headers, 键, 获取不到时返回的值="") -> str:
                return 响应头.get(键, 获取不到时返回的值)

            @staticmethod
            def 属性设置(响应头: Headers, 键, 值):
                响应头[键] = 值

            @staticmethod
            def 属性获取_多个(响应头, 键) -> list:
                return 响应头.getlist(键)

            @staticmethod
            def 所有属性获取(响应头):
                return dict(响应头)

        class 临时存储cookies:
            @staticmethod
            def 属性设置(响应对象: Response, 键, 值, 持续时间=5 * 60):
                当前时间时间戳 = 时间类.转换_到时间戳(时间类.时间创建_当前())
                截止时间 = 当前时间时间戳 + 持续时间
                响应对象.set_cookie(key=键, value=值, expires=截止时间)

            @staticmethod
            def 属性删除(响应对象: Response, 键):
                响应对象.set_cookie(key=键, value="", expires=0)


class 蓝图类(_框架及蓝图类模版):
    @staticmethod
    def 蓝图创建(蓝图名称, 蓝图所在位置=__name__, URL前缀=None, 静态资源路径=None, 静态资源路径更改=None, 模板路径=None):
        from flask import Blueprint

        ret = Blueprint(
            name=蓝图名称,
            import_name=蓝图所在位置,
            url_prefix=URL前缀,
            static_folder=静态资源路径,
            static_url_path=静态资源路径更改,
            template_folder=模板路径,
        )
        return ret

    @staticmethod
    def 记录一次请求的信息(蓝图: Blueprint, func):
        @蓝图.record_once
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            return res

        return wrapper


class 框架类(_框架及蓝图类模版):
    @staticmethod
    def 框架创建(名称, 静态资源路径="static", 模板路径="templates", 跨域规则_是否允许请求发送cookie=True, 跨域规则_允许跨域的API接口=r"/*"):
        from flask_cors import CORS
        from flask import Flask

        app = Flask(名称, static_folder=静态资源路径, template_folder=模板路径)
        CORS(app, supports_credentials=跨域规则_是否允许请求发送cookie, resources=跨域规则_允许跨域的API接口)
        框架类.配置.属性设置_会话密钥(app)
        框架类.配置.属性设置_json是否作为ascii处理(app, False)
        框架类.配置.属性设置_会话和cookie是否同源(app, "None")
        框架类.配置.属性设置_会话和cookie是否安全(app, "None")
        return app

    @staticmethod
    def 属性获取_根目录(框架: Flask):
        return 框架.root_path

    @staticmethod
    def 属性获取_是否调试模式(框架: Flask):
        return 框架.debug

    @staticmethod
    def 属性设置_是否调试模式(框架: Flask, 值=True):
        框架.debug = 值

    @staticmethod
    def 运行(框架: Flask, IP地址="0.0.0.0", 端口=5000, 调试模式=None):
        框架.run(host=IP地址, port=端口, debug=调试模式)

    @staticmethod
    def 蓝图挂载(框架: Flask, 蓝图对象):
        框架.register_blueprint(蓝图对象)

    @staticmethod
    def 属性设置_跨域规则(框架: Flask, 是否允许请求发送cookie=True, 允许跨域的API接口=r"/*"):
        return CORS(框架, supports_credentials=是否允许请求发送cookie, resources=允许跨域的API接口)

    @staticmethod
    def 错误处理(框架: Flask, 错误代码):
        def decorator(f):
            框架.register_error_handler(错误代码, f)
            return f

        return decorator

    class 临时会话类session:
        """就是加密后的cookies"""

        @staticmethod
        def 属性获取(键):
            from flask import session

            return session[键]

        @staticmethod
        def 属性设置(键, 值):
            from flask import session

            session[键] = 值

        @staticmethod
        def 属性删除(键):
            from flask import session

            return session.pop(键, None)

    class 临时会话类flash:
        """也是session，即也是加密后的cookies，但是读取一次后会被销毁"""

        @staticmethod
        def 属性设置(值, 标签=None):
            from flask import flash

            if 标签:
                return flash(值, category=标签)
            return flash(值)

        @staticmethod
        def 属性获取(标签过滤=None):
            from flask import get_flashed_messages

            if 标签过滤:
                return get_flashed_messages(category_filter=标签过滤)
            return get_flashed_messages()

    class 配置:
        """
        # app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
        # app.config['UPLOAD_FOLDER'] = 'static/uploads/'
        # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        """

        @staticmethod
        def 属性获取_会话密钥(框架: Flask):
            return 框架.secret_key

        @staticmethod
        def 属性设置_会话密钥(框架: Flask, 密钥字符串="LoenDSdtjbX#%@!!*(0&^%)"):
            框架.secret_key = 密钥字符串

        @staticmethod
        def 属性获取_json是否作为ascii处理(框架: Flask):
            return 框架.config["JSON_AS_ASCII"]

        @staticmethod
        def 属性设置_json是否作为ascii处理(框架: Flask, 值=False):
            框架.config["JSON_AS_ASCII"] = 值

        @staticmethod
        def 属性获取_会话和cookie是否同源(框架: Flask):
            return 框架.config["SESSION_COOKIE_SAMESITE"]

        @staticmethod
        def 属性设置_会话和cookie是否同源(框架: Flask, 值="None"):
            框架.config["SESSION_COOKIE_SAMESITE"] = 值

        @staticmethod
        def 属性获取_会话和cookie是否安全(框架: Flask):
            return 框架.config["SESSION_COOKIE_SECURE"]

        @staticmethod
        def 属性设置_会话和cookie是否安全(框架: Flask, 值="None"):
            框架.config["SESSION_COOKIE_SECURE"] = 值

        @staticmethod
        def 属性获取_上传文件的存放路径(框架: Flask):
            return 框架.config["UPLOAD_FOLDER"]

        @staticmethod
        def 属性设置_上传文件的存放路径(框架: Flask, 值="static/"):
            框架.config["UPLOAD_FOLDER"] = 值

        @staticmethod
        def 属性获取_上传文件的允许类型(框架: Flask):
            return 框架.config["ALLOWED_EXTENSIONS"]

        @staticmethod
        def 属性设置_上传文件的允许类型(框架: Flask, 值={"png", "jpg", "jpeg", "gif"}):
            框架.config["ALLOWED_EXTENSIONS"] = 值

        @staticmethod
        def 属性获取_上传文件的最大容量(框架: Flask):
            return 框架.config["MAX_CONTENT_LENGTH"]

        @staticmethod
        def 属性设置_上传文件的最大容量(框架: Flask, 值=16 * 1024 * 1024):
            框架.config["MAX_CONTENT_LENGTH"] = 值

        @staticmethod
        def 属性获取_会话是否保留_即使关闭浏览器():
            return session.permanent

        @staticmethod
        def 属性设置_会话是否保留_即使关闭浏览器(框架: Flask, 值=False):
            session.permanent = 值

        @staticmethod
        def 属性获取_会话持续时间(框架: Flask):
            return 框架.permanent_session_lifetime

        @staticmethod
        def 属性设置_会话持续时间(框架: Flask, 值=时间间隔类.时间间隔创建(分=5)):
            框架.permanent_session_lifetime = 值

        @staticmethod
        def 属性获取_路径变量类型转换器(框架: Flask):
            return 框架.url_map.converters

        @staticmethod
        def 属性设置_路径变量类型转换器(框架: Flask, 值={}):
            # :param 值: 形式类似{'转换器名称str': 转换器类class, …}
            框架.url_map.converters = 值

        # class MyIntConverter(BaseConverter):
        #     """
        #     路径变量类型转化器
        #     """
        #
        #     def __init__(self, url_map):
        #         super(MyIntConverter, self).__init__(url_map)
        #
        #     def to_python(self, value):
        #         """
        #         to_python方法用于将url中的变量转换后供被@app.route包装的函数使用
        #         :param value:
        #         :return:
        #         """
        #         return int(value)
        #
        #     def to_url(self, value):
        #         """
        #         to_url方法用于flask.url_for中的参数转换
        #         :param value:
        #         :return:
        #         """
        #         return value * 2


if __name__ == "__main__":
    # from werkzeug.datastructures.headers import Headers

    # app = 框架("app")

    # app.配置.上传文件的存放路径 = 'static/uploads/'
    # app.配置.上传文件的允许类型 = {'png', 'jpg', 'jpeg', 'gif'}

    # @app.路由("/")
    # def hello_world():
    #     return "OK"

    # app.运行()
    # 框架.配置['上传路径'] = 'static/uploads/'
    # 框架.配置['上传允许拓展名'] = {'png', 'jpg', 'jpeg', 'gif'}
    # 框架.配置["会话密钥"] = r'LoenDSdtj\9bX#%@!!*(0&^%)'
    #
    #
    # @框架.路由("/register", 请求方法=['POST'])
    # def register():
    #     # print(框架.请求.请求头)
    #     # print(框架.请求.参数集post_data.获取参数值_所有("name"))
    #     # result = {'sum': 框架.请求.参数集json['n1'] + 框架.请求.参数集json['n2']}
    #     # print(框架.请求.参数集json._内嵌对象["name"])
    #     # resp = 响应(json.dumps(result), 类型='application/json')
    #     # resp.响应头.键值对新增('Server', 'python flask11')
    #     # resp = 响应(json.dumps(result), 类型='application/json')
    #     # resp = 响应(result, 类型='json')._内嵌对象
    #     return "/register"
    #
    #
    # @框架.路由("/uploads", 请求方法=['POST'])
    # def uploads():
    #     def allowed_file(filename):
    #         return '.' in filename and filename.rsplit('.', 1)[1] in 框架.配置[
    #             '上传允许拓展名']
    #
    #     上传文件 = 框架.请求.参数集files['image']
    #     if 上传文件 and allowed_file(上传文件.文件名):  # 上传前文件在客户端的文件名
    #         安全文件名 = secure_filename(上传文件.文件名)
    #         # 将文件保存到 static/uploads 目录，文件名同上传时使用的文件名
    #         上传文件.保存(os.path.join(框架.根路径, 框架.配置['上传路径'], 安全文件名))
    #         return 'info is ' + 框架.请求.参数集postData.获取参数值_第一个('info') + '. success'
    #     else:
    #         return 'failed'
    #
    #
    # @框架.路由("/uploads", 请求方法=['GET'])
    # def uploads1():
    #     return "/register"
    #
    #
    # @框架.路由('/user/<username>')
    # def user(username):
    #     print(username)
    #     print(type(username))
    #     return 'hello ' + username
    #
    #
    # @框架.路由('/old')
    # def old():
    #     print('this is old')
    #     return 框架.响应.响应输出_重定向('https://www.baidu.com')
    #
    #
    # @框架.路由('/new')
    # def new():
    #     print('this is new')
    #     return 'this is new'
    #
    #
    # @框架.路由('/user')
    # def userinfo():
    #     user_info = {
    #         'name': 'loen',
    #         'email': '425389019@qq.com',
    #         'age': 0,
    #         'github': 'https://github.com/lucoo01'
    #     }
    #     return 框架.响应.响应输出_渲染网页_通过模板('default.html',
    #                                 page_title="loen's info", user_info=user_info)
    #
    #
    # @框架.路由('/user1')
    # def user1():
    #     return 框架.响应.响应输出_错误(401)
    #
    #
    # @框架.路由('/login')
    # def login():
    #     page = '''
    #     <form action="{{ url_for('do_login') }}" method="post">
    #         <p>name: <input type="text" name="user_name" /></p>
    #         <input type="submit" value="Submit" />
    #     </form>
    #     '''
    #     return 框架.响应.响应输出_渲染网页_通过字符串(page)
    #
    #
    # @框架.路由('/do_login', 请求方法=['POST'])
    # def do_login():
    #     name = 框架.请求.参数集postData.获取参数值_第一个('user_name')
    #     框架.会话.会话新增('user_name', name)
    #     框架.配置.会话参数 = True
    #     return 'success'
    #
    #
    # @框架.路由('/show')
    # def show():
    #     return 框架.会话._内嵌对象session
    #
    #
    # @框架.路由('/logout')
    # def logout():
    #     框架.会话.会话删除('user_name')
    #     return 框架.响应.响应输出_重定向('/login')
    #
    #
    # @框架.路由('/addcookies')
    # def addcookies():
    #     框架.响应.响应修改('add cookies')
    #     框架.响应.本地cookies设置('name3', 'loen')
    #     return 框架.响应.响应输出_常规()
    #
    #
    # @框架.路由('/showcookies')
    # def showcookies():
    #     return 框架.请求.本地cookies.__str__()
    #
    #
    # @框架.路由('/delcookies')
    # def delcookies():
    #     框架.响应.响应修改('delete cookies')
    #     框架.响应.本地cookies删除('name3')
    #     return 框架.响应.响应输出_常规()
    #
    #
    # @框架.路由('/gen')
    # def gen():
    #     info = 'access at ' + time.time().__str__()
    #     框架.会话.闪存新增("show1 " + info, 标签="show1")
    #     框架.会话.闪存新增("show2 " + info, 标签="show2")
    #     框架.响应.响应修改(info)
    #     return 框架.响应.响应输出_常规()
    #
    #
    # @框架.路由('/show1')
    # def show1():
    #     框架.响应.响应修改(框架.会话.闪存获取(标签过滤="show1").__str__())
    #     return 框架.响应.响应输出_常规()
    #
    #
    # @框架.路由('/show2')
    # def show2():
    #     框架.响应.响应修改(框架.会话.闪存获取(标签过滤="show2").__str__())
    #     return 框架.响应.响应输出_常规()
    #
    #
    # 框架.运行(调试模式=True)
    # app = Flask("app")
    # app.route
    pass
