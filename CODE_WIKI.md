# MDCx Code Wiki

## 目录

1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [核心模块](#核心模块)
4. [数据模型](#数据模型)
5. [配置系统](#配置系统)
6. [爬虫系统](#爬虫系统)
7. [工具类与辅助函数](#工具类与辅助函数)
8. [项目运行方式](#项目运行方式)
9. [依赖关系](#依赖关系)

---

## 项目概述

### 项目简介

MDCx 是一个影视元数据抓取和整理工具，主要用于从多个成人视频网站获取元数据信息，包括标题、简介、演员、标签、封面图等，并支持与 Emby 等媒体服务器集成。

### 历史沿革

- 上游项目：yoshiko2/Movie_Data_Capture（已闭源）
- 后续分支：moyy996/AVDC（已停止维护）
- 基于：sqzw-x/mdcx
- 当前：Hazard804/mdcx

### 核心功能

1. 支持多个数据源网站抓取
2. 多线程并发处理
3. 元数据翻译（支持多种翻译服务）
4. 文件整理和重命名
5. 图片下载和水印添加
6. NFO 生成
7. Emby/Jellyfin 集成
8. 软链接创建
9. 多语言支持

---

## 项目架构

### 目录结构

```
/workspace/
├── main.py                 # 程序入口
├── mdcx/                   # 主源码目录
│   ├── base/               # 基础功能模块
│   ├── cmd/                # 命令行工具
│   ├── config/             # 配置管理
│   ├── controllers/        # 控制器（业务逻辑）
│   ├── core/               # 核心功能
│   ├── crawlers/           # 爬虫实现
│   ├── gen/                # 自动生成的枚举
│   ├── models/             # 数据模型
│   ├── tools/              # 工具模块
│   ├── utils/              # 工具函数
│   ├── views/              # UI 视图
│   ├── consts.py           # 常量定义
│   ├── crawler.py          # 爬虫提供者
│   ├── number.py           # 番号识别
│   ├── signals.py          # 信号系统
│   └── web_async.py        # 异步 web 请求
├── resources/              # 资源文件
│   ├── Img/                # 图片资源
│   ├── config/             # 默认配置
│   ├── fonts/              # 字体文件
│   └── mapping_table/      # 映射表
├── tests/                  # 测试代码
├── scripts/                # 脚本工具
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

### 架构分层

1. **表现层（Views）**：PyQt6 图形界面
2. **控制层（Controllers）**：业务逻辑和事件处理
3. **核心层（Core）**：刮削、文件处理、NFO 生成等
4. **数据层（Models）**：数据模型定义
5. **基础设施层**：爬虫、配置、网络请求等

### 主要模块依赖关系

```
main.py
  └─> controllers/main_window/
        └─> core/scraper.py
              └─> crawler.py
                    └─> crawlers/
              ├─> core/file_crawler.py
              ├─> core/nfo.py
              ├─> core/media_resource.py
              └─> config/manager.py
```

---

## 核心模块

### 1. 入口模块 ([main.py](file:///workspace/main.py))

**功能**：程序启动入口，初始化 GUI 应用

**主要类/函数**：
- `show_constants()`：显示运行时常量
- 主程序入口：初始化 PyQt6 应用，加载配置，显示主窗口

### 2. 常量定义 ([mdcx/consts.py](file:///workspace/mdcx/consts.py))

**功能**：定义项目常量

**主要常量**：
- `LOCAL_VERSION`：本地版本号
- `GITHUB_REPO`：GitHub 仓库地址
- `GITHUB_RELEASES_URL`：发布页地址
- `IS_WINDOWS`、`IS_MAC`、`IS_DOCKER`：平台判断
- `MAIN_PATH`：主路径
- `MARK_FILE`：配置标记文件

### 3. 信号系统 ([mdcx/signals.py](file:///workspace/mdcx/signals.py))

**功能**：PyQt6 信号定义，用于组件间通信

### 4. 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))

**功能**：管理和提供爬虫实例

**主要类**：
- `CrawlerProvider`：爬虫提供者，管理爬虫实例生命周期

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

**主要方法**：
- `crawler_input()`：转换为爬虫输入
- `crawl_task()`：转换为刮削任务

#### `CrawlerInput`
单个爬虫调用输入

#### `CrawlTask`
单个文件刮削任务

#### `BaseCrawlerResult`
爬虫结果基础类型

**主要字段**：
- `number`、`title`、`outline`、`actors`、`tags` 等元数据
- `poster`、`thumb`、`trailer` 等资源 URL

#### `CrawlerResult`
单一网站爬虫结果

#### `CrawlersResult`
整合所有网站的结果

#### `OtherInfo`
其他处理信息（文件移动、水印等）

---

## 配置系统

### 配置模型 ([mdcx/config/models.py](file:///workspace/mdcx/config/models.py))

#### `Config`
主配置类，基于 Pydantic

**主要配置区域**：

1. **General Settings（通用设置）**
   - `media_path`：媒体路径
   - `success_output_folder`：成功输出目录
   - `media_type`：媒体文件类型
   - `sub_type`：字幕文件类型

2. **Cleaning Settings（清理设置）**
   - `folders`：排除目录
   - `string`：需要从文件名删除的字符串
   - `clean_enable`：启用的清理规则

3. **Scraping Settings（刮削设置）**
   - `thread_number`：并发数
   - `download_files`：下载文件类型
   - `website_youma`：有码网站源
   - `website_wuma`：无码网站源
   - `website_fc2`：FC2 网站源
   - 等等...

4. **字段配置**
   - `field_configs`：各字段的网站优先级、语言、翻译开关

5. **Naming and Formatting（命名和格式化）**
   - `folder_name`：目录名模板
   - `naming_file`：文件名模板
   - `nfo_include_new`：NFO 包含内容

6. **Server Settings（服务器设置）**
   - `server_type`：服务器类型（emby/jellyfin）
   - `emby_url`：Emby 地址
   - `api_key`：API 密钥

7. **Watermark Settings（水印设置）**
   - `poster_mark`、`thumb_mark`、`fanart_mark`：水印开关
   - `mark_type`：水印类型
   - `mark_size`：水印大小

8. **Network Settings（网络设置）**
   - `use_proxy`：代理开关
   - `proxy`：代理地址
   - `timeout`：超时时间
   - `retry`：重试次数

9. **Translation Settings（翻译设置）**
   - `translate_config`：翻译配置（TranslateConfig）

#### `TranslateConfig`
翻译服务配置

**主要字段**：
- `translate_by`：翻译服务列表
- `baidu_appid`、`baidu_key`：百度翻译配置
- `deepl_key`：DeepL 配置
- `llm_url`、`llm_model`、`llm_key`：LLM 翻译配置

### 配置枚举 ([mdcx/config/enums.py](file:///workspace/mdcx/config/enums.py))

#### `Website`
支持的网站枚举

**主要网站**：
- DMM、MGSTAGE、PRESTIGE、OFFICIAL（官方）
- JAVBUS、JAV321、JAVDB、JAVDBAPI
- MISSAV、AVSOX、MMTV、MYWIFE
- FC2、FC2HUB、FC2CLUB、FC2PPVDB
- THEPORNDB（欧美）
- HDOUBAN、CNMDB、GUOCHAN、MADOUQU（国产）
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
- `Language`：语言
- `Translator`：翻译服务
- 等等...

### 配置管理器 ([mdcx/config/manager.py](file:///workspace/mdcx/config/manager.py))

管理配置的加载、保存、迁移等

---

## 爬虫系统

### 爬虫基类 ([mdcx/crawlers/base/base.py](file:///workspace/mdcx/crawlers/base/base.py))

#### `GenericBaseCrawler[T]`
爬虫抽象基类

**主要方法**：
- `run(input)`：执行爬虫
- `_generate_search_url(ctx)`：生成搜索 URL（抽象）
- `_parse_search_page(ctx, html, search_url)`：解析搜索页（抽象）
- `_parse_detail_page(ctx, html, detail_url)`：解析详情页（抽象）
- `post_process(ctx, res)`：后处理

**生命周期**：
1. 生成搜索 URL
2. 请求搜索页
3. 解析搜索页，获取详情页 URL
4. 请求详情页
5. 解析详情页，获取数据
6. 后处理

#### `BaseCrawler`
基础爬虫实现（使用默认 Context）

### 爬虫注册与获取

**主要函数**：
- `register_crawler(crawler_cls)`：注册爬虫
- `get_crawler(site)`：获取网站爬虫

### 爬虫实现目录 ([mdcx/crawlers/](file:///workspace/mdcx/crawlers/))

每个网站一个爬虫文件，例如：
- `dmm_new/`：DMM 爬虫
- `javbus.py`：JavBus 爬虫
- `missav.py`：MissAV 爬虫
- 等等...

### 爬虫提供者 ([mdcx/crawler.py](file:///workspace/mdcx/crawler.py))

#### `CrawlerProvider`
管理爬虫实例，提供获取和关闭功能

**主要方法**：
- `get(site)`：获取爬虫实例（懒加载）
- `close()`：关闭所有爬虫

### 核心刮削器 ([mdcx/core/scraper.py](file:///workspace/mdcx/core/scraper.py))

#### `Scraper`
主刮削器类

**主要方法**：
- `run(file_mode, movie_list)`：执行刮削
- `process_one_file(task)`：处理单个文件
- `_process_one_file(file_info, file_mode)`：内部处理

**刮削流程**：
1. 获取文件信息
2. 调用爬虫获取数据
3. 翻译元数据
4. 下载图片和预告片
5. 添加水印
6. 生成 NFO
7. 移动和重命名文件
8. 创建软链接（可选）

### 文件刮削器 ([mdcx/core/file_crawler.py](file:///workspace/mdcx/core/file_crawler.py))

#### `FileScraper`
处理单个文件的刮削逻辑

**主要功能**：
- 识别番号和刮削类型
- 调用多个网站爬虫
- 整合各网站结果
- 字段优先级处理

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

---

## 核心功能模块

### NFO 生成 ([mdcx/core/nfo.py](file:///workspace/mdcx/core/nfo.py))

生成符合 Kodi/Emby 规范的 NFO 文件

### 媒体资源处理 ([mdcx/core/media_resource.py](file:///workspace/mdcx/core/media_resource.py))

处理图片、预告片等媒体资源下载

### 翻译功能 ([mdcx/core/translate.py](file:///workspace/mdcx/core/translate.py))

支持多种翻译服务：
- Google
- Baidu
- DeepL
- DeepLX
- LLM（大语言模型）

### 图片处理 ([mdcx/core/image.py](file:///workspace/mdcx/core/image.py))

图片下载、水印添加等

### 命名模板 ([mdcx/core/naming/](file:///workspace/mdcx/core/naming/))

文件和目录命名模板系统

---

## 项目运行方式

### 开发模式

1. **安装依赖**
   ```bash
   pip install -e .
   # 或使用 uv
   uv sync
   ```

2. **运行程序**
   ```bash
   python main.py
   ```

### 打包发布

使用 `scripts/build.py` 进行打包

### 命令行工具

项目提供了命令行工具：

1. **crawl**：命令行刮削
   ```bash
   python -m mdcx.cmd.crawl
   ```

2. **gen_enums**：生成枚举
   ```bash
   python -m mdcx.cmd.gen_enums
   ```

### 测试

运行测试：
```bash
pytest tests/
```

---

## 依赖关系

### 主要依赖 ([pyproject.toml](file:///workspace/pyproject.toml))

| 依赖 | 用途 |
|------|------|
| Python | >= 3.13.4 |
| PyQt6 | GUI 框架 |
| httpx | 异步 HTTP 请求 |
| curl-cffi | HTTP 请求（支持 Cloudflare） |
| beautifulsoup4 | HTML 解析 |
| parsel | 选择器解析 |
| lxml | XML/HTML 解析 |
| pillow | 图片处理 |
| opencv-contrib-python-headless | 图片处理 |
| av | 视频处理 |
| pydantic-settings | 配置管理 |
| openai | LLM 翻译 |
| zhconv | 中文简繁转换 |
| aiofiles | 异步文件操作 |
| aiolimiter | 异步限流 |
| oshash | OpenSubtitles 哈希 |
| jinja2 | 模板引擎 |
| ping3 | 网络检查 |

### 开发依赖

- pytest
- pytest-asyncio
- pytest-cov
- pyinstaller
- ruff
- rich
- typer

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
  │           └─> ...
  │
  ├─> FileScraper (core/file_crawler.py)
  │
  ├─> MediaResourceContext (core/media_resource.py)
  │
  └─> write_nfo (core/nfo.py)


Config (config/models.py)
  │
  ├─> TranslateConfig
  ├─> SiteConfig
  └─> FieldConfig


数据流程：
FileInfo ──> CrawlTask ──> [Crawlers] ──> CrawlersResult ──> (translation) ──> NFO / Files
```

---

## 开发注意事项

1. **异步编程**：项目大量使用 asyncio，注意协程安全
2. **配置迁移**：配置版本管理，支持旧配置迁移
3. **平台兼容性**：注意 Windows/macOS/Linux 的差异
4. **爬虫更新**：网站结构变化时需要更新对应爬虫
5. **测试**：新增功能需添加对应测试

---

## 扩展开发

### 添加新的爬虫

1. 在 `mdcx/crawlers/` 下创建新文件
2. 继承 `BaseCrawler`
3. 实现抽象方法
4. 使用 `@register_crawler` 装饰器注册
5. 在 `Website` 枚举中添加对应网站

### 添加新的翻译服务

1. 在 `Translator` 枚举中添加
2. 在 `core/translate.py` 中实现对应翻译函数
3. 在 `TranslateConfig` 中添加配置（如需要）

---

*文档生成时间：2026-05-22*
