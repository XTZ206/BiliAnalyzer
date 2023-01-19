./venv/Scripts/activate
Remove-Item .\dist\BiliAnalyzer -Recurse -Force
pyinstaller -D .\bilianalyzer\main.py -i .\bilianalyzer\icon\main.ico -n BiliAnalyzer -w

# 资源文件夹不存在时创建对应资源文件夹
if ((Test-Path -Path .\dist\BiliAnalyzer\icon) -eq $false)
{
    mkdir -Path .\dist\BiliAnalyzer\icon
}
Copy-Item -Path .\bilianalyzer\icon\* -Destination .\dist\BiliAnalyzer\icon -Force

if ((Test-Path -Path .\dist\BiliAnalyzer\docs) -eq $false)
{
    mkdir -Path .\dist\BiliAnalyzer\docs
}
Copy-Item -Path .\bilianalyzer\docs\* -Destination .\dist\BiliAnalyzer\docs -Force