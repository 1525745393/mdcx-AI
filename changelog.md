## 220260527 (2026-05-23)

### 修复
- 修复 save_config.py 第 375 行 IndentationError 错误
- 确保代码缩进正确，符合 Python 语法规范

## 220260526 (2026-05-23)

### 修复
- 重新编译 UI 文件，修复 AttributeError: 'Ui_MDCx' object has no attribute 'checkBox_download_vsmeta' 错误
- 确保所有 VSMETA 相关 UI 控件正确绑定

## 220260525 (2026-05-22)

### 新增
- 修复 PyInstaller 打包配置，确保所有模块正确包含在安装包中

### 修复
- 修复安装包运行时 ModuleNotFoundError 错误
