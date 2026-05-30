# AGENTS.md

本文件为 AI 编程助手提供项目上下文，帮助其理解项目结构、代码规范和开发流程。

---

## 项目概述

MDCx 是一个现代化的视频元数据刮削和管理工具：

- **语言**: Python 3.13+
- **包管理**: uv
- **UI 框架**: PyQt6
- **主要功能**: 从 40+ 网站自动获取视频信息，生成 NFO/VSMETA 元数据文件

---

## 目录结构

```
mdcx/
├── base/                    # 基础工具模块
│   ├── file.py            # 文件操作
│   ├── image.py           # 图片处理
│   ├── number.py          # 番号解析
│   ├── translate.py       # 翻译接口
│   ├── video.py           # 视频处理
│   ├── web.py             # 异步网络请求
│   └── web_sync.py        # 同步网络请求
│
├── cmd/                    # 命令行入口
│   ├── crawl.py           # 爬虫 CLI (crawl 命令)
│   └── gen_enums.py       # 枚举生成工具
│
├── config/                  # 配置管理
│   ├── enums.py           # 配置枚举 (OutlineShow, Switch, etc.)
│   ├── models.py          # Pydantic Config 模型定义
│   ├── manager.py         # ConfigManager 单例，运行时配置访问入口
│   └── migrations.py      # 配置迁移逻辑
│
├── controllers/             # Qt UI 控制器层
│   └── main_window/
│       ├── init.py        # 信号连接初始化
│       ├── handlers.py    # UI 事件处理器
│       ├── main_window.py # 主窗口控制器
│       ├── load_config.py # 从 Config 模型加载到 UI
│       ├── save_config.py # 从 UI 保存到 Config 模型
│       ├── bind_utils.py  # UI 绑定工具
│       └── style.py       # Qt 样式表
│
├── core/                   # 核心业务逻辑
│   ├── naming/            # 文件命名系统
│   │   ├── template.py    # Jinja2 模板引擎
│   │   ├── renderer.py    # 模板渲染器
│   │   ├── fields.py      # 命名字段定义
│   │   └── sanitize.py    # 文件名消毒
│   ├── scraper.py         # 刮削主流程
│   ├── file_crawler.py    # 文件扫描和处理
│   ├── nfo.py             # NFO 文件生成
│   ├── vsmeta.py          # VSMETA 二进制文件生成
│   ├── translate.py        # LLM 翻译服务
│   ├── mosaic.py          # 马赛克检测
│   ├── face_crop.py       # 人脸检测裁剪
│   └── amazon.py          # Amazon 条码识别
│
├── crawlers/              # 网站爬虫 (40+ 实现)
│   ├── base/
│   │   ├── base.py        # GenericBaseCrawler[T] 抽象基类
│   │   ├── parser.py      # 通用解析器
│   │   └── types.py       # 爬虫数据类型
│   ├── javbus.py         # JavBus 爬虫
│   ├── javdbapi.py       # JavDB API 爬虫
│   ├── missav.py         # MissAV 爬虫
│   └── [其他 40+ 爬虫实现]
│
├── models/                 # 数据模型
│   ├── types.py           # CrawlerResult, FileInfo 等核心类型
│   ├── enums.py           # 业务枚举
│   ├── flags.py           # 命名旗标
│   └── log_buffer.py      # 日志缓冲
│
├── tools/                  # 独立工具
│   ├── emby_actor_info.py # Emby 演员信息
│   ├── missing.py         # 缺失文件检查
│   └── wiki.py            # Wiki 数据获取
│
├── utils/                  # 通用工具
│   ├── file.py           # 文件工具
│   ├── path.py           # 路径工具
│   ├── video.py          # 视频工具
│   ├── language.py       # 语言检测
│   └── leb128.py         # VSMETA 编码
│
├── views/                 # Qt UI 定义 (由 .ui 自动生成)
│   ├── MDCx.ui           # Qt Designer 主窗口文件
│   ├── MDCx.py           # 自动生成，不直接编辑
│   ├── posterCutTool.ui  # 海报裁剪窗口
│   └── posterCutTool.py  # 自动生成
│
├── signals.py             # Qt 信号定义
├── consts.py             # 常量 (版本号等)
└── web_async.py          # 异步 HTTP 客户端

scripts/                    # 开发脚本
├── build.py               # PyInstaller 构建脚本
├── bump.py                # 版本号递增工具
├── changelog.py           # 变更日志生成
├── pyuic.sh              # Qt UI → Python 代码转换
└── extract.py             # 数据提取工具

tests/                      # 单元测试
├── core/                  # 核心模块测试
├── crawlers/              # 爬虫测试
└── test_*.py             # 功能测试

.github/workflows/          # CI/CD
├── ci.yaml               # 代码质量检查 (ruff format/check)
├── test.yml              # 测试工作流
└── release.yml           # 发布工作流 (构建 + Release)
```

---

## 开发命令

### 环境准备

```bash
# 克隆并安装依赖
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI
uv sync --locked --all-extras --dev

# 安装 pre-commit hooks
uv run pre-commit install

# 安装为可编辑包
uv pip install -e .
```

### 运行

```bash
# 运行 GUI 版本
uv run python mdcx/views/MDCx.py

# 运行 CLI 版本
uv run crawl --help
```

### 构建

```bash
# 构建可执行文件 (需要 PyInstaller)
uv run build

# 仅递增版本号
uv run bump --increment 1

# 指定版本号
uv run bump --version 123456789

# 生成变更日志模板
uv run changelog
```

### 代码生成

```bash
# 重新生成 Qt UI Python 代码
bash scripts/pyuic.sh

# 生成枚举代码
uv run gen_enums
```

---

## 测试命令

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/core/test_nfo_read.py

# 带覆盖率
uv run pytest --cov=mdcx --cov-report=html

# 跳过需要网络的测试
uv run pytest -m "not network"

# 仅运行特定标记的测试
uv run pytest -m "unit"
```

---

## 代码风格

### 工具链

- **格式化**: ruff format (基于 Black)
- **检查**: ruff check
- **行长度**: 120 字符
- **缩进**: 4 空格

### 启用的检查规则

| 规则前缀 | 说明 |
|---------|------|
| `I` | isort 导入排序 |
| `UP` | pyupgrade (现代 Python 语法) |
| `E` | pycodestyle (语法错误) |
| `F` | Pyflakes (常见错误) |
| `B` | flake8-bugbear (潜在 bug) |
| `C4` | flake8-comprehensions (列表推导等) |
| `FAST` | 性能建议 |
| `ASYNC230` | 异步函数不应使用阻塞 I/O |
| `ASYNC251` | 异步函数不应使用 time.sleep |

### 常用命令

```bash
# 检查并修复
uv run ruff check --fix .

# 格式化
uv run ruff format .

# 检查特定文件
uv run ruff check mdcx/core/vsmeta.py

# 忽略行长度警告 (E501 默认忽略)
```

### 特殊规则

- `__init__.py`: 允许 E402, F401, F403, F811 (导入相关警告)
- `**/views/*.py`: 不检查 (自动生成文件)

---

## 禁止事项

### 1. 不要直接编辑自动生成的文件

```
禁止编辑:
- mdcx/views/MDCx.py      # 由 pyuic.sh 从 MDCx.ui 自动生成
- mdcx/views/posterCutTool.py  # 由 pyuic.sh 从 posterCutTool.ui 生成
- mdcx/gen/field_enums.py  # 由 gen_enums 命令自动生成
```

如需修改 UI，编辑对应的 `.ui` 文件后运行 `bash scripts/pyuic.sh`。

### 2. 不要在 views/ 中添加业务逻辑

views/ 目录应该只包含 Qt UI 相关的代码。业务逻辑应该放在 controllers/ 或 core/ 中。

### 3. 不要硬编码敏感信息

- API 密钥、Token 等应通过环境变量或配置文件管理
- 日志输出不应包含个人隐私信息

### 4. 不要混用同步/异步代码

- `mdcx/core/` 中的业务逻辑使用 `async/await`
- `mdcx/base/web_sync.py` 用于需要同步执行的场景
- 异步函数不应使用 `time.sleep()`，应使用 `asyncio.sleep()`

### 5. 不要忽略类型注解

- 公开接口应添加类型注解
- 使用 Pydantic 模型进行配置和数据验证
- 关键函数应添加 docstring

### 6. 不要提交未通过检查的代码

```bash
# 推送前确保通过
uv run ruff check --fix .
uv run ruff format .
uv run pytest
```

---

## 配置管理规范

### 添加新配置项流程

1. **定义枚举** (如需): 在 `mdcx/config/enums.py` 中添加枚举类
2. **添加字段**: 在 `mdcx/config/models.py` 的 `Config` 类中添加字段及默认值
3. **UI 绑定**:
   - 在 `mdcx/views/MDCx.ui` 中使用 Qt Designer 添加控件
   - 运行 `bash scripts/pyuic.sh` 重新生成 Python 代码
   - 在 `mdcx/controllers/main_window/load_config.py` 中添加加载逻辑
   - 在 `mdcx/controllers/main_window/save_config.py` 中添加保存逻辑
4. **使用配置**: 通过 `from mdcx.models.config.manager import manager` 访问

### 配置访问方式

```python
from mdcx.models.config.manager import manager

# 读取配置
value = manager.config.some_field

# 写入配置
manager.config.some_field = new_value
```

---

## 发布流程

1. 更新 changelog.md
2. 运行 `uv run bump --increment 1` 或指定版本号
3. 提交并推送
4. 创建并推送 tag (`git tag <version> && git push origin <version>`)
5. GitHub Actions 自动触发构建和发布

---

## 常用文件位置参考

| 功能 | 文件路径 |
|------|----------|
| 版本号 | `mdcx/consts.py` → `LOCAL_VERSION` |
| 配置模型 | `mdcx/config/models.py` → `class Config` |
| ConfigManager | `mdcx/config/manager.py` |
| NFO 生成 | `mdcx/core/nfo.py` |
| VSMETA 生成 | `mdcx/core/vsmeta.py` |
| 爬虫基类 | `mdcx/crawlers/base/base.py` |
| 命名系统 | `mdcx/core/naming/` |
| 日志输出 | `mdcx/models/log_buffer.py` → `LogBuffer` |
