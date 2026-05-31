# VSMETA UI 配置详细说明 - 任务列表

## [x] Task 1: 分析现有 VSMETA UI 控件状态
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 检查 mdcx/views/MDCx.py 和 MDCx.ui 中所有 VSMETA 相关控件
  - 列出已有 tooltip 的控件和缺失的控件
  - 确定需要添加 tooltip 的完整控件列表
- **Acceptance Criteria Addressed**: [AC-1, AC-2, AC-3, AC-4]
- **Test Requirements**:
  - `programmatic` TR-1.1: 生成完整的 VSMETA UI 控件清单
  - `human-judgment` TR-1.2: 确认清单包含所有相关控件
- **Notes**: 这是基础工作，已完成

## [x] Task 2: 为标题配置控件添加 tooltip
- **Priority**: P0
- **Depends On**: [Task 1]
- **Description**: 
  - 为 comboBox_vsmeta_show_title 添加详细 tooltip
  - 为 lineEdit_vsmeta_custom_title 添加详细 tooltip
  - tooltip 内容包括功能说明、可选值含义和使用建议
- **Acceptance Criteria Addressed**: [AC-1, AC-6]
- **Test Requirements**:
  - `human-judgment` TR-2.1: 验证 tooltip 文字清晰准确
  - `human-judgment` TR-2.2: 验证与文档术语一致
- **Notes**: tooltip 应详细说明每个可选值的效果

## [x] Task 3: 为副标题配置控件添加 tooltip
- **Priority**: P0
- **Depends On**: [Task 1]
- **Description**: 
  - 为 comboBox_vsmeta_show_title2 添加详细 tooltip
  - 为 lineEdit_vsmeta_custom_title2 添加详细 tooltip
  - tooltip 内容包括功能说明、可选值含义和使用建议
- **Acceptance Criteria Addressed**: [AC-2, AC-6]
- **Test Requirements**:
  - `human-judgment` TR-3.1: 验证 tooltip 文字清晰准确
  - `human-judgment` TR-3.2: 验证与文档术语一致
- **Notes**: 参考现有文档中的副标题配置说明

## [x] Task 4: 为简介配置控件添加 tooltip
- **Priority**: P0
- **Depends On**: [Task 1]
- **Description**: 
  - 为 comboBox_vsmeta_summary 添加详细 tooltip
  - 为 plainTextEdit_vsmeta_custom_summary 添加详细 tooltip
  - tooltip 内容包括功能说明、可选值含义和使用建议
- **Acceptance Criteria Addressed**: [AC-3, AC-6]
- **Test Requirements**:
  - `human-judgment` TR-4.1: 验证 tooltip 文字清晰准确
  - `human-judgment` TR-4.2: 验证与文档术语一致
- **Notes**: 简介配置的可选值较多，需要清晰说明

## [x] Task 5: 完善其他 VSMETA 配置控件的 tooltip
- **Priority**: P0
- **Depends On**: [Task 1]
- **Description**: 
  - 检查并完善 checkBox_vsmeta_include_poster 的 tooltip
  - 检查并完善 checkBox_vsmeta_include_backdrop 的 tooltip
  - 检查并完善 checkBox_vsmeta_locked 的 tooltip
  - 检查并完善 spinBox_vsmeta_image_dimension 的 tooltip
  - 检查并完善 spinBox_vsmeta_jpeg_quality 的 tooltip
  - 检查并完善 spinBox_vsmeta_actor_limit 的 tooltip
  - 检查并完善 spinBox_vsmeta_tag_limit 的 tooltip
  - 为 label_vsmeta_template_help 添加模板语法参考提示
- **Acceptance Criteria Addressed**: [AC-4, AC-5, AC-6]
- **Test Requirements**:
  - `human-judgment` TR-5.1: 验证所有 tooltip 完整准确
  - `human-judgment` TR-5.2: 验证模板语法提示清晰可用
- **Notes**: 部分控件可能已有基础 tooltip，需要补充完善

## [x] Task 6: 验证并测试所有 tooltip
- **Priority**: P1
- **Depends On**: [Task 2, Task 3, Task 4, Task 5]
- **Description**: 
  - 运行应用程序测试所有 tooltip 的显示
  - 验证 tooltip 内容的准确性和完整性
  - 检查术语与配置文档的一致性
  - 收集用户体验反馈
- **Acceptance Criteria Addressed**: [AC-1, AC-2, AC-3, AC-4, AC-5, AC-6]
- **Test Requirements**:
  - `programmatic` TR-6.1: 应用程序能正常启动
  - `human-judgment` TR-6.2: 所有 tooltip 正常显示且内容准确
- **Notes**: 这是最终的验证和测试步骤

## 任务依赖关系

```
Task 1 (分析 UI 控件)
    ↓
Task 2 (标题配置 tooltip)
    ↓
Task 3 (副标题配置 tooltip)
    ↓
Task 4 (简介配置 tooltip)
    ↓
Task 5 (其他配置项 tooltip)
    ↓
Task 6 (验证测试)
```

## 优先级说明

- **P0**: 必须完成，直接影响用户体验
- **P1**: 重要但不紧急，确保质量和一致性
