# 项目复刻与重新品牌化 - 产品需求文档

## Overview
- **Summary**: 将项目从原作者 moyy996/AVDC 的 Fork 复刻为用户自己的项目，替换所有原作者信息和引用
- **Purpose**: 将项目从原项目标识转换为用户自己的项目标识，移除原作者的所有引用
- **Target Users**: 项目维护者

## Why
当前项目是 moyy996/AVDC 的一个分支复刻，但仓库地址和所有文档中仍包含原项目的信息。需要将这些信息替换为用户自己的项目信息。

## What Changes

### 需要修改的信息：

1. **GitHub 仓库地址**：
   - 原：`https://github.com/1525745393/mdcx-AI`
   - 待替换为用户自己的仓库地址

2. **原作者信息**：
   - moyy996（原作者 GitHub 用户名）
   - 1525745393（当前仓库所有者）
   - yoshiko2（Core 作者）

3. **项目引用**：
   - AVDC（原作者项目名称）
   - moyy996/AVDC（原项目仓库地址）
   - anyabc/something（相关历史分支）

## Impact

### Affected Files (45 处需要修改)：

**代码文件：**
- `mdcx/consts.py` - GITHUB_REPO 常量
- `mdcx/views/MDCx.py` - UI 中显示的链接和版权信息（约 6 处）
- `mdcx/views/MDCx.ui` - UI 定义文件（约 6 处）
- `mdcx/controllers/main_window/init.py` - 打开的链接

**文档文件：**
- `README.md` - 项目说明（约 4 处）
- `CODE_WIKI.md` - Code Wiki 文档
- `USER_GUIDE.md` - 用户指南（约 4 处）
- `DEVELOPMENT.md` - 开发文档
- `CONTRIBUTING.md` - 贡献指南
- `FAQ.md` - 常见问题（约 3 处）
- `INSTALL.md` - 安装说明（约 9 处）
- `docs/README.md` - 文档索引
- `docs/api-documentation.md` - API 文档
- `docs/architecture.md` - 架构文档

## Goals
- [ ] 替换所有 `1525745393/mdcx-AI` 为用户自己的仓库地址
- [ ] 替换所有 `moyy996/AVDC` 为用户自己的项目引用
- [ ] 替换所有 `moyy996` 引用
- [ ] 替换 `yoshiko2` 引用
- [ ] 保留必要的致谢信息（在 Credits 部分）
- [ ] 提供用户输入接口（让用户填写自己的信息）

## Non-Goals (Out of Scope)
- 不修改核心业务逻辑
- 不修改项目名称 MDCx
- 不删除原作者的致谢信息（在合适的部分）
- 不修改版本号

## Functional Requirements

- **FR-1**: 用户提供新的 GitHub 用户名
- **FR-2**: 用户提供新的仓库名称
- **FR-3**: 系统批量替换所有引用
- **FR-4**: 保留必要的致谢信息

## Non-Functional Requirements

- **NFR-1**: 替换过程可追溯
- **NFR-2**: 保持代码可运行
- **NFR-3**: 不破坏现有功能

## Open Questions
- [ ] 用户的 GitHub 用户名是什么？
- [ ] 用户的新仓库名称是什么？
- [ ] 是否需要在 README 中保留原作者的致谢？
- [ ] 是否需要修改 GitHub Actions 工作流？
- [ ] 是否需要修改项目描述（description）？
