# 发布说明

## 版本 220260529

发布日期: 2026-05-24

### 新增功能

- 新增 Amazon 核心模块单元测试 (37个测试用例)
- 新增 Scraper 核心模块单元测试
- 添加 CI/CD 测试工作流

### Bug修复

- 修复 tab_3 命名标签页布局重叠问题
- 修复代码质量问题 (Ruff)
- 优化滚动区域高度设置

### 改进

- 增加测试覆盖率至 42%
- 完善 CI 环境配置文档
- 添加 PyQt6 依赖跳过机制

### 文件变更

- 新增: .github/workflows/test.yml
- 新增: tests/core/test_amazon_core.py
- 新增: tests/core/test_scraper_core.py
- 新增: tests/conftest.py
- 新增: docs/ci-testing.md
- 修改: mdcx/views/MDCx.ui

### 测试状态

- ✅ 59 个核心测试通过
- ⏭️ 2 个测试跳过 (OpenCV相关)

### 手动创建 Release

由于 GitHub CLI 未安装，请手动创建 Release：

1. 访问: https://github.com/1525745393/mdcx-AI/releases/new
2. 选择标签: `220260529`
3. 标题: `版本 220260529`
4. 复制上方发布说明到说明框
5. 点击 "Publish release"
