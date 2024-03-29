./venv/Scripts/activate

pyside6-uic.exe ./bilianalyzer/ui/main.ui -o ./bilianalyzer/ui/ui_main.py
pyside6-uic.exe ./bilianalyzer/ui/config.ui -o ./bilianalyzer/ui/ui_config.py
pyside6-uic.exe ./bilianalyzer/ui/about.ui -o ./bilianalyzer/ui/ui_about.py
pyside6-uic.exe ./bilianalyzer/ui/tutorial.ui -o ./bilianalyzer/ui/ui_tutorial.py

python ./scripts/relocate.py ./bilianalyzer/ui/ui_main.py
python ./scripts/relocate.py ./bilianalyzer/ui/ui_config.py
python ./scripts/relocate.py ./bilianalyzer/ui/ui_about.py
python ./scripts/relocate.py ./bilianalyzer/ui/ui_tutorial.py

Write-Output "Task Complete!"