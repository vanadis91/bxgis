# bxgis工具箱

## 简介

一个近期用于实现杭州详规入库数据库构建，远期用于协助国土空间规划编制的包。

## 使用说明

当前项目处于**极其**初级的阶段，**不建议用于生产环境，切记，切记，切记**，之所以发布，主要是个人时间有限，希望有经验丰富的人能够来继续进行完善。

### 1. 环境构建

- 克隆默认Python运行环境（arcgispro-py3）。代码运行基于ArcGISPro。在ArcGISPro的**工程/包管理器**菜单中，通过**环境管理器**按钮来克隆默认Python运行环境（arcgispro-py3）。不建议修改ArcGISPro默认Python环境（arcgispro-py3），直接修改可能会导致意想不到的后果，建议仅修改克隆环境。
- 将**src**目录下的**bxgis**包复制到克隆的环境的site-packages文件夹。
- 在ArcGISPro的**工程/包管理器**菜单中，通过**环境管理器**将当前ArcGISPro的活动环境切换为克隆的环境。
- 重启ArcGISPro后，bxgis工具箱将会出现在**地理处理**窗格中。

### 2. 修改配置文件

- 修改**bxgis/config/配置.py**文件中的内容。主要包括对项目基本信息的录入，一些要素的字段名称映射的录入。

### 3. 完成要素的输入

- 可通过**bxgis/常用/导入从CAD**从CAD导入要素，该工具支持拓扑检查，曲线转折线等功能。
- 完成**规划范围线、街坊范围线、街区范围线、分村范围线、工业片区范围线**等**区域要素**的输入。
- 完成**三调**字段的汉化，并完成**扣除地类系数、种植属性名称、城镇村属性码、坐落单位名称**等**参照要素**的输入。通过**arcgis/用地/基期/字段处理并生成分项**可以完成上述的工作。
- 完成**基期用地**的生成。可以通过**bxgis/用地/基期/初步基数转换**等工具来协助基数转换。
- 完成**永久基本农田、生态保护红线、城镇集建区、城镇弹性区**等**控制线要素**的输入。
- 完成**现状用地**的生成。通过**bxgis/用地/用地现状图生成**可以叠合生成用地现状图，同时可以进行拓扑检查和范围检查。
- 完成**规划用地**的生成。通过**bxgis/用地/用地规划图生成**可以叠合生成用地规划图，处理好CAD中图斑和GIS中图斑的关系，并且可以进行细小面的检查、拓扑检查和范围检查。
- 完成**规划设施**的输入。
- 完成**规划用途分区**的生成。通过**bxgis/分区/用途分区规划图生成**可以叠合生成用途分区规划图。
- 对**规划用地**进行更新。通过**bxgis/用地/用地更新**可以对用地内各字段进行自动计算。
- 对**规划设施**进行更新。通过**bxgis/设施/设施更新**可以对设施内各字段进行自动计算。
- 对**街区、街坊、分村**进行更新。通过**bxgis/区域/区域更新**可以对区域内各字段进行自动计算。

### 4. 自动生成入库文件

- 通过**bxgis/入库**中的各个工具，可以生成符合入库规范要求的相关要素。

## 开发说明

### 项目结构

当前的目录结构采用的是ESRI网站上**创建地理处理模块**页面中的结构。
<https://pro.arcgis.com/zh-cn/pro-app/latest/arcpy/geoprocessing_and_python/extending-geoprocessing-through-python-modules.htm>

### 环境构建

123
