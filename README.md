# 本地安全表格工具

## 安装
```bash
python3 -m pip install -r requirements.txt
```

## 使用
图形界面：
```bash
python3 app.py
```

## 打包
macOS：双击或执行 `build-mac.sh`，产物在 `dist/LocalSecureSheet.app`。
Windows：双击 `build-windows.bat`，产物在 `dist/LocalSecureSheet/LocalSecureSheet.exe`。

命令行：
```bash
python3 secure_sheet.py encrypt 原始.xlsx 加密.xlsx 手机号,身份证号 "双方约定的密码"
python3 secure_sheet.py decrypt 加密.xlsx 还原.xlsx 手机号,身份证号 "双方约定的密码"
```

算法为 AES-256-GCM，密码通过 PBKDF2-HMAC-SHA256 派生。数据只在本机处理。
