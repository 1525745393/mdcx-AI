# MDCx 开发指南

> 📖 **更多文档**: [文档中心](docs/README.md) | [主 README](README.md) | [架构设计](docs/architecture.md) | [API 文档](docs/api-documentation.md) | [贡献指南](CONTRIBUTING.md)

本文档详细介绍 MDCx 项目的开发流程、最佳实践、代码规范、环境配置、测试和调试方法。

## 目录

1. [开发环境搭建](#开发环境搭建)
2. [项目结构](#项目结构)
3. [开发流程](#开发流程)
4. [代码规范](#代码规范)
5. [最佳实践](#最佳实践)
6. [测试指南](#测试指南)
7. [调试技巧](#调试技巧)
8. [常见任务](#常见任务)

## 开发环境搭建

### 前置要求

- **Python**: >= 3.13.4
- **Git**: 最新版本
- **uv**: 包管理工具（推荐）

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI
```

2. **安装依赖**

使用 uv（推荐）：

```bash
uv sync --all-extras --dev
```

或者使用 pip：

```bash
pip install -e .[dev]
```

3. **安装 pre-commit hooks**

```bash
uv run pre-commit install
```

4. **验证安装**

```bash
# 运行测试
uv run pytest

# 运行程序
uv run python main.py
```

### IDE 配置

推荐使用 VS Code 或 PyCharm。

**VS Code 配置建议**：

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "ruff"
}
```

## 项目结构

```
mdcx/
├── main.py                    # 程序入口
├── mdcx/                      # 主源码目录
│   ├── base/                  # 基础功能模块
│   │   ├── file.py            # 文件处理
│   │   ├── image.py           # 图像处理
│   │   ├── number.py          # 番号处理
│   │   ├── translate.py       # 翻译基类
│   │   ├── video.py           # 视频处理
│   │   ├── web.py             # Web 请求基类
│   │   └── web_sync.py        # 同步 Web 请求
│   ├── cmd/                   # 命令行工具
│   │   ├── crawl.py           # 命令行刮削
│   │   └── gen_enums.py       # 生成枚举
│   ├── config/                # 配置管理
│   │   ├── computed.py        # 计算配置
│   │   ├── enums.py           # 配置枚举
│   │   ├── extend.py          # 配置扩展
│   │   ├── manager.py         # 配置管理器
│   │   ├── migrations.py      # 配置迁移
│   │   ├── models.py          # 配置模型
│   │   ├── resource_policy.py # 资源策略
│   │   └── resources.py       # 资源定义
│   ├── controllers/           # 控制器（业务逻辑）
│   │   ├── cut_window.py      # 裁剪窗口控制器
│   │   └── main_window/       # 主窗口控制器
│   ├── core/                  # 核心功能
│   │   ├── naming/            # 命名模板
│   │   ├── amazon.py          # Amazon 集成
│   │   ├── face_crop.py       # 人脸裁剪
│   │   ├── file.py            # 文件处理
│   │   ├── file_crawler.py    # 文件刮削
│   │   ├── image.py           # 图像处理
│   │   ├── media_resource.py  # 媒体资源
│   │   ├── mosaic.py          # 马赛克处理
│   │   ├── network_check.py   # 网络检查
│   │   ├── nfo.py             # NFO 生成
│   │   ├── scraper.py         # 刮削器
│   │   ├── tag_priority.py    # 标签优先级
│   │   ├── translate.py       # 翻译
│   │   ├── utils.py           # 核心工具
│   │   └── vsmeta.py          # VSMETA 生成
│   ├── crawlers/              # 爬虫实现
│   │   ├── base/              # 爬虫基类
│   │   ├── dmm_new/           # DMM 爬虫
│   │   └── ...                # 其他网站爬虫
│   ├── gen/                   # 自动生成的代码
│   ├── models/                # 数据模型
│   │   ├── emby.py            # Emby 模型
│   │   ├── enums.py           # 枚举
│   │   ├── flags.py           # 标志
│   │   ├── log_buffer.py      # 日志缓冲
│   │   └── types.py           # 类型定义
│   ├── tools/                 # 工具模块
│   │   ├── actress_db.py      # 演员数据库
│   │   ├── emby_actor_image.py # Emby 演员图片
│   │   ├── emby_actor_info.py # Emby 演员信息
│   │   ├── missing.py         # 缺失文件检测
│   │   ├── subtitle.py        # 字幕工具
│   │   └── wiki.py            # Wiki 工具
│   ├── utils/                 # 工具函数
│   │   ├── crawler_health.py  # 爬虫健康检查
│   │   ├── dataclass.py       # 数据类工具
│   │   ├── file.py            # 文件工具
│   │   ├── gather_group.py    # 收集组
│   │   ├── language.py        # 语言工具
│   │   ├── leb128.py          # LEB128 编码
│   │   ├── path.py            # 路径工具
│   │   ├── perf.py            # 性能工具
│   │   ├── report_system.py   # 报告系统
│   │   ├── video.py           # 视频工具
│   │   └── vsmeta_template_helper.py # VSMETA 模板助手
│   ├── views/                 # UI 视图
│   │   ├── CustomClass.py     # 自定义类
│   │   ├── MDCx.py            # 主窗口 UI（生成）
│   │   ├── MDCx.ui            # 主窗口 UI 定义
│   │   ├── posterCutTool.py   # 裁剪工具 UI（生成）
│   │   └── posterCutTool.ui   # 裁剪工具 UI 定义
│   ├── browser.py             # 浏览器集成
│   ├── consts.py              # 常量
│   ├── crawler.py             # 爬虫提供者
│   ├── image.py               # 图像工具
│   ├── llm.py                 # LLM 集成
│   ├── manual.py              # 手动模式
│   ├── network_fingerprint.py # 网络指纹
│   ├── number.py              # 番号识别
│   ├── signals.py             # 信号定义
│   └── web_async.py           # 异步 Web 请求
├── resources/                 # 资源文件
├── tests/                     # 测试代码
├── scripts/                   # 开发脚本
│   ├── build.py               # 构建脚本
│   ├── bump.py                # 版本升级
│   ├── changelog.py           # 变更日志
│   ├── extract.py             # 提取工具
│   ├── filter_map_xml.py      # 过滤 XML
│   ├── get-dev-info.sh        # 获取开发信息
│   ├── performance_demo.py    # 性能演示
│   ├── pyuic.sh               # UI 转 Python
│   └── stress_missav_cf.py    # 压力测试
├── docs/                      # 文档
├── pyproject.toml             # 项目配置
├── ruff.toml                  # Ruff 配置
└── uv.lock                    # 依赖锁定文件
```

## 开发流程

### Git 工作流

我们使用 [GitHub Flow](https://guides.github.com/introduction/flow/)：

1. **从 main 创建功能分支**

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

2. **进行开发**

```bash
# 添加更改
git add .

# 提交（使用规范的提交信息）
git commit -m "feat: 添加新功能"
```

3. **推送到远程仓库**

```bash
git push origin feature/your-feature-name
```

4. **创建 Pull Request**

在 GitHub 上创建 PR，等待审查。

### 开发周期

1. **理解需求** - 明确要解决的问题
2. **设计方案** - 考虑架构和实现方式
3. **编写代码** - 遵循代码规范
4. **添加测试** - 确保代码质量
5. **运行测试** - 验证功能正常
6. **提交代码** - 使用规范的提交信息

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://peps.python.org/pep-0008/)
- 使用类型注解
- 行长度最大 120 字符
- 使用 4 空格缩进

### 类型注解

```python
# 好的示例
def process_file(file_path: Path, config: Config) -> Result:
    """处理文件并返回结果。"""
    ...

# 避免
def process_file(file_path, config):
    ...
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def scrape_website(number: str, website: Website) -> CrawlerResult:
    """从指定网站刮取番号信息。
    
    Args:
        number: 视频番号
        website: 目标网站
        
    Returns:
        包含刮取结果的 CrawlerResult 对象
        
    Raises:
        CrawlerError: 当刮取失败时
    """
    ...
```

### 导入顺序

1. 标准库导入
2. 第三方库导入
3. 本地模块导入

```python
import os
from pathlib import Path

import httpx
from pydantic import BaseModel

from mdcx.config import Config
from mdcx.models import CrawlerResult
```

### 错误处理

```python
# 使用 try-except 处理预期的错误
try:
    result = await crawler.run(input)
except NetworkError as e:
    logger.error(f"网络错误: {e}")
    raise CrawlerError(f"无法连接到网站: {e}") from e
except Exception as e:
    logger.exception("意外错误")
    raise
```

### Ruff 检查

运行代码检查：

```bash
uv run ruff check .
```

自动修复：

```bash
uv run ruff check . --fix
```

## 最佳实践

### 异步编程

项目大量使用 asyncio，遵循以下原则：

```python
# 使用 await 调用异步函数
async def fetch_data():
    response = await client.get(url)
    return response.json()

# 避免在异步函数中使用阻塞调用
# 错误
async def bad_example():
    time.sleep(1)  # 阻塞！

# 正确
async def good_example():
    await asyncio.sleep(1)
```

### 配置管理

- 在 `mdcx/config/models.py` 中添加新配置项
- 使用配置管理器访问配置
- 考虑配置迁移

```python
from mdcx.config.manager import manager

# 访问配置
config = manager.config
print(config.media_path)
```

### 爬虫开发

添加新爬虫的步骤：

1. 在 `mdcx/crawlers/` 创建新文件
2. 继承 `BaseCrawler`
3. 实现抽象方法
4. 使用 `@register_crawler` 装饰器注册

```python
from mdcx.crawlers.base import BaseCrawler, register_crawler
from mdcx.config.enums import Website

@register_crawler(Website.MY_NEW_SITE)
class MyNewSiteCrawler(BaseCrawler):
    """新网站爬虫。"""
    
    def _generate_search_url(self, ctx, number):
        return f"https://example.com/search?q={number}"
    
    def _parse_search_page(self, ctx, html, search_url):
        # 解析搜索页面
        ...
    
    def _parse_detail_page(self, ctx, html, detail_url):
        # 解析详情页面
        ...
```

### UI 开发

- 修改 `.ui` 文件使用 Qt Designer
- 运行 `scripts/pyuic.sh` 生成 Python 代码
- 在控制器中处理事件

```bash
# 更新 UI 代码
./scripts/pyuic.sh
```

## 测试指南

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/crawlers/test_javbus.py

# 运行特定测试
uv run pytest tests/crawlers/test_javbus.py::test_search

# 显示详细输出
uv run pytest -v

# 生成覆盖率报告
uv run pytest --cov=mdcx --cov-report=html
```

### 编写测试

使用 pytest 编写测试：

```python
import pytest
from mdcx.crawlers.javbus import JavBusCrawler

@pytest.mark.asyncio
async def test_javbus_search():
    """测试 JavBus 搜索功能。"""
    crawler = JavBusCrawler()
    result = await crawler.run("ABP-123")
    
    assert result is not None
    assert result.number == "ABP-123"
```

### 测试分类

- **单元测试**: 测试单个函数或类
- **集成测试**: 测试多个组件的协作
- **爬虫测试**: 测试爬虫功能（可能需要网络）

### 测试 Fixtures

项目提供了一些有用的 fixtures：

```python
# tests/conftest.py 中定义了常用 fixtures
@pytest.fixture
def sample_config():
    """提供示例配置。"""
    return Config(media_path=Path("/test"))
```

## 调试技巧

### 日志记录

使用项目的日志系统：

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
```

### 调试爬虫

在爬虫中添加调试输出：

```python
async def _parse_detail_page(self, ctx, html, detail_url):
    logger.debug(f"解析详情页: {detail_url}")
    # 保存 HTML 用于调试
    with open("debug.html", "w", encoding="utf-8") as f:
        f.write(html)
    ...
```

### 使用调试器

使用 pdb 或 IDE 调试器：

```python
import pdb; pdb.set_trace()  # 在代码中添加断点
```

### 性能分析

使用性能工具：

```python
from mdcx.utils.perf import timing

@timing
async def process_files():
    ...
```

### 常见问题排查

**问题**: 爬虫无法访问网站
**解决**:
1. 检查网络连接
2. 检查代理设置
3. 查看是否有 Cloudflare 保护

**问题**: 测试失败
**解决**:
1. 检查是否有网络依赖
2. 查看测试日志
3. 运行单个测试定位问题

## 常见任务

### 添加新配置项

1. 在 `mdcx/config/models.py` 的 `Config` 类中添加字段
2. 更新 `mdcx/controllers/main_window/load_config.py` 和 `save_config.py`
3. 在 UI 中添加相应控件（如需要）

### 构建可执行文件

```bash
uv run python scripts/build.py
```

### 生成变更日志

```bash
uv run python scripts/changelog.py
```

### 版本升级

```bash
uv run python scripts/bump.py patch  # 补丁版本
uv run python scripts/bump.py minor  # 次版本
uv run python scripts/bump.py major  # 主版本
```

### 运行性能演示

```bash
uv run python scripts/performance_demo.py
```

---

## 获取帮助

- 📚 阅读 [Code Wiki](CODE_WIKI.md) 了解更多技术细节
- 📖 查看 [API 文档](docs/api-documentation.md)
- 🏗️ 参考 [架构设计](docs/architecture.md)
- 🔬 了解 [CI/CD 测试](docs/ci-testing.md)
- 🤝 查看 [贡献指南](CONTRIBUTING.md)
- 在 GitHub Issues 中提问
- 加入 Telegram 交流群

---

祝您开发愉快！

