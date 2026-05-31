# VSMETA 自定义模板功能优化 - 产品需求文档

## Overview
- **Summary**: 优化VSMETA自定义模板功能，增强用户体验、扩展功能、提高稳定性
- **Purpose**: 提供更强大、更易用的模板系统，满足用户多样化的定制需求
- **Target Users**: MDCx用户，特别是深度使用VSMETA功能的用户

## Goals
- 改进模板渲染引擎，增强功能和安全性
- 提供更好的用户体验和辅助功能
- 支持模板管理和复用
- 增强错误处理和用户反馈

## Non-Goals (Out of Scope)
- 不改变现有的基本占位符功能（保持向后兼容）
- 不添加脚本编程功能（避免复杂性和安全风险）
- 不改变VSMETA文件格式

## Background & Context
当前的实现（[vsmeta.py#401-433](file:///workspace/mdcx/core/vsmeta.py#L401-L433)）使用简单的字符串替换，功能有限，用户体验可以进一步改善。

## Functional Requirements
- **FR-1**: 增强的模板语法和渲染引擎
- **FR-2**: 模板验证和错误提示
- **FR-3**: 模板管理功能（保存、加载、预设）
- **FR-4**: UI辅助功能（占位符选择器、语法高亮、预览）
- **FR-5**: 扩展占位符支持

## Non-Functional Requirements
- **NFR-1**: 向后兼容现有模板
- **NFR-2**: 保持渲染性能（<1ms）
- **NFR-3**: 清晰的错误提示和用户引导

## Constraints
- **Technical**: 使用现有Python环境，不引入额外依赖
- **Business**: 保持代码简洁易维护
- **Dependencies**: 依赖现有CrawlersResult数据结构

## Assumptions
- 用户熟悉基本的模板概念
- 现有占位符功能使用场景良好

## Acceptance Criteria

### AC-1: 增强模板语法
- **Given**: 用户使用模板
- **When**: 模板包含条件占位符 `{if:number}{number}{/if}`
- **Then**: 只在字段有值时渲染该部分
- **Verification**: `programmatic`

### AC-2: 模板验证
- **Given**: 用户输入包含无效占位符的模板
- **When**: 系统验证模板
- **Then**: 提示无效占位符并提供帮助
- **Verification**: `human-judgment`

### AC-3: 模板预设
- **Given**: 用户打开VSMETA设置
- **When**: 用户选择预设模板
- **Then**: 预设模板自动填充到输入框
- **Verification**: `human-judgment`

### AC-4: 占位符选择器
- **Given**: 用户在编辑模板
- **When**: 用户点击占位符按钮
- **Then**: 显示可选占位符列表，点击后自动插入
- **Verification**: `human-judgment`

### AC-5: 实时预览更新
- **Given**: 用户在编辑模板
- **When**: 模板内容改变
- **Then**: 预览实时更新
- **Verification**: `human-judgment`

## Open Questions
- [ ] 是否需要用户自定义模板保存功能？
- [ ] 是否需要支持更复杂的格式化功能（如日期格式化）？
