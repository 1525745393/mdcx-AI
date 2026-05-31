# MDCx 安装和部署指南

> 📖 **更多文档**: [文档中心](docs/README.md) | [主 README](README.md) | [用户手册](USER_GUIDE.md) | [FAQ](FAQ.md)

本文档详细介绍 MDCx 在不同平台的安装方法、从源码构建步骤以及部署最佳实践。

## 目录

- [系统要求](#系统要求)
- [快速安装](#快速安装)
  - [Windows 安装](#windows-安装)
  - [macOS 安装](#macos-安装)
  - [Linux 安装](#linux-安装)
- [从源码运行](#从源码运行)
- [从源码构建](#从源码构建)
- [部署最佳实践](#部署最佳实践)
- [故障排除](#故障排除)

## 系统要求

### 最低配置

- **操作系统**:
  - Windows 10 或更高版本
  - macOS 10.15 (Catalina) 或更高版本
  - Linux (现代发行版，如 Ubuntu 20.04+, Fedora 35+)
- **Python**: 3.13.4 或更高版本（仅从源码运行需要）
- **内存**: 4 GB RAM
- **磁盘空间**: 500 MB 可用空间
- **网络**: 需要互联网连接用于刮取数据

### 推荐配置

- **操作系统**: Windows 11, macOS 13+, 最新的 Linux 发行版
- **内存**: 8 GB RAM 或更多
- **磁盘空间**: 1 GB 可用空间
- **Python**: 3.13.4 或更高版本

### 依赖说明

MDCx 使用以下主要依赖：
- **PyQt6**: 图形界面框架
- **httpx / curl_cffi**: 网络请求
- **Pillow**: 图像处理
- **OpenCV**: 人脸裁剪等高级图像处理
- **av**: 视频处理
- **pydantic**: 数据验证

---

## 快速安装

### 方法一：使用预编译版本（推荐）

预编译版本是最简单的安装方式，无需安装 Python 或配置开发环境。

#### Windows 安装

1. **下载预编译版本**
   - 访问 [GitHub Releases](https://github.com/1525745393/mdcx-AI/releases)
   - 下载最新版本的 `MDCx-*.exe` 文件

2. **安装步骤**
   - 将下载的 `.exe` 文件放到您想要的文件夹中
   - 双击运行即可（无需安装过程）

3. **创建快捷方式（可选）**
   - 右键点击 `.exe` 文件
   - 选择"发送到" > "桌面快捷方式"
   - 重命名快捷方式为 "MDCx"

4. **首次运行**
   - 首次启动可能会被 Windows SmartScreen 拦截
   - 点击"更多信息"，然后点击"仍要运行"

#### macOS 安装

1. **下载预编译版本**
   - 访问 [GitHub Releases](https://github.com/1525745393/mdcx-AI/releases)
   - 下载最新版本的 `MDCx-*.dmg` 文件

2. **安装步骤**
   - 双击下载的 `.dmg` 文件
   - 将 `MDCx.app` 拖入 `Applications` 文件夹
   - 从 `Applications` 文件夹中打开 MDCx

3. **打开未签名的应用（如需要）**
   macOS 可能会阻止未签名的应用运行：
   - 右键点击 `MDCx.app`
   - 选择"打开"
   - 在弹出的对话框中再次点击"打开"

   或者通过系统设置允许：
   - 打开"系统设置" > "隐私与安全性"
   - 在"安全性"部分，点击"仍要打开"

#### Linux 安装

目前官方没有提供预编译的 Linux 版本，请参考[从源码运行](#从源码运行) 部分。

---

### 方法二：从源码运行

如果您想要最新的开发版本或需要修改代码，可以从源码运行。

#### 前置准备

1. **安装 Git**
   - Windows: 下载并安装 [Git for Windows](https://git-scm.com/download/win)
   - macOS: 安装 Xcode Command Line Tools: `xcode-select --install` 或使用 Homebrew: `brew install git`
   - Linux: 使用包管理器安装，例如: `sudo apt install git` (Ubuntu/Debian) 或 `sudo dnf install git` (Fedora)

2. **安装 Python 3.13.4+**
   - Windows/macOS: 从 [python.org](https://www.python.org/downloads/) 下载安装
   - Linux: 使用包管理器安装（可能需要添加 PPA 或第三方源）

3. **安装 uv（推荐的包管理器）**
   ```bash
   # 自动安装脚本（适用于所有平台）
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # 或者使用 pip 安装
   pip install uv
   ```

#### Windows 从源码运行

```powershell
# 1. 克隆仓库
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI

# 2. 安装依赖
uv sync --locked --all-extras --dev

# 3. 运行程序
uv run python main.py
```

#### macOS 从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI

# 2. 安装依赖
uv sync --locked --all-extras --dev

# 3. 运行程序
uv run python main.py
```

#### Linux 从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI

# 2. 安装系统依赖（根据发行版）
# Ubuntu/Debian
sudo apt update
sudo apt install python3.13 python3.13-dev python3.13-venv \
                 build-essential libgl1 libxkbcommon-x11-0 \
                 libxcb-cursor0 libxkbcommon0

# Fedora
sudo dnf install python3.13 python3.13-devel gcc-c++ \
                 mesa-libGL xcb-util-cursor libxkbcommon

# 3. 安装 Python 依赖
uv sync --locked --all-extras --dev

# 4. 运行程序
uv run python main.py
```

#### 使用 pip（替代 uv）

如果您不想使用 uv，也可以使用 pip：

```bash
# 克隆仓库
git clone https://github.com/1525745393/mdcx-AI.git
cd mdcx-AI

# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -e .[dev]

# 运行程序
python main.py
```

---

## 从源码构建

如果您想要自己构建可执行文件，可以按照以下步骤操作。

### 构建环境准备

#### Windows 构建环境

1. 安装 Python 3.13.4+
2. 安装 Git
3. 安装 uv（参考前面的步骤）
4. 安装 [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)（需要 C++ 构建工具）

#### macOS 构建环境

1. 安装 Python 3.13.4+
2. 安装 Git
3. 安装 uv
4. 安装 Xcode Command Line Tools: `xcode-select --install`
5. 安装 create-dmg（用于生成 DMG 文件）: `brew install create-dmg`

#### Linux 构建环境

1. 安装 Python 3.13.4+
2. 安装 Git
3. 安装 uv
4. 安装系统构建工具

### 构建步骤

1. **获取源代码**
   ```bash
   git clone https://github.com/1525745393/mdcx-AI.git
   cd mdcx-AI
   ```

2. **安装开发依赖**
   ```bash
   uv sync --locked --all-extras --dev
   ```

3. **运行构建脚本**

   **Windows**:
   ```bash
   uv run python scripts/build.py --debug
   ```

   **macOS**:
   ```bash
   # 构建并生成 DMG 文件
   uv run python scripts/build.py --create-dmg --version 220260563 --debug
   ```

   **Linux**:
   ```bash
   uv run python scripts/build.py --debug
   ```

4. **查找构建产物**
   - Windows: `dist/MDCx.exe`
   - macOS: `dist/MDCx.app` 或 `dist/MDCx.dmg`（如果使用 `--create-dmg`）
   - Linux: `dist/MDCx`

### 构建脚本参数

`scripts/build.py` 支持以下参数：

| 参数 | 说明 |
|------|------|
| `--version, -v` | 指定版本号（默认从代码读取） |
| `--app-name, -n` | 指定应用名称（默认: MDCx） |
| `--create-dmg, --dmg` | 创建 DMG 文件（仅 macOS） |
| `--debug` | 启用调试模式，保留临时文件 |
| `--no-color` | 禁用颜色输出 |

### 使用 GitHub Actions 构建

您也可以使用项目的 GitHub Actions 工作流来自动构建：

1. Fork 项目仓库
2. 在仓库设置中启用 Actions
3. 设置构建变量（如需要）：
   - `BUILD_FOR_WINDOWS_LEGACY`: 为 Windows 7 构建
   - `BUILD_FOR_MACOS_LEGACY`: 为旧版本 macOS 构建
4. 手动触发 "Build and Release" 工作流

---

## 部署最佳实践

### 生产环境部署

#### 配置文件位置

MDCx 的配置文件默认存储在以下位置：

| 平台 | 配置目录 |
|------|----------|
| Windows | `%APPDATA%\MDCx\` |
| macOS | `~/Library/Application Support/MDCx/` |
| Linux | `~/.config/MDCx/` |

#### 数据备份建议

建议定期备份以下内容：

1. **配置文件**: 包含所有设置和自定义配置
2. **媒体库元数据**: 如果使用本地存储
3. **演员数据库**: 如果使用自定义演员信息

备份方法：
```bash
# Windows
xcopy "%APPDATA%\MDCx" "D:\Backup\MDCx\%DATE%" /E /I

# macOS
cp -r ~/Library/Application\ Support/MDCx ~/Backups/MDCx-$(date +%Y%m%d)

# Linux
cp -r ~/.config/MDCx ~/Backups/MDCx-$(date +%Y%m%d)
```

### 性能优化

#### 1. 调整并发数

根据您的网络和系统性能调整并发刮削数量：
- 打开 MDCx > 设置 > 刮削
- 调整"最大并发数"（推荐 2-10）

#### 2. 优化图片下载

- 降低图片质量（如果不需要最高质量）
- 禁用不需要的图片类型（如背景图）
- 启用图片压缩

#### 3. 网络优化

- 使用代理加速访问（如需要）
- 设置合理的超时时间
- 启用重试机制

### 安全建议

1. **不要分享配置文件** - 配置文件可能包含 API 密钥
2. **使用防火墙** - 限制不必要的网络访问
3. **定期更新** - 保持 MDCx 为最新版本
4. **API 密钥保护** - 不要将包含 API 密钥的配置提交到公开仓库

### 多用户部署

对于服务器环境或多用户场景：

1. **使用独立配置目录**
   - 为每个用户指定单独的配置目录
   - 通过命令行参数或环境变量指定

2. **权限管理**
   - 确保用户对媒体目录有适当的读写权限
   - 配置文件目录权限设置为 700（仅用户可读写）

### Docker 部署（高级）

虽然 MDCx 主要是桌面应用，但可以通过 Docker 部署到服务器（需要配合 X11 转发或 VNC）：

```dockerfile
# 示例 Dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    libxkbcommon-x11-0 \
    libxcb-cursor0 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆代码
RUN git clone https://github.com/1525745393/mdcx-AI.git .

# 安装依赖
RUN uv sync --locked --all-extras

# 设置环境变量
ENV DISPLAY=:0

# 运行应用
CMD ["uv", "run", "python", "main.py"]
```

---

## 故障排除

### 常见问题

#### 问题：程序无法启动

**Windows**:
- 确保安装了 [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- 尝试以管理员身份运行
- 检查是否被杀毒软件拦截

**macOS**:
- 检查 Gatekeeper 设置（系统设置 > 隐私与安全性）
- 尝试右键点击 > 打开

**所有平台**:
- 查看日志文件（通常在配置目录下）
- 从命令行运行查看详细错误信息

#### 问题：网络连接失败

1. 检查网络连接
2. 在设置中配置代理
3. 检查防火墙设置
4. 尝试使用 curl_cffi 而不是 httpx

#### 问题：刮削失败

1. 检查目标网站是否可访问
2. 尝试更换刮削源
3. 检查网络设置
4. 查看日志获取详细错误信息

#### 问题：Python 依赖安装失败

1. 更新 pip/uv:
   ```bash
   uv self update
   # 或
   pip install --upgrade pip
   ```

2. 使用国内镜像源：
   ```bash
   # 使用清华镜像
   uv pip install -e .[dev] --index-url https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. 清除缓存重新安装：
   ```bash
   uv cache clean
   rm -rf .venv
   uv sync --locked --all-extras --dev
   ```

#### 问题：构建失败

1. 确保所有构建依赖都已安装
2. 检查 Python 版本（需要 3.13.4+）
3. 查看构建脚本的详细输出
4. 使用 `--debug` 参数保留临时文件进行调试

### 获取帮助

如果您遇到问题：

1. 查看 [FAQ.md](FAQ.md)
2. 查看 [GitHub Issues](https://github.com/1525745393/mdcx-AI/issues) 是否有类似问题
3. 加入 [Telegram 交流群](https://t.me/mdcx_chat) 寻求帮助
4. 创建新的 Issue 并提供详细信息：
   - 操作系统版本
   - MDCx 版本
   - 错误日志
   - 复现步骤

---

## 附录

### 命令行工具

MDCx 提供了一些命令行工具：

```bash
# 命令行刮削
uv run python -m mdcx.cmd.crawl

# 生成枚举
uv run python -m mdcx.cmd.gen_enums

# 运行构建
uv run python scripts/build.py

# 版本升级
uv run python scripts/bump.py patch

# 生成变更日志
uv run python scripts/changelog.py
```

### 相关文档

- [README.md](README.md) - 项目简介和快速开始
- [DEVELOPMENT.md](DEVELOPMENT.md) - 开发指南
- [CODE_WIKI.md](CODE_WIKI.md) - 技术文档
- [USER_GUIDE.md](USER_GUIDE.md) - 用户使用指南
- [FAQ.md](FAQ.md) - 常见问题解答

---

祝您使用愉快！如有问题，请参考上述资源获取帮助。
