# CI 测试说明

本项目使用 GitHub Actions 进行自动化测试和构建。

## CI 工作流程

### 1. 测试工作流 (`.github/workflows/test.yml`)

自动在以下事件触发时运行测试：
- 推送到 `main`/`master` 分支
- 拉取请求
- 手动触发

**测试覆盖平台：**
- Ubuntu (最新版)
- macOS (最新版)
- Windows (最新版)

### 2. 发布工作流 (`.github/workflows/release.yml`)

自动在标签推送或发布时构建可执行文件。

## CI 环境配置

### Linux 依赖安装

在 Ubuntu CI 环境中安装必要的系统库以支持 PyQt6：

```bash
sudo apt-get install -y \
  libegl1-mesa \
  libxkbcommon-x11-0 \
  libxcb-cursor0 \
  libxcb-xinerama0 \
  libxkbcommon0 \
  libx11-xcb1 \
  xvfb
```

### 使用 Xvfb 运行测试

在 Linux 无头环境中，使用 `xvfb-run` 来提供虚拟 X 窗口环境：

```bash
xvfb-run -a python -m pytest tests/
```

## 本地开发

### 在本地环境运行测试

```bash
# 安装依赖
uv sync --locked --all-extras --dev

# 运行所有测试
uv run python -m pytest tests/ -v

# 运行特定测试
uv run python -m pytest tests/core/test_amazon_core.py -v
```

### 跳过 PyQt6 相关测试

如果您的环境没有可用的 GUI 或不想运行 PyQt6 依赖的测试，可以使用跳过装饰器：

```python
from tests.conftest import requires_pyqt6_available, skip_on_ci

@pytest.mark.pyqt6
@requires_pyqt6_available
def test_gui_feature():
    # 需要 PyQt6 的测试代码
    pass
```

## 测试跳过规则

测试跳过逻辑定义在 `tests/conftest.py` 中：

1. `is_ci()` - 检测 CI 环境
2. `is_headless()` - 检测无头 Linux 环境
3. `@skip_if_ci_headless()` - CI/无头环境下跳过
4. `@skip_on_ci()` - CI 环境下跳过
5. `@requires_pyqt6_available` - 要求 PyQt6 可用

## 覆盖率报告

CI 运行后会生成覆盖率报告并上传为 artifact。

```bash
# 本地生成覆盖率报告
uv run python -m pytest tests/ --cov=mdcx --cov-report=html
```
