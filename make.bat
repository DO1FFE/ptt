@echo off
set "ROOT=%~dp0"
pyinstaller --noconfirm --onefile --windowed --icon "%ROOT%pics\ptt.ico" --name "PTT" --add-data "%ROOT%pics\ptt.png;pics" "%ROOT%main.py"
