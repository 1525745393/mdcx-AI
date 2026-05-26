# MDCx 项目完整 Code Wiki

## 目录
1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [核心模块详解](#核心模块详解)
4. [爬虫框架](#爬虫框架)
5. [业务流程](#业务流程)
6. [VSMETA 生成](#vsmeta-生成-synology-video-station)
7. [配置管理](#配置管理)
8. [数据模型](#数据模型)
9. [依赖关系](#依赖关系)
10. [项目运行方式](#项目运行方式)
11. [开发指南](#开发指南)

---

## 项目概述

### 简介

MDCx 是一个现代化的视频元数据刮削和管理工具，用于从 40+ 个网站自动获取视频信息，生成符合 KODI/Emby 规范的 NFO 文件，并提供完整的图片处理和翻译功能。

### 核心特性

- 🤖 **智能刮削**: 支持 40+ 个数据源，自动识别番号
- 📄 **NFO 生成**: 生成符合 KODI/Emby 规范的元数据文件
- 📺 **VSMETA 支持**: 完整实现 Synology Video Station 的 VSMETA 格式
- 🖼️ **图片处理**: 自动下载、裁剪、添加水印
- 🌐 **多语言翻译**: 支持 Google/DeepL/LLM 翻译
- 📁 **灵活命名**: Jinja2 模板系统，支持自定义命名规则
- 🔍 **Amazon 集成**: 条码识别，自动匹配封面
- ⚡ **异步处理**: 高效的并发刮削能力
- 🧪 **全面测试**: 59+ 个单元测试，覆盖率 42%+

### 技术栈

- **语言**: Python 3.13+
- **GUI 框架**: PyQt6
- **爬虫**: httpx, curl_cffi, BeautifulSoup4, Parsel
- **数据处理**: Pydantic, Jinja2
- **异步**: asyncio, aiofiles
- **图像处理**: Pillow, OpenCV
- **构建**: PyInstaller, uv

---

## 项目架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      UI Layer (PyQt6)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ MainWindow   │  │ SettingsUI   │  │ ProgressUI   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Controller Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ EventHandler │  │ ConfigMgr    │  │ SignalBus    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Core Business Logic                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Scraper      │  │ FileCrawler  │  │NamingSystem  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ NFO Gen      │  │ Amazon OCR   │  │ Translator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Crawler Framework                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          GenericBaseCrawler[T]                     │   │
│  │  ┌──────┐ ┌──────┐ ┌─────┐ ┌──────┐                 │   │
│  │  │JAVBus│ │JAVLib│ │ DMM │ │ FC2  │ ... 40+ 个      │   │
│  │  └──────┘ └──────┘ └─────┘ └──────┘ 爬虫实现         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                Infrastructure Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ HTTP Client  │  │ File System  │  │ Image Proc   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 目录结构

```
/workspace/
├── mdcx/                      # 主源码目录
│   ├── base/                 # 基础工具模块
│   ├── cmd/                  # 命令行工具
│   ├── config/               # 配置管理
│   ├── controllers/          # 控制器层
│   ├── core/                 # 核心业务逻辑
│   ├── crawlers/             # 爬虫实现
│   ├── gen/                  # 生成的代码
│   ├── models/               # 数据模型
│   ├── tools/                # 工具类
│   ├── utils/                # 工具函数
│   ├── views/                # UI 视图
│   ├── browser.py            # 浏览器功能
│   ├── consts.py             # 常量定义
│   ├── crawler.py            # 爬虫管理器
│   ├── image.py              # 图像处理
│   ├── manual.py             # 手动配置
│   ├── network_fingerprint.py # 网络指纹
│   ├── signals.py            # 信号系统
│   └── web_async.py          # 异步 HTTP 客户端
├── resources/                # 资源文件
├── scripts/                  # 构建脚本
├── tests/                    # 测试目录
├── main.py                   # 主入口文件
└── pyproject.toml            # 项目配置
```

---

## 核心模块详解

### 1. 主入口 (`main.py`)

应用程序的入口点，负责初始化 PyQt6 应用、设置 UI 主题、创建主窗口。

**关键文件**: [main.py](file:///workspace/main.py)

**主要功能**:
- 设置高 DPI 缩放策略
- 初始化 QApplication
- 应用程序主题设置
- 创建并显示主窗口

### 2. 常量定义 (`consts.py`)

定义项目全局常量，包括版本信息、路径配置、平台判断等。

**关键文件**: [consts.py](file:///workspace/mdcx/consts.py)

**主要常量**:
- `LOCAL_VERSION`: 本地版本号
- `MAIN_PATH`: 主路径（根据运行环境自动判断）
- `IS_WINDOWS`, `IS_MAC`, `IS_DOCKER`: 平台判断
- `IS_PYINSTALLER`: 是否为打包版本

### 3. 信号系统 (`signals.py`)

基于 PyQt6 的信号槽机制，实现模块间的解耦通信。

---

## 爬虫框架

### 架构概述

MDCx 的爬虫框架采用了泛型基类设计，支持不同网站的爬虫实现，同时提供统一的接口和错误处理。

### 核心类: `GenericBaseCrawler[T]`

**关键文件**: [crawlers/base/base.py](file:///workspace/mdcx/crawlers/base/base.py)

这是所有爬虫的基类，定义了爬虫的标准接口和流程。

**主要方法**:

| 方法 | 功能 | 是否必须实现 |
|------|------|-------------|
| `site()` | 返回爬虫对应的网站枚举 | ✅ 是 |
| `base_url_()` | 返回网站的默认 URL | ✅ 是 |
| `new_context()` | 创建爬虫上下文 | ✅ 是 |
| `run()` | 执行爬虫（公共入口） | ❌ 否（已实现） |
| `_run()` | 内部执行逻辑 | ❌ 否（已实现，但可重写） |
| `_generate_search_url()` | 生成搜索 URL | ✅ 是（除非重写 `_run`） |
| `_parse_search_page()` | 解析搜索页 | ✅ 是（除非重写 `_run`） |
| `_parse_detail_page()` | 解析详情页 | ✅ 是（除非重写 `_run`） |
| `post_process()` | 结果后处理 | ❌ 否 |

### 爬虫上下文 (`Context`)

**关键文件**: [crawlers/base/types.py](file:///workspace/mdcx/crawlers/base/types.py)

```python
@dataclass
class Context:
    input: CrawlerInput              # 输入数据
    debug_info: CrawlerDebugInfo    # 调试信息

    def debug(self, message: str):   # 添加调试日志
        self.debug_info.logs.append(message)
```

### 爬虫数据 (`CrawlerData`)

**关键文件**: [crawlers/base/types.py](file:///workspace/mdcx/crawlers/base/types.py)

爬虫返回的原始数据结构，包含所有可能的元数据字段。

```python
@dataclass
class CrawlerData:
    title: FieldValue
    actors: FieldValue[list[str]]
    all_actors: FieldValue[list[str]]
    directors: FieldValue[list[str]]
    extrafanart: FieldValue[list[str]]
    originalplot: FieldValue
    originaltitle: FieldValue
    outline: FieldValue
    poster: FieldValue
    publisher: FieldValue
    release: FieldValue
    runtime: FieldValue
    score: FieldValue
    series: FieldValue
    studio: FieldValue
    tags: FieldValue[list[str]]
    thumb: FieldValue
    trailer: FieldValue
    wanted: FieldValue
    year: FieldValue
    image_download: FieldValue[bool]
    number: FieldValue
    mosaic: FieldValue
    external_id: FieldValue
    source: FieldValue
```

### 爬虫注册与获取

**关键文件**: [crawlers/base/base.py](file:///workspace/mdcx/crawlers/base/base.py)

```python
# 注册爬虫
def register_crawler(crawler_cls: type[GenericBaseCrawler[Any]]):
    crawler_registry[crawler_cls.site()] = crawler_cls

# 获取爬虫
def get_crawler(site: Website) -> type[GenericBaseCrawler[Never]] | None:
    return crawler_registry.get(site)

# 获取已注册的网站列表
def get_registered_crawler_sites(*, include_hidden: bool = False) -> list[Website]:
    ...
```

### 爬虫管理器 (`CrawlerProvider`)

**关键文件**: [crawler.py](file:///workspace/mdcx/crawler.py)

负责管理爬虫实例的生命周期、提供爬虫获取接口。

```python
class CrawlerProvider:
    def __init__(self, config: Config, client: AsyncWebClient, ...):
        self.instances: dict[Website, GenericBaseCrawler[Never]] = {}
        self.config = config
        self.client = client
        self.lock = asyncio.Lock()

    async def get(self, site: Website) -> GenericBaseCrawler[Never]:
        # 懒加载模式创建爬虫实例
        ...

    async def close(self):
        # 关闭所有爬虫实例
        ...
```

### 示例爬虫: JAVBus

**关键文件**: [crawlers/javbus.py](file:///workspace/mdcx/crawlers/javbus.py)

这是一个完整的爬虫实现示例，展示了如何继承和使用 `GenericBaseCrawler`。

```python
class JavbusCrawler(BaseCrawler):
    @classmethod
    @override
    def site(cls) -> Website:
        return Website.JAVBUS

    @classmethod
    @override
    def base_url_(cls) -> str:
        return manager.config.get_site_url(Website.JAVBUS, "https://www.javbus.com")

    @override
    async def _run(self, ctx: Context):
        # 自定义执行逻辑
        ...
```

### 支持的网站列表

项目支持 40+ 个网站，包括但不限于：
- JAVBus, JAVLibrary, DMM
- MGStage, Prestige, FC2
- ThePornDB, MissAV, AVBase
- 国产类：HDOUBAN, MDTV, MADOUQU
- 等等...

---

## 业务流程

### 1. 刮削主流程 (`Scraper`)

**关键文件**: [core/scraper.py](file:///workspace/mdcx/core/scraper.py)

这是刮削流程的主要控制器，协调整个刮削过程。

```python
class Scraper:
    async def run(self, file_mode: FileMode, movie_list: list[Path] | None) -> None:
        # 1. 初始化
        # 2. 获取待刮削文件列表
        # 3. 并发刮削处理
        # 4. 后处理

    async def process_one_file(self, task: tuple[Path, int, int]) -> None:
        # 处理单个文件的刮削
        # 1. 获取文件信息
        # 2. 调用爬虫获取数据
        # 3. 数据处理和翻译
        # 4. 下载图片
        # 5. 生成 NFO
        # 6. 移动/重命名文件
```

### 2. 文件爬虫 (`FileScraper`)

**关键文件**: [core/file_crawler.py](file:///workspace/mdcx/core/file_crawler.py)

负责从文件识别番号、选择合适的网站进行刮削、合并多源数据。

**核心功能**:

#### 刮削任务分类 (`classify_scrape_task`)

根据番号、文件路径等信息自动判断影片类型，选择合适的网站组。

```python
def classify_scrape_task(task_input: CrawlTask, config: Config, ...) -> ScrapeClassification:
    # 支持的类型:
    # - 有码
    # - 无码
    # - 素人
    # - FC2
    # - 欧美
    # - 国产
```

#### 多源数据合并 (`_call_crawlers`)

按照字段优先级从多个网站获取数据，合并为最终结果。

**策略**:
1. 按字段配置的优先级依次尝试获取
2. 对于失败的网站记录并跳过
3. 对于每个字段，采用第一个成功获取到的值
4. 收集所有来源的海报、缩略图、演员信息作为备选

#### 速度优先模式 (`_call_speed_crawlers`)

按顺序尝试网站，第一个成功的网站结果直接作为最终结果。

### 3. 数据处理流程

```
1. 文件扫描
   ↓
2. 番号识别
   ↓
3. 网站匹配/分类
   ↓
4. 爬虫执行
   ├─ 搜索页请求
   ├─ 详情页 URL 解析
   └─ 详情页数据提取
   ↓
5. 多源数据合并
   ↓
6. 数据处理
   ├─ 字段映射/清洗
   ├─ 翻译（标题、简介）
   ├─ 演员名映射
   └─ 标签处理
   ↓
7. 图片下载
   ├─ 海报
   ├─ 缩略图
   ├─ Fanart
   └─ 剧照
   ↓
8. NFO 生成
   ↓
9. 文件整理
   ├─ 移动文件
   ├─ 重命名
   ├─ 移动字幕
   └─ 创建目录
```

### 4. 命名系统

使用 Jinja2 模板引擎，支持灵活的文件和目录命名规则。

### 5. NFO 生成

生成符合 KODI/Emby 规范的 XML 元数据文件。

### 6. VSMETA 生成 (Synology Video Station)

**关键文件**: [core/vsmeta.py](file:///workspace/mdcx/core/vsmeta.py)

完整实现 Synology Video Station 专用的 VSMETA 二进制格式。

#### 核心特性 (Core Features)
- 📺 **Protobuf 风格编码**: 使用 protobuf 风格的标签编码
- 🖼️ **图片嵌入**: 支持嵌入海报和背景图，自动压缩至 200KB 以内
- 🔒 **元数据锁定**: 可配置是否禁止 Video Station 自动更新
- ⚙️ **高度可配置**: 图片尺寸、JPEG 质量、演员数量等均可配置
- 💾 **原子写入**: 使用临时文件确保写入不会损坏数据

#### 主要标签 (Main Tags)
| Tag | Hex | 说明 | Description |
|-----|-----|------|-------------|
| TAG_SHOW_TITLE | 0x12 | 显示标题 | Display title |
| TAG_SHOW_TITLE2 | 0x1A | 排序/备用标题 | Sort/alternative title |
| TAG_EPISODE_TITLE | 0x22 | 简短标题(番号) | Short title (number) |
| TAG_YEAR | 0x28 | 年份 | Year |
| TAG_EPISODE_RELEASE_DATE | 0x32 | 发布日期 | Release date |
| TAG_EPISODE_LOCKED | 0x38 | 锁定元数据 | Lock metadata |
| TAG_CHAPTER_SUMMARY | 0x42 | 简介/剧情 | Plot/Summary |
| TAG_EPISODE_META_JSON | 0x4A | 元数据 JSON | Metadata JSON |
| TAG_GROUP1 | 0x52 | 演员、导演、类型 | Cast, director, genre |
| TAG_CLASSIFICATION | 0x5A | 内容分级 | Content classification |
| TAG_RATING | 0x60 | 评分(×10) | Rating (×10) |
| TAG_EPISODE_THUMB_DATA | 0x8A | 海报数据 | Poster data |
| TAG_EPISODE_THUMB_MD5 | 0x92 | 海报 MD5 | Poster MD5 |
| TAG_GROUP2 | 0x9A | 剧集信息+海报 | Series info + poster |
| TAG_GROUP3 | 0xAA | 背景图+时间戳 | Backdrop + timestamp |

#### 核心类 (Core Class)
```python
class VSMetaEncoder:
    """VSMETA protobuf encoder for Synology Video Station"""
    
    def write_header(self):
        """写入头部 (Write header)"""
    
    def write_string_field(self, tag: int, value: str, label: str | None = None):
        """写入字符串字段 (Write string field)"""
    
    def write_poster(self, image_path: Path | None, label: str = "poster"):
        """写入海报 (Write poster)"""
    
    def write_submessage(self, tag: int, build_func, label: str | None = None, index: int | None = None):
        """写入子消息 (Write submessage)"""
```

#### 配置选项 (Configuration Options)
**关键文件**: [config/models.py](file:///workspace/mdcx/config/models.py#L538-L545)
```python
vsmeta_keep_ext: bool              # 保留视频扩展名 (Keep video extension)
vsmeta_include_poster: bool        # 嵌入封面图 (Include poster)
vsmeta_include_backdrop: bool      # 嵌入背景图 (Include backdrop)
vsmeta_locked: bool                # 锁定元数据 (Lock metadata)
vsmeta_image_max_dimension: int    # 图片最大尺寸 (Max image dimension)
vsmeta_jpeg_quality: int           # JPEG 质量 (JPEG quality)
vsmeta_actor_limit: int            # 演员数量上限 (Actor limit)
vsmeta_tag_limit: int              # 标签数量上限 (Tag limit)
```

#### 相关文档 (Related Documents)
- [VSMETA_COMPARISON.md](file:///workspace/VSMETA_COMPARISON.md) - 格式对比文档

---

## 配置管理

### 配置模型 (`Config`)

**关键文件**: [config/models.py](file:///workspace/mdcx/config/models.py)

基于 Pydantic 的配置模型，提供类型安全的配置管理。

**主要配置分类**:

1. **常规设置**
   - 媒体路径
   - 成功/失败输出目录
   - 文件类型过滤

2. **刮削设置**
   - 并发数
   - 各类型网站优先级
   - 字段优先级配置
   - 刮削模式（速度/信息/单一）

3. **网站设置**
   - 各网站自定义 URL
   - Cookie/Token 配置

4. **翻译设置**
   - 翻译引擎选择（Google/DeepL/LLM）
   - 目标语言

5. **NFO 包含内容**
   - 可配置 NFO 中包含的字段

6. **命名规则**
   - 目录命名模板
   - 文件命名模板

7. **水印设置**
   - 水印内容和位置

8. **网络设置**
   - 代理
   - Cloudflare 绕过

### 配置管理器 (`ConfigManager`)

**关键文件**: [config/manager.py](file:///workspace/mdcx/config/manager.py)

负责配置的加载、保存、迁移和热更新。

```python
class ConfigManager:
    def __init__(self):
        # 初始化配置路径

    def load(self) -> list[str]:
        # 加载配置文件
        # 支持从旧版本自动迁移

    def save(self):
        # 保存当前配置

    def reset(self):
        # 重置为默认配置

    def acquire_computed(self) -> ComputedLease:
        # 获取配置派生对象（包含 AsyncWebClient 等）
```

### 配置文件格式

使用 JSON 格式存储配置，配置文件路径由 `MDCx.config` 标记文件指定。

---

## 数据模型

### 核心数据类型

**关键文件**: [models/types.py](file:///workspace/mdcx/models/types.py)

#### FileInfo

从文件系统读取的基础信息。

```python
@dataclass
class FileInfo:
    number: str              # 番号
    mosaic: str              # 马赛克类型
    file_path: Path          # 文件路径
    folder_path: Path        # 目录路径
    has_sub: bool            # 是否有字幕
    # ... 更多字段
```

#### CrawlerInput

单个爬虫的输入数据。

```python
@dataclass
class CrawlerInput:
    number: str
    mosaic: str
    appoint_number: str
    appoint_url: str
    short_number: str
    language: Language
    org_language: Language
```

#### CrawlTask

一个文件的完整刮削任务信息。

```python
@dataclass
class CrawlTask(CrawlerInput):
    has_sub: bool
    c_word: str
    cd_part: str
    leak: str
    destroyed: str
    website_name: str
```

#### CrawlerResult

单个网站爬虫的返回结果。

```python
@dataclass
class CrawlerResult(BaseCrawlerResult):
    source: str              # 数据来源网站
    external_id: str         # 外部 ID
```

#### CrawlersResult

合并多个网站后的最终刮削结果。

```python
@dataclass
class CrawlersResult(BaseCrawlerResult):
    scraping_type: FixedScrapingType
    scraping_type_source: str
    actor_amazon: list[str]
    thumb_list: list[tuple[str, str]]
    poster_list: list[tuple[str, str, bool]]
    field_sources: dict[CrawlerResultFields, str]
    external_ids: dict[Website, str]
    # ... 更多字段
```

### 枚举定义

**关键文件**: [config/enums.py](file:///workspace/mdcx/config/enums.py)

主要枚举:
- `Website`: 支持的网站
- `FixedScrapingType`: 刮削类型（有码/无码/FC2/国产等）
- `Language`: 语言选项
- `Translator`: 翻译引擎
- `DownloadableFile`: 可下载的文件类型
- 等等...

---

## 依赖关系

### 项目依赖

**关键文件**: [pyproject.toml](file:///workspace/pyproject.toml)

```toml
dependencies = [
    "aiofiles==24.1.0",              # 异步文件操作
    "aiolimiter==1.2.1",             # 异步限流
    "av>=15.0.0",                    # 视频处理
    "beautifulsoup4==4.13.4",        # HTML 解析
    "curl_cffi==0.11.4",             # 基于 libcurl 的 HTTP 客户端（支持模拟浏览器指纹）
    "httpx[socks]>=0.28.1",          # 现代 HTTP 客户端
    "lxml>=5.2.0",                   # 高性能 XML/HTML 解析
    "openai==1.91.0",                # OpenAI API（用于 LLM 翻译）
    "oshash==0.1.1",                 # 视频哈希
    "parsel>=1.10.0",                # Scrapy 的选择器库
    "pillow==11.3.0",                # 图像处理
    "ping3==4.0.4",                  # 网络 ping
    "pydantic-settings>=2.10.1",     # Pydantic 设置管理
    "pyqt6==6.11.0",                 # GUI 框架
    "zhconv==1.4.3",                 # 中文简繁转换
    "opencv-contrib-python-headless==4.13.0.92",  # 图像处理
    "jinja2>=3.1.6",                 # 模板引擎
]
```

### 模块依赖关系图

```
main.py
│
├─> views/MDCx.py (UI)
│   └─> controllers/main_window/main_window.py
│       ├─> config/manager.py
│       ├─> core/scraper.py
│       │   ├─> crawler.py
│       │   ├─> core/file_crawler.py
│       │   ├─> core/nfo.py
│       │   ├─> core/image.py
│       │   └─> core/translate.py
│       └─> ...
│
└─> consts.py
```

---

## 项目运行方式

### 从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI

# 2. 安装依赖
uv sync --locked --all-extras --dev

# 3. 运行应用
uv run python mdcx/views/MDCx.py
# 或
uv run python main.py
```

### 命令行工具

项目包含一些命令行工具:

```bash
# 刮削命令
uv run crawl

# 生成枚举
uv run gen_enums

# 构建
uv run build
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/crawlers/

# 生成覆盖率报告
uv run pytest --cov=mdcx --cov-report=html
```

### 构建可执行文件

项目使用 PyInstaller 进行打包。

```bash
uv run python scripts/build.py
```

---

## 开发指南

### 添加新爬虫

1. **在 `mdcx/crawlers/` 下创建新文件**，例如 `mywebsite.py`
2. **继承基类**，选择 `GenericBaseCrawler` 或 `BaseCrawler`
3. **实现必需方法**：
   - `site()` - 返回网站枚举
   - `base_url_()` - 返回默认 URL
   - `new_context()` - 创建上下文
   - `_generate_search_url()` - 生成搜索 URL（如果使用默认流程）
   - `_parse_search_page()` - 解析搜索页（如果使用默认流程）
   - `_parse_detail_page()` - 解析详情页（如果使用默认流程）
4. **注册爬虫** - 在文件末尾添加 `register_crawler(MyCrawler)`
5. **在 `__init__.py` 中导入** - 确保爬虫被注册

**示例**:

```python
from .base import BaseCrawler, Context, register_crawler
from ..config.enums import Website

class MyWebsiteCrawler(BaseCrawler):
    @classmethod
    def site(cls) -> Website:
        return Website.MY_WEBSITE

    @classmethod
    def base_url_(cls) -> str:
        return "https://mywebsite.com"

    async def _generate_search_url(self, ctx: Context) -> str:
        return f"{self.base_url}/search/{ctx.input.number}"

    async def _parse_search_page(self, ctx: Context, html, search_url):
        # 解析搜索结果
        ...

    async def _parse_detail_page(self, ctx: Context, html, detail_url):
        # 解析详情页
        ...

register_crawler(MyWebsiteCrawler)
```

### 扩展字段优先级

在 `config/models.py` 中的 `Config` 类可以配置各字段的网站优先级。

### 代码风格

项目使用以下工具保持代码质量:
- `ruff` - 代码格式化和 linting
- `pytest` - 单元测试

```bash
# 代码检查
uv run ruff check

# 代码格式化
uv run ruff format
```

---

## 关键类速查表

| 类名 | 文件 | 功能 |
|------|------|------|
| `Scraper` | `core/scraper.py` | 刮削主流程控制器 |
| `FileScraper` | `core/file_crawler.py` | 文件爬虫，多源数据合并 |
| `GenericBaseCrawler[T]` | `crawlers/base/base.py` | 爬虫基类 |
| `CrawlerProvider` | `crawler.py` | 爬虫实例管理器 |
| `ConfigManager` | `config/manager.py` | 配置管理器 |
| `Config` | `config/models.py` | 配置模型 |
| `AsyncWebClient` | `web_async.py` | 异步 HTTP 客户端 |
| `MyMAinWindow` | `controllers/main_window/main_window.py` | 主窗口控制器 |

---

## 扩展阅读

- [README.md](file:///workspace/README.md) - 项目概览
- [docs/architecture.md](file:///workspace/docs/architecture.md) - 架构文档
- [docs/api-documentation.md](file:///workspace/docs/api-documentation.md) - API 文档
- [CONTRIBUTING.md](file:///workspace/CONTRIBUTING.md) - 贡献指南

---

*文档版本: 2.0.0*
*最后更新: 2026-05-26*
