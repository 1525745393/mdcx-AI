# MDCx

![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Tests](https://img.shields.io/badge/Tests-59%20passed-brightgreen.svg)

## 简介

MDCx 是一个现代化的视频元数据刮削和管理工具，支持从 40+ 个网站自动获取视频信息，生成符合 KODI/Emby 规范的 NFO 文件，并提供完整的图片处理和翻译功能。

### 核心特性

- 🤖 **智能刮削**: 支持 40+ 个数据源，自动识别番号
- 📄 **NFO 生成**: 生成符合 KODI/Emby 规范的元数据文件
- 📺 **VSMETA 支持**: 完整实现 Synology Video Station 的 VSMETA 二进制格式
  - 与 [JuanWoo/nfo-to-vsmeta](https://github.com/JuanWoo/nfo-to-vsmeta) 完全兼容
  - 支持嵌入海报、背景图，自动压缩至 200KB
  - 可配置的简介格式（日文标题+中日/日中双语）
  - 完整的错误处理和原子写入，确保文件完整性
  - 高度可配置：图片尺寸、JPEG 质量、演员/标签数量限制等
- 🖼️ **图片处理**: 自动下载、裁剪、添加水印
- 🌐 **多语言翻译**: 支持 Google/DeepL/LLM 翻译
- 📁 **灵活命名**: Jinja2 模板系统，支持自定义命名规则
- 🔍 **Amazon 集成**: 条码识别，自动匹配封面
- ⚡ **异步处理**: 高效的并发刮削能力
- 🧪 **全面测试**: 59+ 个单元测试，覆盖率 42%+

## 文档

- 📖 [API 文档](docs/api-documentation.md) - 完整的 API 参考
- 🏗️ [架构设计](docs/architecture.md) - 系统架构和设计模式
- 🔧 [CI/CD 指南](docs/ci-testing.md) - 持续集成和测试
- 📝 [变更日志](changelog.md) - 版本更新历史

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI

# 安装依赖
uv sync --locked --all-extras --dev

# 运行应用
uv run python mdcx/views/MDCx.py
```

### 从 Release 下载

预编译版本可在 [Release](https://github.com/1525745393/mdcx-AI/releases/latest) 页面下载。

## 交流群

[![Telegram](https://img.shields.io/badge/Telegram-Join_Chat-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/mdcx_chat)

> [!TIP]
> **使用问题**：有关软件配置、使用心得等非技术性问题，建议优先加入 **Telegram 交流群**与群友交流。  
> **Bug 反馈**：如遇程序异常或功能缺陷，请先确认是否为已知问题，再提交 **Issue** 并附上相关日志、问题番号等内容。

## 上游项目

* [yoshiko2/Movie_Data_Capture](https://github.com/yoshiko2/Movie_Data_Capture): CLI 工具,
  开源版本现已不活跃, 新版本已闭源商业化.
* [moyy996/AVDC](https://github.com/moyy996/AVDC): 上述项目早期的一个 Fork, 使用 PyQt 实现了图形界面, 已停止维护
* @Hermit/MDCx: AVDC 的 Fork, 一度在 [anyabc/something](https://github.com/anyabc/something/releases) 分发源代码及可执行文件.
* 2023-11-3 @anyabc 因未知原因销号删库, 其分发的最后一个版本号为 20231014.
* [@sqzw-x/mdcx](https://github.com/sqzw-x/mdcx)当前暂时停止维护.
* 本项目基于 [@sqzw-x/mdcx](https://github.com/sqzw-x/mdcx), 继续进行维护及优化.

向相关开发者表示敬意.

## 特别致谢

### VSMETA 格式

特别感谢 [JuanWoo/nfo-to-vsmeta](https://github.com/JuanWoo/nfo-to-vsmeta) 项目，本项目的 VSMETA 实现基于该项目的格式规范，确保与 Synology Video Station 完全兼容。

### 格式逆向工程

感谢 soywiz / Carlos Ballesteros Velasco 对 VSMETA 格式的逆向工程研究，为我们提供了格式解析的基础。

## 构建

> 一般情况请勿自行构建, 至 [Release](https://github.com/sqzw-x/mdcx/releases) 下载最新版

### Windows 7

> 即将放弃对 Windows 7 的支持. [#494](https://github.com/sqzw-x/mdcx/issues/494)

Windows 7 上需使用 Python 3.8 构建, 代码及依赖均兼容, 可在本地自行构建. 也可使用 GitHub Actions 构建:

1. fork 本仓库, 在仓库设置中启用 Actions
2. 参考 [为存储库创建配置变量](https://docs.github.com/zh/actions/learn-github-actions/variables#creating-configuration-variables-for-a-repository), 设置 `BUILD_FOR_WINDOWS_LEGACY` 变量, 值非空即可
3. 在 Actions 中手动运行 `Build and Release`

### macOS

低版本 macOS: 需注意 opencv 兼容性问题, 参考 [issue #82](https://github.com/sqzw-x/mdcx/issues/82#issuecomment-1947973961).
也可使用 GitHub Actions 构建, 步骤同上, 需设置 `BUILD_FOR_MACOS_LEGACY` 变量, 值非空即可;
以及 `MACOS_LEGACY_CV_VERSION` 变量, 值为兼容的 `opencv-contrib-python-headless` 版本

## 授权许可

本插件项目在 GPLv3 许可授权下发行。此外，如果使用本项目表明还额外接受以下条款：

* 本项目仅供学习以及技术交流使用
* 请勿在公共社交平台上宣传此项目
* 使用本软件时请遵守当地法律法规
* 法律及使用后果由使用者自己承担
* 禁止将本软件用于任何的商业用途
