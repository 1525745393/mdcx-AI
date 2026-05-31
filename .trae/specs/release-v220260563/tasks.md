# v220260563 版本发布 - The Implementation Plan (Decomposed and Prioritized Task List)

## [x] Task 1: 更新版本号
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 更新 mdcx/consts.py 文件中的 LOCAL_VERSION 从 220260562 到 220260563
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-1.1: 验证 LOCAL_VERSION 常量已更新为 220260563
- **Notes**: 这是发布的第一步，所有后续任务都依赖此

## [x] Task 2: 更新 Changelog 文档
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 在 changelog.md 文件顶部添加新的版本条目
  - 包含发布日期 (2026-05-31)
  - 列出本次发布的变更内容
- **Acceptance Criteria Addressed**: [AC-2]
- **Test Requirements**:
  - `programmatic` TR-2.1: 验证 changelog.md 第一个标题是 "## 220260563 (2026-05-31)"
  - `human-judgement` TR-2.2: 验证 changelog 条目内容合理清晰
- **Notes**: 添加"维护更新"条目，说明此版本的更新内容

## [x] Task 3: 提交变更
- **Priority**: P0
- **Depends On**: Task 1, Task 2
- **Description**: 
  - 将版本号和 changelog 更新提交到 git
  - 使用合适的 commit message
- **Acceptance Criteria Addressed**: [AC-1, AC-2]
- **Test Requirements**:
  - `programmatic` TR-3.1: 验证 git status 显示 "nothing to commit, working tree clean"
  - `programmatic` TR-3.2: 验证最新提交是本次发布相关的
- **Notes**: commit message 格式为 "release: v220260563 版本更新"

## [x] Task 4: 创建 Git 标签
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 创建标签 220260563
  - 创建标签 v220260563
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `programmatic` TR-4.1: 验证 git tag 列表包含 "220260563"
  - `programmatic` TR-4.2: 验证 git tag 列表包含 "v220260563"
- **Notes**: 两个标签都需要创建，保持与之前版本的一致性

## [x] Task 5: 推送标签到远程仓库
- **Priority**: P0
- **Depends On**: Task 4
- **Description**: 
  - 将新标签推送到 origin
  - 将当前分支也推送到 origin
- **Acceptance Criteria Addressed**: [AC-4]
- **Test Requirements**:
  - `programmatic` TR-5.1: 验证 git push 命令成功执行
  - `programmatic` TR-5.2: 验证 git ls-remote 显示远程有新标签
- **Notes**: 使用 --tags 参数推送所有标签

## [x] Task 6: 验证 GitHub Actions 触发
- **Priority**: P1
- **Depends On**: Task 5
- **Description**: 
  - 检查 GitHub Actions 是否已自动触发
  - 确认构建正在进行或已完成
- **Acceptance Criteria Addressed**: [AC-5]
- **Test Requirements**:
  - `human-judgement` TR-6.1: 验证 Actions 页面显示新的构建
- **Notes**: 如果有 gh CLI 可用，可以使用它检查

## 任务依赖关系
- Task 2 依赖于 Task 1
- Task 3 依赖于 Task 1 和 Task 2
- Task 4 依赖于 Task 3
- Task 5 依赖于 Task 4
- Task 6 依赖于 Task 5
