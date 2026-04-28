# 给 minichat 加了图片和表情支持

最近和朋友在微信上聊点“不可描述”的东西，越聊越觉得不太安全，想着找个匿名聊天室，简单点、匿名点、隐私别太差的那种。

本来想自己撸一个，反正 Cursor 也开着不用白不用。但既然在 L 站，咱就得先白嫖一波！

一搜，还真有现成的，体验还挺不错，就是L站佬 "hahahaha" 写的这个：[minichat](https://github.com/byebyehair/minichat)

---

用了几天，感觉挺顺手的，就是有点小遗憾：**不能发图片，也没有表情**。

看了下 issue，确实有人提过，但还没排上优先级。那就自己动手搞一下吧。

开干！Cursor + Tera + Copilot 一起上，一个下午，搞定！

---

## 改了些啥？

- 支持发图片消息 ✅  
- 加了默认表情库，聊天更生动 ✅  
- 写了个一键打包脚本 `build.sh` ✅  
- 调了点主题样式  
- 修改了一些代码逻辑

👉 [改进版下载地址](https://github.com/CJSen/minichat/releases/tag/v1.0.0)

---

## 效果图

<img width="601" alt="Image" src="https://github.com/user-attachments/assets/8e8cb29e-4786-4f66-ab92-2f9c2190f3a0" />

---

## 最后

再次感谢L站佬 "hahahaha" 开源了这么一个好用的项目！

这个小改版如果对你有用，欢迎给我和原项目都点个 star～  
有建议欢迎提 issue 或直接来个 PR，一起完善～