# VSMETA 配置详细说明 - 产品需求文档

## Overview
- **Summary**: 为 MDCx 的 VSMETA 配置选项添加详细的中文说明文档，帮助用户理解每个配置项的作用和使用方法
- **Purpose**: 降低用户的学习成本，提高 VSMETA 功能的可理解性和易用性
- **Target Users**: 所有使用 MDCx VSMETA 功能的用户，特别是新用户和需要深度定制的用户

## Why
当前 VSMETA 配置界面缺乏详细的中文说明，用户难以理解每个选项的具体作用和最佳使用场景。这导致：
- 用户需要反复试验才能找到合适的配置
- 配置错误导致生成的 VSMETA 文件不符合预期
- 高级功能（如自定义模板）利用率低

## What Changes
- 在 UI 界面的 VSMETA 配置区域添加悬停提示和说明文字
- 更新配置文档（docs/CONFIGURATION.md）添加 VSMETA 章节
- 为每个配置项提供：
  - 功能说明
  - 可选值列表及含义
  - 使用场景和示例
  - 注意事项和最佳实践
- 添加配置项与 VSMETA 标签的对应关系说明

## Impact
- **Affected specs**:
  - VSMETA Template Enhancements: 扩展文档覆盖范围
  - Documentation Improvement: 补充技术文档内容
- **Affected code**:
  - `mdcx/views/MDCx.py`: UI 说明文字更新
  - `mdcx/views/MDCx.ui`: 界面元素补充
  - `docs/CONFIGURATION.md`: 新增配置章节

## ADDED Requirements

### Requirement: VSMETA 配置界面提示完善
系统 SHALL 为 VSMETA 配置界面的每个选项提供详细的中文提示信息，包括功能说明、可用选项和推荐设置。

#### Scenario: 查看配置项说明
- **WHEN** 用户将鼠标悬停在 VSMETA 配置项上
- **THEN** 显示该配置项的详细功能说明和使用建议

#### Scenario: 选择配置选项
- **WHEN** 用户打开配置下拉框查看选项
- **THEN** 每个选项显示中文名称和简要说明

### Requirement: VSMETA 配置文档补充
系统 SHALL 在配置文档中添加完整的 VSMETA 配置章节，包含所有配置项的详细说明。

#### Scenario: 查阅配置文档
- **WHEN** 用户打开 docs/CONFIGURATION.md
- **THEN** 可以找到 VSMETA 配置的专门章节，包含所有配置项的完整说明

#### Scenario: 理解配置效果
- **WHEN** 用户阅读配置说明后进行设置
- **THEN** 生成的 VSMETA 文件内容与文档描述一致

### Requirement: 自定义模板使用指南
系统 SHALL 提供自定义模板的完整使用指南，包括语法说明、占位符列表和使用示例。

#### Scenario: 学习自定义模板
- **WHEN** 用户想使用自定义模板功能
- **THEN** 可以找到详细的语法说明和丰富的使用示例

#### Scenario: 使用占位符
- **WHEN** 用户在模板中使用占位符
- **THEN** 可以查看所有可用占位符的中文说明及其含义

## MODIFIED Requirements

### Requirement: 配置项标签文字优化
现有要求：配置项应有清晰的标签
- **MODIFIED TO**: 配置项应有清晰的中文标签和详细的功能说明

## REMOVED Requirements

### Requirement: N/A
无删除需求

## Acceptance Criteria

### AC-1: UI 配置提示完善
- **Given**: 用户在 VSMETA 设置界面
- **When**: 鼠标悬停在任意配置项上
- **Then**: 显示该项的中文功能说明和可选值列表
- **Verification**: `human-judgment`

### AC-2: 配置文档完整
- **Given**: 用户打开配置文档
- **When**: 查看 VSMETA 配置章节
- **Then**: 包含所有配置项的详细说明、使用示例和最佳实践
- **Verification**: `human-judgment`

### AC-3: 自定义模板文档完善
- **Given**: 用户想使用自定义模板功能
- **When**: 查看相关文档
- **Then**: 提供完整的语法说明、所有占位符含义和实际使用示例
- **Verification**: `human-judgment`

### AC-4: 配置效果示例
- **Given**: 用户配置了特定的 VSMETA 选项
- **When**: 查看文档中的示例
- **Then**: 示例清晰展示该配置将产生的 VSMETA 文件内容效果
- **Verification**: `human-judgment`

### AC-5: 术语一致性
- **Given**: 用户查看任意 VSMETA 相关内容
- **When**: 涉及配置项名称
- **Then**: UI、代码、文档中的术语保持一致
- **Verification**: `programmatic`

## Open Questions
- [ ] 是否需要添加配置预设模板？如"最佳兼容性"、"最高信息量"等
- [ ] 是否需要添加配置冲突检测？如同时选择多个可能冲突的选项时给出警告
- [ ] 是否需要添加配置导出/导入功能？
