@echo off
cd /d "%~dp0"
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m pip install pyinstaller
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller --windowed --name "LocalSecureSheet" --clean app.py
echo 已生成：dist\LocalSecureSheet\LocalSecureSheet.exe
pause
