

> 记录一次为 AstrBot 写插件的经历，顺便安利下这个自动推送新闻的小工具

---

## 1. 为什么要做这个插件？

群聊里总有人问“今天有什么大新闻？”手动转发太麻烦，爬新闻又怕漏掉重点。正好 AstrBot 支持插件，于是就有了这个 `astrbot_plugin_daliy_60s_news` —— 每天自动推送 60 秒新闻，文本/图片随你选，群友再也不会错过热点。

---

## 2. 插件亮点

astrbot_plugin_daily_60s_news 是一个为  [AstrBot](https://github.com/AstrBotDevs/AstrBot)  设计的每日 60 秒新闻插件。该插件可自动或手动推送每日新闻（文本或图片）到指定群组，帮助群成员快速获取当天要闻
- **自动推送**：定时把当天 60 秒新闻（文本/图片）发到指定群聊，完全不用操心
- **命令获取**：支持 `/新闻 news`、`/新闻 text`、`/新闻 image` 等命令，随时查当天要闻
- **管理员功能**：一键手动推送、清理过期新闻、查询插件状态
- **多平台兼容**：理论上支持 AstrBot 目前所有平台（QQ、微信、TG、钉钉等）
- **缓存优化**：自动下载并缓存新闻内容，节省流量，响应更快
- **开源可改**：代码清晰，方便魔改和二次开发

---

## 3. 怎么用？

1. 克隆插件到 AstrBot 的 `/data/plugin/` 目录：
   ```bash
   git clone https://github.com/CJSen/astrbot_plugin_daliy_60s_news.git
   ```
2. 进入 AstrBot 网页插件配置界面，按需调整参数并保存。
3. 配置群聊 ID（/sid 获取），支持多平台多群聊。
4. 插件启动后，新闻会自动推送到配置的群聊。
5. 常用命令：
   - `/新闻 news` `/新闻 早报` `/新闻 新闻`：获取今日新闻（文本/图片）
   - `/新闻 text`：只要文本
   - `/新闻 image`：只要图片
   - `/新闻 status`：查插件状态（管理员）
   - `/新闻 clean`：清理过期新闻（管理员）
   - `/新闻 push`：手动推送（管理员）
  ![命令](https://github.com/CJSen/astrbot_plugin_daliy_60s_news/raw/master/static/image.png)

---

## 4. 适合谁用？

- 各类群聊机器人管理员
- 想让群友每天都能看到新鲜资讯的你
- 喜欢自动化、开源、可自定义工具的你

---

## 5. 开发&致谢

部分代码参考自 [anka-afk/astrbot_plugin_daily_news](https://github.com/anka-afk/astrbot_plugin_daily_news)。

项目完全开源，欢迎提 issue、PR 或点个 star 支持！

> 让群聊更有温度，信息更高效。

[项目地址](https://github.com/CJSen/astrbot_plugin_daliy_60s_news)
