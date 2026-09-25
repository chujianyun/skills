> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sambert WebSocket API 参考

> 通过 WebSocket 长连接实时合成 Sambert 语音，支持流式音频输出与字/音素级时间戳

本文介绍通过 WebSocket 连接访问 Sambert 实时语音合成服务的交互流程、服务端点和请求头。

DashScope SDK 目前仅支持 Java 和 Python。使用其他编程语言时，可通过 WebSocket 连接与服务进行通信。

**用户指南**： 关于模型介绍和选型建议请参见[语音合成](/developer-guides/speech/tts)。

## 服务端点

WebSocket 服务端点固定为：`wss://dashscope.aliyuncs.com/api-ws/v1/inference`

<Warning>
  URL 必须使用 `wss://` 协议，且固定不变。Authorization 在请求头中设置（参见[请求头](#请求头)）。
</Warning>

## 请求头

请求头中需添加如下信息：

| 参数                         | 类型     | 是否必选 | 说明                                          |
| -------------------------- | ------ | ---- | ------------------------------------------- |
| Authorization              | string | 是    | `Bearer $DASHSCOPE_API_KEY`                 |
| user-agent                 | string | 否    | 客户端标识，便于服务端追踪来源。                            |
| X-DashScope-WorkSpace      | string | 否    | 千问AI平台业务空间 ID。                              |
| X-DashScope-DataInspection | string | 否    | 是否启用数据合规检测功能。默认不传或设为 `enable`。如非必要，请勿启用该参数。 |

<Warning>
  Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。
</Warning>

## 交互流程

客户端事件和服务端事件的详细说明，请参见[客户端事件](/api-reference/speech-synthesis/sambert/client-events)和[服务端事件](/api-reference/speech-synthesis/sambert/server-events)。

按时间顺序，客户端与服务端的交互流程如下：

1. **建立连接**：客户端与服务端建立 WebSocket 连接。
2. **开启任务**：客户端发送 run-task 事件以开启任务。Sambert 在 run-task 中一次性发送全部待合成文本。
3. **等待确认**：客户端收到服务端返回的 task-started 事件，标志着任务已成功开启。
4. **接收音频**：客户端通过 `binary` 通道接收服务端持续返回的音频流，同时收到 result-generated 事件（携带时间戳等附加信息）。
5. **任务结束**：客户端收到服务端返回的 task-finished 事件，标志着任务结束。
6. **关闭连接**：客户端关闭 WebSocket 连接。

为提高资源利用率，建议复用 WebSocket 连接处理多个任务，而非为每个任务建立新连接。

<Warning>
  Sambert 不支持流式输入（streaming 为 `out` 而非 duplex），所有待合成文本必须在 run-task 事件中一次性发送。不支持 continue-task 和 finish-task 指令。
</Warning>

## 前提条件

- 已获取 DashScope API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。
- 网络环境支持访问 `dashscope.aliyuncs.com`（国内访问）。

## 约束

- WebSocket 连接建立后，需先发送 `run-task` 指令，服务端才会开始合成并推送音频。
- 一次 WebSocket 连接只对应一次合成任务（一个 `task_id`）。任务完成（`task-finished`）后可复用同一连接发起新任务；任务失败（`task-failed`）后连接将被关闭，需重新建立连接。
- 待合成文本长度上限：一次 `run-task` 请求不超过 **10,000** 个字符（含标点）。

### 二、异步监听服务器返回的消息

服务端返回两种类型的消息：

- **二进制消息**：音频数据流，客户端直接写入文件或播放缓冲区。
- **文本消息（JSON）**：事件通知，包含以下类型：

**服务端消息 header 字段说明**

| 字段               | 类型     | 说明                                                                   |
| ---------------- | ------ | -------------------------------------------------------------------- |
| `header`         | Object | 消息头                                                                  |
| `header.event`   | String | 事件类型：`task-started`、`result-generated`、`task-finished`、`task-failed` |
| `header.task_id` | String | 任务 ID，与发送 `run-task` 时的 `task_id` 一致                                 |

**task-started 事件**

```json
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-started",
        "attributes": {}
    },
    "payload": {}
}
```

**result-generated 事件**（含时间戳示例）

```json
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "result-generated",
        "attributes": {}
    },
    "payload": {
        "output": {
            "sentence": {
                "begin_time": 0,
                "end_time": 1162,
                "words": [
                    {
                        "text": "床",
                        "begin_time": 0,
                        "end_time": 263,
                        "phonemes": [
                            {
                                "begin_time": 0,
                                "end_time": 119,
                                "text": "ch_c",
                                "tone": 2
                            },
                            {
                                "begin_time": 119,
                                "end_time": 263,
                                "text": "uang_c",
                                "tone": 2
                            }
                        ]
                    }
                ]
            }
        },
        "usage": null
    }
}
```

`output.sentence` 字段说明：

| 字段           | 类型      | 说明                                        |
| ------------ | ------- | ----------------------------------------- |
| `begin_time` | Integer | 句子开始时间（毫秒）                                |
| `end_time`   | Integer | 句子结束时间（毫秒）                                |
| `words`      | Array   | 字级别时间戳列表（开启 `word_timestamp_enabled` 后返回） |

`words` 中每个元素的字段：

| 字段           | 类型      | 说明                                           |
| ------------ | ------- | -------------------------------------------- |
| `text`       | String  | 汉字文本                                         |
| `begin_time` | Integer | 开始时间（毫秒）                                     |
| `end_time`   | Integer | 结束时间（毫秒）                                     |
| `phonemes`   | Array   | 音素级时间戳列表（开启 `phoneme_timestamp_enabled` 后返回） |

`phonemes` 中每个元素的字段：

| 字段           | 类型      | 说明             |
| ------------ | ------- | -------------- |
| `begin_time` | Integer | 开始时间（毫秒）       |
| `end_time`   | Integer | 结束时间（毫秒）       |
| `text`       | String  | 音素文本           |
| `tone`       | Integer | 声调（1–4，0 表示轻声） |

**task-finished 事件**

```json
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-finished",
        "attributes": {}
    },
    "payload": {
        "output": null,
        "usage": {
            "characters": 6
        }
    }
}
```

**task-failed 事件**

```json
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-failed",
        "error_code": "CLIENT_ERROR",
        "error_message": "request timeout after 23 seconds.",
        "attributes": {}
    },
    "payload": {}
}
```

`task-failed` 错误字段说明：

| 字段                     | 类型     | 说明                                    |
| ---------------------- | ------ | ------------------------------------- |
| `header.error_code`    | String | 错误码，如 `CLIENT_ERROR`、`SERVER_ERROR` 等 |
| `header.error_message` | String | 错误详情描述                                |

### 三、给服务器发送消息

客户端只需发送一条 JSON 消息：`run-task` 指令。

**消息结构**

```json
{
    "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "out"
    },
    "payload": {
        "model": "sambert-zhichu-v1",
        "task_group": "audio",
        "task": "tts",
        "function": "SpeechSynthesizer",
        "input": {
            "text": "床前明月光，"
        },
        "parameters": {
            "text_type": "PlainText",
            "format": "mp3",
            "sample_rate": 16000,
            "volume": 50,
            "rate": 1,
            "pitch": 1,
            "word_timestamp_enabled": true,
            "phoneme_timestamp_enabled": true
        }
    }
}
```

**run-task header 字段说明**

| 字段                 | 类型     | 必填 | 说明                         |
| ------------------ | ------ | -- | -------------------------- |
| `header.action`    | String | 是  | 固定值 `run-task`             |
| `header.task_id`   | String | 是  | 任务 ID，格式为随机 UUID，同一连接内不可重复 |
| `header.streaming` | String | 是  | 固定值 `out`，表示流式输出           |

Python 生成 UUID 示例：

```python
import uuid

def generate_task_id():
  # 生成随机UUID
  return uuid.uuid4().hex
```

**run-task payload 参数说明**

| 参数                                     | 类型      | 必填 | 说明                                        |
| -------------------------------------- | ------- | -- | ----------------------------------------- |
| `task_group`                           | String  | 是  | 固定值 `audio`                               |
| `task`                                 | String  | 是  | 固定值 `tts`                                 |
| `function`                             | String  | 是  | 固定值 `SpeechSynthesizer`                   |
| `model`                                | String  | 是  | 模型名称，详见[模型列表](#模型列表)                      |
| `input.text`                           | String  | 是  | 待合成文本，最长 10,000 个字符                       |
| `parameters.text_type`                 | String  | 否  | 文本类型。`PlainText`（默认）：纯文本；`SSML`：SSML 标记语言 |
| `parameters.format`                    | String  | 否  | 音频格式。支持 `pcm`、`wav`、`mp3`（默认 `pcm`）       |
| `parameters.sample_rate`               | Integer | 否  | 采样率（Hz）。默认值由模型决定，常见值为 `16000`、`48000`     |
| `parameters.volume`                    | Integer | 否  | 音量，范围 `0`–`100`，默认 `50`                   |
| `parameters.rate`                      | Float   | 否  | 语速，范围 `0.5`–`2.0`，默认 `1.0`（1.0 为正常语速）     |
| `parameters.pitch`                     | Float   | 否  | 音调，范围 `0.5`–`2.0`，默认 `1.0`（1.0 为正常音调）     |
| `parameters.word_timestamp_enabled`    | Boolean | 否  | 是否返回字级别时间戳，默认 `false`                     |
| `parameters.phoneme_timestamp_enabled` | Boolean | 否  | 是否返回音素级别时间戳，默认 `false`                    |

### 四、关闭 WebSocket 连接

收到 `task-finished` 事件后，客户端可选择：

- **关闭连接**：调用 WebSocket 关闭接口（推荐在不再需要合成时关闭）。
- **复用连接**：使用新的 `task_id` 发送下一个 `run-task` 指令，继续合成新文本，无需重新建立连接（节省握手开销）。

收到 `task-failed` 事件后，连接由服务端关闭，客户端需要重新建立连接。

## 关于建连开销和连接复用

建立 WebSocket 连接需要 TLS 握手，有一定延迟开销。对于需要高频合成的场景，建议：

- 维持长连接，通过切换 `task_id` 复用同一连接。
- 对连接进行池化管理，避免频繁断连重连。

## 示例代码

<CodeGroup>
  ```go Go
  package main

  import (
      "encoding/json"
      "fmt"
      "net/http"
      "os"
      "time"

      "github.com/google/uuid"
      "github.com/gorilla/websocket"
  )

  const (
      wsURL      = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/" // WebSocket服务器地址
      outputFile = "output.mp3"                                        // 输出文件路径
  )

  func main() {
      // 若没有将API Key配置到环境变量，可将下行替换为：apiKey := "your_api_key"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
      apiKey := os.Getenv("DASHSCOPE_API_KEY")

      if err := clearOutputFile(outputFile); err != nil {
          fmt.Println("清空输出文件失败：", err)
          return
      }

      conn, err := connectWebSocket(apiKey)
      if err != nil {
          fmt.Println("连接WebSocket失败：", err)
          return
      }
      defer closeConnection(conn)

      done := make(chan struct{})
      go receiveMessage(conn, done)

      if err := sendRunTaskMsg(conn); err != nil {
          fmt.Println("发送run-task指令失败：", err)
          return
      }

      select {
      case <-done:
          fmt.Println("任务结束")
      case <-time.After(5 * time.Minute):
          fmt.Println("任务超时")
      }
  }

  type Message struct {
      Header  Header  `json:"header"`
      Payload Payload `json:"payload"`
  }

  type Header struct {
      Action       string                 `json:"action,omitempty"`
      TaskID       string                 `json:"task_id"`
      Streaming    string                 `json:"streaming,omitempty"`
      Event        string                 `json:"event,omitempty"`
      ErrorCode    string                 `json:"error_code,omitempty"`
      ErrorMessage string                 `json:"error_message,omitempty"`
      Attributes   map[string]interface{} `json:"attributes"`
  }

  type Payload struct {
      Model      string     `json:"model,omitempty"`
      TaskGroup  string     `json:"task_group,omitempty"`
      Task       string     `json:"task,omitempty"`
      Function   string     `json:"function,omitempty"`
      Input      Input      `json:"input,omitempty"`
      Parameters Parameters `json:"parameters,omitempty"`
      Output     Output     `json:"output,omitempty"`
      Usage      Usage      `json:"usage,omitempty"`
  }

  type Input struct {
      Text string `json:"text"`
  }

  type Parameters struct {
      TextType                string  `json:"text_type"`
      Format                  string  `json:"format"`
      SampleRate              int     `json:"sample_rate"`
      Volume                  int     `json:"volume"`
      Rate                    float64 `json:"rate"`
      Pitch                   float64 `json:"pitch"`
      WordTimestampEnabled    bool    `json:"word_timestamp_enabled"`
      PhonemeTimestampEnabled bool    `json:"phoneme_timestamp_enabled"`
  }

  type Output struct {
      Sentence Sentence `json:"sentence"`
  }

  type Sentence struct {
      BeginTime int    `json:"begin_time"`
      EndTime   int    `json:"end_time"`
      Words     []Word `json:"words"`
  }

  type Word struct {
      Text      string    `json:"text"`
      BeginTime int       `json:"begin_time"`
      EndTime   int       `json:"end_time"`
      Phonemes  []Phoneme `json:"phonemes"`
  }

  type Phoneme struct {
      BeginTime int    `json:"begin_time"`
      EndTime   int    `json:"end_time"`
      Text      string `json:"text"`
      Tone      int    `json:"tone"`
  }

  type Usage struct {
      Characters int `json:"characters"`
  }

  func receiveMessage(conn *websocket.Conn, done chan struct{}) {
      for {
          msgType, message, err := conn.ReadMessage()
          if err != nil {
              fmt.Println("解析服务器消息失败：", err)
              close(done)
              break
          }

          if msgType == websocket.BinaryMessage {
              if err := writeBinaryDataToFile(message, outputFile); err != nil {
                  fmt.Println("写入二进制数据失败：", err)
                  close(done)
                  break
              }
              fmt.Println("音频片段已写入本地文件")
          } else {
              var msg Message
              if err := json.Unmarshal(message, &msg); err != nil {
                  fmt.Println("解析事件失败：", err)
                  continue
              }
              if handleMessage(conn, msg, done) {
                  break
              }
          }
      }
  }

  func handleMessage(conn *websocket.Conn, msg Message, done chan struct{}) bool {
      switch msg.Header.Event {
      case "task-started":
          fmt.Println("任务已启动")
      case "result-generated":
          // 如需获取附加消息，可在此处添加相应代码
      case "task-finished":
          fmt.Println("任务已完成")
          close(done)
          return true
      case "task-failed":
          if msg.Header.ErrorMessage != "" {
              fmt.Printf("任务失败：%s\n", msg.Header.ErrorMessage)
          } else {
              fmt.Println("未知原因导致任务失败")
          }
          close(done)
          return true
      default:
          fmt.Printf("预料之外的事件：%v\n", msg)
          close(done)
      }
      return false
  }

  func sendRunTaskMsg(conn *websocket.Conn) error {
      runTaskMsg, err := generateRunTaskMsg()
      if err != nil {
          return err
      }
      return conn.WriteMessage(websocket.TextMessage, []byte(runTaskMsg))
  }

  func generateRunTaskMsg() (string, error) {
      runTaskMessage := Message{
          Header: Header{
              Action:    "run-task",
              TaskID:    uuid.New().String(),
              Streaming: "out",
          },
          Payload: Payload{
              Model:     "sambert-zhichu-v1",
              TaskGroup: "audio",
              Task:      "tts",
              Function:  "SpeechSynthesizer",
              Input: Input{
                  Text: "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
              },
              Parameters: Parameters{
                  TextType:                "PlainText",
                  Format:                  "mp3",
                  SampleRate:              16000,
                  Volume:                  50,
                  Rate:                    1.0,
                  Pitch:                   1.0,
                  WordTimestampEnabled:    true,
                  PhonemeTimestampEnabled: true,
              },
          },
      }
      runTaskMsgJSON, err := json.Marshal(runTaskMessage)
      return string(runTaskMsgJSON), err
  }

  func connectWebSocket(apiKey string) (*websocket.Conn, error) {
      header := make(http.Header)
      header.Add("X-DashScope-DataInspection", "enable")
      header.Add("Authorization", fmt.Sprintf("Bearer %s", apiKey))
      conn, _, err := websocket.DefaultDialer.Dial(wsURL, header)
      if err != nil {
          fmt.Println("连接WebSocket失败：", err)
          return nil, err
      }
      return conn, nil
  }

  func writeBinaryDataToFile(data []byte, filePath string) error {
      file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
      if err != nil {
          return err
      }
      defer file.Close()
      _, err = file.Write(data)
      return err
  }

  func closeConnection(conn *websocket.Conn) {
      if conn != nil {
          conn.Close()
      }
  }

  func clearOutputFile(filePath string) error {
      file, err := os.OpenFile(filePath, os.O_TRUNC|os.O_CREATE|os.O_WRONLY, 0644)
      if err != nil {
          return err
      }
      file.Close()
      return nil
  }
  ```

  ```csharp C#
  using System.Net.WebSockets;
  using System.Text;
  using System.Text.Json;

  class Program {
      // 若没有将API Key配置到环境变量，可将下行替换为：private const string ApiKey="REDACTED"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
      private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

      private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/";
      private const string OutputFilePath = "output.mp3";

      static async Task Main(string[] args) {
          var ws = new ClientWebSocket();
          try {
              await ConnectWithAuth(ws, WebSocketUrl);
              var receiveTask = ReceiveMessages(ws);

              string textToSynthesize = "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。";
              string taskId = GenerateTaskId();
              await SendRunTaskCommand(ws, textToSynthesize, taskId);

              await receiveTask;
          } catch (Exception ex) {
              Console.WriteLine($"错误：{ex.Message}");
          } finally {
              if (ws.State == WebSocketState.Open) {
                  await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, "关闭连接", CancellationToken.None);
              }
          }
      }

      private static async Task ConnectWithAuth(ClientWebSocket ws, string url) {
          var uri = new Uri(url);
          ws.Options.SetRequestHeader("Authorization", $"Bearer {ApiKey}");
          ws.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");
          await ws.ConnectAsync(uri, CancellationToken.None);
          Console.WriteLine("已连接到WebSocket服务器。");
      }

      private static string GenerateTaskId() {
          return Guid.NewGuid().ToString("N");
      }

      private static async Task SendRunTaskCommand(ClientWebSocket ws, string text, string taskId) {
          var command = CreateRunTaskCommand(text, taskId);
          var buffer = Encoding.UTF8.GetBytes(command);
          await ws.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, CancellationToken.None);
          Console.WriteLine("已发送run-task指令。");
      }

      private static string CreateRunTaskCommand(string text, string taskId) {
          var command = new {
              header = new {
                  action = "run-task",
                  task_id = taskId,
                  streaming = "out"
              },
              payload = new {
                  model = "sambert-zhichu-v1",
                  task_group = "audio",
                  task = "tts",
                  function = "SpeechSynthesizer",
                  input = new { text = text },
                  parameters = new {
                      text_type = "PlainText",
                      format = "mp3",
                      sample_rate = 16000,
                      volume = 50,
                      rate = 1,
                      pitch = 1,
                      word_timestamp_enabled = true,
                      phoneme_timestamp_enabled = true
                  }
              }
          };
          return JsonSerializer.Serialize(command);
      }

      private static async Task ReceiveMessages(ClientWebSocket ws) {
          var buffer = new byte[1024 * 4];
          var fs = new FileStream(OutputFilePath, FileMode.Create, FileAccess.Write);
          bool taskStarted = false;
          bool taskFinished = false;

          while (ws.State == WebSocketState.Open && !taskFinished) {
              var result = await ws.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);

              switch (result.MessageType) {
                  case WebSocketMessageType.Text:
                      var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                      var jsonMessage = JsonSerializer.Deserialize<JsonElement>(message);
                      ProcessTextMessage(jsonMessage, ref taskStarted, ref taskFinished);
                      break;
                  case WebSocketMessageType.Binary:
                      if (taskStarted) {
                          await fs.WriteAsync(buffer, 0, result.Count);
                          Console.WriteLine("收到音频数据。");
                      }
                      break;
                  case WebSocketMessageType.Close:
                      Console.WriteLine("服务器关闭了连接。");
                      taskFinished = true;
                      break;
              }
          }
          fs.Close();
      }

      private static void ProcessTextMessage(JsonElement jsonMessage, ref bool taskStarted, ref bool taskFinished) {
          if (jsonMessage.TryGetProperty("header", out JsonElement header) &&
              header.TryGetProperty("event", out JsonElement eventToken)) {
              var eventType = eventToken.GetString();
              switch (eventType) {
                  case "task-started":
                      taskStarted = true;
                      Console.WriteLine("任务开始。");
                      break;
                  case "result-generated":
                      // 如需获取附加消息，可在此处添加相应代码
                      break;
                  case "task-finished":
                      taskFinished = true;
                      Console.WriteLine("任务完成。");
                      break;
                  case "task-failed":
                      taskFinished = true;
                      Console.WriteLine("任务失败。");
                      break;
              }
          }
      }
  }
  ```

  ```php PHP (composer.json)
  {
      "require": {
          "react/event-loop": "^1.3",
          "react/socket": "^1.11",
          "react/stream": "^1.2",
          "react/http": "^1.1",
          "ratchet/pawl": "^0.4"
      },
      "autoload": {
          "psr-4": {
              "App\\": "src/"
          }
      }
  }
  ```

  ```php PHP
  <?php

  require 'vendor/autoload.php';

  use Ratchet\Client\Connector;
  use React\EventLoop\Loop;
  use React\Socket\Connector as SocketConnector;

  # 若没有将API Key配置到环境变量，可将下行替换为：$api_key="REDACTED"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
  $api_key = getenv("DASHSCOPE_API_KEY");
  $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/';
  $output_file = 'output.mp3';

  $loop = Loop::get();

  if (file_exists($output_file)) {
      file_put_contents($output_file, '');
      echo "文件已清空\n";
  }

  $socketConnector = new SocketConnector($loop, [
      'tcp' => ['bindto' => '0.0.0.0:0'],
      'tls' => [
          'verify_peer' => false,
          'verify_peer_name' => false,
      ],
  ]);

  $connector = new Connector($loop, $socketConnector);

  $headers = [
      'Authorization' => 'Bearer ' . $api_key,
      'X-DashScope-DataInspection' => 'enable'
  ];

  $connector($websocket_url, [], $headers)
      ->then(function ($conn) use ($output_file) {
          echo "连接成功\n";

          $conn->on('message', function ($msg) use ($conn, $output_file) {
              if ($msg->isBinary()) {
                  file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
                  echo "二进制数据写入文件\n";
              } else {
                  $data = json_decode($msg, true);
                  switch ($data['header']['event']) {
                      case 'task-started':
                          echo "任务开始\n";
                          break;
                      case 'result-generated':
                          // 如需获取附加消息，可在此处添加相应代码
                          break;
                      case 'task-finished':
                          echo "任务完成\n";
                          $conn->close();
                          break;
                      case 'task-failed':
                          echo "任务失败：" . $data['header']['error_message'] . "\n";
                          $conn->close();
                          break;
                      default:
                          echo "未知事件：" . $msg . "\n";
                  }
              }
          });

          $conn->on('close', function($code = null, $reason = null) {
              echo "连接已关闭\n";
              if ($code !== null) echo "关闭代码：" . $code . "\n";
              if ($reason !== null) echo "关闭原因：" . $reason . "\n";
          });

          $conn->send(json_encode([
              'header' => [
                  'action' => 'run-task',
                  'task_id' => bin2hex(random_bytes(16)),
                  'streaming' => 'out'
              ],
              'payload' => [
                  'model' => 'sambert-zhichu-v1',
                  'task_group' => 'audio',
                  'task' => 'tts',
                  'function' => 'SpeechSynthesizer',
                  'input' => ['text' => '床前明月光，疑是地上霜。举头望明月，低头思故乡。'],
                  'parameters' => [
                      'text_type' => 'PlainText',
                      'format' => 'mp3',
                      'sample_rate' => 16000,
                      'volume' => 50,
                      'rate' => 1,
                      'pitch' => 1,
                      'word_timestamp_enabled' => true,
                      'phoneme_timestamp_enabled' => true
                  ]
              ]
          ]));
          echo "run-task指令已发送\n";
      }, function (Exception $e) {
          echo "连接失败：{$e->getMessage()}\n";
          file_put_contents('error.log', $e->getMessage() . "\n", FILE_APPEND);
      });

  $loop->run();
  ```

  ```bash Node.js 安装依赖
  npm install ws
  npm install uuid
  ```

  ```javascript Node.js
  const WebSocket = require('ws');
  const fs = require('fs');
  const { v4: uuidv4 } = require('uuid');

  // 若没有将API Key配置到环境变量，可将下行替换为：apiKey = 'REDACTED'。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
  const apiKey = process.env.DASHSCOPE_API_KEY;
  const wsUrl = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/';
  const outputFilePath = 'output.mp3';

  async function main() {
    await checkAndClearOutputFile(outputFilePath);
    createWebSocketConnection();
  }

  const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });

  function createWebSocketConnection() {
    const ws = new WebSocket(wsUrl, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'X-DashScope-DataInspection': 'enable'
      }
    });

    ws.on('open', () => {
      console.log('已连接到WebSocket服务器');
      sendRunTaskMessage(ws);
    });

    ws.on('message', (data, isBinary) => handleWebSocketMessage(data, isBinary, ws));
    ws.on('error', (error) => console.error('WebSocket错误:', error));
    ws.on('close', () => console.log('WebSocket连接已关闭'));

    return ws;
  }

  function sendRunTaskMessage(ws) {
    const taskId = uuidv4();
    const runTaskMessage = {
      header: {
        action: 'run-task',
        task_id: taskId,
        streaming: 'out'
      },
      payload: {
        model: 'sambert-zhichu-v1',
        task_group: 'audio',
        task: 'tts',
        function: 'SpeechSynthesizer',
        input: {
          text: '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。'
        },
        parameters: {
          text_type: 'PlainText',
          format: 'mp3',
          sample_rate: 16000,
          volume: 50,
          rate: 1,
          pitch: 1,
          word_timestamp_enabled: true,
          phoneme_timestamp_enabled: true
        }
      }
    };
    ws.send(JSON.stringify(runTaskMessage));
    console.log('run-task指令已发送');
  }

  function handleWebSocketMessage(data, isBinary, ws) {
    if (isBinary) {
      fileStream.write(data);
    } else {
      const message = JSON.parse(data);
      handleWebSocketEvent(message, ws);
    }
  }

  function handleWebSocketEvent(message, ws) {
    switch (message.header.event) {
      case 'task-started':
        console.log('任务已启动');
        break;
      case 'result-generated':
        console.log('结果已生成');
        break;
      case 'task-finished':
        console.log('任务已完成');
        ws.close();
        fileStream.end(() => console.log('文件流已关闭'));
        break;
      case 'task-failed':
        console.error('任务失败：', message.header.error_message);
        ws.close();
        fileStream.end(() => console.log('文件流已关闭'));
        break;
      default:
        console.log('未知事件：', message.header.event);
    }
  }

  function checkAndClearOutputFile(filePath) {
    return new Promise((resolve, reject) => {
      fs.access(filePath, fs.F_OK, (err) => {
        if (!err) {
          fs.truncate(filePath, 0, (truncateErr) => {
            if (truncateErr) return reject(truncateErr);
            console.log('文件已清空');
            resolve();
          });
        } else {
          fs.open(filePath, 'w', (openErr) => {
            if (openErr) return reject(openErr);
            console.log('文件已创建');
            resolve();
          });
        }
      });
    });
  }

  main().catch(console.error);
  ```
</CodeGroup>

## 错误码

通用错误码请参阅[错误信息](/api-reference/preparation/error-messages)。

WebSocket 特有错误通过 `task-failed` 事件返回，错误码位于 `header.error_code`，错误信息位于 `header.error_message`。

## 常见问题

**Q：连接建立后没有收到任何音频数据？**

A：请确认已发送 `run-task` 指令，且指令格式正确。检查 `payload.input.text` 是否非空，`model` 是否为有效的模型名称。

**Q：`task-failed` 错误码为 `CLIENT_ERROR`，错误信息包含 `timeout`？**

A：连接建立后需在较短时间内（通常 23 秒内）发送 `run-task` 指令，否则服务端会超时并关闭连接。

**Q：能否在同一连接内合成多段文本？**

A：可以。收到 `task-finished` 后，使用不同的 `task_id` 再次发送 `run-task` 指令即可。注意 `task-failed` 后连接已关闭，需重新建连。

## 模型列表

### 中文音色（48 kHz）

| 音色名  | model 参数            | 时间戳支持 | 适用场景  | 特色    | 默认采样率（Hz） |
| ---- | ------------------- | ----- | ----- | ----- | --------- |
| 广告男声 | sambert-zhinan-v1   | 是     | 广告配音  | 磁性、自信 | 48000     |
| 温柔女声 | sambert-zhiqi-v1    | 是     | 情感类内容 | 柔和、亲切 | 48000     |
| 舌尖男声 | sambert-zhichu-v1   | 是     | 通用    | 清晰、标准 | 48000     |
| 新闻男声 | sambert-zhide-v1    | 是     | 新闻播报  | 沉稳、权威 | 48000     |
| 标准女声 | sambert-zhijia-v1   | 是     | 通用    | 标准、清晰 | 48000     |
| 新闻女声 | sambert-zhiru-v1    | 是     | 新闻播报  | 专业、流畅 | 48000     |
| 资讯女声 | sambert-zhiqian-v1  | 是     | 资讯播报  | 干练、利落 | 48000     |
| 磁性男声 | sambert-zhixiang-v1 | 是     | 有声读物  | 磁性、浑厚 | 48000     |
| 萝莉女声 | sambert-zhiwei-v1   | 是     | 动漫、娱乐 | 活泼、可爱 | 48000     |

### 中文音色（16 kHz）

| 音色名 | model 参数               | 时间戳支持 | 适用场景 | 语言 | 默认采样率（Hz） |
| --- | ---------------------- | ----- | ---- | -- | --------- |
| —   | sambert-zhihao-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhijing-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiming-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhimo-v1       | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhina-v1       | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhishu-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhistella-v1   | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiting-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhixiao-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiya-v1       | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiye-v1       | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiying-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiyuan-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhiyue-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhigui-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhishuo-v1     | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhimiao-emo-v1 | 是     | 情感类  | 中文 | 16000     |
| —   | sambert-zhimao-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhilun-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhifei-v1      | 是     | 通用   | 中文 | 16000     |
| —   | sambert-zhida-v1       | 是     | 通用   | 中文 | 16000     |

### 多语种音色（16 kHz）

| 音色名 | model 参数          | 时间戳支持 | 语言   | 默认采样率（Hz） |
| --- | ----------------- | ----- | ---- | --------- |
| —   | sambert-camila-v1 | 否     | 西班牙语 | 16000     |
| —   | sambert-perla-v1  | 否     | 意大利语 | 16000     |
| —   | sambert-indah-v1  | 否     | 印尼语  | 16000     |
| —   | sambert-clara-v1  | 否     | 法语   | 16000     |
| —   | sambert-hanna-v1  | 否     | 德语   | 16000     |

### 英语音色（美式，16 kHz）

| 音色名 | model 参数         | 时间戳支持 | 语言     | 默认采样率（Hz） |
| --- | ---------------- | ----- | ------ | --------- |
| —   | sambert-beth-v1  | 是     | 英语（美式） | 16000     |
| —   | sambert-betty-v1 | 是     | 英语（美式） | 16000     |
| —   | sambert-cally-v1 | 是     | 英语（美式） | 16000     |
| —   | sambert-cindy-v1 | 是     | 英语（美式） | 16000     |
| —   | sambert-eva-v1   | 是     | 英语（美式） | 16000     |
| —   | sambert-donna-v1 | 是     | 英语（美式） | 16000     |
| —   | sambert-brian-v1 | 是     | 英语（美式） | 16000     |

### 泰语音色（16 kHz）

| 音色名 | model 参数        | 时间戳支持 | 语言 | 默认采样率（Hz） |
| --- | --------------- | ----- | -- | --------- |
| —   | sambert-waan-v1 | 否     | 泰语 | 16000     |
