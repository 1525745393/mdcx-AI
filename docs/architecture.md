# MDCx 架构设计文档

## 📋 文档信息

- **项目名称**: MDCx
- **版本**: 2.0.0
- **最后更新**: 2026-05-24
- **作者**: MDCx Team

---

## 1. 系统概述

### 1.1 项目背景

MDCx 是一个现代化的视频元数据刮削和管理工具，用于自动从多个网站获取视频信息、生成 NFO 文件、管理演员库等。

### 1.2 核心功能

1. **多源刮削**: 支持 40+ 个网站的数据源
2. **智能识别**: 自动识别番号、马赛克类型
3. **元数据管理**: 生成符合 KODI/Emby 规范的 NFO 文件
4. **图片处理**: 自动下载、裁剪、添加水印
5. **翻译功能**: 支持 Google/DeepL/LLM 翻译
6. **命名管理**: 灵活的命名模板系统

### 1.3 技术栈

- **语言**: Python 3.13+
- **GUI框架**: PyQt6
- **爬虫**: httpx, curl-cffi, BeautifulSoup4
- **数据处理**: Pydantic, Jinja2
- **异步**: asyncio, aiofiles
- **图像处理**: Pillow, OpenCV
- **构建**: PyInstaller, uv

---

## 2. 架构设计原则

### 2.1 设计目标

1. **模块化**: 高度解耦，便于维护和扩展
2. **可测试性**: 核心逻辑完全可单元测试
3. **性能**: 异步 I/O，提高并发效率
4. **可扩展性**: 易于添加新的爬虫和数据源
5. **用户体验**: 友好的 GUI 和错误处理

### 2.2 SOLID 原则

- **S**: 单一职责原则 - 每个模块只做一件事
- **O**: 开闭原则 - 对扩展开放，对修改关闭
- **L**: 里氏替换原则 - 子类可以替换父类
- **I**: 接口隔离原则 - 使用小而专的接口
- **D**: 依赖倒置原则 - 依赖抽象而非具体实现

### 2.3 设计模式

1. **策略模式**: 不同的刮削策略
2. **工厂模式**: 爬虫实例创建
3. **观察者模式**: 信号系统
4. **模板方法模式**: 爬虫基类
5. **单例模式**: 配置管理器

---

## 3. 系统架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        UI Layer (PyQt6)                     │
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
│                     Core Business Logic                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Scraper     │  │ FileCrawler  │  │ NamingSystem │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   NFO Gen    │  │  Amazon OCR  │  │  Translator  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Crawler Framework                       │
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

### 3.2 分层架构

#### Layer 1: UI Layer

**职责**: 用户界面展示和交互

**组件**:
- `MDCx.py`: 主窗口
- `SettingsUI`: 设置界面
- `ProgressUI`: 进度显示
- `PosterCutTool`: 海报裁剪工具

**技术**: PyQt6

#### Layer 2: Controller Layer

**职责**: UI 与业务逻辑的协调

**组件**:
- `EventHandler`: 事件处理
- `ConfigManager`: 配置管理
- `SignalBus`: 信号总线

#### Layer 3: Core Layer

**职责**: 核心业务逻辑

**组件**:
- `Scraper`: 刮削流程控制
- `FileCrawler`: 文件扫描
- `NamingSystem`: 命名模板
- `NFOGenerator`: NFO 生成
- `AmazonOCR`: Amazon 条码识别
- `Translator`: 翻译服务

#### Layer 4: Crawler Layer

**职责**: 数据采集

**组件**:
- `GenericBaseCrawler`: 爬虫基类
- `JAVBusCrawler`: JAVBus 爬虫
- `JAVLibraryCrawler`: JAVLibrary 爬虫
- ... 40+ 个爬虫实现

#### Layer 5: Infrastructure Layer

**职责**: 基础设施支持

**组件**:
- HTTP 客户端
- 异步文件系统
- 图像处理
- 数据库访问

---

## 4. 核心模块设计

### 4.1 爬虫框架

#### 设计目标

1. 统一的爬虫接口
2. 灵活的网站适配
3. 错误处理和重试
4. 并发控制

#### 架构

```python
class GenericBaseCrawler[T: Context]:
    """泛型爬虫基类"""
    
    def __init__(self):
        self.context: T
        self.site_name: str
        self.site_url: str
    
    async def match(self, number: str) -> bool:
        """匹配番号"""
        ...
    
    async def scrape(self, number: str, **kwargs) -> CrawlersResult:
        """执行刮削"""
        ...
    
    async def parse(self, html: str) -> ParsedData:
        """解析网页"""
        ...
```

#### 泛型设计

```python
from typing import Generic, TypeVar

T = TypeVar('T', bound='Context')

class GenericBaseCrawler(Generic[T]):
    """支持不同上下文类型的爬虫基类"""
    
    def __init__(self, context: T):
        self.context = context
```

### 4.2 刮削流程

#### 流程图

```
开始刮削
    │
    ▼
┌─────────────────┐
│ 1. 文件扫描      │
│ FileCrawler     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. 番号识别      │
│ NumberParser    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. 网站匹配      │
│ SiteMatcher     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. 爬虫执行      │
│ CrawlerRunner   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. 数据处理      │
│ DataProcessor   │
│ - 翻译          │
│ - 命名          │
│ - 图片处理      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. 文件写入      │
│ FileWriter      │
│ - NFO           │
│ - 图片          │
│ - 视频移动      │
└────────┬────────┘
         │
         ▼
结束刮削
```

#### 关键设计

1. **Pipeline 模式**: 数据流式处理
2. **责任链模式**: 各环节独立处理
3. **策略模式**: 不同处理策略可切换

### 4.3 文件扫描模块

#### 设计

```python
class FileScraper:
    """文件扫描器"""
    
    def scan(self, path: Path) -> list[FileInfo]:
        """扫描目录，返回待刮削文件"""
        ...
    
    def classify(self, file_info: FileInfo) -> ScrapeClassification:
        """分类文件"""
        ...
```

#### 分类结果

```python
@dataclass
class ScrapeClassification:
    status: ScrapeStatus  # 枚举: NEED_SCRAPE, ALREADY_DONE, ERROR
    reason: str
    existing_result: Optional[CrawlersResult]
```

### 4.4 命名模板系统

#### 架构

```
┌─────────────────────────────────────────────────┐
│              Naming Template System               │
├─────────────────────────────────────────────────┤
│                                                  │
│  Template String (Jinja2)                        │
│  ┌──────────────────────────────────────────┐   │
│  │ {{ number }}{% if studio %} [{{ studio }}]{% endif %} │
│  └──────────────────────────────────────────┘   │
│                    │                              │
│                    ▼                              │
│  ┌──────────────────────────────────────────┐   │
│  │ Template Renderer                         │   │
│  │ 1. Parse template                        │   │
│  │ 2. Fetch fields                         │   │
│  │ 3. Render output                         │   │
│  └──────────────────────────────────────────┘   │
│                    │                              │
│                    ▼                              │
│  ┌──────────────────────────────────────────┐   │
│  │ Field Sanitizer                           │   │
│  │ 1. Remove invalid chars                   │   │
│  │ 2. Handle reserved names                 │   │
│  │ 3. Truncate long names                   │   │
│  └──────────────────────────────────────────┘   │
│                    │                              │
│                    ▼                              │
│  Final Path: ABC-123 [Studio] Title/            │
│              ABC-123 [Studio] Title.mp4          │
└─────────────────────────────────────────────────┘
```

#### 支持的字段

```python
class NamingFields:
    """可用字段定义"""
    
    CORE_FIELDS = [
        'number', 'title', 'originaltitle',
        'actor', 'studio', 'series', 'release'
    ]
    
    EXTENDED_FIELDS = [
        'director', 'publisher', 'year', 'runtime',
        'mosaic', 'cnword', 'moword'
    ]
    
    METADATA_FIELDS = [
        'outline', 'wanted', 'score', 'four_k'
    ]
```

### 4.5 NFO 生成模块

#### 设计

```python
class NFOGenerator:
    """NFO 文件生成器"""
    
    def generate(self, result: CrawlersResult) -> str:
        """生成 NFO XML"""
        ...
    
    def to_kodi_format(self, result: CrawlersResult) -> str:
        """转换为 KODI 格式"""
        ...
    
    def to_emby_format(self, result: CrawlersResult) -> str:
        """转换为 Emby 格式"""
        ...
```

#### XML 结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<movie>
    <title>Title</title>
    <originaltitle>Original Title</originaltitle>
    <sorttitle>Sort Title</sorttitle>
    <actor>
        <name>Actor Name</name>
        <role>Role</role>
        <thumb>https://example.com/image.jpg</thumb>
    </actor>
    <genre>Genre</genre>
    <rating>8.5</rating>
    <year>2024</year>
    <runtime>120</runtime>
    <director>Director</director>
    <studio>Studio</studio>
    <plot>Plot text...</plot>
    <mpaa>rating</mpaa>
    <premiered>2024-01-01</premiered>
</movie>
```

### 4.6 图片处理模块

#### 功能

1. **下载**: 异步下载图片
2. **裁剪**: 人脸检测裁剪
3. **水印**: 添加水印
4. **格式转换**: 支持多种格式
5. **大小调整**: 缩放和压缩

#### 架构

```python
class ImageProcessor:
    """图片处理器"""
    
    async def download(self, url: str) -> bytes:
        """下载图片"""
        ...
    
    async def crop_face(
        self, 
        image: bytes, 
        mode: CropMode
    ) -> bytes:
        """人脸裁剪"""
        ...
    
    async def add_watermark(
        self, 
        image: bytes, 
        watermark: str
    ) -> bytes:
        """添加水印"""
        ...
    
    async def resize(
        self, 
        image: bytes, 
        width: int, 
        height: int
    ) -> bytes:
        """调整大小"""
        ...
```

### 4.7 配置管理

#### 设计

```python
class ConfigManager:
    """配置管理器（单例模式）"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self) -> None:
        """从文件加载配置"""
        ...
    
    def save(self) -> None:
        """保存配置到文件"""
        ...
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        ...
    
    def set(self, key: str, value: Any) -> None:
        """设置配置项"""
        ...
```

#### 配置项分类

```python
class ConfigKeys:
    """配置项键名"""
    
    # 刮削设置
    SCRAPE_THREADS = "scrape.threads"
    SCRAPE_RETRY = "scrape.retry"
    SCRAPE_TIMEOUT = "scrape.timeout"
    
    # 命名设置
    NAMING_FOLDER = "naming.folder_template"
    NAMING_FILE = "naming.file_template"
    
    # 翻译设置
    TRANSLATE_ENGINE = "translate.engine"
    TRANSLATE_TARGET = "translate.target_lang"
    
    # ... 更多配置
```

### 4.8 信号系统

#### 设计

```python
class SignalBus:
    """信号总线（观察者模式）"""
    
    def connect(self, signal: str, callback: Callable):
        """连接信号"""
        ...
    
    def disconnect(self, signal: str, callback: Callable):
        """断开信号"""
        ...
    
    def emit(self, signal: str, *args, **kwargs):
        """发射信号"""
        ...
```

#### 预定义信号

```python
class Signals:
    """预定义信号"""
    
    SCRAPE_STARTED = "scrape:started"
    SCRAPE_PROGRESS = "scrape:progress"
    SCRAPE_COMPLETED = "scrape:completed"
    SCRAPE_ERROR = "scrape:error"
    
    LOG_UPDATED = "log:updated"
    CONFIG_CHANGED = "config:changed"
```

---

## 5. 数据模型设计

### 5.1 核心数据模型

#### CrawlersResult

```python
@dataclass
class CrawlersResult:
    """刮削结果"""
    
    # 基础信息
    number: str = ""
    title: str = ""
    original_title: str = ""
    
    # 人员信息
    actor: list[str] = field(default_factory=list)
    director: str = ""
    studio: str = ""
    publisher: str = ""
    
    # 发行信息
    release_date: str = ""
    runtime: int = 0
    year: int = 0
    
    # 分类信息
    genre: list[str] = field(default_factory=list)
    mosaic: str = ""
    series: str = ""
    
    # 评分信息
    rating: float = 0.0
    wanted: int = 0
    score: float = 0.0
    
    # 内容
    outline: str = ""
    plot: str = ""
    
    # 图片
    poster_url: str = ""
    thumb_url: str = ""
    fanart_url: str = ""
    extrafanart: list[str] = field(default_factory=list)
    
    # 视频信息
    video_type: str = ""
    cid: str = ""
   VID: str = ""
    
    # 字幕
    subtitles: list[str] = field(default_factory=list)
    
    # 状态
    success: bool = False
    error: str = ""
```

#### FileInfo

```python
@dataclass
class FileInfo:
    """文件信息"""
    
    file_path: Path
    file_name: str
    number: str
    folder_path: Path
    file_show_name: str
    file_show_path: str
    original_file_name: str
```

### 5.2 枚举定义

```python
class ScrapeStatus(Enum):
    """刮削状态"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"

class MosaicType(Enum):
    """马赛克类型"""
    CENSORED = "censored"      # 有码
    UNCENSORED = "uncensored"  # 无码
    WESTERN = "western"        # 欧美
    CHINESE = "chinese"       # 国产

class VideoDefinition(Enum):
    """清晰度"""
    SD = "480p"
    HD = "720p"
    FHD = "1080p"
    UHD_4K = "4K"
    UHD_8K = "8K"
```

---

## 6. 异步架构

### 6.1 异步编程模型

#### 事件循环

```python
import asyncio

async def main():
    # 创建事件循环
    scraper = Scraper(provider)
    
    # 并发执行
    tasks = [
        scraper.scrape(movie)
        for movie in movie_list
    ]
    
    results = await asyncio.gather(*tasks)
    
    return results

asyncio.run(main())
```

#### 并发控制

```python
class ConcurrencyController:
    """并发控制器"""
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run(self, coro):
        async with self.semaphore:
            return await coro
```

### 6.2 异步文件系统

#### aiofiles 使用

```python
import aiofiles

async def write_nfo(path: Path, content: str):
    """异步写入 NFO 文件"""
    async with aiofiles.open(path, 'w', encoding='utf-8') as f:
        await f.write(content)

async def read_file(path: Path) -> bytes:
    """异步读取文件"""
    async with aiofiles.open(path, 'rb') as f:
        return await f.read()
```

#### 异步批量操作

```python
async def batch_write(files: list[tuple[Path, str]]):
    """批量异步写入"""
    tasks = [
        write_nfo(path, content)
        for path, content in files
    ]
    await asyncio.gather(*tasks)
```

---

## 7. 错误处理机制

### 7.1 异常层次

```python
class MDCxError(Exception):
    """基础异常"""
    pass

class CrawlerError(MDCxError):
    """爬虫错误"""
    pass

class NetworkError(MDCxError):
    """网络错误"""
    pass

class ValidationError(MDCxError):
    """验证错误"""
    pass

class FileSystemError(MDCxError):
    """文件系统错误"""
    pass
```

### 7.2 重试机制

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def fetch_with_retry(url: str) -> str:
    """带重试的请求"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
```

### 7.3 降级策略

```python
class FallbackStrategy:
    """降级策略"""
    
    async def scrape_with_fallback(
        self,
        number: str,
        crawlers: list[Crawler]
    ) -> CrawlersResult:
        """尝试多个爬虫"""
        for crawler in crawlers:
            try:
                result = await crawler.scrape(number)
                if result.success:
                    return result
            except Exception as e:
                logger.warning(f"Crawler {crawler.site_name} failed: {e}")
                continue
        
        # 所有爬虫都失败
        return CrawlersResult(success=False, error="All crawlers failed")
```

---

## 8. 性能优化策略

### 8.1 缓存策略

```python
from functools import lru_cache
import asyncio

class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: str):
        async with self._lock:
            return self._cache.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        async with self._lock:
            self._cache[key] = {
                'value': value,
                'expires': time.time() + ttl
            }
    
    async def cleanup(self):
        """清理过期缓存"""
        async with self._lock:
            now = time.time()
            self._cache = {
                k: v for k, v in self._cache.items()
                if v['expires'] > now
            }
```

### 8.2 连接池

```python
import httpx

class HTTPClientPool:
    """HTTP 连接池"""
    
    def __init__(self, max_connections: int = 100):
        self.limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=20
        )
        self.timeout = httpx.Timeout(30.0)
    
    async def get_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            limits=self.limits,
            timeout=self.timeout
        )
```

### 8.3 批量处理

```python
async def batch_process(
    items: list[Any],
    processor: Callable,
    batch_size: int = 10,
    max_concurrent: int = 5
):
    """批量并发处理"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_item(item):
        async with semaphore:
            return await processor(item)
    
    # 分批处理
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = await asyncio.gather(
            *[process_item(item) for item in batch],
            return_exceptions=True
        )
        results.extend(batch_results)
    
    return results
```

---

## 9. 安全设计

### 9.1 输入验证

```python
import re
from pathlib import Path

class InputValidator:
    """输入验证器"""
    
    @staticmethod
    def validate_number(number: str) -> bool:
        """验证番号格式"""
        pattern = r'^[A-Z]{2,10}-\d{2,6}$'
        return bool(re.match(pattern, number.upper()))
    
    @staticmethod
    def validate_path(path: Path, base_dir: Path) -> bool:
        """验证路径安全性（防止路径遍历）"""
        try:
            resolved = path.resolve()
            base_resolved = base_dir.resolve()
            return str(resolved).startswith(str(base_resolved))
        except:
            return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """清理文件名"""
        # 移除非法字符
        filename = re.sub(r'[<>:"|?*]', '', filename)
        # 限制长度
        if len(filename) > 200:
            filename = filename[:200]
        return filename
```

### 9.2 敏感信息处理

```python
class SecretManager:
    """敏感信息管理器"""
    
    def mask(self, secret: str) -> str:
        """脱敏显示"""
        if len(secret) <= 8:
            return '*' * len(secret)
        return secret[:4] + '*' * (len(secret) - 8) + secret[-4:]
    
    def get_from_env(self, key: str, default: str = "") -> str:
        """从环境变量获取"""
        return os.environ.get(key, default)
```

---

## 10. 可测试性设计

### 10.1 依赖注入

```python
class Scraper:
    """使用依赖注入的刮削器"""
    
    def __init__(
        self,
        crawler_provider: CrawlerProvider,
        file_writer: FileWriter,
        image_processor: ImageProcessor,
        translator: Translator
    ):
        self.crawler_provider = crawler_provider
        self.file_writer = file_writer
        self.image_processor = image_processor
        self.translator = translator
```

### 10.2 Mock 对象

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_crawler():
    """Mock 爬虫 fixture"""
    crawler = AsyncMock()
    crawler.scrape.return_value = CrawlersResult(
        number="ABC-123",
        title="Test Title",
        success=True
    )
    return crawler

@pytest.mark.asyncio
async def test_scraper_with_mock(mock_crawler):
    """使用 Mock 测试刮削"""
    provider = MagicMock()
    provider.get_crawler.return_value = mock_crawler
    
    scraper = Scraper(provider, MockFileWriter(), MockImageProcessor())
    result = await scraper.scrape(Path("/test/video.mp4"))
    
    assert result.success
    assert result.number == "ABC-123"
```

### 10.3 测试覆盖率

```bash
# 生成覆盖率报告
uv run python -m pytest tests/ \
    --cov=mdcx \
    --cov-report=html \
    --cov-report=term

# 查看最低覆盖率
uv run python -m pytest tests/ \
    --cov=mdcx.core \
    --cov-fail-under=80
```

---

## 11. 部署架构

### 11.1 打包方式

#### PyInstaller

```python
# build.py
from PyInstaller.__main__ import run

if __name__ == "__main__":
    run([
        "mdcx/views/MDCx.py",
        "--name=MDCx",
        "--onefile",
        "--windowed",
        "--add-data=mdcx/views:mdcx/views",
        "--hidden-import=mdcx",
        ...
    ])
```

### 11.2 跨平台构建

#### GitHub Actions

```yaml
# .github/workflows/release.yml
jobs:
  build:
    strategy:
      matrix:
        include:
          - os: macos-latest
            target: macOS
          - os: windows-latest
            target: Windows
          - os: ubuntu-latest
            target: Linux
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
      
      - name: Build
        run: uv run scripts/build.py --debug
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
```

---

## 12. 监控与日志

### 12.1 日志系统

```python
import logging
from rich.logging import RichHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("mdcx")

# 使用
logger.info("Starting scrape")
logger.error(f"Failed: {error}", exc_info=True)
logger.debug(f"Response: {response}")
```

### 12.2 结构化日志

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

# 使用
log = structlog.get_logger()
log.info("scrape_completed",
    number="ABC-123",
    duration=2.5,
    success=True
)
```

---

## 13. 扩展性设计

### 13.1 插件系统

```python
class PluginInterface:
    """插件接口"""
    
    def on_scrape_start(self, number: str):
        """刮削开始时调用"""
        pass
    
    def on_scrape_complete(self, result: CrawlersResult):
        """刮削完成时调用"""
        pass
    
    def on_error(self, error: Exception):
        """发生错误时调用"""
        pass

class PluginManager:
    """插件管理器"""
    
    def load_plugins(self, plugin_dir: Path):
        """加载插件"""
        ...
    
    def register_plugin(self, plugin: PluginInterface):
        """注册插件"""
        ...
```

### 13.2 自定义爬虫

```python
class MyCustomCrawler(GenericBaseCrawler):
    """自定义爬虫示例"""
    
    site_name = "MySite"
    site_url = "https://mysite.com"
    
    async def match(self, number: str) -> bool:
        # 自定义匹配逻辑
        return True
    
    async def scrape(self, number: str, **kwargs) -> CrawlersResult:
        # 自定义刮削逻辑
        ...
```

---

## 14. 配置管理

### 14.1 配置加载流程

```
启动应用
    │
    ▼
┌─────────────────┐
│ 加载默认配置     │
│ (defaults.json) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 加载用户配置     │
│ (config.json)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 合并配置         │
│ (用户配置优先)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 验证配置         │
│ (Pydantic)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 应用配置         │
└─────────────────┘
```

### 14.2 配置版本迁移

```python
class ConfigMigration:
    """配置迁移"""
    
    migrations = {
        "1.0": migrate_from_v1,
        "1.1": migrate_from_v1_to_v2,
        "2.0": migrate_to_v2
    }
    
    def migrate(self, config: dict, from_version: str) -> dict:
        """执行迁移"""
        while from_version in self.migrations:
            config = self.migrations[from_version](config)
            from_version = self.get_next_version(from_version)
        return config
```

---

## 15. 未来架构规划

### 15.1 微服务化

- 将爬虫抽取为独立服务
- 使用消息队列协调
- 支持分布式刮削

### 15.2 云原生支持

- Docker 容器化
- Kubernetes 部署
- 自动扩缩容

### 15.3 AI 增强

- 智能番号识别
- 自动分类
- 相似视频推荐

---

## 16. 附录

### A. 术语表

| 术语 | 说明 |
|------|------|
| 番号 | 视频的唯一标识符，如 ABC-123 |
| 刮削 | 从网站获取视频元数据的过程 |
| NFO | 游戏/视频元数据文件格式 |
| 马赛克 | 视频的马赛克类型（有码/无码） |
| 素人 | 非职业AV女优 |

### B. 参考资料

- [Qt Documentation](https://doc.qt.io/)
- [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### C. 联系方式

- **GitHub**: https://github.com/1525745393/mdcx-AI
- **Telegram**: https://t.me/mdcx_chat

---

*文档版本: 2.0.0*
*最后更新: 2026-05-24*
