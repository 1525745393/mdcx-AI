# v220260565 版本发布 - Product Requirement Document

## Overview
- **Summary**: 发布新版本 v220260565，包含 VSMETA UI 配置 tooltip 完善和详细的配置说明
- **Purpose**: 将最新的 UI 改进和文档完善打包发布，提升用户使用体验
- **Target Users**: MDCx 应用的所有用户，特别是使用 VSMETA 功能的用户

## Goals
- [ ] 更新版本号至 220260565
- [ ] 更新 changelog 文档，添加本次发布的变更内容
- [ ] 创建并推送 git 标签
- [ ] 触发 GitHub Actions 自动构建和发布
- [ ] 确保发布过程顺利完成

## Non-Goals (Out of Scope)
- 不添加新功能（本次版本主要是 UI 改进和文档完善）
- 不修改核心业务逻辑
- 不进行重大重构

## Background & Context
当前项目状态：
- 最新版本：220260564
- 主要变更：
  - VSMETA UI 配置控件的详细 tooltip 添加
  - VSMETA 配置完整的 UI 说明文档
  - VSMETA 自定义模板语法完整指南
  - 所有 VSMETA 相关配置选项的说明完善
- 工作树：干净，无未提交的修改
- Git 标签：v220260564 已存在
- 远程仓库：已同步

## Functional Requirements
- **FR-1**: 版本号更新
- **FR-2**: Changelog 文档更新
- **FR-3**: Git 标签创建
- **FR-4**: 触发自动构建和发布

## Non-Functional Requirements
- **NFR-1**: 发布过程要安全可靠
- **NFR-2**: 保持代码库的完整性
- **NFR-3**: 构建应成功通过
- **NFR-4**: 发布应可追踪

## Constraints
- **Technical**: 使用现有的 GitHub Actions 工作流
- **Business**: 需保持向后兼容
- **Dependencies**: 项目依赖的外部库保持不变

## Assumptions
- 所有代码变更已经过验证
- 远程仓库访问正常
- GitHub Actions 工作流配置正确
- 用户可以正常访问 GitHub

## Acceptance Criteria

### AC-1: 版本号正确更新
- **Given**: 版本号当前为 220260564
- **When**: 更新 consts.py
- **Then**: LOCAL_VERSION 应为 220260565
- **Verification**: `programmatic`

### AC-2: Changelog 文档已更新
- **Given**: changelog.md 当前有 220260564 条目
- **When**: 添加新的版本条目，包含 VSMETA UI tooltip 完善、VSMETA 配置说明、UI 文档等内容
- **Then**: 文件应包含 220260565 版本信息
- **Verification**: `programmatic`

### AC-3: Git 标签已创建
- **Given**: 本地仓库状态干净
- **When**: 创建 git 标签
- **Then**: 标签 220260565 和 v220260565 应存在
- **Verification**: `programmatic`

### AC-4: 标签已推送到远程
- **Given**: 本地标签已创建
- **When**: 推送到远程仓库
- **Then**: 远程仓库应包含新标签
- **Verification**: `programmatic`

### AC-5: GitHub Actions 已触发
- **Given**: 标签已推送
- **When**: 检查 Actions 状态
- **Then**: 应能看到新的构建正在运行或已完成
- **Verification**: `human-judgment`

## Open Questions
- [ ] 本次发布是否需要其他特殊的发布处理？
