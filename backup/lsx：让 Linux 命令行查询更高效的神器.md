# lsx：让 Linux 命令行查询更高效的神器

> 记录一次二次开发 CLI 工具的心路历程，顺便安利下这个小而美的项目--[lsx](https://github.com/CJSen/lsx)

---

## 1. 为什么会有 [lsx](https://github.com/CJSen/lsx)？

作为一个常年混迹在 Linux/Macos 终端的用户，命令行速查一直是刚需。自带的man命令，全英文，阅读难；原本用的是 [pls](https://github.com/chenjiandongx/pls)，但随着时间推移，原项目多年未更新维护，命令数据老旧，查询需要多打一个`show` 二级命令，每次想同步最新的 [linux-command](https://github.com/jaywcjlove/linux-command) 数据都很麻烦。

于是，基于pls源代码，撸了个二开的 lsx 项目，主打“轻量、易用、数据新”，让命令速查这件事变得更丝滑。

---

## 2. lsx 有啥特别的？

- **命令速查**：一句 `lsx your-cmd`，立刻查到详细用法和示例，支持关键字搜索。
- **数据实时更新**：一键 `lsx upcommands && lsx upgrade`，命令库永远保持最新。
- **多平台支持**：Linux、macOS、Windows，amd64/arm64 架构全覆盖。
- **自定义配置**：支持 YAML 配置文件，数据目录/远程源/输出方式随心调。
- **less 分页**：输出太长？配置 `useLess: true`，自动分页浏览。
- **极简依赖**：Go 语言开发，单文件可执行，开箱即用。

---

## 3. 怎么用？

1. [下载最新版二进制](https://github.com/CJSen/lsx/releases)，解压后赋予执行权限，建议放到 `/usr/local/bin` 等可执行目录下，方便全局调用。
2. 初始化命令库（首次使用建议联网）：
   ```bash
   lsx upcommands && lsx upgrade
   ```
3. 速查命令用法：
   ```bash
   lsx grep
   lsx show curl  // 当useShow配置为true时(默认false)，可是用此二级命令。lsx xxx将失效。
   lsx search 文件
   ```
4. 配置文件自定义（可选）：
   ```yaml
   dataDir: "/Users/yourname/.lsx"
   remoteBaseUrl: "https://unpkg.com/linux-command@latest"
   useShow: false
   useLess: true
   ```
   并通过 `export LSXCONFIG=/path/to/lsx.yaml` 指定配置。

---

## 4. 适合谁用？

- Linux/Unix/Mac 终端党
- DevOps/运维/开发/学生
- 喜欢极简、开源、可自定义工具的你

---

## 5. 预览

<img width="601" alt="Image" src="https://raw.githubusercontent.com/CJSen/cjsen.github.io/main/static/images/lsx-cmd.gif" />
<img width="601" alt="Image" src="https://raw.githubusercontent.com/CJSen/cjsen.github.io/main/static/images/lsx-search.gif" />

```shell
~ lsx -h
Impressive Linux commands cheat sheet cli.

Usage:
  lsx [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  help        Help about any command
  search      Search command by keywords
  show        Show the specified command usage.
  upcommands  Update the embedded linux-command.json to the latest version.
  upgrade     Upgrade all commands from remote.
  version     Prints the version about lsx

Flags:
  -h, --help   help for lsx

Use "lsx [command] --help" for more information about a command.
```


## 6. 开发&致谢

lsx 基于 [pls](https://github.com/chenjiandongx/pls) 二次开发，数据源感谢 [linux-command](https://github.com/jaywcjlove/linux-command)。

项目完全开源，欢迎提 issue、PR 或点个 star 支持！

> 让命令行更高效，生活更简单。

[lsx项目地址](https://github.com/CJSen/lsx)

如果对大家有用的话，麻烦点点stars～感谢！