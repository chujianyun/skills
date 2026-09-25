> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# GUI-Plus 界面交互

> GUI-Plus 模型基于屏幕截图和自然语言指令解析用户意图，转换为标准化的 GUI 操作

GUI-Plus 可基于屏幕截图和自然语言指令来解析用户意图，并转换为标准化的图像用户界面（GUI）操作（如点击、输入、滚动等），供外部系统决策或执行。相较于千问 VL 系列模型，提升了 GUI 操作的准确性。

<Note>
  GUI-Plus 模型的服务部署范围仅支持中国内地。
</Note>

## 支持的模型

| 模型名称                | 支持的模式      |
| ------------------- | ---------- |
| gui-plus            | 非思考模式      |
| gui-plus-2026-02-26 | 思考模式、非思考模式 |

关于模型的计费、上下文长度等详细信息，请参见[模型市场](https://www.qianwenai.com/models)。

<Note>
  `gui-plus-2026-02-26` 模型能力全面升级，支持思考与非思考模式，相较于 `gui-plus` 模型，`gui-plus-2026-02-26` 在处理跨平台、多 APP 任务的效果上得到大幅提升。**推荐优先使用该模型。**
</Note>

## 快速开始

本节将演示如何快速发起 GUI-Plus 模型调用，获取执行 GUI 任务的指令。关于如何将指令转换为实际的 GUI 操作并执行，请参阅后文的[如何使用](#如何使用)章节。**如需快速体验模型效果，可进行[在线试用](https://modelscope.cn/studios/MobileAgentTest/computer_use)。**

### 前提条件

- 需要已配置 API Key 并将 API Key 配置到环境变量。
- 如果通过 SDK 进行调用，需安装最新版 SDK。

### 推荐 System Prompt

`System Prompt` 可定义模型角色、能力和输出规范等，推荐 `gui-plus-2026-02-26` 模型使用以下系统提示词，否则会影响模型输出结果。

<Note>
  `gui-plus` 和 `gui-plus-2026-02-26` 的系统提示词不可共用，`gui-plus` 的系统提示词请参见[GUI-Plus 模型推荐提示词](#gui-plus-模型推荐提示词)。
</Note>

<CodeGroup>
  ```python 电脑端 System Prompt
  """# Tools

  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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
  ```

  ```python 手机端 System Prompt
  '''# Tools
  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.
  * This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.
  * Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.
  * The screen's resolution is 1000x1000.
  * Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:
  * `key`: Perform a key event on the mobile device.
    - This supports adb's `keyevent` syntax.
    - Examples: "volume_up", "volume_down", "power", "camera", "clear".
  * `click`: Click the point on the screen with coordinate (x, y).
  * `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.
  * `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).
  * `type`: Input the specified text into the activated input box.
  * `system_button`: Press the system button.
  * `open`: Open an app on the device.
  * `wait`: Wait specified seconds for the change to happen.
  * `answer`: Terminate the current task and output the answer.
  * `interact`: Resolve the blocking window by interacting with the user.
  * `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
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
  - If finishing, use action=terminate in the tool call.'''
  ```
</CodeGroup>

### 快速调用示例

<CodeGroup>
  ```python OpenAI Python
  import os
  from openai import OpenAI

  system_prompt = """# Tools

  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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
        {"type": "image_url", "image_url": {"url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"}},
        {"type": "text", "text": "帮我打开浏览器"}
      ]
    }
  ]

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="gui-plus-2026-02-26",
    messages=messages,
    extra_body={"vl_high_resolution_images": True}
  )

  print(completion.choices[0].message.content)
  ```

  ```javascript OpenAI Node.js
  import OpenAI from "openai";

  const systemPrompt = `# Tools

  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* \`key\`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* \`type\`: Type a string of text on the keyboard.\\n* \`mouse_move\`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`left_click\`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`left_click_drag\`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`right_click\`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`middle_click\`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`double_click\`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`triple_click\`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* \`scroll\`: Performs a scroll of the mouse scroll wheel.\\n* \`hscroll\`: Performs a horizontal scroll (mapped to regular scroll).\\n* \`wait\`: Wait specified seconds for the change to happen.\\n* \`terminate\`: Terminate the current task and report its completion status.\\n* \`answer\`: Answer a question.\\n* \`interact\`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by \`action=key\`.", "type": "array"}, "text": {"description": "Required only by \`action=type\`, \`action=answer\` and \`action=interact\`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by \`action=mouse_move\` and \`action=left_click_drag\`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by \`action=scroll\` and \`action=hscroll\`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by \`action=wait\`.", "type": "number"}, "status": {"description": "The status of the task. Required only by \`action=terminate\`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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
  - If finishing, use action=terminate in the tool call.`;

  const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  });

  const messages = [
    {
      role: "system",
      content: systemPrompt,
    },
    {
      role: "user",
      content: [
        {
          type: "image_url",
          image_url: {
            url: "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png",
          },
        },
        { type: "text", text: "帮我打开浏览器" },
      ],
    },
  ];

  const completion = await client.chat.completions.create({
    model: "gui-plus-2026-02-26",
    messages: messages,
    extra_body: { vl_high_resolution_images: true },
  });

  console.log(completion.choices[0].message.content);
  ```

  ```bash OpenAI curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "gui-plus-2026-02-26",
      "messages": [
        {
          "role": "system",
          "content": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
        },
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
              }
            },
            {
              "type": "text",
              "text": "帮我打开浏览器"
            }
          ]
        }
      ],
      "vl_high_resolution_images": true
    }'
  ```
</CodeGroup>

<Accordion title="OpenAI 兼容返回结果">
  ```json
  {
    "choices": [
      {
        "message": {
          "content": "<tool_call>\n{\"name\": \"computer_use\", \"arguments\": {\"action\": \"left_click\", \"coordinate\": [2530, 314]}}\n</tool_call>",
          "role": "assistant"
        },
        "finish_reason": "stop",
        "index": 0,
        "logprobs": null
      }
    ],
    "object": "chat.completion",
    "usage": {
      "prompt_tokens": 7750,
      "completion_tokens": 36,
      "total_tokens": 7786,
      "prompt_tokens_details": {
        "image_tokens": 6743,
        "text_tokens": 1007
      },
      "completion_tokens_details": {
        "text_tokens": 36
      }
    },
    "created": 1773133741,
    "system_fingerprint": null,
    "model": "gui-plus",
    "id": "chatcmpl-8b375016-abb8-9791-856c-74b2825c22d5"
  }
  ```
</Accordion>

<CodeGroup>
  ```python DashScope Python
  import os
  import dashscope

  system_prompt = """# Tools

  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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

  ```

  ```java DashScope Java
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
  ```

  ```bash DashScope curl
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
                "text": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name\": \"computer_use\", \"description\": \"Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\", \"enum\": [\"key\", \"type\", \"mouse_move\", \"left_click\", \"left_click_drag\", \"right_click\", \"middle_click\", \"double_click\", \"triple_click\", \"scroll\", \"hscroll\", \"wait\", \"terminate\", \"answer\", \"interact\"], \"type\": \"string\"}, \"keys\": {\"description\": \"Required only by `action=key`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=type`, `action=answer` and `action=interact`.\", \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\", \"type\": \"array\"}, \"pixels\": {\"description\": \"The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\", \"type\": \"number\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=wait`.\", \"type\": \"number\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
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
  ```
</CodeGroup>

<Accordion title="DashScope 返回结果">
  ```json
  {
    "output": {
      "choices": [
        {
          "finish_reason": "stop",
          "message": {
            "content": [
              {
                "text": "<tool_call>\n{\"name\": \"computer_use\", \"arguments\": {\"action\": \"left_click\", \"coordinate\": [2530, 314]}}\n</tool_call>"
              }
            ],
            "role": "assistant"
          }
        }
      ]
    },
    "usage": {
      "image_tokens": 6743,
      "input_tokens": 7750,
      "input_tokens_details": {
        "image_tokens": 6743,
        "text_tokens": 1007
      },
      "output_tokens": 36,
      "output_tokens_details": {
        "text_tokens": 36
      },
      "total_tokens": 7786
    },
    "request_id": "6821285d-e40f-4bca-903f-69f220e3c948"
  }
  ```
</Accordion>

## 如何使用

### 电脑 GUI 任务

<Note>
  本示例适用于 `Windows` 操作系统，若在 `Mac/Linux` 环境下，需修改 ComputerTools 类中的系统命令。
</Note>

#### 步骤1. 构造 System Prompt

```python
system_prompt = """# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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
```

以上系统提示词要求模型：

- 假设屏幕分辨率为 **1000x1000**（归一化坐标系）
- 输出格式严格：先输出动作（`Action`）的描述，然后输出 \`\`\`
- 支持的操作类型：点击、拖拽、输入、滚动、按键等

#### 步骤2. 构造多轮对话消息

在 GUI 自动化任务中，模型需要基于历史操作上下文做出决策。为了让模型理解当前任务进度并生成合理的下一步操作，模型采用以下策略构造多轮对话消息：

- 仅保留最近 N 轮（默认 4 轮）的完整对话（截图 + 模型输出），避免模型上下文过长导致的性能下降
- 对更早的历史操作，仅保留文本摘要（模型输出的动作（`Action`）部分），不包含截图，节省 token 消耗

```python
def get_messages(image, instruction, history_output, model_name, system_prompt):
  """
  构造多轮对话消息

  参数:
    image: 当前截图路径
    instruction: 用户指令
    history_output: 历史对话记录 [{"output": "...", "image": "..."}]
    model_name: 模型名称
  """
  history_n = 4  # 保留最近4轮历史
  current_step = len(history_output)

  # 构造历史操作摘要
  history_start_idx = max(0, current_step - history_n)
  previous_actions = []
  for i in range(history_start_idx):
    if i < len(history_output):
      history_output_str = history_output[i]['output']
      if 'Action:' in history_output_str and '<tool_call>':
        history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
      previous_actions.append(f"Step {i + 1}: {history_output_str}")

  previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

  instruction_prompt = f"""
   Please generate the next move according to the UI screenshot, instruction and previous actions.

   Instruction: {instruction}

   Previous actions:
   {previous_actions_str}"""

  # 构造 messages 数组
  messages = [
    {
      "role": "system",
      "content": [{"text": system_prompt}],
    }
  ]

  history_len = min(history_n, len(history_output))
  if history_len > 0:
    # 添加历史对话
    for history_id, history_item in enumerate(history_output[-history_n:], 0):
      if history_id == 0:
        messages.append({
          "role": "user",
          "content": [
            {"text": instruction_prompt},
            {"image": "file://" + history_item['image']}
          ]
        })
      else:
        messages.append({
          "role": "user",
          "content": [{"image": "file://" + history_item['image']}]
        })

      messages.append({
        "role": "assistant",
        "content": [{"text": history_item['output']}],
      })

    # 添加当前截图
    messages.append({
      "role": "user",
      "content": [{"image": "file://" + image}]
    })
  else:
    # 首轮对话
    messages.append({
      "role": "user",
      "content": [
        {"text": instruction_prompt},
        {"image": "file://" + image}
      ]
    })

  return messages
```

GUI模型的多轮对话的`message`数组示例如下（以7轮对话为例）

```json
model_input
  [{
    "role": "system",
    "content": [{
      "text": "# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within <tools></tools> XML tags:\n<tools>\n{\"type\": \"function\", \"function\": {\"name_for_human\": \"mobile_use\", \"name\": \"mobile_use\", \"description\": \"Use a touchscreen to interact with a mobile device, and take screenshots.\n* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.\n* The screen's resolution is 1000x1000.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\", \"parameters\": {\"properties\": {\"action\": {\"description\": \"The action to perform. The available actions are:\n* `key`: Perform a key event on the mobile device.\n    - This supports adb's `keyevent` syntax.\n    - Examples: \"volume_up\", \"volume_down\", \"power\", \"camera\", \"clear\".\n* `click`: Click the point on the screen with coordinate (x, y).\n* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.\n* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).\n* `type`: Input the specified text into the activated input box.\n* `system_button`: Press the system button.\n* `open`: Open an app on the device.\n* `wait`: Wait specified seconds for the change to happen.\n* `answer`: Terminate the current task and output the answer.\n* `interact`: Resolve the blocking window by interacting with the user.\n* `terminate`: Terminate the current task and report its completion status.\", \"enum\": [\"key\", \"click\", \"long_press\", \"swipe\", \"type\", \"system_button\", \"open\", \"wait\", \"answer\", \"interact\", \"terminate\"], \"type\": \"string\"}, \"coordinate\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.\", \"type\": \"array\"}, \"coordinate2\": {\"description\": \"(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.\", \"type\": \"array\"}, \"text\": {\"description\": \"Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.\", \"type\": \"string\"}, \"time\": {\"description\": \"The seconds to wait. Required only by `action=long_press` and `action=wait`.\", \"type\": \"number\"}, \"button\": {\"description\": \"Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`\", \"enum\": [\"Back\", \"Home\", \"Menu\", \"Enter\"], \"type\": \"string\"}, \"status\": {\"description\": \"The status of the task. Required only by `action=terminate`.\", \"type\": \"string\", \"enum\": [\"success\", \"failure\"]}}, \"required\": [\"action\"], \"type\": \"object\"}, \"args_format\": \"Format the arguments as a JSON object.\"}}\n</tools>\n\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single <tool_call>...</tool_call> block containing only the JSON: {\"name\": <function-name>, \"arguments\": <args-json-object>}.\n\nRules:\n- Output exactly in the order: Action, <tool_call>.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call."
    }]
  }, {
    "role": "user",
    "content": [{
      "text": "\nPlease generate the next move according to the UI screenshot, instruction and previous actions.\n\nInstruction: 帮我在携程搜一下今天济南喜来登酒店的价格\n\nPrevious actions:\nStep 1: 点击携程旅行应用图标以启动携程旅行预订应用程序。\nStep 2: 等待促销启动画面自动过渡到携程主应用界面。"
    }, {
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_a84122ac_853a630315784b64988492c9c07b5534.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 点击应用更新通知弹窗右上角的关闭按钮（X图标）以将其关闭。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"click\", \"coordinate\": [789, 280]}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_6010a769_089b9b35b1904913bd5df492563b02b9.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 点击搜索栏中的“济南的酒店”文本区域，以激活搜索输入框并准备修改搜索词。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"click\", \"coordinate\": [112, 134]}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_47446db4_fd4a5022002c4db99f110d5c7261fea2.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 点击显示“厦门”的位置字段，将搜索位置从厦门更改为济南。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"click\", \"coordinate\": [156, 347]}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_3832132c_8c55861c1716467e802a3554402f3580.png"
    }]
  }, {
    "role": "assistant",
    "content": [{
      "text": "Action: 在搜索输入框中键入“济南”，以指定酒店搜索的城市位置。\n<tool_call>\n{\"name\": \"mobile_use\", \"arguments\": {\"action\": \"type\", \"text\": \"济南\"}}\n</tool_call>"
    }]
  }, {
    "role": "user",
    "content": [{
      "image": "http://nlp-mobile-agent.oss-cn-zhangjiakou.aliyuncs.com/computer-use%2Fscreenshot%2Fscreenshot_ff247bac_39c3e20be32c4baf8677a2b6b61bc021.png"
    }]
  }]
```

#### 步骤3. 解析模型输出

由于模型在处理图像时会进行内部缩放，其返回的坐标是基于缩放后图像的归一化坐标。为在原图上准确执行 GUI 操作，需要进行坐标映射。

1. **提取 Tool Call 字段**

首先从模型返回的字符串中提取 Tool Call：

```python
import re
import json

def extract_tool_calls(text):
  """
  从模型输出中提取所有 <tool_call> 块

  参数:
    text: 模型返回的文本

  返回:
    actions: 解析后的操作列表
  """
  pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
  blocks = pattern.findall(text)

  actions = []
  for blk in blocks:
    blk = blk.strip()
    try:
      actions.append(json.loads(blk))
    except json.JSONDecodeError as e:
      print(f'解析失败: {e} | 片段: {blk[:80]}...')

  return actions
```

<a id="2-坐标映射函数" />

2. **坐标映射函数**

模型处理图像时会进行内部缩放，以下函数用于计算缩放后的尺寸：

```python
import math
from PIL import Image

def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
  """
  计算模型内部缩放后的图像尺寸

  参数:
    height: 原始图像高度
    width: 原始图像宽度
    factor: 分辨率因子（固定为 16）
    min_pixels: 最小像素值
    max_pixels: 最大像素值
    max_long_side: 最长边限制

  返回:
    (h_bar, w_bar): 缩放后的高度和宽度
  """
  def round_by_factor(number, factor):
    return round(number / factor) * factor

  def ceil_by_factor(number, factor):
    return math.ceil(number / factor) * factor

  def floor_by_factor(number, factor):
    return math.floor(number / factor) * factor

  if height < 2 or width < 2:
    raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
  elif max(height, width) / min(height, width) > 200:
    raise ValueError(f"absolute aspect ratio must be smaller than 200, got {height} / {width}")

  # 限制最长边
  if max(height, width) > max_long_side:
    beta = max(height, width) / max_long_side
    height, width = int(height / beta), int(width / beta)

  # 计算缩放后的尺寸
  h_bar = round_by_factor(height, factor)
  w_bar = round_by_factor(width, factor)

  if h_bar * w_bar > max_pixels:
    beta = math.sqrt((height * width) / max_pixels)
    h_bar = floor_by_factor(height / beta, factor)
    w_bar = floor_by_factor(width / beta, factor)
  elif h_bar * w_bar < min_pixels:
    beta = math.sqrt(min_pixels / (height * width))
    h_bar = ceil_by_factor(height * beta, factor)
    w_bar = ceil_by_factor(width * beta, factor)

  return h_bar, w_bar
```

#### 步骤4. 执行GUI操作

解析动作指令后，接下来演示如何使用`pyautogui`库模拟用户的鼠标点击、键盘输入、滚动等物理 GUI 操作。

```python
import pyautogui
import pyperclip
import time
from PIL import Image
import os

class ComputerTools:
  """电脑端 GUI 操作工具类"""

  def __init__(self):
    self.image_info = None

  def load_image_info(self, path):
    """加载图像尺寸信息"""
    width, height = Image.open(path).size
    self.image_info = (width, height)

  def get_screenshot(self, image_path, retry_times=3):
    """获取桌面截图"""
    if os.path.exists(image_path):
      os.remove(image_path)

    for i in range(retry_times):
      screenshot = pyautogui.screenshot()
      screenshot.save(image_path)
      if os.path.exists(image_path):
        self.load_image_info(image_path)
        return True
      else:
        time.sleep(0.1)
    return False

  def reset(self):
    """显示桌面"""
    pyautogui.hotkey('win', 'd')

  def press_key(self, keys):
    """按键操作"""
    if isinstance(keys, list):
      cleaned_keys = []
      for key in keys:
        if isinstance(key, str):
          # 处理键名格式
          if key.startswith("keys=["):
            key = key[6:]
          if key.endswith("]"):
            key = key[:-1]
          if key.startswith("['") or key.startswith('["'):
            key = key[2:] if len(key) > 2 else key
          if key.endswith("']") or key.endswith('"]'):
            key = key[:-2] if len(key) > 2 else key
          key = key.strip()

          # 转换键名
          key_map = {
            "arrowleft": "left",
            "arrowright": "right",
            "arrowup": "up",
            "arrowdown": "down"
          }
          key = key_map.get(key, key)
          cleaned_keys.append(key)
        else:
          cleaned_keys.append(key)
      keys = cleaned_keys
    else:
      keys = [keys]

    if len(keys) > 1:
      pyautogui.hotkey(*keys)
    else:
      pyautogui.press(keys[0])

  def type(self, text):
    """输入文本（使用剪贴板方式支持中文）"""
    pyperclip.copy(text)
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('v')
    pyautogui.keyUp('v')
    pyautogui.keyUp('ctrl')

  def mouse_move(self, x, y):
    """移动鼠标到指定坐标"""
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.moveTo(x, y)

  def left_click(self, x, y):
    """左键点击"""
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.click()

  def left_click_drag(self, x, y):
    """从当前位置拖拽到指定坐标"""
    pyautogui.dragTo(x, y, duration=0.5)
    pyautogui.moveTo(x, y)

  def right_click(self, x, y):
    """右键点击"""
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.rightClick()

  def middle_click(self, x, y):
    """中键点击"""
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.middleClick()

  def double_click(self, x, y):
    """双击"""
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.doubleClick()

  def triple_click(self, x, y):
    """三击"""
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    pyautogui.tripleClick()

  def scroll(self, pixels):
    """滚轮滚动"""
    pyautogui.scroll(pixels)
```

#### 步骤5. 完整自动化流程

将以上所有步骤整合到一个完整的自动化流程中，循环执行截图` 模型推理` 执行GUI操作，直到任务完成。

```python
import os
import dashscope
import time

def run_gui_automation(instruction, max_step=30):
  """
  运行完整的 GUI 自动化流程

  参数:
    instruction: 用户指令
    max_step: 最大执行步骤数
  """
  # 配置 API
  dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
  model_name = 'gui-plus-2026-02-26'

  # 初始化工具
  computer_tools = ComputerTools()
  computer_tools.reset()  # 显示桌面

  # 创建输出目录
  output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "gui_automation")
  os.makedirs(output_dir, exist_ok=True)

  # 对话历史
  history = []
  stop_flag = False

  print(f"[任务] {instruction}")
  print("=" * 60)

  for step_id in range(max_step):
    if stop_flag:
      break

    print(f"\n[步骤 {step_id + 1}]")

    # 1. 截图
    screen_shot = os.path.join(output_dir, f'screenshot_{step_id}.png')
    computer_tools.get_screenshot(screen_shot)

    # 2. 构造消息
    messages = get_messages(screen_shot, instruction, history, model_name)

    # 3. 调用模型
    response = dashscope.MultiModalConversation.call(
      model=model_name,
      messages=messages,
      vl_high_resolution_images=True,
      stream=False
    )

    output_text = response.output.choices[0].message.content[0]['text']
    print(f"[模型输出]\n{output_text}\n")

    # 4. 解析操作
    action_list = extract_tool_calls(output_text)
    if not action_list:
      print("未提取到有效操作")
      break

    # 5. 执行操作
    for action_id, action in enumerate(action_list):
      action_parameter = action['arguments']
      action_type = action_parameter['action']

      # 获取图像尺寸用于坐标映射
      dummy_image = Image.open(screen_shot)
      resized_height, resized_width = smart_resize(
        dummy_image.height,
        dummy_image.width,
        factor=16,
        min_pixels=3136,
        max_pixels=1003520 * 200
      )

      # 映射坐标（从归一化坐标 1000x1000 映射到实际尺寸）
      for key in ['coordinate', 'coordinate1', 'coordinate2']:
        if key in action_parameter:
          action_parameter[key][0] = int(action_parameter[key][0] / 1000 * resized_width)
          action_parameter[key][1] = int(action_parameter[key][1] / 1000 * resized_height)

      # 执行对应操作
      if action_type in ['click', 'left_click']:
        computer_tools.left_click(
          action_parameter['coordinate'][0],
          action_parameter['coordinate'][1]
        )
        print(f"[OK] 左键点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")

      elif action_type == 'mouse_move':
        computer_tools.mouse_move(
          action_parameter['coordinate'][0],
          action_parameter['coordinate'][1]
        )
        print(f"[OK] 移动鼠标到 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")

      elif action_type == 'middle_click':
        computer_tools.middle_click(
          action_parameter['coordinate'][0],
          action_parameter['coordinate'][1]
        )
        print(f"[OK] 中键点击")

      elif action_type in ['right click', 'right_click']:
        computer_tools.right_click(
          action_parameter['coordinate'][0],
          action_parameter['coordinate'][1]
        )
        print(f"[OK] 右键点击")

      elif action_type in ['key', 'hotkey']:
        computer_tools.press_key(action_parameter['keys'])
        print(f"[OK] 按键 {action_parameter['keys']}")

      elif action_type == 'type':
        text = action_parameter['text']
        computer_tools.type(text)
        print(f"[OK] 输入文本: {text}")

      elif action_type == 'drag':
        computer_tools.left_click_drag(
          action_parameter['coordinate'][0],
          action_parameter['coordinate'][1]
        )
        print(f"[OK] 拖拽到 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")

      elif action_type == 'scroll':
        if 'coordinate' in action_parameter:
          computer_tools.mouse_move(
            action_parameter['coordinate'][0],
            action_parameter['coordinate'][1]
          )
        computer_tools.scroll(action_parameter.get("pixels", 1))
        print(f"[OK] 滚动 {action_parameter.get('pixels', 1)} 像素")

      elif action_type in ['computer_double_click', 'double_click']:
        computer_tools.double_click(
          action_parameter['coordinate'][0],
          action_parameter['coordinate'][1]
        )
        print(f"[OK] 双击")

      elif action_type == 'wait':
        time.sleep(action_parameter.get('time', 2))
        print(f"[OK] 等待 {action_parameter.get('time', 2)} 秒")

      elif action_type == 'answer':
        print(f"[OK] 任务完成: {action_parameter.get('text', '')}")
        stop_flag = True
        break

      elif action_type in ['stop', 'terminate', 'done']:
        print(f"[OK] 任务终止: {action_parameter.get('status', 'success')}")
        stop_flag = True
        break

      else:
        print(f"未知操作类型: {action_type}")

    # 6. 保存历史
    history.append({
      'output': output_text,
      'image': screen_shot
    })

    time.sleep(2)  # 操作间隔

  print("\n" + "=" * 60)
  print(f"[完成] 共执行 {len(history)} 步")

# 使用示例
if __name__ == '__main__':
  run_gui_automation(
    instruction='帮我打开chrome,在百度中搜索阿里巴巴',
    max_step=30
  )
```

<Accordion title="电脑端完整示例代码">
  ```python
  import os
  import re
  import json
  import math
  import time
  import pyautogui
  import pyperclip
  import dashscope
  from PIL import Image

  # ===================== 步骤1：System Prompt =====================

  system_prompt = """# Tools

  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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

  # ===================== 步骤2：构造多轮对话消息 =====================

  def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)

    history_start_idx = max(0, current_step - history_n)
    previous_actions = []
    for i in range(history_start_idx):
      if i < len(history_output):
        history_output_str = history_output[i]['output']
        if 'Action:' in history_output_str and '<tool_call>':
          history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
        previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = "\\n".join(previous_actions) if previous_actions else "None"

    instruction_prompt = f"""
     Please generate the next move according to the UI screenshot, instruction and previous actions.

     Instruction: {instruction}

     Previous actions:
     {previous_actions_str}"""

    messages = [{"role": "system", "content": [{"text": system_prompt}]}]

    history_len = min(history_n, len(history_output))
    if history_len > 0:
      for history_id, history_item in enumerate(history_output[-history_n:], 0):
        if history_id == 0:
          messages.append({
            "role": "user",
            "content": [
              {"text": instruction_prompt},
              {"image": "file://" + history_item['image']}
            ]
          })
        else:
          messages.append({
            "role": "user",
            "content": [{"image": "file://" + history_item['image']}]
          })
        messages.append({
          "role": "assistant",
          "content": [{"text": history_item['output']}],
        })
      messages.append({
        "role": "user",
        "content": [{"image": "file://" + image}]
      })
    else:
      messages.append({
        "role": "user",
        "content": [
          {"text": instruction_prompt},
          {"image": "file://" + image}
        ]
      })
    return messages

  # ===================== 步骤3：解析模型输出与坐标映射 =====================

  def extract_tool_calls(text):
    pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL | re.IGNORECASE)
    blocks = pattern.findall(text)
    actions = []
    for blk in blocks:
      blk = blk.strip()
      try:
        actions.append(json.loads(blk))
      except json.JSONDecodeError as e:
        print(f'解析失败: {e} | 片段: {blk[:80]}...')
    return actions

  def smart_resize(height, width, factor=32, min_pixels=32*32*4, max_pixels=32*32*1280, max_long_side=8192):
    def round_by_factor(number, factor):
      return round(number / factor) * factor
    def ceil_by_factor(number, factor):
      return math.ceil(number / factor) * factor
    def floor_by_factor(number, factor):
      return math.floor(number / factor) * factor

    if height < 2 or width < 2:
      raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
      raise ValueError(f"absolute aspect ratio must be smaller than 200, got {height} / {width}")

    if max(height, width) > max_long_side:
      beta = max(height, width) / max_long_side
      height, width = int(height / beta), int(width / beta)

    h_bar = round_by_factor(height, factor)
    w_bar = round_by_factor(width, factor)

    if h_bar * w_bar > max_pixels:
      beta = math.sqrt((height * width) / max_pixels)
      h_bar = floor_by_factor(height / beta, factor)
      w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
      beta = math.sqrt(min_pixels / (height * width))
      h_bar = ceil_by_factor(height * beta, factor)
      w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

  # ===================== 步骤4：GUI 操作工具类 =====================

  class ComputerTools:
    def __init__(self):
      self.image_info = None

    def load_image_info(self, path):
      width, height = Image.open(path).size
      self.image_info = (width, height)

    def get_screenshot(self, image_path, retry_times=3):
      if os.path.exists(image_path):
        os.remove(image_path)
      for i in range(retry_times):
        screenshot = pyautogui.screenshot()
        screenshot.save(image_path)
        if os.path.exists(image_path):
          self.load_image_info(image_path)
          return True
        else:
          time.sleep(0.1)
      return False

    def reset(self):
      pyautogui.hotkey('win', 'd')

    def press_key(self, keys):
      if isinstance(keys, list):
        cleaned_keys = []
        for key in keys:
          if isinstance(key, str):
            if key.startswith("keys=["): key = key[6:]
            if key.endswith("]"): key = key[:-1]
            if key.startswith("['") or key.startswith('["'): key = key[2:] if len(key) > 2 else key
            if key.endswith("']") or key.endswith('"]'): key = key[:-2] if len(key) > 2 else key
            key = key.strip()
            key_map = {"arrowleft": "left", "arrowright": "right", "arrowup": "up", "arrowdown": "down"}
            key = key_map.get(key, key)
            cleaned_keys.append(key)
          else:
            cleaned_keys.append(key)
        keys = cleaned_keys
      else:
        keys = [keys]
      if len(keys) > 1:
        pyautogui.hotkey(*keys)
      else:
        pyautogui.press(keys[0])

    def type(self, text):
      pyperclip.copy(text)
      pyautogui.keyDown('ctrl')
      pyautogui.keyDown('v')
      pyautogui.keyUp('v')
      pyautogui.keyUp('ctrl')

    def mouse_move(self, x, y):
      pyautogui.moveTo(x, y)
      time.sleep(0.1)
      pyautogui.moveTo(x, y)

    def left_click(self, x, y):
      pyautogui.moveTo(x, y)
      time.sleep(0.1)
      pyautogui.click()

    def left_click_drag(self, x, y):
      pyautogui.dragTo(x, y, duration=0.5)
      pyautogui.moveTo(x, y)

    def right_click(self, x, y):
      pyautogui.moveTo(x, y)
      time.sleep(0.1)
      pyautogui.rightClick()

    def middle_click(self, x, y):
      pyautogui.moveTo(x, y)
      time.sleep(0.1)
      pyautogui.middleClick()

    def double_click(self, x, y):
      pyautogui.moveTo(x, y)
      time.sleep(0.1)
      pyautogui.doubleClick()

    def triple_click(self, x, y):
      pyautogui.moveTo(x, y)
      time.sleep(0.1)
      pyautogui.tripleClick()

    def scroll(self, pixels):
      pyautogui.scroll(pixels)

  # ===================== 步骤5：完整自动化流程 =====================

  def run_gui_automation(instruction, max_step=30):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    model_name = 'gui-plus-2026-02-26'

    computer_tools = ComputerTools()
    computer_tools.reset()

    output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "gui_automation")
    os.makedirs(output_dir, exist_ok=True)

    history = []
    stop_flag = False

    print(f"[任务] {instruction}")
    print("=" * 60)

    for step_id in range(max_step):
      if stop_flag:
        break

      print(f"\n[步骤 {step_id + 1}]")

      screen_shot = os.path.join(output_dir, f'screenshot_{step_id}.png')
      computer_tools.get_screenshot(screen_shot)

      messages = get_messages(screen_shot, instruction, history, system_prompt)

      response = dashscope.MultiModalConversation.call(
        model=model_name,
        messages=messages,
        vl_high_resolution_images=True,
        stream=False
      )

      output_text = response.output.choices[0].message.content[0]['text']
      print(f"[模型输出]\n{output_text}\n")

      action_list = extract_tool_calls(output_text)
      if not action_list:
        print("未提取到有效操作")
        break

      for action_id, action in enumerate(action_list):
        action_parameter = action['arguments']
        action_type = action_parameter['action']

        dummy_image = Image.open(screen_shot)
        resized_height, resized_width = smart_resize(
          dummy_image.height, dummy_image.width,
          factor=16, min_pixels=3136, max_pixels=1003520 * 200
        )

        for key in ['coordinate', 'coordinate1', 'coordinate2']:
          if key in action_parameter:
            action_parameter[key][0] = int(action_parameter[key][0] / 1000 * resized_width)
            action_parameter[key][1] = int(action_parameter[key][1] / 1000 * resized_height)

        if action_type in ['click', 'left_click']:
          computer_tools.left_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          print(f"[OK] 左键点击 ({action_parameter['coordinate'][0]}, {action_parameter['coordinate'][1]})")
        elif action_type == 'mouse_move':
          computer_tools.mouse_move(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          print(f"[OK] 移动鼠标")
        elif action_type == 'middle_click':
          computer_tools.middle_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          print(f"[OK] 中键点击")
        elif action_type in ['right click', 'right_click']:
          computer_tools.right_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          print(f"[OK] 右键点击")
        elif action_type in ['key', 'hotkey']:
          computer_tools.press_key(action_parameter['keys'])
          print(f"[OK] 按键 {action_parameter['keys']}")
        elif action_type == 'type':
          computer_tools.type(action_parameter['text'])
          print(f"[OK] 输入文本: {action_parameter['text']}")
        elif action_type == 'drag':
          computer_tools.left_click_drag(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          print(f"[OK] 拖拽")
        elif action_type == 'scroll':
          if 'coordinate' in action_parameter:
            computer_tools.mouse_move(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          computer_tools.scroll(action_parameter.get("pixels", 1))
          print(f"[OK] 滚动 {action_parameter.get('pixels', 1)} 像素")
        elif action_type in ['computer_double_click', 'double_click']:
          computer_tools.double_click(action_parameter['coordinate'][0], action_parameter['coordinate'][1])
          print(f"[OK] 双击")
        elif action_type == 'wait':
          time.sleep(action_parameter.get('time', 2))
          print(f"[OK] 等待 {action_parameter.get('time', 2)} 秒")
        elif action_type == 'answer':
          print(f"[OK] 任务完成: {action_parameter.get('text', '')}")
          stop_flag = True
          break
        elif action_type in ['stop', 'terminate', 'done']:
          print(f"[OK] 任务终止: {action_parameter.get('status', 'success')}")
          stop_flag = True
          break
        else:
          print(f"未知操作类型: {action_type}")

      history.append({'output': output_text, 'image': screen_shot})
      time.sleep(2)

    print("\n" + "=" * 60)
    print(f"[完成] 共执行 {len(history)} 步")

  if __name__ == '__main__':
    run_gui_automation(
      instruction='帮我打开chrome,在百度中搜索阿里巴巴',
      max_step=30
    )
  ```
</Accordion>

### 手机端 GUI 任务

手机端通过 ADB（Android Debug Bridge）工具实现自动化操作。

**环境准备**：

1. 下载适合系统的 [Android Debug Bridge](https://developer.android.com/tools/releases/platform-tools?hl=en)，保存到指定路径
2. 在手机上开启"USB 调试"或"ADB调试"（通常需要先开启开发者选项）
3. 通过数据线连接手机和电脑，选择"传输文件"模式
4. 下载 [ADB 键盘](https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk) 的安装包，并将安装包传输到手机上打开，选择无视风险安装
5. 在系统设置中将默认输入法切换为 `ADB Keyboard`
6. 在电脑终端上测试连接：`/path/to/adb devices`（设备列表不为空说明连接成功）
7. 电脑系统为 `macOS/Linux` 时，需要开启权限：`sudo chmod +x /path/to/adb`
8. 进入手机的某个 App，然后执行命令：`/path/to/adb shell am start -a android.intent.action.MAIN -c android.intent.category.HOME`，如果手机设备退回到桌面，则说明一切就绪

手机端GUI示例与电脑端大致相同，完整示例代码如下：

<Accordion title="手机端完整示例代码">
  1. **构造手机端`System Prompt`**

  ```python
  import json, os, subprocess
  import dashscope, time, math
  from PIL import Image, ImageDraw
  import shutil, requests
  from datetime import datetime

  mobile_system_prompt = '''# Tools
          You may call one or more functions to assist with the user query.

          You are provided with function signatures within <tools></tools> XML tags:
          <tools>
          {"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.
          * This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.
          * Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.
          * The screen's resolution is 1000x1000.
          * Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:
          * `key`: Perform a key event on the mobile device.
              - This supports adb's `keyevent` syntax.
              - Examples: "volume_up", "volume_down", "power", "camera", "clear".
          * `click`: Click the point on the screen with coordinate (x, y).
          * `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.
          * `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).
          * `type`: Input the specified text into the activated input box.
          * `system_button`: Press the system button.
          * `open`: Open an app on the device.
          * `wait`: Wait specified seconds for the change to happen.
          * `answer`: Terminate the current task and output the answer.
          * `interact`: Resolve the blocking window by interacting with the user.
          * `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
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
          - If finishing, use action=terminate in the tool call.'''
  ```

  2. **构造多轮对话消息**

  ```python
  from datetime import datetime

  def get_messages(image, instruction, history_output, system_prompt):
    history_n = 4
    current_step = len(history_output)

    history_start_idx = max(0, current_step - history_n)

    previous_actions = []
    for i in range(history_start_idx):
      if i < len(history_output):
        history_output_str = history_output[i]['output']
        if 'Action:' in history_output_str and '<tool_call>':
          history_output_str = history_output_str.split('Action:')[1].split('<tool_call>')[0].strip()
        previous_actions.append(f"Step {i + 1}: {history_output_str}")

    previous_actions_str = (
      "\n".join(previous_actions) if previous_actions else "None"
    )
    # 添加背景信息
    today = datetime.today()
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[today.weekday()]
    formatted_date = today.strftime("%Y年%m月%d日") + " " + weekday
    ground_info = f'''今天的日期是:{formatted_date}。'''

    instruction_prompt = f"""
      Please generate the next move according to the UI screenshot, instruction and previous actions.

      Instruction: {ground_info}{instruction}

      Previous actions:
      {previous_actions_str}"""

    ## 模型调用
    messages = [
      {
        "role": "system",
        "content": [
          {"text": system_prompt}
        ],
      }
    ]
    history_len = min(history_n, len(history_output))
    if history_len > 0:
      for history_id, history_item in enumerate(history_output[-history_n:], 0):
        if history_id == 0:
          messages.append({
            "role": "user",
            "content": [
              {"text": instruction_prompt},
              {"image": "file://" +history_item['image']}
            ]
          })
        else:
          messages.append({
            "role": "user",
            "content": [
              {"image": "file://" +history_item['image']}
            ]
          })
        messages.append({
          "role": "assistant",
          "content": [
            {"text": history_item['output']},
          ]
        })
      messages.append({
        "role": "user",
        "content": [
          {"image": "file://" +image},
        ]
      })
    else:
      messages.append(
        {
          "role": "user",
          "content": [
            {
              "text": instruction_prompt
            },
            {
              "image": "file://" +image,
            },
          ],
        }
      )

    return messages
  ```

  3. **计算缩放后的图像大小**

  手机端与电脑端共用一套 `smart_resize` 函数。详情请参见前文[坐标映射函数](#2-坐标映射函数)。

  4. **执行GUI操作**

  使用 ADB 命令执行实际的手机操作。

  ```python
  import subprocess
  import os
  import time
  from PIL import Image

  class AdbTools:
    def __init__(self, adb_path, device=None):
      self.adb_path = adb_path
      self.device = device
      self.__device_str__ = f" -s {device} " if device is not None else ' '
      self.image_info = None

    def adb_shell(self, command):
      command = self.adb_path + self.__device_str__ + command
      subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 载入手机size
    def load_image_info(self, path):
      width, height = Image.open(path).size
      self.image_info = (width, height)

    ## 获取截图
    def get_screenshot(self, image_path, retry_times=3):
      command = self.adb_path + (f" -s {self.device}" if self.device is not None else '') + f" exec-out screencap -p > {image_path}"

      for i in range(retry_times):
        subprocess.run(command, capture_output=True, text=True, shell=True)
        if os.path.exists(image_path):
          self.load_image_info(image_path)
          return True
        else:
          time.sleep(0.1)
      else:
        return False

    ## 点击(x,y)
    ## coordinate_size: 输入图片的尺寸，默认为None，则使用当前手机的尺寸, 传入为{'x': int, 'y': int}
    def click(self, x, y, coordinate_size=None):
      command = self.adb_path + self.__device_str__ + f" shell input tap {x} {y}"
      subprocess.run(command, capture_output=True, text=True, shell=True)

    def long_press(self, x, y, time=800):
      command = self.adb_path + self.__device_str__ + f" shell input swipe {x} {y} {x} {y} {time}"
      subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 滑动从(x1,y1)->(x2,y2)
    ## coordinate_size: 输入图片的尺寸，默认为None，则使用当前手机的尺寸, 传入为{'x': int, 'y': int}
    def slide(self, x1, y1, x2, y2, coordinate_size=None, slide_time=800):
      command = self.adb_path + self.__device_str__ + f" shell input swipe {x1} {y1} {x2} {y2} {slide_time}"
      subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 返回
    def back(self):
      command = self.adb_path + self.__device_str__ + f"  shell input keyevent 4"
      subprocess.run(command, capture_output=True, text=True, shell=True)

    # 点击Home键
    def home(self):
      command = self.adb_path + self.__device_str__ + f" shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
      subprocess.run(command, capture_output=True, text=True, shell=True)

    ## 打字(中英均可，不确定其他语言是否可以)，注意需要先在手机安装 adb 键盘
    def type(self, text):
      escaped_text = text.replace('"', '\\"').replace("'", "\\'")
      command_list = [
        f"shell ime enable com.android.adbkeyboard/.AdbIME ",
        f"shell ime set com.android.adbkeyboard/.AdbIME ",
        0.1,
        f'shell am broadcast -a ADB_INPUT_TEXT --es msg "{escaped_text}" ',
        0.1,
        f"shell ime disable com.android.adbkeyboard/.AdbIME"
      ]

      for command in command_list:
        if isinstance(command, float):
          time.sleep(command)
        elif isinstance(command, str):
          subprocess.run(self.adb_path + self.__device_str__ + command.strip(), capture_output=True, text=True, shell=True)

    def get_package_name(self, all_packages=False):
      try:
        if all_packages:
          command = self.adb_path + self.__device_str__ + " shell pm list packages"
        else:
          command = self.adb_path + self.__device_str__ + " shell pm list packages -3"
        res = subprocess.run(command, capture_output=True, text=True, shell=True)
        pkgs = []
        for line in res.stdout.splitlines():
          s = line.strip()
          if not s:
            continue
          # 去掉前缀 "package:"
          if s.startswith("package:"):
            s = s[len("package:"):]
          # 如果包含 "="，右侧才是包名
          if "=" in s:
            _, s = s.split("=", 1)
          if s:
            pkgs.append(s)
        return sorted(set(pkgs))
      except Exception as e:
        print(e)
        return []

    def open_app(self, package_name):
      command = self.adb_path + self.__device_str__ + f" shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
      subprocess.run(command, capture_output=True, text=True, shell=True)
  ```

  5. **应用包名映射**

  包名是 Android 应用的唯一标识符（格式如：`com.公司名.产品名`，示例：`com.tencent.mm`）

  为了支持通过应用名称打开应用（`action=open`），需要维护应用名称到包名的映射。

  ```python
  # 常见应用包名映射（示例，可根据需要扩展）
  package_str_list = '''com.tencent.mm    微信    wechat
  com.tencent.mobileqq    qq    腾讯qq
  com.sina.weibo    微博
  com.taobao.taobao    淘宝
  com.jingdong.app.mall    京东    京东秒送
  com.xunmeng.pinduoduo    拼多多
  com.xingin.xhs    小红书
  com.douban.frodo    豆瓣
  com.zhihu.android    知乎
  com.autonavi.minimap    高德地图    高德
  com.baidu.BaiduMap    百度地图
  com.sankuai.meituan.takeoutnew    美团外卖
  com.sankuai.meituan    美团    美团外卖
  com.dianping.v1    大众点评    点评
  me.ele    饿了么    淘宝闪购
  com.yek.android.kfc.activitys    肯德基
  ctrip.android.view    携程    携程旅行
  com.MobileTicket    铁路12306    12306
  com.Qunar    去哪儿旅行    去哪儿网    去哪儿
  com.sdu.didi.psnger    滴滴出行    滴滴
  tv.danmaku.bili    bilibili    b站    哔哩哔哩    哔站    bili
  com.ss.android.ugc.aweme    抖音
  com.smile.gifmaker    快手
  com.tencent.qqlive    腾讯视频
  com.qiyi.video    爱奇艺
  com.youku.phone    优酷    优酷视频
  com.hunantv.imgo.activity    芒果tv    芒果
  com.phoenix.read    红果短剧    红果
  com.netease.cloudmusic    网易云音乐    网易云
  com.tencent.qqmusic    qq音乐
  com.luna.music    汽水音乐
  com.ximalaya.ting.android    喜马拉雅
  com.dragon.read    番茄免费小说    番茄小说
  com.kmxs.reader    七猫免费小说
  com.ss.android.lark    飞书
  com.tencent.androidqqmail    qq邮箱
  com.larus.nova    豆包    豆包
  com.gotokeep.keep    keep
  com.lingan.seeyou    美柚
  com.tencent.news    腾讯新闻
  com.ss.android.article.news    今日头条
  com.lianjia.beike    贝壳找房
  com.anjuke.android.app    安居客
  com.hexin.plat.android    同花顺
  com.miHoYo.hkrpg    星穹铁道    崩坏
  com.papegames.lysk.cn    恋与深空
  com.android.settings    settings    androidsystemsettings
  com.android.soundrecorder    audiorecorder
  com.rammigsoftware.bluecoins    bluecoins
  com.flauschcode.broccoli    broccoli
  com.booking    booking
  com.android.chrome    谷歌浏览器    googlechrome    chrome
  com.android.deskclock    时钟    闹钟    clock
  com.android.contacts    contacts
  com.duolingo    duolingo    多邻国
  com.expedia.bookings    expedia
  com.android.fileexplorer    files    filemanager
  com.google.android.gm    gmail    googlemail
  com.google.android.apps.nbu.files    googlefiles    filesbygoogle
  com.google.android.calendar    googlecalendar
  com.google.android.apps.dynamite    googlechat
  com.google.android.deskclock    googleclock
  com.google.android.contacts    googlecontacts
  com.google.android.apps.docs.editors.docs    googledocs
  com.google.android.apps.docs    googledrive
  com.google.android.apps.fitness    googlefit
  com.google.android.keep    googlekeep
  com.google.android.apps.maps    googlemaps
  com.google.android.apps.books    googleplaybooks
  com.android.vending    googleplaystore
  com.google.android.apps.docs.editors.slides    googleslides
  com.google.android.apps.tasks    googletasks
  net.cozic.joplin    joplin
  com.mcdonalds.app    麦当劳    mcdonald
  net.osmand    osmand
  com.Project100Pi.themusicplayer    pimusicplayer
  com.quora.android    quora
  com.reddit.frontpage    reddit
  code.name.monkey.retromusic    retromusic
  com.scientificcalculatorplus.simplecalculator.basiccalculator.mathcalc    simplecalendarpro
  com.simplemobiletools.smsmessenger    simplesmsmessenger
  org.telegram.messenger    telegram
  com.einnovation.temu    temu
  com.zhiliaoapp.musically    tiktok
  com.twitter.android    twitter    x
  org.videolan.vlc    vlc
  com.whatsapp    whatsapp
  com.taobao.movie.android    淘票票
  com.tongcheng.android    同程旅行    同程
  com.sankuai.movie    猫眼
  com.wuba.zhuanzhuan    转转
  com.tencent.weread    微信读书
  com.taobao.idlefish    闲鱼
  com.wudaokou.hippo    盒马
  com.eg.android.AlipayGphone    支付宝
  com.jd.jrapp    京东金融
  com.achievo.vipshop    唯品会
  com.smzdm.client.android    什么值得买
  cn.kuwo.player    酷我音乐
  com.taobao.trip    飞猪    飞猪旅行
  com.jingdong.pdj    京东到家
  com.tencent.map    腾讯地图
  com.shizhuang.duapp    得物
  cn.damai    大麦    大麦网
  com.ss.android.auto    懂车帝
  com.cubic.autohome    汽车之家
  com.wuba    58同城    五八同城
  com.android.calendar    日历
  com.alibaba.android.rimet    钉钉
  com.meituan.retail.v.android    小象超市
  com.aliyun.tongyi    通义    千问    通义千问
  com.hupu.games    虎扑    虎扑体育
  com.quark.browser    夸克    夸克浏览器
  com.yuantiku.tutor    猿辅导
  com.tencent.mtt    qq浏览器
  com.umetrip.android.msky.app    航旅纵横
  com.UCMobile    UC浏览器
  com.ss.android.ugc.aweme.lite    抖音极速版    抖音
  air.tv.douyu.android    斗鱼
  com.tencent.hunyuan.app.chat    元宝
  com.baidu.searchbox    百度
  com.lemon.lv    剪映
  cn.soulapp.android    soul
  com.baidu.netdisk    百度网盘
  com.tmri.app.main    交管12123    12123
  com.kugou.android    酷狗    酷狗音乐
  com.ss.android.lark    飞书
  com.tencent.android.qqdownloader    应用宝
  com.mt.mtxx.mtxx    美图    美图秀秀
  com.tencent.karaoke    全民k歌
  com.intsig.camscanner    扫描全能王
  com.android.bankabc    农业银行    农行
  cmb.pb    招商银行    招行
  com.ganji.android.haoche_c    瓜子二手车    瓜子
  com.sf.activity    顺丰    顺丰快递    顺丰速运
  com.ziroom.ziroomcustomer    自如
  com.yumc.phsuperapp    必胜客
  cn.dominos.pizza    达美乐披萨    达美乐
  cn.wps.moffice_eng    WPS Office    WPS
  com.mfw.roadbook    马蜂窝
  com.moonshot.kimichat    kimi
  com.tencent.wemeet.app    腾讯会议
  com.deepseek.chat    deepseek
  com.spdbccc.app    浦发银行
  cn.samsclub.app    山姆超市    山姆    山姆会员商店    山姆会员店
  com.tencent.qqsports    腾讯体育
  com.hanweb.android.zhejiang.activity    浙里办
  com.ss.android.article.video    西瓜视频
  com.taou.maimai    脉脉    '''

  PACKAGES_NAME_DICT = {}
  NAME_PACKAGE_DICT = {}

  def normalize_package_name(name):
    name = name.lower().strip().replace(" ", "").replace("-", "")
    return name

  for package_str in package_str_list.split("\n"):
    package_name = package_str.strip().split("\t")
    PACKAGES_NAME_DICT[package_name[0]] = [normalize_package_name(i) for i in package_name[1:]]
    for name in package_name[1:]:
      name = normalize_package_name(name)
      if name not in NAME_PACKAGE_DICT:
        NAME_PACKAGE_DICT[name] = [package_name[0]]
      else:
        NAME_PACKAGE_DICT[name].append(package_name[0])
  ```
</Accordion>

### 浏览器 GUI 任务

浏览器端通过 Playwright 控制浏览器实现自动化操作，并结合 SoM（Set-of-Mark）技术为页面元素自动添加数字标签，模型通过标签编号来精确操作网页元素。

**环境准备**：

1. 安装依赖：`pip install playwright pillow dashscope playwright-stealth termcolor`
2. 安装 Playwright 浏览器：`playwright install chromium`

完整示例代码包含以下核心流程：构造多轮对话消息、解析模型输出的工具调用、执行浏览器 GUI 操作。

<Accordion title="浏览器端完整示例代码">
  **步骤1：构造 System Prompt 和消息构造**

  浏览器自动化涉及多个模块的协同，包括 SoM 标注模块、Playwright 浏览器控制模块等。以下是核心代码片段：

  **SoM 标注模块核心函数**：

  SoM（Set-of-Mark）技术通过以下方式实现网页元素标注：

  - 收集页面可交互元素（按钮、链接、输入框等）
  - 为每个元素分配唯一数字标签
  - 在截图上绘制虚线框和标签
  - 生成元素的文本描述供模型理解

  **Playwright 浏览器控制**：

  浏览器控制模块提供以下核心功能：

  - 页面导航和加载
  - 元素点击和文本输入
  - 页面滚动和等待
  - 键盘快捷键操作
  - 新标签页处理

  **主链路运行**：

  自动化流程循环执行：获取页面状态（含 SoM 标注）`调用模型` 解析工具调用 \` 执行操作。
</Accordion>

## 工具调用模式

GUI-Plus 模型支持与其他工具或自定义函数结合使用，实现更复杂的自动化任务。

### 多轮对话模式

在多轮对话中，模型基于历史截图和输出生成连续的 GUI 操作指令。每次调用保留最近 4 轮完整对话（含截图），更早的历史仅保留文本摘要。

### 混合工具调用

模型可以同时调用 GUI 操作工具和自定义工具（如数据库查询、API 调用等），实现跨系统的复杂任务自动化。

### GUI + 网页操作

模型可以同时控制桌面应用和浏览器，实现跨应用的复合操作，如在桌面应用中获取数据后在浏览器中搜索。

## 图片格式限制

- 支持的图片格式：JPEG、PNG、WEBP、GIF
- 单图最大 Token 数：16,384
- 图片会被自动缩放到模型内部处理的尺寸
- 建议上传清晰的屏幕截图以获得最佳效果
- 过大的图片会增加 Token 消耗和响应时间

## 计费与限流

### 计费说明

- 按输入和输出 Token 数计费
- 图片会转换为 Token 进行计费
- 具体价格请参见[计费说明](/developer-guides/getting-started/pricing)

### 限流

- 请参见各模型的调用频率限制

## API 参考

- OpenAI 兼容接口：[Chat Completions](/api-reference/chat/openai-chat)
- DashScope 接口：[多模态对话](/api-reference/chat/dashscope)

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](/api-reference/preparation/error-messages)进行解决。

## GUI-Plus 模型推荐提示词

### 电脑端 System Prompt

以下系统提示词适用于 `gui-plus` 模型：

```python
"""# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.", "enum": ["key", "type", "mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click", "triple_click", "scroll", "hscroll", "wait", "terminate", "answer", "interact"], "type": "string"}, "keys": {"description": "Required only by `action=key`.", "type": "array"}, "text": {"description": "Required only by `action=type`, `action=answer` and `action=interact`.", "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.", "type": "array"}, "pixels": {"description": "The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.", "type": "number"}, "time": {"description": "The seconds to wait. Required only by `action=wait`.", "type": "number"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}}}
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
```

### 手机端 System Prompt

以下系统提示词适用于 `gui-plus` 模型：

```python
'''# Tools
You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name_for_human": "mobile_use", "name": "mobile_use", "description": "Use a touchscreen to interact with a mobile device, and take screenshots.\n* This is an interface to a mobile device with touchscreen. You can perform actions like clicking, typing, swiping, etc.\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions.\n* The screen's resolution is 1000x1000.\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.", "parameters": {"properties": {"action": {"description": "The action to perform. The available actions are:\n* `key`: Perform a key event on the mobile device.\n  - This supports adb's `keyevent` syntax.\n  - Examples: \"volume_up\", \"volume_down\", \"power\", \"camera\", \"clear\".\n* `click`: Click the point on the screen with coordinate (x, y).\n* `long_press`: Press the point on the screen with coordinate (x, y) for specified seconds.\n* `swipe`: Swipe from the starting point with coordinate (x, y) to the end point with coordinates2 (x2, y2).\n* `type`: Input the specified text into the activated input box.\n* `system_button`: Press the system button.\n* `open`: Open an app on the device.\n* `wait`: Wait specified seconds for the change to happen.\n* `answer`: Terminate the current task and output the answer.\n* `interact`: Resolve the blocking window by interacting with the user.\n* `terminate`: Terminate the current task and report its completion status.", "enum": ["key", "click", "long_press", "swipe", "type", "system_button", "open", "wait", "answer", "interact", "terminate"], "type": "string"}, "coordinate": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=click`, `action=long_press`, and `action=swipe`.", "type": "array"}, "coordinate2": {"description": "(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=swipe`.", "type": "array"}, "text": {"description": "Required only by `action=key`, `action=type`, `action=open`, `action=answer`,and `action=interact`.", "type": "string"}, "time": {"description": "The seconds to wait. Required only by `action=long_press` and `action=wait`.", "type": "number"}, "button": {"description": "Back means returning to the previous interface, Home means returning to the desktop, Menu means opening the application background menu, and Enter means pressing the enter. Required only by `action=system_button`", "enum": ["Back", "Home", "Menu", "Enter"], "type": "string"}, "status": {"description": "The status of the task. Required only by `action=terminate`.", "type": "string", "enum": ["success", "failure"]}}, "required": ["action"], "type": "object"}, "args_format": "Format the arguments as a JSON object."}}
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
- If finishing, use action=terminate in the tool call.'''
```

## 相关文档

- [API Key](/developer-guides/administration/api-keys)
- [计费说明](/developer-guides/getting-started/pricing)
