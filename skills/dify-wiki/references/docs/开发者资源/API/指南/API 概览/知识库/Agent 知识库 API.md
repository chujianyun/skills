# Agent 知识库 API

> 在自己的代码中查询 Agent 知识库，回查某次运行检索到的内容，并维护知识库的文档、数据源和设置

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/api-reference/guides/knowledge-base.md)。

> [!NOTE]
>
> 本 API 仅适用于 [Agent 知识库](../../../../../%E4%BD%BF%E7%94%A8/%E7%9F%A5%E8%AF%86%E5%BA%93/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93.md)。经典知识库使用 [经典知识库 API](%E7%BB%8F%E5%85%B8%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md)。

有些操作只能在 Dify 中完成，例如创建知识库及其元数据字段、上传文件，以及启用或禁用文档。

## 获取知识库端点

API 密钥及其访问范围详见 [知识库 API](%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md)。

在 Dify 中打开该知识库，点击左下角的 **API 访问**，复制其中的端点。端点以 `/knowledge-fs/spaces/<knowledge base ID>` 结尾，其中的 ID 就是各操作所需的 `knowledge_base_id`。

## 查询知识库

先确定检索深度（`mode`）：

| 深度 | 返回内容 | 适用场景 |
| :- | :- | :- |
| `fast` | 检索到的分段摘要，按章节逐一整理 | 大多数直接提问。先从它开始 |
| `deep` | 同样的摘要，但检索范围更广、速度更慢 | 答案涉及多个关联主题，`fast` 找不全 |
| `research` | 根据检索到的分段写成的回答，以流式返回 | 需要 Dify 直接写出回答，或问题需要多次检索才能回答 |

下面的脚本需要 Bash、curl、jq 和 Python 3。按顺序把两个代码块复制到 `query.sh` 中，运行 `bash query.sh`，再根据提示输入刚才复制的端点和 API 密钥。

**1. 创建查询令牌**

调用 [创建查询令牌](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2/%E5%88%9B%E5%BB%BA%E6%9F%A5%E8%AF%A2%E4%BB%A4%E7%89%8C.md)，在 `query` 中传入问题，在 `mode` 中传入检索深度。

```bash theme={null}
set -euo pipefail
read -r -p "Knowledge base Service API endpoint: " ENDPOINT
ENDPOINT="${ENDPOINT%/}"
read -r -s -p "Knowledge base API key: " API_KEY
printf '\n'

ADMISSION=$(curl --fail-with-body -sS "$ENDPOINT/queries/admission" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"What changed in the refund policy this quarter?","mode":"fast"}')
TOKEN=$(printf '%s' "$ADMISSION" | jq -er '.token')
REQUEST=$(printf '%s' "$ADMISSION" | jq -c '.request')
URL=$(printf '%s' "$ADMISSION" | jq -er '.url')
TRACE_ID=$(printf '%s' "$ADMISSION" | jq -er '.trace_id')
URL=$(python3 -c '
import sys
from urllib.parse import urljoin
print(urljoin(sys.argv[1] + "/", sys.argv[2]))
' "$ENDPOINT" "$URL")
```

**2. 运行查询**

把 `request` 原样 POST 到 [运行查询](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2/%E8%BF%90%E8%A1%8C%E6%9F%A5%E8%AF%A2.md)，用查询令牌代替 API 密钥，并把 `trace_id` 放进 `X-Trace-ID` 请求头。

```bash theme={null}
curl --fail-with-body -sS -N "$URL" \
  -D query-headers.txt \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Trace-ID: $TRACE_ID" \
  -H "Content-Type: application/json" \
  -d "$REQUEST"

QUERY_RECORD_ID=$(awk 'tolower($1) == "x-query-run-id:" {sub(/\r$/, "", $2); print $2}' query-headers.txt)
SESSION_ID=$(awk 'tolower($1) == "x-session-id:" {sub(/\r$/, "", $2); print $2}' query-headers.txt)
printf '\nQuery record: %s\nSession: %s\n' "$QUERY_RECORD_ID" "$SESSION_ID"
```

保存 `x-query-run-id` 响应头中的查询记录 ID，之后 [排查回答](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#investigate-an-answer) 时要用。它与第 1 步的 `trace_id` 不是同一个值。

**3. 读取事件**

只有 `answer.done` 才算成功。`answer.error` 可能在若干 `answer.delta` 帧之后到达，此时 HTTP 状态仍是 200：丢弃已收到的部分文本。连接断开后无法续传。无论失败发生在流打开之前还是之后，都从第 1 步重新开始。

按你所用的最慢深度设置客户端的读取超时。运行查询接口不发送保活事件，默认超时可能会切断 `deep` 或 `research` 的流。

无论哪种深度，返回的文本最多 2,000 个字符，被截断时也没有任何提示。`answer.done` 的 `metadata.evidenceBundle` 中的分段文本从不截断，需要完整的检索文本时，从这里读取。

每次查询都会单独作答，即使把之前响应的 `x-session-id` 作为 `sessionId` 传入也一样，所以追问需要的信息都要写进这次的 `query`。

## 排查回答

回答看起来不对时，把它的查询记录 ID 传给 [获取查询记录](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95/%E8%8E%B7%E5%8F%96%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95.md)，查看这次运行记录下的各个步骤。用同一个 ID 还可以检查证据：

* 调用 [获取查询分段列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95/%E8%8E%B7%E5%8F%96%E6%9F%A5%E8%AF%A2%E5%88%86%E6%AE%B5%E5%88%97%E8%A1%A8.md)，查看检索到的分段、得分和引用。
* 如果检索到的文本自相矛盾，调用 [获取查询冲突列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95/%E8%8E%B7%E5%8F%96%E6%9F%A5%E8%AF%A2%E5%86%B2%E7%AA%81%E5%88%97%E8%A1%A8.md)，找出相互冲突的分段。
* 调用 [获取缺失分段列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95/%E8%8E%B7%E5%8F%96%E7%BC%BA%E5%A4%B1%E5%88%86%E6%AE%B5%E5%88%97%E8%A1%A8.md)，查看这次运行需要但没能用上的分段，以及没用上的原因。

如果没有检索到正确的分段，或正确的分段排名靠后，在 Dify 中 [调优检索](../../../../../%E4%BD%BF%E7%94%A8/%E7%9F%A5%E8%AF%86%E5%BA%93/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%B5%8B%E8%AF%95%E5%B9%B6%E8%B0%83%E4%BC%98%E6%A3%80%E7%B4%A2.md#问题案例)。

如果没有保存 ID，可在 [获取查询记录列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95/%E8%8E%B7%E5%8F%96%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95%E5%88%97%E8%A1%A8.md) 中查找这次运行。

## 防止重复写入和过期写入

凡是支持 `Idempotency-Key` 请求头的写操作，都带上它。如果响应丢失，用同一个键再发一次相同的请求：返回的是原来的任务、运行或作业，不会再新建一个。每个新操作都要用新的键，因为重复的键会返回之前的结果，即使那次操作已经结束。

在更新或删除对象的前一刻读取它当前的版本，放进该操作的版本字段一起发送。这样，收到 409 就说明对象在你读取之后发生了变化：重新读取，确认你的变更仍然适用，再重新发送。409 也可能表示该 `Idempotency-Key` 已用于其他请求：此时改用新的键。

## 运行研究任务

`research` 深度的查询在流中直接给出回答，研究任务则在后台运行，并保留结果。用户正在等回答时，用查询；工作可以稍后完成，或之后还要用到结果时，用研究任务。

**1. 规划**

把问题作为 `query` 发送给 [规划研究任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1/%E8%A7%84%E5%88%92%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1.md)，同时传入想用的 `mode` 和 `topK`。它会返回预估的成本、延迟和步骤，但不会启动任何任务。

**2. 创建**

调用 [创建研究任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1/%E5%88%9B%E5%BB%BA%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1.md)，传入相同的问题和设置。想在预估超出可接受范围时直接拒绝任务，就加上 `limits`：预估超出这些限制的任务会失败，返回 422。

如需限制任务运行期间的花费，加上 `budgetUsd`。需要回答时，把预算设得远高于规划结果中的 `estimates.costUsd.max`，因为每次调用模型时，预算都要容得下这次调用最多可能的花费。因预算停止的任务，状态为 `canceled`。

**3. 轮询**

用返回的任务 ID 调用 [获取研究任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1.md)，直到任务结束。

**4. 读取结果**

调用 [获取研究任务结果列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E7%A0%94%E7%A9%B6%E4%BB%BB%E5%8A%A1%E7%BB%93%E6%9E%9C%E5%88%97%E8%A1%A8.md)，在最后一条结果中查看 `answer`。

## 浏览文档和分段

文档就是 **文档** 页面中显示的条目。文档有自己的文档 ID，背后存储的文件另有一个文档文件 ID。每次内容更新（包括数据源同步带来的更新）都会存入一个新文件，生成新的 ID，但文档 ID 保持不变。保存文档 ID，并通过它的修订版本追溯内容历史。

| ID | 来源 | 使用该 ID 的操作 |
| :- | :- | :- |
| 文档文件 ID | [获取文档文件列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8.md)、引用中的 `documentAssetId`，或 [获取查询分段列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2%E8%AE%B0%E5%BD%95/%E8%8E%B7%E5%8F%96%E6%9F%A5%E8%AF%A2%E5%88%86%E6%AE%B5%E5%88%97%E8%A1%A8.md) 中的 `metadata.documentId`，这个字段名看似指文档 ID，实际存的是文档文件 ID | [获取文档文件](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6.md)、[获取文档大纲](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E5%A4%A7%E7%BA%B2.md)、[按文件获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%8C%89%E6%96%87%E4%BB%B6%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md)、[删除文档文件](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E5%88%A0%E9%99%A4%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6.md)、[批量删除文档文件](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%89%B9%E9%87%8F%E5%88%A0%E9%99%A4%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6.md) |
| 文档 ID | [获取文档列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E5%88%97%E8%A1%A8.md)、[按文件获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%8C%89%E6%96%87%E4%BB%B6%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md)，或已打开文档的地址栏（`/datasets/new/<knowledge base ID>/documents/<document ID>`） | [获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md)、[更新文档元数据](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%9B%B4%E6%96%B0%E6%96%87%E6%A1%A3%E5%85%83%E6%95%B0%E6%8D%AE.md)、[删除文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E5%88%A0%E9%99%A4%E6%96%87%E6%A1%A3.md)、[获取文档修订版本列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E4%BF%AE%E8%AE%A2%E7%89%88%E6%9C%AC%E5%88%97%E8%A1%A8.md)、[获取分段列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E5%88%86%E6%AE%B5%E5%88%97%E8%A1%A8.md)、[获取分段](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E5%88%86%E6%AE%B5.md)、[获取文档的索引任务列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E7%9A%84%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8.md)、[获取文档的索引任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E7%9A%84%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1.md) |

要显示某条引用来自哪个文档，把它的 `documentAssetId` 传给 [按文件获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%8C%89%E6%96%87%E4%BB%B6%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md)，并将 `document_asset_version` 设为 `1`。

要读取文档的分段，把文档 ID 和修订版本号传给 [获取分段列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E5%88%86%E6%AE%B5%E5%88%97%E8%A1%A8.md)。要读取当前用于检索的内容，从 [获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md) 中取 `active.revision`。要读取更早的内容，在 [获取文档修订版本列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E4%BF%AE%E8%AE%A2%E7%89%88%E6%9C%AC%E5%88%97%E8%A1%A8.md) 中找到对应的修订版本。

要从其他系统（例如 CMS 或工单工具）设置文档的元数据，调用 [更新文档元数据](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%9B%B4%E6%96%B0%E6%96%87%E6%A1%A3%E5%85%83%E6%95%B0%E6%8D%AE.md)。

## 添加数据源

数据源通过连接读取内容。连接指在 **集成** > **数据来源** 中配置、并关联到该知识库的提供商账号或 API 密钥。每个提供商的第一个数据源需在 Dify 中添加，入口是知识库的 **数据源** 页面。如需通过 API 添加更多数据源：

1. 调用 [获取数据源连接列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E8%BF%9E%E6%8E%A5%E5%88%97%E8%A1%A8.md)，选择一个状态为 `active`、且 `configuration` 指明了目标提供商的连接。
2. 调用 [创建数据源](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E5%88%9B%E5%BB%BA%E6%95%B0%E6%8D%AE%E6%BA%90.md)，将连接的 `id` 作为 `connectionId`，将其 `configuration.providerKind` 作为 `metadata.providerKind`。按数据源读取的内容设置 `type` 和 `uri`：

   * 网站：`type: web`，`uri` 为网站的根 URL。
   * 在线文档平台或在线云盘：`type: connector`，`uri` 为 `connector://<connectionId>`。

   创建数据源接口不支持 `Idempotency-Key`，同一请求发送两次会创建两个数据源。附上一个唯一的 `metadata.client_request_id`：如果响应丢失，重新创建数据源之前，先在 [获取数据源列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E5%88%97%E8%A1%A8.md) 中查找这个值。

## 导入网站页面

网站数据源有 3 种填充方式：

* 从抓取预览中挑选页面。
* 导入已知的 URL。
* [同步](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#sync-and-schedule-sources) 一个还没有页面列表的数据源：Dify 会抓取整个网站，并导入找到的每个页面。

每次导入都会替换数据源的页面列表，因此要发送所有想保留的页面，而不只是新页面。之后的同步会刷新列表中的页面。

从抓取预览中挑选页面的步骤如下：

**1. 预览抓取**

调用 [预览网站抓取](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E9%A2%84%E8%A7%88%E7%BD%91%E7%AB%99%E6%8A%93%E5%8F%96.md)，然后用返回的 `id` 轮询 [获取数据源运行](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E8%BF%90%E8%A1%8C.md)，直到 `state` 变为 `preview_ready` 或运行结束。

以 `zero_results` 结束的运行表示没有找到任何页面。检查数据源的 URL 和抓取设置，然后重新预览。

**2. 挑选页面**

用运行 ID 分页调用 [获取抓取预览页面列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E8%8E%B7%E5%8F%96%E6%8A%93%E5%8F%96%E9%A2%84%E8%A7%88%E9%A1%B5%E9%9D%A2%E5%88%97%E8%A1%A8.md)，收集每个要导入页面的 `page_id`。

**3. 导入**

在同一次运行上调用 [导入所选页面](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E5%AF%BC%E5%85%A5%E6%89%80%E9%80%89%E9%A1%B5%E9%9D%A2.md)，传入这些 `pageIds`。运行会沿用同一个 ID 继续：[跟踪这次运行](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#follow-source-runs)，直到它结束。

要导入已知 URL 的页面，调用 [导入网站页面](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E5%AF%BC%E5%85%A5%E7%BD%91%E7%AB%99%E9%A1%B5%E9%9D%A2.md)，将这些 URL 作为 `sourceUrls` 传入。未传入页面对应的文档会在下次同步时删除。要改为在同一次运行中删除，同时设置 `replaceExistingSelection: true`。

## 导入在线文档和云盘文件

通过 API，可为新的 `connector` 数据源填充一次内容。数据源一旦导入过条目，无论是在 Dify 中还是通过 API，之后的导入就只能移除条目：包含新条目的导入会失败，尽管其 `failure` 提示可以重试。新条目需在 Dify 中添加。

你发送的条目就是该数据源的全部内容：未发送条目对应的文档会在同一次运行中删除。

1. 根据数据源的 `metadata.providerKind`，在线文档数据源用 [获取数据源页面列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E9%A1%B5%E9%9D%A2%E5%88%97%E8%A1%A8.md) 浏览，在线云盘用 [获取数据源文件列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8.md) 浏览。
2. 调用 [导入数据源条目](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E5%AF%BC%E5%85%A5%E6%95%B0%E6%8D%AE%E6%BA%90%E6%9D%A1%E7%9B%AE.md)，传入与提供商匹配的 `kind`，以及根据浏览结果构建的 `items`，并严格遵循该操作规定的 `providerItemId` 格式。
3. 用返回的 `id` [跟踪这次运行](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#follow-source-runs)。

## 跟踪数据源运行

用发起运行时返回的 `id` 调用 [获取数据源运行](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E8%BF%90%E8%A1%8C.md)，一直跟踪到运行结束。运行进入 `completed` 时，它导入或刷新的每个条目都已完成索引并激活，无需另外跟踪索引。

一个数据源同一时间只处理一次运行：已有运行在进行时，再发起同步或导入会失败，返回 502。等进行中的运行结束，或调用 [取消数据源运行](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E5%8F%96%E6%B6%88%E6%95%B0%E6%8D%AE%E6%BA%90%E8%BF%90%E8%A1%8C.md) 将其取消。抓取预览在你从中导入或将其取消之前，都算作进行中的运行，因此不打算从中导入的预览要取消掉。

要查找不是你发起的运行（例如定时同步，或在 Dify 中发起的运行），调用 [获取数据源运行列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90%E8%BF%90%E8%A1%8C%E5%88%97%E8%A1%A8.md)。

运行失败时，查看其 `failure` 了解原因。要排除凭据错误，调用 [测试数据源凭据](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E6%B5%8B%E8%AF%95%E6%95%B0%E6%8D%AE%E6%BA%90%E5%87%AD%E6%8D%AE.md)：如果 `valid` 为 `false`，在 Dify 中修正该连接的凭据。

要让 `failed` 或 `canceled` 状态的运行沿用同一个 ID 从头再跑一次，调用 [重试数据源运行](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E9%87%8D%E8%AF%95%E6%95%B0%E6%8D%AE%E6%BA%90%E8%BF%90%E8%A1%8C.md)。如果要重做已取消的抓取预览，或失败的 [导入网站页面](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E5%AF%BC%E5%85%A5%E7%BD%91%E7%AB%99%E9%A1%B5%E9%9D%A2.md) 运行，改用新的 `Idempotency-Key` 发起新的预览或导入。

## 同步数据源与定时同步

要立即获取数据源的最新内容，调用 [同步数据源](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%AF%BC%E5%85%A5/%E5%90%8C%E6%AD%A5%E6%95%B0%E6%8D%AE%E6%BA%90.md)，然后 [跟踪它返回的运行](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#follow-source-runs)。

要定时同步，需为每个数据源分别保存定时同步设置：

**1. 读取两个版本号**

先从 [获取数据源](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E8%8E%B7%E5%8F%96%E6%95%B0%E6%8D%AE%E6%BA%90.md) 读取数据源的 `version`，再从 [获取同步策略](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E8%8E%B7%E5%8F%96%E5%90%8C%E6%AD%A5%E7%AD%96%E7%95%A5.md) 读取定时同步的 `revision`。如果数据源还没有定时同步，获取同步策略接口会返回 404：此时修订版本号取 `0`。

**2. 保存定时同步**

调用 [更新同步策略](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E6%9B%B4%E6%96%B0%E5%90%8C%E6%AD%A5%E7%AD%96%E7%95%A5.md)，将 `revision` 作为 `expectedRevision`、`version` 作为 `expectedSourceVersion` 传入。

第一次定时同步会在保存后经过一个同步间隔才运行，如果想马上拿到最新内容，现在也手动同步一次。

每次向设有定时同步的数据源导入完成后，都要重新读取这两个值，再保存一次定时同步。导入会改变数据源的 `version`，仍绑定在旧值上的定时同步会在下一次到期时自行关闭。

要停止定时同步，保存 `mode: manual` 并设置 `enabled: false`。用 [更新数据源](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E6%9B%B4%E6%96%B0%E6%95%B0%E6%8D%AE%E6%BA%90.md) 把数据源的 `status` 设为 `disabled` 只会暂停定时同步，暂停期间到期的同步会在数据源重新启用后立即运行。

## 重新索引并跟踪索引进度

索引失败或已取消时，用 [重试索引任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E9%87%8D%E8%AF%95%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1.md) 重新启动该任务。文档已完成索引但结果有误时，重新索引该文档。

更换嵌入模型会自动重新嵌入所有文档。更换推理模型后，已索引的文档仍保留原模型构建的内容，直到你重新索引为止。

调用 [重新索引文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E9%87%8D%E6%96%B0%E7%B4%A2%E5%BC%95%E6%96%87%E6%A1%A3.md)，传入 `documentIds` 或 `all: true`。只有状态为 `queued` 的条目启动了任务：逐一保存它们的 `compilation_job.id`。

要知道新内容何时生效，轮询索引任务，直到其结束：

* 对于重新索引，用 `compilation_job.id` 轮询 [获取索引任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1.md)。
* 对于不是通过 API 发起的索引（例如在 Dify 中上传文件），从 [获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md) 或 [获取文档列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E5%88%97%E8%A1%A8.md) 中读取 `latest_task.id`，再用文档 ID 和该任务 ID 轮询 [获取文档的索引任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E7%9A%84%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1.md)。

## 更换模型或检索设置

从 [获取可用模型](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/%E7%BB%8F%E5%85%B8%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%A8%A1%E5%9E%8B/%E8%8E%B7%E5%8F%96%E5%8F%AF%E7%94%A8%E6%A8%A1%E5%9E%8B.md) 返回的结果中选择模型。该操作需要可访问所有知识库的密钥：仅限特定知识库的密钥会收到 403 `forbidden`。

如果在第一个文档完成索引之前设置模型，模型要等到该文档索引完成后才会校验。届时查看 [获取知识库设置](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E8%AE%BE%E7%BD%AE/%E8%8E%B7%E5%8F%96%E7%9F%A5%E8%AF%86%E5%BA%93%E8%AE%BE%E7%BD%AE.md) 中的 `issues`：其中列出了所有让知识库无法就绪的问题。

更换模型前，先等正在索引的文档完成索引，或取消相应的索引任务。如果更改生效时文档仍在索引，该文档会索引失败；等更改完成后，用 [重试索引任务](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E9%87%8D%E8%AF%95%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1.md) 重新启动它的索引任务。

知识库有了已索引的内容后，大多数设置变更都会作为迁移在后台运行：

**1. 更新**

调用 [更新知识库设置](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E8%AE%BE%E7%BD%AE/%E6%9B%B4%E6%96%B0%E7%9F%A5%E8%AF%86%E5%BA%93%E8%AE%BE%E7%BD%AE.md)。返回 202 表示该变更启动了一次迁移：保存 `migration.id`。

**2. 轮询**

用 `migration.id` 调用 [获取设置迁移](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E8%AE%BE%E7%BD%AE/%E8%8E%B7%E5%8F%96%E8%AE%BE%E7%BD%AE%E8%BF%81%E7%A7%BB.md)，直到迁移结束。

每次更新只能更换嵌入模型或检索设置中的一项，不能两者都改：同时包含两者的调用会被拒绝，返回 422。要两者都更换，先发送嵌入模型的变更，等它的迁移成功后，再发送检索设置的变更。

## 删除文档和数据源

要删除整个文档，调用 [删除文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E5%88%A0%E9%99%A4%E6%96%87%E6%A1%A3.md)，并将 [获取文档](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3.md) 返回的文档 `row_version` 作为 `expectedRevision` 传入。删除完成后，该文档不再占用文档配额。也可删除文档文件（[删除文档文件](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E5%88%A0%E9%99%A4%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6.md)、[批量删除文档文件](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E6%89%B9%E9%87%8F%E5%88%A0%E9%99%A4%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6.md)）和数据源（[删除数据源](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%95%B0%E6%8D%AE%E6%BA%90/%E5%88%A0%E9%99%A4%E6%95%B0%E6%8D%AE%E6%BA%90.md)）。

删除文档文件只会删除基于该文件的修订版本，不会删除文档本身。不要删除生效修订版本的文件：旧的修订版本不会顶替上来，文档也会从获取文档列表的结果和 Dify 的文档列表中消失。但文档并没有被删除，仍会占用文档配额。

删除数据源会同时删除它导入的文档。要保留这些文档，先从 [获取文档文件列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%96%87%E6%A1%A3%E4%B8%8E%E5%88%86%E6%AE%B5/%E8%8E%B7%E5%8F%96%E6%96%87%E6%A1%A3%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8.md) 中保存带有该 `source_id` 的文件 ID，因为删除完成后，这些文件的 `source_id` 会变为 `null`。然后用 `documents=keep` 删除数据源。保留的文档在删除完成前处于隐藏状态，之后也不再随任何数据源更新。

要确认删除已完成，用 `job.id` 轮询 [获取删除作业](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E5%88%A0%E9%99%A4%E4%BD%9C%E4%B8%9A/%E8%8E%B7%E5%8F%96%E5%88%A0%E9%99%A4%E4%BD%9C%E4%B8%9A.md)，直到作业结束。

对于批量删除，用 `batch_id` 轮询 [获取删除批次](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E5%88%A0%E9%99%A4%E4%BD%9C%E4%B8%9A/%E8%8E%B7%E5%8F%96%E5%88%A0%E9%99%A4%E6%89%B9%E6%AC%A1.md)，直到 `results` 中的每一项要么为 `rejected`，要么对应的作业已经结束。`rejected` 的文件没有删除，`error` 说明了原因。出现 `pending` 的项，说明批次中途停止，继续轮询也不会让它变化：用同一个 `Idempotency-Key` 再次发送相同的请求，即可只重试 `pending` 的文件。

以 `failed` 结束的删除，无论通过 API 还是在 Dify 中，都无法重试或清除。要删除的内容会一直隐藏，包括以 `documents=keep` 删除数据源时保留的文档。

## 处理错误

与 [错误与速率限制](../../%E5%A4%84%E7%90%86%E9%94%99%E8%AF%AF%E4%B8%8E%E9%80%9F%E7%8E%87%E9%99%90%E5%88%B6.md) 中介绍的一样，错误带有 `code`、`message` 和 `status`，很多错误还会附带 `failure` 对象：其中的 `retryPolicy` 说明重试是否有用。[运行查询](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%9F%A5%E8%AF%A2/%E8%BF%90%E8%A1%8C%E6%9F%A5%E8%AF%A2.md) 的错误有自己的结构，列在该操作的页面上。

遇到 502 时，读操作可稍等片刻后重试。写操作则可能在响应丢失之前就已生效：[用同一个 `Idempotency-Key` 重新发送](#prevent-duplicate-and-stale-writes)；不支持幂等键的写操作，先确认结果再重新发送。发起同步或导入时遇到 502，也可能是因为该数据源已有进行中的运行：详见 [跟踪数据源运行](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md#follow-source-runs)。

除 [获取可用模型](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/%E7%BB%8F%E5%85%B8%E7%9F%A5%E8%AF%86%E5%BA%93/%E6%A8%A1%E5%9E%8B/%E8%8E%B7%E5%8F%96%E5%8F%AF%E7%94%A8%E6%A8%A1%E5%9E%8B.md) 外，403 `forbidden` 表示工作空间已达到知识库的 [请求频率限制](../../../../../%E4%BD%BF%E7%94%A8/%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%9F%A5%E8%AF%86%E5%BA%93%E8%AF%B7%E6%B1%82%E9%A2%91%E7%8E%87%E9%99%90%E5%88%B6.md)。整个工作空间共享这一限制，每次调用都会计入，读操作也不例外。被限制拒绝的调用同样计入，因此重试前要先退避，轮询时也要拉开间隔。要在一次调用中轮询多个索引任务或批量任务，将它们的 ID 作为 `task_ids` 传给 [获取后台任务列表](../../../%E7%9F%A5%E8%AF%86%E5%BA%93%20API/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%B4%A2%E5%BC%95%E4%BB%BB%E5%8A%A1/%E8%8E%B7%E5%8F%96%E5%90%8E%E5%8F%B0%E4%BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8.md)。

### 请求大小限制

每个请求都要低于其操作页面上标注的字节上限，并留出一定余量。Dify 会在补上默认值和自身字段之后再计算请求大小，因此即使每个字段都在字符数限制以内，请求整体仍可能超限。
