> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 实时语音识别 WebSocket API

> 实时语音识别 WebSocket API

通过 WebSocket API，您可以使用任意编程语言接入 Fun-ASR 实时语音识别服务。如需更便捷的集成方式，请使用 [Python SDK](/api-reference/speech-recognition/fun-asr-realtime/python-sdk) 或 [Java SDK](/api-reference/speech-recognition/fun-asr-realtime/java-sdk)。

**用户指南**： 模型详情与选型建议请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

## 快速开始

### 示例代码

<Tabs>
  <Tab title="Node.js">
    安装依赖：

    ```sh
    npm install ws
    npm install uuid
    ```

    示例代码：

    ```javascript
    const fs = require('fs');
    const WebSocket = require('ws');
    const { v4: uuidv4 } = require('uuid'); // 用于生成 UUID

    // 若未配置环境变量，请将下行替换为您的 API Key：const apiKey = "sk-xxx"
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/'; // WebSocket 服务地址
    const audioFile = 'asr_example.wav'; // 替换为您的音频文件路径

    // 生成 32 位随机 ID
    const TASK_ID = uuidv4().replace(/-/g, '').slice(0, 32);

    // 创建 WebSocket 客户端
    const ws = new WebSocket(url, {
      headers: {
        Authorization: `Bearer ${apiKey}`
      }
    });

    let taskStarted = false; // 标识任务是否已启动

    // 连接建立后发送 run-task 指令
    ws.on('open', () => {
      console.log('已连接到服务器');
      sendRunTask();
    });

    // 处理接收到的消息
    ws.on('message', (data) => {
      const message = JSON.parse(data);
      switch (message.header.event) {
        case 'task-started':
          console.log('任务已启动');
          taskStarted = true;
          sendAudioStream();
          break;
        case 'result-generated':
          console.log('识别结果:', message.payload.output.sentence.text);
          if (message.payload.usage) {
            console.log('任务计费时长（秒）:', message.payload.usage.duration);
          }
          break;
        case 'task-finished':
          console.log('任务已完成');
          ws.close();
          break;
        case 'task-failed':
          console.error('任务失败:', message.header.error_message);
          ws.close();
          break;
        default:
          console.log('未知事件:', message.header.event);
      }
    });

    // 若未收到 task-started 事件，关闭连接
    ws.on('close', () => {
      if (!taskStarted) {
        console.error('任务未启动，正在关闭连接。');
      }
    });

    // 发送 run-task 指令
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
          model: 'fun-asr-realtime',
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
          setTimeout(sendNextChunk, 100); // 每 100 毫秒发送一个分片
        }
      }

      audioStream.on('readable', () => {
        sendNextChunk();
      });

      audioStream.on('end', () => {
        console.log('音频流发送完毕');
        sendFinishTask();
      });

      audioStream.on('error', (err) => {
        console.error('读取音频文件出错:', err);
        ws.close();
      });
    }

    // 发送 finish-task 指令
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

    // 处理错误
    ws.on('error', (error) => {
      console.error('WebSocket 错误:', error);
    });
    ```
  </Tab>

  <Tab title="C#">
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
      // 若未配置环境变量，请将下行替换为您的 API Key：private static readonly string ApiKey = "sk-xxx"
      private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

      private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/";
      // 替换为您的音频文件路径
      private const string AudioFilePath = "asr_example.wav";

      static async Task Main(string[] args) {
        // 建立 WebSocket 连接并配置认证头
        _webSocket.Options.SetRequestHeader("Authorization", $"Bearer {ApiKey}");

        await _webSocket.ConnectAsync(new Uri(WebSocketUrl), _cancellationTokenSource.Token);

        // 启动线程异步接收 WebSocket 消息
        var receiveTask = ReceiveMessagesAsync();

        // 发送 run-task 指令
        string _taskId = Guid.NewGuid().ToString("N"); // 生成 32 位随机 ID
        var runTaskJson = GenerateRunTaskJson(_taskId);
        await SendAsync(runTaskJson);

        // 等待 task-started 事件
        while (!_taskStartedReceived) {
          await Task.Delay(100, _cancellationTokenSource.Token);
        }

        // 读取本地文件，将音频流发送到服务器进行识别
        await SendAudioStreamAsync(AudioFilePath);

        // 发送 finish-task 指令结束任务
        var finishTaskJson = GenerateFinishTaskJson(_taskId);
        await SendAsync(finishTaskJson);

        // 等待 task-finished 事件
        while (!_taskFinishedReceived && !_cancellationTokenSource.IsCancellationRequested) {
          try {
            await Task.Delay(100, _cancellationTokenSource.Token);
          } catch (OperationCanceledException) {
            // 任务已取消，退出循环
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
                  Console.WriteLine("任务启动成功");
                  _taskStartedReceived = true;
                  break;
                case "result-generated":
                  Console.WriteLine($"识别结果: {message["payload"]?["output"]?["sentence"]?["text"]?.GetValue<string>()}");
                  if (message["payload"]?["usage"] != null && message["payload"]?["usage"]?["duration"] != null) {
                    Console.WriteLine($"任务计费时长（秒）: {message["payload"]?["usage"]?["duration"]?.GetValue<int>()}");
                  }
                  break;
                case "task-finished":
                  Console.WriteLine("任务已完成");
                  _taskFinishedReceived = true;
                  _cancellationTokenSource.Cancel();
                  break;
                case "task-failed":
                  Console.WriteLine($"任务失败: {message["header"]?["error_message"]?.GetValue<string>()}");
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
          var buffer = new byte[1024]; // 每次发送 100 毫秒的音频数据
          int bytesRead;

          while ((bytesRead = await audioStream.ReadAsync(buffer, 0, buffer.Length)) > 0) {
            var segment = new ArraySegment<byte>(buffer, 0, bytesRead);
            await _webSocket.SendAsync(segment, WebSocketMessageType.Binary, true, _cancellationTokenSource.Token);
            await Task.Delay(100); // 间隔 100 毫秒
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
            ["model"] = "fun-asr-realtime",
            ["parameters"] = new JsonObject {
              ["format"] = "wav",
              ["sample_rate"] = 16000,
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
    示例代码使用如下目录结构：

    ```text
    my-php-project/
    ├── composer.json
    ├── vendor/
    └── index.php
    ```

    `composer.json` 内容（依赖版本请按需调整）：

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

    `index.php` 内容：

    ```php
    <?php

    require __DIR__ . '/vendor/autoload.php';

    use Ratchet\Client\Connector;
    use React\EventLoop\Loop;
    use React\Socket\Connector as SocketConnector;
    use Ratchet\rfc6455\Messaging\Frame;

    // 若未配置环境变量，请将下行替换为您的 API Key：$api_key = "sk-xxx"
    $api_key = getenv("DASHSCOPE_API_KEY");
    $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/';
    $audio_file_path = 'asr_example.wav'; // 替换为您的音频文件路径

    $loop = Loop::get();

    // 创建自定义连接器
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
        echo "已连接到 WebSocket 服务器\n";

        // 生成任务 ID
        $taskId = generateTaskId();

        // 启动线程异步接收 WebSocket 消息
        $conn->on('message', function($msg) use ($conn, $loop, $audio_file_path, $taskId) {
            $response = json_decode($msg, true);

            if (isset($response['header']['event'])) {
                handleEvent($conn, $response, $loop, $audio_file_path, $taskId);
            } else {
                echo "未知消息格式\n";
            }
        });

        // 监听连接关闭
        $conn->on('close', function($code = null, $reason = null) {
            echo "连接已关闭\n";
            if ($code !== null) {
                echo "关闭代码: " . $code . "\n";
            }
            if ($reason !== null) {
                echo "关闭原因: " . $reason . "\n";
            }
        });

        // 发送 run-task 指令
        sendRunTaskMessage($conn, $taskId);

    }, function ($e) {
        echo "连接失败: {$e->getMessage()}\n";
    });

    $loop->run();

    /**
     * 生成任务 ID
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
                "model" => "fun-asr-realtime",
                "parameters" => [
                    "format" => "wav",
                    "sample_rate" => 16000
                ],
                "input" => []
            ]
        ]);
        echo "准备发送 run-task 指令: " . $runTaskMessage . "\n";
        $conn->send($runTaskMessage);
        echo "run-task 指令已发送\n";
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
        echo "准备发送 finish-task 指令: " . $finishTaskMessage . "\n";
        $conn->send($finishTaskMessage);
        echo "finish-task 指令已发送\n";
    }

    /**
     * 处理事件
     * @param $conn
     * @param $response
     * @param $loop
     * @param $audio_file_path
     * @param $taskId
     */
    function handleEvent($conn, $response, $loop, $audio_file_path, $taskId) {
        static $chunks;
        static $allChunksSent = false;

        switch ($response['header']['event']) {
            case 'task-started':
                echo "任务已启动，正在发送音频数据...\n";
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
                        // 100 毫秒后发送下一个分片
                        $loop->addTimer(0.1, $sendChunk);
                    } else {
                        echo "所有分片已发送完毕\n";
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
                echo "识别结果: " . $result['text'] . "\n";
                if (isset($response['payload']['usage']['duration'])) {
                    echo "任务计费时长（秒）: " . $response['payload']['usage']['duration'] . "\n";
                }
                break;
            case 'task-finished':
                echo "任务已完成\n";
                $conn->close();
                break;
            case 'task-failed':
                echo "任务失败\n";
                echo "错误代码: " . $response['header']['error_code'] . "\n";
                echo "错误信息: " . $response['header']['error_message'] . "\n";
                $conn->close();
                break;
            case 'error':
                echo "错误: " . $response['payload']['message'] . "\n";
                break;
            default:
                echo "未知事件: " . $response['header']['event'] . "\n";
                break;
        }

        // 如果所有数据已发送且任务已完成，关闭连接
        if ($allChunksSent && $response['header']['event'] == 'task-finished') {
            // 等待 1 秒以确保所有数据传输完成
            $loop->addTimer(1, function() use ($conn) {
                $conn->close();
                echo "客户端关闭连接\n";
            });
        }
    }
    ```
  </Tab>

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
      wsURL     = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/" // WebSocket 服务地址
      audioFile = "asr_example.wav"                                   // 替换为您的音频文件路径
    )

    var dialer = websocket.DefaultDialer

    func main() {
      // 若未配置环境变量，请将下行替换为您的 API Key：apiKey := "sk-xxx"
      apiKey := os.Getenv("DASHSCOPE_API_KEY")

      // 连接 WebSocket 服务
      conn, err := connectWebSocket(apiKey)
      if err != nil {
        log.Fatal("WebSocket 连接失败:", err)
      }
      defer closeConnection(conn)

      // 启动 goroutine 接收结果
      taskStarted := make(chan bool)
      taskDone := make(chan bool)
      startResultReceiver(conn, taskStarted, taskDone)

      // 发送 run-task 指令
      taskID, err := sendRunTaskCmd(conn)
      if err != nil {
        log.Fatal("发送 run-task 指令失败:", err)
      }

      // 等待 task-started 事件
      waitForTaskStarted(taskStarted)

      // 发送音频文件流进行识别
      if err := sendAudioData(conn); err != nil {
        log.Fatal("发送音频失败:", err)
      }

      // 发送 finish-task 指令
      if err := sendFinishTaskCmd(conn, taskID); err != nil {
        log.Fatal("发送 finish-task 指令失败:", err)
      }

      // 等待任务完成或失败
      <-taskDone
    }

    // 定义 JSON 数据结构
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
      Input      Input  `json:"input"`
      Output     Output `json:"output,omitempty"`
      Usage      *struct {
        Duration int `json:"duration"`
      } `json:"usage,omitempty"`
    }

    type Params struct {
      Format                   string `json:"format"`
      SampleRate               int    `json:"sample_rate"`
      VocabularyID             string `json:"vocabulary_id"`
      DisfluencyRemovalEnabled bool   `json:"disfluency_removal_enabled"`
    }

    type Input struct {
    }

    type Event struct {
      Header  Header  `json:"header"`
      Payload Payload `json:"payload"`
    }

    // 连接 WebSocket 服务
    func connectWebSocket(apiKey string) (*websocket.Conn, error) {
      header := make(http.Header)
      header.Add("Authorization", fmt.Sprintf("Bearer %s", apiKey))
      conn, _, err := dialer.Dial(wsURL, header)
      return conn, err
    }

    // 启动 goroutine 异步接收 WebSocket 消息
    func startResultReceiver(conn *websocket.Conn, taskStarted chan<- bool, taskDone chan<- bool) {
      go func() {
        for {
          _, message, err := conn.ReadMessage()
          if err != nil {
            log.Println("解析服务器消息失败:", err)
            return
          }
          var event Event
          err = json.Unmarshal(message, &event)
          if err != nil {
            log.Println("解析事件失败:", err)
            continue
          }
          if handleEvent(conn, event, taskStarted, taskDone) {
            return
          }
        }
      }()
    }

    // 发送 run-task 指令
    func sendRunTaskCmd(conn *websocket.Conn) (string, error) {
      runTaskCmd, taskID, err := generateRunTaskCmd()
      if err != nil {
        return "", err
      }
      err = conn.WriteMessage(websocket.TextMessage, []byte(runTaskCmd))
      return taskID, err
    }

    // 生成 run-task 指令
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
          Model:     "fun-asr-realtime",
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

    // 等待 task-started 事件
    func waitForTaskStarted(taskStarted chan bool) {
      select {
      case <-taskStarted:
        fmt.Println("任务启动成功")
      case <-time.After(10 * time.Second):
        log.Fatal("等待 task-started 超时，任务启动失败。")
      }
    }

    // 发送音频数据
    func sendAudioData(conn *websocket.Conn) error {
      file, err := os.Open(audioFile)
      if err != nil {
        return err
      }
      defer file.Close()

      buf := make([]byte, 1024)
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

    // 发送 finish-task 指令
    func sendFinishTaskCmd(conn *websocket.Conn, taskID string) error {
      finishTaskCmd, err := generateFinishTaskCmd(taskID)
      if err != nil {
        return err
      }
      err = conn.WriteMessage(websocket.TextMessage, []byte(finishTaskCmd))
      return err
    }

    // 生成 finish-task 指令
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
        fmt.Println("收到 task-started 事件")
        taskStarted <- true
      case "result-generated":
        if event.Payload.Output.Sentence.Text != "" {
          fmt.Println("识别结果:", event.Payload.Output.Sentence.Text)
        }
        if event.Payload.Usage != nil {
          fmt.Println("任务计费时长（秒）:", event.Payload.Usage.Duration)
        }
      case "task-finished":
        fmt.Println("任务已完成")
        taskDone <- true
        return true
      case "task-failed":
        handleTaskFailed(event, conn)
        taskDone <- true
        return true
      default:
        log.Printf("未知事件: %v", event)
      }
      return false
    }

    // 处理 task-failed 事件
    func handleTaskFailed(event Event, conn *websocket.Conn) {
      if event.Header.ErrorMessage != "" {
        log.Fatalf("任务失败: %s", event.Header.ErrorMessage)
      } else {
        log.Fatal("任务失败，原因未知")
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
</Tabs>

## 核心概念

### 交互流程

客户端与服务器的交互流程如下：

![交互时序图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6983102771/CAEQUBiBgMCriYSA2RkiIGY1NDE4OTBjOGM3NTRiNjc4MGQ1YzRiMmE3YWQ3ODE44709861_20241015153444.149.svg)

<Steps>
  <Step title="建立连接">
    发送 WebSocket 连接请求，在请求头中携带认证信息。
  </Step>

  <Step title="启动任务">
    发送 [run-task 指令](/api-reference/speech-recognition/fun-asr-realtime/client-events#run-task)，设置模型和音频参数。
  </Step>

  <Step title="确认启动">
    服务器返回 [task-started 事件](/api-reference/speech-recognition/fun-asr-realtime/server-events#task-started)，此时可以开始发送音频。
  </Step>

  <Step title="流式传输音频">
    - 持续发送二进制音频数据。
    - 服务器实时返回 [result-generated 事件](/api-reference/speech-recognition/fun-asr-realtime/server-events#result-generated)，包含中间结果和最终结果。
  </Step>

  <Step title="结束任务">
    音频发送完毕后，发送 [finish-task 指令](/api-reference/speech-recognition/fun-asr-realtime/client-events#finish-task)。
  </Step>

  <Step title="确认完成">
    服务器处理完剩余音频后，返回 [task-finished 事件](/api-reference/speech-recognition/fun-asr-realtime/server-events#task-finished)。
  </Step>

  <Step title="断开连接">
    任意一方关闭 WebSocket 连接。
  </Step>
</Steps>

### 音频要求

- **声道**：仅支持单声道。
- **格式**：支持 pcm、wav、mp3、opus、speex、aac、amr。WAV 文件须为 PCM 编码。Opus 和 Speex 文件须使用 Ogg 容器。amr 格式仅支持 AMR-NB。
- **采样率**：须与 [run-task 指令](/api-reference/speech-recognition/fun-asr-realtime/client-events#run-task)中的 `sample_rate` 一致。

## API 参考

### 连接端点

```http
wss://dashscope.aliyuncs.com/api-ws/v1/inference/
```

### 请求头

| **参数**                     | **类型** | **是否必选** | **说明**                               |
| -------------------------- | ------ | -------- | ------------------------------------ |
| Authorization              | string | 是        | 认证令牌。格式：`Bearer $DASHSCOPE_API_KEY`。 |
| user-agent                 | string | 否        | 客户端标识。用于帮助服务器追踪请求来源。                 |
| X-DashScope-WorkSpace      | string | 否        | 千问AI平台业务空间 ID。                       |
| X-DashScope-DataInspection | string | 否        | 是否开启数据合规检查。默认值：`enable`。仅在必要时关闭。     |

### 事件参考

客户端事件和服务端事件的详细参数说明请参见：

- [客户端事件](/api-reference/speech-recognition/fun-asr-realtime/client-events)（`run-task`、`finish-task`）
- [服务端事件](/api-reference/speech-recognition/fun-asr-realtime/server-events)（`task-started`、`result-generated`、`task-finished`、`task-failed`）

## 连接复用

WebSocket 连接支持跨任务复用。服务器返回 [task-finished 事件](/api-reference/speech-recognition/fun-asr-realtime/server-events#task-finished)后，可在同一连接上发送新的 [run-task 指令](/api-reference/speech-recognition/fun-asr-realtime/client-events#run-task)启动下一个任务。

<Warning>
  1. 复用连接上的每个任务须使用唯一的 `task_id`。
  2. 任务失败时，服务器返回 [task-failed 事件](/api-reference/speech-recognition/fun-asr-realtime/server-events#task-failed)并关闭连接（无法复用）。
  3. 连接空闲超过 60 秒会自动超时断开。
</Warning>
