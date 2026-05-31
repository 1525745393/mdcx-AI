# 发布前检查清单

## 代码完整性检查
- [ ] git status 显示工作树干净
- [ ] git log 显示所有必要的提交
- [ ] 版本号已更新到正确版本

## 功能完整性检查

### VSMETA 自定义模板功能
- [ ] VsmetaShowTitle 枚举包含 CUSTOM 选项（7个选项）
- [ ] VsmetaShowTitle2 枚举包含 CUSTOM 选项（5个选项）
- [ ] VsmetaSummary 枚举包含 CUSTOM 选项（8个选项）
- [ ] Config 模型包含 vsmeta_custom_title 字段
- [ ] Config 模型包含 vsmeta_custom_title2 字段
- [ ] Config 模型包含 vsmeta_custom_summary 字段
- [ ] vsmeta.py 实现了 render_template 函数
- [ ] vsmeta.py 标题生成逻辑支持 CUSTOM 模式
- [ ] vsmeta.py 副标题生成逻辑支持 CUSTOM 模式
- [ ] vsmeta.py 简介生成逻辑支持 CUSTOM 模式
- [ ] MDCx.py 包含 comboBox_vsmeta_show_title 控件
- [ ] MDCx.py 包含 comboBox_vsmeta_show_title2 控件
- [ ] MDCx.py 包含 comboBox_vsmeta_summary 控件
- [ ] MDCx.py 包含 lineEdit_vsmeta_custom_title 控件
- [ ] MDCx.py 包含 lineEdit_vsmeta_custom_title2 控件
- [ ] MDCx.py 包含 plainTextEdit_vsmeta_custom_summary 控件
- [ ] load_config.py 加载自定义模板配置
- [ ] save_config.py 保存自定义模板配置

### 性能监控功能
- [ ] MDCx.py 包含 pushButton_performance_monitor 控件
- [ ] init.py 包含性能监控信号连接

## 代码质量检查
- [ ] Python 语法检查通过
- [ ] 没有遗留的调试代码或 print 语句
- [ ] 代码风格符合项目规范

## 配置检查
- [ ] default_config.json 包含 vsmeta_keep_ext 字段
- [ ] default_config.json 包含 vsmeta_include_poster 字段
- [ ] default_config.json 包含 vsmeta_include_backdrop 字段
- [ ] default_config.json 包含 vsmeta_locked 字段
- [ ] default_config.json 包含 vsmeta_image_max_dimension 字段
- [ ] default_config.json 包含 vsmeta_jpeg_quality 字段
- [ ] default_config.json 包含 vsmeta_actor_limit 字段
- [ ] default_config.json 包含 vsmeta_tag_limit 字段
- [ ] default_config.json 包含 vsmeta_show_title 字段
- [ ] default_config.json 包含 vsmeta_show_title2 字段
- [ ] default_config.json 包含 vsmeta_summary 字段
- [ ] default_config.json 包含 vsmeta_custom_title 字段（默认值正确）
- [ ] default_config.json 包含 vsmeta_custom_title2 字段（默认值正确）
- [ ] default_config.json 包含 vsmeta_custom_summary 字段（默认值正确）

## UI 检查
- [ ] MDCx.py 中 VSMETA 设置界面完整
- [ ] 所有 UI 元素都有正确的 objectName
- [ ] 翻译文本完整
- [ ] 布局正确，不需要滚动条即可查看所有内容

## 发布检查
- [ ] changelog.md 已更新，包含新功能说明
- [ ] git 标签已创建
- [ ] git 标签已推送到远程仓库
- [ ] GitHub Actions 已触发构建

## GitHub Actions 检查
- [ ] release.yml 工作流配置正确
- [ ] build.py 脚本完整
- [ ] 构建脚本包含必要的隐藏导入
