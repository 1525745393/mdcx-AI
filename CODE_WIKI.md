# MDCx Code Wiki

## 目录

1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [核心模块](#核心模块)
4. [数据模型](#数据模型)
5. [配置系统](#配置系统)
6. [爬虫系统](#爬虫系统)
7. [VSMETA 生成](#vsmeta-生成)
8. [工具类与辅助函数](#工具类与辅助函数)
9. [项目运行方式](#项目运行方式)
10. [依赖关系](#依赖关系)

---

## 项目概述

### 项目简介

MDCx 是一个现代化的视频元数据刮削和管理工具，主要用于从多个成人视频网站获取元数据信息，包括标题、简介、演员、标签、封面图等，并支持与 Emby、Jellyfin、Kodi 以及 Synology Video Station 等媒体服务器集成。

### 历史沿革

- 上游项目：yoshiko2/Movie_Data_Capture（已闭源）
- 后续分支：moyy996/AVDC（已停止维护）
- 基于：sqzw-x/mdcx
- 当前：1525745393/mdcx-AI

### 核心功能

1. **智能刮削**：支持 40+ 个数据源网站，自动识别番号和马赛克类型
2. **元数据管理**：生成符合 Kodi/Emby 规范的 NFO 文件
3. **VSMETA 支持**：完整支持 Synology Video Station 的 VSMETA 二进制格式
4. **图片处理**：自动下载、裁剪、添加水印
5. **翻译功能**：支持 Google/DeepL/LLM 翻译
6. **命名管理**：灵活的 Jinja2 模板系统，支持自定义命名规则
7. **Amazon 集成**：条码识别，自动匹配封面
8. **异步处理**：高效的并发刮削能力
9. **丰富的工具集**：演员数据库管理、Emby 演员图片和信息同步、字幕管理、缺失文件检测、海报裁剪工具

### 项目特色

- 高度模块化设计，易于维护和扩展
- 完整的测试覆盖，59+ 个单元测试
- 支持字段级优先级配置
- 强大的自定义模板系统
- 完善的错误处理和降级策略
- 跨平台支持（Windows、macOS、Linux）

---

## 项目架构

### 目录结构

```
/workspace/
├── main.py                         # 程序入口
├── mdcx/                           # 主源码目录
│   ├── base/                       # 基础功能模块
│   │   ├── file.py                 # 文件操作
│   │   ├── image.py                # 图片处理
│   │   ├── number.py               # 番号处理
│   │   ├── translate.py            # 翻译
│   │   ├── video.py                # 视频处理
│   │   ├── web.py                  # 网络请求
│   │   └── web_sync.py             # 同步网络请求
│   ├── cmd/                        # 命令行工具
│   │   ├── crawl.py                # 命令行刮削
│   │   └── gen_enums.py            # 生成枚举
│   ├── config/                     # 配置管理
│   │   ├── computed.py             # 计算属性
│   │   ├── enums.py                # 配置枚举
│   │   ├── extend.py               # 扩展配置
│   │   ├── manager.py              # 配置管理器
│   │   ├── migrations.py           # 配置迁移
│   │   ├── models.py               # 配置模型
│   │   ├── resource_policy.py      # 资源策略
│   │   ├── resources.py            # 资源管理
│   │   └── v1.py                   # V1 配置兼容
│   ├── controllers/                # 控制器（业务逻辑）
│   │   └── main_window/            # 主窗口控制器
│   │       ├── bind_utils.py       # 绑定工具
│   │       ├── handlers.py         # 事件处理
│   │       ├── init.py             # 初始化
│   │       ├── load_config.py      # 加载配置
│   │       ├── main_window.py      # 主窗口
│   │       ├── performance_dialog.py # 性能对话框
│   │       ├── save_config.py      # 保存配置
│   │       ├── site_priority_dialog.py # 站点优先级对话框
│   │       └── style.py            # 样式
│   ├── core/                       # 核心功能
│   │   ├── __init__.py
│   │   ├── amazon.py               # Amazon 集成
│   │   ├── face_crop.py            # 人脸裁剪
│   │   ├── file.py                 # 文件处理
│   │   ├── file_crawler.py         # 文件刮削
│   │   ├── image.py                # 图片处理
│   │   ├── media_resource.py       # 媒体资源
│   │   ├── mosaic.py               # 马赛克处理
│   │   ├── naming/                 # 命名系统
│   │   │   ├── __init__.py
│   │   │   ├── fields.py           # 命名字段
│   │   │   ├── renderer.py         # 渲染器
│   │   │   ├── sanitize.py         # 清理
│   │   │   └── template.py         # 模板
│   │   ├── network_check.py        # 网络检查
│   │   ├── nfo.py                  # NFO 生成
│   │   ├── scraper.py              # 刮削器
│   │   ├── tag_priority.py         # 标签优先级
│   │   ├── translate.py            # 翻译
│   │   ├── utils.py                # 工具函数
│   │   ├── vsmeta.py               # VSMETA 生成
│   │   └── web.py                  # Web 操作
│   ├── crawlers/                   # 爬虫实现
│   │   ├── base/                   # 爬虫基类
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # 基础爬虫类
│   │   │   ├── parser.py           # 解析器
│   │   │   └── types.py            # 类型定义
│   │   ├── dmm_new/                # DMM 爬虫
│   │   ├── airav_cc.py             # Airav.cc 爬虫
│   │   ├── avbase_new.py           # AVBase 爬虫
│   │   ├── avsex.py                # AVSex 爬虫
│   │   ├── avsox.py                # AVSoX 爬虫
│   │   ├── cableav.py              # CableAV 爬虫
│   │   ├── cnmdb.py                # CNMDB 爬虫
│   │   ├── dahlia.py               # Dahlia 爬虫
│   │   ├── faleno.py               # Faleno 爬虫
│   │   ├── fantastica.py           # Fantastica 爬虫
│   │   ├── fc2.py                  # FC2 爬虫
│   │   ├── fc2club.py              # FC2Club 爬虫
│   │   ├── fc2hub.py               # FC2Hub 爬虫
│   │   ├── fc2ppvdb.py             # FC2PPVDB 爬虫
│   │   ├── freejavbt.py            # FreeJAVBT 爬虫
│   │   ├── getchu.py               # Getchu 爬虫
│   │   ├── getchu_dl.py            # Getchu DL 爬虫
│   │   ├── getchu_dmm.py           # Getchu DMM 爬虫
│   │   ├── giga.py                 # Giga 爬虫
│   │   ├── guochan.py              # 国产爬虫
│   │   ├── hdouban.py              # HDouban 爬虫
│   │   ├── hscangku.py             # HSCangku 爬虫
│   │   ├── iqqtv.py                # IQQTV 爬虫
│   │   ├── jav321.py               # Jav321 爬虫
│   │   ├── javbus.py               # JavBus 爬虫
│   │   ├── javday.py               # JavDay 爬虫
│   │   ├── javdb_new.py            # JavDB 爬虫
│   │   ├── javdbapi.py             # JavDB API 爬虫
│   │   ├── javlibrary.py           # JavLibrary 爬虫
│   │   ├── kin8.py                 # Kin8 爬虫
│   │   ├── love6.py                # Love6 爬虫
│   │   ├── lulubar.py              # Lulubar 爬虫
│   │   ├── madouqu.py              # Madouqu 爬虫
│   │   ├── mgstage.py              # MGStage 爬虫
│   │   ├── missav.py               # MissAV 爬虫
│   │   ├── mmtv.py                 # MMTV 爬虫
│   │   ├── mywife.py               # MyWife 爬虫
│   │   ├── official.py             # Official 爬虫
│   │   ├── prestige.py             # Prestige 爬虫
│   │   ├── theporndb.py            # ThePornDB 爬虫
│   │   └── xcity.py                # XCity 爬虫
│   ├── gen/                        # 自动生成的枚举
│   │   └── field_enums.py
│   ├── models/                     # 数据模型
│   │   ├── emby.py                 # Emby 模型
│   │   ├── enums.py                # 枚举
│   │   ├── flags.py                # 标志
│   │   ├── log_buffer.py           # 日志缓冲
│   │   └── types.py                # 类型定义
│   ├── tools/                      # 工具模块
│   │   ├── actress_db.py           # 演员数据库
│   │   ├── emby_actor_image.py     # Emby 演员图片
│   │   ├── emby_actor_info.py      # Emby 演员信息
│   │   ├── missing.py              # 缺失文件检测
│   │   ├── subtitle.py             # 字幕管理
│   │   └── wiki.py                 # Wiki 工具
│   ├── utils/                      # 工具函数
│   │   ├── __init__.py
│   │   ├── crawler_health.py       # 爬虫健康监测
│   │   ├── dataclass.py            # 数据类工具
│   │   ├── file.py                 # 文件工具
│   │   ├── gather_group.py         # 分组工具
│   │   ├── language.py             # 语言工具
│   │   ├── leb128.py               # LEB128 编码
│   │   ├── path.py                 # 路径工具
│   │   ├── perf.py                 # 性能工具
│   │   ├── report_system.py        # 报告系统
│   │   ├── video.py                # 视频工具
│   │   └── vsmeta_template_helper.py # VSMETA 模板助手
│   ├── views/                      # UI 视图
│   │   ├── CustomClass.py          # 自定义类
│   │   ├── MDCx.py                 # 主视图
│   │   ├── MDCx.ui                 # UI 文件
│   │   ├── posterCutTool.py        # 海报裁剪工具
│   │   └── posterCutTool.ui        # 海报裁剪 UI
│   ├── __init__.py
│   ├── browser.py                  # 浏览器
│   ├── consts.py                   # 常量
│   ├── crawler.py                  # 爬虫提供者
│   ├── image.py                    # 图片
│   ├── llm.py                      # LLM 集成
│   ├── manual.py                   # 手动配置
│   ├── network_fingerprint.py      # 网络指纹
│   ├── number.py                   # 番号
│   ├── signals.py                  # 信号系统
│   └── web_async.py                # 异步 Web 客户端
├── resources/                      # 资源文件
│   ├── Img/                        # 图片资源
│   ├── c_number/                   # C 番号数据
│   ├── config/                     # 默认配置
│   │   └── default_config.json
│   ├── fonts/                      # 字体
│   ├── mapping_table/              # 映射表
│   │   ├── mapping_actor.xml
│   │   └── mapping_info.xml
│   └── zhconv/                     # 中文简繁转换
├── tests/                          # 测试代码
│   ├── core/                       # 核心模块测试
│   ├── crawlers/                   # 爬虫测试
│   ├── utils/                      # 工具测试
│   ├── __init__.py
│   ├── conftest.py                 # 测试配置
│   └── random_generator.py         # 随机生成器
├── scripts/                        # 脚本工具
│   ├── __init__.py
│   ├── build.py                    # 构建脚本
│   ├── bump.py                     # 版本升级
│   ├── changelog.py                # 变更日志
│   ├── extract.py                  # 提取
│   ├── filter_map_xml.py           # 过滤映射 XML
│   ├── get-dev-info.sh             # 获取开发信息
│   ├── performance_demo.py         # 性能演示
│   ├── pyuic.sh                    # PyQt UI 转换
│   └── stress_missav_cf.py         # 压力测试
├── .github/                        # GitHub 配置
│   ├── workflows/                  # GitHub Actions
│   └── ISSUE_TEMPLATE/             # Issue 模板
├── pyproject.toml                  # 项目配置
├── ruff.toml                       # Ruff 配置
├── README.md                       # 项目说明
├── USER_GUIDE.md                   # 用户手册
├── DEVELOPMENT.md                  # 开发指南
├── CONTRIBUTING.md                 # 贡献指南
├── FAQ.md                          # 常见问题
├── INSTALL.md                      # 安装指南
├── VSMETA_COMPARISON.md            # VSMETA 对比
├── SOUL.md                         # 项目理念
├── LICENSE                         # 许可证
└── changelog.md                    # 变更日志
```

### 架构分层

MDCx 采用经典的分层架构设计：

```
┌─────────────────────────────────────────────────────────────┐
│                      UI Layer (PyQt6)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ MainWindow   │  │ SettingsUI   │  │ ProgressUI   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Controller Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ EventHandler │  │ ConfigMgr    │  │ SignalBus   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Core Business Logic                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Scraper     │  │ FileCrawler  │  │ NamingSystem │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   NFO Gen    │  │  Amazon OCR  │  │  Translator  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ VSMETA Gen   │  │ Image Proc   │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Crawler Framework                        │
│  ┌──────────────────────────────────────────────────┐      │
│  │              GenericBaseCrawler[T]                │      │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐│      │
│  │  │ JAVBus │  │JAVLib  │  │  DMM   │  │  FC2   ││      │
│  │  └────────┘  └────────┘  └────────┘  └────────┘│      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ HTTP Client  │  │ File System  │  │ Image Proc   │     │
│  │ (httpx)      │  │ (asyncio)    │  │ (OpenCV)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 主要模块依赖关系

```
main.py
  └─> controllers/main_window/
        └─> core/scraper.py
              ├─> crawler.py
              │     └─> crawlers/
              ├─> core/file_crawler.py
              ├─> core/nfo.py
              ├─> core/vsmeta.py
              ├─> core/media_resource.py
              ├─> core/translate.py
              └─> config/manager.py
```

### 数据流程

1. **文件扫描**：FileCrawler 扫描媒体目录，识别视频文件
2. **番号识别**：从文件名中提取番号，识别马赛克类型
3. **爬虫执行**：根据配置调用相应网站的爬虫
4. **数据整合**：整合多个网站的结果，应用字段优先级
5. **翻译处理**：根据配置翻译元数据
6. **命名生成**：应用命名模板生成新的文件名和目录名
7. **资源下载**：下载海报、缩略图、背景图、预告片等
8. **元数据写入**：生成 NFO 文件和 VSMETA 文件
9. **文件移动**：移动和重命名文件到目标位置

---

## 核心模块

### 1. 入口模块 ([main.py](file:///workspace/main.py))

**功能**：程序启动入口，初始化 GUI 应用

**主要类/函数**：
- `show_constants()`：显示运行时常量
- 主程序入口：初始化 PyQt6 应用，加载配置，显示主窗口

**关键代码**：
```python
# 初始化 Qt 应用
app = QApplication(sys.argv)
app.setStyle("Fusion")
apply_application_palette(False)

# 显示主窗口
ui = MyMAinWindow()
ui.show()

# 运行事件循环
sys.exit(app.exec())
```

### 2. 常量定义 ([mdcx/consts.py](file:///workspace/mdcx/consts.py))

**功能**：定义项目常量

**主要常量**：
- `LOCAL_VERSION`：本地版本号
- `GITHUB_REPO`：GitHub 仓库地址
- `GITHUB_RELEASES_URL`：发布页地址
- `IS_WINDOWS`、`IS_MAC`、`IS_LINUX`、`IS_DOCKER`：平台判断
- `MAIN_PATH`：主路径
- `MARK_FILE`：配置标记文件

### 3. 信号系统 ([mdcx/signals.py](file:///workspace/mdcx/signals.py))

**功能**：PyQt6 信号定义，用于组件间通信

### 4. 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))

**功能**：管理和提供爬虫实例

**主要类**：
- `CrawlerProvider`：爬虫提供者，管理爬虫实例生命周期

### 5. 刮削器 ([mdcx/core/scraper.py](file:///workspace/mdcx/core/scraper.py))

**功能**：主刮削器，协调整个刮削流程

**主要类**：
- `Scraper`：刮削器主类
  - `run()`：执行刮削
  - `process_one_file()`：处理单个文件
  - `_process_one_file_with_context()`：内部处理逻辑

**刮削流程**：
1. 获取文件信息
2. 调用爬虫获取数据
3. 翻译元数据
4. 下载图片和预告片
5. 添加水印
6. 生成 NFO
7. 生成 VSMETA
8. 移动和重命名文件
9. 创建软链接（可选）

**关键特性**：
- 渐进式任务调度，支持大量文件
- 并发控制，可配置线程数
- 间歇刮削支持
- 停止/恢复支持

### 6. 文件刮削器 ([mdcx/core/file_crawler.py](file:///workspace/mdcx/core/file_crawler.py))

**功能**：处理单个文件的刮削逻辑

**主要类**：
- `FileScraper`：文件刮削器
  - 识别番号和刮削类型
  - 调用多个网站爬虫
  - 整合各网站结果
  - 字段优先级处理

### 7. NFO 生成器 ([mdcx/core/nfo.py](file:///workspace/mdcx/core/nfo.py))

**功能**：生成符合 Kodi/Emby 规范的 NFO 文件

**主要功能**：
- 生成 XML 格式的 NFO
- 支持所有元数据字段
- 可配置包含的内容

### 8. VSMETA 生成器 ([mdcx/core/vsmeta.py](file:///workspace/mdcx/core/vsmeta.py))

**功能**：生成 Synology Video Station 的 VSMETA 二进制格式

**主要类**：
- `VSMetaEncoder`：VSMETA 编码器
  - `write_header()`：写入文件头
  - `write_string_field()`：写入字符串字段
  - `write_varint_field()`：写入 Varint 字段
  - `write_poster()`：写入海报图片
  - `write_submessage()`：写入嵌套子消息
  - `get_bytes()`：获取最终的 VSMETA 字节数据

**VSMETA 格式规范**：
- 使用 Protobuf 风格的二进制编码
- 支持图片 Base64 编码和 MD5 校验
- 支持嵌套子消息（Group1/Group2/Group3）
- 最大支持 200KB 的图片

### 9. 命名系统 ([mdcx/core/naming/](file:///workspace/mdcx/core/naming/))

**功能**：灵活的文件和目录命名系统

**主要模块**：
- `template.py`：模板解析
- `renderer.py`：模板渲染
- `sanitize.py`：名称清理
- `fields.py`：可用字段

**支持的字段**：
- 基础字段：number, title, originaltitle
- 人员字段：actor, actors, director, directors
- 发行字段：release, year, runtime
- 分类字段：mosaic, series, studio, publisher
- 评分字段：score, wanted
- 资源字段：poster, thumb, fanart
- 其他字段：outline, originalplot, tag, tags

### 10. 翻译系统 ([mdcx/core/translate.py](file:///workspace/mdcx/core/translate.py))

**功能**：支持多种翻译服务

**支持的翻译服务**：
- Google 翻译
- 百度翻译
- DeepL 翻译
- DeepLX 翻译
- LLM 翻译（支持自定义 API）

**可配置项**：
- 翻译服务选择
- API 密钥配置
- 字段级翻译开关
- 目标语言选择

### 11. 媒体资源 ([mdcx/core/media_resource.py](file:///workspace/mdcx/core/media_resource.py))

**功能**：处理媒体资源下载（海报、缩略图、背景图、预告片等）

### 12. 图片处理 ([mdcx/core/image.py](file:///workspace/mdcx/core/image.py))

**功能**：图片下载、裁剪、添加水印

### 13. 人脸裁剪 ([mdcx/core/face_crop.py](file:///workspace/mdcx/core/face_crop.py))

**功能**：智能人脸检测和裁剪

### 14. Amazon 集成 ([mdcx/core/amazon.py](file:///workspace/mdcx/core/amazon.py))

**功能**：Amazon 条码识别，自动匹配高清封面

---

## 数据模型

### 文件信息模型 ([mdcx/models/types.py](file:///workspace/mdcx/models/types.py))

#### `FileInfo`

媒体文件基础信息

**主要字段**：
- `number`：番号
- `mosaic`：马赛克类型
- `file_path`：文件路径
- `has_sub`：是否有字幕
- `definition`：分辨率
- `codec`：编码格式
- `actors`：演员列表
- `director`：导演
- `studio`：制作商
- `publisher`：发行商
- `series`：系列
- `release`：发行日期
- `year`：年份
- `runtime`：片长
- `score`：评分
- `tags`：标签列表
- `outline`：简介
- `originalplot`：原始简介
- `title`：标题
- `originaltitle`：原始标题
- `poster`：海报 URL
- `thumb`：缩略图 URL
- `fanart`：背景图 URL
- `trailer`：预告片 URL
- `extrafanart`：额外剧照 URL 列表

**主要方法**：
- `crawler_input()`：转换为爬虫输入
- `crawl_task()`：转换为刮削任务
- `empty()`：创建空实例

#### `CrawlerInput`

单个爬虫调用输入

**主要字段**：
- `appoint_number`：指定番号
- `appoint_url`：指定 URL
- `file_path`：文件路径
- `number`：番号
- `mosaic`：马赛克类型
- `short_number`：短番号
- `language`：语言
- `org_language`：原始语言

#### `CrawlTask`

单个文件刮削任务，继承自 `CrawlerInput`

**主要字段**：
- `c_word`：中文词
- `cd_part`：CD 部分
- `destroyed`：损坏信息
- `has_sub`：是否有字幕
- `leak`：泄露信息
- `website_name`：网站名称（仅用于重新刮削）
- `wuma`：无码信息
- `youma`：有码信息

#### `BaseCrawlerResult`

爬虫结果基础类型

**主要字段**：
- `number`：番号
- `mosaic`：马赛克类型
- `image_download`：是否需要下载图片
- `actors`：演员列表
- `all_actors`：所有演员列表
- `directors`：导演列表
- `extrafanart`：额外剧照 URL 列表
- `originalplot`：原始简介（日文）
- `originaltitle`：原始标题（日文）
- `outline`：简介
- `poster`：海报 URL
- `publisher`：发行商
- `release`：发行日期
- `runtime`：片长（分钟）
- `score`：评分
- `series`：系列
- `studio`：制作商
- `tags`：标签列表
- `thumb`：缩略图 URL
- `title`：标题
- `trailer`：预告片 URL
- `wanted`：想看数
- `year`：发行年份

**主要方法**：
- `country`：根据 mosaic 字段返回国家代码（CN/JP/US）

#### `CrawlerResult`

单一网站爬虫结果

#### `CrawlersResult`

整合所有网站的结果

#### `OtherInfo`

其他处理信息（文件移动、水印等）

#### `ScrapeResult`

刮削结果封装

#### `ShowData`

显示数据

### 枚举定义 ([mdcx/models/enums.py](file:///workspace/mdcx/models/enums.py))

主要枚举包括：
- `FileMode`：文件模式
- 各种状态标志

---

## 配置系统

### 配置模型 ([mdcx/config/models.py](file:///workspace/mdcx/config/models.py))

#### `Config`

主配置类，基于 Pydantic

**主要配置区域**：

1. **通用设置 (General Settings)**
   - `media_path`：媒体路径
   - `softlink_path`：软链接路径
   - `success_output_folder`：成功输出目录
   - `failed_output_folder`：失败输出目录
   - `media_type`：媒体文件类型列表
   - `sub_type`：字幕文件类型列表
   - `scrape_softlink_path`：是否刮削软链接路径
   - `auto_link`：是否自动创建软链接

2. **清理设置 (Cleaning Settings)**
   - `folders`：排除目录列表
   - `string`：要从文件名删除的字符串列表
   - `file_size`：要处理的最小文件大小（MB）
   - `no_escape`：不转义的字符串列表
   - `clean_ext`：清理规则：扩展名
   - `clean_name`：清理规则：文件名（完全匹配）
   - `clean_contains`：清理规则：文件名包含
   - `clean_size`：清理小于此大小的文件（KB）
   - `clean_ignore_ext`：清理规则：排除扩展名
   - `clean_ignore_contains`：清理规则：排除文件名包含
   - `clean_enable`：启用的清理规则

3. **刮削设置 (Scraping Settings)**
   - `thread_number`：并发数
   - `thread_time`：线程延时
   - `javdb_time`：JavDB 时间
   - `main_mode`：主模式
   - `read_mode`：读取模式
   - `update_mode`：更新模式
   - `update_a_folder`：更新 A 目录
   - `update_b_folder`：更新 B 目录
   - `update_c_filetemplate`：更新 C 文件模板
   - `update_d_folder`：更新 D 目录
   - `update_titletemplate`：更新标题模板
   - `soft_link`：软链接
   - `success_file_move`：成功后移动文件
   - `failed_file_move`：失败后移动文件
   - `success_file_rename`：成功后重命名文件
   - `del_empty_folder`：删除空目录
   - `show_poster`：显示海报
   - `download_files`：下载文件类型列表
   - `keep_files`：保留文件类型列表
   - `download_hd_pics`：Amazon 高清封面图源列表
   - `amazon_skip_poster_size_precheck`：跳过前置海报大小校验
   - `amazon_strict_pic_verify`：严格校验 Amazon 图片
   - `scrape_like`：刮削模式（speed/info/single）
   - `field_priority_try_all_images`：字段优先时尝试所有图片

4. **网站设置 (Website Settings)**
   - `website_single`：单个网站
   - `website_youma`：有码网站源列表
   - `website_wuma`：无码网站源列表
   - `website_suren`：素人网站源列表
   - `website_fc2`：FC2 网站源列表
   - `website_oumei`：欧美网站源列表
   - `website_guochan`：国产网站源列表
   - `fixed_scraping_type`：锁定刮削类型
   - `actor_realname`：演员真名
   - `outline_format`：简介格式

5. **字段配置 (Field Configurations)**
   - `field_configs`：各字段的网站优先级、语言、翻译开关
     - 键：`CrawlerResultFields` 枚举
     - 值：`FieldConfig` 对象
   - `type_field_configs`：按类型字段优先级
     - 键：`FixedScrapingType` 枚举
     - 值：字段配置字典
   - `site_configs`：网站配置
     - 键：`Website` 枚举
     - 值：`SiteConfig` 对象

6. **翻译配置 (Translation Config)**
   - `translate_config`：`TranslateConfig` 对象
     - `translate_by`：翻译服务列表
     - `baidu_appid`：百度 APP ID
     - `baidu_key`：百度密钥
     - `deepl_key`：DeepL 密钥
     - `deeplx_url`：DeepLX URL
     - `llm_url`：LLM API 地址
     - `llm_model`：LLM 模型
     - `llm_key`：LLM API 密钥
     - `llm_prompt_title`：LLM 标题提示词
     - `llm_prompt_outline`：LLM 简介提示词
     - `llm_read_timeout`：LLM 读取超时（秒）
     - `llm_max_req_sec`：LLM 每秒最大请求数
     - `llm_max_try`：LLM 最大尝试次数
     - `llm_temperature`：LLM 温度

7. **命名和格式化 (Naming and Formatting)**
   - `nfo_include_new`：NFO 包含内容列表
   - `nfo_tagline`：NFO 标语
   - `nfo_tag_include`：包含标签列表
   - `nfo_tag_series`：NFO 系列标签
   - `nfo_tag_studio`：NFO 工作室标签
   - `nfo_tag_publisher`：NFO 发行商标签
   - `nfo_tag_actor`：NFO 演员标签
   - `nfo_tag_actor_contains`：NFO 演员名白名单
   - `folder_name`：目录名称模板
   - `naming_file`：文件命名模板
   - `naming_media`：媒体命名模板
   - `prevent_char`：禁止字符
   - `fields_rule`：字段规则列表
   - `suffix_sort`：后缀排序列表
   - `actor_no_name`：未知演员名称
   - `release_rule`：发布规则
   - `folder_name_max`：目录名称最大长度
   - `file_name_max`：文件名称最大长度
   - `actor_name_max`：演员名称最大数量
   - `actor_name_more`：更多演员名称
   - `umr_style`：UMR 样式
   - `leak_style`：泄露样式
   - `wuma_style`：无码样式
   - `youma_style`：有码样式
   - `cd_name`：CD 名称
   - `cd_char`：CD 字符列表
   - `pic_simple_name`：图片简化命名
   - `trailer_simple_name`：预告片简化命名
   - `vsmeta_keep_ext`：VSMETA 保留视频扩展名
   - `vsmeta_include_poster`：VSMETA 嵌入封面图
   - `vsmeta_include_backdrop`：VSMETA 嵌入背景图
   - `vsmeta_locked`：VSMETA 锁定元数据
   - `vsmeta_image_max_dimension`：VSMETA 图片最大尺寸
   - `vsmeta_jpeg_quality`：VSMETA 图片 JPEG 质量
   - `vsmeta_actor_limit`：VSMETA 演员数量上限
   - `vsmeta_tag_limit`：VSMETA 标签数量上限
   - `vsmeta_show_title`：VSMETA 标题内容
   - `vsmeta_show_title2`：VSMETA 副标题内容
   - `vsmeta_summary`：VSMETA 简介内容
   - `custom_presets`：VSMETA 自定义预设列表
   - `vsmeta_custom_title`：VSMETA 标题自定义模板
   - `vsmeta_custom_title2`：VSMETA 副标题自定义模板
   - `vsmeta_custom_summary`：VSMETA 简介自定义模板
   - `hd_name`：高清名称
   - `hd_get`：获取高清
   - `folder_moword`：目录版本字符
   - `file_moword`：文件版本字符
   - `folder_hd`：目录画质字符
   - `file_hd`：文件画质字符
   - `cnword_char`：中文字符列表
   - `cnword_style`：中文样式
   - `folder_cnword`：目录中文
   - `file_cnword`：文件中文
   - `subtitle_folder`：字幕目录
   - `subtitle_add`：添加字幕
   - `subtitle_add_chs`：添加中文字幕
   - `subtitle_add_rescrape`：重新刮削时添加字幕

8. **服务器设置 (Server Settings)**
   - `server_type`：服务器类型（emby/jellyfin）
   - `emby_url`：Emby 地址
   - `api_key`：API 密钥
   - `user_id`：用户 ID
   - `emby_on`：Emby 功能开关列表
   - `use_database`：使用数据库
   - `info_database_path`：信息数据库路径
   - `gfriends_github`：Gfriends GitHub
   - `actor_photo_folder`：演员照片目录
   - `actor_photo_kodi_auto`：演员照片 Kodi 自动

9. **水印设置 (Watermark Settings)**
   - `poster_mark`：海报水印
   - `thumb_mark`：缩略图水印
   - `fanart_mark`：背景图水印
   - `mark_size`：水印大小
   - `mark_type`：水印类型列表
   - `mark_fixed`：水印添加规则（not_fixed/fixed/corner）
   - `mark_pos`：水印规则为不固定时首个水印的位置
   - `mark_pos_corner`：水印规则为固定时的位置
   - `mark_pos_sub`：中文字幕水印位置
   - `mark_pos_mosaic`：马赛克类型水印位置
   - `mark_pos_hd`：清晰度水印位置

10. **网络设置 (Network Settings)**
    - `use_proxy`：是否使用代理
    - `proxy`：代理地址
    - `cf_bypass_url`：Cloudflare Bypass 地址
    - `cf_bypass_proxy`：Cloudflare Bypass 代理地址
    - `timeout`：超时
    - `retry`：重试次数
    - `theporndb_api_token`：ThePornDB API 令牌
    - `javdb`：JavDB
    - `fc2ppvdb`：FC2PPVDB
    - `javbus`：JavBus

11. **日志设置 (Log Settings)**
    - `show_web_log`：显示网页日志
    - `show_from_log`：显示来源日志
    - `show_data_log`：显示数据日志
    - `save_log`：保存日志

12. **其他设置 (Misc Settings)**
    - `update_check`：检查更新
    - `local_library`：本地库列表
    - `actors_name`：演员名称
    - `netdisk_path`：网盘路径
    - `localdisk_path`：本地磁盘路径
    - `window_title`：窗口标题
    - `switch_on`：功能开关列表
    - `timed_interval`：定时器间隔
    - `rest_count`：休息计数
    - `rest_time`：休息时间

**主要方法**：
- `get_site_config(site)`：获取网站配置
- `get_site_url(site, default)`：获取网站自定义 URL
- `get_field_config(field)`：获取字段配置
- `get_type_sites(scraping_type)`：获取类型网站
- `get_type_field_config(scraping_type, field)`：获取类型字段配置
- `set_type_field_sites(scraping_type, field, sites)`：设置类型字段网站
- `build_type_field_configs(scraping_type)`：构建类型字段配置
- `set_field_sites(field, sites)`：设置字段网站
- `set_field_language(field, language)`：设置字段语言
- `set_field_translate(field, translate)`：设置字段翻译
- `parse_sites(sites)`：解析网站列表
- `update(d)`：处理字段变更
- `from_legacy(data)`：从旧版配置创建
- `json_schema()`：获取 JSON Schema

#### `TranslateConfig`

翻译服务配置

**主要字段**：
- `translate_by`：翻译服务列表
- `baidu_appid`：百度 APP ID
- `baidu_key`：百度密钥
- `deepl_key`：DeepL 密钥
- `deeplx_url`：DeepLX URL
- `llm_url`：LLM API 地址
- `llm_model`：LLM 模型
- `llm_key`：LLM API 密钥
- `llm_prompt_title`：LLM 标题提示词
- `llm_prompt_outline`：LLM 简介提示词
- `llm_read_timeout`：LLM 读取超时（秒）
- `llm_max_req_sec`：LLM 每秒最大请求数
- `llm_max_try`：LLM 最大尝试次数
- `llm_temperature`：LLM 温度

#### `SiteConfig`

网站配置

**主要字段**：
- `custom_url`：自定义 URL

#### `FieldConfig`

字段配置

**主要字段**：
- `site_prority`：来源网站优先级
- `language`：语言偏好
- `translate`：是否翻译此字段

#### `FieldPriorityConfig`

字段优先级配置

**主要字段**：
- `site_prority`：来源网站优先级

#### `VsmetaCustomPreset`

VSMETA 自定义预设

**主要字段**：
- `name`：预设名称
- `show_title_type`：标题类型
- `show_title2_type`：副标题类型
- `summary_type`：简介类型
- `custom_title`：自定义标题
- `custom_title2`：自定义副标题
- `custom_summary`：自定义简介

### 配置枚举 ([mdcx/config/enums.py](file:///workspace/mdcx/config/enums.py))

#### `Website`

支持的网站枚举

**主要网站**：
- DMM
- MGStage
- Prestige
- Official
- JavBus
- Jav321
- JavDB
- JavDBAPI
- MissAV
- AVSoX
- MMTV
- MyWife
- FC2
- FC2Club
- FC2Hub
- FC2PPVDB
- ThePornDB（欧美）
- HDouban（国产）
- CNMDB（国产）
- GUOCHAN（国产）
- Madouqu（国产）
- 等等...

#### `FixedScrapingType`

刮削类型枚举

**类型**：
- `AUTO`：自动
- `YOUMA`：有码
- `WUMA`：无码
- `SUREN`：素人
- `FC2`：FC2
- `OUMEI`：欧美
- `GUOCHAN`：国产

#### 其他枚举

- `DownloadableFile`：可下载文件类型
- `KeepableFile`：可保留文件类型
- `ReadMode`：读取模式
- `Switch`：功能开关
- `Language`：语言
- `Translator`：翻译服务
- `NfoInclude`：NFO 包含内容
- `TagInclude`：标签包含内容
- `OutlineShow`：简介显示方式
- `FieldRule`：字段规则
- `SuffixSort`：后缀排序
- `CDChar`：CD 字符
- `CleanAction`：清理动作
- `NoEscape`：不转义
- `HDPicSource`：高清图片源
- `MarkType`：水印类型
- `EmbyAction`：Emby 动作
- `VsmetaShowTitle`：VSMETA 标题显示方式
- `VsmetaShowTitle2`：VSMETA 副标题显示方式
- `VsmetaSummary`：VSMETA 简介显示方式

### 配置管理器 ([mdcx/config/manager.py](file:///workspace/mdcx/config/manager.py))

管理配置的加载、保存、迁移等

**主要类**：
- `ConfigManager`：配置管理器
  - `__init__()`：初始化
  - `load()`：加载配置
  - `save()`：保存配置
  - `reset()`：重置为默认配置
  - `handle_v1()`：处理 V1 配置
  - `_replace_config()`：热切换配置
  - `acquire_computed()`：获取计算属性租约
  - `list_configs()`：列出配置文件
  - `write_mark_file()`：写入标记文件
  - `read_mark_file()`：读取标记文件

- `ComputedLease`：计算属性租约
  - 用于线程安全地访问计算属性

**配置加载流程**：
1. 检查标记文件确定配置路径
2. 尝试加载配置文件
3. 如果是旧版 .ini 配置，自动转换为新版
4. 验证配置
5. 应用配置

**配置迁移**：
- 支持从 V1 配置迁移到 V2
- 自动处理字段变更
- 保留用户自定义配置

---

## 爬虫系统

### 爬虫基类 ([mdcx/crawlers/base/base.py](file:///workspace/mdcx/crawlers/base/base.py))

#### `GenericBaseCrawler[T]`

泛型爬虫基类，所有具体爬虫均应继承此类并实现其抽象方法

**主要特性**：
- 支持自定义上下文类型
- 统一的爬虫生命周期管理
- 性能监控集成
- 爬虫健康监测集成
- 完善的错误处理

**主要方法**：
- `__init__(client, base_url, browser)`：初始化爬虫
- `close()`：释放资源
- `site()`：返回此爬虫对应的网站枚举（抽象方法）
- `base_url_()`：返回默认 URL（抽象方法）
- `display_name()`：返回前端显示名称
- `hidden_in_ui()`：是否在前端站点枚举中隐藏
- `supports_custom_url()`：是否支持在前端配置自定义网址
- `new_context(input)`：创建新上下文（抽象方法）
- `run(input)`：执行爬虫任务
- `_run(ctx)`：内部执行逻辑
- `_generate_search_url(ctx)`：生成搜索 URL（抽象方法）
- `_search(ctx, search_urls)`：执行搜索
- `_fetch_search(ctx, search_url)`：获取搜索页
- `_parse_search_page(ctx, selector, search_url)`：解析搜索页（抽象方法）
- `_detail(ctx, detail_urls)`：获取详情页
- `_fetch_detail(ctx, detail_url)`：获取详情页
- `_parse_detail_page(ctx, selector, detail_url)`：解析详情页（抽象方法）
- `post_process(ctx, data)`：后处理

**爬虫生命周期**：
1. 初始化爬虫实例
2. 创建上下文
3. 生成搜索 URL（或使用指定 URL）
4. 请求搜索页
5. 解析搜索页，获取详情页 URL
6. 请求详情页
7. 解析详情页，获取数据
8. 后处理
9. 返回结果

### 爬虫注册与获取

**主要机制**：
- 装饰器模式注册爬虫
- 工厂模式获取爬虫实例
- 懒加载优化性能

### 爬虫实现目录 ([mdcx/crawlers/](file:///workspace/mdcx/crawlers/))

每个网站一个爬虫文件，例如：
- `dmm_new/`：DMM 爬虫
- `javbus.py`：JavBus 爬虫
- `missav.py`：MissAV 爬虫
- 等等...

**添加新爬虫的步骤**：
1. 在 `mdcx/crawlers/` 下创建新文件
2. 继承 `BaseCrawler`（或 `GenericBaseCrawler`）
3. 实现抽象方法
4. 使用 `@register_crawler` 装饰器注册
5. 在 `Website` 枚举中添加对应网站

### 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))

#### `CrawlerProvider`

管理爬虫实例，提供获取和关闭功能

**主要方法**：
- `get(site)`：获取爬虫实例（懒加载）
- `close()`：关闭所有爬虫

**特点**：
- 懒加载：首次访问时创建爬虫实例
- 复用：同一网站的爬虫实例复用
- 资源管理：自动清理资源

---

## VSMETA 生成

### 概述

VSMETA 是 Synology Video Station 使用的二进制元数据格式，用于在群晖 NAS 上为视频文件提供元数据（如标题、演员、海报、评分等）。MDCx 完整实现了该格式，确保与 Synology Video Station 完全兼容。

### 核心文件

- **[mdcx/core/vsmeta.py](file:///workspace/mdcx/core/vsmeta.py)**：VSMETA 编码器核心实现

### 格式规范

VSMETA 使用 Protobuf 风格的二进制编码：

| 特性 | 说明 |
|------|------|
| **头部标识** | `0x08 0x01`（field 1, wire 0, value 1 = movie） |
| **标签编码** | `(field_number << 3) | wire_type` |
| **Wire Type 0** | Varint 整数 |
| **Wire Type 2** | Length-delimited（字符串、字节数组、子消息） |
| **图片格式** | Base64 编码的 JPEG，最大 200KB |
| **Base64 换行** | 每 76 字符换行 |
| **MD5 校验** | 基于 Base64 字符串计算 |

### 主要标签详解

#### 顶层标签

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 | 示例内容 |
|--------|----------|-------|------|----------|------|----------|
| `TAG_SHOW_TITLE` | 0x12 | 2 | 2 | string | 显示标题 | `[ABP-123] 作品标题` |
| `TAG_SHOW_TITLE2` | 0x1A | 3 | 2 | string | 排序/备用标题 | `Original Title` |
| `TAG_EPISODE_TITLE` | 0x22 | 4 | 2 | string | 简短标题（番号） | `ABP-123` |
| `TAG_YEAR` | 0x28 | 5 | 0 | varint | 年份 | `2024` |
| `TAG_EPISODE_RELEASE_DATE` | 0x32 | 6 | 2 | string | 发布日期 | `2024-01-15` |
| `TAG_EPISODE_LOCKED` | 0x38 | 7 | 0 | varint | 锁定元数据 | `1`（锁定） |
| `TAG_CHAPTER_SUMMARY` | 0x42 | 8 | 2 | string | 简介/剧情 | 日文标题+中日简介 |
| `TAG_EPISODE_META_JSON` | 0x4A | 9 | 2 | string | 外部 ID JSON | `{"external_ids": {...}}` |
| `TAG_GROUP1` | 0x52 | 10 | 2 | submessage | 演员、导演、类型 | 嵌套结构 |
| `TAG_CLASSIFICATION` | 0x5A | 11 | 2 | string | 内容分级 | `JP-18+` / `NC-17` |
| `TAG_RATING` | 0x60 | 12 | 0 | special | 评分（×10） | `85`（表示 8.5 分） |
| `TAG_EPISODE_THUMB_DATA` | 0x8A | 17 | 2 | string | 海报数据（含索引） | Base64 图片 |
| `TAG_EPISODE_THUMB_MD5` | 0x92 | 18 | 2 | string | 海报 MD5（含索引） | MD5 十六进制 |
| `TAG_GROUP2` | 0x9A | 19 | 2 | submessage | 剧集信息+海报 | 嵌套结构 |
| `TAG_GROUP3` | 0xAA | 21 | 2 | submessage | 背景图+时间戳 | 嵌套结构 |

#### GROUP1 内部标签（演员/导演/类型）

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 |
|--------|----------|-------|------|----------|------|
| `TAG1_CAST` | 0x0A | 1 | 2 | string (repeated) | 演员列表 |
| `TAG1_DIRECTOR` | 0x12 | 2 | 2 | string (repeated) | 导演列表 |
| `TAG1_GENRE` | 0x1A | 3 | 2 | string (repeated) | 类型/标签列表 |
| `TAG1_WRITER` | 0x22 | 4 | 2 | string (repeated) | 编剧列表（保留） |

#### GROUP2 内部标签（剧集信息）

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 |
|--------|----------|-------|------|----------|------|
| `TAG2_SEASON` | 0x08 | 1 | 0 | varint | 季数（电影为 0） |
| `TAG2_EPISODE` | 0x10 | 2 | 0 | varint | 集数（电影为 0） |
| `TAG2_TV_SHOW_YEAR` | 0x18 | 3 | 0 | varint | 电视剧年份 |
| `TAG2_RELEASE_DATE_TV_SHOW` | 0x22 | 4 | 2 | string | 电视剧发布日期 |
| `TAG2_LOCKED` | 0x28 | 5 | 0 | varint | 锁定电视剧元数据 |
| `TAG2_TV_SHOW_SUMMARY` | 0x32 | 6 | 2 | string | 系列名称 |
| `TAG2_POSTER_DATA` | 0x3A | 7 | 2 | string | 海报 Base64 数据 |
| `TAG2_POSTER_MD5` | 0x42 | 8 | 2 | string | 海报 MD5 |
| `TAG2_TV_SHOW_META_JSON` | 0x4A | 9 | 2 | string | 电视剧元数据 JSON |

#### GROUP3 内部标签（背景图）

| 标签名 | 十六进制 | Field | Wire | 数据类型 | 说明 |
|--------|----------|-------|------|----------|------|
| `TAG3_BACKDROP_DATA` | 0x0A | 1 | 2 | string | 背景图 Base64 数据 |
| `TAG3_BACKDROP_MD5` | 0x12 | 2 | 2 | string | 背景图 MD5 |
| `TAG3_TIMESTAMP` | 0x18 | 3 | 0 | varint | Unix 时间戳 |

### 核心类：VSMetaEncoder

**主要方法**：

| 方法 | 功能 | 示例 |
|------|------|------|
| `__init__()` | 初始化编码器 | - |
| `reset()` | 重置编码器状态 | - |
| `write_header()` | 写入文件头 `0x08 0x01` | - |
| `write_string_field(tag, value)` | 写入字符串字段 | `write_string_field(0x12, "标题")` |
| `write_varint_field(tag, value)` | 写入 Varint 整数字段 | `write_varint_field(0x28, 2024)` |
| `write_bytes_field(tag, data)` | 写入字节字段 | `write_bytes_field(0x8A, b"...")` |
| `write_indexed_string_field(tag, index, value)` | 写入带索引的字符串 | `write_indexed_string_field(0x8A, 0x01, base64_data)` |
| `write_submessage(tag, build_func, index)` | 写入嵌套子消息 | `write_submessage(0x52, build_group1)` |
| `write_poster(image_path)` | 写入海报图片 | `write_poster(Path("poster.jpg"))` |
| `write_poster_in_group2(image_path)` | 在 GROUP2 中写入海报 | - |
| `write_backdrop_in_group3(image_path)` | 在 GROUP3 中写入背景图 | - |
| `write_rating(score_str)` | 写入评分 | `write_rating("8.5")` |
| `normalize_vsmeta_text(text)` | 清理文本中的控制字符和 HTML 实体 | - |
| `get_bytes()` | 获取最终的 VSMETA 字节数据 | - |

### VSMETA 自定义模板系统

MDCx 支持使用自定义模板来格式化 VSMETA 文件的标题、副标题和简介。

**支持的占位符**：
- `{number}`：作品番号
- `{title}`：中文标题
- `{originaltitle}`：原始标题（通常是日文）
- `{publisher}`：发行商
- `{studio}`：制作商
- `{series}`：系列
- `{actors}`：演员列表（前 3 个，逗号分隔）
- `{actors_full}`：完整演员列表（所有）
- `{all_actors}`：所有演员（前 3 个）
- `{all_actors_full}`：完整所有演员列表
- `{actor}`：第一个演员
- `{outline}`：中文简介
- `{originalplot}`：原始剧情简介
- `{year}`：年份
- `{release}`：发行日期
- `{score}`：评分
- `{country}`：国家
- `{director}`：导演
- `{director_list}`：导演列表（逗号分隔）
- `{genre}`：类型/标签（前 5 个，逗号分隔）
- `{mosaic}`：马赛克类型
- `{runtime}`：片长
- `{label}`：标签（同 publisher）
- `{website}`：网站
- `{letters}`：番号字母前缀
- `{wanted}`：想看数
- `{tag}`：标签（逗号分隔）
- `{tags_list}`：标签列表（同 tag）
- `{thumb}`：缩略图 URL
- `{poster}`：海报 URL
- `{trailer}`：预告片 URL
- `{extrafanart}`：额外剧照 URL（逗号分隔）

**条件语法**：
```
{number} - {title}{if:director} (导演: {director}){/if}
```

**默认值语法**：
```
{title|无标题}
```

### 简介格式详解

VSMETA 的简介字段（`TAG_CHAPTER_SUMMARY`）支持多种预定义格式：

1. `JP_ZH_JP`：日文标题 + 中文简介 + 日文简介
2. `OUTLINE`：仅中文简介
3. `ORIGINALPLOT`：仅日文简介
4. `ZH_JP`：中文简介 + 日文简介
5. `JP_ZH`：日文标题 + 中文简介
6. `TITLE_ONLY`：仅标题
7. `OUTLINE_PUBLISHER`：中文简介 + 发行商/工作室信息
8. `NUMBER_TITLE`：番号 + 标题

### 配置选项

在 `Config` 类中提供了丰富的 VSMETA 配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `vsmeta_include_poster` | bool | `True` | 是否在 VSMETA 中嵌入封面图 |
| `vsmeta_include_backdrop` | bool | `True` | 是否在 VSMETA 中嵌入背景图 |
| `vsmeta_locked` | bool | `True` | 是否锁定元数据（禁止 Video Station 自动更新） |
| `vsmeta_image_max_dimension` | int | `1920` | 图片最大尺寸（像素） |
| `vsmeta_jpeg_quality` | int | `90` | JPEG 质量（1-100） |
| `vsmeta_actor_limit` | int | `20` | 演员数量上限 |
| `vsmeta_tag_limit` | int | `10` | 标签数量上限 |
| `vsmeta_keep_ext` | bool | `False` | 生成的 VSMETA 文件是否保留视频扩展名 |
| `vsmeta_show_title` | enum | `TITLE` | 标题显示方式 |
| `vsmeta_show_title2` | enum | `ORIGINALTITLE` | 副标题显示方式 |
| `vsmeta_summary` | enum | `JP_ZH_JP` | 简介显示方式 |
| `vsmeta_custom_title` | string | `"{number} - {title} ({originaltitle})"` | 标题自定义模板 |
| `vsmeta_custom_title2` | string | `"{publisher} / {studio}"` | 副标题自定义模板 |
| `vsmeta_custom_summary` | string | `"{originaltitle}\n\n{outline}\n\n{originalplot}"` | 简介自定义模板 |

### 关键特性

1. **格式兼容性**：与 JuanWoo/nfo-to-vsmeta 项目完全一致，确保被 Synology Video Station 识别
2. **字符清理**：自动清理控制字符和 HTML 转义实体（`normalize_vsmeta_text`）
3. **图片压缩**：自动将图片压缩到 200KB 以内
4. **原子写入**：使用临时文件 → 重命名的方式确保写入不会损坏
5. **完整错误处理**：完善的异常处理和日志记录
6. **高度可配置**：多项配置选项满足不同需求

### 实际生成的 VSMETA 结构示例

```
0x08 0x01                              # HEADER_MOVIE (field 1, value 1)
0x12 len(title) [title bytes]         # TAG_SHOW_TITLE
0x1A len(title2) [title2 bytes]       # TAG_SHOW_TITLE2
0x22 len(number) [number bytes]       # TAG_EPISODE_TITLE
0x28 [year varint]                    # TAG_YEAR
0x32 len(date) [date bytes]           # TAG_EPISODE_RELEASE_DATE
0x38 0x01                             # TAG_EPISODE_LOCKED (locked)
0x42 len(summary) [summary bytes]     # TAG_CHAPTER_SUMMARY
0x4A len(json) [json bytes]           # TAG_EPISODE_META_JSON
0x52 len(group1) [group1 bytes]       # TAG_GROUP1 (cast/director/genre)
0x5A len(classification) [...]        # TAG_CLASSIFICATION
0x60 [rating byte]                    # TAG_RATING
0x8A 0x01 len(data) [base64 data]     # TAG_EPISODE_THUMB_DATA (with index)
0x92 0x01 len(md5) [md5 bytes]        # TAG_EPISODE_THUMB_MD5 (with index)
0x9A 0x01 len(group2) [group2 bytes]  # TAG_GROUP2 (with index)
0xAA 0x01 len(group3) [group3 bytes]  # TAG_GROUP3 (with index)
```

### 写入流程

`write_vsmeta()` 函数的完整流程：

1. 创建 `VSMetaEncoder` 实例
2. 写入文件头
3. 根据配置写入标题、副标题、番号、年份、发布日期等字段
4. 构建并写入 GROUP1（演员、导演、标签）
5. 写入内容分级和评分
6. 写入海报（如果配置启用）
7. 构建并写入 GROUP2（剧集信息、海报）
8. 构建并写入 GROUP3（背景图、时间戳）
9. 获取字节数据
10. 原子写入文件（临时文件 → 重命名）

---

## 工具类与辅助函数

### 工具函数 ([mdcx/utils/__init__.py](file:///workspace/mdcx/utils/__init__.py))

#### `AsyncBackgroundExecutor`

异步后台任务执行器

**主要方法**：
- `submit(coro)`：提交协程
- `run(coro)`：阻塞运行协程
- `wait_all(timeout)`：等待所有任务完成
- `cancel()`：取消所有任务

**其他工具函数**：
- `get_current_time()`：获取当前时间
- `get_used_time(start_time)`：计算耗时
- `add_html(text)`：添加 HTML 链接
- `get_random_headers()`：生成随机 HTTP 头
- `singleton(cls)`：单例装饰器
- 等等...

### 文件工具 ([mdcx/utils/file.py](file:///workspace/mdcx/utils/file.py))

文件相关工具函数

### 路径工具 ([mdcx/utils/path.py](file:///workspace/mdcx/utils/path.py))

路径相关工具函数

### 视频工具 ([mdcx/utils/video.py](file:///workspace/mdcx/utils/video.py))

视频相关工具函数

### LEB128 编码 ([mdcx/utils/leb128.py](file:///workspace/mdcx/utils/leb128.py))

用于 VSMETA 格式的 Varint 编码

### VSMETA 模板助手 ([mdcx/utils/vsmeta_template_helper.py](file:///workspace/mdcx/utils/vsmeta_template_helper.py))

VSMETA 模板验证和渲染辅助

### 爬虫健康监测 ([mdcx/utils/crawler_health.py](file:///workspace/mdcx/utils/crawler_health.py))

监控爬虫状态和性能

### 性能工具 ([mdcx/utils/perf.py](file:///workspace/mdcx/utils/perf.py))

性能监控和计时工具

### 数据类工具 ([mdcx/utils/dataclass.py](file:///workspace/mdcx/utils/dataclass.py))

数据类操作工具

### 语言工具 ([mdcx/utils/language.py](file:///workspace/mdcx/utils/language.py))

语言检测和转换工具

---

## 控制器层

### 主窗口控制器 ([mdcx/controllers/main_window/](file:///workspace/mdcx/controllers/main_window/))

#### `MyMAinWindow`

主窗口控制器（[main_window.py](file:///workspace/mdcx/controllers/main_window/main_window.py)）

**主要功能**：
- 初始化 UI
- 绑定事件处理
- 管理配置加载和保存
- 处理刮削任务

**主要文件**：
- `main_window.py`：主窗口类
- `init.py`：初始化
- `handlers.py`：事件处理
- `load_config.py`：加载配置
- `save_config.py`：保存配置
- `bind_utils.py`：绑定工具
- `style.py`：样式
- `site_priority_dialog.py`：站点优先级对话框
- `performance_dialog.py`：性能对话框

---

## 项目运行方式

### 开发模式

1. **安装依赖**
   ```bash
   # 使用 uv（推荐）
   uv sync --locked --all-extras --dev

   # 或使用 pip
   pip install -e .
   ```

2. **运行程序**
   ```bash
   # 使用 uv
   uv run python main.py

   # 或直接运行
   python main.py
   ```

### 打包发布

使用 `scripts/build.py` 进行打包：

```bash
# 使用 uv
uv run python scripts/build.py

# 或直接运行
python scripts/build.py
```

**GitHub Actions 构建**：
项目配置了完整的 CI/CD 流程，可通过 GitHub Actions 自动构建多平台版本。

### 命令行工具

项目提供了命令行工具：

1. **crawl**：命令行刮削
   ```bash
   # 使用 uv
   uv run python -m mdcx.cmd.crawl

   # 或直接运行
   python -m mdcx.cmd.crawl
   ```

2. **gen_enums**：生成枚举
   ```bash
   uv run python -m mdcx.cmd.gen_enums
   ```

### 测试

运行测试：

```bash
# 运行所有测试
uv run pytest tests/

# 运行测试并生成覆盖率报告
uv run pytest tests/ --cov=mdcx --cov-report=html

# 运行特定测试
uv run pytest tests/core/test_scraper.py
```

### 代码规范

项目使用 `ruff` 进行代码检查：

```bash
# 代码检查
uv run ruff check .

# 自动修复
uv run ruff check . --fix
```

---

## 依赖关系

### 主要依赖 ([pyproject.toml](file:///workspace/pyproject.toml))

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | >= 3.13.4 | 运行时 |
| PyQt6 | 6.11.0 | GUI 框架 |
| httpx | >=0.28.1 | 异步 HTTP 客户端 |
| curl-cffi | 0.11.4 | HTTP 请求（支持 Cloudflare 绕过） |
| beautifulsoup4 | 4.13.4 | HTML 解析 |
| parsel | >=1.10.0 | 选择器解析 |
| lxml | >=5.2.0 | XML/HTML 解析 |
| pillow | 11.3.0 | 图像处理 |
| opencv-contrib-python-headless | 4.13.0.92 | 图像处理（人脸检测等） |
| av | >=15.0.0 | 视频处理 |
| pydantic-settings | >=2.10.1 | 配置管理 |
| openai | 1.91.0 | LLM 翻译 |
| zhconv | 1.4.3 | 中文简繁转换 |
| aiofiles | 24.1.0 | 异步文件操作 |
| aiolimiter | 1.2.1 | 异步限流 |
| oshash | 0.1.1 | OpenSubtitles 哈希 |
| jinja2 | >=3.1.6 | 模板引擎 |
| ping3 | 4.0.4 | 网络检查 |

### 开发依赖

| 依赖 | 用途 |
|------|------|
| pytest | 测试框架 |
| pytest-asyncio | 异步测试 |
| pytest-cov | 测试覆盖率 |
| pyinstaller | 打包工具 |
| ruff | 代码检查 |
| rich | 终端富文本 |
| typer | 命令行工具 |
| types-lxml | 类型注解 |

---

## 关键类关系图

```
Scraper (core/scraper.py)
  │
  ├─> CrawlerProvider (crawler.py)
  │     │
  │     └─> GenericBaseCrawler (crawlers/base/base.py)
  │           ├─> DMMNewCrawler
  │           ├─> JavBusCrawler
  │           ├─> MissAVCrawler
  │           └─> ... (40+ 爬虫)
  │
  ├─> FileScraper (core/file_crawler.py)
  │
  ├─> MediaResourceContext (core/media_resource.py)
  │
  ├─> write_nfo (core/nfo.py)
  │
  └─> write_vsmeta (core/vsmeta.py)


Config (config/models.py)
  │
  ├─> TranslateConfig
  ├─> SiteConfig
  ├─> FieldConfig
  └─> Computed (config/computed.py)


数据流程：
FileInfo ──> CrawlTask ──> [Crawlers] ──> CrawlersResult ──> (translation) ──> NFO / VSMETA / Files
```

---

## 开发注意事项

1. **异步编程**：项目大量使用 asyncio，注意协程安全
2. **配置迁移**：配置版本管理，支持旧配置迁移
3. **平台兼容性**：注意 Windows/macOS/Linux 的差异
4. **爬虫更新**：网站结构变化时需要更新对应爬虫
5. **测试**：新增功能需添加对应测试
6. **类型注解**：项目使用类型注解，保持类型安全

---

## 扩展开发

### 添加新的爬虫

1. 在 `mdcx/crawlers/` 下创建新文件
2. 继承 `BaseCrawler`（或 `GenericBaseCrawler`）
3. 实现抽象方法：
   - `site()`：返回网站枚举
   - `base_url_()`：返回默认 URL
   - `new_context()`：创建上下文
   - `_generate_search_url()`：生成搜索 URL
   - `_parse_search_page()`：解析搜索页
   - `_parse_detail_page()`：解析详情页
4. 使用 `@register_crawler` 装饰器注册
5. 在 `Website` 枚举中添加对应网站（如需要）

### 添加新的翻译服务

1. 在 `Translator` 枚举中添加
2. 在 `core/translate.py` 中实现对应翻译函数
3. 在 `TranslateConfig` 中添加配置（如需要）

### 自定义 VSMETA 模板

1. 在配置中设置 `vsmeta_show_title`、`vsmeta_show_title2`、`vsmeta_summary` 为 `CUSTOM`
2. 设置对应的自定义模板：
   - `vsmeta_custom_title`
   - `vsmeta_custom_title2`
   - `vsmeta_custom_summary`
3. 使用占位符和条件语法

---

## 参考资料

- **用户文档**：[USER_GUIDE.md](file:///workspace/USER_GUIDE.md)
- **开发文档**：[DEVELOPMENT.md](file:///workspace/DEVELOPMENT.md)
- **贡献指南**：[CONTRIBUTING.md](file:///workspace/CONTRIBUTING.md)
- **FAQ**：[FAQ.md](file:///workspace/FAQ.md)
- **安装指南**：[INSTALL.md](file:///workspace/INSTALL.md)
- **架构设计**：[docs/architecture.md](file:///workspace/docs/architecture.md)
- **VSMETA 对比**：[VSMETA_COMPARISON.md](file:///workspace/VSMETA_COMPARISON.md)
- **GitHub 仓库**：https://github.com/1525745393/mdcx-AI
- **Telegram 群**：https://t.me/mdcx_chat

---

## 附录

### 术语表

| 术语 | 说明 |
|------|------|
| 番号 | 视频的唯一标识符，如 ABP-123 |
| 刮削 | 从网站获取视频元数据的过程 |
| NFO | 游戏/视频元数据文件格式（XML） |
| VSMETA | Synology Video Station 使用的二进制元数据格式 |
| 马赛克 | 视频的马赛克类型（有码/无码/素人等） |
| 素人 | 非职业 AV 女优 |
| FC2 | 日本个人视频分享网站 |

### 项目历史

MDCx 项目源自多个开源项目的演进：

1. **Movie_Data_Capture**：最初的命令行工具（现已闭源）
2. **AVDC**：添加了 PyQt 图形界面（已停止维护）
3. **MDCx**：继续改进和优化
4. **当前版本**：基于 sqzw-x/mdcx，持续维护和优化

---

*文档生成时间：2026-06-03*
*最后更新：2026-06-03*
