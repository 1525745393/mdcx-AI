# v220260565 版本发布 - The Implementation Plan (Decomposed and Prioritized Task List)

## [/] Task 1: 更新版本号
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 更新 consts.py 文件中的 LOCAL_VERSION 从 220260564 到 220260565
  - 可以使用 `uv run python -m scripts.bump` 脚本或手动编辑
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-1.1: 检查 consts.py 文件中的 LOCAL_VERSION 确实是 220260565
  - `programmatic` TR-1.2: 运行 `grep LOCAL_VERSION mdcx/consts.py` 验证
- **Notes**: 使用 bump 脚本更安全，避免手动编辑出错

## [ ] Task 2: 更新 Changelog 文档
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 在 changelog.md 文件顶部添加 220260565 版本的变更条目
  - 包含以下内容：
    - VSMETA UI 配置 tooltip 完善：为所有 VSMETA 控件添加详细的说明提示
    - VSMETA 配置说明完善：完整的 UI 配置说明文档
    - VSMETA 自定义模板语法完整指南：包括占位符、条件语法、默认值和示例
- **Acceptance Criteria Addressed**: [AC-2]
- **Test Requirements**:
  - `programmatic` TR-2.1: 检查 changelog.md 文件首行为 "## 220260565"
  - `human-judgment` TR-2.2: 确认变更内容描述准确完整

## [ ] Task 3: 创建 Release Commit
- **Priority**: P0
- **Depends On**: [Task 1, Task 2]
- **Description**: 
  - 将版本更新和 changelog 更新提交
  - 提交信息应为 "release: v220260565 版本发布"
- **Acceptance Criteria Addressed**: [AC-1, AC-2]
- **Test Requirements**:
  - `programmatic` TR-3.1: 检查 git log 最新提交信息
  - `programmatic` TR-3.2: 确认工作树干净无未提交修改

## [ ] Task 4: 创建 Git 标签
- **Priority**: P0
- **Depends On**: [Task 3]
- **Description**: 
  - 创建轻量级标签或附注标签：220260565 和 v220260565
  - 建议使用附注标签：`git tag -a v220260565 -m "Release v220260565"`
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `programmatic` TR-4.1: 运行 `git tag` 确认标签存在
  - `programmatic` TR-4.2: 运行 `git rev-parse v220260565` 验证标签指向正确的提交

## [ ] Task 5: 推送到远程仓库
- **Priority**: P0
- **Depends On**: [Task 4]
- **Description**: 
  - 推送代码：`git push`
  - 推送标签：`git push origin 220260565 v220260565` 或 `git push --tags`
- **Acceptance Criteria Addressed**: [AC-4]
- **Test Requirements**:
  - `programmatic` TR-5.1: 运行 `git ls-remote --tags origin` 确认远程标签存在
  - `human-judgment` TR-5.2: 确认 GitHub 仓库中可以看到新标签

## [ ] Task 6: 监控 GitHub Actions 构建
- **Priority**: P0
- **Depends On**: [Task 5]
- **Description**: 
  - 访问 GitHub 仓库的 Actions 页面
  - 确认新的构建任务已启动
  - 等待构建完成，检查是否有错误
- **Acceptance Criteria Addressed**: [AC-5]
- **Test Requirements**:
  - `human-judgment` TR-6.1: 确认 GitHub Actions 中有新的构建任务
  - `human-judgment` TR-6.2: 监控构建状态直至成功完成
  - `human-judgment` TR-6.3: 确认 GitHub Releases 中有新的发布

## 任务依赖关系

```
Task 1 (版本号更新)
  ↓
Task 2 (Changelog 更新)
  ↓
Task 3 (Release Commit)
  ↓
Task 4 (Git 标签创建)
  ↓
Task 5 (推送到远程)
  ↓
Task 6 (监控构建)
```

## 优先级说明

- **P0**: 必须完成，直接影响发布过程
