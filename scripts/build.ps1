.\venv\Scripts\activate
Remove-Item .\dist\BiliAnalyzer -Recurse -Force
pyinstaller .\BiliAnalyzer.spec

# 打包为压缩包
7z a .\dist\BiliAnalyzer-windows.zip .\dist\BiliAnalyzer\
Copy-Item -Path .\dist\BiliAnalyzer-windows.zip -Destination .\releases\ -Force

Write-Output "Build Complete!"