# VSMETA 配置详细说明 - 验证检查清单

## 分析和规划检查

- [ ] 已分析所有 VSMETA 相关枚举定义
- [ ] 已生成完整的配置项清单
- [ ] 清单包含配置项名称、类型、可选值
- [ ] 已确认所有需要添加说明的配置项

## UI 说明完善检查

- [ ] 已检查 mdcx/views/MDCx.ui 文件
- [ ] VSMETA 标签配置项已添加 tooltip
- [ ] VSMETA 副标题配置项已添加 tooltip
- [ ] VSMETA 简介配置项已添加 tooltip
- [ ] VSMETA 自定义标题模板已添加 tooltip
- [ ] VSMETA 自定义副标题模板已添加 tooltip
- [ ] VSMETA 自定义简介模板已添加 tooltip
- [ ] 其他 VSMETA 配置项已添加 tooltip
- [ ] tooltip 包含中文功能说明
- [ ] tooltip 包含可选值说明
- [ ] MDCx.py 控件正确绑定
- [ ] UI 编译后 tooltip 正常显示

## 配置文档检查

- [ ] docs/CONFIGURATION.md 文件存在
- [ ] VSMETA 配置章节已创建
- [ ] 章节包含配置项总览表
- [ ] 每个配置项包含：
  - [ ] 功能说明
  - [ ] 可选值列表及含义
  - [ ] 使用场景说明
  - [ ] 注意事项
  - [ ] 配置示例

### 标签配置项检查

- [ ] show_title 配置说明完整
- [ ] show_title2 配置说明完整
- [ ] vsmeta_custom_title 配置说明完整
- [ ] vsmeta_custom_title2 配置说明完整

### 简介配置项检查

- [ ] summary 配置说明完整
- [ ] vsmeta_custom_summary 配置说明完整

### 图片配置项检查

- [ ] poster 配置说明完整
- [ ] thumb 配置说明完整
- [ ] backdrop 配置说明完整

### 其他配置项检查

- [ ] vsmeta_output_dir 配置说明完整
- [ ] vsmeta_update_mode 配置说明完整
- [ ] 其他相关配置说明完整

## 自定义模板指南检查

- [ ] 模板语法说明已添加
- [ ] 基本占位符列表完整：
  - [ ] number (番号)
  - [ ] title (中文标题)
  - [ ] originaltitle (日文原始标题)
  - [ ] publisher (制作商)
  - [ ] studio (工作室)
  - [ ] series (系列名称)
  - [ ] actors (演员列表)
  - [ ] outline (中文简介)
  - [ ] originalplot (日文简介)
  - [ ] year (年份)
  - [ ] release (发布日期)
  - [ ] score (评分)
  - [ ] country (国家)
  - [ ] director (导演)
  - [ ] genre (类型)
  - [ ] mosaic (马赛克类型)
  - [ ] runtime (时长)
  - [ ] label (标签)
  - [ ] website (官网)
- [ ] 每个占位符包含中文说明
- [ ] 增强语法说明已添加：
  - [ ] 条件渲染 {if:field}...{/if}
  - [ ] 默认值 {field|default}
- [ ] 使用示例完整：
  - [ ] 简单模板示例
  - [ ] 复杂模板示例
  - [ ] 条件渲染示例
  - [ ] 默认值使用示例
- [ ] 常见问题解答已添加
- [ ] 最佳实践建议已添加

## 术语一致性检查

- [ ] UI 中的配置项名称与文档一致
- [ ] 代码中的枚举值与文档描述一致
- [ ] 所有术语使用统一的中文翻译
- [ ] 没有英文术语混杂（除非是通用的技术术语）

## 用户体验检查

- [ ] tooltip 文字简洁明了
- [ ] tooltip 不会遮挡重要信息
- [ ] 文档结构清晰易读
- [ ] 文档链接导航正常
- [ ] 配置示例可直接复制使用

## 测试验证检查

- [ ] 应用启动正常
- [ ] VSMETA 配置界面正常显示
- [ ] 鼠标悬停显示 tooltip
- [ ] tooltip 内容正确
- [ ] 配置保存和加载正常
- [ ] 生成的 VSMETA 文件符合预期

## 质量保证检查

- [ ] 文档无错别字
- [ ] 文档格式统一
- [ ] 代码注释清晰
- [ ] 没有遗留的调试信息
- [ ] 文档和代码同步更新
