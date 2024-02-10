cd C:\Users\beixiao\Project\bxpy
"C:\Program Files\Python39\Scripts\pyarmor.exe" gen -O ..\bxgis\src\bxgis\common bxpy
cd C:\Users\beixiao\Project\bxgeo
"C:\Program Files\Python39\Scripts\pyarmor.exe" gen -O ..\bxgis\src\bxgis\common bxgeo
cd C:\Users\beixiao\Project\bxpandas
"C:\Program Files\Python39\Scripts\pyarmor.exe" gen -O ..\bxgis\src\bxgis\common bxpandas
"C:\Users\beixiao\Project\bxgis\.condavenv\arcgispro-py3-clone\python.exe" -c "import arcpy; arcpy.gp.createtoolboxsupportfiles(r'C:\Users\beixiao\Project\bxgis\src\bxgis\bxgis.pyt')"

cd C:\Users\beixiao\Project\bxgis\src\bxgis
set source_file1="bxgis.pyt"
set destination_folder1="esri\toolboxes"
copy %source_file1% %destination_folder1%

set source_file2="bxgis.ExportToCAD.pyt.xml"
set destination_folder2="esri\toolboxes"
move %source_file2% %destination_folder2%

set source_file3="bxgis.pyt.xml"
set destination_folder3="esri\toolboxes"
move %source_file3% %destination_folder3%