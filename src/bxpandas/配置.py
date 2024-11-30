import pandas


class _配置:
    def __init__(self) -> None:
        pandas.set_option("display.max_columns", 100)  # 最大列数
        pandas.set_option("display.width", 1000)  # 最多显示多少字符
        pandas.set_option("display.expand_frame_repr", False)  # 不换行
        pandas.set_option("display.colheader_justify", "left")  # 数据对齐方式
        pandas.set_option("display.unicode.ambiguous_as_wide", True)  # 中文对齐
        pandas.set_option("display.unicode.east_asian_width", True)  # 中文对齐
        pandas.set_option("display.max_colwidth", 100)

        self.数据读取顺序映射 = {"先行后列": "C", "C": "C", "先列后行": "F", "F": "F", "以内存中连续存储的方式": "A", "A": "A", "以内存中出现的顺序": "K", "K": "K"}
        self.空值填充映射 = {"左值填充": "ffill", "右值填充": "bfill", "上值填充": "ffill", "下值填充": "bfill"}


class 枚举_字典结构:
    分割 = "split"
    SPLIT = "split"
    分割_三个键值_行标签列表_列标签列表_数据 = "split"
    # {'index':[row1,...],'columns':[col1,...],'data':[[x1,x2,...],...]}
    记录 = "records"
    RECORDS = "records"
    JSON = "records"
    记录_字典列表_每个字典的键为列标签 = "records"
    # [{'col1':x1,'col2':x2,...},{'col1':x3,'col2':x4,...},...]
    按索引 = "index"
    INDEX = "index"
    按索引_一级键是行标签_二级键是列标签 = "index"
    # {'row1':{'col1':x1,'col2':x2,...},'row2':{'col1':x2,'col2':x3,...},...}
    按列 = "columns"
    COLUMNS = "columns"
    按列_一级键是列标签_二级键是行标签 = "columns"
    # {'col1':{'row1':x1,'row2':x3,...},'col2':{'row1':x2,'row2':x4,...},...}
    仅值 = "values"
    VALUES = "values"
    仅值_没有行标签和列标签 = "values"
    # [[x1,x2,...],[x3,x4,...],...]
    含结构表 = "table"
    TABLE = "table"


配置 = _配置()
