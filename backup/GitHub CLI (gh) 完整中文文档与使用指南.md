GitHub CLI (gh) 完整中文文档与使用指南

创建人：chjs

创建时间：2026.04.02

最近使用了github cli，遂使用大模型将其文档翻译整理了一下。

## 一、快速入门与安装配置

GitHub CLI (简称 gh) 是 GitHub 官方提供的命令行工具，它允许您直接在终端中与 GitHub 交互，管理仓库、议题、拉取请求等工作，从而显著提升工作效率，减少在浏览器和终端之间切换的上下文成本。本章将指导您完成从安装到首次登录的完整设置流程。

### 🔧 安装 GitHub CLI

GitHub CLI 支持所有主流操作系统。请根据您的系统选择下方推荐的官方安装方法。

**重要**：以下所有安装方法均来源于官方文档，请根据您的操作系统参考执行。

| **操作系统** | **推荐安装方法及命令** | **补充说明** |
| --- | --- | --- |
| **Windows** | **使用 WinGet (推荐)** winget install --id GitHub.cli | 从[官方发布页](https://github.com/cli/cli/releases)下载 .msi 安装包双击运行亦可。 |
| **macOS** | **使用 Homebrew (推荐)** brew install gh | 也可通过 MacPorts、Conda 或下载 .pkg 安装包安装。 |
| **Linux (Ubuntu/Debian)** | **使用官方 APT 仓库** ```bash curl -fsSL <https://cli.github.com/packages/githubcli-archive-keyring.gpg> | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg echo “deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] <https://cli.github.com/packages> stable main” |
| **Linux (其他发行版)** | **使用系统包管理器** Fedora: sudo dnf install gh CentOS/RHEL (需EPEL): sudo yum install gh |  |

安装完成后，在终端中运行以下命令验证安装是否成功。如果安装正确，将显示 GitHub CLI 的版本号。

gh --version

### 🔐 身份认证与首次登录 (gh auth)

安装 gh 后，必须进行身份验证才能使用其完整的远程操作功能。这是通过 gh auth login 命令完成的交互式流程。

**登录流程详细步骤**

1. **启动登录**：在终端运行以下命令，进入交互式引导流程。

* gh auth login

1. **选择 GitHub 主机**：根据提示选择要登录的平台。
   * 对于公开的 GitHub.com，选择 GitHub.com。
   * 如果您使用 GitHub Enterprise Server，选择 Other，然后输入企业实例的主机名（例如 octocorp.ghe.com）。
2. **选择 Git 协议（关键步骤）**：
   * **HTTPS (推荐)**：这是更简单的选项。如果您同意，GitHub CLI **可以自动存储您的 Git 凭据**。这意味着之后使用 git push、git pull 等原生 Git 命令时，无需单独设置凭据管理器或 SSH 密钥。
   * **SSH**：如果您已配置 SSH 密钥并偏好使用它，可以选择此选项。
3. **选择认证方式**：
   * **Login with a web browser (推荐)**：这是最安全便捷的方式。CLI 会生成一个一次性代码。
     1. 终端显示一次性代码（如 0XXC-09XC）并提示按 **Enter** 键。
     2. 按 Enter 键，您的默认浏览器将自动打开 GitHub 的设备授权页面。
     3. 在浏览器中输入终端显示的一次性代码。
     4. 跟随浏览器提示完成对“GitHub CLI”应用的授权。
   * **Paste an authentication token**：如果您希望使用个人访问令牌 (PAT)，可以选择此方式。对应的非交互式命令是 gh auth login --with-token <your-token>。
4. **登录成功**：浏览器授权成功后，返回终端，您将看到如下确认信息：
   * ✓ Authentication complete.
   * ✓ Configured git protocol
   * ✓ Logged in as <您的用户名>

**验证与管理登录状态**

* 要随时检查当前认证状态，请运行：
* gh auth status
* 该命令会显示您当前登录的主机和账户。
* 如果您在同一主机（如 GitHub.com）上有多个账户，可以使用 gh auth switch 命令在它们之间切换。

**📌 重要注意事项**

* **权限范围**：当您首次使用某些需要额外权限的命令（例如 gh codespace 相关命令）时，可能会被提示为您的认证令牌添加额外的权限范围（scopes），只需跟随屏幕指示操作即可。
* **安全建议**：对于自动化场景（如 CI/CD），建议使用细粒度的个人访问令牌进行认证。在个人账户中，启用双因素认证 (2FA) 是重要的安全最佳实践。

完成以上**安装验证**与**身份认证**步骤后，您的 GitHub CLI 就已准备就绪。您可以立即开始使用 gh repo clone、gh issue create、gh pr create 等核心命令来高效管理工作流。接下来的章节将详细介绍这些功能的用法。

## 二、仓库管理（gh repo）

gh repo 是 GitHub CLI 最核心的子命令集之一，它让你无需离开终端即可完成仓库的完整生命周期管理。本章将详细介绍其所有子命令，助你将前序步骤的认证成果直接应用于实战。

### 1. gh repo clone - 🧬 **智能克隆**

此命令在原生 git clone 基础上进行了智能化封装，能自动处理身份认证和协议选择，且克隆 Fork 仓库时会自动添加上游（upstream）远程引用，极大简化了流程。

**基本语法**：

gh repo clone [<owner>/]<repository> [<directory>] [flags]

**常用示例**：

* **基础克隆**：克隆指定仓库到以仓库名命名的目录。
* gh repo clone cli/cli
* **指定目标目录**：克隆到自定义的本地目录。
* gh repo clone cli/cli my-cli-directory
* **高级 Git 参数**：通过 -- 分隔符，可以向底层的 git clone 传递任意参数，实现精细控制。
* # 浅克隆，仅获取最近一次提交历史
  gh repo clone owner/repo -- --depth=1
  # 仅克隆特定分支
  gh repo clone SAP/fundamental-tools sample -- --branch sample --single-branch

### 2. gh repo create - 🆕 **多场景创建**

这是功能最为强大的命令，完美覆盖了从零创建、基于模板生成和一键推送本地项目三大核心场景。

**基本语法**：

gh repo create [<name>] [flags]

**核心场景与示例**：

**场景一：从零开始创建（交互式/非交互式）**

* **交互式引导**：直接运行命令，跟随提示逐步设置。
* gh repo create
* **命令行一键创建**：通过参数直接指定所有属性。
* # 创建公共仓库，并附带描述
  gh repo create my-project --public --description “我的项目描述”
  # 创建私有仓库，并立即克隆到本地
  gh repo create my-project --private --clone

**场景二：基于模板创建**
快速使用已有仓库作为模板来初始化新项目。

gh repo create my-app --template owner/template-repo

**场景三：推送现有本地项目（革命性功能）**
此功能将传统的“网页创建 -> 添加远程 -> 首次推送”三步流程合并为一步，极大提升效率。

# 在已初始化的本地 Git 项目根目录执行
gh repo create my-project --source=. --public --push

**常用创建选项**：

* -d, --description <string>：设置仓库描述。
* -g, --gitignore <string>：指定 .gitignore 模板（如 Python, Node）。
* -l, --license <string>：指定开源许可证（如 MIT, Apache-2.0）。
* --add-readme：自动生成 README 文件。

### 3. gh repo view - 👁️ **快速查看**

用于在终端或浏览器中快速获取仓库信息。

**常用示例**：

* **终端概览**：在命令行中查看仓库的详细信息摘要。
* gh repo view owner/repo
* **网页打开**：在默认浏览器中打开该仓库的主页。
* gh repo view owner/repo --web
* **脚本友好输出**：以 JSON 格式输出特定字段，便于后续用 jq 等工具处理。
* gh repo view --json name,description,stargazerCount,url

### 4. gh repo fork - 🍴 **便捷分叉**

轻松为任何公开仓库创建个人 Fork，是参与开源贡献的标准第一步。

**常用示例**：

* **创建 Fork**：
* gh repo fork owner/repo
* **创建并克隆**：一键完成 Fork 和本地克隆。
* gh repo fork owner/repo --clone
* **手动添加上游源**（克隆后如需同步更新）：
* git remote add upstream https://github.com/original-owner/repo.git

### 5. gh repo list - 📜 **清单列表**

列出你个人账户或所属组织下的所有仓库。

**常用示例**：

# 列出你个人账户下的仓库
gh repo list
# 列出指定组织的仓库
gh repo list org-name
# 使用JSON输出，并限制数量、筛选字段
gh repo list --limit 10 --json name,isPrivate,pushedAt

### 6. gh repo edit - ✏️ **编辑属性**

修改仓库的元数据信息，如描述、主页 URL 等。

通过掌握 gh repo 这一系列命令，你几乎可以完全在终端内完成仓库的克隆、创建、查看、分叉和列表管理，将 GitHub 的仓库操作无缝集成到你的本地工作流中，显著提升效率。对于任何子命令，随时可以使用 gh repo <subcommand> --help 获取最详尽的参数说明。

## 三、议题管理（gh issue）

继掌握了仓库的创建、克隆与查看后，下一个核心协作环节便是**议题（Issue）** 的管理。gh issue 命令集允许你在终端中完成议题的创建、查看、列表、评论与状态跟踪，将问题追踪和讨论完全融入你的命令行工作流。

### 1. 创建议题：gh issue create

直接在当前仓库或指定仓库中创建新的议题，支持丰富的元数据设置。

* **基本语法**：
* gh issue create [flags]
* **关键参数与示例**：
  + **设置标题与正文**：使用 -t 或 --title 设置标题，-b 或 --body 设置详细描述。
  + gh issue create --title “Bug: 登录失败” --body “在输入用户名后，界面无响应。”
  + **分配与分类**：可以指定受理人、添加标签、关联至里程碑或项目。
    - -a, --assignee <string>: 分配受理人（可使用@me指代自己）。
    - -l, --label <strings>: 添加标签（多个标签用逗号分隔）。
    - -m, --milestone <string>: 关联里程碑。
    - --project <string>: 添加到指定项目。
  + gh issue create --title “文档改进” --body “需要更新 README.md” --assignee @me,monalisa --label “bug,help wanted” --project onboarding
  + **交互式与网页创建**：直接运行 gh issue create 会进入交互式引导；添加 --web 参数则会在浏览器中打开创建页面。

### 2. 查看与列表议题：gh issue list / gh issue view

快速浏览和筛选议题，或在终端/浏览器中查看详情。

* **gh issue list - 列出并筛选议题**
  + **常用筛选参数**：

| 参数 | 用途 | 示例 |
| --- | --- | --- |
| -s, --state | 按状态筛选：open, closed, all | --state all |
| -a, --assignee | 按受理人筛选 | --assignee "n8ebel" |
| -l, --label | 按标签筛选 | --label "bug" |
| -A, --author | 按作者筛选 | --author monalisa |
| -L, --limit | 限制输出数量（默认30） | --limit 50 |
| -R, --repo | 对指定仓库操作 | --repo owner/repo |

* + **输出控制**：
    - -w, --web：在浏览器中打开议题列表页。
    - --json <fields>：以JSON格式输出，支持字段包括 number, title, state, author, labels, assignees 等，便于脚本处理。
    - gh issue list --json number,title,assignees
* **gh issue view - 查看特定议题详情**
  + **语法**：gh issue view <number> [flags]
  + **示例**：
  + # 在终端查看15号议题
    gh issue view 15
    # 在浏览器中查看123号议题
    gh issue view 123 --web
    # 以JSON格式输出详情
    gh issue view 15 --json body,comments

### 3. 状态概览：gh issue status

快速查看与你相关的议题摘要，例如分配给你、由你创建或提及你的议题，帮你掌握待办事项。

gh issue status

### 4. 议题互动操作：评论、关闭与重开

对议题进行跟进和生命周期管理。

* **gh issue comment - 添加评论**
* gh issue comment <number> --body “已在 v2.3.0 版本中确认此问题，正在添加重现步骤。”
* **gh issue close - 关闭议题**（可附带说明）
* gh issue close 15 --comment “已在提交 abc123 中修复。”
* **gh issue reopen - 重新打开议题**
* gh issue reopen <number>

### 5. 高级用法：脚本集成与效率提升

将 gh issue 无缝集成到自动化脚本和个性化工作流中。

* **脚本自动化处理**：结合 --json 输出和 jq 等命令行JSON处理工具，可以轻松实现议题数据的提取、过滤和批量操作。
* # 获取所有开放议题的编号，并循环处理
  gh issue list --state open --json number | jq ‘.[].number’ | while read num; do
   echo “处理议题 #$num”
   # 此处可添加你的自动化逻辑，例如添加特定评论
  done
* **设置命令别名**：通过 gh alias set 为高频操作创建快捷方式，大幅提升日常效率。
* # 将“列出我所有开放议题”设置为别名 `myissues`
  gh alias set myissues ‘issue list --assignee @me --state open’
  # 之后即可使用
  gh myissues

通过 gh issue 命令集，你可以将议题跟踪这一核心协作活动深度绑定到终端环境，减少上下文切换，实现从编码、问题反馈到讨论解决的全流程命令行闭环。

## 四、拉取请求管理（gh pr）

承接前序的仓库管理与议题追踪，代码协作的核心环节——**拉取请求（Pull Request）** ——将通过 gh pr 命令集在终端内完成全程管理。该命令覆盖了从创建、列表查看、代码审查到合并的完整生命周期，极大简化了基于分支的协作流程。

### 🔍 核心子命令全景

gh pr 提供了管理拉取请求生命周期所需的全部工具，其主要子命令包括：

| 命令 | 核心功能 | 关键场景 |
| --- | --- | --- |
| **list** | 列出并筛选拉取请求 | 查看当前开放的PR、需要你审查的PR |
| **create** | 创建新的拉取请求 | 推送分支后，发起代码合并请求 |
| **view** | 查看PR详情 | 在终端或浏览器中检查PR描述、状态 |
| **checkout** | 检出PR到本地 | 将他人的PR分支拉到本地进行测试或审查 |
| **merge** | 合并拉取请求 | 在审查通过后，将更改合并入目标分支 |
| **status** | 查看相关PR状态 | 快速概览由你创建或等待你处理的PR |
| **diff** | 查看代码差异 | 审查PR引入的具体代码更改 |

### 📋 列表与筛选：gh pr list

此命令用于列出当前仓库的拉取请求，支持丰富的过滤条件，便于快速定位。

* **常用参数选项**：
  + --state <string>： 按状态过滤，可选 open（默认）、closed、merged 或 all。
  + --assignee <string>： 按受理人过滤。
  + --label <string>： 按标签过滤。
  + --web： 在默认浏览器中打开仓库的PR列表页面。
  + --json <fields>： 以指定的JSON字段输出结果，便于后续脚本处理。
* **使用示例**：
* # 列出所有开放的PR
  gh pr list
  # 列出所有已关闭的PR
  gh pr list --state closed
  # 列出带有“bug”标签的PR
  gh pr list --label bug
  # 以JSON格式输出PR编号和标题，用于脚本处理
  gh pr list --state open --json number,title

### 🚀 创建与发起：gh pr create

这是最常用的命令之一，用于为当前分支或指定分支创建拉取请求。支持直接定义标题、正文、审查者等所有属性。

* **常用参数选项**：
  + --title <string>： 设置PR的标题。
  + --body <string>： 设置PR的详细描述正文。
  + --base <branch>： 指定目标分支（即要合并到的分支，如 main）。
  + --head <branch>： 指定源分支（包含更改的分支）。默认使用当前分支。
  + --draft： 创建为**草稿PR**，表示尚未准备就绪。
  + --assignee <login>： 分配PR给特定用户。使用 @me 表示分配给自己。
  + --reviewer <logins>： 请求指定用户或团队进行审查。
  + --label <labels>： 为PR添加标签。
  + --project <name>： 将PR添加到特定项目板。
  + --web： 在浏览器中打开创建页面，使用网页表单填写。
  + --fill： **自动使用最近的提交信息**来填充标题和正文。
* **使用示例**：
* # 基于当前分支创建PR，目标分支为main，并设置标题和正文
  gh pr create --base main --title "添加登录功能" --body "实现了OAuth2登录流程"
  # 创建草稿PR
  gh pr create --title "WIP: 新功能" --draft
  # 分配给自己，并请求同事'octocat'和团队'myorg/core-team'审查
  gh pr create --assignee @me --reviewer octocat,myorg/core-team
  # 使用最近的提交信息自动填充标题和正文（非常高效）
  gh pr create --fill

### 👁️ 查看与审查：gh pr view、diff 与 checkout

这三个命令构成了本地代码审查的核心工作流。

1. **gh pr view**： 查看特定PR的详细信息。
   * 示例：
   * # 在终端查看编号为123的PR详情
     gh pr view 123
     # 在浏览器中打开该PR进行查看
     gh pr view 123 --web
2. **gh pr diff**： 查看指定PR引入的所有代码更改（diff）。
   * 示例：
   * # 查看PR #789的代码差异
     gh pr diff 789
3. **gh pr checkout**： **将指定PR对应的远程分支拉取到本地并切换过去**，便于进行本地运行测试或深度代码审查。
   * 示例：
   * # 检出编号为42的PR到本地（会创建一个对应的本地分支）
     gh pr checkout 42

### ✅ 合并与清理：gh pr merge

在PR通过审查后，使用此命令将其合并到目标分支。

* **常用参数选项**：
  + <number>： 要合并的PR编号（必填）。
  + --merge, --squash, --rebase： 指定**合并策略**。
    - --merge： 创建合并提交，保留完整历史。
    - --squash： 将所有提交压缩为**一个提交**再合并，保持线性历史。
    - --rebase： 变基合并。
  + --delete-branch： 合并后**删除源分支**（头部分支）。
* **使用示例**：
* # 使用合并提交的方式合并PR #456
  gh pr merge 456 --merge
  # 使用压缩提交的方式合并，并自定义提交信息
  gh pr merge 456 --squash --commit-message “合并功能X”
  # 合并后删除源分支
  gh pr merge 789 --squash --delete-branch

### 📊 状态概览：gh pr status

快速查看与你相关的PR摘要，通常分为“你创建的”、“等待你审查的”等类别，是每日站会的利器。

* 示例：
* gh pr status

### ⚙️ 进阶技巧与工作流集成

掌握基础命令后，以下技巧能进一步提升效率：

1. **典型Git工作流集成**： 在本地完成功能开发、提交并推送到远程分支后，直接使用 gh pr create 发起合并请求，形成无缝衔接的终端协作流。
2. **利用别名简化操作**： 通过 gh alias set 为常用命令设置快捷方式。

* gh alias set pc 'pr create --web' # 之后可用 `gh pc` 快速通过网页创建PR
  gh alias set pv 'pr view --web' # 快速在浏览器中查看PR

1. **脚本化与自动化**： 结合 --json 参数输出结构化数据，利用 jq 等工具编写脚本，实现自动检查PR状态、批量合并等流程。

* # 获取所有开放PR的编号列表，用于脚本循环处理
  gh pr list --state open --json number | jq '.[].number'

1. **随时获取帮助**： 任何子命令均可通过 --help 标志查看最详细、最新的官方参数说明。

* gh pr create --help

通过 gh pr 命令集，你可以将拉取请求的创建、跟踪、审查和合并完全嵌入到终端工作流中，显著减少上下文切换，提升代码协作的效率与流畅度。

## 五、GitHub Actions 集成（gh workflow / gh run / gh cache）

借助 gh，你可以高效地在命令行中管理 GitHub Actions，包括触发、监控工作流，管理缓存，甚至在工作流内部使用 gh 来操作 GitHub，构建强大的自动化流程。

### gh workflow: 管理工作流定义

gh workflow 命令用于管理 GitHub Actions 的工作流定义，例如查看、启用、禁用以及最重要的**手动触发**工作流。

#### gh workflow list: 列出所有工作流

用于查看仓库中定义的工作流文件及其状态。

* **常用选项**：
  + 清楚列出所有工作流，包括已禁用的。
  + 限制显示的数量（默认：50）。
* **示例**：
* # 列出当前仓库的活跃工作流
  gh workflow list

  # 列出指定仓库的所有工作流（包括已禁用的）
  gh workflow list --all --repo owner/repo

#### gh workflow view: 查看工作流详情

查看指定工作流的 YAML 文件内容或最近运行状态。

* **常用选项**：
  + 在默认浏览器中打开工作流页面。
  + 查看指定分支上的工作流文件内容。
  + 以原始 YAML 格式输出工作流文件内容。
* **示例**：
* # 查看名为 “CI” 的工作流详情
  gh workflow view “CI”
  # 获取 main 分支上 “deploy.yml” 工作流的原始 YAML
  gh workflow view deploy.yml --ref main --yaml

#### gh workflow run: 手动触发工作流运行

这是最强大和常用的子命令，可使用命令行参数直接触发配置了 workflow\_dispatch 事件的工作流。它可以替代 Web 界面上的 “Run workflow” 按钮，并支持参数化和脚本化调用。

* **触发前提**：目标工作流必须在仓库的默认分支中，并已配置 workflow\_dispatch 触发器。
* **核心语法**：gh workflow run <workflow> [flags]。其中 <workflow> 可以是工作流名称、ID 或 YAML 文件名。
* **关键参数**：
  + 在指定的分支、标签或提交上运行工作流。
  + 为工作流提供输入参数，可以多次使用。
  + 从文件中读取内容作为输入参数的值。
  + 通过标准输入（stdin）以 JSON 格式传递所有输入。
* **使用示例**：
* # 触发名为 “Link Checker” 的工作流（CLI 会交互式提示输入）
  gh workflow run “Link Checker”

  # 在 “develop” 分支上运行工作流
  gh workflow run “CI” --ref develop

  # 传递输入参数（例如，传递多个构建参数）
  gh workflow run “go构建并下载” \
   --ref main \
   -f repoPath=”https://github.com/owner/repo.git” \
   -f GO\_VERSION=”1.20” \
   -f platforms=”linux/amd64,darwin/arm64”

  # 通过 stdin 传递 JSON 格式的输入
  echo ‘{“name”:”mona”, “greeting”:”hello”}’ | gh workflow run greet.yml --json

#### 启用与禁用

* gh workflow disable <workflow>: 禁用指定工作流。
* gh workflow enable <workflow>: 启用指定工作流。

### gh run: 管理工作流运行实例

触发工作流后，gh run 命令组用于监控、检查和重新运行这些具体的执行实例。它涵盖了工作流运行的整个生命周期。

#### gh run list: 列出历史运行记录

查看仓库中最近的工作流执行历史，并支持强大的过滤。

* **常用过滤器**：限制返回数量、按工作流筛选、按状态筛选（如 failure）、按分支筛选。
* **脚本化输出**：—json 标志可以输出结构化数据，便于配合 jq 进行自动化处理。
* **示例**：
* # 列出名为 “Deploy” 的工作流所有失败的运行
  gh run list --workflow “Deploy” --status failure
  # 以 JSON 格式输出最近的运行信息
  gh run list --limit 3 --json number,workflowName,status,conclusion

#### gh run view: 查看运行详情与日志

深入查看某次特定运行的详细信息，包括每个作业和步骤的状态、日志输出。

* **常用选项**：
  + 查看本次运行中某个特定作业的详细信息。
  + 查看完整日志（结合 —job 可看特定作业的日志）。
  + 仅输出失败步骤的日志，便于快速排查。
  + 如果运行失败，命令以非零状态退出，便于在脚本中判断结果。
* **示例**：
* # 查看 ID 为 123456 的运行详情
  gh run view 123456 —verbose
  # 查看特定作业（ID: 987654）的完整日志，并过滤错误
  gh run view --job 987654 --log | grep “ERROR”
  # 在脚本中判断运行是否成功
  if gh run view 0451 --exit-status; then
   echo “运行成功或进行中”
  else
   echo “运行失败”
  fi

#### gh run rerun: 重新运行

重新触发已经执行过的工作流或其中特定的作业。这是调试失败 CI 的常用操作。

* **重要机制**：重新运行时将使用**原始触发者**的权限以及相同的提交 SHA 和 Git 引用。
* **常用选项**：
  + 仅重新运行指定运行中失败的作业及其依赖。
  + 重新运行工作流中的某个特定作业及其依赖。
  + 为重新运行启用运行器诊断日志和步骤调试日志记录。
* **示例**：
* # 重新运行整个工作流
  gh run rerun 754118627
  # 仅重新运行失败的作业
  gh run rerun 754118627 --failed
  # 重新运行特定作业并启用调试
  gh run rerun --job 1234567 --debug

#### gh run watch: 实时监控运行进度

在终端中实时流式输出（tail）某次工作流运行的日志。这让你无需刷新网页即可观察 CI/CD 进度。

# 监控最近一次运行的实时日志（不指定 ID，CLI 提供交互菜单）
gh run watch
# 监控特定运行的进度
gh run watch 123456

#### gh run download: 下载构件 (Artifacts)

用于下载工作流运行生成的产物。

# 下载某次运行中名为 “coverage-report” 的构件
gh run download 123456 -n coverage-report

### gh cache: 管理 Actions 依赖缓存

GitHub Actions 缓存用于存储依赖项以加速工作流运行。gh cache 命令允许你直接从命令行查看和管理这些缓存条目，是自动化缓存维护、防止存储配额被占满的关键工具。

#### gh cache list: 列出与筛选缓存

列出仓库中的缓存条目，并提供丰富的过滤、排序和输出格式化选项。这是核心的管理命令。

* **关键参数**：

| 选项 | 描述 | 默认值 |
| --- | --- | --- |
| 按缓存键（key）的前缀进行过滤 | - |  |
| 要获取的最大缓存数量 | 30 |  |
| 按 Git 引用（ref）过滤（如 refs/heads/main） | - |  |
| 对缓存进行排序的字段：created\_at, last\_accessed\_at 或 size\_in\_bytes | "last\_accessed\_at" |  |
| 排序顺序：asc（升序）或 desc（降序） | "desc" |  |
| 使用指定的字段输出 JSON 格式的结果（如 id,key,sizeInBytes） | - |  |
| 使用 jq 表达式过滤 JSON 输出 | - |  |

* **示例**：
* # 列出 main 分支的缓存
  gh cache list --ref refs/heads/main
  # 列出与 PR #123 相关的缓存
  gh cache list --ref refs/pull/123/merge
  # 以 JSON 格式仅输出键为 “npm-” 开头的缓存 ID 和大小
  gh cache list --key “npm-” --json id,key,sizeInBytes
  # 使用 jq 筛选出大于 100MB 的庞大缓存
  gh cache list --json id,key,sizeInBytes --jq ‘.[] | select(.sizeInBytes > 100\*1024\*1024)’

#### gh cache delete: 删除缓存

删除特定的缓存条目。通常与 gh cache list 结合，用于自动化清理脚本，例如在拉取请求关闭后移除其相关缓存。

* **基本用法**：
* gh cache delete <cache-id>
* 其中 <cache-id> 通过 gh cache list --json id 获取。
* **自动化清理示例**：以下是一个在 PR 关闭后清理其缓存的 GitHub Actions 工作流片段，展示了如何组合使用 list 和 delete：
* - name: Cleanup PR Caches
   runs-on: ubuntu-latest
   permissions:
   actions: write # 必须有写入权限才能删除缓存
   steps:
   - run: |
   # 获取特定引用下的缓存 ID 列表
   cacheKeysForPR=$(gh cache list --ref $BRANCH --limit 100 --json id --jq ‘.[].id’)
   set +e # 不因删除失败而中断工作流
   for cacheKey in $cacheKeysForPR
   do
   gh cache delete $cacheKey
   done
   env:
   GH\_TOKEN: ${{ github.token }}
   GH\_REPO: ${{ github.repository }}
   BRANCH: refs/pull/${{ github.event.pull\_request.number }}/merge

### 在 Actions 工作流中使用 gh

GitHub CLI (gh) 本身已预装在 GitHub 托管的运行器上。这意味着你可以在 Actions 工作流的步骤中直接使用 gh 命令来操作 GitHub，实现更高级的自动化。

* **关键设置**：必须在步骤中设置 GH\_TOKEN 环境变量（通常值为 ${{ github.token }}），为 gh 命令提供权限。
* **应用场景**：
  + **自动化 Issue/PR 管理**：在工作流步骤中自动创建 Issue、评论 PR。
  + **调用 GitHub API**：结合 gh api 查询 REST 或 GraphQL API，并将结果用于后续逻辑。
  + **触发其他工作流**：使用 gh workflow run 实现工作流间的链式触发。

通过 gh workflow、gh run 和 gh cache 命令组，你可以构建一个完全在命令行中闭环的 CI/CD 操作与监控环境，实现从触发、监控到资源管理的全链路高效管理。

## 六、扩展与高级配置（gh extension / gh config / gh alias）

熟练运用 GitHub CLI 的核心命令后，你可以通过本章介绍的高级功能，将 gh 彻底定制为你的专属效率工具。本节将系统讲解如何管理第三方扩展 (gh extension)、调整 CLI 的全局行为 (gh config)，以及创建和管理命令别名 (gh alias)。

### 安装与管理第三方扩展

gh extension 命令为你打开了 GitHub CLI 的生态世界，允许你安装、使用和创建社区开发的扩展，无缝添加新功能。

**安装扩展**：每个扩展都是一个 GitHub 仓库，其名称**必须**以 gh- 开头（例如 gh-whoami）。你可以从仓库简写或完整 URL 安装。

# 从 GitHub.com 安装扩展
gh extension install dlvhdr/gh-dash

# 使用完整 URL 安装（适用于从 GitHub Enterprise Server 安装 GitHub.com 的扩展）
gh extension install https://github.com/octocat/gh-whoami

# 安装本地正在开发的扩展
cd ~/projects/gh-my-extension
gh extension install .

注意：如果已安装同名扩展，安装新来源的同名扩展会失败，需先卸载。

**管理已安装的扩展**：

* 列出所有已安装的扩展，并查看是否有更新：gh extension list
* 更新特定扩展：gh extension upgrade <扩展名> （扩展名是仓库名去掉 gh- 前缀的部分）
* 更新所有扩展：gh extension upgrade --all
* 卸载扩展：gh extension remove <扩展名>

**创建新扩展**：gh 提供了便捷的脚手架命令。

# 创建解释型扩展（如 Bash 脚本）
gh extension create hello

# 创建基于 Go 的预编译扩展（包含 Go 脚手架和工作流配置）
gh extension create --precompiled=go hello-go

# 创建基于其他语言（如 Rust）的预编译扩展（包含工作流脚手架）
gh extension create --precompiled=other hello-rust

安装扩展后，即可像使用内置命令一样运行它：gh <扩展名>。所有传递给 gh <扩展名> 的参数都会传递给扩展脚本。

### 精细调整 CLI 全局行为

gh config 命令用于查看和修改 GitHub CLI 的本地配置，所有设置存储在用户主目录下的配置文件（如 ~/.config/gh/config.yml）中。

**查看配置**：使用 gh config get 查询指定配置项的当前值。

# 查看当前设置的默认文本编辑器
gh config get editor

# 查看 Git 操作默认使用的协议
gh config get git\_protocol

**修改配置**：使用 gh config set 更新配置，这是定制工作流的关键。

# 设置默认编辑器为 Visual Studio Code，并等待编辑完成
gh config set editor "code -w"

# 设置 Git 操作用 HTTPS 协议（便于自动存储凭据，简化 git push/pull）
gh config set git\_protocol https

除了 editor 和 git\_protocol，你还可以配置 prompt（交互式提示）、pager（分页程序）等选项。

### 创建与管理命令别名

gh alias 命令允许你为常用或复杂的命令序列创建简短易记的快捷方式，这是提升日常操作效率最直接的方法。

**设置别名**：使用 gh alias set 定义新别名。

# 为常用操作设置短别名
gh alias set co 'pr checkout'
gh alias set pc 'pr create'

# 为带复杂参数的查询设置别名（回顾第三章的例子）
gh alias set myissues 'issue list --assignee=@me --state=open'

# 为创建草稿 PR 设置专门别名（回顾第四章的例子）
gh alias set prd "pr create --draft"

设置后，gh co 123 等同于 gh pr checkout 123，gh prd 则直接启动创建草稿 PR 的流程。

**管理别名**：

* 列出所有已设置的别名及其对应命令：gh alias list
* 删除不再需要的别名：gh alias delete <别名>

**手动编辑配置**：除了命令行，你还可以直接编辑配置文件来管理别名，便于批量操作或备份。
配置文件通常位于 ~/.config/gh/config.yml。在 aliases: 节点下直接添加或修改即可：

aliases:
 co: pr checkout
 pc: pr create
 prd: pr create --draft

通过合理组合使用扩展、配置和别名，你可以将 GitHub CLI 打造成一个高度个性化、高效无缝的命令行工作环境，真正实现“将 GitHub 带到命令行”的愿景。

## 七、通用 API 调用（gh api）

经过前面对仓库、议题、PR 和 Actions 等具体功能的学习，你已掌握了 gh 面向特定场景的命令。现在，让我们进入最通用、最强大的环节：gh api。它允许你直接向 GitHub 的 REST API 或 GraphQL API 发送经过身份验证的请求，实现任何 gh 原生命令未覆盖或需要高度自定义的自动化操作。

gh api 的设计哲学是 **“终端优先、无缝集成”**。它自动处理认证（复用 gh auth login 的令牌），支持智能参数传递，并能与 jq 等工具完美结合，让你将 GitHub 的完整能力深度嵌入命令行工作流和自动化脚本中。

### 🧠 核心语法与自动替换

其基本语法极为简洁：

gh api <endpoint> [flags]

* **<endpoint>**： GitHub API v3 (REST) 的路径，或使用 graphql 来访问 API v4 (GraphQL)。例如 /repos/{owner}/{repo}/issues。
* **关键特性**：路径中的占位符 {owner}、{repo}、{branch} 会被**自动替换**。在当前 Git 仓库目录下操作时，这些占位符会填充为当前仓库的值；若非 Git 仓库，则使用 GH\_REPO 环境变量中的值。这使命令通用且简洁。

### ⚙️ 核心参数详解

gh api 提供了丰富的标志来精细控制请求，下表是核心参数的快速参考：

| 选项 | 缩写 | 描述与典型用途 |
| --- | --- | --- |
| --method | -X | 指定 HTTP 请求方法（GET, POST, PATCH 等）。 |
| --field | -F | **智能参数传递**：传递 key=value，支持 JSON 类型转换（如 true 转布尔值）、读取文件（@filename）和自动替换占位符。 |
| --raw-field | -f | 传递字符串参数 key=value。添加此参数会自动将请求方法切换为 POST。 |
| --header | -H | 添加自定义 HTTP 请求头，如控制返回格式。 |
| --jq | -q | **响应处理利器**：使用 jq 查询语法从 JSON 响应中提取和筛选数据。 |
| --paginate |  | 自动请求并合并所有分页的结果，用于处理列表数据。 |
| --slurp |  | 与 --paginate 同用，将所有分页结果包装到一个 JSON 数组中输出。 |
| --input |  | 从文件或标准输入（-）读取内容作为请求主体。 |
| --template | -t | 使用 Go 模板语法自定义格式化 JSON 输出，可添加颜色。 |
| --verbose |  | 输出完整的 HTTP 请求和响应细节，用于调试。 |
| --silent |  | 不打印响应主体，仅执行请求。 |
| --hostname |  | 指定 GitHub 主机名，用于 GitHub Enterprise Server。 |
| --cache |  | 缓存响应，格式如 1h。 |

### 🚀 基础使用示例

以下示例直接基于现有知识，展示常见场景。

1. **获取数据（GET）**： 列出当前仓库的所有发布（Releases）。

* gh api /repos/{owner}/{repo}/releases
* 利用了路径占位符的便利性。

1. **创建资源（POST）**： 在 Issues #123 下发表评论。

* gh api /repos/{owner}/{repo}/issues/123/comments -f body='评论内容'
* 使用 -f 传递内容，方法自动变为 POST。

1. **发送文件内容**： 创建一个包含本地文件内容的 Gist。

* gh api gists -F 'description=我的代码片段' -F 'files[test.sh][content]=@./local\_script.sh'
* 演示了 -F 如何通过嵌套语法（key[subkey]=value）和 @ 符号读取文件。

1. **使用 jq 过滤**： 仅获取当前仓库所有 Issue 的标题。

* gh api /repos/{owner}/{repo}/issues --jq '.[].title'
* 这与之前 gh issue list --json title 的输出类似，但 gh api 让你能访问 API 提供的任何字段。

### 🧰 高级用法实战

掌握了基础后，这些技巧能将你的自动化提升到新的层次。

#### 1. 复杂参数传递与类型转换

gh api 的参数传递非常强大。你可以传递数组：

gh api --method PATCH /orgs/{org}/properties/schema \
 -F 'properties[][property\_name]=environment' \
 -F 'properties[][default\_value]=production' \
 -F 'properties[][allowed\_values][]=staging' \
 -F 'properties[][allowed\_values][]=production'

#### 2. 高效处理分页数据

对于可能返回大量结果的列表型 API（如 user/repos），使用 --paginate 自动获取所有页面。

# 获取用户的所有仓库（自动处理分页）
gh api user/repos --paginate

如果需要对所有数据进行整体分析，结合 --slurp 将所有页结果合并为一个 JSON 数组，方便 jq 处理。

#### 3. 执行 GraphQL 查询

gh api 同样完美支持更灵活的 GraphQL API。

gh api graphql -F owner='{owner}' -F name='{repo}' -f query='
 query($name: String!, $owner: String!) {
 repository(owner: $owner, name: $name) {
 releases(last: 3) {
 nodes { tagName }
 }
 }
 }
'

注意，通过 -F 传递的字段（如 owner, name）会被视为 GraphQL 变量。

#### 4. 自定义输出模板

使用 --template 可以定制化输出格式和样式。

gh api /repos/{owner}/{repo}/issues --template \
 '{{range .}}{{.title}} ({{.labels | pluck "name" | join ", " | color "yellow"}}){{\"\n\"}}{{end}}'

此模板输出每个 Issue 的标题，并将其标签名称用黄色高亮显示。

#### 5. 在 CI/CD 工作流中集成

在 GitHub Actions 中，使用内置的 GITHUB\_TOKEN 进行认证， gh api 是实现复杂逻辑的利器。

- name: 通过 API 创建 Issue
 env:
 GH\_TOKEN: ${{ secrets.GITHUB\_TOKEN }}
 run: |
 gh api /repos/${{ github.repository }}/issues \
 -f title="自动化报告" \
 -f body="此 Issue 由工作流于 ${{ github.sha }} 创建"

### 📝 最佳实践总结

1. **善用占位符**：在仓库目录下操作时，充分利用 {owner}、{repo} 的自动替换，使命令更通用。
2. **优先使用 -F**：相比 -f，-F 支持类型转换和文件读取，功能更全面。
3. **响应处理管道化**：将 gh api 与 jq、--template 或 --paginate 结合，在命令行中直接完成数据提取、格式化和分析。
4. **认证安全**：在自动化环境中，使用 GITHUB\_TOKEN 或从安全存储中读取令牌，并遵循最小权限原则。

通过 gh api，你获得的不只是一个 API 调用工具，而是一个能够将任意 GitHub 操作编织进你本地开发与自动化流水线中的强大引擎。

## 八、完整命令索引与速查表

本节提供 GitHub CLI (gh) 所有命令的完整索引，旨在作为日常使用时的快速参考手册。命令按功能领域分组，每个条目包含命令、简要说明及一个典型用法示例，以兼顾入门指引与高阶查询需求。

### 核心命令 (Core Commands)

这些命令用于处理 GitHub 上的日常核心操作。

| 命令 | 作用 | 典型用法 |
| --- | --- | --- |
| **gh auth** | 管理认证 | gh auth login |
| gh auth login | 交互式登录 GitHub | gh auth login |
| gh auth logout | 退出登录 | gh auth logout |
| gh auth refresh | 刷新认证状态 | gh auth refresh |
| gh auth setup-git | 配置 Git 使用 gh 进行认证 | gh auth setup-git |
| gh auth status | 显示当前登录状态 | gh auth status |
| gh auth switch | 在多个账户间切换 | gh auth switch |
| gh auth token | 打印认证令牌 | gh auth token |
| **gh browse** | 在浏览器中打开仓库、议题或 PR | gh browse --issues |
| **gh codespace** | 管理 GitHub Codespaces | gh codespace list |
| gh codespace code | 在 VS Code 中打开 Codespace | gh codespace code -c <name> |
| gh codespace cp | 在本地与 Codespace 间复制文件 | gh codespace cp ./localfile .:/remote/path -c <name> |
| gh codespace create | 新建一个 Codespace | gh codespace create -r owner/repo |
| gh codespace delete | 删除 Codespace | gh codespace delete -c <name> |
| gh codespace edit | 编辑 Codespace 属性 | gh codespace edit -c <name> --display-name “New Name” |
| gh codespace jupyter | 在浏览器中打开 JupyterLab | gh codespace jupyter -c <name> |
| gh codespace list | 列出可用的 Codespaces | gh codespace list |
| gh codespace logs | 获取 Codespace 日志 | gh codespace logs -c <name> |
| gh codespace ports | 列出 Codespace 端口 | gh codespace ports -c <name> |
| gh codespace ports forward | 转发端口到本地 | gh codespace ports forward <port> -c <name> |
| gh codespace ports visibility | 设置端口可见性 | gh codespace ports visibility <port>:private -c <name> |
| gh codespace rebuild | 重建 Codespace | gh codespace rebuild -c <name> |
| gh codespace ssh | 通过 SSH 连接至 Codespace | gh codespace ssh -c <name> |
| gh codespace stop | 停止 Codespace | gh codespace stop -c <name> |
| gh codespace view | 查看 Codespace 详情 | gh codespace view -c <name> |
| **gh gist** | 管理 Gists | gh gist list |
| gh gist clone | 克隆一个 Gist 到本地 | gh gist clone <gist-id> |
| gh gist create | 创建一个新的 Gist | gh gist create <file> |
| gh gist delete | 删除一个 Gist | gh gist delete <gist-id> |
| gh gist edit | 编辑一个 Gist | gh gist edit <gist-id> |
| gh gist list | 列出你的 Gists | gh gist list |
| gh gist rename | 重命名一个 Gist | gh gist rename <gist-id> <new-name> |
| gh gist view | 查看一个 Gist | gh gist view <gist-id> |
| **gh issue** | 管理议题 | gh issue list |
| gh issue close | 关闭议题 | gh issue close 123 |
| gh issue comment | 在议题下发表评论 | gh issue comment 123 --body “确认问题” |
| gh issue create | 创建议题 | gh issue create -t “标题” -b “正文” |
| gh issue delete | 删除议题 | gh issue delete 123 |
| gh issue develop | 为议题创建开发分支 | gh issue develop 123 |
| gh issue edit | 编辑议题 | gh issue edit 123 --title “新标题” |
| gh issue list | 列出现有议题 | gh issue list --state open --assignee @me |
| gh issue lock | 锁定议题（禁止评论） | gh issue lock 123 |
| gh issue pin | 置顶议题 | gh issue pin 123 |
| gh issue reopen | 重新打开已关闭的议题 | gh issue reopen 123 |
| gh issue status | 展示与你相关议题的概览 | gh issue status |
| gh issue transfer | 将议题转移到其他仓库 | gh issue transfer 123 --repo new-owner/new-repo |
| gh issue unlock | 解锁议题 | gh issue unlock 123 |
| gh issue unpin | 取消议题置顶 | gh issue unpin 123 |
| gh issue view | 查看议题详情 | gh issue view 123 --web |
| **gh org** | 管理组织 | gh org list |
| **gh pr** | 管理拉取请求 | gh pr create |
| gh pr checkout | 将 PR 分支检出到本地 | gh pr checkout 456 |
| gh pr checks | 查看 PR 的 CI 检查状态 | gh pr checks 456 |
| gh pr close | 关闭 PR | gh pr close 456 |
| gh pr comment | 在 PR 下发表评论 | gh pr comment 456 --body “LGTM” |
| gh pr create | 创建 PR | gh pr create --fill --reviewer octocat |
| gh pr diff | 查看 PR 的代码差异 | gh pr diff 456 |
| gh pr edit | 编辑 PR 元数据 | gh pr edit 456 --title “新标题” |
| gh pr list | 列出 PR | gh pr list --state open --label bug |
| gh pr lock | 锁定 PR 对话 | gh pr lock 456 |
| gh pr merge | 合并 PR | gh pr merge 456 --squash --delete-branch |
| gh pr ready | 标记 PR 为准备评审 | gh pr ready 456 |
| gh pr reopen | 重新打开已关闭的 PR | gh pr reopen 456 |
| gh pr revert | 还原一个合并的 PR | gh pr revert 456 |
| gh pr review | 提交 PR 评审 | gh pr review 456 --approve --body “很好！” |
| gh pr status | 展示与你相关 PR 的概览 | gh pr status |
| gh pr unlock | 解锁 PR | gh pr unlock 456 |
| gh pr update-branch | 更新 PR 分支（合并目标分支） | gh pr update-branch 456 |
| gh pr view | 查看 PR 详情 | gh pr view 456 --web |
| **gh project** | 管理 GitHub 项目 | gh project list |
| gh project close | 关闭项目 | gh project close <number> |
| gh project copy | 复制项目 | gh project copy <number> |
| gh project create | 创建项目 | gh project create --owner org --title “新项目” |
| gh project delete | 删除项目 | gh project delete <number> |
| gh project edit | 编辑项目元数据 | gh project edit <number> --title “新标题” |
| gh project field-create | 为项目创建字段 | gh project field-create <number> --name “状态” --data-type SINGLE\_SELECT |
| gh project field-delete | 删除项目字段 | gh project field-delete <number> --id <field-id> |
| gh project field-list | 列出项目字段 | gh project field-list <number> |
| gh project item-add | 将议题/PR 添加到项目 | gh project item-add <number> --url <issue-url> |
| gh project item-archive | 归档项目项 | gh project item-archive <number> --id <item-id> |
| gh project item-create | 在项目中创建新项 | gh project item-create <number> --title “新任务” |
| gh project item-delete | 删除项目项 | gh project item-delete <number> --id <item-id> |
| gh project item-edit | 编辑项目项 | gh project item-edit <number> --id <item-id> --field “状态:进行中” |
| gh project item-list | 列出项目项 | gh project item-list <number> |
| gh project link | 链接项目模板 | gh project link <template-url> |
| gh project list | 列出项目 | gh project list --owner org |
| gh project mark-template | 将项目标记为模板 | gh project mark-template <number> |
| gh project unlink | 取消项目与模板的链接 | gh project unlink <number> |
| gh project view | 查看项目详情 | gh project view <number> --web |
| **gh release** | 管理发布 | gh release list |
| gh release create | 创建发布 | gh release create v1.0.0 --title “正式版” |
| gh release delete-asset | 删除发布中的资源文件 | gh release delete-asset v1.0.0 <asset-name> |
| gh release delete | 删除发布 | gh release delete v1.0.0 |
| gh release download | 下载发布资源 | gh release download v1.0.0 |
| gh release edit | 编辑发布信息 | gh release edit v1.0.0 --title “新标题” |
| gh release list | 列出发布 | gh release list |
| gh release upload | 上传资源到发布 | gh release upload v1.0.0 ./build.zip |
| gh release verify-asset | 验证发布资源签名 | gh release verify-asset v1.0.0 <asset-name> |
| gh release verify | 验证发布签名 | gh release verify v1.0.0 |
| gh release view | 查看发布详情 | gh release view v1.0.0 |
| **gh repo** | 管理仓库 | gh repo clone |
| gh repo archive | 归档仓库 | gh repo archive owner/repo |
| gh repo autolink | 管理自动链接引用 | gh repo autolink list |
| gh repo autolink create | 创建自动链接引用 | gh repo autolink create --key TRELLO --url-template ‘...’ |
| gh repo autolink delete | 删除自动链接引用 | gh repo autolink delete <id> |
| gh repo autolink list | 列出自动链接引用 | gh repo autolink list |
| gh repo autolink view | 查看自动链接引用 | gh repo autolink view <id> |
| gh repo clone | 克隆仓库 | gh repo clone owner/repo |
| gh repo create | 创建新仓库 | gh repo create my-proj --public --push |
| gh repo delete | 删除仓库 | gh repo delete owner/repo |
| gh repo deploy-key | 管理部署密钥 | gh repo deploy-key list |
| gh repo deploy-key add | 添加部署密钥 | gh repo deploy-key add --title “服务器” --key ./key.pub |
| gh repo deploy-key delete | 删除部署密钥 | gh repo deploy-key delete <id> |
| gh repo deploy-key list | 列出部署密钥 | gh repo deploy-key list |
| gh repo edit | 编辑仓库属性 | gh repo edit --description “新描述” |
| gh repo fork | Fork 一个仓库 | gh repo fork owner/repo --clone |
| gh repo gitignore | 查看 .gitignore 模板 | gh repo gitignore list |
| gh repo gitignore list | 列出可用 .gitignore 模板 | gh repo gitignore list |
| gh repo gitignore view | 查看特定 .gitignore 模板 | gh repo gitignore view Node |
| gh repo license | 查看许可证模板 | gh repo license list |
| gh repo license list | 列出可用许可证模板 | gh repo license list |
| gh repo license view | 查看特定许可证模板 | gh repo license view MIT |
| gh repo list | 列出仓库 | gh repo list org-name |
| gh repo rename | 重命名仓库 | gh repo rename new-name |
| gh repo set-default | 设置默认仓库 | gh repo set-default owner/repo |
| gh repo sync | 同步 Fork 的仓库 | gh repo sync |
| gh repo unarchive | 取消仓库归档 | gh repo unarchive owner/repo |
| gh repo view | 查看仓库信息 | gh repo view owner/repo --web |

### GitHub Actions 命令

这些命令用于管理和交互 GitHub Actions。

| 命令 | 作用 | 典型用法 |
| --- | --- | --- |
| **gh cache** | 管理 Actions 缓存 | gh cache list |
| gh cache delete | 删除 Actions 缓存 | gh cache delete <cache-id> |
| gh cache list | 列出 Actions 缓存 | gh cache list --ref refs/heads/main |
| **gh run** | 管理工作流运行 | gh run list |
| gh run cancel | 取消一个工作流运行 | gh run cancel 123456 |
| gh run delete | 删除工作流运行记录 | gh run delete 123456 |
| gh run download | 下载运行产生的构件 | gh run download 123456 -n artifact-name |
| gh run list | 列出工作流运行记录 | gh run list --workflow CI |
| gh run rerun | 重新运行一个工作流 | gh run rerun 123456 --failed |
| gh run view | 查看工作流运行详情 | gh run view 123456 --log |
| gh run watch | 实时查看运行日志 | gh run watch 123456 |
| **gh workflow** | 管理工作流 | gh workflow list |
| gh workflow disable | 禁用工作流 | gh workflow disable “CI” |
| gh workflow enable | 启用工作流 | gh workflow enable “CI” |
| gh workflow list | 列出仓库工作流 | gh workflow list |
| gh workflow run | 手动触发工作流 | gh workflow run “CI” --ref main |
| gh workflow view | 查看工作流定义 | gh workflow view “CI” --yaml |

### 附加命令 (Additional Commands)

这些命令提供扩展功能、配置和底层操作。

| 命令 | 作用 | 典型用法 |
| --- | --- | --- |
| **gh agent-task** | 管理代号为“agent-task”的功能 | gh agent-task list |
| **gh alias** | 管理命令别名 | gh alias set co ‘pr checkout’ |
| gh alias delete | 删除别名 | gh alias delete co |
| gh alias import | 从文件导入别名 | gh alias import < aliases.yml |
| gh alias list | 列出所有别名 | gh alias list |
| gh alias set | 设置别名 | gh alias set bugs ‘issue list --label bug’ |
| **gh api** | 直接调用 GitHub API | gh api repos/octocat/hello-world |
| **gh attestation** | 管理证明材料 (Attestations) | gh attestation download |
| gh attestation download | 下载证明材料 | gh attestation download --owner org --repo repo --bundle <file> |
| gh attestation trusted-root | 管理可信根证书 | gh attestation trusted-root get |
| gh attestation verify | 验证证明材料 | gh attestation verify --bundle <file> |
| **gh completion** | 生成 Shell 自动补全脚本 | gh completion -s zsh |
| **gh config** | 管理 CLI 配置 | gh config set editor “code -w” |
| gh config clear-cache | 清除内部缓存 | gh config clear-cache |
| gh config get | 获取配置项 | gh config get editor |
| gh config list | 列出所有配置 | gh config list |
| gh config set | 设置配置项 | gh config set pager ‘less -FRX’ |
| **gh copilot** | GitHub Copilot 相关功能（实验性） | gh copilot |
| **gh extension** | 管理扩展 | gh extension install user/extension |
| gh extension browse | 在浏览器中打开扩展仓库 | gh extension browse |
| gh extension create | 创建新的扩展模板 | gh extension create my-ext |
| gh extension exec | 直接执行扩展命令 | gh extension exec user/extension |
| gh extension install | 安装扩展 | gh extension install dlvhdr/gh-dash |
| gh extension list | 列出已安装扩展 | gh extension list |
| gh extension remove | 卸载扩展 | gh extension remove user/extension |
| gh extension search | 搜索扩展 | gh extension search “dashboard” |
| gh extension upgrade | 升级扩展 | gh extension upgrade --all |
| **gh gpg-key** | 管理 GPG 密钥 | gh gpg-key list |
| gh gpg-key add | 添加 GPG 密钥 | gh gpg-key add ./key.asc |
| gh gpg-key delete | 删除 GPG 密钥 | gh gpg-key delete <key-id> |
| gh gpg-key list | 列出 GPG 密钥 | gh gpg-key list |
| **gh label** | 管理标签 | gh label list |
| gh label clone | 克隆标签到其他仓库 | gh label clone owner/source-repo --repo owner/target-repo |
| gh label create | 创建新标签 | gh label create “priority:high” --color “ff0000” |
| gh label delete | 删除标签 | gh label delete “priority:high” |
| gh label edit | 编辑标签 | gh label edit “bug” --name “Bug” --color “d73a49” |
| gh label list | 列出仓库标签 | gh label list |
| **gh licenses** | 查看开源许可证 | gh licenses list |
| **gh preview** | 预览实验性功能 | gh preview <command> |
| **gh ruleset** | 管理仓库规则集 | gh ruleset list |
| gh ruleset check | 检查规则集与分支的匹配 | gh ruleset check --branch feature |
| gh ruleset list | 列出仓库规则集 | gh ruleset list |
| gh ruleset view | 查看规则集详情 | gh ruleset view <id> |
| **gh search** | 搜索 GitHub | gh search code “function main()” |
| gh search code | 搜索代码 | gh search code “console.log” --repo owner/repo |
| gh search commits | 搜索提交 | gh search commits “fix bug” --author octocat |
| gh search issues | 搜索议题 | gh search issues “label:bug is:open” |
| gh search prs | 搜索拉取请求 | gh search prs “is:merged reviewed-by:@me” |
| gh search repos | 搜索仓库 | gh search repos “topic:cli” |
| **gh secret** | 管理 Actions 仓库/组织密钥 | gh secret list |
| gh secret delete | 删除密钥 | gh secret delete API\_TOKEN |
| gh secret list | 列出密钥 | gh secret list |
| gh secret set | 设置密钥 | gh secret set API\_TOKEN -b “my-secret-value” |
| **gh ssh-key** | 管理 SSH 密钥 | gh ssh-key list |
| gh ssh-key add | 添加 SSH 密钥 | gh ssh-key add --title “MacBook” --key ./id\_ed25519.pub |
| gh ssh-key delete | 删除 SSH 密钥 | gh ssh-key delete <key-id> |
| gh ssh-key list | 列出 SSH 密钥 | gh ssh-key list |
| **gh status** | 显示用户状态（如提及、议题、PR等） | gh status |
| **gh variable** | 管理 Actions 仓库/组织变量 | gh variable list |
| gh variable delete | 删除变量 | gh variable delete ENV |
| gh variable get | 获取变量值 | gh variable get ENV |
| gh variable list | 列出变量 | gh variable list |
| gh variable set | 设置变量 | gh variable set ENV -b “production” |

**全局选项**（适用于所有 gh 命令）:

* --version: 显示 CLI 版本。
* --help: 显示任何命令的帮助信息。

此速查表整合了 GitHub CLI (gh) 的全部功能，覆盖日常开发、协作、自动化及系统管理的绝大多数场景。遇到具体参数疑问时，可随时使用 gh <command> --help 获取最详细的官方说明。

内容由AI生成仅供参考
