记录一次使用 OpenSpec 为 minichat 增加特性的实践笔记

minichat 是我二开的一个私密聊天室，之前给它加了图片和表情发送功能。但因为使用很少，基本没有用户反馈，所以也就很久没更新。

最近再次使用时发现了两个问题：

- 发送图片后，查看大图时仍显示缩略图，导致大图无法看清；
- 切换网络时容易断线（客户端不保留聊天数据且退出后清空），重连体验差，影响使用感受。

计划对它做一次小更新。第一个问题已经悄悄修好了（忘记记录了），第二个问题我打算借此机会体验一下 OpenSpec 的工作流并记录过程。

**关于 OpenSpec**

[OpenSpec](https://github.com/Fission-AI/OpenSpec) 是一个面向 AI 编码助手的规范驱动开发框架，支持 Cursor、Codex、Claude Code 等工具。相比其他工具，它通过轻量级的规范流程，让人和 AI 在编写代码前就对要做的事情达成一致，适合在已有项目上渐进式增加新功能。

安装：

```bash
npm install -g @fission-ai/openspec@latest
```

使用过程（我个人实践的步骤）

1. 初始化

在项目根目录运行 `openspec init`，按照交互完成配置后，会在项目里生成若干 OpenSpec 相关目录和文件。我选择的编辑器是 OpenCode。下面是初始化后的界面截图：

![1776778113220](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776778113220.png)

2. 探索流程的选择

使用中有个疑问：应该从 `/openspec-explore` 开始，还是直接从 `/openspec-propose` 开始？

简要区分：

- `/openspec-explore`：当你对项目或某个功能还不熟，需要先“读懂”代码和现状时使用，适合接手陌生项目、排查实现细节、评估改动影响等；
- `/openspec-propose`：在明确目标后用于提出功能升级、架构调整、API 改造或新增能力等。

在和 AI 交流后，我决定从 `/openspec-explore` 开始：

![1776779840619](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776779840619.png)

3. 我用的探索 prompt（示例）

```
/opsx-explore minichat 项目中，聊天室创建/连接/断线处理机制是如何实现的？包括：
- 使用的协议
- 房间/会话如何存储
- 如何保证隐私
- 断开连接后服务端如何处理
- 前端是否有重连逻辑
```
![1776834754070](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776834754070.png)
（中间的思考与输出就不截图了,贴个开头和结果）

4. 进入 `/opsx-propose`

在有了探索上下文后，进入 `/opsx-propose`，OpenSpec 会生成对应的策划与约束文件，通常会产生一个 `tasks.md`，把接下来的工作分成若干可执行的步骤：

![1776835023459](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776835023459.png)
![1776835038485](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776835038485.png)

5. `/opsx-apply`：按任务执行

按 `tasks.md` 的步骤交给 AI 去执行，我这儿是边看边改，期间喝了杯 82 年的咖啡，等待 AI 输出。

![1776835277852](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776835277852.png)

6. 测试

因为是聊天功能，我主要做了手工测试，验证断线重连逻辑在不同网络切换（例如切换节点、Wi‑Fi 切换）下的表现。

7. 修复与迭代

根据测试结果，和 AI 进行了几轮对话，对出现的问题进行了修复和微调（此处略）。

8. 归档

完成后使用 `/opsx-archive` 将本次变更归档，保存完整的工作内容和文件：

![1776836023105](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776836023105.png)

总结：

一次简短的 OpenSpec 流程体验结束。通过这次流程，我把 minichat 的断线重连功能强化了（例如在切换节点或 Wi‑Fi 时的重连策略有所改善），同时对整个人机协作的开发流程有了更直观的认识。

![1776836197632](https://github.com/CJSen/cjsen.github.io/blob/main/backup/image/使用openspec为minichat更新新特性/1776836197632.png)
