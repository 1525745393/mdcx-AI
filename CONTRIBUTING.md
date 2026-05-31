# MDCx 贡献指南

> 📖 **更多文档**: [文档中心](docs/README.md) | [主 README](README.md) | [开发指南](DEVELOPMENT.md) | [架构设计](docs/architecture.md)

欢迎您参与 MDCx 项目的开发！本指南将帮助您了解如何贡献代码、报告问题和提出改进建议。

## 目录

1. [行为准则](#行为准则)
2. [如何贡献](#如何贡献)
3. [开发环境配置](#开发环境配置)
4. [代码规范](#代码规范)
5. [提交规范](#提交规范)
6. [PR 流程](#pr-流程)
7. [问题反馈](#问题反馈)

## 行为准则

### 我们的承诺

为了营造开放和友好的社区环境，我们承诺：

- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像
- 恶意评论或人身攻击
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不专业或不恰当的行为

## 如何贡献

### 报告 Bug

1. 首先在 [Issues](https://github.com/1525745393/mdcx-AI/issues) 中搜索是否已有相关问题
2. 如果没有找到，创建新的 Issue，使用提供的模板
3. 提供详细的信息：
   - 问题描述
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（操作系统、Python 版本、MDCx 版本）
   - 日志文件（敏感信息请脱敏）
   - 截图（如适用）

### 提出新功能

1. 在 Issues 中搜索是否已有相关建议
2. 创建新的 Issue，描述您的想法
3. 说明功能的使用场景和预期效果
4. 如果可能，提供实现思路

### 贡献代码

#### 准备工作

1. 阅读本文档和 [DEVELOPMENT.md](DEVELOPMENT.md)
2. 确保您的开发环境已配置好
3. 了解项目的代码结构

#### 选择任务

- 修复已知的 Bug（查看 Issues 中的 `bug` 标签）
- 实现新功能（查看 Issues 中的 `enhancement` 标签）
- 改进文档
- 编写测试
- 优化性能

#### 开发流程

1. Fork 本仓库
2. 克隆您的 Fork 到本地
3. 创建功能分支
4. 进行开发
5. 运行测试确保一切正常
6. 提交代码
7. 推送到您的 Fork
8. 创建 Pull Request

## 开发环境配置

详细的开发环境配置请参考 [DEVELOPMENT.md](DEVELOPMENT.md)。

快速开始：

```bash
# 克隆仓库
git clone https://github.com/您的用户名/mdcx-AI.git
cd mdcx-AI

# 安装依赖
uv sync --all-extras --dev

# 安装 pre-commit hooks
uv run pre-commit install

# 运行测试
uv run pytest
```

## 代码规范

### Python 代码

- 遵循 [PEP 8](https://peps.python.org/pep-0008/) 风格指南
- 使用类型注解（Type Hints）
- 代码使用 `ruff` 进行格式化和检查

```bash
# 代码检查
uv run ruff check .

# 自动修复
uv run ruff check . --fix
```

### 代码组织

- 新功能应该放在合适的模块中
- 保持函数和类的单一职责
- 添加必要的文档字符串（Docstrings）

### Git 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：

- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

示例：

```
feat(crawler): add support for new website XYZ

- 实现 XYZ 网站的爬虫
- 添加相应的测试用例
- 更新文档

Closes #123
```

## 提交规范

### 提交前检查清单

- [ ] 代码已通过 `ruff` 检查
- [ ] 所有测试通过
- [ ] 已添加必要的测试用例
- [ ] 文档已更新（如需要）
- [ ] 提交信息符合规范

### 代码审查

所有 PR 都需要至少一位维护者审查通过才能合并。审查要点：

- 代码质量和可读性
- 是否符合项目架构
- 是否有足够的测试覆盖
- 是否有安全隐患
- 性能影响（如适用）

## PR 流程

### 创建 PR

1. 确保您的分支与 `main` 分支同步
2. 提交您的更改
3. 推送到您的 Fork
4. 在 GitHub 上创建 Pull Request
5. 填写 PR 模板
6. 等待审查

### PR 模板

```markdown
## 变更类型

- [ ] Bug 修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 性能优化
- [ ] 其他

## 描述

简要描述这次变更的内容。

## 相关 Issue

Closes #xxx

## 变更内容

- 变更 1
- 变更 2

## 测试

- [ ] 已添加新的测试用例
- [ ] 所有现有测试通过

## 截图（如适用）

##  Checklist

- [ ] 代码已通过 lint 检查
- [ ] 文档已更新
- [ ] 提交信息符合规范
```

## 问题反馈

### 社区交流

- 加入 [Telegram 群](https://t.me/mdcx_chat) 与其他用户交流
- 在 Discussions 中提出问题和建议

### 安全问题

如果发现安全漏洞，请不要公开报告，而是通过私人方式联系维护者。

---

感谢您对 MDCx 项目的贡献！

