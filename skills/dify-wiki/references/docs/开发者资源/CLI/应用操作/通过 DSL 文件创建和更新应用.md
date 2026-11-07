# 通过 DSL 文件创建和更新应用

> 用 difyctl 通过 DSL 文件更新 Dify 应用，再发布或回滚，从文件或应用包创建应用，并修改 Web 应用设置

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cli/create-and-update-apps-from-dsl-files.md)。

> [!TIP]
>
> 要交给编码 Agent 来做，先 [为它配置好 `difyctl` Skill](https://docs.dify.ai/zh/cli/get-started#配置编码-agent)，再把这个页面发给它。

## 开始之前

* 用来导出文件的应用和待更新的应用，都需开启服务 API 访问。

* 如果应用分别在两台 Dify 服务器上，把 `DIFY_CONFIG_DIR` 设为各自单独的目录，再 [分别登录](../%E7%AE%A1%E7%90%86%20difyctl/%E7%AE%A1%E7%90%86%E7%99%BB%E5%BD%95.md#使用多个服务器或账户)。然后分别用这两个目录运行 `difyctl version`，确认两台服务器的版本都与你的 `difyctl` 一致。

  > [!NOTE]
  >
  > 每条命令操作的是哪台服务器上的应用，就用那台服务器的目录运行。

* 如果应用分别在两个工作空间中 Cloud，把 `difyctl` [切换](../%E7%AE%A1%E7%90%86%20difyctl/%E7%AE%A1%E7%90%86%E7%99%BB%E5%BD%95.md#switch-your-workspace) 到待更新应用所在的工作空间。另一个工作空间中的应用，仍可用它的 `--app-id` 导出。要查到这个 ID，给 `get console_app` 加上另一个工作空间的 `--workspace-id`。

## 更新应用

只有 Workflow 和 Chatflow 应用能通过文件更新。其他类型的应用，改为 [用文件新建一个](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#通过-dsl-文件创建应用)。

更新后，应用的 Web 应用 URL 和 API 密钥保持不变（[还会保留哪些内容](../../../%E4%BD%BF%E7%94%A8/%E5%B7%A5%E4%BD%9C%E7%A9%BA%E9%97%B4/%E5%AF%BC%E5%87%BA%E5%92%8C%E5%AF%BC%E5%85%A5%E5%BA%94%E7%94%A8.md#update-an-existing-app)）。导入会替换应用的草稿，尚未发布的改动也包括在内。新的工作流要等你发布后才生效。

> [!TIP]
>
> 要在流水线中执行这些步骤，还可参考 [在 CI 和自动化中使用 `difyctl`](https://docs.dify.ai/zh/cli/scripts-and-ci)，其中介绍了任务如何登录、出错时如何停下。

**1. 查找应用 ID**

列出你的应用，记下待更新应用的 `id`；如果要从其他应用导出文件，也记下那个应用的 `id`：

```bash theme={null}
difyctl get console_app
```

本页示例从经过测试的副本 Order Status (staging) 导出文件，用它更新生产环境中的应用 Order Status：

```json theme={null}
{
  "data": [
    {
      "id": "9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d",
      "name": "Order Status",
      "mode": "workflow",
      …
    },
    {
      "id": "5c1e8f2a-7b3d-4e9a-8f6c-2d4b1a9e7c3f",
      "name": "Order Status (staging)",
      "mode": "workflow",
      …
    },
    …
  ],
  …
}
```

**2. 获取文件**

如果 [DSL 文件](../../../%E5%AD%A6%E4%B9%A0/%E6%A0%B8%E5%BF%83%E6%A6%82%E5%BF%B5.md#dify-dsl) 已经存放在 Git 中，直接跳到第 3 步。否则，从另一个应用导出文件，例如待更新应用经过测试的副本。

首先，在那个应用中把 [Web 应用设置](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#修改-web-应用和应用信息)（例如标题）改成用户应当看到的样子。文件会带上这些设置，导入后用户会立刻看到。

然后导出那个应用的线上版本，即 `get console_app version` 中标为 `current: true` 的版本：

```bash theme={null}
V=$(difyctl get console_app version --app-id 5c1e8f2a-7b3d-4e9a-8f6c-2d4b1a9e7c3f | jq -r '.data[] | select(.current) | .id')
difyctl export console_app dsl --app-id 5c1e8f2a-7b3d-4e9a-8f6c-2d4b1a9e7c3f --workflow-id $V | jq -r .data > order-status.yml
```

要改为导出它尚未发布的改动，去掉 `--workflow-id` 即可。

导出时，Secret 值一律留空。只有当待更新的应用要用这个应用的 Secret 值替换自己的值时，才加上 `--include-secret`。这样导出的文件以明文保存这些值，不要放进 Git，也不要放到任何会共享出去的地方。

如果待更新的应用在另一个工作空间或另一台服务器上，导入后每个知识检索节点都会丢失关联的知识库。要保留关联，把文件中该节点 `dataset_ids` 下的 ID 换成目标工作空间或服务器上知识库的 ID。这些 ID 可在那边运行 `get knowledge_base` 查到。

**3. 检查文件**

```bash theme={null}
difyctl check console_app dsl --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --yaml-content "$(cat order-status.yml)"
```

如果结果中有 `valid: true`，导入就会接受这个文件。否则，找出 `severity` 为 `error` 的每个问题，按它的 `loc` 定位到对应的节点和字段并修正，再检查一遍。

`severity` 为 `warning` 的问题不会阻止导入。这类问题提示缺少某个凭据或模型，到第 5 步再配置即可。

**4. 导入文件**

先读取应用的草稿哈希值，再带上它导入文件。带上哈希值后，如果有人在此期间改动了草稿，导入会被拒绝，不会覆盖对方的改动。

> [!WARNING]
>
> 一导入，文件中的名称、描述、图标和 Web 应用设置就会立即替换应用原有的内容，**即使还没有发布**。

要保留应用原有的名称和描述，用 `--name` 和 `--description` 传入。如果文件中的图标或 Web 应用设置不适合这个应用，导入后立即 [修改](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#修改-web-应用和应用信息)。

```bash theme={null}
H=$(difyctl export console_app dsl --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d | jq -r .draft_hash)
difyctl import console_app dsl --mode yaml-content --yaml-content "$(cat order-status.yml)" \
  --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --draft-hash $H --name "Order Status" --description "汇总订单的状态。"
```

导入成功时返回 `status: completed`，也可能返回 `completed-with-warnings` 并附上警告，继续之前先读一读这些警告。未成功时：

* 如果读取哈希值之后草稿有了改动，导入会被拒绝，退出码为 1：`The draft changed after it was exported.`

  到工作室中查看草稿改了什么。

  * 如果这些改动可以丢弃，重新读取哈希值，再次导入：导入会替换掉这些改动。
  * 如果需要保留，在文件中或导出文件的那个应用中做同样的改动，再从第 2 步重新开始。

* 如果文件的 DSL `version` 比服务器支持的版本新，`status` 为 `pending`。如仍要导入，[运行结果中的提示](../%E6%9F%A5%E6%89%BE%E5%B9%B6%E8%BF%90%E8%A1%8C%E5%91%BD%E4%BB%A4.md#按提示运行后续命令)，即 `confirm console_app dsl_import`。

* 如果文件无效，导入会被拒绝，退出码为 1。按第 3 步检查文件，修正检查报出的问题，再次导入。

遇到其他错误，到 [故障排查](../%E5%8F%82%E8%80%83/%E7%BB%93%E6%9E%9C%E3%80%81%E9%94%99%E8%AF%AF%E4%B8%8E%E9%80%80%E5%87%BA%E7%A0%81.md#故障排查) 中查看处理方法。

要丢弃导入的工作流，[把线上版本恢复到草稿中](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#回滚更新)。它本来就是线上版本，无需发布。

**5. 安装缺少的集成**

即使工作空间缺少文件用到的某个集成，文件也能通过检查并成功导入。在导入后 10 分钟内列出缺少的集成，过了这个时间，返回的列表就是空的：

```bash theme={null}
difyctl check console_app dependency --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d
```

要从 Marketplace 安装某个集成，[运行它对应的提示](../%E6%9F%A5%E6%89%BE%E5%B9%B6%E8%BF%90%E8%A1%8C%E5%91%BD%E4%BB%A4.md#按提示运行后续命令)。在第 7 步测试之前，到工作室中为需要凭据的集成添加凭据。

**6. 设置环境变量**

导入后，应用的环境变量取的是文件中的值。有些变量在这个应用里应该取别的值，例如它调用的 API 地址，这些要重新设置。

列出应用的环境变量。保留了这个应用原有值的 Secret 变量显示为一串星号，空的显示为 `""`：

```bash theme={null}
difyctl get console_app env --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d
```

把变量的 `id` 传给 `--env-id`，逐一设置需要修改的值，空的 Secret 变量也要设置：

```bash theme={null}
# Secret 变量：从 Shell 变量读取值，免得它留在 Shell 历史记录中
difyctl set console_app env --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --env-id 2a7c4e9b-6d1f-4b3a-9e8c-5f0d1a2b3c4d --name ORDERS_API_KEY --value "$ORDERS_API_KEY" --value-type secret

# 普通值
difyctl set console_app env --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --env-id 6f3b8d1e-4c2a-4e7f-a9b5-0d8c7e6f5a4b --name API_BASE_URL --value "https://orders.example.com/api" --value-type string
```

**7. 测试草稿**

用一组典型的输入运行一次草稿。测试用的是这个应用的环境变量，例如它真实的 API 密钥，所以要选真实运行也无妨的输入。`describe console_app` 可查看 [应用接受哪些输入](%E8%BF%90%E8%A1%8C%E5%BA%94%E7%94%A8.md#查看应用的输入变量)。

```bash theme={null}
difyctl test console_app workflow --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --inputs '{"topic": "order 1042"}'
```

Chatflow 应用改用 `test console_app advanced_chat`。

运行完成时，结果中为 `status: ended`；失败时为 `status: failed`，原因见 `error.message`。在文件中或导出文件的那个应用中修正工作流，再从第 2 步重新开始。

如果 DSL 版本较新的文件无法在这台服务器上运行，改为 [把线上版本恢复到草稿中](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#回滚更新)。该版本已在线上，不必再发布。

**8. 确认草稿可以发布**

```bash theme={null}
difyctl check console_app release --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d
```

`ready: true` 表示草稿有效，且通过了最近一次测试。

如果 `ready` 为 `false`，[按结果中的提示操作](../%E6%9F%A5%E6%89%BE%E5%B9%B6%E8%BF%90%E8%A1%8C%E5%91%BD%E4%BB%A4.md#按提示运行后续命令)，再检查一遍。

如果重新运行测试后 `ready` 仍为 `false`，说明测试中有节点失败，但该节点设置了 **异常处理**，运行照常完成。要找出这个节点，用 `run_id` 来 [查看这次测试运行](%E8%BF%90%E8%A1%8C%E5%BA%94%E7%94%A8.md#排查运行失败的原因)。

* 如果这个节点本不该失败，在文件中或导出文件的那个应用中修正它，再从第 2 步重新开始。
* 如果工作流本就设计为处理这种失败，换一组任何节点都不会失败的输入来测试。

发布前，查看 `changes`，了解草稿与已发布版本有哪些不同。

**9. 发布**

```bash theme={null}
difyctl publish console_app --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --marked-name v2
```

## 回滚更新

如果已发布的更新出了问题，列出应用的已发布版本，按 `id` 把之前的某个版本恢复到草稿中，再发布。这个版本以前上线过，所以可以跳过测试和就绪检查。

恢复会替换草稿。要保留草稿，先不带 `--workflow-id` 把它导出。

```bash theme={null}
difyctl get console_app version --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d

difyctl restore console_app version --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --version-id 8e1d3c5a-2b4f-4a6e-9c7d-1f0b2a3c4d5e

difyctl publish console_app --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d
```

环境变量会恢复为该版本的值，名称、描述、图标和 Web 应用设置则保持导入时的样子。要把这些也改回去，[手动修改](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#修改-web-应用和应用信息)。

## 通过 DSL 文件创建应用

导入文件时不带 `--app-id`，即可新建一个与文件同类型的应用，并用 `--name` 为它命名：

```bash theme={null}
difyctl import console_app dsl --mode yaml-content --yaml-content "$(cat order-status.yml)" --name "Order Status (Acme)"
```

此后的命令都把结果中的 `app_id` 传给 `--app-id`。

新应用的 Web 应用标题取自文件，与 `--name` 无关。如果不想让用户看到这个标题，[修改它](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#修改-web-应用和应用信息)。

Workflow 或 Chatflow 应用还需完成 [更新应用](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#更新应用) 中的第 5～9 步。其他类型的应用只需完成第 5 步。

## 导入应用包

要导入从工作室导出的 [应用包](../../../%E5%AD%A6%E4%B9%A0/%E6%A0%B8%E5%BF%83%E6%A6%82%E5%BF%B5.md#dify-dsl)（`.ifpkg`），先解压，再把其中的 `app.yaml` 当作 DSL 文件使用。上传的图标不会随之导入，导入后需 [重新设置](%E9%80%9A%E8%BF%87%20DSL%20%E6%96%87%E4%BB%B6%E5%88%9B%E5%BB%BA%E5%92%8C%E6%9B%B4%E6%96%B0%E5%BA%94%E7%94%A8.md#修改-web-应用和应用信息)。

## 修改 Web 应用和应用信息

修改 Web 应用的设置（例如标题）用 `set webapp`，修改应用的名称、描述或图标用 `set app_info`。未传入的字段保持不变。

```bash theme={null}
difyctl set webapp workflow --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --title "Order Status"

difyctl set app_info workflow --app-id 9b4d2e7c-1a6f-4c8e-b3d5-7e2a9f1c4b6d --name "Order Status"
```

如果应用不是 Workflow 应用，运行 `difyctl help set webapp` 或 `difyctl help set app_info`，找到适用于它的命令。
