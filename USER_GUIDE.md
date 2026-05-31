# MDCx 用户使用手册

> 📖 **更多文档**: [文档中心](docs/README.md) | [主 README](README.md) | [FAQ](FAQ.md) | [配置说明](docs/CONFIGURATION.md)

## 目录
1. [项目简介](#1-项目简介)
2. [安装和启动](#2-安装和启动)
3. [功能介绍](#3-功能介绍)
4. [使用步骤](#4-使用步骤)
5. [配置说明](#5-配置说明)
6. [操作示例](#6-操作示例)
7. [常见问题](#7-常见问题)

---

## 1. 项目简介

### 1.1 什么是 MDCx
MDCx 是一个现代化的视频元数据刮削和管理工具，专为影视收藏爱好者和媒体服务器用户打造。它支持从 40+ 个网站自动获取视频信息，生成符合 KODI/Emby 规范的 NFO 文件，并提供完整的图片处理和翻译功能。

### 1.2 主要特性
- 🤖 **智能刮削**：支持 40+ 个数据源，自动识别番号
- 📄 **NFO 生成**：生成符合 KODI/Emby 规范的元数据文件
- 📺 **VSMETA 支持**：完整实现 Synology Video Station 的 VSMETA 二进制格式
- 🖼️ **图片处理**：自动下载、裁剪、添加水印
- 🌐 **多语言翻译**：支持 Google/DeepL/LLM 翻译
- 📁 **灵活命名**：Jinja2 模板系统，支持自定义命名规则
- ⚡ **异步处理**：高效的并发刮削能力

### 1.3 支持的网站
MDCx 支持多种类型的视频网站，包括：
- 有码网站：DMM, MGStage, JavBus, JavDB, MissAV 等
- 无码网站：Kin8, Love6 等
- FC2 网站：FC2, FC2Club, FC2Hub, FC2PPVDB
- 国产网站：HDOUBAN, CNMDB, GUOCHAN, MADOUQU
- 欧美网站：THEPORNDB

---

## 2. 安装和启动

### 2.1 系统要求
- Windows 10+ / macOS 10.15+ / Linux
- 网络连接（用于刮削数据）
- Python 3.13+（从源码运行时需要）

### 2.2 安装方法

#### 方法一：从 Release 下载（推荐）
1. 访问 [GitHub Release 页面](https://github.com/1525745393/mdcx-AI/releases/latest)
2. 下载适合您操作系统的预编译版本
3. 解压压缩包
4. 直接运行可执行文件

#### 方法二：从源码运行
1. 克隆仓库：
   ```bash
   git clone https://github.com/1525745393/mdcx-AI.git
   cd mdcx-AI
   ```
2. 安装依赖：
   ```bash
   # 使用 uv（推荐）
   uv sync --locked --all-extras --dev
   
   # 或使用 pip
   pip install -e .
   ```
3. 运行程序：
   ```bash
   uv run python main.py
   # 或
   python main.py
   ```

### 2.3 首次启动
首次启动 MDCx 时，程序会自动：
1. 在用户目录下创建配置文件夹
2. 生成默认配置文件
3. 显示主界面

---

## 3. 功能介绍

### 3.1 视频刮削
MDCx 核心功能是自动从多个网站获取视频元数据，包括：
- 番号识别和分类
- 多网站并行刮削
- 字段优先级管理
- 结果整合与优化

### 3.2 文件管理
- 自动扫描媒体目录
- 文件重命名（支持自定义模板）
- 文件移动和整理
- 软链接创建
- 字幕文件管理

### 3.3 图片处理
- 海报、缩略图、背景图下载
- 智能人脸裁剪
- 自定义水印添加
- 图片质量和尺寸优化

### 3.4 NFO 生成
- 生成符合 KODI/Emby 规范的 NFO 文件
- 支持自定义 NFO 包含的字段
- 完整的 XML 结构

### 3.5 VSMETA 支持
- 完整实现 Synology Video Station 的 VSMETA 二进制格式
- 支持嵌入海报、背景图
- 高度可配置的简介格式
- 自定义模板支持

### 3.6 翻译功能
- 支持多种翻译服务：Google、DeepL、LLM 等
- 字段级翻译配置
- 中文简繁转换

### 3.7 工具集
- 演员数据库管理
- Emby 演员图片和信息同步
- 字幕管理
- 缺失文件检测
- 海报裁剪工具

---

## 4. 使用步骤

### 4.1 基本使用流程

#### 步骤 1：配置媒体路径
1. 启动 MDCx
2. 点击「设置」按钮
3. 在「通用」选项卡中设置：
   - 媒体路径：存放待刮削视频文件的目录
   - 成功输出目录（可选）：刮削成功后文件移动的位置
   - 失败输出目录（可选）：刮削失败后文件移动的位置

#### 步骤 2：配置刮削源
1. 进入「刮削」选项卡
2. 选择您想要使用的刮削网站
3. 可以为不同类型（有码/无码/FC2等）配置不同的网站
4. 调整刮削并发数（根据您的网络情况）

#### 步骤 3：配置下载选项
1. 进入「下载」选项卡
2. 选择需要下载的文件类型：
   - poster（海报）
   - thumb（缩略图）
   - fanart（背景图）
   - extrafanart（额外背景图）
   - nfo（NFO 文件）
   - vsmeta（VSMETA 文件）
3. 配置图片质量和尺寸

#### 步骤 4：配置命名规则（可选）
1. 进入「命名」选项卡
2. 根据需要调整文件夹和文件命名模板
3. 配置 VSMETA 自定义模板（如果使用 Synology）

#### 步骤 5：配置翻译（可选）
1. 进入「翻译」选项卡
2. 选择翻译服务
3. 配置相应的 API 密钥（如需要）
4. 选择需要翻译的字段

#### 步骤 6：开始刮削
1. 返回主界面
2. 点击「扫描」按钮扫描媒体目录
3. 在文件列表中选择要刮削的文件
4. 点击「开始」按钮开始刮削
5. 等待刮削完成，查看结果

### 4.2 VSMETA 自定义模板使用

#### 模板占位符
VSMETA 支持以下占位符：
- `{number}`：番号
- `{title}`：标题
- `{originaltitle}`：原始标题
- `{publisher}`：发行商
- `{studio}`：制作商
- `{series}`：系列
- `{actors}`：演员
- `{outline}`：简介
- `{originalplot}`：原始简介
- `{year}`：年份
- `{release}`：发行日期
- `{score}`：评分
- `{country}`：国家
- `{director}`：导演
- `{genre}`：类型
- `{mosaic}`：马赛克类型
- `{runtime}`：时长
- `{label}`：标签
- `{website}`：网站

#### 条件语法
支持条件渲染：
```
{if:field}内容{/if}
```

#### 默认值语法
支持默认值：
```
{field|默认值}
```

#### 示例模板
```
标题模板：{number} - {title}
副标题模板：{originaltitle}
简介模板：{originaltitle}\n\n{outline}\n\n{originalplot}
```

### 4.3 命令行使用

MDCx 也提供命令行工具：

#### 命令行刮削
```bash
uv run python -m mdcx.cmd.crawl
```

#### 生成枚举
```bash
uv run python -m mdcx.cmd.gen_enums
```

---

## 5. 配置说明

> 💡 **详细配置文档**: [配置说明](docs/CONFIGURATION.md)

### 5.1 配置文件位置
配置文件默认存储在以下位置：
- Windows：`%APPDATA%\MDCx\`
- macOS：`~/Library/Application Support/MDCx/`
- Linux：`~/.config/MDCx/`

### 5.2 主要配置项

#### 通用设置
- `media_path`：媒体路径
- `success_output_folder`：成功输出目录
- `failed_output_folder`：失败输出目录
- `media_type`：媒体文件类型
- `sub_type`：字幕文件类型

#### 清理设置
- `folders`：排除目录
- `string`：需要从文件名删除的字符串
- `clean_enable`：启用的清理规则

#### 刮削设置
- `thread_number`：并发数
- `download_files`：下载文件类型
- `website_youma`：有码网站源
- `website_wuma`：无码网站源
- `website_fc2`：FC2 网站源
- `website_oumei`：欧美网站源
- `website_guochan`：国产网站源

#### 字段配置
- `field_configs`：各字段的网站优先级、语言、翻译开关

#### 命名和格式化
- `folder_name`：目录名模板
- `naming_file`：文件名模板
- `nfo_include_new`：NFO 包含内容
- `vsmeta_show_title`：VSMETA 显示标题
- `vsmeta_show_title2`：VSMETA 显示副标题
- `vsmeta_summary`：VSMETA 简介格式

#### 服务器设置
- `server_type`：服务器类型（emby/jellyfin）
- `emby_url`：Emby 地址
- `api_key`：API 密钥

#### 水印设置
- `poster_mark`、`thumb_mark`、`fanart_mark`：水印开关
- `mark_type`：水印类型
- `mark_size`：水印大小

#### 网络设置
- `use_proxy`：代理开关
- `proxy`：代理地址
- `timeout`：超时时间
- `retry`：重试次数

#### 翻译设置
- `translate_config.translate_by`：翻译服务列表
- `translate_config.baidu_appid`、`translate_config.baidu_key`：百度翻译配置
- `translate_config.deepl_key`：DeepL 配置
- `translate_config.llm_url`、`translate_config.llm_model`、`translate_config.llm_key`：LLM 翻译配置

---

## 6. 操作示例

### 6.1 基本刮削示例

假设您有以下视频文件：
```
D:\Media\Input\ABP-123.mp4
D:\Media\Input\FC2-123456.mp4
```

#### 操作步骤：
1. 打开 MDCx，进入「设置」→「通用」
2. 设置媒体路径为 `D:\Media\Input`
3. 进入「刮削」选项卡，选择有码和 FC2 的刮削源
4. 进入「下载」选项卡，勾选需要下载的文件类型
5. 返回主界面，点击「扫描」
6. 选中扫描到的文件，点击「开始」
7. 等待刮削完成

#### 结果：
程序会自动：
1. 识别番号类型
2. 从配置的网站获取元数据
3. 下载图片
4. 生成 NFO/VSMETA 文件
5. 重命名和移动文件（如果配置了）

### 6.2 VSMETA 配置示例

假设您使用 Synology Video Station，想要自定义 VSMETA 的显示：

1. 进入「设置」→「命名」
2. 找到 VSMETA 设置区域
3. 配置如下：
   ```
   标题模板：{number} - {title}
   副标题模板：{publisher} ({release})
   简介模板：{originaltitle}\n\n{outline}\n\n演员：{actors}
   ```
4. 勾选「包含海报」和「包含背景图」
5. 点击「保存设置」

### 6.3 翻译配置示例

假设您想使用 DeepL 翻译元数据：

1. 进入「设置」→「翻译」
2. 在翻译服务中选择「DeepL」
3. 输入您的 DeepL API Key
4. 选择需要翻译的字段（如 title、outline、actors）
5. 点击「保存设置」

### 6.4 Emby 集成示例

假设您想将元数据同步到 Emby：

1. 进入「设置」→「服务器」
2. 选择服务器类型为「Emby」
3. 输入 Emby 地址（如 `http://192.168.1.100:8096`）
4. 输入 Emby API Key
5. 勾选需要的功能（如演员信息同步、演员图片同步）
6. 点击「保存设置」

---

## 7. 常见问题

### 7.1 网络问题

#### Q: 刮削时提示网络连接失败怎么办？
A: 
1. 检查您的网络连接
2. 在「设置」→「网络」中配置代理
3. 检查防火墙设置
4. 尝试增加超时时间和重试次数

#### Q: 某些网站无法访问怎么办？
A: 
1. 尝试使用代理
2. 更换其他刮削源
3. 检查该网站是否正常运行

### 7.2 刮削问题

#### Q: 某些视频无法识别番号怎么办？
A: 
1. 检查文件名是否包含完整的番号
2. 尝试手动修改文件名，使其包含正确的番号
3. 在设置中检查番号识别规则

#### Q: 刮削结果不正确怎么办？
A: 
1. 检查刮削源配置
2. 调整字段优先级
3. 尝试更换其他刮削源
4. 查看日志了解详细信息

### 7.3 VSMETA 问题

#### Q: Synology Video Station 不显示 VSMETA 元数据怎么办？
A: 
1. 确认已勾选「下载 VSMETA」选项
2. 检查 VSMETA 配置是否正确
3. 在 Synology Video Station 中刷新媒体库
4. 确认 VSMETA 文件与视频文件在同一目录

#### Q: VSMETA 中的图片不显示怎么办？
A: 
1. 检查「包含海报」和「包含背景图」选项是否勾选
2. 检查图片质量和尺寸设置
3. 尝试减小图片尺寸和质量

### 7.4 翻译问题

#### Q: 翻译失败怎么办？
A: 
1. 检查翻译服务配置
2. 确认 API Key 有效
3. 检查网络连接
4. 查看日志了解详细错误信息

#### Q: 翻译质量不理想怎么办？
A: 
1. 尝试更换其他翻译服务
2. 对于 LLM 翻译，可以自定义提示词
3. 手动编辑 NFO 文件

### 7.5 其他问题

#### Q: 如何查看日志？
A: 
1. 在主界面点击「日志」按钮
2. 或在配置文件夹中查找日志文件

#### Q: 如何重置配置？
A: 
1. 关闭 MDCx
2. 删除配置文件夹中的配置文件
3. 重新启动 MDCx，会自动生成默认配置

#### Q: MDCx 会更新吗？
A: 
1. 是的，MDCx 会定期更新
2. 可以在「设置」中启用自动更新检查
3. 或访问 GitHub Release 页面查看最新版本

---

## 附录

### A. 支持的文件类型

#### 媒体文件
- .mp4, .avi, .rmvb, .wmv, .mov, .mkv, .flv, .ts, .webm, .iso, .mpg, .m4v, .hevc

#### 字幕文件
- .smi, .srt, .idx, .sub, .sup, .psb, .ssa, .ass, .usf, .xss, .ssf, .rt, .lrc, .sbv, .vtt, .ttml

### B. 命名模板变量

MDCx 使用 Jinja2 模板系统，支持以下变量：
- `number`：番号
- `title`：标题
- `originaltitle`：原始标题
- `outline`：简介
- `originalplot`：原始简介
- `actors`：演员列表
- `tags`：标签列表
- `release`：发行日期
- `year`：年份
- `runtime`：时长
- `score`：评分
- `studio`：制作商
- `publisher`：发行商
- `series`：系列
- `director`：导演
- `genre`：类型
- `mosaic`：马赛克类型
- `letters`：番号前缀字母
- `definition`：分辨率
- `cnword`：中文字幕标记
- `moword`：马赛克标记
- 等等...

### C. 获取帮助

- **Telegram 交流群**：[加入群聊](https://t.me/mdcx_chat)
- **GitHub Issues**：[提交问题](https://github.com/1525745393/mdcx-AI/issues)

---

*手册版本：1.0*
*最后更新：2026-05-31*
