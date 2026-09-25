> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 实时语音识别 WebSocket API

> 通过 WebSocket 连接使用 Paraformer 实时语音识别服务的完整 API 参考。

Paraformer 实时语音识别通过 WebSocket 全双工协议实现流式语音输入与实时识别结果输出，适用于直播字幕、实时会议转写、电话客服等场景。

## 前提条件

- 已获取 API Key（参见[获取 API Key](/api-reference/preparation/api-key)）并配置到环境变量（参见[配置 API Key 到环境变量](/api-reference/preparation/export-api-key-env)）
- 如需临时访问，可使用[临时鉴权 Token](/api-reference/more/generate-a-temporary-api-key)

## 模型列表

| 特性   | paraformer-realtime-v2                                            | paraformer-realtime-8k-v2                                         | paraformer-realtime-v1                                                           | paraformer-realtime-8k-v1                                                        |
| ---- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 适用场景 | 直播、会议                                                             | 电话客服、语音信箱（8kHz）                                                   | 直播、会议                                                                            | 电话客服、语音信箱（8kHz）                                                                  |
| 采样率  | 任意                                                                | 8kHz                                                              | 16kHz                                                                            | 8kHz                                                                             |
| 语种   | 中文（含方言）、英、日、韩、德、法、俄                                               | 中文                                                                | 中文                                                                               | 中文                                                                               |
| 标点   | 默认支持                                                              | 默认支持                                                              | 默认支持                                                                             | 默认支持                                                                             |
| ITN  | 默认支持                                                              | 默认支持                                                              | 默认支持                                                                             | 默认支持                                                                             |
| 定制热词 | [定制热词（v2）](/developer-guides/speech/improve-recognition-accuracy) | [定制热词（v2）](/developer-guides/speech/improve-recognition-accuracy) | [Paraformer 热词定制与管理](/api-reference/speech-recognition/custom-hotwords/http-api) | [Paraformer 热词定制与管理](/api-reference/speech-recognition/custom-hotwords/http-api) |
| 指定语种 | ✓ `language_hints`                                                | ✗                                                                 | ✗                                                                                | ✗                                                                                |
| 情感识别 | ✗                                                                 | ✓（有约束条件）                                                          | ✗                                                                                | ✗                                                                                |

## 交互流程

与 Paraformer 实时语音识别服务交互须遵循以下步骤：

1. **建立 WebSocket 连接** — 使用 WebSocket 客户端库，向服务地址发起连接，并在请求头中携带 Authorization 鉴权信息。

2. **监听服务端消息（开启独立线程）** — 在独立于主线程的线程中异步监听服务端消息，并根据事件类型分别处理：
   - 收到 `task-started` 事件后，开始向服务端发送音频。
   - 收到 `result-generated` 事件后，处理识别结果。
   - 收到 `task-finished` 事件时，表示任务已完成，可关闭连接。
   - 收到 `task-failed` 事件时，表示任务失败，需关闭连接并根据错误信息排查。

3. **向服务端发送指令和二进制音频（请务必注意时序）** — 在主线程（或与监听线程不同的线程）中发送指令和音频，发送时序如下：
   1. 发送 `run-task` 指令，启动识别任务
   2. 收到 `task-started` 事件后，持续发送二进制音频（单声道）
   3. 音频发送完毕后，发送 `finish-task` 指令结束任务

4. **关闭 WebSocket 连接** — 在程序正常结束、出现异常或收到 `task-finished` / `task-failed` 事件后，调用客户端库的 `close` 方法关闭连接。

## 连接地址

```
wss://dashscope.aliyuncs.com/api-ws/v1/inference/
```

## 请求头

| 参数                           | 是否必填 | 说明                                          |
| ---------------------------- | ---- | ------------------------------------------- |
| `Authorization`              | 必填   | 鉴权信息，格式：`Bearer $DASHSCOPE_API_KEY`         |
| `user-agent`                 | 可选   | 用户代理标识，用于版本追踪                               |
| `X-DashScope-WorkSpace`      | 可选   | 业务空间 ID，用于指定请求所属业务空间                        |
| `X-DashScope-DataInspection` | 可选   | 是否启用数据合规检测功能。默认不传或设为 `enable`。如非必要，请勿启用该参数。 |

## 事件参考

客户端事件和服务端事件的详细参数说明请参见：

- [客户端事件](/api-reference/speech-recognition/paraformer-realtime/client-events)（`run-task`、二进制音频、`finish-task`）
- [服务端事件](/api-reference/speech-recognition/paraformer-realtime/server-events)（`task-started`、`result-generated`、`task-finished`、`task-failed`）

## 复用连接

同一 WebSocket 连接可复用于多个识别任务，但须注意：

- 每次新任务必须使用不同的 `task_id`。
- 若某次任务失败（收到 `task-failed`），连接将被关闭，不可复用。
- 任务结束后连接保持空闲超过 60 秒，服务端将主动关闭连接。

## 示例代码

以下示例使用音频文件 [asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241114/mgiguo/asr_example.wav) 演示完整交互流程。

<Tabs>
  <Tab title="Go">
    ```go
    package main

    import (
      "encoding/json"
      "fmt"
      "io"
      "log"
      "net/http"
      "os"
      "time"

      "github.com/google/uuid"
      "github.com/gorilla/websocket"
    )

    const (
      wsURL     = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/" // WebSocket服务器地址
      audioFile = "asr_example.wav"                                   // 替换为您的音频文件路径
    )

    var dialer = websocket.DefaultDialer

    func main() {
      // 若没有将API Key配置到环境变量，可将下行替换为：apiKey := "your_api_key"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
      apiKey := os.Getenv("DASHSCOPE_API_KEY")

      // 连接WebSocket服务
      conn, err := connectWebSocket(apiKey)
      if err != nil {
        log.Fatal("连接WebSocket失败：", err)
      }
      defer closeConnection(conn)

      // 启动一个goroutine来接收结果
      taskStarted := make(chan bool)
      taskDone := make(chan bool)
      startResultReceiver(conn, taskStarted, taskDone)

      // 发送run-task指令
      taskID, err := sendRunTaskCmd(conn)
      if err != nil {
        log.Fatal("发送run-task指令失败：", err)
      }

      // 等待task-started事件
      waitForTaskStarted(taskStarted)

      // 发送待识别音频文件流
      if err := sendAudioData(conn); err != nil {
        log.Fatal("发送音频失败：", err)
      }

      // 发送finish-task指令
      if err := sendFinishTaskCmd(conn, taskID); err != nil {
        log.Fatal("发送finish-task指令失败：", err)
      }

      // 等待任务完成或失败
      <-taskDone
    }

    // 定义结构体来表示JSON数据
    type Header struct {
      Action       string                 `json:"action"`
      TaskID       string                 `json:"task_id"`
      Streaming    string                 `json:"streaming"`
      Event        string                 `json:"event"`
      ErrorCode    string                 `json:"error_code,omitempty"`
      ErrorMessage string                 `json:"error_message,omitempty"`
      Attributes   map[string]interface{} `json:"attributes"`
    }

    type Output struct {
      Sentence struct {
        BeginTime int64  `json:"begin_time"`
        EndTime   *int64 `json:"end_time"`
        Text      string `json:"text"`
        Words     []struct {
          BeginTime   int64  `json:"begin_time"`
          EndTime     *int64 `json:"end_time"`
          Text        string `json:"text"`
          Punctuation string `json:"punctuation"`
        } `json:"words"`
      } `json:"sentence"`
    }

    type Payload struct {
      TaskGroup  string `json:"task_group"`
      Task       string `json:"task"`
      Function   string `json:"function"`
      Model      string `json:"model"`
      Parameters Params `json:"parameters"`
      Input  Input  `json:"input"`
      Output Output `json:"output,omitempty"`
      Usage  *struct {
        Duration int `json:"duration"`
      } `json:"usage,omitempty"`
    }

    type Params struct {
      Format                   string   `json:"format"`
      SampleRate               int      `json:"sample_rate"`
      DisfluencyRemovalEnabled bool     `json:"disfluency_removal_enabled"`
      LanguageHints            []string `json:"language_hints"`
    }

    type Input struct {
    }

    type Event struct {
      Header  Header  `json:"header"`
      Payload Payload `json:"payload"`
    }

    // 连接WebSocket服务
    func connectWebSocket(apiKey string) (*websocket.Conn, error) {
      header := make(http.Header)
      header.Add("Authorization", fmt.Sprintf("Bearer %s", apiKey))
      conn, _, err := dialer.Dial(wsURL, header)
      return conn, err
    }

    // 启动一个goroutine异步接收WebSocket消息
    func startResultReceiver(conn *websocket.Conn, taskStarted chan<- bool, taskDone chan<- bool) {
      go func() {
        for {
          _, message, err := conn.ReadMessage()
          if err != nil {
            log.Println("解析服务器消息失败：", err)
            return
          }
          var event Event
          err = json.Unmarshal(message, &event)
          if err != nil {
            log.Println("解析事件失败：", err)
            continue
          }
          if handleEvent(conn, event, taskStarted, taskDone) {
            return
          }
        }
      }()
    }

    // 发送run-task指令
    func sendRunTaskCmd(conn *websocket.Conn) (string, error) {
      runTaskCmd, taskID, err := generateRunTaskCmd()
      if err != nil {
        return "", err
      }
      err = conn.WriteMessage(websocket.TextMessage, []byte(runTaskCmd))
      return taskID, err
    }

    // 生成run-task指令
    func generateRunTaskCmd() (string, string, error) {
      taskID := uuid.New().String()
      runTaskCmd := Event{
        Header: Header{
          Action:    "run-task",
          TaskID:    taskID,
          Streaming: "duplex",
        },
        Payload: Payload{
          TaskGroup: "audio",
          Task:      "asr",
          Function:  "recognition",
          Model:     "paraformer-realtime-v2",
          Parameters: Params{
            Format:     "wav",
            SampleRate: 16000,
          },
          Input: Input{},
        },
      }
      runTaskCmdJSON, err := json.Marshal(runTaskCmd)
      return string(runTaskCmdJSON), taskID, err
    }

    // 等待task-started事件
    func waitForTaskStarted(taskStarted chan bool) {
      select {
      case <-taskStarted:
        fmt.Println("任务开启成功")
      case <-time.After(10 * time.Second):
        log.Fatal("等待task-started超时，任务开启失败")
      }
    }

    // 发送音频数据
    func sendAudioData(conn *websocket.Conn) error {
      file, err := os.Open(audioFile)
      if err != nil {
        return err
      }
      defer file.Close()

      buf := make([]byte, 1024) // 假设100ms的音频数据大约为1024字节
      for {
        n, err := file.Read(buf)
        if n == 0 {
          break
        }
        if err != nil && err != io.EOF {
          return err
        }
        err = conn.WriteMessage(websocket.BinaryMessage, buf[:n])
        if err != nil {
          return err
        }
        time.Sleep(100 * time.Millisecond)
      }
      return nil
    }

    // 发送finish-task指令
    func sendFinishTaskCmd(conn *websocket.Conn, taskID string) error {
      finishTaskCmd, err := generateFinishTaskCmd(taskID)
      if err != nil {
        return err
      }
      err = conn.WriteMessage(websocket.TextMessage, []byte(finishTaskCmd))
      return err
    }

    // 生成finish-task指令
    func generateFinishTaskCmd(taskID string) (string, error) {
      finishTaskCmd := Event{
        Header: Header{
          Action:    "finish-task",
          TaskID:    taskID,
          Streaming: "duplex",
        },
        Payload: Payload{
          Input: Input{},
        },
      }
      finishTaskCmdJSON, err := json.Marshal(finishTaskCmd)
      return string(finishTaskCmdJSON), err
    }

    // 处理事件
    func handleEvent(conn *websocket.Conn, event Event, taskStarted chan<- bool, taskDone chan<- bool) bool {
      switch event.Header.Event {
      case "task-started":
        fmt.Println("收到task-started事件")
        taskStarted <- true
      case "result-generated":
        if event.Payload.Output.Sentence.Text != "" {
          fmt.Println("识别结果：", event.Payload.Output.Sentence.Text)
        }
        if event.Payload.Usage != nil {
          fmt.Println("任务计费时长（秒）：", event.Payload.Usage.Duration)
        }
      case "task-finished":
        fmt.Println("任务完成")
        taskDone <- true
        return true
      case "task-failed":
        handleTaskFailed(event, conn)
        taskDone <- true
        return true
      default:
        log.Printf("预料之外的事件：%v", event)
      }
      return false
    }

    // 处理任务失败事件
    func handleTaskFailed(event Event, conn *websocket.Conn) {
      if event.Header.ErrorMessage != "" {
        log.Fatalf("任务失败：%s", event.Header.ErrorMessage)
      } else {
        log.Fatal("未知原因导致任务失败")
      }
    }

    // 关闭连接
    func closeConnection(conn *websocket.Conn) {
      if conn != nil {
        conn.Close()
      }
    }
    ```
  </Tab>

  <Tab title="C#">
    示例代码如下：

    ```csharp
    using System.Net.WebSockets;
    using System.Text;
    using System.Text.Json;
    using System.Text.Json.Nodes;

    class Program {
      private static ClientWebSocket _webSocket = new ClientWebSocket();
      private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
      private static bool _taskStartedReceived = false;
      private static bool _taskFinishedReceived = false;
      // 若没有将API Key配置到环境变量，可将下行替换为：private const string ApiKey="REDACTED"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
      private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

      // WebSocket服务器地址
      private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/";
      // 替换为您的音频文件路径
      private const string AudioFilePath = "asr_example.wav";

      static async Task Main(string[] args) {
        // 建立WebSocket连接，配置headers进行鉴权
        _webSocket.Options.SetRequestHeader("Authorization", $"Bearer {ApiKey}");

        await _webSocket.ConnectAsync(new Uri(WebSocketUrl), _cancellationTokenSource.Token);

        // 启动线程异步接收WebSocket消息
        var receiveTask = ReceiveMessagesAsync();

        // 发送run-task指令
        string _taskId = Guid.NewGuid().ToString("N"); // 生成32位随机ID
        var runTaskJson = GenerateRunTaskJson(_taskId);
        await SendAsync(runTaskJson);

        // 等待task-started事件
        while (!_taskStartedReceived) {
          await Task.Delay(100, _cancellationTokenSource.Token);
        }

        // 读取本地文件，向服务器发送待识别音频流
        await SendAudioStreamAsync(AudioFilePath);

        // 发送finish-task指令结束任务
        var finishTaskJson = GenerateFinishTaskJson(_taskId);
        await SendAsync(finishTaskJson);

        // 等待task-finished事件
        while (!_taskFinishedReceived && !_cancellationTokenSource.IsCancellationRequested) {
          try {
            await Task.Delay(100, _cancellationTokenSource.Token);
          } catch (OperationCanceledException) {
            // 任务已被取消，退出循环
            break;
          }
        }

        // 关闭连接
        if (!_cancellationTokenSource.IsCancellationRequested) {
          await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cancellationTokenSource.Token);
        }

        _cancellationTokenSource.Cancel();
        try {
          await receiveTask;
        } catch (OperationCanceledException) {
          // 忽略操作取消异常
        }
      }

      private static async Task ReceiveMessagesAsync() {
        try {
          while (_webSocket.State == WebSocketState.Open && !_cancellationTokenSource.IsCancellationRequested) {
            var message = await ReceiveMessageAsync(_cancellationTokenSource.Token);
            if (message != null) {
              var eventValue = message["header"]?["event"]?.GetValue<string>();
              switch (eventValue) {
                case "task-started":
                  Console.WriteLine("任务开启成功");
                  _taskStartedReceived = true;
                  break;
                case "result-generated":
                  Console.WriteLine($"识别结果：{message["payload"]?["output"]?["sentence"]?["text"]?.GetValue<string>()}");
                  if (message["payload"]?["usage"] != null && message["payload"]?["usage"]?["duration"] != null) {
                    Console.WriteLine($"任务计费时长（秒）：{message["payload"]?["usage"]?["duration"]?.GetValue<int>()}");
                  }
                  break;
                case "task-finished":
                  Console.WriteLine("任务完成");
                  _taskFinishedReceived = true;
                  _cancellationTokenSource.Cancel();
                  break;
                case "task-failed":
                  Console.WriteLine($"任务失败：{message["header"]?["error_message"]?.GetValue<string>()}");
                  _cancellationTokenSource.Cancel();
                  break;
              }
            }
          }
        } catch (OperationCanceledException) {
          // 忽略操作取消异常
        }
      }

      private static async Task<JsonNode?> ReceiveMessageAsync(CancellationToken cancellationToken) {
        var buffer = new byte[1024 * 4];
        var segment = new ArraySegment<byte>(buffer);
        var result = await _webSocket.ReceiveAsync(segment, cancellationToken);

        if (result.MessageType == WebSocketMessageType.Close) {
          await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", cancellationToken);
          return null;
        }

        var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
        return JsonNode.Parse(message);
      }

      private static async Task SendAsync(string message) {
        var buffer = Encoding.UTF8.GetBytes(message);
        var segment = new ArraySegment<byte>(buffer);
        await _webSocket.SendAsync(segment, WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
      }

      private static async Task SendAudioStreamAsync(string filePath) {
        using (var audioStream = File.OpenRead(filePath)) {
          var buffer = new byte[1024]; // 每次发送100ms的音频数据
          int bytesRead;

          while ((bytesRead = await audioStream.ReadAsync(buffer, 0, buffer.Length)) > 0) {
            var segment = new ArraySegment<byte>(buffer, 0, bytesRead);
            await _webSocket.SendAsync(segment, WebSocketMessageType.Binary, true, _cancellationTokenSource.Token);
            await Task.Delay(100); // 间隔100ms
          }
        }
      }

      private static string GenerateRunTaskJson(string taskId) {
        var runTask = new JsonObject {
          ["header"] = new JsonObject {
            ["action"] = "run-task",
            ["task_id"] = taskId,
            ["streaming"] = "duplex"
          },
          ["payload"] = new JsonObject {
            ["task_group"] = "audio",
            ["task"] = "asr",
            ["function"] = "recognition",
            ["model"] = "paraformer-realtime-v2",
            ["parameters"] = new JsonObject {
              ["format"] = "wav",
              ["sample_rate"] = 16000,
              ["disfluency_removal_enabled"] = false
            },
            ["input"] = new JsonObject()
          }
        };
        return JsonSerializer.Serialize(runTask);
      }

      private static string GenerateFinishTaskJson(string taskId) {
        var finishTask = new JsonObject {
          ["header"] = new JsonObject {
            ["action"] = "finish-task",
            ["task_id"] = taskId,
            ["streaming"] = "duplex"
          },
          ["payload"] = new JsonObject {
            ["input"] = new JsonObject()
          }
        };
        return JsonSerializer.Serialize(finishTask);
      }
    }
    ```
  </Tab>

  <Tab title="PHP">
    示例代码目录结构如下：

    ```
    my-php-project/
    ├── composer.json
    ├── vendor/
    └── index.php
    ```

    `composer.json` 内容如下，相关依赖的版本号请根据实际情况自行决定：

    ```json
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

    `index.php` 内容如下：

    ```php
    <?php

    require __DIR__ . '/vendor/autoload.php';

    use Ratchet\Client\Connector;
    use React\EventLoop\Loop;
    use React\Socket\Connector as SocketConnector;
    use Ratchet\rfc6455\Messaging\Frame;

    # 若没有将API Key配置到环境变量，可将下行替换为：$api_key="REDACTED"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    $api_key = getenv("DASHSCOPE_API_KEY");
    $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/'; // WebSocket服务器地址
    $audio_file_path = 'asr_example.wav'; // 替换为您的音频文件路径

    $loop = Loop::get();

    // 创建自定义的连接器
    $socketConnector = new SocketConnector($loop, [
      'tcp' => [
        'bindto' => '0.0.0.0:0',
      ],
      'tls' => [
        'verify_peer' => false,
        'verify_peer_name' => false,
      ],
    ]);

    $connector = new Connector($loop, $socketConnector);

    $headers = [
      'Authorization' => 'Bearer ' . $api_key
    ];

    $connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $audio_file_path) {
      echo "连接到WebSocket服务器\n";

      // 启动异步接收WebSocket消息的线程
      $conn->on('message', function($msg) use ($conn, $loop, $audio_file_path) {
        $response = json_decode($msg, true);

        if (isset($response['header']['event'])) {
          handleEvent($conn, $response, $loop, $audio_file_path);
        } else {
          echo "未知的消息格式\n";
        }
      });

      // 监听连接关闭
      $conn->on('close', function($code = null, $reason = null) {
        echo "连接已关闭\n";
        if ($code !== null) {
          echo "关闭代码: " . $code . "\n";
        }
        if ($reason !== null) {
          echo "关闭原因：" . $reason . "\n";
        }
      });

      // 生成任务ID
      $taskId = generateTaskId();

      // 发送 run-task 指令
      sendRunTaskMessage($conn, $taskId);

    }, function ($e) {
      echo "无法连接：{$e->getMessage()}\n";
    });

    $loop->run();

    /**
     * 生成任务ID
     * @return string
     */
    function generateTaskId(): string {
      return bin2hex(random_bytes(16));
    }

    /**
     * 发送 run-task 指令
     * @param $conn
     * @param $taskId
     */
    function sendRunTaskMessage($conn, $taskId) {
      $runTaskMessage = json_encode([
        "header" => [
          "action" => "run-task",
          "task_id" => $taskId,
          "streaming" => "duplex"
        ],
        "payload" => [
          "task_group" => "audio",
          "task" => "asr",
          "function" => "recognition",
          "model" => "paraformer-realtime-v2",
          "parameters" => [
            "format" => "wav",
            "sample_rate" => 16000
          ],
          "input" => []
        ]
      ]);
      echo "准备发送run-task指令：" . $runTaskMessage . "\n";
      $conn->send($runTaskMessage);
      echo "run-task指令已发送\n";
    }

    /**
     * 读取音频文件
     * @param string $filePath
     * @return bool|string
     */
    function readAudioFile(string $filePath) {
      $voiceData = file_get_contents($filePath);
      if ($voiceData === false) {
        echo "无法读取音频文件\n";
      }
      return $voiceData;
    }

    /**
     * 分割音频数据
     * @param string $data
     * @param int $chunkSize
     * @return array
     */
    function splitAudioData(string $data, int $chunkSize): array {
      return str_split($data, $chunkSize);
    }

    /**
     * 发送 finish-task 指令
     * @param $conn
     * @param $taskId
     */
    function sendFinishTaskMessage($conn, $taskId) {
      $finishTaskMessage = json_encode([
        "header" => [
          "action" => "finish-task",
          "task_id" => $taskId,
          "streaming" => "duplex"
        ],
        "payload" => [
          "input" => []
        ]
      ]);
      echo "准备发送finish-task指令: " . $finishTaskMessage . "\n";
      $conn->send($finishTaskMessage);
      echo "finish-task指令已发送\n";
    }

    /**
     * 处理事件
     * @param $conn
     * @param $response
     * @param $loop
     * @param $audio_file_path
     */
    function handleEvent($conn, $response, $loop, $audio_file_path) {
      static $taskId;
      static $chunks;
      static $allChunksSent = false;

      if (is_null($taskId)) {
        $taskId = generateTaskId();
      }

      switch ($response['header']['event']) {
        case 'task-started':
          echo "任务开始，发送音频数据...\n";
          // 读取音频文件
          $voiceData = readAudioFile($audio_file_path);
          if ($voiceData === false) {
            echo "无法读取音频文件\n";
            $conn->close();
            return;
          }

          // 分割音频数据
          $chunks = splitAudioData($voiceData, 1024);

          // 定义发送函数
          $sendChunk = function() use ($conn, &$chunks, $loop, &$sendChunk, &$allChunksSent, $taskId) {
            if (!empty($chunks)) {
              $chunk = array_shift($chunks);
              $binaryMsg = new Frame($chunk, true, Frame::OP_BINARY);
              $conn->send($binaryMsg);
              // 100ms后发送下一个片段
              $loop->addTimer(0.1, $sendChunk);
            } else {
              echo "所有数据块已发送\n";
              $allChunksSent = true;

              // 发送 finish-task 指令
              sendFinishTaskMessage($conn, $taskId);
            }
          };

          // 开始发送音频数据
          $sendChunk();
          break;
        case 'result-generated':
          $result = $response['payload']['output']['sentence'];
          echo "识别结果：" . $result['text'] . "\n";
          if (isset($response['payload']['usage']['duration'])) {
            echo "任务计费时长（秒）：" . $response['payload']['usage']['duration'] . "\n";
          }
          break;
        case 'task-finished':
          echo "任务完成\n";
          $conn->close();
          break;
        case 'task-failed':
          echo "任务失败\n";
          echo "错误代码：" . $response['header']['error_code'] . "\n";
          echo "错误信息：" . $response['header']['error_message'] . "\n";
          $conn->close();
          break;
        case 'error':
          echo "错误：" . $response['payload']['message'] . "\n";
          break;
        default:
          echo "未知事件：" . $response['header']['event'] . "\n";
          break;
      }

      // 如果所有数据已发送且任务已完成，关闭连接
      if ($allChunksSent && $response['header']['event'] == 'task-finished') {
        // 等待1秒以确保所有数据都已传输完毕
        $loop->addTimer(1, function() use ($conn) {
          $conn->close();
          echo "客户端关闭连接\n";
        });
      }
    }
    ```
  </Tab>

  <Tab title="Node.js">
    安装依赖：

    ```sh
    npm install ws
    npm install uuid
    ```

    示例代码如下：

    ```js
    import fs from 'fs';
    import WebSocket from 'ws';
    import { v4 as uuidv4 } from 'uuid'; // 用于生成UUID

    // 若没有将API Key配置到环境变量，可将下行替换为：apiKey = 'REDACTED'。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/'; // WebSocket服务器地址
    const audioFile = 'asr_example.wav'; // 替换为您的音频文件路径

    // 生成32位随机ID
    const TASK_ID = uuidv4().replace(/-/g, '').slice(0, 32);

    // 创建WebSocket客户端
    const ws = new WebSocket(url, {
      headers: {
        Authorization: `Bearer ${apiKey}`
      }
    });

    let taskStarted = false; // 标记任务是否已启动

    // 连接打开时发送run-task指令
    ws.on('open', () => {
      console.log('连接到服务器');
      sendRunTask();
    });

    // 接收消息处理
    ws.on('message', (data) => {
      const message = JSON.parse(data);
      switch (message.header.event) {
        case 'task-started':
          console.log('任务开始');
          taskStarted = true;
          sendAudioStream();
          break;
        case 'result-generated':
          console.log('识别结果：', message.payload.output.sentence.text);
          if (message.payload.usage) {
            console.log('任务计费时长（秒）：', message.payload.usage.duration);
          }
          break;
        case 'task-finished':
          console.log('任务完成');
          ws.close();
          break;
        case 'task-failed':
          console.error('任务失败：', message.header.error_message);
          ws.close();
          break;
        default:
          console.log('未知事件：', message.header.event);
      }
    });

    // 如果没有收到task-started事件，关闭连接
    ws.on('close', () => {
      if (!taskStarted) {
        console.error('任务未启动，关闭连接');
      }
    });

    // 发送run-task指令
    function sendRunTask() {
      const runTaskMessage = {
        header: {
          action: 'run-task',
          task_id: TASK_ID,
          streaming: 'duplex'
        },
        payload: {
          task_group: 'audio',
          task: 'asr',
          function: 'recognition',
          model: 'paraformer-realtime-v2',
          parameters: {
            sample_rate: 16000,
            format: 'wav'
          },
          input: {}
        }
      };
      ws.send(JSON.stringify(runTaskMessage));
    }

    // 发送音频流
    function sendAudioStream() {
      const audioStream = fs.createReadStream(audioFile);
      let chunkCount = 0;

      function sendNextChunk() {
        const chunk = audioStream.read();
        if (chunk) {
          ws.send(chunk);
          chunkCount++;
          setTimeout(sendNextChunk, 100); // 每100ms发送一次
        }
      }

      audioStream.on('readable', () => {
        sendNextChunk();
      });

      audioStream.on('end', () => {
        console.log('音频流结束');
        sendFinishTask();
      });

      audioStream.on('error', (err) => {
        console.error('读取音频文件错误：', err);
        ws.close();
      });
    }

    // 发送finish-task指令
    function sendFinishTask() {
      const finishTaskMessage = {
        header: {
          action: 'finish-task',
          task_id: TASK_ID,
          streaming: 'duplex'
        },
        payload: {
          input: {}
        }
      };
      ws.send(JSON.stringify(finishTaskMessage));
    }

    // 错误处理
    ws.on('error', (error) => {
      console.error('WebSocket错误：', error);
    });
    ```
  </Tab>
</Tabs>

## 错误码

如遇报错问题，请参见[错误信息](/api-reference/preparation/error-messages)文档进行排查。

若问题仍未解决，可加入[开发者社区](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈，并提供 Request ID 以便进一步排查。

## 常见问题

### 功能特性

**Q：在长时间静默的情况下，如何保持与服务端长连接？**

将请求参数 `heartbeat` 设置为 `true`，并持续向服务端发送静音音频。

静音音频指在音频文件或数据流中没有声音信号的内容，可通过音频编辑软件（如 Audacity、Adobe Audition）或命令行工具（如 FFmpeg）生成。

**Q：如何将音频格式转换为满足要求的格式？**

可使用 [FFmpeg](https://ffmpeg.en.lo4d.com/download) 工具进行转换，更多用法请参见 FFmpeg 官网。

```bash
# 基础转换命令（万能模板）
# -i，作用：输入文件路径，常用值示例：audio.wav
# -c:a，作用：音频编码器，常用值示例：aac, libmp3lame, pcm_s16le
# -b:a，作用：比特率（音质控制），常用值示例：192k, 320k
# -ar，作用：采样率，常用值示例：44100 (CD), 48000, 16000
# -ac，作用：声道数，常用值示例：1(单声道), 2(立体声)
# -y，作用：覆盖已存在文件(无需值)
ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

# 例如：WAV → MP3（保持原始质量）
ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
# 例如：MP3 → WAV（16bit PCM标准格式）
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
# 例如：M4A → AAC（提取/转换苹果音频）
ffmpeg -i input.m4a -c:a copy output.aac  # 直接提取不重编码
ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac  # 重编码提高质量
# 例如：FLAC无损 → Opus（高压缩）
ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
```

**Q：是否支持查看每句话对应的时间范围？**

支持。语音识别结果中包含每句话的 `begin_time` 和 `end_time`，可通过它们确定每句话的时间范围。

**Q：为什么使用 WebSocket 协议而非 HTTP/HTTPS 协议？**

语音服务选择 WebSocket 而非 HTTP/HTTPS/RESTful，根本在于其依赖全双工通信能力。WebSocket 允许服务端与客户端主动双向传输数据（如实时推送识别进度），而基于 HTTP 的 RESTful 仅支持客户端发起的单向请求-响应模式，无法满足实时交互需求。

**Q：如何识别本地文件（录音文件）？**

将本地文件转成二进制音频流，通过 WebSocket 的二进制通道上传进行识别。代码片段如下：

<Tabs>
  <Tab title="Go">
    ```go
    // 发送音频数据
    func sendAudioData(conn *websocket.Conn) error {
      file, err := os.Open(audioFile)
      if err != nil {
        return err
      }
      defer file.Close()

      buf := make([]byte, 1024) // 假设100ms的音频数据大约为1024字节
      for {
        n, err := file.Read(buf)
        if n == 0 {
          break
        }
        if err != nil && err != io.EOF {
          return err
        }
        err = conn.WriteMessage(websocket.BinaryMessage, buf[:n])
        if err != nil {
          return err
        }
        time.Sleep(100 * time.Millisecond)
      }
      return nil
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    private static async Task SendAudioStreamAsync(string filePath) {
      using (var audioStream = File.OpenRead(filePath)) {
        var buffer = new byte[1024]; // 每次发送100ms的音频数据
        int bytesRead;

        while ((bytesRead = await audioStream.ReadAsync(buffer, 0, buffer.Length)) > 0) {
          var segment = new ArraySegment<byte>(buffer, 0, bytesRead);
          await _webSocket.SendAsync(segment, WebSocketMessageType.Binary, true, _cancellationTokenSource.Token);
          await Task.Delay(100); // 间隔100ms
        }
      }
    }
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    // 读取音频文件
    $voiceData = readAudioFile($audio_file_path);
    if ($voiceData === false) {
      echo "无法读取音频文件\n";
      $conn->close();
      return;
    }

    // 分割音频数据
    $chunks = splitAudioData($voiceData, 1024);

    // 定义发送函数
    $sendChunk = function() use ($conn, &$chunks, $loop, &$sendChunk, &$allChunksSent, $taskId) {
      if (!empty($chunks)) {
        $chunk = array_shift($chunks);
        $binaryMsg = new Frame($chunk, true, Frame::OP_BINARY);
        $conn->send($binaryMsg);
        // 100ms后发送下一个片段
        $loop->addTimer(0.1, $sendChunk);
      } else {
        echo "所有数据块已发送\n";
        $allChunksSent = true;

        // 发送 finish-task 指令
        sendFinishTaskMessage($conn, $taskId);
      }
    };

    // 开始发送音频数据
    $sendChunk();
    ```
  </Tab>

  <Tab title="Node.js">
    ```js
    // 发送音频流
    function sendAudioStream() {
      const audioStream = fs.createReadStream(audioFile);
      let chunkCount = 0;

      function sendNextChunk() {
        const chunk = audioStream.read();
        if (chunk) {
          ws.send(chunk);
          chunkCount++;
          setTimeout(sendNextChunk, 100); // 每100ms发送一次
        }
      }

      audioStream.on('readable', () => {
        sendNextChunk();
      });

      audioStream.on('end', () => {
        console.log('音频流结束');
        sendFinishTask();
      });

      audioStream.on('error', (err) => {
        console.error('读取音频文件错误：', err);
        ws.close();
      });
    }
    ```
  </Tab>
</Tabs>

### 故障排查

如遇代码报错问题，请根据[错误信息](/api-reference/preparation/error-messages)中的信息进行排查。

**Q：无法识别语音（无识别结果）是什么原因？**

1. 请检查请求参数中的音频格式（`format`）和采样率（`sample_rate`）设置是否正确且符合参数约束。常见错误示例：

   - 音频文件扩展名为 .wav，但实际为 MP3 格式，而请求参数 `format` 设置为 `mp3`（参数设置错误）。
   - 音频采样率为 3600Hz，但请求参数 `sample_rate` 设置为 `48000`（参数设置错误）。

   可使用 [ffprobe](https://ffmpeg.org/ffprobe.html) 工具获取音频的容器、编码、采样率、声道等信息：

```sh
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
```

2. 使用 `paraformer-realtime-v2` 模型时，请检查 `language_hints` 设置的语言是否与音频实际语言一致。例如：音频为中文，但 `language_hints` 设置为 `en`（英文）。

3. 若以上检查均无问题，可通过定制热词提升对特定词语的识别效果。
