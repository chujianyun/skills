> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-OCR 文字提取模型

> 通过 DashScope 原生 HTTP API 调用 Qwen-OCR 文字提取模型。

## OpenAPI

````yaml post /api/v1/services/aigc/multimodal-generation/generation
openapi: 3.1.0
info:
  title: Qwen-OCR 文字提取 API
  description: Qwen-OCR 文字提取模型的 API 参考文档，支持 OpenAI 兼容协议和 DashScope 协议。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 北京
security:
  - bearer: []
paths:
  /api/v1/services/aigc/multimodal-generation/generation:
    post:
      operationId: ocrDashScopeGeneration
      summary: 文字提取（DashScope）
      description: 使用 DashScope API 调用 Qwen-OCR 文字提取模型，支持内置 OCR 任务，包括通用文字识别、信息提取、文档解析、表格解析、公式识别和多语言识别。
      security:
        - bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DashScopeRequest"
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeResponse"
      x-codeSamples:
        - lang: python
          label: 高精度识别
          source: |-
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [{
                  "role": "user",
                  "content": [{
                    "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                    # 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                    "min_pixels": 32 * 32 * 3,
                    # 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                    "max_pixels": 32 * 32 * 8192,
                    # 指定是否开启图像自动旋转。
                    "enable_rotate": False}]
                  }]

            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.5-ocr',
              messages=messages,
              # 将内置任务设置为高精度识别。
              ocr_options={"task": "advanced_recognition"}
            )
            # 高精度识别任务以纯文本形式返回结果。
            print(response["output"]["choices"][0]["message"].content[0]["text"])
        - lang: java
          label: 高精度识别
          source: |-
            // dashscope SDK 版本 >= 2.21.8
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels", 3072);
                // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                // 配置内置 OCR 任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.ADVANCED_RECOGNITION)
                    .build();
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 高精度识别
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '
            {
              "model": "qwen3.5-ocr",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                        "min_pixels": 3072,
                        "max_pixels": 8388608,
                        "enable_rotate": false
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "ocr_options": {
                  "task": "advanced_recognition"
                }
              }
            }
            '
        - lang: python
          label: 信息提取
          source: |-
            # 使用 [pip install -U dashscope] 更新 SDK

            import os
            import dashscope
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [
                  {
                    "role":"user",
                    "content":[
                      {
                          "image":"http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg",
                          "min_pixels": 3072,
                          "max_pixels": 8388608,
                          "enable_rotate": False
                      }
                    ]
                  }
                ]

            params = {
              "ocr_options":{
                "task": "key_information_extraction",
                "task_config": {
                  "result_schema": {
                      "Ride Date": "Corresponds to the ride date and time in the image, in the format YYYY-MM-DD, for example, 2025-03-05",
                      "Invoice Code": "Extract the invoice code from the image, usually a combination of numbers or letters",
                      "Invoice Number": "Extract the number from the invoice, usually composed of only digits."
                  }
                }
              }
            }

            response = dashscope.MultiModalConversation.call(
                api_key=os.getenv('DASHSCOPE_API_KEY'),
                model='qwen3.5-ocr',
                messages=messages,
                **params)

            print(response.output.choices[0].message.content[0]["ocr_result"])
        - lang: java
          label: 信息提取
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.google.gson.JsonObject;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels", 3072);
                     // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();

                // 创建结果 schema 的 JSON 对象。
                JsonObject resultSchema = new JsonObject();
                resultSchema.addProperty("Ride Date", "Corresponds to the ride date and time in the image, in the format YYYY-MM-DD, for example, 2025-03-05");
                resultSchema.addProperty("Invoice Code", "Extract the invoice code from the image, usually a combination of numbers or letters");
                resultSchema.addProperty("Invoice Number", "Extract the number from the invoice, usually composed of only digits.");

                // 配置内置 OCR 任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.KEY_INFORMATION_EXTRACTION)
                    .taskConfig(OcrOptions.TaskConfig.builder()
                        .resultSchema(resultSchema)
                        .build())
                    .build();

                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("ocr_result"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 信息提取
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '
            {
              "model": "qwen3.5-ocr",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg",
                        "min_pixels": 3072,
                        "max_pixels": 8388608,
                        "enable_rotate": false
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "ocr_options": {
                  "task": "key_information_extraction",
                  "task_config": {
                    "result_schema": {
                        "Ride Date": "Corresponds to the ride date and time in the image, in the format YYYY-MM-DD, for example, 2025-03-05",
                        "Invoice Code": "Extract the invoice code from the image, usually a combination of numbers or letters",
                        "Invoice Number": "Extract the number from the invoice, usually composed of only digits."
                    }
                }
                }
              }
            }
            '
        - lang: python
          label: 表格解析
          source: |-
            import os
            import dashscope
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [{
                  "role": "user",
                  "content": [{
                    "image": "http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/doc_parsing/tables/photo/eng/17.jpg",
                    # 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                    "min_pixels": 32 * 32 * 3,
                    # 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                    "max_pixels": 32 * 32 * 8192,
                    # 指定是否开启图像自动旋转。
                    "enable_rotate": False}]
                       }]

            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.5-ocr',
              messages=messages,
              # 将内置任务设置为表格解析。
              ocr_options= {"task": "table_parsing"}
            )
            # 表格解析任务以 HTML 格式返回结果。
            print(response["output"]["choices"][0]["message"].content[0]["text"])
        - lang: java
          label: 表格解析
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "https://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/doc_parsing/tables/photo/eng/17.jpg");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels",3072);
                // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                // 配置内置 OCR 任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.TABLE_PARSING)
                    .build();
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 表格解析
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '
            {
              "model": "qwen3.5-ocr",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/doc_parsing/tables/photo/eng/17.jpg",
                        "min_pixels": 3072,
                        "max_pixels": 8388608,
                        "enable_rotate": false
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "ocr_options": {
                  "task": "table_parsing"
                }
              }
            }
            '
        - lang: python
          label: 文档解析
          source: |-
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [{
                  "role": "user",
                  "content": [{
                    "image": "https://img.alicdn.com/imgextra/i1/O1CN01ukECva1cisjyK6ZDK_!!6000000003635-0-tps-1500-1734.jpg",
                    # 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                    "min_pixels": 32 * 32 * 3,
                    # 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                    "max_pixels": 32 * 32 * 8192,
                    # 指定是否开启图像自动旋转。
                    "enable_rotate": False}]
                  }]

            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.5-ocr',
              messages=messages,
              # 将内置任务设置为文档解析。
              ocr_options= {"task": "document_parsing"}
            )
            # 文档解析任务以 LaTeX 格式返回结果。
            print(response["output"]["choices"][0]["message"].content[0]["text"])
        - lang: java
          label: 文档解析
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "https://img.alicdn.com/imgextra/i1/O1CN01ukECva1cisjyK6ZDK_!!6000000003635-0-tps-1500-1734.jpg");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels", 3072);
                // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                // 配置内置 OCR 任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.DOCUMENT_PARSING)
                    .build();
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 文档解析
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'\
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"\
              --header 'Content-Type: application/json'\
              --data '{
            "model": "qwen3.5-ocr",
            "input": {
              "messages": [
                {
                  "role": "user",
                  "content": [{
                      "image": "https://img.alicdn.com/imgextra/i1/O1CN01ukECva1cisjyK6ZDK_!!6000000003635-0-tps-1500-1734.jpg",
                      "min_pixels": 3072,
                      "max_pixels": 8388608,
                      "enable_rotate": false
                    }
                  ]
                }
              ]
            },
            "parameters": {
              "ocr_options": {
                "task": "document_parsing"
              }
            }
            }
            '
        - lang: python
          label: 公式识别
          source: |-
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [{
              "role": "user",
              "content": [{
                "image": "http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/formula_handwriting/test/inline_5_4.jpg",
                # 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                "min_pixels": 32 * 32 * 3,
                # 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                "max_pixels": 32 * 32 * 8192,
                # 指定是否开启图像自动旋转。
                "enable_rotate": False
              }]
            }]

            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.5-ocr',
              messages=messages,
              # 将内置任务设置为公式识别。
              ocr_options= {"task": "formula_recognition"}
            )
            # 公式识别任务以 LaTeX 格式返回结果。
            print(response["output"]["choices"][0]["message"].content[0]["text"])
        - lang: java
          label: 公式识别
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/formula_handwriting/test/inline_5_4.jpg");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels", 3072);
                // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                // 配置内置 OCR 任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.FORMULA_RECOGNITION)
                    .build();
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 公式识别
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '
            {
              "model": "qwen3.5-ocr",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/formula_handwriting/test/inline_5_4.jpg",
                        "min_pixels": 3072,
                        "max_pixels": 8388608,
                        "enable_rotate": false
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "ocr_options": {
                  "task": "formula_recognition"
                }
              }
            }
            '
        - lang: python
          label: 通用文字识别
          source: |-
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [{
                  "role": "user",
                  "content": [{
                    "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                    # 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                    "min_pixels": 32 * 32 * 3,
                    # 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                    "max_pixels": 32 * 32 * 8192,
                    # 指定是否开启图像自动旋转。
                    "enable_rotate": False}]
                }]

            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.5-ocr',
              messages=messages,
              # 将内置任务设置为通用文字识别。
              ocr_options= {"task": "text_recognition"}
            )
            # 通用文字识别任务以纯文本格式返回结果。
            print(response["output"]["choices"][0]["message"].content[0]["text"])
        - lang: java
          label: 通用文字识别
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels", 3072);
                // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                // 配置内置任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.TEXT_RECOGNITION)
                    .build();
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 通用文字识别
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'\
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"\
              --header 'Content-Type: application/json'\
              --data '{
            "model": "qwen3.5-ocr",
            "input": {
              "messages": [
                {
                  "role": "user",
                  "content": [{
                      "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                      "min_pixels": 3072,
                      "max_pixels": 8388608,
                      "enable_rotate": false
                    }
                  ]
                }
              ]
            },
            "parameters": {
              "ocr_options": {
                  "task": "text_recognition"
                }
            }
            }'
        - lang: python
          label: 多语言识别
          source: |-
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [{
                  "role": "user",
                  "content": [{
                    "image": "https://img.alicdn.com/imgextra/i2/O1CN01VvUMNP1yq8YvkSDFY_!!6000000006629-2-tps-6000-3000.png",
                    # 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                    "min_pixels": 32 * 32 * 3,
                    # 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                    "max_pixels": 32 * 32 * 8192,
                    # 指定是否开启图像自动旋转。
                    "enable_rotate": False}]
                  }]

            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.5-ocr',
              messages=messages,
              # 将内置任务设置为多语言识别。
              ocr_options={"task": "multi_lan"}
            )
            # 多语言识别任务以纯文本形式返回结果。
            print(response["output"]["choices"][0]["message"].content[0]["text"])
        - lang: java
          label: 多语言识别
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.Map;
            import java.util.HashMap;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "https://img.alicdn.com/imgextra/i2/O1CN01VvUMNP1yq8YvkSDFY_!!6000000006629-2-tps-6000-3000.png");
                // 输入图像的最大像素阈值。如果图像大于该值，则图像会被缩小，直到总像素数小于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像小于该值，则图像会被放大，直到总像素数大于 min_pixels。
                map.put("min_pixels", 3072);
                // 指定是否开启图像自动旋转。
                map.put("enable_rotate", false);

                // 配置内置 OCR 任务。
                OcrOptions ocrOptions = OcrOptions.builder()
                    .task(OcrOptions.Task.MULTI_LAN)
                    .build();
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map
                        )).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .ocrOptions(ocrOptions)
                    .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 多语言识别
          source: |-
            # ======= 重要 =======
            # === 运行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '
            {
              "model": "qwen3.5-ocr",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "https://img.alicdn.com/imgextra/i2/O1CN01VvUMNP1yq8YvkSDFY_!!6000000006629-2-tps-6000-3000.png",
                        "min_pixels": 3072,
                        "max_pixels": 8388608,
                        "enable_rotate": false
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "ocr_options": {
                  "task": "multi_lan"
                }
              }
            }
            '
        - lang: python
          label: 流式输出
          source: |-
            import os
            import dashscope

            PROMPT_TICKET_EXTRACTION = """
            Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image.
            You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?).
            Return the data in JSON format as follows: {'invoice_number': 'xxx', 'departure_station': 'xxx', 'arrival_station': 'xxx', 'departure_date_and_time':'xxx', 'seat_number': 'xxx','ticket_price':'xxx', 'id_card_number': 'xxx', 'passenger_name': 'xxx'},
            """

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            messages = [
              {
                "role": "user",
                "content": [
                  {
                    "image": "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg",
                    # 输入图像的最小像素阈值。如果图像的像素数低于该值，则图像会被放大，直到总像素数超过 min_pixels。
                    "min_pixels": 32 * 32 * 3,
                    # 输入图像的最大像素阈值。如果图像的像素数超过该值，则图像会被缩小，直到总像素数低于 max_pixels。
                    "max_pixels": 32 * 32 * 8192},
                  # 未设置内置任务时，可在 text 字段中传入提示词。如果未传入提示词，则使用默认提示词：请输出图片中的文本内容，不要输出其他内容。
                  {
                    "type": "text",
                    "text": PROMPT_TICKET_EXTRACTION,
                  },
                ],
              }
            ]
            response = dashscope.MultiModalConversation.call(
              # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              model="qwen3.5-ocr",
              messages=messages,
              stream=True,
              incremental_output=True,
            )
            full_content = ""
            print("Streaming output content:")
            for response in response:
              try:
                print(response["output"]["choices"][0]["message"].content[0]["text"])
                full_content += response["output"]["choices"][0]["message"].content[0]["text"]
              except:
                pass
            print(f"Full content: {full_content}")
        - lang: java
          label: 流式输出
          source: |-
            import java.util.*;

            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import io.reactivex.Flowable;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {

              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }

              public static void simpleMultiModalConversationCall()
                  throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> map = new HashMap<>();
                map.put("image", "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg");
                // 输入图像的最大像素阈值。如果图像的像素数超过该值，则图像会被缩小，直到总像素数低于 max_pixels。
                map.put("max_pixels", 8388608);
                // 输入图像的最小像素阈值。如果图像的像素数低于该值，则图像会被放大，直到总像素数超过 min_pixels。
                map.put("min_pixels", 3072);
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(
                        map,
                        // 未设置内置任务时，可在 text 字段中传入提示词。如果未传入提示词，则使用默认提示词：请输出图片中的文本内容，不要输出其他内容。
                        Collections.singletonMap("text", "Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image. You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?). Return the data in JSON format as follows: {\'invoice_number\': \'xxx\', \'departure_station\': \'xxx\', \'arrival_station\': \'xxx\', \'departure_date_and_time\':\'xxx\', \'seat_number\': \'xxx\',\'ticket_price\':\'xxx\', \'id_card_number\': \'xxx\', \'passenger_name\': \'xxx\'"))).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-ocr")
                    .message(userMessage)
                    .incrementalOutput(true)
                    .build();
                Flowable<MultiModalConversationResult> result = conv.streamCall(param);
                result.blockingForEach(item -> {
                  try {
                    List<Map<String, Object>> contentList = item.getOutput().getChoices().get(0).getMessage().getContent();
                    if (!contentList.isEmpty()){
                      System.out.println(contentList.get(0).get("text"));
                    }//
                  } catch (Exception e){
                    System.exit(0);
                  }
                });
              }

              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: bash
          label: 流式输出
          source: |-
            # === 执行前请删除此注释 ===

            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            -H 'X-DashScope-SSE: enable' \
            --data '{
              "model": "qwen3.5-ocr",
              "input":{
                "messages":[
                      {
                  "role": "user",
                  "content": [
                    {
                      "image": "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg",
                      "min_pixels": 3072,
                      "max_pixels": 8388608
                    },
                    {"type": "text", "text": "Please extract the invoice number, train number, departure station, arrival station, departure date and time, seat number, seat class, ticket price, ID card number, and passenger name from the train ticket image. You must accurately extract the key information. Do not omit or fabricate information. Replace any single character that is blurry or obscured by strong light with an English question mark (?). Return the data in JSON format as follows: {\'invoice_number\': \'xxx\', \'departure_station\': \'xxx\', \'arrival_station\': \'xxx\', \'departure_date_and_time\':\'xxx\', \'seat_number\': \'xxx\',\'ticket_price\':\'xxx\', \'id_card_number\': \'xxx\', \'passenger_name\': \'xxx\'}"}
                  ]
                      }
                ]
              },
              "parameters": {
                "incremental_output": true
              }
            }'
components:
  securitySchemes:
    bearer:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    OpenAIRequest:
      type: object
      required:
        - model
        - messages
      properties:
        model:
          type: string
          description: 模型名称。支持的模型列表请参见 [Qwen-OCR](#)。
          example: qwen3.5-ocr
        messages:
          type: array
          description: 按对话顺序向模型提供上下文的消息序列。
          items:
            type: object
            title: 用户消息
            description: 包含指令和图像的用户消息，供模型处理。
            required:
              - role
              - content
            properties:
              role:
                type: string
                description: 用户消息的角色，值必须为 `user`。
                enum:
                  - user
              content:
                type: array
                description: 消息内容。
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: 内容类型。文本输入使用 `text`，图像输入使用 `image_url`。
                      enum:
                        - text
                        - image_url
                    text:
                      type: string
                      description: 输入文本。默认值：`Please output only the text content from the image without any additional descriptions or formatting.`
                    image_url:
                      type: object
                      description: 输入图像的相关信息。当 type 为 `image_url` 时必填。
                      properties:
                        url:
                          type: string
                          description: 图像的 URL 或 Base64 编码的 Data URL。有关传入本地文件的更多信息，请参见文字提取。
                      required:
                        - url
                    min_pixels:
                      type: integer
                      description: |-
                        输入图像的最小像素阈值（单位：像素）。如果输入图像的像素数低于 min_pixels，则图像会被放大，直到总像素数超过 min_pixels。

                        **图像 token 与像素的换算关系：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                        **取值范围：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：默认值和最小值为 3072（3×32×32）。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值和最小值为 3136（4×28×28）。
                    max_pixels:
                      type: integer
                      description: |-
                        输入图像的最大像素阈值（单位：像素）。如果输入图像的像素数在 [min_pixels, max_pixels] 范围内，模型将直接处理原始图像，不进行缩放。如果像素数超过 max_pixels，则图像会被缩小，直到像素数小于 max_pixels。

                        **图像 token 与像素的换算关系：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                        **取值范围：**
                        - qwen3.5-ocr、qwen-vl-ocr-latest：默认值 8388608（8192×32×32），最大值 30720000（30000×32×32）。
                        - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值 6422528（8192×28×28），最大值 23520000（30000×28×28）。
        stream:
          type: boolean
          default: false
          description: 指定是否以流式模式返回响应。`false`：一次性返回完整响应。`true`：随模型生成过程逐块返回数据。
        stream_options:
          type: object
          description: 流式输出的配置项，仅在 `stream` 为 `true` 时生效。
          properties:
            include_usage:
              type: boolean
              default: false
              description: 是否在流式输出的最后一个数据块中包含 token 用量信息。
        max_tokens:
          type: integer
          description: |-
            输出的最大 token 数。如果生成内容超过该值，响应将被截断。

            - 对于 qwen3.5-ocr、qwen-vl-ocr-latest 和 qwen-vl-ocr-2024-10-28，默认值和最大值与模型的最大输出长度相同。
            - 对于 qwen-vl-ocr、qwen-vl-ocr-2025-04-13 和 qwen-vl-ocr-2025-08-28，默认值和最大值均为 4096。
        logprobs:
          type: boolean
          default: false
          description: 指定是否返回输出 token 的对数概率。
        top_logprobs:
          type: integer
          default: 0
          description: 指定每个生成步骤中返回的最可能 token 数量。取值范围：[0, 5]。仅在 `logprobs` 为 `true` 时生效。
        temperature:
          type: number
          default: 0.01
          description: 采样温度，控制生成文本的多样性。值越高越多样，值越低越确定。取值范围：[0, 2)。`temperature` 和 `top_p` 只能设置其中之一。
        top_p:
          type: number
          default: 0.001
          description: 核采样的概率阈值。值越高越多样，值越低越确定。取值范围：(0, 1.0]。`temperature` 和 `top_p` 只能设置其中之一。
        top_k:
          type: integer
          default: 1
          description: '采样候选集大小。值越大随机性越高。若为 None 或大于 100，则仅 `top_p` 生效。必须 >= 0。非标准 OpenAI 参数，Python SDK 中请使用 `extra_body={"top_k": xxx}`。'
        repetition_penalty:
          type: number
          default: 1
          description: 重复序列的惩罚系数。值越高越能减少重复。1.0 表示不惩罚。
        presence_penalty:
          type: number
          default: 0
          description: 控制内容重复程度。取值范围：[-2.0, 2.0]。正值减少重复，负值增加重复。
        seed:
          type: integer
          description: 用于复现结果的随机数种子。取值范围：[0, 2^31−1]。
        stop:
          description: 停止词。当出现指定字符串或 token_id 时，立即停止生成。可以是字符串或数组。stop 为数组时，不能混用 token_id 和字符串。
          oneOf:
            - type: string
            - type: array
              items:
                type: string
    OpenAIResponse:
      type: object
      properties:
        id:
          type: string
          description: 本次请求的唯一标识符。
        choices:
          type: array
          items:
            type: object
            properties:
              finish_reason:
                type: string
                description: 模型停止生成的原因。完成时为 `stop`，截断时为 `length`。
                enum:
                  - stop
                  - length
              index:
                type: integer
                description: 在 choices 数组中的索引。
              logprobs:
                type: object
                nullable: true
                description: 对数概率信息。除非启用 `logprobs`，否则为 null。
              message:
                type: object
                properties:
                  content:
                    type: string
                    description: 模型返回的内容。
                  processed_text:
                    type: string
                    description: 对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。
                  refusal:
                    type: string
                    nullable: true
                    description: 始终为 null。
                  role:
                    type: string
                    description: 始终为 `assistant`。
                    enum:
                      - assistant
                  audio:
                    type: object
                    nullable: true
                    description: 始终为 null。
                  function_call:
                    type: object
                    nullable: true
                    description: 始终为 null。
                  tool_calls:
                    type: array
                    nullable: true
                    description: 始终为 null。
                  annotations:
                    type:
                      - array
                      - "null"
                    description: 预留字段，当前为 null。
        created:
          type: integer
          description: 本次请求创建时的 UNIX 时间戳。
        model:
          type: string
          description: 本次请求使用的模型。
        object:
          type: string
          description: 始终为 `chat.completion`。
          enum:
            - chat.completion
        service_tier:
          type: string
          nullable: true
          description: 始终为 null。
        system_fingerprint:
          type: string
          nullable: true
          description: 始终为 null。
        usage:
          type: object
          description: Token 用量信息。
          properties:
            completion_tokens:
              type: integer
              description: 模型输出的 token 数量。
            prompt_tokens:
              type: integer
              description: 输入的 token 数量。
            total_tokens:
              type: integer
              description: prompt_tokens 和 completion_tokens 的总和。
            completion_tokens_details:
              type: object
              properties:
                accepted_prediction_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                audio_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                reasoning_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                text_tokens:
                  type: integer
                  description: 文本输出的 token 数量。
                rejected_prediction_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
            prompt_tokens_details:
              type: object
              properties:
                audio_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                cached_tokens:
                  type: integer
                  nullable: true
                  description: 始终为 null。
                image_tokens:
                  type: integer
                  description: 图像输入的 token 数量。
                text_tokens:
                  type: integer
                  description: 文本输入的 token 数量。
    OpenAIStreamResponse:
      type: object
      properties:
        id:
          type: string
          description: 本次调用的唯一标识符，每个数据块的 id 相同。
        choices:
          type: array
          description: 生成的内容。当 `include_usage` 为 true 时，最后一个数据块的 choices 为空。
          items:
            type: object
            properties:
              delta:
                type: object
                description: 流式模式下返回的输出内容。
                properties:
                  content:
                    type: string
                    description: 模型返回的内容。
                  processed_text:
                    type: string
                    description: 对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。
                  function_call:
                    type: object
                    nullable: true
                    description: 当前为 null。
                  refusal:
                    type: object
                    nullable: true
                    description: 当前为 null。
                  role:
                    type: string
                    description: 消息的角色，仅在第一个数据块中出现。
              finish_reason:
                type: string
                nullable: true
                description: 生成完成时为 `stop`，生成中为 `null`，截断时为 `length`。
              index:
                type: integer
              logprobs:
                type: object
                nullable: true
        created:
          type: integer
          description: UNIX 时间戳，每个数据块相同。
        model:
          type: string
        object:
          type: string
          description: 始终为 `chat.completion.chunk`。
          enum:
            - chat.completion.chunk
        service_tier:
          type: string
          nullable: true
          description: 当前为 null。
        system_fingerprint:
          type: string
          nullable: true
          description: 当前为 null。
        usage:
          type: object
          nullable: true
          description: Token 用量，仅在 `include_usage` 为 true 时的最后一个数据块中出现。
          properties:
            completion_tokens:
              type: integer
            prompt_tokens:
              type: integer
            total_tokens:
              type: integer
            completion_tokens_details:
              type: object
              properties:
                accepted_prediction_tokens:
                  type: integer
                  nullable: true
                audio_tokens:
                  type: integer
                  nullable: true
                reasoning_tokens:
                  type: integer
                  nullable: true
                text_tokens:
                  type: integer
                rejected_prediction_tokens:
                  type: integer
                  nullable: true
            prompt_tokens_details:
              type: object
              properties:
                audio_tokens:
                  type: integer
                  nullable: true
                cached_tokens:
                  type: integer
                  nullable: true
                image_tokens:
                  type: integer
                text_tokens:
                  type: integer
    DashScopeRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。支持的模型列表请参见 [Qwen-OCR](#)。
          example: qwen3.5-ocr
        input:
          type: object
          required:
            - messages
          description: 包含消息的输入对象。
          properties:
            messages:
              type: array
              description: 以消息序列形式提供给模型的上下文。
              items:
                type: object
                title: 用户消息
                description: 包含图像和可选文本的用户消息。
                required:
                  - role
                  - content
                properties:
                  role:
                    type: string
                    enum:
                      - user
                    description: 必须为 `user`。
                  content:
                    type: array
                    description: 消息内容，图像输入使用数组格式。
                    items:
                      type: object
                      properties:
                        text:
                          type: string
                          description: 输入文本。默认值：`Please output only the text content from the image without any additional descriptions or formatting.`
                        image:
                          type: string
                          description: 图像的 URL、Base64 Data URL 或本地路径。有关传入本地文件的更多信息，请参见传入本地文件。
                        enable_rotate:
                          type: boolean
                          default: false
                          description: 是否对倾斜图像进行校正。
                        min_pixels:
                          type: integer
                          description: |-
                            输入图像的最小像素阈值（单位：像素）。如果输入图像的像素数低于 min_pixels，则图像会被放大，直到总像素数超过 min_pixels。

                            **图像 token 与像素的换算关系：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                            **取值范围：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：默认值和最小值为 3072（3×32×32）。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值和最小值为 3136（4×28×28）。
                        max_pixels:
                          type: integer
                          description: |-
                            输入图像的最大像素阈值（单位：像素）。如果输入图像的像素数在 [min_pixels, max_pixels] 范围内，模型将直接处理原始图像，不进行缩放。如果像素数超过 max_pixels，则图像会被缩小，直到像素数小于 max_pixels。

                            **图像 token 与像素的换算关系：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：每个 token 对应 32×32 像素。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：每个 token 对应 28×28 像素。

                            **取值范围：**
                            - qwen3.5-ocr、qwen-vl-ocr-latest：默认值 8388608（8192×32×32），最大值 30720000（30000×32×32）。
                            - qwen-vl-ocr、qwen-vl-ocr-2025-08-28 及更早版本：默认值 6422528（8192×28×28），最大值 23520000（30000×28×28）。
        parameters:
          type: object
          description: 模型参数。
          properties:
            ocr_options:
              type: object
              description: 内置 OCR 任务的配置项。使用内置任务时，模型会使用默认提示词，无需在用户消息中传入文本。最低 SDK 版本要求：Python 1.22.2，Java 2.18.4。
              properties:
                task:
                  type: string
                  description: 内置任务名称。
                  enum:
                    - text_recognition
                    - key_information_extraction
                    - document_parsing
                    - table_parsing
                    - formula_recognition
                    - multi_lan
                    - advanced_recognition
                task_config:
                  type: object
                  description: "`key_information_extraction` 任务的配置项，用于指定要提取的字段。如果省略，则提取所有字段。"
                  properties:
                    result_schema:
                      type: object
                      description: 指定要提取字段的 JSON 对象。键为字段名，值为字段描述或格式要求。最多支持 3 层嵌套。
                      additionalProperties:
                        type: string
            max_tokens:
              type: integer
              description: |-
                输出的最大 token 数。如果生成内容超过该值，响应将被截断。

                - 对于 qwen3.5-ocr、qwen-vl-ocr-latest 和 qwen-vl-ocr-2024-10-28，默认值和最大值与模型的最大输出长度相同。
                - 对于 qwen-vl-ocr、qwen-vl-ocr-2025-04-13 和 qwen-vl-ocr-2025-08-28，默认值和最大值均为 4096。
            seed:
              type: integer
              description: 用于复现结果的随机数种子。取值范围：[0, 2^31−1]。
            temperature:
              type: number
              default: 0.01
              description: 采样温度。值越高越多样，值越低越确定。取值范围：[0, 2)。`temperature` 和 `top_p` 只能设置其中之一。
            top_p:
              type: number
              default: 0.001
              description: 核采样阈值。取值范围：(0, 1.0]。`temperature` 和 `top_p` 只能设置其中之一。
            top_k:
              type: integer
              default: 1
              description: 采样候选集大小。值越大随机性越高。必须 >= 0。
            repetition_penalty:
              type: number
              default: 1
              description: 重复序列的惩罚系数。1.0 表示不惩罚。
            presence_penalty:
              type: number
              default: 0
              description: 控制内容重复程度。取值范围：[-2.0, 2.0]。
            stop:
              description: 停止词。可以是字符串或数组。stop 为数组时，不能混用 token_id 和字符串。
              oneOf:
                - type: string
                - type: array
                  items:
                    type: string
            logprobs:
              type: boolean
              default: false
              description: 是否返回对数概率。支持的版本：qwen-vl-ocr-2025-04-13 及更高版本。
            top_logprobs:
              type: integer
              default: 0
              description: 每个生成步骤中返回的最可能 token 数量。取值范围：[0, 5]。仅在 `logprobs` 为 true 时生效。
            incremental_output:
              type: boolean
              default: false
              description: 流式输出时，`true` 表示每个数据块仅返回新生成的内容；`false` 表示返回累积的完整内容。
            stream:
              type: boolean
              default: false
              description: |-
                指定是否流式返回响应。

                - Python SDK：在调用时设置 `stream=True`。
                - Java SDK：使用 `streamCall` 接口。
                - HTTP：在请求头中设置 `X-DashScope-SSE: enable`。
    DashScopeResponse:
      type: object
      properties:
        status_code:
          type: integer
          description: 请求状态码。200 表示成功。Java SDK 不返回此字段。
        request_id:
          type: string
          description: 本次调用的唯一标识符。Java SDK 返回 `requestId`。
        code:
          type: string
          description: 错误码。成功时为空。仅由 Python SDK 返回。
        message:
          type: string
          description: 错误信息。成功时为空。
        output:
          type: object
          description: 调用结果信息。
          properties:
            text:
              type: string
              nullable: true
              description: 当前固定为 null。
            finish_reason:
              type: string
              nullable: true
              description: 生成中为 `null`，完成时为 `stop`，截断时为 `length`。
            choices:
              type: array
              description: 模型输出。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    nullable: true
                    description: 生成中为 `null`，完成时为 `stop`，截断时为 `length`。
                  message:
                    type: object
                    properties:
                      role:
                        type: string
                        description: 始终为 `assistant`。
                        enum:
                          - assistant
                      content:
                        type: array
                        description: 输出消息内容。
                        items:
                          type: object
                          properties:
                            text:
                              type: string
                              description: 输出的文本内容。
                            processed_text:
                              type: string
                              description: 对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。
                            ocr_result:
                              type: object
                              description: 信息提取（`key_information_extraction`）和高精度识别（`advanced_recognition`）任务的返回结果。
                              properties:
                                kv_result:
                                  type: object
                                  description: 信息提取任务的结果。
                                  additionalProperties:
                                    type: string
                                words_info:
                                  type: array
                                  description: 高精度识别任务的结果。
                                  items:
                                    type: object
                                    properties:
                                      rotate_rect:
                                        type: array
                                        description: 旋转矩形 [center_x, center_y, width, height, angle]。angle 取值范围：[-90, 90]。
                                        items:
                                          type: number
                                      location:
                                        type: array
                                        description: 四顶点坐标 [x1,y1,x2,y2,x3,y3,x4,y4]，从左上角顺时针排列。
                                        items:
                                          type: number
                                      text:
                                        type: string
                                        description: 文本行内容。
                      logprobs:
                        type: object
                        nullable: true
                        description: 对数概率信息。
                        properties:
                          content:
                            type: array
                            items:
                              type: object
                              properties:
                                token:
                                  type: string
                                bytes:
                                  type: array
                                  items:
                                    type: integer
                                  description: token 的 UTF-8 字节序列。
                                logprob:
                                  type: number
                                  nullable: true
                                top_logprobs:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      token:
                                        type: string
                                      bytes:
                                        type: array
                                        items:
                                          type: integer
                                      logprob:
                                        type: number
                                        nullable: true
        usage:
          type: object
          description: Token 用量信息。
          properties:
            input_tokens:
              type: integer
              description: 输入 token 数量。
            output_tokens:
              type: integer
              description: 输出 token 数量。
            total_tokens:
              type: integer
              description: input_tokens 和 output_tokens 的总和。
            characters:
              type: integer
              description: 当前固定为 0。
            image_tokens:
              type: integer
              description: 图像输入的 token 数量。
            input_tokens_details:
              type: object
              properties:
                image_tokens:
                  type: integer
                  description: 图像输入的 token 数量。
                text_tokens:
                  type: integer
                  description: 文本输入的 token 数量。
            output_tokens_details:
              type: object
              properties:
                text_tokens:
                  type: integer
                  description: 模型输出的 token 数量。
````
