# MDCx 220260525 发布说明

## 🐛 Bug 修复

### 修复打包问题 (更彻底的修复)
- 使用 `--collect-all mdcx` 确保整个 mdcx 包被完整包含在安装包中
- 修复安装包运行时 ModuleNotFoundError 错误
- 确保 `mdcx.controllers.main_window.save_config` 等所有模块正确导入

## 📋 文件变更

### 新增文件
- `mdcx/core/vsmeta.py` - VSMETA 核心生成模块
- `CODE_WIKI.md` - 项目完整文档

### 修改文件
- `mdcx/config/enums.py` - 添加 VSMETA 枚举
- `mdcx/config/models.py` - 添加 VSMETA 配置项
- `mdcx/core/scraper.py` - 集成 VSMETA 功能
- `mdcx/core/file.py` - VSMETA 文件处理
- `mdcx/controllers/main_window/load_config.py` - VSMETA 配置加载
- `mdcx/controllers/main_window/save_config.py` - VSMETA 配置保存
- `mdcx/views/MDCx.ui` - VSMETA 配置界面
- `mdcx/consts.py` - 版本号更新
- `changelog.md` - 更新日志
- `RELEASE_NOTES.md` - 发布说明

## 📦 安装与使用

### 下载安装包
请从 GitHub Release 下载对应平台的安装包：
- **Windows**: `.exe` 文件
- **macOS**: `.dmg` 文件

### VSMETA 功能使用
1. 打开 MDCx 设置
2. 在「下载文件类型」中勾选「VSMETA」
3. 如需修改 VSMETA 命名格式，可在设置中调整「VSMETA保留视频扩展名」选项
4. 进行刮削时，会自动在输出目录生成对应的 .vsmeta 文件

## 📝 完整变更日志

参见项目目录下的 `changelog.md` 文件。

## 🙌 致谢

感谢所有贡献者！

---

发布日期: 2026-05-22
