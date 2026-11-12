# 来源与范围

- Wiki：WorkBuddy
- 规范来源：<https://www.workbuddy.cn/docs>
- 语言 / 版本：与来源链接一致
- 抓取范围：workbuddy.cn/docs 五个板块（workbuddy 桌面端、workbuddyapp 手机 App、workbuddymini 小程序、enterprise 企业版、/docs 首页）
- 当前快照：已完整覆盖全部公开可访问文档，共 136 篇；精确覆盖数与最近一次有变化的同步时间见 `wiki-manifest.json`
- 快照边界：enterprise 板块的 26 篇后台管理文档需登录才可见（未登录时站点统一重定向到企业版“产品概述”），无法公开抓取，已记入 `inventory.json` 的 `coverage.excluded`；另有 5 个板块首页 / `/docs` 为其 Overview 的重定向副本，同样排除。企业版本板块仅收录公开的“产品概述”。
- 正文截图仍指向上游 CDN（`download.codebuddy.cn`，约 646 张、总量约 1.6GB），未打包进本地，离线时图片不可见，但文字与结构完整
- 上游许可：未确认；仅限本地使用，公开分发前必须核对

离线快照可能落后于上游。许可证不明或不允许再分发时，本 Skill 仅限用户授权的本地使用，不应提交到公开仓库或发布到市场。
