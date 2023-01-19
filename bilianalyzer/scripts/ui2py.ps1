.\venv\Scripts\activate

pyside6-uic.exe .\bilianalyzer\ui\main_window.ui -o .\bilianalyzer\ui\ui_main.py
pyside6-uic.exe .\bilianalyzer\ui\config_window.ui -o .\bilianalyzer\ui\ui_config.py
pyside6-uic.exe .\bilianalyzer\ui\about_window.ui -o .\bilianalyzer\ui\ui_about.py
pyside6-uic.exe .\bilianalyzer\ui\tutorial_window.ui -o .\bilianalyzer\ui\ui_tutorial.py

python .\bilianalyzer\scripts\relocate.py .\bilianalyzer\ui\ui_main.py
python .\bilianalyzer\scripts\relocate.py .\bilianalyzer\ui\ui_config.py
python .\bilianalyzer\scripts\relocate.py .\bilianalyzer\ui\ui_about.py
python .\bilianalyzer\scripts\relocate.py .\bilianalyzer\ui\ui_tutorial.py

Write-Output "Task Complete!"