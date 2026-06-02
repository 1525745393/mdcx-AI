# MDCx Changelog

## v220260566 (2026-06-02)

### 新增
* 新增多个工具函数的单元测试（测试覆盖显著提升）
* 新增测试文件：`test_language_utils.py` - 语言检测功能测试
* 新增测试文件：`test_leb128.py` - LEB128编码工具测试
* 新增测试文件：`test_path_utils.py` - 路径工具函数测试
* 新增测试文件：`test_vsmeta_template_helper.py` - VSMETA模板辅助功能测试
* 完善 `vsmeta_template_helper.py` 模块，新增 `get_all_presets()`、`get_preset_by_name()`、`extract_placeholders()`、`render_template()` 函数
* 建立系统化的代码审查机制（CODE_REVIEW_STANDARDS.md、CODE_REVIEW_CHECKLIST.md等文档）
* 完善项目 Code Wiki 文档

### 修复
* 修复 `update_existing` 和 `update_existing_valid` 函数会意外修改原始字典的问题
* 修复 `test_file_utils.py` 中的 PyQt6 依赖问题，使用 mock 避免导入错误
* 修复代码审查中发现的 lint 问题（未使用的导入、裸异常捕获等）
* 修复多个测试文件末尾缺少换行符的问题
* 完善 `base/number.py` 中的文档字符串和类型注解
* 修复 `validate_template()` 函数以正确检测嵌套大括号错误

### 改进
* 显著提升测试覆盖度（新增 65 个测试用例）
* 完善代码质量检查流程
* 建立 GitHub Actions CI/CD 自动化检查
* 配置 ESLint 和 Prettier 用于代码风格统一
* 添加 JSDoc 注释到 JavaScript 文件
* 代码质量整体改进

<details>
<summary>Full Changelog</summary>

03f79e5 fix: 修复 lint 检查发现的问题
a7c4eba fix: 代码审查问题修复
247a3ec feat: 生成项目Code Wiki文档
97f9256 feat: 生成项目Code Wiki文档
32a206e feat: 生成项目Code Wiki文档
e3f4f92 feat: 生成项目Code Wiki文档
7d55110 feat: 生成项目Code Wiki文档
1acdceb feat: 生成项目Code Wiki文档
6709262 feat: 生成项目Code Wiki文档
dfb1221 feat: 生成项目Code Wiki文档
ce8453f feat: 生成项目Code Wiki文档
32c3b8e feat: 生成项目Code Wiki文档
c58b550 feat: 生成项目Code Wiki文档

</details>

## v220260565 (Previous Release)
* Initial release of the current branch
