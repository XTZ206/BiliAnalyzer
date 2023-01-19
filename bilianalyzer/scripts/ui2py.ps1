Set-Location D:\Repositories\BiliAnalyzer\bilianalyzer
pyside6-uic.exe .\ui\main_window.ui -o .\ui\ui_main.py
pyside6-uic.exe .\ui\config_window.ui -o .\ui\ui_config.py
pyside6-uic.exe .\ui\about_window.ui -o .\ui\ui_about.py
pyside6-uic.exe .\ui\tutorial_window.ui -o .\ui\ui_tutorial.py
python .\scripts\relocate.py .\ui\ui_main.py
python .\scripts\relocate.py .\ui\ui_config.py
python .\scripts\relocate.py .\ui\ui_about.py
python .\scripts\relocate.py .\ui\ui_tutorial.py
Write-Output "Task Complete!"