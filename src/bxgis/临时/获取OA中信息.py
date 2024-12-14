# *-* coding:utf8 *-*
def 获取OA系统中控规信息():
    from bxpy.网络会话包 import 会话类, 会话配置类

    请求头 = {
        "Cookie": "sys-auth=MzI5YWE4ODMtNWQ3Mi00MGY1LWE2OWEtZGZjOGEyMTAyZjY0; ASP.NET_SessionId=t1cqcqvrfxhrmdfbgw1l3vo4; ASP.NET_SessionId=n2imrz2idgyjyqhpmhmpotlt",
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Host": "gdbh.hzsgis.com:18455",
        "Connection": "keep-alive",
    }
    构造表单数据1 = {
        "f": "json",
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "geometry": '{"spatialReference":{"wkid":4490},"rings":[[[120.18563687328779,30.34299495435778],[120.18564590309589,30.342994269146942],[120.18565465853746,30.342992234334243],[120.18566287358252,30.342988911746517]]]}',
        "spatialRel": "esriSpatialRelIntersects",
        "geometryType": "esriGeometryPolygon",
    }
    响应 = 会话类.会话创建("https://gdbh.hzsgis.com:18455/server3/34d664a4d3407b4c18ba3e8b3b66373945ec/ArcGIS/MapService/Catalog/HZGIS2000.KG_GHDK_WBZ.gis/query", 方式="post", 数据_form=构造表单数据1, 请求头=请求头)
    print(f"{会话类.响应类.属性获取_内容(响应)}")


if __name__ == "__main__":
    获取OA系统中控规信息()
