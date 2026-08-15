> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# DashScope 文本向量

> DashScope embedding API

将文本转换为向量，用于语义搜索、推荐、聚类和分类。

<Note>
  开始之前：[获取 API Key](/api-reference/preparation/api-key)，[将其设置为环境变量](/api-reference/preparation/export-api-key-env)，如果使用 SDK，还需[安装 DashScope SDK](/api-reference/preparation/install-sdk)。
</Note>

## 设置 SDK 基础 URL

**Python SDK**：

```python
import dashscope
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
```

**Java SDK**：

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
```

## 支持的模型

| 模型                | 向量维度                                  | 最大 Token 数 | 批量大小 | 语言支持   |
| ----------------- | ------------------------------------- | ---------- | ---- | ------ |
| text-embedding-v4 | 2048、1536、1024（默认）、768、512、256、128、64 | 8,192      | 10   | 100+ 种 |
| text-embedding-v3 | 1024（默认）、768、512                      | 8,192      | 10   | 50+ 种  |

关于模型计费，请参见[模型市场](https://www.qianwenai.com/models)。

## 输入格式

- **单个字符串**：最多 8,192 个 Token
- **数组**：最多 10 个字符串，每个最多 8,192 个 Token
- **文本文件**：最多 10 行，每行最多 8,192 个 Token

## DashScope 特有功能

- `text_type`：设置为 `query` 或 `document`，适用于检索等非对称任务。
- `output_type`：返回稀疏向量（`dense&sparse`），用于混合搜索（仅 v3/v4 支持）。
- `instruct`：添加任务描述以提升准确率约 1-5%（仅 v4 支持；建议使用英文）。

参见[限流](/developer-guides/administration/rate-limits)。

## OpenAPI

````yaml post /api/v1/services/embeddings/text-embedding/text-embedding
openapi: 3.1.0
info:
  title: 文本向量 API
  description: 文本向量模型 API 参考文档，支持 OpenAI 兼容协议和 DashScope 协议。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 服务端点
security:
  - bearer: []
paths:
  /api/v1/services/embeddings/text-embedding/text-embedding:
    post:
      operationId: createEmbeddingsDashScope
      summary: 创建文本向量（DashScope）
      description: 使用 DashScope 协议创建文本向量。
      security:
        - bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DashScopeEmbeddingRequest"
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeEmbeddingResponse"
        "400":
          description: 请求参数有误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
      x-codeSamples:
        - lang: python
          label: 输入字符串
          source: |
            import dashscope
            from http import HTTPStatus

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            resp = dashscope.TextEmbedding.call(
              model=dashscope.TextEmbedding.Models.text_embedding_v4,
              input='Semantic search finds documents by meaning rather than exact keyword matching. Text embeddings map words and sentences into high-dimensional vector spaces. Retrieval-augmented generation combines search results with language models. Document clustering groups similar texts based on their vector representations.',
              dimension=1024,
              output_type="dense&sparse"
            )

            print(resp) if resp.status_code == HTTPStatus.OK else print(resp)
        - lang: java
          label: 输入字符串
          source: |-
            import java.util.Arrays;
            import java.util.concurrent.Semaphore;
            import com.alibaba.dashscope.common.ResultCallback;
            import com.alibaba.dashscope.embeddings.TextEmbedding;
            import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
            import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;

            public final class Main {
                static {
                    Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
                }
                public static void basicCall() throws ApiException, NoApiKeyException{
                    TextEmbeddingParam param = TextEmbeddingParam
                    .builder()
                    .model(TextEmbedding.Models.TEXT_EMBEDDING_V4)
                    .texts(Arrays.asList("Semantic search finds documents by meaning rather than exact keyword matching.", "Text embeddings map words and sentences into high-dimensional vector spaces.", "Retrieval-augmented generation combines search results with language models.", "Document clustering groups similar texts based on their vector representations.")).build();
                    TextEmbedding textEmbedding = new TextEmbedding();
                    TextEmbeddingResult result = textEmbedding.call(param);
                    System.out.println(result);
                }

                public static void callWithCallback() throws ApiException, NoApiKeyException, InterruptedException{
                    TextEmbeddingParam param = TextEmbeddingParam
                    .builder()
                    .model(TextEmbedding.Models.TEXT_EMBEDDING_V4)
                    .texts(Arrays.asList("Semantic search finds documents by meaning rather than exact keyword matching.", "Text embeddings map words and sentences into high-dimensional vector spaces.", "Retrieval-augmented generation combines search results with language models.", "Document clustering groups similar texts based on their vector representations.")).build();
                    TextEmbedding textEmbedding = new TextEmbedding();
                    Semaphore sem = new Semaphore(0);
                    textEmbedding.call(param, new ResultCallback<TextEmbeddingResult>() {

                      @Override
                      public void onEvent(TextEmbeddingResult message) {
                        System.out.println(message);
                      }
                      @Override
                      public void onComplete(){
                        sem.release();
                      }

                      @Override
                      public void onError(Exception err){
                        System.out.println(err.getMessage());
                        err.printStackTrace();
                        sem.release();
                      }

                    });
                    sem.acquire();
                }

              public static void main(String[] args){
                try{
                  callWithCallback();
                }catch(ApiException|NoApiKeyException|InterruptedException e){
                  e.printStackTrace();
                  System.out.println(e);

                }
                  try {
                    basicCall();
                } catch (ApiException | NoApiKeyException e) {
                    System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 输入字符串
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "text-embedding-v4",
              "input": {
                "texts": [
                "Semantic search finds documents by meaning rather than exact keyword matching. Text embeddings map words and sentences into high-dimensional vector spaces. Retrieval-augmented generation combines search results with language models. Document clustering groups similar texts based on their vector representations."
                ]
              },
              "parameters": {
                "dimension": 1024,
                "output_type": "dense"
              }
            }'
        - lang: python
          label: 输入字符串列表
          source: |
            import dashscope
            from http import HTTPStatus

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            DASHSCOPE_MAX_BATCH_SIZE = 10

            inputs = ['Semantic search finds documents by meaning rather than exact keyword matching.', 'Text embeddings map words and sentences into high-dimensional vector spaces.', 'Retrieval-augmented generation combines search results with language models.', 'Document clustering groups similar texts based on their vector representations.']

            result = None
            batch_counter = 0
            for i in range(0, len(inputs), DASHSCOPE_MAX_BATCH_SIZE):
              batch = inputs[i:i + DASHSCOPE_MAX_BATCH_SIZE]
              resp = dashscope.TextEmbedding.call(
                model=dashscope.TextEmbedding.Models.text_embedding_v4,
                input=batch,
                dimension=1024
              )
              if resp.status_code == HTTPStatus.OK:
                if result is None:
                  result = resp
                else:
                  for emb in resp.output['embeddings']:
                    emb['text_index'] += batch_counter
                    result.output['embeddings'].append(emb)
                  result.usage['total_tokens'] += resp.usage['total_tokens']
              else:
                print(resp)
              batch_counter += len(batch)

            print(result)
        - lang: java
          label: 输入字符串列表
          source: |
            import java.util.Arrays;
            import java.util.List;
            import com.alibaba.dashscope.embeddings.TextEmbedding;
            import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
            import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;

            public final class Main {
              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }
              private static final int DASHSCOPE_MAX_BATCH_SIZE = 10;

              public static void main(String[] args) {
                List<String> inputs = Arrays.asList(
                    "Semantic search finds documents by meaning rather than exact keyword matching.",
                    "Text embeddings map words and sentences into high-dimensional vector spaces.",
                    "Retrieval-augmented generation combines search results with language models.",
                    "Document clustering groups similar texts based on their vector representations."
                );

                TextEmbeddingResult result = null;
                int batchCounter = 0;

                for (int i = 0; i < inputs.size(); i += DASHSCOPE_MAX_BATCH_SIZE) {
                  List<String> batch = inputs.subList(i, Math.min(i + DASHSCOPE_MAX_BATCH_SIZE, inputs.size()));
                  TextEmbeddingParam param = TextEmbeddingParam.builder()
                      .model(TextEmbedding.Models.TEXT_EMBEDDING_V4)
                      .texts(batch)
                      .build();

                  TextEmbedding textEmbedding = new TextEmbedding();
                  try {
                    TextEmbeddingResult resp = textEmbedding.call(param);
                    if (resp != null) {
                      if (result == null) {
                        result = resp;
                      } else {
                        for (var emb : resp.getOutput().getEmbeddings()) {
                          emb.setTextIndex(emb.getTextIndex() + batchCounter);
                          result.getOutput().getEmbeddings().add(emb);
                        }
                        result.getUsage().setTotalTokens(result.getUsage().getTotalTokens() + resp.getUsage().getTotalTokens());
                      }
                    } else {
                      System.out.println(resp);
                    }
                  } catch (ApiException | NoApiKeyException e) {
                    e.printStackTrace();
                  }
                  batchCounter += batch.size();
                }

                System.out.println(result);
              }
            }
        - lang: bash
          label: 输入字符串列表
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "text-embedding-v4",
              "input": {
              "texts": [
                      "Semantic search finds documents by meaning rather than exact keyword matching.",
                      "Text embeddings map words and sentences into high-dimensional vector spaces.",
                      "Retrieval-augmented generation combines search results with language models.",
                      "Document clustering groups similar texts based on their vector representations."
              ]
              },
              "parameters": {
                      "dimension": 1024,
                      "output_type": "dense"
              }
            }'
        - lang: python
          label: 输入文件
          source: |
            import dashscope
            from http import HTTPStatus
            from dashscope import TextEmbedding

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 请将 'texts_to_embedding.txt' 替换为您自己的文件名或路径。
            with open('texts_to_embedding.txt', 'r', encoding='utf-8') as f:
              resp = TextEmbedding.call(
                model=TextEmbedding.Models.text_embedding_v4,
                input=f,
                dimension=1024
              )

              if resp.status_code == HTTPStatus.OK:
                print(resp)
              else:
                print(resp)
        - lang: java
          label: 输入文件
          source: |-
            import java.io.BufferedReader;
            import java.io.FileReader;
            import java.io.IOException;
            import com.alibaba.dashscope.embeddings.TextEmbedding;
            import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
            import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;

            public final class Main {
              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }
              public static void main(String[] args) {
                // 请将 'tests_to_embedding.txt' 替换为您文件的完整路径。
                try (BufferedReader reader = new BufferedReader(new FileReader("texts_to_embedding.txt"))) {
                  StringBuilder content = new StringBuilder();
                  String line;
                  while ((line = reader.readLine()) != null) {
                    content.append(line).append("\n");
                  }

                  TextEmbeddingParam param = TextEmbeddingParam.builder()
                      .model(TextEmbedding.Models.TEXT_EMBEDDING_V4)
                      .text(content.toString())
                      .build();

                  TextEmbedding textEmbedding = new TextEmbedding();
                  TextEmbeddingResult result = textEmbedding.call(param);

                  if (result != null) {
                    System.out.println(result);
                  } else {
                    System.out.println("Failed to get embedding: " + result);
                  }
                } catch (IOException | ApiException | NoApiKeyException e) {
                  e.printStackTrace();
                }
              }
            }
        - lang: bash
          label: 输入文件
          source: |
            FILE_CONTENT=$(cat texts_to_embedding.txt | jq -Rs .)
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "text-embedding-v4",
              "input": {
                "texts": ['"$FILE_CONTENT"']
              },
              "parameters": {
                "dimension": 1024,
                "output_type": "dense"
              }
            }'
components:
  securitySchemes:
    bearer:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    EmbeddingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用的模型名称，支持 `text-embedding-v4` 和 `text-embedding-v3`。
          example: text-embedding-v4
        input:
          description: 待处理的输入文本。支持字符串、字符串数组或文件。单个字符串最多包含 8,192 个 token；字符串列表或文件最多包含 10 条（行），每条最多 8,192 个 token。
          oneOf:
            - type: string
              description: 单个文本字符串。
            - type: array
              items:
                type: string
              description: 字符串数组（最多 10 条）。
        dimensions:
          type: integer
          description: 向量维度。可选值：2048（仅 text-embedding-v4）、1536（仅 text-embedding-v4）、1024、768、512、256（仅 text-embedding-v4）、128（仅 text-embedding-v4）、64（仅 text-embedding-v4）。默认值：1024。
          default: 1024
          enum:
            - 2048
            - 1536
            - 1024
            - 768
            - 512
            - 256
            - 128
            - 64
        encoding_format:
          type: string
          description: 返回向量的格式，目前仅支持 `float`。
          default: float
          enum:
            - float
    EmbeddingResponse:
      type: object
      properties:
        data:
          type: array
          description: 任务输出数据。
          items:
            type: object
            properties:
              embedding:
                type: array
                items:
                  type: number
                description: 向量表示，为浮点数数组。
              index:
                type: integer
                description: 本结果对应输入数组中的文本索引。
              object:
                type: string
                description: 调用返回的对象类型，默认为 `embedding`。
                default: embedding
        model:
          type: string
          description: 调用的模型名称。
        object:
          type: string
          description: 返回的数据类型，默认为 `list`。
          default: list
        usage:
          type: object
          description: Token 用量统计。
          properties:
            prompt_tokens:
              type: integer
              description: 输入文本的 token 数量。
            total_tokens:
              type: integer
              description: 请求中 token 的总数，按模型分词器计算。
        id:
          type: string
          description: 请求的唯一标识符，可用于追踪和排查问题。
      example:
        data:
          - embedding:
              - -0.0695386752486229
              - 0.030681096017360687
            index: 0
            object: embedding
          - embedding:
              - -0.06348952651023865
              - 0.060446035116910934
            index: 5
            object: embedding
        model: text-embedding-v4
        object: list
        usage:
          prompt_tokens: 184
          total_tokens: 184
        id: 73591b79-d194-9bca-8bb5-xxxxxxxxxxxx
    DashScopeEmbeddingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用的模型名称，支持 `text-embedding-v4` 和 `text-embedding-v3`。
          example: text-embedding-v4
        input:
          type: object
          required:
            - texts
          description: 包含待向量化文本的输入对象。
          properties:
            texts:
              description: 待处理的输入文本，可以是字符串或字符串数组。单个字符串最多 8,192 个 token；字符串列表最多 10 条，每条最多 8,192 个 token。
              oneOf:
                - type: string
                  description: 单个文本字符串。
                - type: array
                  items:
                    type: string
                  description: 字符串数组（最多 10 条）。
        parameters:
          type: object
          description: 向量化请求的可选参数。
          properties:
            text_type:
              type: string
              description: 指定文本类型，用于非对称任务。检索场景下区分 `query`（查询词）和 `document`（文档）有助于提升效果；聚类、分类等对称任务使用默认值 `document`。
              default: document
              enum:
                - query
                - document
            dimension:
              type: integer
              description: 向量维度。可选值：2048（仅 text-embedding-v4）、1536（仅 text-embedding-v4）、1024、768、512、256（仅 text-embedding-v4）、128（仅 text-embedding-v4）、64（仅 text-embedding-v4）。默认值：1024。
              default: 1024
              enum:
                - 2048
                - 1536
                - 1024
                - 768
                - 512
                - 256
                - 128
                - 64
            output_type:
              type: string
              description: 是否输出稀疏向量表示，仅适用于 text-embedding-v3 和 text-embedding-v4。默认值：`dense`（仅返回稠密向量）。
              default: dense
              enum:
                - dense
                - sparse
                - dense&sparse
            instruct:
              type: string
              description: 自定义任务描述，仅在 text-embedding-v4 且 `text_type` 为 `query` 时生效，推荐使用英文描述（可提升约 1%~5% 的效果）。
    DashScopeEmbeddingResponse:
      type: object
      properties:
        status_code:
          type: integer
          description: 状态码，200 表示请求成功。
        request_id:
          type: string
          description: 请求的唯一标识符，可用于追踪和排查问题。
        code:
          type: string
          description: 请求失败时的错误码，成功时为空。
        message:
          type: string
          description: 请求失败时的详细错误信息，成功时为空。
        output:
          type: object
          description: 任务输出数据。
          properties:
            embeddings:
              type: array
              description: 结构体数组，每个结构体包含对应输入文本的向量输出。
              items:
                type: object
                properties:
                  sparse_embedding:
                    type: array
                    description: 稀疏向量表示，仅在 `output_type` 包含 `sparse` 时适用于 text-embedding-v3 和 text-embedding-v4。
                    items:
                      type: object
                      properties:
                        index:
                          type: integer
                          description: 词或字符在词汇表中的索引。
                        value:
                          type: number
                          description: 该 token 的权重或重要性分数，值越高表示越重要。
                        token:
                          type: string
                          description: 来自词汇表的实际文本单元或词语。
                  embedding:
                    type: array
                    items:
                      type: number
                    description: 稠密向量表示（dense embedding）。
                  text_index:
                    type: integer
                    description: 本结果对应输入数组中的文本索引。
        usage:
          type: object
          description: Token 用量统计。
          properties:
            total_tokens:
              type: integer
              description: 请求中 token 的总数，按模型分词器计算。
      example:
        status_code: 200
        request_id: 1ba94ac8-e058-99bc-9cc1-7fdb37940a46
        code: ""
        message: ""
        output:
          embeddings:
            - sparse_embedding:
                - index: 7149
                  value: 0.829
                  token: wind
                - index: 111290
                  value: 0.9004
                  token: sorrow
              embedding:
                - -0.006929283495992422
                - -0.005336422007530928
              text_index: 0
        usage:
          total_tokens: 27
    ErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 详细错误信息。
        request_id:
          type: string
          description: 请求的唯一标识符，可用于追踪和排查问题。
      example:
        code: InvalidParameter
        message: "The model name is invalid. Supported models: text-embedding-v4, text-embedding-v3."
        request_id: a1b2c3d4-e5f6-7890-abcd-xxxxxxxxxxxx
````
