# MDCx 核心模块 API 文档

> 📖 **更多文档**: [文档中心](README.md) | [主 README](../README.md) | [开发指南](../DEVELOPMENT.md) | [架构设计](architecture.md)

## 📋 概述

本文档详细描述 MDCx 项目的核心模块功能、API 接口和使用方法。

---

## 1. 核心模块结构

```
mdcx/core/
├── amazon.py          # Amazon 条码识别和封面搜索
├── scraper.py         # 刮削主流程控制
├── file_crawler.py    # 文件扫描和分类
├── web.py             # Web 请求和处理
├── image.py           # 图片处理
├── nfo.py             # NFO 文件生成
├── vsmeta.py          # VSMETA 文件生成
├── mosaic.py          # 马赛克/无码识别
├── face_crop.py       # 人脸检测和裁剪
├── translate.py       # 翻译功能
├── naming/            # 命名模板系统
│   ├── template.py    # 模板解析
│   ├── fields.py      # 字段处理
│   ├── renderer.py    # 渲染器
│   └── sanitize.py    # 文件名清洗
└── utils.py           # 工具函数
```

---

## 2. Amazon 条码识别模块 (amazon.py)

### 2.1 模块简介

Amazon 模块负责从视频/封面图像中识别 EAN-13 条码，并从网页文本中提取条码信息，用于匹配 Amazon 封面。

### 2.2 核心函数

#### `_normalize_amazon_barcode(barcode: str) -> str`

标准化条码字符串。

**参数**:
- `barcode` (str): 原始条码字符串

**返回**: 
- 标准化后的 13 位数字条码，若无效返回空字符串

**示例**:
```python
>>> from mdcx.core.amazon import _normalize_amazon_barcode
>>> _normalize_amazon_barcode("455-1234-567-890")
'4551234567890'
```

#### `_extract_labeled_amazon_barcodes(text: str) -> set[str]`

从文本中提取标注的条码（EAN/JAN/ISBN）。

**参数**:
- `text` (str): 待搜索的文本内容

**返回**: 
- 有效条码的集合

**示例**:
```python
>>> from mdcx.core.amazon import _extract_labeled_amazon_barcodes
>>> barcodes = _extract_labeled_amazon_barcodes("EAN: 4551234567890")
>>> "4551234567890" in barcodes
True
```

#### `_is_valid_ean13_barcode(barcode: str) -> bool`

验证 EAN-13 条码的校验和是否正确。

**参数**:
- `barcode` (str): 13 位数字条码

**返回**: 
- 校验通过返回 True

**示例**:
```python
>>> from mdcx.core.amazon import _is_valid_ean13_barcode
>>> _is_valid_ean13_barcode("4549831546432")
True
>>> _is_valid_ean13_barcode("1234567890123")
False
```

#### `_beam_search_amazon_ean13_from_ranked_digits(ranked_digits) -> str`

使用波束搜索算法识别图像中的条码。

**参数**:
- `ranked_digits`: 排序后的数字候选列表

**返回**: 
- 识别到的条码字符串

#### `is_amazon_hard_match(result: CrawlersResult) -> bool`

判断是否为 Amazon 硬匹配。

**参数**:
- `result` (CrawlersResult): 爬虫结果对象

**返回**: 
- 硬匹配返回 True

---

## 3. 刮削核心模块 (scraper.py)

### 3.1 模块简介

Scraper 是整个刮削流程的核心控制器，负责协调各个模块完成从文件发现到元数据写入的完整流程。

### 3.2 核心类

#### `Scraper`

刮削任务控制器类。

**主要方法**:

##### `__init__(self, crawler_provider: CrawlerProvider)`

初始化 Scraper。

**参数**:
- `crawler_provider`: 爬虫提供者实例

##### `scrape(self, movie_list: list[Path])`

执行刮削任务。

**参数**:
- `movie_list` (list[Path]): 待刮削的视频文件路径列表

**示例**:
```python
from mdcx.crawler import CrawlerProvider
from mdcx.core.scraper import Scraper

provider = CrawlerProvider()
scraper = Scraper(provider)
results = await scraper.scrape(movie_list)
```

##### `process_one_file(self, task)`

处理单个文件。

**参数**:
- `task` (tuple): (文件路径, 线程ID, 任务ID) 元组

##### `_run_tasks_with_limit(self, tasks, thread_count, max_concurrent)`

并发执行任务，支持并发数限制。

**参数**:
- `tasks`: 任务列表
- `thread_count`: 线程数
- `max_concurrent`: 最大并发数

### 3.3 异常类

#### `StopScrape`

用户主动停止刮削时抛出。

#### `UnexpectedScrapeCancellation`

意外的取消操作时抛出。

---

## 4. 文件扫描模块 (file_crawler.py)

### 4.1 模块简介

FileCrawler 负责扫描指定目录，发现需要刮削的视频文件，并进行分类。

### 4.2 核心函数

#### `classify_scrape_task(file_path: Path, settings: dict) -> ScrapeClassification`

对文件进行刮削分类。

**参数**:
- `file_path` (Path): 文件路径
- `settings` (dict): 刮削设置

**返回**: 
- ScrapeClassification 分类结果

#### `classify_existing_scrape_result(file_path: Path) -> ScrapeResult`

对已存在的刮削结果进行分类。

**参数**:
- `file_path` (Path): 文件路径

**返回**: 
- ScrapeResult 刮削结果

#### `get_file_info_v2(file_path: Path) -> FileInfo`

获取文件信息（支持重试）。

**参数**:
- `file_path` (Path): 文件路径

**返回**: 
- FileInfo 文件信息对象

### 4.3 FileInfo 数据类

```python
@dataclass
class FileInfo:
    file_path: Path              # 文件路径
    file_name: str               # 文件名
    number: str                  # 番号
    folder_path: Path            # 文件夹路径
    file_show_name: str          # 显示名称
    file_show_path: str          # 显示路径
    original_file_name: str       # 原始文件名
```

---

## 5. NFO 文件模块 (nfo.py)

### 5.1 模块简介

NFO 模块负责生成符合 KODI/Emby 规范的 NFO 元数据文件。

### 5.2 核心函数

#### `write_nfo(result: CrawlersResult, file_info: FileInfo)`

写入 NFO 文件。

**参数**:
- `result` (CrawlersResult): 刮削结果
- `file_info` (FileInfo): 文件信息

**示例**:
```python
from mdcx.core.nfo import write_nfo

write_nfo(result, file_info)
```

#### `get_nfo_data(result: CrawlersResult) -> str`

生成 NFO XML 数据。

**参数**:
- `result` (CrawlersResult): 刮削结果

**返回**: 
- NFO XML 字符串

---

## 6. 命名模板模块 (naming/)

### 6.1 模块简介

命名模板系统使用 Jinja2 语法，支持灵活的视频文件和目录命名规则。

### 6.2 核心函数

#### `render_naming_template(template: str, result: CrawlersResult) -> str`

渲染命名模板。

**参数**:
- `template` (str): Jinja2 模板字符串
- `result` (CrawlersResult): 刮削结果

**返回**: 
- 渲染后的命名字符串

**示例**:
```python
from mdcx.core.naming import render_naming_template

template = "{{ number }}{% if studio %} [{{ studio }}]{% endif %}"
result = CrawlersResult(...)
name = render_naming_template(template, result)
```

### 6.3 可用字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| `number` | 番号 | ABC-123 |
| `title` | 标题 | Sample Title |
| `originaltitle` | 原标题 | Original Title |
| `actor` | 演员 | John Doe |
| `studio` | 片商 | Studio Name |
| `series` | 系列 | Series Name |
| `release` | 发行日期 | 2024-01-01 |
| `definition` | 清晰度 | 1080P |
| `filename` | 原文件名 | video.mp4 |
| `all_actor` | 全部演员 | Actor1, Actor2 |
| `first_actor` | 首位演员 | Actor1 |
| `letters` | 番号前缀 | ABC |
| `first_letter` | 番号首字符 | A |
| `outline` | 剧情简介 | ... |
| `director` | 导演 | Director Name |
| `publisher` | 发行商 | Publisher Name |
| `year` | 年份 | 2024 |
| `runtime` | 时长 | 120 |
| `mosaic` | 有码/无码标识 | 有码 |
| `cnword` | 字幕标识 | 中字 |
| `moword` | 版本标识 | 无码 |
| `wanted` | 想看人数 | 1000 |
| `score` | 评分 | 8.5 |
| `four_k` | 4K/8K 标识 | 4K |

---

## 7. 马赛克识别模块 (mosaic.py)

### 7.1 模块简介

Mosaic 模块负责识别视频的马赛克类型（有码、无码、流出、破解等）。

### 7.2 核心函数

#### `normalize_mosaic(mosaic_str: str) -> tuple[str, str, bool, bool]`

标准化马赛克标识字符串。

**参数**:
- `mosaic_str` (str): 原始马赛克字符串

**返回**: 
- (标准马赛克类型, 后处理类型, 是否流出, 是否破解) 元组

**示例**:
```python
>>> from mdcx.core.mosaic import normalize_mosaic
>>> normalize_mosaic("有码-有码-False-False")
('有码', '有码', False, False)
```

#### `add_mark(mosaic_str: str, add_leak: bool, add_uncensored: bool) -> str`

添加马赛克标记。

**参数**:
- `mosaic_str` (str): 原始马赛克字符串
- `add_leak` (bool): 是否添加流出标记
- `add_uncensored` (bool): 是否添加无码标记

**返回**: 
- 添加标记后的字符串

---

## 8. 翻译模块 (translate.py)

### 8.1 模块简介

Translate 模块提供标题、简介、演员的翻译功能，支持多种翻译引擎。

### 8.2 核心函数

#### `translate_title_outline(title: str, outline: str, target_lang: str = "zh-CN") -> tuple[str, str]`

翻译标题和简介。

**参数**:
- `title` (str): 标题
- `outline` (str): 简介
- `target_lang` (str): 目标语言，默认 "zh-CN"

**返回**: 
- (翻译后的标题, 翻译后的简介) 元组

**示例**:
```python
>>> from mdcx.core.translate import translate_title_outline
>>> title, outline = translate_title_outline("Sample Title", "Sample outline")
>>> print(title)
样本标题
```

#### `translate_actor(actor: str, target_lang: str = "zh-CN") -> str`

翻译演员名。

**参数**:
- `actor` (str): 演员名
- `target_lang` (str): 目标语言

**返回**: 
- 翻译后的演员名

---

## 9. 爬虫框架 (crawlers/)

### 9.1 基础类

#### `GenericBaseCrawler[T]`

所有爬虫的基类，使用泛型支持不同上下文类型。

**主要属性**:
- `context`: 爬取上下文
- `site_name`: 网站名称
- `site_url`: 网站 URL

**主要方法**:

##### `match(number: str) -> bool`

匹配番号。

##### `scrape(number: str, **kwargs) -> CrawlersResult`

执行刮削。

### 9.2 支持的网站

项目支持 40+ 个网站爬虫，包括：

- **JAVBus** (`javbus.py`)
- **JAVLibrary** (`javlibrary.py`)
- **JAVDB** (`javdb_new.py`, `javdbapi.py`)
- **DMM** (`dmm_new/`)
- **FC2** (`fc2.py`, `fc2hub.py`, `fc2ppvdb.py`)
- **素人系列** (`airav_cc.py`, `cableav.py` 等)
- 以及更多...

---

## 10. 数据模型

### 10.1 CrawlersResult

刮削结果数据类，包含所有元数据字段。

### 10.2 FileInfo

文件信息数据类。

### 10.3 ScrapeClassification

刮削分类枚举。

### 10.4 ScrapeResult

刮削结果枚举。

---

## 11. 配置管理

### 11.1 ConfigManager

配置管理器 (`mdcx.config.manager`)

**主要方法**:

#### `load() -> None`

加载配置。

#### `save() -> None`

保存配置。

#### `get(key: str, default: Any = None) -> Any`

获取配置项。

#### `set(key: str, value: Any) -> None`

设置配置项。

---

## 12. 工具函数

### 12.1 文件工具 (`mdcx.utils.file`)

- `copy_file_async()`: 异步复制文件
- `move_file_async()`: 异步移动文件
- `check_file()`: 检查文件是否存在

### 12.2 路径工具 (`mdcx.utils.path`)

- `is_any_descendant()`: 检查路径关系
- `split_path()`: 分割路径

### 12.3 视频工具 (`mdcx.utils.video`)

- `get_video_size()`: 获取视频分辨率
- `get_video_duration()`: 获取视频时长

---

## 13. 信号系统

### 13.1 Signal

全局信号系统，用于组件间通信。

**主要信号**:

- `signal.scrape_started`: 刮削开始
- `signal.scrape_finished`: 刮削完成
- `signal.scrape_error`: 刮削错误
- `signal.progress_updated`: 进度更新
- `signal.log_updated`: 日志更新

**使用示例**:
```python
from mdcx.signals import signal

def on_progress(progress):
    print(f"Progress: {progress}%")

signal.progress_updated.connect(on_progress)
```

---

## 14. 测试

### 14.1 测试文件

- `tests/core/test_amazon_core.py`: Amazon 模块测试
- `tests/core/test_scraper_core.py`: Scraper 模块测试
- `tests/core/test_mosaic.py`: 马赛克识别测试
- `tests/crawlers/`: 各爬虫测试

### 14.2 运行测试

```bash
# 运行所有测试
uv run python -m pytest tests/ -v

# 运行核心模块测试
uv run python -m pytest tests/core/ -v

# 运行特定测试
uv run python -m pytest tests/core/test_amazon_core.py -v

# 生成覆盖率报告
uv run python -m pytest tests/ --cov=mdcx --cov-report=html
```

---

## 15. 错误处理

### 15.1 常见异常

- `StopScrape`: 用户停止刮削
- `UnexpectedScrapeCancellation`: 意外取消
- `CrawlerError`: 爬虫错误
- `NetworkError`: 网络错误
- `ValidationError`: 验证错误

### 15.2 错误处理建议

```python
from mdcx.core.scraper import StopScrape, UnexpectedScrapeCancellation

try:
    await scraper.scrape(movie_list)
except StopScrape as e:
    print(f"用户停止了刮削: {e}")
except UnexpectedScrapeCancellation as e:
    print(f"意外取消: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 16. 最佳实践

### 16.1 异步编程

项目大量使用 asyncio，遵循以下最佳实践：

```python
import asyncio
from mdcx.core.scraper import Scraper

async def main():
    scraper = Scraper(provider)
    await scraper.scrape(movie_list)

asyncio.run(main())
```

### 16.2 类型注解

所有公共 API 都包含类型注解：

```python
def process_file(path: Path) -> CrawlersResult:
    ...
```

### 16.3 错误处理

使用 try-except 块处理异常：

```python
try:
    result = await crawler.scrape(number)
except Exception as e:
    logger.error(f"Scrape failed: {e}")
    return None
```

---

## 17. 性能优化

### 17.1 并发控制

使用 `_run_tasks_with_limit` 控制并发数：

```python
await scraper._run_tasks_with_limit(
    movie_list, 
    thread_count=5, 
    max_concurrent=10
)
```

### 17.2 缓存

部分函数使用 `@lru_cache` 缓存结果：

```python
@lru_cache(maxsize=128)
def expensive_operation(param):
    ...
```

### 17.3 异步 I/O

优先使用异步文件操作：

```python
import aiofiles

async with aiofiles.open(path, 'w') as f:
    await f.write(content)
```

---

## 18. 安全注意事项

### 18.1 路径遍历防护

使用 `Path` 对象的安全方法：

```python
# ❌ 不安全
path = user_input
os.listdir(path)

# ✅ 安全
path = Path(user_input).resolve()
path = Path(path).absolute()
```

### 18.2 输入验证

所有用户输入都应验证：

```python
def process_number(number: str) -> str:
    if not re.match(r'^[A-Z]+-\d+$', number):
        raise ValueError(f"Invalid number format: {number}")
    return number.upper()
```

---

## 19. 调试

### 19.1 日志

使用日志系统：

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug info")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### 19.2 断点调试

支持 pdb/IPDB：

```python
import pdb
pdb.set_trace()
```

---

## 20. 贡献指南

### 20.1 代码风格

遵循项目代码规范，使用 ruff 检查：

```bash
ruff check .
```

### 20.2 提交规范

使用语义化提交信息：

```
feat: 添加新爬虫
fix: 修复 bug
docs: 更新文档
test: 添加测试
refactor: 重构代码
```

### 20.3 PR 要求

- 通过所有测试
- 添加必要的测试
- 更新相关文档
- 遵循代码规范

---

## 21. 联系方式

- **GitHub Issues**: https://github.com/1525745393/mdcx-AI/issues
- **Telegram 交流群**: https://t.me/mdcx_chat

---

## 22. 许可证

本项目在 GPLv3 许可证下发行。

---

*文档最后更新: 2026-05-24*
