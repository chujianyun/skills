> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenAI 兼容文本向量

> OpenAI 兼容的文本向量接口

<Note>
  调用 API 前，请先[获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如果使用 OpenAI SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

## 支持的模型

| 模型                | 向量维度                                  | 最大 Token 数 | 批量大小 | 语言支持       |
| ----------------- | ------------------------------------- | ---------- | ---- | ---------- |
| text-embedding-v4 | 2048、1536、1024（默认）、768、512、256、128、64 | 8,192      | 10   | 100+ 种主流语言 |
| text-embedding-v3 | 1024（默认）、768、512                      | 8,192      | 10   | 50+ 种语言    |

关于模型计费，请参见[模型市场](https://www.qianwenai.com/models)。

## 服务地址

`POST https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`

SDK 使用 base URL 时无需包含 `/embeddings`。

## OpenAPI

````yaml post /compatible-mode/v1/embeddings
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
  /compatible-mode/v1/embeddings:
    post:
      operationId: createEmbeddingsOpenAI
      summary: 创建文本向量（OpenAI 兼容）
      description: 使用 OpenAI 兼容协议创建文本向量。
      security:
        - bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/EmbeddingRequest"
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/EmbeddingResponse"
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
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如未配置环境变量，请用您的 API Key 替换此处。
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )

            completion = client.embeddings.create(
              model="text-embedding-v4",
              input='The clothes are of good quality and look good, definitely worth the wait. I love them.',
              dimensions=1024,
              encoding_format="float"
            )

            print(completion.model_dump_json())
        - lang: java
          label: 输入字符串
          source: |
            import java.net.URI;
            import java.net.http.HttpClient;
            import java.net.http.HttpRequest;
            import java.net.http.HttpResponse;
            import java.util.HashMap;
            import java.util.Map;
            import com.alibaba.dashscope.utils.JsonUtils;

            public final class Main {
              public static void main(String[] args) {
                String apiKey = System.getenv("DASHSCOPE_API_KEY");
                if (apiKey == null) {
                  System.out.println("DASHSCOPE_API_KEY not found in environment variables");
                  return;
                }
                String baseUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings";
                HttpClient client = HttpClient.newHttpClient();

                Map<String, Object> requestBody = new HashMap<>();
                requestBody.put("model", "text-embedding-v4");
                requestBody.put("input", "Semantic search finds documents by meaning rather than exact keyword matching. Text embeddings map words and sentences into high-dimensional vector spaces. Retrieval-augmented generation combines search results with language models. Document clustering groups similar texts based on their vector representations.");
                requestBody.put("dimensions", 1024);
                requestBody.put("encoding_format", "float");

                try {
                  String requestBodyString = JsonUtils.toJson(requestBody);
                  HttpRequest request = HttpRequest.newBuilder()
                      .uri(URI.create(baseUrl))
                      .header("Content-Type", "application/json")
                      .header("Authorization", "Bearer " + apiKey)
                      .POST(HttpRequest.BodyPublishers.ofString(requestBodyString))
                      .build();

                  HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                  if (response.statusCode() == 200) {
                    System.out.println("Response: " + response.body());
                  } else {
                    System.out.printf("Failed to retrieve response, status code: %d, response: %s%n", response.statusCode(), response.body());
                  }
                } catch (Exception e) {
                  System.err.println("Error: " + e.getMessage());
                }
              }
            }
        - lang: bash
          label: 输入字符串
          source: |
            curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "text-embedding-v4",
              "input": "Semantic search finds documents by meaning rather than exact keyword matching. Text embeddings map words and sentences into high-dimensional vector spaces. Retrieval-augmented generation combines search results with language models. Document clustering groups similar texts based on their vector representations.",
              "dimensions": 1024,
              "encoding_format": "float"
            }'
        - lang: python
          label: 输入字符串列表
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如未配置环境变量，请用您的 API Key 替换此处。
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )

            completion = client.embeddings.create(
              model="text-embedding-v4",
              input=['Semantic search finds documents by meaning rather than exact keyword matching.', 'Text embeddings map words and sentences into high-dimensional vector spaces.', 'Retrieval-augmented generation combines search results with language models.', 'Document clustering groups similar texts based on their vector representations.'],
              dimensions=1024,
              encoding_format="float"
            )

            print(completion.model_dump_json())
        - lang: java
          label: 输入字符串列表
          source: |
            import java.net.URI;
            import java.net.http.HttpClient;
            import java.net.http.HttpRequest;
            import java.net.http.HttpResponse;
            import java.util.HashMap;
            import java.util.Map;
            import java.util.List;
            import java.util.Arrays;
            import com.alibaba.dashscope.utils.JsonUtils;

            public final class Main {
              public static void main(String[] args) {
                /** 从环境变量中获取 API Key。如未配置，请用您的 API Key 替换此处。 */
                String apiKey = System.getenv("DASHSCOPE_API_KEY");
                if (apiKey == null) {
                  System.out.println("DASHSCOPE_API_KEY not found in environment variables");
                  return;
                }
                String baseUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings";
                HttpClient client = HttpClient.newHttpClient();
                Map<String, Object> requestBody = new HashMap<>();
                requestBody.put("model", "text-embedding-v4");
                List<String> inputList = Arrays.asList("Semantic search finds documents by meaning rather than exact keyword matching.", "Text embeddings map words and sentences into high-dimensional vector spaces.", "Retrieval-augmented generation combines search results with language models.", "Document clustering groups similar texts based on their vector representations.");
                requestBody.put("input", inputList);
                requestBody.put("encoding_format", "float");

                try {
                  /** 将请求体转换为 JSON 字符串。 */
                  String requestBodyString = JsonUtils.toJson(requestBody);

                  /** 构建 HTTP 请求。 */
                  HttpRequest request = HttpRequest.newBuilder()
                      .uri(URI.create(baseUrl))
                      .header("Content-Type", "application/json")
                      .header("Authorization", "Bearer " + apiKey)
                      .POST(HttpRequest.BodyPublishers.ofString(requestBodyString))
                      .build();

                  /** 发送请求并接收响应。 */
                  HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                  if (response.statusCode() == 200) {
                    System.out.println("Response: " + response.body());
                  } else {
                    System.out.printf("Failed to retrieve response, status code: %d, response: %s%n", response.statusCode(), response.body());
                  }
                } catch (Exception e) {
                  /** 捕获并打印异常。 */
                  System.err.println("Error: " + e.getMessage());
                }
              }
            }
        - lang: bash
          label: 输入字符串列表
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "text-embedding-v4",
              "input": [
                "Semantic search finds documents by meaning rather than exact keyword matching.",
                "Text embeddings map words and sentences into high-dimensional vector spaces.",
                "Retrieval-augmented generation combines search results with language models.",
                "Document clustering groups similar texts based on their vector representations."
                ],
              "dimensions": 1024,
              "encoding_format": "float"
            }'
        - lang: python
          label: 输入文件
          source: |
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如未配置环境变量，请用您的 API Key 替换此处。
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            # 请将 'texts_to_embedding.txt' 替换为您自己的文件名或路径。
            with open('texts_to_embedding.txt', 'r', encoding='utf-8') as f:
              completion = client.embeddings.create(
                model="text-embedding-v4",
                input=f,
                encoding_format="float"
              )
            print(completion.model_dump_json())
        - lang: java
          label: 输入文件
          source: |
            import java.net.URI;
            import java.net.http.HttpClient;
            import java.net.http.HttpRequest;
            import java.net.http.HttpResponse;
            import java.util.HashMap;
            import java.util.Map;
            import java.io.BufferedReader;
            import java.io.FileReader;
            import java.io.IOException;
            import com.alibaba.dashscope.utils.JsonUtils;

            public class Main {
              public static void main(String[] args) {
                /** 从环境变量中获取 API Key。如未配置，请用您的 API Key 替换此处。 */
                String apiKey = System.getenv("DASHSCOPE_API_KEY");
                if (apiKey == null) {
                  System.out.println("DASHSCOPE_API_KEY not found in environment variables");
                  return;
                }
                String baseUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings";
                HttpClient client = HttpClient.newHttpClient();

                /** 读取输入文件。 */
                StringBuilder inputText = new StringBuilder();
                try (BufferedReader reader = new BufferedReader(new FileReader("<path_to_your_content_root>"))) {
                  String line;
                  while ((line = reader.readLine()) != null) {
                    inputText.append(line).append("\n");
                  }
                } catch (IOException e) {
                  System.err.println("Error reading input file: " + e.getMessage());
                  return;
                }

                Map<String, Object> requestBody = new HashMap<>();
                requestBody.put("model", "text-embedding-v4");
                requestBody.put("input", inputText.toString().trim());
                requestBody.put("dimensions", 1024);
                requestBody.put("encoding_format", "float");

                try {
                  String requestBodyString = JsonUtils.toJson(requestBody);

                  /** 构建 HTTP 请求。 */
                  HttpRequest request = HttpRequest.newBuilder()
                      .uri(URI.create(baseUrl))
                      .header("Content-Type", "application/json")
                      .header("Authorization", "Bearer " + apiKey)
                      .POST(HttpRequest.BodyPublishers.ofString(requestBodyString))
                      .build();
                  HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                  if (response.statusCode() == 200) {
                    System.out.println("Response: " + response.body());
                  } else {
                    System.out.printf("Failed to retrieve response, status code: %d, response: %s%n", response.statusCode(), response.body());
                  }
                } catch (Exception e) {
                  System.err.println("Error: " + e.getMessage());
                }
              }
            }
        - lang: bash
          label: 输入文件
          source: |-
            FILE_CONTENT=$(cat texts_to_embedding.txt | jq -Rs .)
            curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "text-embedding-v4",
              "input": ['"$FILE_CONTENT"'],
              "dimensions": 1024,
              "encoding_format": "float"
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
