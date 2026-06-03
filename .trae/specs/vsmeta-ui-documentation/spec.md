# VSMETA UI 配置详细说明 - 产品需求文档

## Overview
- **Summary**: 为 MDCx 的 VSMETA 配置界面添加完整的悬停提示（tooltip）和详细说明，提升用户体验
- **Purpose**: 解决用户在配置 VSMETA 选项时的困惑，让用户在无需查阅外部文档的情况下就能理解每个配置项的作用
- **Target Users**: 所有使用 MDCx VSMETA 功能的用户，特别是新用户

## Why
虽然已有完整的配置文档，但用户在实际配置时需要来回切换查看文档。通过在 UI 界面直接提供详细的 tooltip，可以：
- 大幅减少用户的学习成本
- 降低配置错误率
- 提升用户满意度
- 减少对外部文档的依赖

## What Changes
- 为所有 VSMETA 相关的 UI 控件添加详细的 tooltip 说明
- tooltip 内容包括：
  - 配置项的功能说明
  - 可选值的含义解释
  - 使用建议和最佳实践
  - 常见用例示例
- 确保 UI 标签文字清晰易懂
- 添加模板语法快速参考提示

## Impact
- **Affected specs**:
  - vsmeta-config-documentation: 保持文档与 UI 说明的一致性
- **Affected code**:
  - `mdcx/views/MDCx.py`: 为 UI 控件添加 tooltip 属性
  - `mdcx/views/MDCx.ui`: 更新 UI 定义文件（如需要）

## ADDED Requirements

### Requirement: VSMETA 标题配置 tooltip
系统 SHALL 为 VSMETA 标题配置控件（comboBox_vsmeta_show_title、lineEdit_vsmeta_custom_title）添加详细的 tooltip 说明。

#### Scenario: 悬停查看标题配置说明
- **WHEN** 用户鼠标悬停在标题配置控件上
- **THEN** 显示标题配置的功能说明、可选值含义和使用示例

### Requirement: VSMETA 副标题配置 tooltip
系统 SHALL 为 VSMETA 副标题配置控件（comboBox_vsmeta_show_title2、lineEdit_vsmeta_custom_title2）添加详细的 tooltip 说明。

#### Scenario: 悬停查看副标题配置说明
- **WHEN** 用户鼠标悬停在副标题配置控件上
- **THEN** 显示副标题配置的功能说明、可选值含义和使用示例

### Requirement: VSMETA 简介配置 tooltip
系统 SHALL 为 VSMETA 简介配置控件（comboBox_vsmeta_summary、plainTextEdit_vsmeta_custom_summary）添加详细的 tooltip 说明。

#### Scenario: 悬停查看简介配置说明
- **WHEN** 用户鼠标悬停在简介配置控件上
- **THEN** 显示简介配置的功能说明、可选值含义和使用示例

### Requirement: VSMETA 其他配置项 tooltip
系统 SHALL 为 VSMETA 其他配置控件（图片嵌入、质量设置、数量限制等）添加详细的 tooltip 说明。

#### Scenario: 悬停查看其他配置项说明
- **WHEN** 用户鼠标悬停在任意 VSMETA 配置控件上
- **THEN** 显示该配置项的功能说明和使用建议

### Requirement: 自定义模板语法提示
系统 SHALL 为自定义模板输入框提供模板语法快速参考提示。

#### Scenario: 使用自定义模板
- **WHEN** 用户在自定义模板输入框旁悬停或查看提示
- **THEN** 显示可用占位符列表和基本语法说明

## MODIFIED Requirements
无修改现有需求

## REMOVED Requirements
无删除需求

## Acceptance Criteria

### AC-1: 标题配置 tooltip 完整
- **Given**: 用户在 VSMETA 设置界面
- **When**: 鼠标悬停在标题配置控件上
- **Then**: 显示完整的功能说明、可选值含义和建议
- **Verification**: `human-judgment`

### AC-2: 副标题配置 tooltip 完整
- **Given**: 用户在 VSMETA 设置界面
- **When**: 鼠标悬停在副标题配置控件上
- **Then**: 显示完整的功能说明、可选值含义和建议
- **Verification**: `human-judgment`

### AC-3: 简介配置 tooltip 完整
- **Given**: 用户在 VSMETA 设置界面
- **When**: 鼠标悬停在简介配置控件上
- **Then**: 显示完整的功能说明、可选值含义和建议
- **Verification**: `human-judgment`

### AC-4: 其他配置项 tooltip 完整
- **Given**: 用户在 VSMETA 设置界面
- **When**: 鼠标悬停在其他 VSMETA 配置控件上
- **Then**: 显示该配置项的功能说明和使用建议
- **Verification**: `human-judgment`

### AC-5: 模板语法提示清晰
- **Given**: 用户使用自定义模板功能
- **When**: 查看模板输入区域的提示
- **Then**: 显示清晰的占位符列表和基本语法说明
- **Verification**: `human-judgment`

### AC-6: UI 说明与文档一致
- **Given**: 用户同时查看 UI 和配置文档
- **When**: 比较同一配置项的说明
- **Then**: UI tooltip 和文档说明保持术语一致
- **Verification**: `human-judgment`

## Open Questions
- [ ] 是否需要在 UI 中添加"帮助"按钮，直接跳转到配置文档？
- [ ] tooltip 文字长度是否需要限制？
- [ ] 是否需要添加配置项的默认值提示？
