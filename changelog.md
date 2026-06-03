# 版本更新记录

## V220260605 - VSMeta 预设导入/导出功能

### 新增

- **VSMeta 预设导入功能**
  - 新增"导入配置"按钮，支持从JSON文件导入VSMETA配置
  - 自动检测已存在的预设，避免重复导入
  - 提供详细的导入反馈信息（成功导入数量、跳过数量）
  - 导入后自动刷新预设列表

- **UI 增强**
  - 在VSMETA配置页面添加"导入配置"按钮
  - 按钮布局：重置(30, 1150) → 导出(140, 1150) → 导入(250, 1150)
  - 完整的按钮文本和翻译

### 改进

- 优化预设导出功能的JSON格式，包含完整的配置和所有自定义预设
- 完整的错误处理和用户友好的界面反馈
- 导入功能与现有导出功能完美配合

## V220260604 - VSMeta 占位符自动补全功能

### 新增

- **VSMeta 占位符自动补全功能**
  - 在标题、副标题、简介模板输入框中输入 `{` 时自动触发补全
  - 补全列表显示占位符名称和描述（例如：`number - 视频番号`）
  - 支持模糊匹配，输入字母即可筛选
  - 选择后自动替换为完整的 `{placeholder}` 格式

### 修复

- 简化了PlainTextEdit的自动补全逻辑，移除了不必要的事件过滤器
- 修复了自动补全功能的绑定问题

### 改进

- 自动补全功能现在覆盖所有三个VSMeta模板输入框（标题、副标题、简介）
- 更稳定可靠的补全触发机制

## V220260603 - 修复VSMeta方法绑定问题

### 修复

- 修复运行时 AttributeError：`MyMAinWindow` 对象缺少 `_load_vsmeta_custom_presets` 等VSMeta相关方法
- 在 [main_window.py](file:///workspace/mdcx/controllers/main_window/main_window.py#L3417-L3435) 文件末尾补全了9个VSMeta方法的外部绑定：
  - `_load_vsmeta_custom_presets`
  - `_update_vsmeta_preview`
  - `_save_vsmeta_preset`
  - `_delete_vsmeta_preset`
  - `_on_vsmeta_title_preset_changed`
  - `_on_vsmeta_title2_preset_changed`
  - `_on_vsmeta_summary_preset_changed`
  - `_reset_vsmeta_config`
  - `_export_vsmeta_config`

---

## VSMeta 界面配置优化

### 新增功能

- **模板预览功能**
  - 实时预览标题、副标题、简介模板渲染效果
  - 使用示例数据展示渲染结果
  - 语法错误时显示红色背景提示

- **自定义预设管理**
  - 支持保存当前配置为自定义预设
  - 支持删除自定义预设
  - 预设存储在配置文件中，重启后保留

- **模板语法验证**
  - 实时检查 `{if:}` 和 `{/if}` 标签配对
  - 错误时显示具体错误信息

- **批量操作**
  - 重置为默认配置按钮
  - 导出配置为 JSON 文件

- **帮助文档增强**
  - 添加默认值语法示例
  - 更详细的模板语法说明

### 修复

- 修复 UI 初始化失败的问题：添加缺失的预览标签组件创建代码
- 修复控制器初始化失败的问题：恢复缺失的 VSMeta 实现方法
