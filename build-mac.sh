#!/bin/bash
set -e
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
if [ ! -d .venv ]; then
  "$PYTHON" -m venv .venv
fi
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install pyinstaller
rm -rf build dist
pyinstaller --windowed --name "LocalSecureSheet" --clean app.py
echo "已生成：$(pwd)/dist/LocalSecureSheet.app"
