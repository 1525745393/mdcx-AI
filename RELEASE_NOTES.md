# MDCx 220260523 发布说明

## 🚀 新功能

### 1. 项目 Code Wiki 文档
- 完整的项目架构说明
- 核心模块职责分析
- 数据模型文档
- 开发指南
- 快速上手指南

### 2. VSMETA 配置界面
- 新增 VSMETA 配置选项到设置界面
- 支持配置 VSMETA 文件命名格式
- 用户友好的界面交互

### 3. 群晖 Video Station VSMETA 元数据生成
- **完整支持 VSMETA 格式**：自动生成符合群晖 Video Station 规范的元数据文件
- **图片嵌入**：支持将海报和背景图嵌入 VSMETA 文件
- **完整元数据**：包含标题、简介、演员、导演、标签、评分、发布日期、片长等字段

### 2. VSMETA 配置选项
- **命名格式选择**：可配置是否保留视频文件扩展名
  - 不保留扩展名（默认）：`SDDE-123.vsmeta`
  - 保留扩展名：`SDDE-123.mp4.vsmeta`

### 3. 项目 Code Wiki 文档
- 完整的项目架构说明
- 核心模块职责分析
- 数据模型文档
- 开发指南

## 🔧 改进与优化

### Amazon 海报增强
- 新增海报候选尺寸预检查选项
- 优化海报候选来源优先级
- 减少低优先级来源覆盖更合适候选的情况

### 命名模板改进
- 完善命名模板字段说明
- 保留 four_k 作为 4K/8K/UHD 标识字段
- 优化超长截断与清洗逻辑
- 更好地保留番号等关键字段

### 人脸裁剪优化
- 增强旋转检测能力
- 提升旋转画面下的裁剪准确性

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
