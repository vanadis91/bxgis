class 字段类:
    def __init__(self, 内嵌对象) -> None:
        self.内嵌对象 = 内嵌对象
        self.名称 = self.内嵌对象.name
        self.类型 = self.内嵌对象.type
        self.长度 = self.内嵌对象.length

    def __repr__(self) -> str:
        return f"<对象 bxarcpy.字段类 {{名称:{self.名称}, 类型:{self.类型}, 长度:{self.长度}}}>"