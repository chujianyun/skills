> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# GUI-Plus DashScope

> 通过 DashScope 原生 HTTP API 调用 GUI-Plus 界面交互专用模型。

## OpenAPI

````yaml post /api/v1/services/aigc/multimodal-generation/generation
openapi: 3.1.0
info:
  title: GUI-Plus DashScope API
  description: 通过 DashScope 原生 HTTP API 调用 GUI-Plus 界面交互专用模型，支持流式输出和多模态输入（图片）。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 中国
security:
  - ApiKeyAuth: []
paths:
  /api/v1/services/aigc/multimodal-generation/generation:
    post:
      operationId: guiPlusDashscopeGeneration
      summary: GUI-Plus 多模态生成
      description: |-
        通过 DashScope 原生 HTTP API 向 GUI-Plus 界面交互专用模型发送消息并获取生成回复。支持多轮对话和流式输出。

        如需通过 HTTP 实现流式输出，请添加 `X-DashScope-SSE: enable` 请求头。

        GUI-Plus 模型通过系统提示中嵌入的 `computer_use` 工具函数来控制界面交互，返回包含操作指令的 JSON。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/GuiPlusDashScopeRequest"
            example:
              model: gui-plus-2026-02-26
              input:
                messages:
                  - role: system
                    content:
                      - text: You are a helpful GUI assistant.
                  - role: user
                    content:
                      - image: https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png
                      - text: 帮我打开浏览器
              parameters:
                vl_high_resolution_images: true
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GuiPlusDashScopeResponse"
              example:
                status_code: 200
                request_id: b74b3a25-3968-4059-8c44-63d793c07f02
                code: ""
                message: ""
                output:
                  text: null
                  finish_reason: null
                  choices:
                    - finish_reason: stop
                      message:
                        role: assistant
                        content:
                          - text: |-
                              ```json
                              {"thought": "用户想要打开浏览器，我观察到屏幕截图中有一个Google Chrome的图标，其位置在右上角一排的最后一个。因此，下一步操作应该是点击这个Chrome浏览器图标来启动它。", "action": "CLICK", "parameters": {"x": 1086, "y": 127}}
                              ```
                  audio: null
                usage:
                  input_tokens: 2021
                  output_tokens: 78
                  characters: 0
                  image_tokens: 1244
                  input_tokens_details:
                    image_tokens: 1244
                    text_tokens: 777
                  output_tokens_details:
                    text_tokens: 78
                  total_tokens: 2099
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeError"
              example:
                status_code: 400
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                code: InvalidParameter
                message: The request body is invalid.
        "401":
          description: 身份验证失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeError"
              example:
                status_code: 401
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                code: InvalidApiKey
                message: Invalid API-key provided.
        "429":
          description: 超出速率限制
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeError"
              example:
                status_code: 429
                request_id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
                code: Throttling
                message: Requests rate limit exceeded.
      x-codeSamples:
        - lang: python
          label: 非流式
          source: |-
            import os
            import dashscope

            system_prompt = """# Tools

            You may call one or more functions to assist with the user query.

            You are provided with function signatures within <tools></tools> XML tags:
            <tools>
            {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\n* The screen's resolution is 1000x1000.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\n* `type`: Type a string of text on the keyboard.\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\n* `scroll`: Performs a scroll of the mouse scroll wheel.\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\n* `wait`: Wait specified seconds for the change to happen.\n* `terminate`: Terminate the current task and report its completion status.\n* `answer`: Answer a question.\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
            </tools>

            For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
            <tool_call>
            {"name": <function-name>, "arguments": <args-json-object>}
            </tool_call>

            # Response format

            Response format for every step:
            1) Action: a short imperative describing what to do in the UI.
            2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

            Rules:
            - Output exactly in the order: Action, <tool_call>.
            - Be brief: one for Action.
            - Do not output anything else outside those two parts.
            - If finishing, use action=terminate in the tool call."""

            messages = [
              {
                "role": "system",
                "content": system_prompt
              },
              {
                "role": "user",
                "content": [
                  {"image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"},
                  {"text": "帮我打开浏览器。"}]
              }]

            response = dashscope.MultiModalConversation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='gui-plus-2026-02-26',
              messages=messages,
              vl_high_resolution_images=True
            )

            print(response.output.choices[0].message.content[0]["text"])
        - lang: java
          label: 非流式
          source: |-
            import java.util.Arrays;
            import java.util.Collections;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;

            public class Main {
                public static void simpleMultiModalConversationCall()
                        throws ApiException, NoApiKeyException, UploadFileException {
                    String systemPrompt = "# Tools\n\n" +
                            "You may call one or more functions to assist with the user query.\n\n" +
                            "You are provided with function signatures within <tools></tools> XML tags:\n" +
                            "<tools>\n" +
                            "{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n" +
                            "</tools>\n\n" +
                            "For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n" +
                            "<tool_call>\n" +
                            "{\"name\": <function-name>, \"arguments\": <args-json-object>}\n" +
                            "</tool_call>\n\n" +
                            "# Response format\n\n" +
                            "Response format for every step:\n" +
                            "1) Action: a short imperative describing what to do in the UI.\n" +
                            "2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\n" +
                            "Rules:\n" +
                            "- Output exactly in the order: Action, <tool_call>.\n" +
                            "- Be brief: one for Action.\n" +
                            "- Do not output anything else outside those two parts.\n" +
                            "- If finishing, use action=terminate in the tool call.";
                    MultiModalConversation conv = new MultiModalConversation();
                    MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                            .content(Arrays.asList(
                                    Collections.singletonMap("text",systemPrompt))).build();
                    MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                            .content(Arrays.asList(
                                    Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"),
                                    Collections.singletonMap("text", "帮我打开浏览器。"))).build();
                    MultiModalConversationParam param = MultiModalConversationParam.builder()
                            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                            .model("gui-plus-2026-02-26")
                            .messages(Arrays.asList(systemMsg,userMessage))
                            .vlHighResolutionImages(true)
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
        - lang: curl
          label: 非流式
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H "Content-Type: application/json" \
              -d '{
                "model": "gui-plus-2026-02-26",
                "input": {
                  "messages": [
                    {
                      "role": "system",
                      "content": [
                        {
                          "text": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
                        }
                      ]
                    },
                    {
                      "role": "user",
                      "content": [
                        {
                          "image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
                        },
                        {
                          "text": "帮我打开浏览器"
                        }
                      ]
                    }
                  ]
                },
                "parameters": {
                  "vl_high_resolution_images": true
                }
              }'
        - lang: python
          label: 流式输出
          source: |-
            import os
            import dashscope

            system_prompt = """# Tools

            You may call one or more functions to assist with the user query.

            You are provided with function signatures within <tools></tools> XML tags:
            <tools>
            {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\n* The screen's resolution is 1000x1000.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\n* `type`: Type a string of text on the keyboard.\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\n* `scroll`: Performs a scroll of the mouse scroll wheel.\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\n* `wait`: Wait specified seconds for the change to happen.\n* `terminate`: Terminate the current task and report its completion status.\n* `answer`: Answer a question.\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
            </tools>

            For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
            <tool_call>
            {"name": <function-name>, "arguments": <args-json-object>}
            </tool_call>

            # Response format

            Response format for every step:
            1) Action: a short imperative describing what to do in the UI.
            2) A single <tool_call>...</tool_call> block containing only the JSON: {"name": <function-name>, "arguments": <args-json-object>}.

            Rules:
            - Output exactly in the order: Action, <tool_call>.
            - Be brief: one for Action.
            - Do not output anything else outside those two parts.
            - If finishing, use action=terminate in the tool call."""

            messages = [
              {
                "role": "system",
                "content": system_prompt
              },
              {
                "role": "user",
                "content": [
                  {"image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"},
                  {"text": "帮我打开浏览器。"}]
              }]

            response = dashscope.MultiModalConversation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='gui-plus-2026-02-26',
              messages=messages,
              vl_high_resolution_images=True,
              stream=True
            )
            for chunk in response:
              print(chunk)
        - lang: java
          label: 流式输出
          source: |-
            import java.util.Arrays;
            import java.util.Collections;

            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import io.reactivex.Flowable;

            public class Main {

                public static void streamCall()
                        throws ApiException, NoApiKeyException, UploadFileException {
                    String systemPrompt = "# Tools\n\n" +
                            "You may call one or more functions to assist with the user query.\n\n" +
                            "You are provided with function signatures within <tools></tools> XML tags:\n" +
                            "<tools>\n" +
                            "{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n" +
                            "</tools>\n\n" +
                            "For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n" +
                            "<tool_call>\n" +
                            "{\"name\": <function-name>, \"arguments\": <args-json-object>}\n" +
                            "</tool_call>\n\n" +
                            "# Response format\n\n" +
                            "Response format for every step:\n" +
                            "1) Action: a short imperative describing what to do in the UI.\n" +
                            "2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\n" +
                            "Rules:\n" +
                            "- Output exactly in the order: Action, <tool_call>.\n" +
                            "- Be brief: one for Action.\n" +
                            "- Do not output anything else outside those two parts.\n" +
                            "- If finishing, use action=terminate in the tool call.";
                    MultiModalConversation conv = new MultiModalConversation();
                    MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                            .content(Arrays.asList(
                                    Collections.singletonMap("text",systemPrompt))).build();
                    MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                            .content(Arrays.asList(
                                    Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"),
                                    Collections.singletonMap("text", "帮我打开浏览器。"))).build();
                    MultiModalConversationParam param = MultiModalConversationParam.builder()
                            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                            .model("gui-plus-2026-02-26")
                            .messages(Arrays.asList(systemMsg,userMessage))
                            .vlHighResolutionImages(true)
                            .incrementalOutput(true)
                            .build();
                    Flowable<MultiModalConversationResult> result = conv.streamCall(param);
                    result.blockingForEach(item -> {
                        try {
                            var content = item.getOutput().getChoices().get(0).getMessage().getContent();
                            if (content != null &&  !content.isEmpty()) {
                                System.out.println(content.get(0).get("text"));
                            }
                        } catch (Exception e) {
                            System.out.println(e.getMessage());
                        }
                    });
                }

                public static void main(String[] args) {
                    try {
                        streamCall();
                    } catch (ApiException | NoApiKeyException | UploadFileException e) {
                        System.out.println(e.getMessage());
                    }
                    System.exit(0);
                }
            }
        - lang: curl
          label: 流式输出
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H "Content-Type: application/json" \
              -H "X-DashScope-SSE: enable" \
              -d '{
                "model": "gui-plus-2026-02-26",
                "input": {
                  "messages": [
                    {
                      "role": "system",
                      "content": [
                        {
                          "text": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
                        }
                      ]
                    },
                    {
                      "role": "user",
                      "content": [
                        {
                          "image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
                        },
                        {
                          "text": "帮我打开浏览器"
                        }
                      ]
                    }
                  ]
                },
                "parameters": {
                  "vl_high_resolution_images": true
                }
              }'
components:
  securitySchemes:
    ApiKeyAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    GuiPlusDashScopeRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          enum:
            - gui-plus
            - gui-plus-2026-02-26
          description: 模型名称。
        input:
          type: object
          required:
            - messages
          properties:
            messages:
              type: array
              description: 模型的对话历史，按时间顺序排列。
              items:
                $ref: "#/components/schemas/GuiPlusDashScopeMessage"
        parameters:
          $ref: "#/components/schemas/GuiPlusDashScopeParameters"
    GuiPlusDashScopeMessage:
      oneOf:
        - $ref: "#/components/schemas/GuiPlusDSSystemMessage"
        - $ref: "#/components/schemas/GuiPlusDSUserMessage"
        - $ref: "#/components/schemas/GuiPlusDSAssistantMessage"
    GuiPlusDSSystemMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - system
          description: 消息角色，固定为 `system`。
        content:
          oneOf:
            - type: string
            - type: array
              items:
                type: object
                properties:
                  text:
                    type: string
                    description: 系统消息文本。
          description: '系统消息内容。可以是字符串或包含 `{"text": "..."}` 的数组。'
    GuiPlusDSUserMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 消息角色，固定为 `user`。
        content:
          type: array
          description: 用户消息内容数组。每个元素可以包含 `image`（图片 URL）或 `text`（文本）。
          items:
            type: object
            properties:
              text:
                type: string
                description: 输入文本。
              image:
                type: string
                description: 图片 URL 或本地文件路径。
              min_pixels:
                type: integer
                description: 最小像素阈值。默认值与最小值均为 3136。
              max_pixels:
                type: integer
                description: 最大像素阈值。`vl_high_resolution_images=false` 时默认 1,003,520，最大 12,845,056；`vl_high_resolution_images=true` 时忽略此参数。
    GuiPlusDSAssistantMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - assistant
          description: 消息角色，固定为 `assistant`。
        content:
          type: string
          description: 模型在上一轮生成的回复文本。
    GuiPlusDashScopeParameters:
      type: object
      properties:
        vl_high_resolution_images:
          type: boolean
          default: false
          description: 是否将输入图像的像素上限提升至 16384 Token 对应的像素量。
        enable_thinking:
          type: boolean
          description: 是否开启思考模式。仅 `gui-plus-2026-02-26` 支持。SDK 参数名：`enableThinking`。
        max_tokens:
          type: integer
          description: 限制模型输出的最大 Token 数。SDK 参数名：`maxTokens`。
        seed:
          type: integer
          description: 随机数种子，范围 `[0, 2^31-1]`。
        temperature:
          type: number
          default: 0.01
          description: 采样温度。取值范围 `[0, 2)`。`temperature` 与 `top_p` 二者只需设置其一。
        top_p:
          type: number
          default: 0.01
          description: 核采样的概率阈值。取值范围 `(0, 1.0]`。SDK 参数名：`topP`。
        top_k:
          type: integer
          default: 1
          description: 采样候选集的大小。SDK 参数名：`topK`。
        repetition_penalty:
          type: number
          default: 1
          description: 连续序列中的重复度惩罚。1.0 表示不惩罚。SDK 参数名：`repetitionPenalty`。
        presence_penalty:
          type: number
          default: 1.5
          description: 控制生成文本的内容重复度。取值范围 `[-2.0, 2.0]`。
        incremental_output:
          type: boolean
          default: false
          description: 流式输出模式下是否开启增量输出，推荐设置为 `true`。`false`：每个数据块包含从开始到当前的所有生成内容（累积输出）。`true`：每个数据块仅包含本次新增内容（增量输出）。SDK 参数名：`incrementalOutput`。
        stop:
          oneOf:
            - type: string
            - type: array
              items:
                type: string
          description: 停止词。当模型生成的文本中出现指定字符串或 token_id 时，生成立即终止。
    GuiPlusDashScopeResponse:
      type: object
      properties:
        status_code:
          type: integer
          description: 本次请求的状态码。`200` 表示成功。Java SDK 不返回该参数，调用失败会抛出异常。
        request_id:
          type: string
          description: 本次调用的唯一标识符。Java SDK 返回参数为 `requestId`。
        code:
          type: string
          description: 错误码，调用成功时为空值。仅 Python SDK 返回该参数。
        message:
          type: string
          description: 错误信息。
        output:
          type: object
          properties:
            text:
              type: "null"
            finish_reason:
              type:
                - string
                - "null"
              description: 生成过程中为 `null`；自然停止为 `stop`；超出 `max_tokens` 为 `length`。
            choices:
              type: array
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    enum:
                      - stop
                      - length
                  message:
                    type: object
                    properties:
                      role:
                        type: string
                        enum:
                          - assistant
                      content:
                        type: array
                        items:
                          type: object
                          properties:
                            text:
                              type: string
                              description: 模型生成的界面操作指令。
            audio:
              type: "null"
        usage:
          type: object
          properties:
            input_tokens:
              type: integer
              description: 输入 Token 数。
            output_tokens:
              type: integer
              description: 输出 Token 数。
            total_tokens:
              type: integer
              description: 总 Token 数。
            image_tokens:
              type: integer
              description: 图像内容占用的 Token 数。
            characters:
              type: integer
            input_tokens_details:
              type: object
              properties:
                image_tokens:
                  type: integer
                text_tokens:
                  type: integer
            output_tokens_details:
              type: object
              properties:
                text_tokens:
                  type: integer
    DashScopeError:
      type: object
      properties:
        status_code:
          type: integer
        request_id:
          type: string
        code:
          type: string
        message:
          type: string
````
