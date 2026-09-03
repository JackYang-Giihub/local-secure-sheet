# 本地安全表格工具｜Intel Mac 使用手册

本工具在本机处理 Excel/CSV 文件，不会上传文件。适用于 Intel 芯片 Mac。

## 一、准备 Python

打开“终端”，先确认芯片类型：

```bash
uname -m
```

如果显示 `x86_64`，就是 Intel Mac。

如果电脑没有 Homebrew，先安装：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装 Python 和 Tk 图形库：

```bash
brew install python@3.12 python-tk@3.12
```

确认 Python 版本：

```bash
python3 --version
```

建议使用 Python 3.11 或 3.12。

## 二、安装工具

将收到的 `local-secure-sheet` 文件夹放到“下载”目录，然后执行：

```bash
cd ~/Downloads/local-secure-sheet
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

看到没有红色错误后，说明安装完成。

## 三、启动工具

每次使用前执行：

```bash
cd ~/Downloads/local-secure-sheet
source .venv/bin/activate
python app.py
```

关闭窗口即可退出。

## 四、加密文件

1. 点击“选择文件”。
2. 选择 Excel 或 CSV 文件。
3. 勾选需要加密的列，例如“手机号”。
4. 输入至少 8 位密码。
5. 点击“加密并导出”。

程序会生成：

```text
原文件名_加密.xlsx
原文件名_加密.xlsx.meta.json
```

发送给对方时，这两个文件必须一起发送。密码请通过其他方式单独告知，不要和文件放在同一条消息里。

## 五、解密文件

1. 确认加密文件和同名 `.meta.json` 文件在同一个文件夹。
2. 点击“选择文件”，选择加密后的 Excel 文件。
3. 勾选与加密时相同的列。
4. 输入完全相同的密码。
5. 点击“解密并导出”。

程序会生成带有 `_解密` 的还原文件。

## 六、常见问题

### 提示找不到 cryptography 或 openpyxl

确认终端前面有 `(.venv)`，然后重新执行：

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 提示无法验证开发者

本项目是本地脚本，不是经过 Apple 公证的商业软件。右键 `app.py` 或工具文件夹，选择“打开”；或者在“系统设置 → 隐私与安全性”中允许打开。

### 解密失败

请检查：

- 密码是否完全一致，注意大小写和空格。
- `.meta.json` 是否与加密文件来自同一次加密。
- 解密时是否选择了正确的列。

### 文件很大，处理时间较长

工具会在本机逐行处理，文件越大耗时越长。处理期间不要关闭窗口。

## 七、安全提醒

- 忘记密码后无法恢复明文。
- 不要把密码写进文件名或发送在同一条消息中。
- 不要发送 `.venv`、`build` 或 `dist` 文件夹；代码和 `requirements.txt` 即可。
- 使用前建议先用几行测试数据验证加密和解密流程。
