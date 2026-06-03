# 版本更新记录

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
