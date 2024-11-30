from bxpy.基本对象包 import 模块加载
from typing import Union, Literal, Any

# class _配置:
#     def __init__(self) -> None:
#         self.设置 = webdriver.ChromeOptions()
# 当前文件内需加载的包 from browsermobproxy import Server

# chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
# chrome_options.add_argument('--proxy-server=' + 代理sl.proxy)
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--headless')

# self.请求头 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (" "KHTML, like Gecko) Chrome/78.0.3904.108 " "Safari/537.36"}
# self.设置.add_argument(r"user-data-dir=C:\Users\beixiao\AppData\Local\Google\Chrome\User Data")
# 设置.add_experimental_option("w3c", False)
# 功能 = {
#     "browserName": "chrome",
#     "loggingPrefs": {
#         "browser": "ALL",
#         "driver": "ALL",
#         "performance": "ALL",
#     },
#     "goog:chromeOptions": {
#         "perfLoggingPrefs": {
#             "enableNetwork": True,
#         },
#         "w3c": False,
#     },
# }
# self.功能 = {
#     "browserName": "chrome",
#     "loggingPrefs": {
#         "browser": "ALL",
#         "driver": "ALL",
#         "performance": "ALL",
#     },
#     "goog:chromeOptions": {
#         "perfLoggingPrefs": {
#             "enableNetwork": True,
#         },
#     },
# }

# def 设置修改(self, *参):
#     self.设置.add_argument(*参)


# 配置 = _配置()


# class 浏览器抓包服务:
#     def __init__(self):
#         from browsermobproxy import Server

#         抓包服务xc = Server(r"C:\Program Files\browsermob-proxy\2.1.5\bin\browsermob-proxy.bat")
#         self.嵌入对象Server = 抓包服务xc

#     def 启动服务(self):
#         self.嵌入对象Server.start()

#     def 创建代理(self):
#         代理xc = self.嵌入对象Server.create_proxy()
#         return _浏览器代理(代理xc)

#     def 关闭服务(self):
#         self.嵌入对象Server.stop()


# class _浏览器代理:
#     def __init__(self, 嵌入对象):
#         self.嵌入对象Proxy = 嵌入对象
#         self.HAR文件 = None
#         self.代理信息 = self.嵌入对象Proxy.proxy

#     def 创建HAR文件(self, *值, **参):
#         self.嵌入对象Proxy.new_har(*值, **参)
#         self.HAR文件 = self.嵌入对象Proxy.har


class 浏览器类:
    @staticmethod
    def 浏览器创建(不显示界面=True, 非沙盒模式=False, 用户数据路径=None):
        模块加载("webdriver_manager")
        from webdriver_manager.chrome import ChromeDriverManager

        driver_path = ChromeDriverManager().install()
        # print(driver_path)
        模块加载("selenium")
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service

        service = Service(driver_path)
        print(f"chromedriver的路径为: {driver_path}")
        options = webdriver.ChromeOptions()
        if 不显示界面:
            options.add_argument("--headless")
        if 非沙盒模式:
            options.add_argument("--no-sandbox")  # 让Chrome在root权限下跑
        if 用户数据路径:
            options.add_argument(f"user-data-dir={用户数据路径}")
            # (r"user-data-dir=C:\Users\beixiao\AppData\Local\Google\Chrome\User Data")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=service, options=options)  # type: ignore

    @staticmethod
    def 网页打开(浏览器对象xc, 网址):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        浏览器对象.get(网址)
        浏览器对象.refresh()
        return 浏览器对象

    class 网页类:
        @staticmethod
        def 属性获取_内容(浏览器对象xc):
            from selenium import webdriver

            浏览器对象: webdriver.Chrome = 浏览器对象xc
            # 文档对象类.文档对象创建(self._内嵌对象WebDriver.page_source)._内嵌对象
            return 浏览器对象.page_source

        @staticmethod
        def 属性获取_内容_节点webdriver(浏览器对象xc):
            from selenium import webdriver

            浏览器对象: webdriver.Chrome = 浏览器对象xc
            # 文档对象类.文档对象创建(self._内嵌对象WebDriver.page_source)._内嵌对象
            return 浏览器对象

        class 节点类webdriver:
            @staticmethod
            def 节点获取_通过XPATH(浏览器对象xc, *列表, **字典):
                from selenium import webdriver

                浏览器对象: webdriver.Chrome = 浏览器对象xc
                模块加载("lxml")
                from lxml import html
                from selenium.webdriver.common.by import By

                etree = html.etree
                return 浏览器对象.find_elements(By.XPATH, *列表, **字典)

            @staticmethod
            def 节点获取_通过CLASS(浏览器对象xc, *列表, **字典):
                from selenium import webdriver

                浏览器对象: webdriver.Chrome = 浏览器对象xc
                from selenium.webdriver.common.by import By

                return 浏览器对象.find_elements(By.CLASS_NAME, *列表, **字典)

            @staticmethod
            def 节点获取_通过ID(浏览器对象xc, *列表, **字典):
                from selenium import webdriver

                浏览器对象: webdriver.Chrome = 浏览器对象xc
                from selenium.webdriver.common.by import By

                return 浏览器对象.find_elements(By.ID, *列表, **字典)

            @staticmethod
            def 属性获取_内容(标签对象):
                return 标签对象.text

            @staticmethod
            def 属性获取_类型(标签对象):
                return 标签对象.tag_name

            @staticmethod
            def 属性获取_节点属性(标签对象, 键):
                return 标签对象.get_attribute(键)

            @staticmethod
            def 互动_写入(标签对象, *列表):
                return 标签对象.send_keys(*列表)

            @staticmethod
            def 互动_单击(标签对象):
                return 标签对象.click()

            @staticmethod
            def 互动_清空(标签对象):
                return 标签对象.clear()

    @staticmethod
    def 浏览器关闭(浏览器对象xc):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.close()

    @staticmethod
    def 执行js代码(浏览器对象xc, 值):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.execute_script(值)

    @staticmethod
    def 操作_前进(浏览器对象xc):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.forward()

    @staticmethod
    def 操作_后退(浏览器对象xc):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.back()

    @staticmethod
    def 操作_刷新(浏览器对象xc):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.refresh()

    @staticmethod
    def 操作_标签页新建(浏览器对象xc):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.execute_script("window.open()")

    @staticmethod
    def 操作_标签页切换(浏览器对象xc, 序号):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.switch_to.window(浏览器对象.window_handles[序号])

    @staticmethod
    def 获取日志(浏览器对象xc, 值):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.get_log(值)

    @staticmethod
    def 增加临时存储Cookie(浏览器对象xc, 值):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        # 浏览器sl.嵌入对象selenium.add_cookie(dict(name='p_uin', value='o0570367169'))
        return 浏览器对象.add_cookie(值)

    @staticmethod
    def 保存截图(浏览器对象xc, 值):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.save_screenshot(值)

    @staticmethod
    def 框架切换(浏览器对象xc, *列表, **字典):
        from selenium import webdriver

        浏览器对象: webdriver.Chrome = 浏览器对象xc
        return 浏览器对象.switch_to.frame(*列表, **字典)


class 会话配置类:
    请求头 = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (" "KHTML, like Gecko) Chrome/78.0.3904.108 " "Safari/537.36',
    }


class 会话类:

    @staticmethod
    def 会话创建(
        网址="",
        方式="get",
        数据_args=None,
        数据_json=None,
        数据_form=None,
        数据_files=None,
        临时存储cookies=None,
        请求头=会话配置类.请求头,
        流模式=False,
    ):
        模块加载("requests")
        import requests

        if 方式 == "get":
            return requests.get(url=网址, headers=请求头, params=数据_args, cookies=临时存储cookies, stream=流模式)
        elif 方式 == "post" and 数据_form and 数据_files:
            return requests.post(url=网址, headers=请求头, params=数据_args, data=数据_form, files=数据_files, cookies=临时存储cookies, stream=流模式)
        elif 方式 == "post" and 数据_json and 数据_files:
            return requests.post(url=网址, headers=请求头, params=数据_args, json=数据_json, files=数据_files, cookies=临时存储cookies, stream=流模式)
        elif 方式 == "post" and 数据_json:
            return requests.post(url=网址, headers=请求头, params=数据_args, json=数据_json, cookies=临时存储cookies, stream=流模式)
        elif 方式 == "post" and 数据_form:
            return requests.post(url=网址, headers=请求头, params=数据_args, data=数据_form, cookies=临时存储cookies, stream=流模式)
        elif 方式 == "post" and 数据_files:
            return requests.post(url=网址, headers=请求头, params=数据_args, files=数据_files, cookies=临时存储cookies, stream=流模式)
        elif 方式 == "delete":
            return requests.delete(url=网址, headers=请求头, params=数据_args, cookies=临时存储cookies, stream=流模式)

    class 响应类:
        @staticmethod
        def 属性获取_编码方式(响应):
            return 响应.encoding

        @staticmethod
        def 属性获取_编码方式_根据内容猜测(响应):
            return 响应.apparent_encoding

        @staticmethod
        def 属性获取_响应头(响应):
            return 响应.headers

        @staticmethod
        def 属性获取_状态码(响应):
            return 响应.status_code

        @staticmethod
        def 属性获取_临时存储cookies(响应):
            # -> Union["cookies.RequestsCookieJar", None]
            # from requests import cookies

            return 响应.cookies

        @staticmethod
        def 属性获取_内容(响应, 编码格式="utf-8"):
            # self._内嵌对象WebDriver.page_source
            return 响应.content.decode(编码格式)

        @staticmethod
        def 属性获取_内容_字节流(响应):
            return 响应.content

        @staticmethod
        def 属性获取_内容_节点bs4(响应, 编码格式="utf-8"):
            # 文档对象类.文档对象创建(self._内嵌对象WebDriver.page_source)._内嵌对象
            return 会话类.响应类.节点类bs4.节点解析(响应.content.decode(编码格式))

        @staticmethod
        def 属性获取_内容_节点etree(响应, 编码格式="utf-8"):
            # 文档对象类.文档对象创建(self._内嵌对象WebDriver.page_source)._内嵌对象
            return 会话类.响应类.节点类etree.节点解析(响应.content.decode(编码格式))

        @staticmethod
        def 属性获取_内容_json(响应):
            return 响应.json()

        @staticmethod
        def 属性获取_网址(响应):
            # self._内嵌对象WebDriver.current_url
            return 响应.url

        @staticmethod
        def 属性获取_标题(响应):
            # self._内嵌对象WebDriver.current_url
            return 响应.title

        class 节点类bs4:
            @staticmethod
            def 节点解析(html字符串, 解析格式: Literal["html", "xml"] = "html"):
                模块加载("bs4", "beautifulsoup4")
                from bs4 import BeautifulSoup

                解析格式映射 = {"html": "html.parser", "xml": "xml"}
                解析格式raw = 解析格式映射[解析格式] if 解析格式 in 解析格式映射 else 解析格式
                ret = BeautifulSoup(html字符串, 解析格式raw)
                return ret

            @staticmethod
            def 输出格式化后字符串(标签对象xc):
                from bs4 import BeautifulSoup

                标签对象: BeautifulSoup = 标签对象xc
                return 标签对象.prettify()

            @staticmethod
            def 子节点获取_单个(标签对象xc, 标签名称):
                from bs4 import BeautifulSoup

                标签对象: BeautifulSoup = 标签对象xc
                return 标签对象.find(name=标签名称)

            @staticmethod
            def 子节点获取_多个(标签对象xc, 标签名称):
                from bs4 import BeautifulSoup

                标签对象: BeautifulSoup = 标签对象xc
                return 标签对象.find_all(name=标签名称)

            @staticmethod
            def 属性获取_类型(标签对象xc):
                from bs4 import BeautifulSoup

                标签对象: BeautifulSoup = 标签对象xc
                return 标签对象.name

            @staticmethod
            def 属性获取_所有节点属性(标签对象xc):
                from bs4 import BeautifulSoup

                标签对象: BeautifulSoup = 标签对象xc
                return 标签对象.attrs

            @staticmethod
            def 属性获取_内容(标签对象xc):
                from bs4 import BeautifulSoup

                标签对象: BeautifulSoup = 标签对象xc
                return 标签对象.string

        class 节点类etree:
            @staticmethod
            def 节点解析(html字符串):
                from lxml import html

                etree = html.etree

                return etree.HTML(html字符串, None)

            @staticmethod
            def 子节点获取_多个_按xpath(标签对象, *列表, **字典):
                return 标签对象.xpath(*列表, **字典)
                # elif self._内嵌对象WebDriver is not None:
                #     网页元素列表xc = self._内嵌对象WebDriver.find_elements(By.XPATH, *列表, **字典)
                #     return list(map(lambda x: 会话类.内容元素(x), 网页元素列表xc))

            @staticmethod
            def 属性获取_内容(标签对象):
                return 标签对象.text

            @staticmethod
            def 属性获取_类型(标签对象):
                return 标签对象.tag

            @staticmethod
            def 属性获取_所有节点属性(标签对象):
                return 标签对象.attrib

            @staticmethod
            def 属性获取_节点属性(标签对象, 键):
                return 标签对象.attrib[键]


if __name__ == "__main__":
    # aa = 获取方式生成网页实例("http://planning.hangzhou.gov.cn/index.aspx?tabid
    # =07c0f0db-9512-42f7-bf32-ce460a52e870") print(aa.xpath提取("//tr[2]/td[
    # 1]/a/text()")) 接收消息()
    # url1 = "https://movie.douban.com/chart"
    # url2 = "http://ghzy.hangzhou.gov.cn/col/col1228968049/index.html"
    # 浏览器sl = 生成浏览器实例()
    # 浏览器sl.生成网页实例(url1)
    # 常用.时间_等待(5)
    # 浏览器sl.生成网页实例(url2)
    # 网页元素sl = 网页sl.按xpath提取('''//a''')
    # 常用.打印详情(网页元素sl)
    # 常用.打印详情(a.嵌入对象WebElement)
    # 常用.打印详情(a.嵌入对象WebElement.value_of_css_property)
    # 常用.打印详情(a.嵌入对象WebElement.id)
    # 浏览器sl.关闭浏览器()
    # 常用.打印详情(网页sl.源代码)
    # 常用.打印详情(etree.tostring(网页sl.嵌入对象etree))
    pass
