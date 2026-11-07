# 发布到个人 GitHub 仓库

> 从自己的 GitHub 仓库分发 Dify 插件，用户通过仓库 URL 直接安装，无需 Marketplace 审核

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/publishing/marketplace-listing/release-to-individual-github-repo.md)。

通过个人 GitHub 仓库发布，可在不经过 Dify Marketplace 审核的情况下交付插件。用户只需输入仓库 URL，并选择一个包含 `.difypkg` 资产的发布版本即可安装插件。

以下场景适合使用这种方式：

* 你希望完全掌控版本管理和发布节奏。
* 插件是开源的，你希望他人能够阅读、复刻或参与贡献。
* 插件供团队或组织内部使用，但你仍想提供一个统一的安装 URL。
* 插件正在等待 Marketplace 审核，你需要一个临时的分发渠道。

如需与其他发布方式对比，详见 [发布概述](../%E5%8F%91%E5%B8%83%E6%8F%92%E4%BB%B6.md)。

## 准备工作

* 一个打包好的插件（`.difypkg` 文件）。如果还没有，详见 [打包为本地文件并分享](../%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6/%E6%89%93%E5%8C%85%E4%B8%BA%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6%E5%B9%B6%E5%88%86%E4%BA%AB.md)。
* 一个 GitHub 账户。
* 一个 Dify 工作空间，且你（或你的用户）拥有安装插件的权限。

## 第 1 步：创建 GitHub 仓库

**1. 创建仓库**

在 GitHub 上新建一个公开仓库。仓库名称通常与插件名称一致（例如 `dify-plugin-flomo`）。

**2. 推送插件源代码**

在插件项目中初始化 git，并推送源代码：

```bash theme={null}
cd your_plugin_project
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/<your-handle>/<repo-name>.git
git push -u origin main
```

**3. 确认清单文件**

`manifest.yaml` 以及所有 `provider/*.yaml` 中的 `author` 字段必须与你的 GitHub 用户名一致。不一致会导致用户安装时出现 `plugin_unique_identifier is not valid`。清单文件的详细信息，详见 [通用规范](../../%E7%89%B9%E6%80%A7%E4%B8%8E%E8%A7%84%E8%8C%83/%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83.md)。

## 第 2 步：构建插件包

在插件项目的 **上一级** 目录中运行：

```bash theme={null}
dify plugin package ./your_plugin_project
```

这会在当前目录生成 `your_plugin_project.difypkg`。

## 第 3 步：发布 GitHub Release

Dify 通过 GitHub release 发现插件的可安装版本。

**1. 标记发布版本**

在仓库页面点击 **Releases** > **Draft a new release**。使用语义化版本创建一个新标签（例如 `v0.0.1`）。标签应与 `manifest.yaml` 中的 `version` 字段一致。

**2. 附加 .difypkg 文件**

在发布表单中，将 `.difypkg` 文件拖入 **Assets** 区域。用户从你的仓库安装时，Dify 会读取该资产。

**3. 发布**

添加发布说明，描述本次更新内容，然后点击 **Publish release**。

> [!TIP]
>
> 每发布一个新版本，都需要重复第 2 步和第 3 步。先在 `manifest.yaml` 中提升 `version`，重新打包，再创建新标签和发布版本。

## 第 4 步：从你的仓库安装

将仓库 URL 分享给用户。他们在 Dify 中按以下步骤安装：

**1. 打开插件页面**

在 Dify 中，点击右上角的 **插件**。

**2. 从 GitHub 安装**

点击 **安装插件** > **从 GitHub 安装**。

**3. 输入仓库信息**

粘贴仓库 URL（例如 `https://github.com/<your-handle>/<repo-name>`），然后从下拉菜单中选择版本。Dify 会从该发布版本中拉取匹配的 `.difypkg` 资产。

**4. 确认安装**

查看插件请求的权限，然后点击 **安装**。

> [!TIP]
>
> 点击 **安装** 后数秒内，插件即会出现在用户的插件页面。Dify 会按需从你的 GitHub release 拉取 `.difypkg`。

## 故障排查

* **`plugin_unique_identifier is not valid`**：`manifest.yaml`（以及 `provider/*.yaml`）中的 `author` 字段与仓库所属的 GitHub 用户名不一致。更新该字段，重新打包并重新发布。
* **安装对话框中不显示任何版本**：发布版本未附加 `.difypkg` 资产，或仓库尚无任何发布版本。在 GitHub 上打开该发布版本，确认资产已列在 **Assets** 下。
* **签名验证错误**：自部署 Dify 实例可能启用了签名验证。为发布版本签名，详见 [第三方签名验证](../%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6/%E4%B8%BA%E7%AC%AC%E4%B8%89%E6%96%B9%E7%AD%BE%E5%90%8D%E9%AA%8C%E8%AF%81%E7%AD%BE%E7%BD%B2%E6%8F%92%E4%BB%B6.md)；绕过方式详见 [常见问题](../%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.md)。

## 相关资源

* [发布概述](../%E5%8F%91%E5%B8%83%E6%8F%92%E4%BB%B6.md)：对比各种发布方式。
* [打包为本地文件并分享](../%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6/%E6%89%93%E5%8C%85%E4%B8%BA%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6%E5%B9%B6%E5%88%86%E4%BA%AB.md)：构建 `.difypkg` 包。
* [发布插件到 Marketplace](../%E5%8F%91%E5%B8%83%E6%8F%92%E4%BB%B6%E5%88%B0%20Marketplace.md#准备软件包)：准备并验证用于官方 Marketplace 的软件包。
* [第三方签名验证](../%E6%9C%AC%E5%9C%B0%E6%96%87%E4%BB%B6/%E4%B8%BA%E7%AC%AC%E4%B8%89%E6%96%B9%E7%AD%BE%E5%90%8D%E9%AA%8C%E8%AF%81%E7%AD%BE%E7%BD%B2%E6%8F%92%E4%BB%B6.md)：为软件包签名以实现已验证安装。
* [通用规范](../../%E7%89%B9%E6%80%A7%E4%B8%8E%E8%A7%84%E8%8C%83/%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83.md)：清单文件字段参考。
