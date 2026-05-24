## 220260532 (2026-05-24)

### 新增
- VSMETA 设置标签页：嵌入封面图/背景图开关、锁定元数据、图片尺寸/质量、数量限制
- VSMETA 保留旧文件勾选框（设置→下载→保留旧文件）
- VSMetaEncoder: 新增 `reset()` 方法支持实例复用
- VSMetaEncoder: 写方法增加 `label` 参数，自动追踪已写入标签

### 优化
- `parse_release_date`: 支持非零填充日期 (2020-5-1, 2020/05/15)
- `parse_score`: 支持中文后缀 (8.5分, ⭐8.5, 评分 8.5)
- `parse_runtime`: 支持中文小时/分钟 (1小时30分钟, 1时30分)
- `write_vsmeta`: 改为 tmp + rename 原子写入，防止写入失败丢失旧文件
- 提取 `get_vsmeta_path()` 消除 scraper.py 中路径构建重复
- `delete_file_async` 内联导入移至模块顶层

### 修复
- 修复 `should_update_vsmeta` 中 `KeepableFile.VSMETA` 通过 UI 无法设置的死代码问题

## 220260531 (2026-05-24)

### 修复
- 修复命名页面 groupBox_vsmeta 与 groupBox_65 布局重叠 131px 的问题
- 同步 MDCx.py 中 10 个组件的 setGeometry 坐标与 MDCx.ui 一致
- 调整命名页面滚动区域高度 3660→3930，确保所有内容可见

## 220260530 (2026-05-24)

### 修复
- 修复命名标签页（tab_3）的布局重叠问题
- 调整 VSMETA 命名规则位置，不再与其他组件重叠
- 更新滚动区域高度，确保所有内容可见

### 改进
- 添加核心模块 API 文档
- 添加架构设计文档
- 更新项目 README，包含完整的特性列表和文档链接
- 添加测试辅助工具和核心模块测试

### 新增
- 添加 CI/CD 工作流配置
- 添加完整的 API 文档
- 添加架构设计文档
- 添加核心模块单元测试
- 添加测试覆盖率报告

## 220260527 (2026-05-23)

### 修复
- 修复 save_config.py 第 375 行 IndentationError 错误
- 确保代码缩进正确，符合 Python 语法规范

## 220260526 (2026-05-23)

### 修复
- 重新编译 UI 文件，修复 AttributeError: 'Ui_MDCx' object has no attribute 'checkBox_download_vsmeta' 错误
- 确保所有 VSMETA 相关 UI 控件正确绑定

## 220260525 (2026-05-22)

### 新增
- 修复 PyInstaller 打包配置，确保所有模块正确包含在安装包中

### 修复
- 修复安装包运行时 ModuleNotFoundError 错误
