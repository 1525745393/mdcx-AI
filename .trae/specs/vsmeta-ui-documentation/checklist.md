# VSMETA UI 配置详细说明 - 验证检查清单

## 分析规划检查

- [x] 已完整分析现有 VSMETA UI 控件状态
- [x] 已生成 VSMETA 相关 UI 控件完整清单
- [x] 已确定需要添加/完善 tooltip 的控件列表

## 标题配置 tooltip 检查

- [x] comboBox_vsmeta_show_title 已添加详细 tooltip
- [x] tooltip 包含标题配置的功能说明
- [x] tooltip 包含所有可选值的含义解释
- [x] tooltip 提供使用建议和示例
- [x] lineEdit_vsmeta_custom_title 已添加详细 tooltip
- [x] tooltip 包含自定义模板的使用说明
- [x] 术语与配置文档保持一致

## 副标题配置 tooltip 检查

- [x] comboBox_vsmeta_show_title2 已添加详细 tooltip
- [x] tooltip 包含副标题配置的功能说明
- [x] tooltip 包含所有可选值的含义解释
- [x] tooltip 提供使用建议和示例
- [x] lineEdit_vsmeta_custom_title2 已添加详细 tooltip
- [x] tooltip 包含自定义模板的使用说明
- [x] 术语与配置文档保持一致

## 简介配置 tooltip 检查

- [x] comboBox_vsmeta_summary 已添加详细 tooltip
- [x] tooltip 包含简介配置的功能说明
- [x] tooltip 包含所有可选值的含义解释
- [x] tooltip 提供使用建议和示例
- [x] plainTextEdit_vsmeta_custom_summary 已添加详细 tooltip
- [x] tooltip 包含自定义模板的使用说明
- [x] 术语与配置文档保持一致

## 其他配置项 tooltip 检查

- [x] checkBox_vsmeta_include_poster 的 tooltip 完整准确
- [x] checkBox_vsmeta_include_backdrop 的 tooltip 完整准确
- [x] checkBox_vsmeta_locked 的 tooltip 完整准确
- [x] spinBox_vsmeta_image_dimension 的 tooltip 完整准确
- [x] spinBox_vsmeta_jpeg_quality 的 tooltip 完整准确
- [x] spinBox_vsmeta_actor_limit 的 tooltip 完整准确
- [x] spinBox_vsmeta_tag_limit 的 tooltip 完整准确
- [x] label_vsmeta_template_help 包含清晰的模板语法参考
- [x] 所有 tooltip 与配置文档术语一致

## 模板语法提示检查

- [x] 模板语法说明清晰易懂
- [x] 包含常用占位符列表：
  - [x] {number} - 番号
  - [x] {title} - 中文标题
  - [x] {originaltitle} - 日文原始标题
  - [x] {publisher} - 制作商
  - [x] {studio} - 工作室
  - [x] {series} - 系列名称
  - [x] {actors} - 演员列表
  - [x] {outline} - 中文简介
  - [x] {originalplot} - 日文简介
  - [x] {year} - 年份
  - [x] {release} - 发布日期
  - [x] {score} - 评分
  - [x] {country} - 国家
  - [x] {director} - 导演
  - [x] {genre} - 类型
  - [x] {mosaic} - 马赛克类型
  - [x] {runtime} - 时长
  - [x] {label} - 标签
  - [x] {website} - 官网
- [x] 包含条件渲染语法说明 {if:field}...{/if}
- [x] 包含默认值语法说明 {field|default}
- [x] 提供简单实用的模板示例

## 测试验证检查

- [x] 应用程序能正常启动（代码完整性验证）
- [x] VSMETA 配置界面正常显示
- [x] 所有 tooltip 能正常显示
- [x] tooltip 内容准确无误
- [x] tooltip 文字清晰易读
- [x] 没有语法错误或错别字
- [x] UI 布局正常，没有错位
- [x] 配置保存和加载功能正常

## 质量保证检查

- [x] 所有 tooltip 文字简洁明了
- [x] 技术术语使用准确
- [x] 与配置文档术语保持一致
- [x] 没有错别字或语法错误
- [x] tooltip 长度适中，不会遮挡重要内容
- [x] 说明文字实用且有帮助性
- [x] 代码风格与现有代码一致
