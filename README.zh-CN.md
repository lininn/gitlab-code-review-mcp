# GitLab MCP 代码审查工具

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 本项目 fork 自 [cayirtepeomer/gerrit-code-review-mcp](https://github.com/cayirtepeomer/gerrit-code-review-mcp) 并为 GitLab 集成进行了适配。

一个用于将 Claude 等 AI 助手与 GitLab 的合并请求（Merge Request）集成的 MCP (Model Context Protocol) 服务器。这使得 AI 助手可以直接通过 GitLab API 审查代码变更。

## 功能

- **完整的合并请求分析**: 获取合并请求的全部详情，包括差异、提交和评论。
- **特定文件的差异**: 分析合并请求中特定文件的变更。
- **版本比较**: 比较不同的分支、标签或提交。
- **审查管理**: 添加评论、批准或取消批准合并请求。
- **项目概览**: 获取项目中的所有合并请求列表。

## 安装

### 环境要求

- Python 3.10+
- 具有 API 范围（`read_api`, `api`）的 GitLab 个人访问令牌
- [Cursor IDE](https://cursor.sh/) 或 [Claude 桌面应用](https://claude.ai/desktop) 用于 MCP 集成

### 快速开始

1.  克隆此仓库：

    ```bash
    git clone https://github.com/mehmetakinn/gitlab-mcp-code-review.git
    cd gitlab-mcp-code-review
    ```

2.  创建并激活虚拟环境：

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # 在 Windows 上使用: .venv\Scripts\activate
    ```

3.  安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

4.  创建一个 `.env` 文件并配置您的 GitLab 信息（可参考 `.env.example` 查看所有选项）：

    ```
    # 必填
    GITLAB_TOKEN=your_personal_access_token_here

    # 可选配置
    GITLAB_HOST=gitlab.com
    GITLAB_API_VERSION=v4
    LOG_LEVEL=INFO
    ```

## 配置选项

以下环境变量可以在您的 `.env` 文件中配置：

| 变量 | 是否必须 | 默认值 | 描述 |
|---|---|---|---|
| `GITLAB_TOKEN` | 是 | - | 您的 GitLab 个人访问令牌 |
| `GITLAB_HOST` | 否 | `gitlab.com` | GitLab 实例主机名 |
| `GITLAB_API_VERSION` | 否 | `v4` | 使用的 GitLab API 版本 |
| `LOG_LEVEL` | 否 | `INFO` | 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `DEBUG` | 否 | `false` | 启用调试模式 |
| `REQUEST_TIMEOUT` | 否 | `30` | API 请求超时时间（秒） |
| `MAX_RETRIES` | 否 | `3` | 失败请求的最大重试次数 |

## Cursor IDE 集成

要将此 MCP 与 Cursor IDE 一起使用，请将以下配置添加到您的 `~/.cursor/mcp.json` 文件中：

```json
{
  "mcpServers": {
    "gitlab-mcp-code-review": {
      "command": "/path/to/your/gitlab-mcp-code-review/.venv/bin/python",
      "args": [
        "/path/to/your/gitlab-mcp-code-review/server.py",
        "--transport",
        "stdio"
      ],
      "cwd": "/path/to/your/gitlab-mcp-code-review",
      "env": {
        "PYTHONPATH": "/path/to/your/gitlab-mcp-code-review",
        "VIRTUAL_ENV": "/path/to/your/gitlab-mcp-code-review/.venv",
        "PATH": "/path/to/your/gitlab-mcp-code-review/.venv/bin:/usr/local/bin:/usr/bin:/bin"
      },
      "stdio": true
    }
  }
}
```

请将 `/path/to/your/gitlab-mcp-code-review` 替换为您克隆仓库的实际路径。

## Claude 桌面应用集成

要将此 MCP 与 Claude 桌面应用一起使用：

1.  打开 Claude 桌面应用
2.  进入 设置 → 高级 → MCP 配置
3.  添加以下配置：

```json
{
  "mcpServers": {
    "gitlab-mcp-code-review": {
      "command": "/path/to/your/gitlab-mcp-code-review/.venv/bin/python",
      "args": [
        "/path/to/your/gitlab-mcp-code-review/server.py",
        "--transport",
        "stdio"
      ],
      "cwd": "/path/to/your/gitlab-mcp-code-review",
      "env": {
        "PYTHONPATH": "/path/to/your/gitlab-mcp-code-review",
        "VIRTUAL_ENV": "/path/to/your/gitlab-mcp-code-review/.venv",
        "PATH": "/path/to/your/gitlab-mcp-code-review/.venv/bin:/usr/local/bin:/usr/bin:/bin"
      },
      "stdio": true
    }
  }
}
```

请将 `/path/to/your/gitlab-mcp-code-review` 替换为您克隆仓库的实际路径。

## 可用工具

该 MCP 服务器提供以下工具用于与 GitLab 交互：

| 工具 | 描述 |
|---|---|
| `fetch_merge_request` | 获取有关合并请求的完整信息 |
| `fetch_merge_request_diff` | 获取特定合并请求的差异 |
| `fetch_commit_diff` | 获取特定提交的差异信息 |
| `compare_versions` | 比较不同的分支、标签或提交 |
| `add_merge_request_comment` | 向合并请求添加评论 |
| `approve_merge_request` | 批准合并请求 |
| `unapprove_merge_request` | 取消批准合并请求 |
| `get_project_merge_requests` | 获取项目的合并请求列表 |

## 使用示例

### 获取合并请求

```python
# 获取项目 ID 为 123 中合并请求 #5 的详细信息
mr = fetch_merge_request("123", "5")
```

### 查看特定文件变更

```python
# 获取合并请求中特定文件的差异
file_diff = fetch_merge_request_diff("123", "5", "path/to/file.js")
```

### 比较分支

```python
# 比较 develop 分支和 master 分支
diff = compare_versions("123", "develop", "master")
```

### 向合并请求添加评论

```python
# 向合并请求添加评论
comment = add_merge_request_comment("123", "5", "这段代码看起来不错！")
```

### 批准合并请求

```python
# 批准一个合并请求并将所需批准数设置为 2
approval = approve_merge_request("123", "5", approvals_required=2)
```

## 问题排查

如果您遇到问题：

1.  验证您的 GitLab 令牌是否具有适当的权限（api, read_api）
2.  检查您的 `.env` 文件设置
3.  确保您的 MCP 配置路径正确
4.  使用以下命令测试连接：`curl -H "Private-Token: your-token" https://gitlab.com/api/v4/projects`
5.  在您的 .env 文件中设置 `LOG_LEVEL=DEBUG` 以获取更详细的日志

## 贡献

欢迎贡献！请随时提交拉取请求（Pull Request）。

1.  Fork 本仓库
2.  创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3.  提交您的更改 (`git commit -m 'Add some amazing feature'`)
4.  推送到分支 (`git push origin feature/amazing-feature`)
5.  创建一个拉取请求

更多关于开发流程的细节，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 文件。

## 代码审查标准

本项目遵循严格的代码审查标准以确保质量和可维护性：

- 📋 **代码审查规范**: 本项目遵循一套严格的代码审查规范以确保质量和一致性。有关审查流程、标准和最佳实践的详细信息，请参阅[代码审查规范](CODE_REVIEW_GUIDELINES.md)。
- ✅ **审查清单**: 所有拉取请求在提交前都应根据 [PULL_REQUEST_CHECKLIST.md](PULL_REQUEST_CHECKLIST.md) 进行检查。
- 🔄 **CI/CD 流水线**: 我们使用 GitLab CI 进行自动化质量检查。在请求审查之前，请确保所有流水线检查都已通过。
- 📝 **模板**: 请使用我们提供的合并请求和问题模板，以确保包含了所有必要信息。

### 贡献者快速入门

1.  阅读[代码审查规范](CODE_REVIEW_GUIDELINES.md)
2.  创建拉取请求时使用适当的 MR 模板
3.  在请求审查前确保所有 CI 检查通过
4.  及时处理所有审查者的反馈

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。