> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# SSML 与 LaTeX

> 通过 SSML 控制语速、停顿、发音等语音特征，或将 LaTeX 公式转换为自然语音

通过 SSML（Speech Synthesis Markup Language）标记语言，可以精细控制语速、停顿、发音等语音特征；通过 LaTeX 公式朗读功能，可以将数学公式转换为自然语音。这两项功能均适用于 CosyVoice 模型。

## 概述

SSML（Speech Synthesis Markup Language）是一种基于 XML 的语音合成标记语言。在文本中嵌入 SSML 标签后，可以精细控制语速、语调、停顿和音量等语音特征，也可以添加背景音乐和音效，实现更丰富的语音表达效果。

CosyVoice 还支持解析文本中嵌入的 LaTeX 公式，并按照符合中文阅读习惯的方式将其朗读出来，适用于在线教育、有声读物等包含数学公式的场景。例如，输入文本"这是一道一元二次方程的求根公式：`$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$`"时，模型会将公式朗读为"x等于负b加减根号下b的平方减四ac，分之二a"。

典型应用场景包括：

- **有声读物**：灵活控制停顿和语速，搭配背景音乐增强沉浸感
- **智能客服**：通过 `<say-as>` 标签确保电话号码、日期等信息的准确朗读
- **多语种播报**：使用 `<phoneme>` 标签精确指定外文发音
- **在线教育**：通过 LaTeX 公式朗读功能将数学公式转为自然语音

两项功能均适用于 CosyVoice 模型系列。如需了解各模型的选型建议，请参见[语音合成模型](/developer-guides/speech/tts-models)。

## SSML 标记语言

### 使用限制

- **模型**：cosyvoice-v3.5-flash、cosyvoice-v3.5-plus、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2。
- **音色**：克隆音色，以及[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注为支持 SSML 的系统音色。
- **接口**：
  - Java SDK（2.20.3 及以上版本）：支持非流式调用和单向流式调用。
  - Python SDK（1.23.4 及以上版本）：支持非流式调用和单向流式调用。
  - WebSocket API：需将参数 `enable_ssml` 设置为 `true`，且只允许发送一次 continue-task 事件。
  - HTTP API：需将参数 `enable_ssml` 设置为 `true`。

<Note>
  `cosyvoice-v3.5-plus` 和 `cosyvoice-v3.5-flash` 模型专用于声音复刻场景（不提供系统音色）。使用前，请先参见[声音复刻](/developer-guides/speech/voice-cloning)创建目标音色。
</Note>

### 快速开始

以下示例展示如何使用 SSML 控制语速进行语音合成。运行前，请完成以下准备工作：

1. [获取 API Key](/developer-guides/administration/api-keys)
2. 安装 DashScope SDK（Python 1.23.4 及以上版本，Java 2.20.3 及以上版本）。详情请参见[安装 SDK](/api-reference/preparation/install-sdk)。

<Tabs>
  <Tab title="Java SDK">
    <CodeGroup>
      ```java 非流式调用
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
      import com.alibaba.dashscope.utils.Constants;
      import java.io.File;
      import java.io.FileOutputStream;
      import java.io.IOException;
      import java.nio.ByteBuffer;
      /**
       * SSML功能说明：
       *     1. 只有非流式调用和单向流式调用支持SSML功能
       *     2. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
       */
      public class Main {
          private static String model = "cosyvoice-v3-flash";
          private static String voice = "longanyang";
          public static void main(String[] args) {
              Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
              streamAudioDataToSpeaker();
              System.exit(0);
          }
          public static void streamAudioDataToSpeaker() {
              SpeechSynthesisParam param =
                      SpeechSynthesisParam.builder()
                              // 若没有配置环境变量，请用API Key将下行替换为：.apiKey("sk-xxx")
                              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                              .model(model)
                              .voice(voice)
                              .build();
              SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
              ByteBuffer audio = null;
              try {
                  // 非流式调用，阻塞直至音频返回
                  // 特殊字符需要进行转义
                  audio = synthesizer.call("<speak rate=\"2\">我的语速比正常人快。</speak>");
              } catch (Exception e) {
                  throw new RuntimeException(e);
              } finally {
                  // 任务结束关闭websocket连接
                  synthesizer.getDuplexApi().close(1000, "bye");
              }
              if (audio != null) {
                  // 将音频数据保存到本地文件"output.mp3"中
                  File file = new File("output.mp3");
                  try (FileOutputStream fos = new FileOutputStream(file)) {
                      fos.write(audio.array());
                  } catch (IOException e) {
                      throw new RuntimeException(e);
                  }
              }
              // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
              System.out.println(
                      "[Metric] requestId为："
                              + synthesizer.getLastRequestId()
                              + "首包延迟（毫秒）为："
                              + synthesizer.getFirstPackageDelay());
          }
      }
      ```

      ```java 单向流式调用
      import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
      import com.alibaba.dashscope.common.ResultCallback;
      import com.alibaba.dashscope.utils.Constants;
      import java.io.FileOutputStream;
      import java.io.IOException;
      import java.util.concurrent.CountDownLatch;
      /**
       * SSML功能说明：
       *     1. 只有非流式调用和单向流式调用支持SSML功能
       *     2. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
       */
      public class Main {
          private static String model = "cosyvoice-v3-flash";
          private static String voice = "longanyang";
          public static void main(String[] args) {
              Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
              streamAudioDataToSpeaker();
              System.out.println("音频已保存到 output.mp3 文件中");
              System.exit(0);
          }
          public static void streamAudioDataToSpeaker() {
              CountDownLatch latch = new CountDownLatch(1);
              final FileOutputStream[] fileOutputStream = new FileOutputStream[1];
              try {
                  fileOutputStream[0] = new FileOutputStream("output.mp3");
              } catch (IOException e) {
                  System.err.println("无法创建输出文件: " + e.getMessage());
                  return;
              }
              // 实现回调接口ResultCallback
              ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
                  @Override
                  public void onEvent(SpeechSynthesisResult result) {
                      if (result.getAudioFrame() != null) {
                          // 将音频数据写入本地文件
                          try {
                              byte[] audioData = result.getAudioFrame().array();
                              fileOutputStream[0].write(audioData);
                              fileOutputStream[0].flush();
                          } catch (IOException e) {
                              System.err.println("写入音频数据失败: " + e.getMessage());
                          }
                      }
                  }
                  @Override
                  public void onComplete() {
                      System.out.println("收到Complete，语音合成结束");
                      closeFileOutputStream(fileOutputStream[0]);
                      latch.countDown();
                  }
                  @Override
                  public void onError(Exception e) {
                      System.out.println("出现异常：" + e.toString());
                      closeFileOutputStream(fileOutputStream[0]);
                      latch.countDown();
                  }
              };
              SpeechSynthesisParam param =
                      SpeechSynthesisParam.builder()
                              // 若没有配置环境变量，请用API Key将下行替换为：.apiKey("sk-xxx")
                              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                              .model(model)
                              .voice(voice)
                              .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS)
                              .build();
              SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
              try {
                  // 单向流式调用，立即返回null（实际结果通过回调接口异步传递），在回调接口的onEvent方法中实时获取二进制音频
                  // 特殊字符需要进行转义
                  synthesizer.call("<speak rate=\"2\">我的语速比正常人快。</speak>");
                  // 等待合成完成
                  latch.await();
              } catch (Exception e) {
                  throw new RuntimeException(e);
              } finally {
                  // 任务结束后关闭websocket连接
                  try {
                      synthesizer.getDuplexApi().close(1000, "bye");
                  } catch (Exception e) {
                      System.err.println("关闭WebSocket连接失败: " + e.getMessage());
                  }
                  // 确保文件流被关闭
                  closeFileOutputStream(fileOutputStream[0]);
              }
              // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
              System.out.println(
                      "[Metric] requestId为："
                              + synthesizer.getLastRequestId()
                              + "，首包延迟（毫秒）为："
                              + synthesizer.getFirstPackageDelay());
          }
          private static void closeFileOutputStream(FileOutputStream fileOutputStream) {
              try {
                  if (fileOutputStream != null) {
                      fileOutputStream.close();
                  }
              } catch (IOException e) {
                  System.err.println("关闭文件流失败: " + e.getMessage());
              }
          }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Python SDK">
    <CodeGroup>
      ```python 非流式调用
      # coding=utf-8
      # SSML功能说明：
      #     1. 只有非流式调用和单向流式调用支持SSML功能
      #     2. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
      import dashscope
      from dashscope.audio.tts_v2 import *
      import os
      # 若没有配置环境变量，请用API Key将下行替换为：dashscope.api_key = "sk-xxx"
      dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
      dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'
      # 模型
      model = "cosyvoice-v3-flash"
      # 音色
      voice = "longanyang"
      # 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
      synthesizer = SpeechSynthesizer(model=model, voice=voice)
      # 非流式调用，阻塞直至音频返回
      # 特殊字符需要进行转义
      audio = synthesizer.call("<speak rate=\"2\">我的语速比正常人快。</speak>")
      # 将音频保存至本地
      with open('output.mp3', 'wb') as f:
          f.write(audio)
      # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
      print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
          synthesizer.get_last_request_id(),
          synthesizer.get_first_package_delay()))
      ```

      ```python 单向流式调用
      # coding=utf-8
      # SSML功能说明：
      #     1. 只有非流式调用和单向流式调用支持SSML功能
      #     2. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
      import dashscope
      from dashscope.audio.tts_v2 import *
      import os
      from datetime import datetime
      def get_timestamp():
          now = datetime.now()
          formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
          return formatted_timestamp
      # 若没有配置环境变量，请用API Key将下行替换为：dashscope.api_key = "sk-xxx"
      dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
      dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'
      # 模型
      model = "cosyvoice-v3-flash"
      # 音色
      voice = "longanyang"
      # 定义回调接口
      class Callback(ResultCallback):
          _player = None
          _stream = None
          def on_open(self):
              # 打开输出文件，准备写入音频数据
              self.file = open("output.mp3", "wb")
              print("连接建立：" + get_timestamp())
          def on_complete(self):
              print("语音合成完成，所有合成结果已被接收：" + get_timestamp())
              if hasattr(self, 'file') and self.file:
                  self.file.close()
              # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
              print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
                  self.synthesizer.get_last_request_id(),
                  self.synthesizer.get_first_package_delay()))
          def on_error(self, message: str):
              print(f"语音合成出现异常：{message}")
              if hasattr(self, 'file') and self.file:
                  self.file.close()
          def on_close(self):
              print("连接关闭：" + get_timestamp())
              if hasattr(self, 'file') and self.file:
                  self.file.close()
          def on_event(self, message):
              pass
          def on_data(self, data: bytes) -> None:
              print(get_timestamp() + " 二进制音频长度为：" + str(len(data)))
              # 将音频数据写入文件
              self.file.write(data)
      callback = Callback()
      # 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
      synthesizer = SpeechSynthesizer(
          model=model,
          voice=voice,
          callback=callback,
      )
      # 将synthesizer实例赋值给callback，以便在on_complete中使用
      callback.synthesizer = synthesizer
      # 单向流式调用，发送待合成文本，在回调接口的on_data方法中实时获取二进制音频
      # 特殊字符需要进行转义
      synthesizer.call("<speak rate=\"2\">我的语速比正常人快。</speak>")
      ```
    </CodeGroup>
  </Tab>

  <Tab title="WebSocket API">
    <Tabs>
      <Tab title="Go">
        ```go
        // SSML功能说明：
        //     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
        //     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
        //     3. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
        package main
        import (
            "encoding/json"
            "fmt"
            "net/http"
            "os"
            "strings"
            "time"
            "github.com/google/uuid"
            "github.com/gorilla/websocket"
        )
        const (
            wsURL      = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"
            outputFile = "output.mp3"
        )
        func main() {
            // 若没有配置环境变量，请用API Key将下行替换为：apiKey := "sk-xxx"
            apiKey := os.Getenv("DASHSCOPE_API_KEY")
            // 清空输出文件
            os.Remove(outputFile)
            os.Create(outputFile)
            // 连接WebSocket
            header := make(http.Header)
            header.Add("X-DashScope-DataInspection", "enable")
            header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))
            conn, resp, err := websocket.DefaultDialer.Dial(wsURL, header)
            if err != nil {
                if resp != nil {
                    fmt.Printf("连接失败 HTTP状态码: %d\n", resp.StatusCode)
                }
                fmt.Println("连接失败:", err)
                return
            }
            defer conn.Close()
            // 生成任务ID
            taskID := uuid.New().String()
            fmt.Printf("生成任务ID: %s\n", taskID)
            // 发送run-task指令
            runTaskCmd := map[string]interface{}{
                "header": map[string]interface{}{
                    "action":    "run-task",
                    "task_id":   taskID,
                    "streaming": "duplex",
                },
                "payload": map[string]interface{}{
                    "task_group": "audio",
                    "task":       "tts",
                    "function":   "SpeechSynthesizer",
                    "model":      "cosyvoice-v3-flash",
                    "parameters": map[string]interface{}{
                        "text_type":   "PlainText",
                        "voice":       "longanyang",
                        "format":      "mp3",
                        "sample_rate": 22050,
                        "volume":      50,
                        "rate":        1,
                        "pitch":       1,
                        // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                        "enable_ssml": true,
                    },
                    "input": map[string]interface{}{},
                },
            }
            runTaskJSON, _ := json.Marshal(runTaskCmd)
            fmt.Printf("发送run-task指令: %s\n", string(runTaskJSON))
            err = conn.WriteMessage(websocket.TextMessage, runTaskJSON)
            if err != nil {
                fmt.Println("发送run-task失败:", err)
                return
            }
            textSent := false
            // 处理消息
            for {
                messageType, message, err := conn.ReadMessage()
                if err != nil {
                    fmt.Println("读取消息失败:", err)
                    break
                }
                // 处理二进制消息
                if messageType == websocket.BinaryMessage {
                    fmt.Printf("收到二进制消息，长度: %d\n", len(message))
                    file, _ := os.OpenFile(outputFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
                    file.Write(message)
                    file.Close()
                    continue
                }
                // 处理文本消息
                messageStr := string(message)
                fmt.Printf("收到文本消息: %s\n", strings.ReplaceAll(messageStr, "\n", ""))
                // 简单解析JSON获取event类型
                var msgMap map[string]interface{}
                if json.Unmarshal(message, &msgMap) == nil {
                    if header, ok := msgMap["header"].(map[string]interface{}); ok {
                        if event, ok := header["event"].(string); ok {
                            fmt.Printf("事件类型: %s\n", event)
                            switch event {
                            case "task-started":
                                fmt.Println("=== 收到task-started事件 ===")
                                if !textSent {
                                    // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                                    continueTaskCmd := map[string]interface{}{
                                        "header": map[string]interface{}{
                                            "action":    "continue-task",
                                            "task_id":   taskID,
                                            "streaming": "duplex",
                                        },
                                        "payload": map[string]interface{}{
                                            "input": map[string]interface{}{
                                                // 特殊字符需要进行转义
                                                "text": "<speak rate=\"2\">我的语速比正常人快。</speak>",
                                            },
                                        },
                                    }
                                    continueTaskJSON, _ := json.Marshal(continueTaskCmd)
                                    fmt.Printf("发送continue-task指令: %s\n", string(continueTaskJSON))
                                    err = conn.WriteMessage(websocket.TextMessage, continueTaskJSON)
                                    if err != nil {
                                        fmt.Println("发送continue-task失败:", err)
                                        return
                                    }
                                    textSent = true
                                    // 延迟发送finish-task
                                    time.Sleep(500 * time.Millisecond)
                                    // 发送finish-task指令
                                    finishTaskCmd := map[string]interface{}{
                                        "header": map[string]interface{}{
                                            "action":    "finish-task",
                                            "task_id":   taskID,
                                            "streaming": "duplex",
                                        },
                                        "payload": map[string]interface{}{
                                            "input": map[string]interface{}{},
                                        },
                                    }
                                    finishTaskJSON, _ := json.Marshal(finishTaskCmd)
                                    fmt.Printf("发送finish-task指令: %s\n", string(finishTaskJSON))
                                    err = conn.WriteMessage(websocket.TextMessage, finishTaskJSON)
                                    if err != nil {
                                        fmt.Println("发送finish-task失败:", err)
                                        return
                                    }
                                }
                            case "task-finished":
                                fmt.Println("=== 任务完成 ===")
                                return
                            case "task-failed":
                                fmt.Println("=== 任务失败 ===")
                                if header["error_message"] != nil {
                                    fmt.Printf("错误信息: %s\n", header["error_message"])
                                }
                                return
                            case "result-generated":
                                fmt.Println("收到result-generated事件")
                            }
                        }
                    }
                }
            }
        }
        ```
      </Tab>

      <Tab title="C#">
        ```csharp
        using System.Net.WebSockets;
        using System.Text;
        using System.Text.Json;
        // SSML功能说明：
        //     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
        //     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
        //     3. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
        class Program {
            // 若没有配置环境变量，请用API Key将下行替换为：private static readonly string ApiKey = "sk-xxx"
            private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
            private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/";
            // 输出文件路径
            private const string OutputFilePath = "output.mp3";
            // WebSocket客户端
            private static ClientWebSocket _webSocket = new ClientWebSocket();
            // 取消令牌源
            private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
            // 任务ID
            private static string? _taskId;
            // 任务是否已启动
            private static TaskCompletionSource<bool> _taskStartedTcs = new TaskCompletionSource<bool>();
            static async Task Main(string[] args) {
                try {
                    // 清空输出文件
                    ClearOutputFile(OutputFilePath);
                    // 连接WebSocket服务
                    await ConnectToWebSocketAsync(WebSocketUrl);
                    // 启动接收消息的任务
                    Task receiveTask = ReceiveMessagesAsync();
                    // 发送run-task指令
                    _taskId = GenerateTaskId();
                    await SendRunTaskCommandAsync(_taskId);
                    // 等待task-started事件
                    await _taskStartedTcs.Task;
                    // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                    // 特殊字符需要进行转义
                    await SendContinueTaskCommandAsync("<speak rate=\"2\">我的语速比正常人快。</speak>");
                    // 发送finish-task指令
                    await SendFinishTaskCommandAsync(_taskId);
                    // 等待接收任务完成
                    await receiveTask;
                    Console.WriteLine("任务完成，连接已关闭。");
                } catch (OperationCanceledException) {
                    Console.WriteLine("任务被取消。");
                } catch (Exception ex) {
                    Console.WriteLine($"发生错误：{ex.Message}");
                } finally {
                    _cancellationTokenSource.Cancel();
                    _webSocket.Dispose();
                }
            }
            private static void ClearOutputFile(string filePath) {
                if (File.Exists(filePath)) {
                    File.WriteAllText(filePath, string.Empty);
                    Console.WriteLine("输出文件已清空。");
                } else {
                    Console.WriteLine("输出文件不存在，无需清空。");
                }
            }
            private static async Task ConnectToWebSocketAsync(string url) {
                var uri = new Uri(url);
                if (_webSocket.State == WebSocketState.Connecting || _webSocket.State == WebSocketState.Open) {
                    return;
                }
                // 设置WebSocket连接的头部信息
                _webSocket.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
                _webSocket.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");
                try {
                    await _webSocket.ConnectAsync(uri, _cancellationTokenSource.Token);
                    Console.WriteLine("已成功连接到WebSocket服务。");
                } catch (OperationCanceledException) {
                    Console.WriteLine("WebSocket连接被取消。");
                } catch (Exception ex) {
                    Console.WriteLine($"WebSocket连接失败: {ex.Message}");
                    throw;
                }
            }
            private static async Task SendRunTaskCommandAsync(string taskId) {
                var command = CreateCommand("run-task", taskId, "duplex", new {
                    task_group = "audio",
                    task = "tts",
                    function = "SpeechSynthesizer",
                    model = "cosyvoice-v3-flash",
                    parameters = new
                    {
                        text_type = "PlainText",
                        voice = "longanyang",
                        format = "mp3",
                        sample_rate = 22050,
                        volume = 50,
                        rate = 1,
                        pitch = 1,
                        // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                        enable_ssml = true
                    },
                    input = new { }
                });
                await SendJsonMessageAsync(command);
                Console.WriteLine("已发送run-task指令。");
            }
            private static async Task SendContinueTaskCommandAsync(string text) {
                if (_taskId == null) {
                    throw new InvalidOperationException("任务ID未初始化。");
                }
                var command = CreateCommand("continue-task", _taskId, "duplex", new {
                    input = new {
                        text
                    }
                });
                await SendJsonMessageAsync(command);
                Console.WriteLine("已发送continue-task指令。");
            }
            private static async Task SendFinishTaskCommandAsync(string taskId) {
                var command = CreateCommand("finish-task", taskId, "duplex", new {
                    input = new { }
                });
                await SendJsonMessageAsync(command);
                Console.WriteLine("已发送finish-task指令。");
            }
            private static async Task SendJsonMessageAsync(string message) {
                var buffer = Encoding.UTF8.GetBytes(message);
                try {
                    await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
                } catch (OperationCanceledException) {
                    Console.WriteLine("消息发送被取消。");
                }
            }
            private static async Task ReceiveMessagesAsync() {
                while (_webSocket.State == WebSocketState.Open) {
                    var response = await ReceiveMessageAsync();
                    if (response != null) {
                        var eventStr = response.RootElement.GetProperty("header").GetProperty("event").GetString();
                        switch (eventStr) {
                            case "task-started":
                                Console.WriteLine("任务已启动。");
                                _taskStartedTcs.TrySetResult(true);
                                break;
                            case "task-finished":
                                Console.WriteLine("任务已完成。");
                                _cancellationTokenSource.Cancel();
                                break;
                            case "task-failed":
                                Console.WriteLine("任务失败：" + response.RootElement.GetProperty("header").GetProperty("error_message").GetString());
                                _cancellationTokenSource.Cancel();
                                break;
                            default:
                                // result-generated可在此处理
                                break;
                        }
                    }
                }
            }
            private static async Task<JsonDocument?> ReceiveMessageAsync() {
                var buffer = new byte[1024 * 4];
                var segment = new ArraySegment<byte>(buffer);
                try {
                    WebSocketReceiveResult result = await _webSocket.ReceiveAsync(segment, _cancellationTokenSource.Token);
                    if (result.MessageType == WebSocketMessageType.Close) {
                        await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cancellationTokenSource.Token);
                        return null;
                    }
                    if (result.MessageType == WebSocketMessageType.Binary) {
                        // 处理二进制数据
                        Console.WriteLine("接收到二进制数据...");
                        // 将二进制数据保存到文件
                        using (var fileStream = new FileStream(OutputFilePath, FileMode.Append)) {
                            fileStream.Write(buffer, 0, result.Count);
                        }
                        return null;
                    }
                    string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    return JsonDocument.Parse(message);
                } catch (OperationCanceledException) {
                    Console.WriteLine("消息接收被取消。");
                    return null;
                }
            }
            private static string GenerateTaskId() {
                return Guid.NewGuid().ToString("N").Substring(0, 32);
            }
            private static string CreateCommand(string action, string taskId, string streaming, object payload) {
                var command = new {
                    header = new {
                        action,
                        task_id = taskId,
                        streaming
                    },
                    payload
                };
                return JsonSerializer.Serialize(command);
            }
        }
        ```
      </Tab>

      <Tab title="PHP">
        示例代码目录结构为：

        my-php-project/

        ├── composer.json

        ├── vendor/

        └── index.php

        composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

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

        index.php内容如下：

        ```php
        <!-- SSML功能说明： -->
        <!--     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持 -->
        <!--     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令 -->
        <!--     3. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色） -->
        <?php
        require __DIR__ . '/vendor/autoload.php';
        use Ratchet\Client\Connector;
        use React\EventLoop\Loop;
        use React\Socket\Connector as SocketConnector;
        // 若没有配置环境变量，请用API Key将下行替换为：$api_key = "sk-xxx"
        $api_key = getenv("DASHSCOPE_API_KEY");
        $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/'; // WebSocket服务器地址
        $output_file = 'output.mp3'; // 输出文件路径
        $loop = Loop::get();
        if (file_exists($output_file)) {
            // 清空文件内容
            file_put_contents($output_file, '');
        }
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
            'Authorization' => 'bearer ' . $api_key,
            'X-DashScope-DataInspection' => 'enable'
        ];
        $connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $output_file) {
            echo "连接到WebSocket服务器\n";
            // 生成任务ID
            $taskId = generateTaskId();
            // 发送 run-task 指令
            sendRunTaskMessage($conn, $taskId);
            // 定义发送 continue-task 指令的函数
            $sendContinueTask = function() use ($conn, $loop, $taskId) {
                // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                $continueTaskMessage = json_encode([
                    "header" => [
                        "action" => "continue-task",
                        "task_id" => $taskId,
                        "streaming" => "duplex"
                    ],
                    "payload" => [
                        "input" => [
                            // 特殊字符需要进行转义
                            "text" => "<speak rate=\"2\">我的语速比正常人快。</speak>"
                        ]
                    ]
                ]);
                $conn->send($continueTaskMessage);
                // 发送 finish-task 指令
                sendFinishTaskMessage($conn, $taskId);
            };
            // 标记是否收到 task-started 事件
            $taskStarted = false;
            // 监听消息
            $conn->on('message', function($msg) use ($conn, $sendContinueTask, $loop, &$taskStarted, $taskId, $output_file) {
                if ($msg->isBinary()) {
                    // 写入二进制数据到本地文件
                    file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
                } else {
                    // 处理非二进制消息
                    $response = json_decode($msg, true);
                    if (isset($response['header']['event'])) {
                        handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, $taskStarted);
                    } else {
                        echo "未知的消息格式\n";
                    }
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
                    "task" => "tts",
                    "function" => "SpeechSynthesizer",
                    "model" => "cosyvoice-v3-flash",
                    "parameters" => [
                        "text_type" => "PlainText",
                        "voice" => "longanyang",
                        "format" => "mp3",
                        "sample_rate" => 22050,
                        "volume" => 50,
                        "rate" => 1,
                        "pitch" => 1,
                        // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                        "enable_ssml" => true
                    ],
                    "input" => (object) []
                ]
            ]);
            echo "准备发送run-task指令: " . $runTaskMessage . "\n";
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
                    "input" => (object) []
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
         * @param $sendContinueTask
         * @param $loop
         * @param $taskId
         * @param $taskStarted
         */
        function handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, &$taskStarted) {
            switch ($response['header']['event']) {
                case 'task-started':
                    echo "任务开始，发送continue-task指令...\n";
                    $taskStarted = true;
                    // 发送 continue-task 指令
                    $sendContinueTask();
                    break;
                case 'result-generated':
                    // 忽略result-generated事件
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
            // 如果任务已完成，关闭连接
            if ($response['header']['event'] == 'task-finished') {
                // 等待1秒以确保所有数据都已传输完毕
                $loop->addTimer(1, function() use ($conn) {
                    $conn->close();
                    echo "客户端关闭连接\n";
                });
            }
            // 如果没有收到 task-started 事件，关闭连接
            if (!$taskStarted && in_array($response['header']['event'], ['task-failed', 'error'])) {
                $conn->close();
            }
        }
        ```
      </Tab>

      <Tab title="Node.js">
        需安装相关依赖：

        ```bash
        npm install ws
        npm install uuid
        ```

        示例代码如下：

        ```javascript
        // SSML功能说明：
        //     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
        //     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
        //     3. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
        import fs from 'fs';
        import WebSocket from 'ws';
        import { v4 as uuid } from 'uuid'; // 用于生成UUID
        // 若没有配置环境变量，请用API Key将下行替换为：const apiKey = "sk-xxx"
        const apiKey = process.env.DASHSCOPE_API_KEY;
        const url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/';
        // 输出文件路径
        const outputFilePath = 'output.mp3';
        // 清空输出文件
        fs.writeFileSync(outputFilePath, '');
        // 创建WebSocket客户端
        const ws = new WebSocket(url, {
          headers: {
            Authorization: `bearer ${apiKey}`,
            'X-DashScope-DataInspection': 'enable'
          }
        });
        let taskStarted = false;
        let taskId = uuid();
        ws.on('open', () => {
          console.log('已连接到WebSocket服务器');
          // 发送run-task指令
          const runTaskMessage = JSON.stringify({
            header: {
              action: 'run-task',
              task_id: taskId,
              streaming: 'duplex'
            },
            payload: {
              task_group: 'audio',
              task: 'tts',
              function: 'SpeechSynthesizer',
              model: 'cosyvoice-v3-flash',
              parameters: {
                text_type: 'PlainText',
                voice: 'longanyang', // 音色
                format: 'mp3', // 音频格式
                sample_rate: 22050, // 采样率
                volume: 50, // 音量
                rate: 1, // 语速
                pitch: 1, // 音调
                enable_ssml: true // 是否开启SSML功能。如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
              },
              input: {}
            }
          });
          ws.send(runTaskMessage);
          console.log('已发送run-task消息');
        });
        const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
        ws.on('message', (data, isBinary) => {
          if (isBinary) {
            // 写入二进制数据到文件
            fileStream.write(data);
          } else {
            const message = JSON.parse(data);
            switch (message.header.event) {
              case 'task-started':
                taskStarted = true;
                console.log('任务已开始');
                // 发送continue-task指令
                sendContinueTasks(ws);
                break;
              case 'task-finished':
                console.log('任务已完成');
                ws.close();
                fileStream.end(() => {
                  console.log('文件流已关闭');
                });
                break;
              case 'task-failed':
                console.error('任务失败：', message.header.error_message);
                ws.close();
                fileStream.end(() => {
                  console.log('文件流已关闭');
                });
                break;
              default:
                // 可以在这里处理result-generated
                break;
            }
          }
        });
        function sendContinueTasks(ws) {
          if (taskStarted) {
            // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
            const continueTaskMessage = JSON.stringify({
              header: {
                action: 'continue-task',
                task_id: taskId,
                streaming: 'duplex'
              },
              payload: {
                input: {
                  // 特殊字符需要进行转义
                  text: '<speak rate="2">我的语速比正常人快。</speak>'
                }
              }
            });
            ws.send(continueTaskMessage);
            // 发送finish-task指令
            const finishTaskMessage = JSON.stringify({
              header: {
                action: 'finish-task',
                task_id: taskId,
                streaming: 'duplex'
              },
              payload: {
                input: {}
              }
            });
            ws.send(finishTaskMessage);
          }
        }
        ws.on('close', () => {
          console.log('已断开与WebSocket服务器的连接');
        });
        ```
      </Tab>

      <Tab title="Java">
        如您使用Java编程语言，建议采用Java DashScope SDK进行开发，详情请参见[Java SDK](/api-reference/speech-synthesis/cosyvoice/java-sdk)。

        以下是Java WebSocket的调用示例。在运行示例前，请确保已导入以下依赖：

        - `Java-WebSocket`
        - `jackson-databind`

        推荐您使用Maven或Gradle管理依赖包，其配置如下：

        <CodeGroup>
          ```xml pom.xml
          <dependencies>
              <!-- WebSocket Client -->
              <dependency>
                  <groupId>org.java-websocket</groupId>
                  <artifactId>Java-WebSocket</artifactId>
                  <version>1.5.3</version>
              </dependency>
              <!-- JSON Processing -->
              <dependency>
                  <groupId>com.fasterxml.jackson.core</groupId>
                  <artifactId>jackson-databind</artifactId>
                  <version>2.13.0</version>
              </dependency>
          </dependencies>
          ```

          ```gradle build.gradle
          // 省略其它代码
          dependencies {
            // WebSocket Client
            implementation 'org.java-websocket:Java-WebSocket:1.5.3'
            // JSON Processing
            implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.0'
          }
          // 省略其它代码
          ```
        </CodeGroup>

        Java代码如下：

        ```java
        import com.fasterxml.jackson.databind.ObjectMapper;
        import org.java_websocket.client.WebSocketClient;
        import org.java_websocket.handshake.ServerHandshake;
        import java.io.FileOutputStream;
        import java.io.IOException;
        import java.net.URI;
        import java.nio.ByteBuffer;
        import java.util.*;
        /**
         * SSML功能说明：
         *     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
         *     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
         *     3. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
         */
        public class TTSWebSocketClient extends WebSocketClient {
            private final String taskId = UUID.randomUUID().toString();
            private final String outputFile = "output_" + System.currentTimeMillis() + ".mp3";
            private boolean taskFinished = false;
            public TTSWebSocketClient(URI serverUri, Map<String, String> headers) {
                super(serverUri, headers);
            }
            @Override
            public void onOpen(ServerHandshake serverHandshake) {
                System.out.println("连接成功");
                // 发送run-task指令
                // 如果enable_ssml设为true，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                String runTaskCommand = "{ \"header\": { \"action\": \"run-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"task_group\": \"audio\", \"task\": \"tts\", \"function\": \"SpeechSynthesizer\", \"model\": \"cosyvoice-v3-flash\", \"parameters\": { \"text_type\": \"PlainText\", \"voice\": \"longanyang\", \"format\": \"mp3\", \"sample_rate\": 22050, \"volume\": 50, \"rate\": 1, \"pitch\": 1, \"enable_ssml\": true }, \"input\": {} }}";
                send(runTaskCommand);
            }
            @Override
            public void onMessage(String message) {
                System.out.println("收到服务端返回的消息：" + message);
                try {
                    // Parse JSON message
                    Map<String, Object> messageMap = new ObjectMapper().readValue(message, Map.class);
                    if (messageMap.containsKey("header")) {
                        Map<String, Object> header = (Map<String, Object>) messageMap.get("header");
                        if (header.containsKey("event")) {
                            String event = (String) header.get("event");
                            if ("task-started".equals(event)) {
                                System.out.println("收到服务端返回的task-started事件");
                                // 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                                // 特殊字符需要进行转义
                                sendContinueTask("<speak rate=\\\"2\\\">我的语速比正常人快。</speak>");
                                // 发送finish-task指令
                                sendFinishTask();
                            } else if ("task-finished".equals(event)) {
                                System.out.println("收到服务端返回的task-finished事件");
                                taskFinished = true;
                                closeConnection();
                            } else if ("task-failed".equals(event)) {
                                System.out.println("任务失败：" + message);
                                closeConnection();
                            }
                        }
                    }
                } catch (Exception e) {
                    System.err.println("出现异常：" + e.getMessage());
                }
            }
            @Override
            public void onMessage(ByteBuffer message) {
                System.out.println("收到的二进制音频数据大小为：" + message.remaining());
                try (FileOutputStream fos = new FileOutputStream(outputFile, true)) {
                    byte[] buffer = new byte[message.remaining()];
                    message.get(buffer);
                    fos.write(buffer);
                    System.out.println("音频数据已写入本地文件" + outputFile + "中");
                } catch (IOException e) {
                    System.err.println("音频数据写入本地文件失败：" + e.getMessage());
                }
            }
            @Override
            public void onClose(int code, String reason, boolean remote) {
                System.out.println("连接关闭：" + reason + " (" + code + ")");
            }
            @Override
            public void onError(Exception ex) {
                System.err.println("报错：" + ex.getMessage());
                ex.printStackTrace();
            }
            private void sendContinueTask(String text) {
                String command = "{ \"header\": { \"action\": \"continue-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": { \"text\": \"" + text + "\" } }}";
                send(command);
            }
            private void sendFinishTask() {
                String command = "{ \"header\": { \"action\": \"finish-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": {} }}";
                send(command);
            }
            private void closeConnection() {
                if (!isClosed()) {
                    close();
                }
            }
            public static void main(String[] args) {
                try {
                    // 若没有配置环境变量，请用API Key将下行替换为：String apiKey = "sk-xxx"
                    String apiKey = System.getenv("DASHSCOPE_API_KEY");
                    if (apiKey == null || apiKey.isEmpty()) {
                        System.err.println("请设置 DASHSCOPE_API_KEY 环境变量");
                        return;
                    }
                    Map<String, String> headers = new HashMap<>();
                    headers.put("Authorization", "bearer " + apiKey);
                    TTSWebSocketClient client = new TTSWebSocketClient(new URI("wss://dashscope.aliyuncs.com/api-ws/v1/inference/"), headers);
                    client.connect();
                    while (!client.isClosed() && !client.taskFinished) {
                        Thread.sleep(1000);
                    }
                } catch (Exception e) {
                    System.err.println("连接WebSocket服务失败：" + e.getMessage());
                    e.printStackTrace();
                }
            }
        }
        ```
      </Tab>

      <Tab title="Python">
        如您使用Python编程语言，建议采用Python DashScope SDK进行开发，详情请参见[Python SDK](/api-reference/speech-synthesis/cosyvoice/python-sdk)。

        以下是Python WebSocket的调用示例。在运行示例前，请确保通过如下方式导入依赖：

        ```bash
        pip uninstall websocket-client
        pip uninstall websocket
        pip install websocket-client
        ```

        <Warning>
          请不要将运行示例代码的Python文件命名为"websocket.py"，否则会报错（AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?）。
        </Warning>

        ```python
        # SSML功能说明：
        #     1. 在发送run-task指令时，将参数enable_ssml设置为true，以开启SSML支持
        #     2. 通过continue-task指令发送包含SSML的文本，且只允许发送一次continue-task指令
        #     3. 只有cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色以及音色列表中标记为支持SSML的系统音色支持SSML功能（例如cosyvoice-v3-flash模型的longanyang音色）
        import websocket
        import json
        import uuid
        import os
        import time
        class TTSClient:
            def __init__(self, api_key, uri):
                """
            初始化 TTSClient 实例
            参数:
                api_key (str): 鉴权用的 API Key
                uri (str): WebSocket 服务地址
            """
                self.api_key = api_key  # 替换为你的 API Key
                self.uri = uri  # 替换为你的 WebSocket 地址
                self.task_id = str(uuid.uuid4())  # 生成唯一任务 ID
                self.output_file = f"output_{int(time.time())}.mp3"  # 输出音频文件路径
                self.ws = None  # WebSocketApp 实例
                self.task_started = False  # 是否收到 task-started
                self.task_finished = False  # 是否收到 task-finished / task-failed
            def on_open(self, ws):
                """
            WebSocket 连接建立时回调函数
            发送 run-task 指令开启语音合成任务
            """
                print("WebSocket 已连接")
                # 构造 run-task 指令
                run_task_cmd = {
                    "header": {
                        "action": "run-task",
                        "task_id": self.task_id,
                        "streaming": "duplex"
                    },
                    "payload": {
                        "task_group": "audio",
                        "task": "tts",
                        "function": "SpeechSynthesizer",
                        "model": "cosyvoice-v3-flash",
                        "parameters": {
                            "text_type": "PlainText",
                            "voice": "longanyang",
                            "format": "mp3",
                            "sample_rate": 22050,
                            "volume": 50,
                            "rate": 1,
                            "pitch": 1,
                            # 如果enable_ssml设为True，只允许发送一次continue-task指令，否则会报错“Text request limit violated, expected 1.”
                            "enable_ssml": True
                        },
                        "input": {}
                    }
                }
                # 发送 run-task 指令
                ws.send(json.dumps(run_task_cmd))
                print("已发送 run-task 指令")
            def on_message(self, ws, message):
                """
            接收到消息时的回调函数
            区分文本和二进制消息处理
            """
                if isinstance(message, str):
                    # 处理 JSON 文本消息
                    try:
                        msg_json = json.loads(message)
                        print(f"收到 JSON 消息: {msg_json}")
                        if "header" in msg_json:
                            header = msg_json["header"]
                            if "event" in header:
                                event = header["event"]
                                if event == "task-started":
                                    print("任务已启动")
                                    self.task_started = True
                                    # 发送 continue-task 指令，使用SSML功能时，该指令只允许发送一次
                                    # 特殊字符需要进行转义
                                    self.send_continue_task("<speak rate=\"2\">我的语速比正常人快。</speak>")
                                    # continue-task 发送完成后发送 finish-task
                                    self.send_finish_task()
                                elif event == "task-finished":
                                    print("任务已完成")
                                    self.task_finished = True
                                    self.close(ws)
                                elif event == "task-failed":
                                    error_msg = msg_json.get("error_message", "未知错误")
                                    print(f"任务失败: {error_msg}")
                                    self.task_finished = True
                                    self.close(ws)
                    except json.JSONDecodeError as e:
                        print(f"JSON 解析失败: {e}")
                else:
                    # 处理二进制消息（音频数据）
                    print(f"收到二进制消息，大小: {len(message)} 字节")
                    with open(self.output_file, "ab") as f:
                        f.write(message)
                    print(f"已将音频数据写入本地文件{self.output_file}中")
            def on_error(self, ws, error):
                """发生错误时的回调"""
                print(f"WebSocket 出错: {error}")
            def on_close(self, ws, close_status_code, close_msg):
                """连接关闭时的回调"""
                print(f"WebSocket 已关闭: {close_msg} ({close_status_code})")
            def send_continue_task(self, text):
                """发送 continue-task 指令，附带要合成的文本内容"""
                cmd = {
                    "header": {
                        "action": "continue-task",
                        "task_id": self.task_id,
                        "streaming": "duplex"
                    },
                    "payload": {
                        "input": {
                            "text": text
                        }
                    }
                }
                self.ws.send(json.dumps(cmd))
                print(f"已发送 continue-task 指令，文本内容: {text}")
            def send_finish_task(self):
                """发送 finish-task 指令，结束语音合成任务"""
                cmd = {
                    "header": {
                        "action": "finish-task",
                        "task_id": self.task_id,
                        "streaming": "duplex"
                    },
                    "payload": {
                        "input": {}
                    }
                }
                self.ws.send(json.dumps(cmd))
                print("已发送 finish-task 指令")
            def close(self, ws):
                """主动关闭连接"""
                if ws and ws.sock and ws.sock.connected:
                    ws.close()
                    print("已主动关闭连接")
            def run(self):
                """启动 WebSocket 客户端"""
                # 设置请求头部（鉴权）
                header = {
                    "Authorization": f"bearer {self.api_key}",
                    "X-DashScope-DataInspection": "enable"
                }
                # 创建 WebSocketApp 实例
                self.ws = websocket.WebSocketApp(
                    self.uri,
                    header=header,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )
                print("正在监听 WebSocket 消息...")
                self.ws.run_forever()  # 启动长连接监听
        # 示例使用方式
        if __name__ == "__main__":
            # 若没有配置环境变量，请用API Key将下行替换为：API_KEY = "sk-xxx"
            API_KEY = os.environ.get("DASHSCOPE_API_KEY")
            SERVER_URI = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"
            client = TTSClient(API_KEY, SERVER_URI)
            client.run()
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="cURL">
    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --header 'X-DashScope-DataInspection: enable' \
    --data '{
        "model": "cosyvoice-v3-flash",
        "input": {
            "text": "<speak rate=\"2\">我的语速比正常人快。</speak>"
        },
        "parameters": {
            "voice": "longanyang",
            "format": "mp3"
        }
    }'
    ```
  </Tab>
</Tabs>

### 标签参考

<Note>
  CosyVoice SSML 基于 [W3C SSML 1.0](https://www.w3.org/TR/speech-synthesis/)，仅支持部分标签。

  **语法规则**：

  - 所有 SSML 内容必须包裹在 `<speak></speak>` 标签中。
  - 可以连续使用多个 `<speak>` 标签，但不能嵌套。
  - 需要转义 XML 特殊字符：`"` → `"`，`'` → `&apos;`，`&` → `&`，`<` → `<`，`>` → `>`。
</Note>

#### `<speak>`：根标签

**说明**

所有 SSML 内容必须包裹在 `<speak></speak>` 标签中。

**语法**

```xml
<speak>需要使用 SSML 功能的文本</speak>
```

**属性**

| 属性                    | 类型     | 必填 | 说明                                                                                                                                                                                                                                                                        |
| --------------------- | ------ | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| voice                 | String | 否  | 音色名称。覆盖 API 参数 `voice`。参见[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。                                                                                                                                                                                    |
| rate                  | String | 否  | 语速。覆盖 API 参数 `speech_rate`。推荐范围：0.5 \~ 2，默认值 1。大于 1 加速，小于 1 减速。                                                                                                                                                                                                           |
| pitch                 | String | 否  | 音调。覆盖 API 参数 `pitch_rate`。推荐范围：0.5 \~ 2，默认值 1。大于 1 升高，小于 1 降低。                                                                                                                                                                                                            |
| volume                | String | 否  | 音量。覆盖 API 参数 `volume`。取值范围：0 \~ 100，默认值 50。                                                                                                                                                                                                                               |
| effect                | String | 否  | 音效。可选值：`robot`、`lolita`（活泼女声）、`lowpass`、`echo`、`eq`（均衡器，高级）、`lpfilter`（低通滤波器，高级）、`hpfilter`（高通滤波器，高级）。`eq`、`lpfilter`、`hpfilter` 需配合 `effectValue` 使用。每个标签只能设置一种音效。音效会增加延迟。                                                                                               |
| effectValue           | String | 否  | 自定义 `effect` 参数。`eq`：8 个以空格分隔的整数（-20 \~ 20），分别对应 `["40 Hz", "100 Hz", "200 Hz", "400 Hz", "800 Hz", "1600 Hz", "4000 Hz", "12000 Hz"]` 频段的增益，示例：`"1 1 1 1 1 1 1 1"`。`lpfilter`：整数频率，范围 (0, sample\_rate/2]，示例：`"800"`。`hpfilter`：整数频率，范围 (0, sample\_rate/2]，示例：`"1200"`。 |
| bgm                   | String | 否  | 背景音乐 URL。文件需存放在 OSS 上，权限至少为公共读。URL 中的 XML 特殊字符需转义。要求：16 kHz 采样率、单声道、WAV 格式、16-bit。如果合成音频长于背景音乐，音乐将循环播放。                                                                                                                                                                   |
| backgroundMusicVolume | String | 否  | 背景音乐音量。                                                                                                                                                                                                                                                                   |

**示例**

音色：

```xml
<speak voice="longcheng_v2">
  我是男声。
</speak>
```

语速：

```xml
<speak rate="2">
  我的语速比正常人快。
</speak>
```

音调：

```xml
<speak pitch="0.5">
  但是我的音调比别人低。
</speak>
```

音量：

```xml
<speak volume="80">
  我的音量也很高。
</speak>
```

音效：

```xml
<speak effect="robot">
  你喜欢机器人瓦力吗？
</speak>
```

音效 + effectValue：

```xml
<speak effect="eq" effectValue="1 -20 1 1 1 1 20 1">
  你喜欢机器人瓦力吗？
</speak>

<speak effect="lpfilter" effectValue="1200">
  你喜欢机器人瓦力吗？
</speak>

<speak effect="hpfilter" effectValue="1200">
  你喜欢机器人瓦力吗？
</speak>
```

如果音频不是 WAV 格式，可使用 `ffmpeg` 转换：

```bash
ffmpeg -i input_audio -acodec pcm_s16le -ac 1 -ar 16000 output.wav
```

背景音乐（bgm）：

```xml
<speak bgm="http://nls.alicdn.com/bgm/2.wav" backgroundMusicVolume="30" rate="-500" volume="40">
  <break time="2s"/>
  阴崖老木苍苍烟
  <break time="700ms"/>
  雨声犹在竹林间
  <break time="700ms"/>
  绵蕝固知裨国计
  <break time="700ms"/>
  绵州风物总堪怜
  <break time="2s"/>
</speak>
```

<Warning>
  上传音频的版权由您自行承担法律责任。
</Warning>

组合属性（空格分隔）：

```xml
<speak rate="200" pitch="-100" volume="80">
  所以放在一起，我的声音是这样的。
</speak>
```

#### `<break>`：停顿

**说明**

插入一段停顿。时长单位为秒（s）或毫秒（ms）。

**语法**

```xml
# 无属性
<break/>
# 带 time 属性
<break time="string"/>
```

<Note>
  **break 标签行为**：

  - 不带属性时，`<break/>` 默认停顿 1 秒。
  - **注意**：连续的 `<break>` 标签时长会累加，但总时长上限为 10 秒。

  例如，以下三个标签总时长为 15 秒，但仅前 10 秒有效：

  ```xml
  <speak>
    请闭上眼睛休息一下。<break time="5s"/><break time="5s"/><break time="5s"/>好了，请睁开眼睛。
  </speak>
  ```
</Note>

**属性**

| 属性   | 类型     | 必填 | 说明                                                       |
| ---- | ------ | -- | -------------------------------------------------------- |
| time | String | 否  | 停顿时长，如 `"2s"` 或 `"50ms"`。秒为单位：1 \~ 10。毫秒为单位：50 \~ 10000。 |

**示例**

```xml
<speak>
  请闭上眼睛休息一下。<break time="500ms"/>好了，请睁开眼睛。
</speak>
```

#### `<sub>`：替换文本

**说明**

将显示文本替换为其他发音。

**语法**

```xml
<sub alias="string"></sub>
```

**属性**

| 属性    | 类型     | 必填 | 说明       |
| ----- | ------ | -- | -------- |
| alias | String | 是  | 替代朗读的文本。 |

**示例**

```xml
<speak>
   <sub alias="network protocol">W3C</sub>
 </speak>
```

#### `<phoneme>`：设置发音

**说明**

使用拼音（中文）或 CMU 音标（英文）指定发音。

**语法**

```xml
<phoneme alphabet="string" ph="string">text</phoneme>
```

**属性**

| 属性       | 类型     | 必填 | 说明                                                                                                              |
| -------- | ------ | -- | --------------------------------------------------------------------------------------------------------------- |
| alphabet | String | 是  | 发音类型：`"py"`（拼音）或 `"cmu"`（音标）。参见 [The CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)。 |
| ph       | String | 是  | 拼音或音标符号。每个汉字的拼音之间用空格分隔，音节数必须与字数一致。每个音节带声调号（1 \~ 5，其中 5 为轻声）。                                                    |

**示例**

```xml
<speak>
  去<phoneme alphabet="py" ph="dian3 dang4 hang2">典当行</phoneme>把这个玩意<phoneme alphabet="py" ph="dang4 diao4">当掉</phoneme>
</speak>

<speak>
  How to spell <phoneme alphabet="cmu" ph="S AY N">sin</phoneme>?
</speak>
```

#### `<soundEvent>`：插入音效

**说明**

在合成语音中插入外部音频文件（提示音、环境音等）。

**语法**

```xml
<soundEvent src="URL"/>
```

**属性**

| 属性  | 类型     | 必填 | 说明                                                                                       |
| --- | ------ | -- | ---------------------------------------------------------------------------------------- |
| src | String | 是  | 音频 URL。文件需存放在 OSS 上，权限至少为公共读。URL 中的 XML 特殊字符需转义。要求：16 kHz 采样率、单声道、WAV 格式、16-bit，最大 2 MB。 |

如果音频不是 WAV 格式，可使用 `ffmpeg` 转换：

```bash
ffmpeg -i input_audio -acodec pcm_s16le -ac 1 -ar 16000 output.wav
```

<Warning>
  上传音频的版权由您自行承担法律责任。
</Warning>

**示例**

```xml
<speak>
  一匹马受了惊吓<soundEvent src="http://nls.alicdn.com/sound-event/horse-neigh.wav"/>人们四散躲避
</speak>
```

#### `<say-as>`：设置朗读格式

**说明**

指定文本的朗读方式（如数字、日期、电话号码等）。

**语法**

```xml
<say-as interpret-as="string">text</say-as>
```

**属性**

| 属性           | 类型     | 必填 | 说明                                                                                                                                                                                       |
| ------------ | ------ | -- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| interpret-as | String | 是  | 文本类型。可选值：`cardinal`（数字）、`digits`（逐位数字）、`telephone`（电话号码）、`name`（姓名）、`address`（地址）、`id`（账号名/昵称）、`characters`（逐字符）、`punctuation`（标点）、`date`（日期）、`time`（时间）、`currency`（货币）、`measure`（度量单位）。 |

##### cardinal

`cardinal` 支持的格式：

| 格式                      | 示例        | 英文读法                                           | 说明                                                                      |
| ----------------------- | --------- | ---------------------------------------------- | ----------------------------------------------------------------------- |
| 纯数字                     | 145       | one hundred forty five                         | 整数范围：最多 13 位，\[-999999999999, 999999999999]。小数：整数部分最多 13 位，小数部分最多 10 位。 |
| 零开头的数字                  | 0145      | one hundred forty five                         |                                                                         |
| 负号 + 数字                 | -145      | minus hundred forty five                       |                                                                         |
| 千分位逗号分隔的数字              | 60,000    | sixty thousand                                 |                                                                         |
| 负号 + 千分位逗号分隔的数字         | -208,000  | minus two hundred eight thousand               |                                                                         |
| 数字 + 小数点 + 零            | 12.00     | twelve                                         |                                                                         |
| 数字 + 小数点 + 数字           | 12.34     | twelve point three four                        |                                                                         |
| 千分位逗号分隔 + 小数点 + 数字      | 1,000.1   | one thousand point one                         |                                                                         |
| 负号 + 数字 + 小数点 + 数字      | -12.34    | minus twelve point three four                  |                                                                         |
| 负号 + 千分位逗号分隔 + 小数点 + 数字 | -1,000.1  | minus one thousand point one                   |                                                                         |
| 千分位数字 + 连字符 + 千分位数字     | 1-1,000   | one to one thousand                            |                                                                         |
| 其他默认读法                  | 012.34    | twelve point three four                        |                                                                         |
|                         | 1/2       | one half                                       |                                                                         |
|                         | -3/4      | minus three quarters                           |                                                                         |
|                         | 5.1/6     | five point one over six                        |                                                                         |
|                         | -3 1/2    | minus three and a half                         |                                                                         |
|                         | 1,000.3^3 | one thousand point three to the power of three |                                                                         |
|                         | 3e9.1     | three times ten to the power of nine point one |                                                                         |
|                         | 23.10%    | twenty three point one percent                 |                                                                         |

**示例**

```xml
<speak>
  <say-as interpret-as="cardinal">12345</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="cardinal">10234</say-as>
</speak>
```

##### digits

`digits` 支持的格式：

| 格式                     | 示例            | 英文读法                                                 | 说明                    |
| ---------------------- | ------------- | ---------------------------------------------------- | --------------------- |
| 纯数字                    | 12034         | one two zero three four                              | 无严格长度限制，建议不超过 20 个字符。 |
| 数字 + 空格或连字符 + 数字 + ... | 1-23-456 7890 | one, two three, four five six, seven eight nine zero |                       |

**示例**

```xml
<speak>
  <say-as interpret-as="digits">12345</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="digits">10234</say-as>
</speak>
```

##### telephone

`telephone` 支持的格式：

| 格式                                     | 示例            | 英文读法                                               | 说明                    |
| -------------------------------------- | ------------- | -------------------------------------------------- | --------------------- |
| 纯数字                                    | 12034         | one two oh three four                              | 无严格长度限制，建议不超过 20 个字符。 |
| 数字 + 空格或连字符 + 数字 + ...                 | 1-23-456 7890 | one, two three, four five six, seven eight nine oh |                       |
| 加号 + 数字 + 空格或连字符 + 数字                  | +43-211-0567  | plus four three, two one one, oh five six seven    |                       |
| 左括号 + 数字 + 右括号 + 空格 + 数字 + 空格或连字符 + 数字 | (21) 654-3210 | (two one) six five four, three two one oh          |                       |

**示例**

```xml
<speak>
  <say-as interpret-as="telephone">12345</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="telephone">10234</say-as>
</speak>
```

##### name

**示例**

```xml
<speak>
  Her former name is <say-as interpret-as="name">Zeng Xiaofan</say-as>
</speak>
```

##### address

<Note>
  英文文本不支持该格式。
</Note>

**示例**

```xml
<speak>
  <say-as interpret-as="address">Fulu International, Building 1, Unit 3, Room 304</say-as>
</speak>
```

##### id

<Note>
  英文文本的效果与 `characters` 相同。
</Note>

**示例**

```xml
<speak>
  <say-as interpret-as="id">myid_1998</say-as>
</speak>
```

##### characters

`characters` 支持的格式：

| 格式  | 示例             | 英文读法                                                                 | 说明                        |
| --- | -------------- | -------------------------------------------------------------------- | ------------------------- |
| 字符串 | \*b+3\$.c-0'=α | asterisk B plus three dollar dot C dash zero apostrophe equals alpha | 支持中文汉字、英文字母、数字 0-9 及常用符号。 |

**示例**

```xml
<speak>
  <say-as interpret-as="characters">Greek letters αβ</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="characters">*b+3.c$=α</say-as>
</speak>
```

##### punctuation

<Note>
  英文文本的效果与 `characters` 相同。
</Note>

**示例**

```xml
<speak>
  <say-as interpret-as="punctuation"> -./:;</say-as>
</speak>
```

##### date

`date` 支持的格式：

| 格式                                                    | 示例                 | 英文读法                                                  | 说明                                          |
| ----------------------------------------------------- | ------------------ | ----------------------------------------------------- | ------------------------------------------- |
| 四位数/两位数 或 四位数-两位数                                     | 2000/01            | two thousand, oh one                                  | 年份跨度。                                       |
|                                                       | 1900-01            | nineteen hundred, oh one                              |                                             |
|                                                       | 2001-02            | twenty oh one, oh two                                 |                                             |
|                                                       | 2019-20            | twenty nineteen, twenty                               |                                             |
|                                                       | 1998-99            | nineteen ninety eight, ninety nine                    |                                             |
|                                                       | 1999-00            | nineteen ninety nine, oh oh                           |                                             |
| 以 1 或 2 开头的四位数                                        | 2000               | two thousand                                          | 四位数年份。                                      |
|                                                       | 1900               | nineteen hundred                                      |                                             |
|                                                       | 1905               | nineteen oh five                                      |                                             |
|                                                       | 2021               | twenty twenty one                                     |                                             |
| 星期-星期 或 星期\~星期 或 星期&星期                                | mon-wed            | monday to wednesday                                   | 范围分隔符中的 XML 特殊字符需转义。                        |
|                                                       | tue\~fri           | tuesday to friday                                     |                                             |
|                                                       | sat\&sun           | saturday and sunday                                   |                                             |
| DD-DD MMM, YYYY 或 DD\~DD MMM, YYYY 或 DD\&DD MMM, YYYY | 19-20 Jan, 2000    | the nineteen to the twentieth of january two thousand | DD = 两位数日期。MMM = 月份缩写或全称。YYYY = 四位数年份。      |
|                                                       | 01 \~ 10 Jul, 2020 | the first to the tenth of july twenty twenty          |                                             |
|                                                       | 05&06 Apr, 2009    | the fifth and the sixth of april two thousand nine    |                                             |
| MMM DD-DD 或 MMM DD\~DD 或 MMM DD\&DD                   | Feb 01 - 03        | february the first to the third                       | MMM = 月份。DD = 日期。                           |
|                                                       | Aug 10-20          | august the tenth to the twentieth                     |                                             |
|                                                       | Dec 11&12          | december the eleventh and the twelfth                 |                                             |
| MMM-MMM 或 MMM\~MMM 或 MMM\&MMM                         | Jan-Jun            | january to june                                       | MMM = 月份。                                   |
|                                                       | Jul - Dec          | july to december                                      |                                             |
|                                                       | sep\&oct           | september and october                                 |                                             |
| YYYY-YYYY 或 YYYY\~YYYY                                | 1990 - 2000        | nineteen ninety to two thousand                       | YYYY = 以 1 或 2 开头的四位数年份。                    |
|                                                       | 2001-2021          | two thousand one to twenty twenty one                 |                                             |
| WWW DD MMM YYYY                                       | Sun 20 Nov 2011    | sunday the twentieth of november twenty eleven        | WWW = 星期（缩写或全称）。DD = 日期。MMM = 月份。YYYY = 年份。 |
| WWW DD MMM                                            | Sun 20 Nov         | sunday the twentieth of november                      |                                             |
| WWW MMM DD YYYY                                       | Sun Nov 20 2011    | sunday november the twentieth twenty eleven           |                                             |
| WWW MMM DD                                            | Sun Nov 20         | sunday november the twentieth                         |                                             |
| WWW YYYY-MM-DD                                        | Sat 2010-10-01     | saturday october the first twenty ten                 |                                             |
| WWW YYYY/MM/DD                                        | Sat 2010/10/01     | saturday october the first twenty ten                 |                                             |
| WWW MM/DD/YYYY                                        | Sun 11/20/2011     | sunday november the twentieth twenty eleven           |                                             |
| MM/DD/YYYY                                            | 11/20/2011         | november the twentieth twenty eleven                  |                                             |
| YYYY                                                  | 1998               | nineteen ninety eight                                 |                                             |
| 其他默认读法                                                | 10 Mar, 2001       | the tenth of march two thousand one                   |                                             |
|                                                       | 10 Mar             | the tenth of march                                    |                                             |
|                                                       | Mar 2001           | march two thousand one                                |                                             |
|                                                       | Fri. 10/Mar/2001   | friday the tenth of march two thousand one            |                                             |
|                                                       | Mar 10th, 2001     | march the tenth two thousand one                      |                                             |
|                                                       | Mar 10             | march the tenth                                       |                                             |
|                                                       | 2001/03/10         | march the tenth two thousand one                      |                                             |
|                                                       | 2001-03-10         | march the tenth two thousand one                      |                                             |
|                                                       | 2000s              | two thousands                                         |                                             |
|                                                       | 2010's             | twenty tens                                           |                                             |
|                                                       | 1900's             | nineteen hundreds                                     |                                             |
|                                                       | 1990s              | nineteen nineties                                     |                                             |

**示例**

```xml
<speak>
  <say-as interpret-as="date">1000-10-10</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="date">10-01-2020</say-as>
</speak>
```

##### time

`time` 支持的格式：

| 格式            | 示例                 | 英文读法                             | 说明                                         |
| ------------- | ------------------ | -------------------------------- | ------------------------------------------ |
| HH:MM AM 或 PM | 09:00 AM           | nine A M                         | HH = 小时（1-2 位）。MM = 分钟（2 位）。AM/PM = 上午或下午。 |
|               | 09:03 PM           | nine oh three P M                |                                            |
|               | 09:13 p.m.         | nine thirteen p m                |                                            |
| HH:MM         | 21:00              | twenty one hundred               |                                            |
| HHMM          | 100                | one oclock                       |                                            |
| 时间点-时间点       | 8:00 am - 05:30 pm | eight a m to five p m            | 时间范围格式。                                    |
|               | 7:05\~10:15 AM     | seven oh five to ten fifteen A M |                                            |
|               | 09:00-13:00        | nine oclock to thirteen hundred  |                                            |

**示例**

```xml
<speak>
  <say-as interpret-as="time">5:00am</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="time">0500</say-as>
</speak>
```

##### currency

`currency` 支持的格式：

| 格式                                | 示例           | 英文读法                                  | 说明                                                            |
| --------------------------------- | ------------ | ------------------------------------- | ------------------------------------------------------------- |
| 数字 + 货币标识符                        | 1.00 RMB     | one yuan                              | 支持整数、小数和千分位逗号分隔。                                              |
|                                   | 2.02 CNY     | two point zero two yuan               |                                                               |
|                                   | 1,000.23 CN¥ | one thousand point two three yuan     |                                                               |
|                                   | 1.01 SGD     | one singapore dollar and one cent     |                                                               |
|                                   | 2.01 CAD     | two canadian dollars and one cent     |                                                               |
|                                   | 3.1 HKD      | three hong kong dollars and ten cents |                                                               |
|                                   | 1,000.00 EUR | one thousand euros                    |                                                               |
| 货币标识符 + 数字                        | US\$ 1.00    | one US dollar                         | 支持整数、小数和千分位逗号分隔。                                              |
|                                   | \$0.01       | one cent                              |                                                               |
|                                   | JPY 1.01     | one japanese yen and one sen          |                                                               |
|                                   | £1.1         | one pound and ten pence               |                                                               |
|                                   | €2.01        | two euros and one cent                |                                                               |
|                                   | USD 1,000    | one thousand united states dollars    |                                                               |
| 数字 + 量词 + 货币标识符 或 货币标识符 + 数字 + 量词 | 1.23 Tn RMB  | one point two three trillion yuan     | 量词：thousand、million、billion、trillion、Mil、mil、K、k、Bn、bn、Tn、tn。 |
|                                   | \$1.2 K      | one point two thousand dollars        |                                                               |

**示例**

```xml
<speak>
  <say-as interpret-as="currency">13,000,000.00RMB</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="currency">$1,000.01</say-as>
</speak>
```

##### measure

`measure` 支持的格式：

| 格式        | 示例          | 英文读法                                                           | 说明                        |
| --------- | ----------- | -------------------------------------------------------------- | ------------------------- |
| 数字 + 度量单位 | 1.0 kg      | one kilogram                                                   | 支持整数、小数和千分位逗号分隔。支持常用单位缩写。 |
|           | 1,234.01 km | one thousand two hundred thirty-four point zero one kilometers |                           |
| 纯度量单位     | mm2         | square millimeter                                              |                           |

**示例**

```xml
<speak>
  <say-as interpret-as="measure">100m12cm6mm</say-as>
</speak>
```

```xml
<speak>
  <say-as interpret-as="measure">1,000.01kg</say-as>
</speak>
```

##### 符号发音

`<say-as>` 常用符号发音：

| 符号   | 英文读法              |
| ---- | ----------------- |
| !    | exclamation mark  |
| "    | double quote      |
| #    | pound             |
| \$   | dollar            |
| %    | percent           |
| &    | and               |
| '    | left quote        |
| (    | left parenthesis  |
| )    | right parenthesis |
| \*   | asterisk          |
| +    | plus              |
| ,    | comma             |
| -    | dash              |
| .    | dot               |
| /    | slash             |
| :    | colon             |
| ;    | semicolon         |
| \<   | less than         |
| =    | equals            |
| >    | greater than      |
| ?    | question mark     |
| @    | at                |
| \[   | left bracket      |
| \\   | backslash         |
| ]    | right bracket     |
| ^    | caret             |
| \_   | underscore        |
| \`   | backtick          |
| `\{` | left brace        |
| \    |                   | vertical bar |
| `\}` | right brace       |
| \~   | tilde             |

全角及特殊符号：

| 符号     | 英文读法                     |
| ------ | ------------------------ |
| ！      | exclamation mark         |
| \u201c | left double quote        |
| \u201d | right double quote       |
| \u2018 | left quote               |
| \u2019 | right quote              |
| （      | left parenthesis         |
| ）      | right parenthesis        |
| ，      | comma                    |
| 。      | full stop                |
| —      | em dash                  |
| ：      | colon                    |
| ；      | semicolon                |
| ？      | question mark            |
| 、      | enumeration comma        |
| …      | ellipsis                 |
| ……     | ellipsis                 |
| 《      | left guillemet           |
| 》      | right guillemet          |
| ￥      | yuan                     |
| ≥      | greater than or equal to |
| ≤      | less than or equal to    |
| ≠      | not equal                |
| ≈      | approximately equal      |
| ±      | plus or minus            |
| ×      | times                    |
| π      | pi                       |

希腊字母（大写）：

| 符号 | 英文读法    |
| -- | ------- |
| Α  | alpha   |
| Β  | beta    |
| Γ  | gamma   |
| Δ  | delta   |
| Ε  | epsilon |
| Ζ  | zeta    |
| Θ  | theta   |
| Ι  | iota    |
| Κ  | kappa   |
| ∧  | lambda  |
| Μ  | mu      |
| Ν  | nu      |
| Ξ  | ksi     |
| Ο  | omicron |
| ∏  | pi      |
| Ρ  | rho     |
| ∑  | sigma   |
| Τ  | tau     |
| Υ  | upsilon |
| Φ  | phi     |
| Χ  | chi     |
| Ψ  | psi     |
| Ω  | omega   |

希腊字母（小写）：

| 符号 | 英文读法    |
| -- | ------- |
| α  | alpha   |
| β  | beta    |
| γ  | gamma   |
| δ  | delta   |
| ε  | epsilon |
| ζ  | zeta    |
| η  | eta     |
| θ  | theta   |
| ι  | iota    |
| κ  | kappa   |
| λ  | lambda  |
| μ  | mu      |
| ν  | nu      |
| ξ  | ksi     |
| ο  | omicron |
| π  | pi      |
| ρ  | rho     |
| σ  | sigma   |
| τ  | tau     |
| υ  | upsilon |
| φ  | phi     |
| χ  | chi     |
| ψ  | psi     |
| ω  | omega   |

##### 常用度量单位

`<say-as>` 常用度量单位：

| 类别 | 单位                                                                    |
| -- | --------------------------------------------------------------------- |
| 长度 | nm（纳米）、μm（微米）、mm（毫米）、cm（厘米）、m（米）、km（千米）、ft（英尺）、in（英寸）                 |
| 面积 | cm²（平方厘米）、m²（平方米）、km²（平方千米）、SqFt（平方英尺）                                |
| 体积 | cm³（立方厘米）、m³（立方米）、km3（立方千米）、mL（毫升）、L（升）、gal（加仑）                       |
| 重量 | μg（微克）、mg（毫克）、g（克）、kg（千克）                                             |
| 时间 | min（分钟）、sec（秒）、ms（毫秒）                                                 |
| 电磁 | μA（微安）、mA（毫安）、Hz（赫兹）、kHz（千赫兹）、MHz（兆赫兹）、GHz（吉赫兹）、V（伏特）、kV（千伏）、kWh（千瓦时） |
| 声音 | dB（分贝）                                                                |
| 气压 | Pa（帕斯卡）、kPa（千帕）、MPa（兆帕）                                               |
| 其他 | 还支持 tsp（茶匙）、rpm（转/分）、KB（千字节）、mmHg（毫米汞柱）等单位。                           |

## LaTeX 公式转语音

CosyVoice 可以将文本中的数学公式转换为自然语音，适用于有声书、在线教育等数理类音频内容场景。

<Warning>
  该功能仅支持**中文**，其他语言可能无法正确朗读公式。
</Warning>

### 使用限制

- **仅支持中文**：不支持其他语言
- **内容限制**：
  - 仅支持[支持的标签和符号](#支持的标签和符号)中列出的标签和符号
  - 不支持 Markdown 数学代码块（` ```math ... ``` `）
  - 分隔符内只能包含公式，混入其他内容可能导致合成结果不准确
- **兼容模型**：cosyvoice-v3.5-flash、cosyvoice-v3.5-plus、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2

### 使用方法

用指定的分隔符包裹文本中的公式，然后调用语音合成 API。

<Steps>
  <Step title="用分隔符标记公式">
    用以下任意分隔符包裹公式（效果相同）：

    - `$...$`
    - `$$...$$`
    - `\(...\)`
    - `\[...\]`

    示例：

    ```plaintext
    这是一元二次方程的求根公式：$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$，请仔细计算。
    ```
  </Step>

  <Step title="调用 API 合成语音">
    调用语音合成 API，传入标记好公式的文本。在 JSON 或字符串中，反斜杠（`\`）是转义字符，需要写成 `\\`。

    Python 调用示例：

    ```python
    # coding=utf-8

    import os
    import dashscope
    from dashscope.audio.tts_v2 import *

    # 如果未配置环境变量，请将下面一行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

    dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

    model = "cosyvoice-v3-flash"
    voice = "longanyang"

    synthesizer = SpeechSynthesizer(model=model, voice=voice)
    audio = synthesizer.call("这是一元二次方程的求根公式：$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$，请仔细计算。")

    print('[Metric] requestId: {}, first-package delay: {} ms'.format(
      synthesizer.get_last_request_id(),
      synthesizer.get_first_package_delay()))

    with open('output.mp3', 'wb') as f:
      f.write(audio)
    ```
  </Step>
</Steps>

### 支持的标签和符号

以下是当前支持的标签和符号列表。

#### 基础运算

| 标签或符号     | 功能   | 公式内容示例            | 公式输入示例              | 朗读效果      |
| --------- | ---- | ----------------- | ------------------- | --------- |
| +         | 加法   | 2 + 3 = 5         | `$2 + 3 = 5$`       | 二加三等于五    |
| -         | 减法   | 3 - 2 = 1         | `$3 - 2 = 1$`       | 三减二等于一    |
| \pm       | 正负号  | \pm 1 \pm 2       | `$\pm 1\pm 2$`      | 正负一、正负二   |
| \times    | 乘法   | 2 \times 3 = 6    | `$2 \times 3 = 6$`  | 二乘三等于六    |
| ×         | 乘法   | 2 × 3 = 6         | `$$2 × 3 = 6$$`     | 二乘三等于六    |
| \*        | 乘法   | 2 \* 3 = 6        | `\(2 * 3 = 6\)`     | 二乘三等于六    |
| \div      | 除法   | 6\div2=3          | `\[6\div2=3\]`      | 六除以二等于三   |
| ÷         | 除法   | 6÷2=3             | `$6÷2=3$`           | 六除以二等于三   |
| /         | 除法   | 6/2=3             | `$6/2=3$`           | 六除以二等于三   |
| =         | 等于   | 3+5=8             | `$3+5=8$`           | 三加五等于八    |
| \<        | 小于   | 1\< 2             | `$1< 2$`            | 一小于二      |
| ≤         | 小于等于 | 3≤5               | `$3≤5$`             | 三小于等于五    |
| \<=       | 小于等于 | 3\<=5             | `$3<=5$`            | 三小于等于五    |
| \leq      | 小于等于 | 3\leq5            | `$3\leq 5$`         | 三小于等于五    |
| \le       | 小于等于 | 3\le5             | `$3\le 5$`          | 三小于等于五    |
| \leqq     | 小于等于 | 3\leqq5           | `$3\leqq 5$`        | 三小于等于五    |
| \leqslant | 小于等于 | 3\leqslant5       | `$3\leqslant 5$`    | 三小于等于五    |
| >         | 大于   | 2>1               | `$2>1$`             | 二大于一      |
| ≥         | 大于等于 | 5≥3               | `$5≥3$`             | 五大于等于三    |
| >=        | 大于等于 | 5>=3              | `$5>=3$`            | 五大于等于三    |
| \geq      | 大于等于 | 5\geq3            | `$5\geq 3$`         | 五大于等于三    |
| \ge       | 大于等于 | 5\ge3             | `$5\ge 3$`          | 五大于等于三    |
| \geqq     | 大于等于 | 5\geqq3           | `$5\geqq 3$`        | 五大于等于三    |
| \geqslant | 大于等于 | 5\geqslant3       | `$5\geqslant 3$`    | 五大于等于三    |
| \frac     | 分数   | `2\frac3`         | `$\frac {2}{3}$`    | 三分之二      |
| ^         | 幂    | `2^1`             | `$2^{1}$`           | 二的一次方     |
| \sqrt     | 开方   | `\sqrt{9} = 3`    | `$\sqrt {9} = 3$`   | 根号九等于三    |
| \sqrt     | 开方   | `\sqrt[3]{8} = 2` | `$\sqrt[3]{8} = 2$` | 八的三次方根等于二 |
| %         | 百分号  | `5\%`             | `$5\%$`             | 百分之五      |
| \         |      | 绝对值               | `∣3∣=3`             | `$\       | 3\ | =3$` | 三的绝对值等于三 |
| \vert     | 绝对值  | `3\vert=3`        | `$\vert 3\vert =3$` | 三的绝对值等于三  |
| \lg       | 对数   | `lg {10}`         | `$\lg {10}$`        | lg 十      |
| \log      | 对数   | `\log{5}`         | `$\log{5}$`         | log 五     |
| \ln       | 自然对数 | `\lnX`            | `$ln {10}$`         | ln 十      |
| !         | 阶乘   | 5!                | `$5!$`              | 五的阶乘      |
| ()        | 括号   | (2+1)             | `$(2+1)$`           | 括号二加一     |
| `\{ \}`   | 花括号  | `\{2+1\}`         | `$\{2+1\}$`         | 花括号二加一    |

#### 特殊数学符号

| 标签或符号  | 转换结果  | 公式内容示例 | 公式输入示例     | 朗读效果 |
| ------ | ----- | ------ | ---------- | ---- |
| \alpha | alpha | \alpha | `$\alpha$` | 阿尔法  |
| \Alpha | alpha | \Alpha | `$\Alpha$` | 阿尔法  |
| \beta  | beta  | \beta  | `$\beta$`  | 贝塔   |
| \Beta  | beta  | \Beta  | `$\Beta$`  | 贝塔   |
| \gamma | gamma | \gamma | `$\gamma$` | 伽马   |
| \Gamma | gamma | \Gamma | `$\Gamma$` | 伽马   |
| \delta | delta | \delta | `$\delta$` | 德尔塔  |
| \Delta | delta | \Delta | `$\Delta$` | 德尔塔  |
| \infty | 无穷大   | \infty | `$\infty$` | 无穷大  |
| ∞      | 无穷大   | ∞      | `$∞$`      | 无穷大  |

#### 几何

| 标签或符号            | 功能    | 公式内容示例                                              | 公式输入示例                                                  | 朗读效果                |
| ---------------- | ----- | --------------------------------------------------- | ------------------------------------------------------- | ------------------- |
| \pi              | 圆周率   | \pi=3.14159                                         | `$\pi =3.14159$`                                        | 派等于 3.14159         |
| \sin             | 三角函数  | `\sin 30^\circ=\frac{1}{2}`                         | `$\sin 30^\circ =\frac {1}{2}$`                         | 正弦三十度等于二分之一         |
| \cos             | 三角函数  | `\cos 30^\circ=\frac{\sqrt{2}}{2}`                  | `$\cos 30^\circ =\frac {\sqrt {2}}{2}$`                 | 余弦三十度等于二分之根号二       |
| \tan             | 三角函数  | `\tan 30^\circ=\frac{\sin 30^\circ}{\cos 30^\circ}` | `$\tan 30^\circ =\frac {\sin 30^\circ}{\cos 30^\circ}$` | 正切三十度等于正弦三十度除以余弦三十度 |
| \csc             | 三角函数  | \csc A                                              | `$\csc A$`                                              | 余割 A                |
| \sec             | 三角函数  | \sec A                                              | `$\sec A$`                                              | 正割 A                |
| \cot             | 三角函数  | \cot A                                              | `$\cot A$`                                              | 余切 A                |
| \angle           | 角     | \angle AB                                           | `$\angle AB$`                                           | 角 AB                |
| ∠                | 角     | ∠AB                                                 | `$∠AB$`                                                 | 角 AB                |
| ^\circ           | 度     | ∠AB = 30^\circ                                      | `$∠AB = 30^\circ$`                                      | 角 AB 等于三十度          |
| \odot            | 圆     | \odot                                               | `$\odot$`                                               | 圆                   |
| `\overset\frown` | 弧     | `\overset\frown {BC}`                               | `$\overset\frown {BC}$`                                 | 弧 BC                |
| `\rm{Rt}`        | 直角    | `\because \rm{Rt}\triangle ABC`                     | `$\because \rm{Rt}\triangle ABC$`                       | 因为三角形 ABC 是直角三角形    |
| `\mathrm{Rt}`    | 直角    | `\therefore AB \perp BC`                            | `$\therefore AB \perp BC$`                              | 所以 AB 垂直于 BC        |
| \triangle        | 三角形   | \triangle ABC                                       | `$\triangle ABC$`                                       | 三角形 ABC             |
| △                | 三角形   | △ABC                                                | `$△ABC$`                                                | 三角形 ABC             |
| \parallelogram   | 平行四边形 | \parallelogram ABCD                                 | `$\parallelogram ABCD$`                                 | 平行四边形 ABCD          |
| \perp            | 垂直    | AB \perp BC                                         | `$AB \perp BC$`                                         | AB 垂直于 BC           |
| \bot             | 垂直    | AB \bot BC                                          | `$AB \bot BC$`                                          | AB 垂直于 BC           |
| ⊥                | 垂直    | AB ⊥ BC                                             | `$AB ⊥ BC$`                                             | AB 垂直于 BC           |
| \parallel        | 平行    | A\parallel B                                        | `$A\parallel B$`                                        | A 平行于 B             |
| \equalparallel   | 平行且等于 | A\equalparallel B                                   | `$A\equalparallel B$`                                   | A 平行且等于 B           |
| \cong            | 全等    | △ABC\cong△DEF                                       | `$△ABC\cong△DEF$`                                       | 三角形 ABC 全等于三角形 DEF  |

#### 条件关系

| 标签或符号      | 功能  | 公式内容示例                        | 公式输入示例                            | 朗读效果                |
| ---------- | --- | ----------------------------- | --------------------------------- | ------------------- |
| \implies   | 推出  | \implies 1+1=2                | `$\implies 1+1=2$`                | 可推出一加一等于二           |
| \iff       | 等价于 | p\iffq                        | `$p\iffq$`                        | p 等价于 q             |
| \because   | 因为  | \because a = b \therefore b=a | `$\because a = b \therefore b=a$` | 因为 a 等于 b，所以 b 等于 a |
| \therefore | 所以  | \because a = b \therefore b=a | `$\because a = b \therefore b=a$` | 因为 a 等于 b，所以 b 等于 a |

#### 单位

单位必须用 `\unit`、`\quantity`、`\mathit`、`\mathrm` 或 `\rm` 标签包裹（例如 `\unit{cm}`）。

| 标签或符号 | 朗读效果  | 公式内容示例             | 公式输入示例               | 朗读示例   |
| ----- | ----- | ------------------ | -------------------- | ------ |
| mm    | 毫米    | `5\quantity{mm}`   | `$5\quantity{mm}$`   | 五毫米    |
| cm    | 厘米    | `5\quantity{cm}`   | `$5\quantity{cm}$`   | 五厘米    |
| dm    | 分米    | `5\quantity{dm}`   | `$5\quantity{dm}$`   | 五分米    |
| m     | 米     | `5\quantity{m}`    | `$5\quantity{m}$`    | 五米     |
| km    | 千米    | `5\quantity{km}`   | `$5\quantity{km}$`   | 五千米    |
| g     | 克     | `5\quantity{g}`    | `$5\quantity{g}$`    | 五克     |
| kg    | 千克    | `5\quantity{kg}`   | `$5\quantity{kg}$`   | 五千克    |
| t     | 吨     | `5\quantity{t}`    | `$5\quantity{t}$`    | 五吨     |
| mm^2  | 平方毫米  | `5\quantity{mm^2}` | `$5\quantity{mm^2}$` | 五平方毫米  |
| cm^2  | 平方厘米  | `5\quantity{cm^2}` | `$5\quantity{cm^2}$` | 五平方厘米  |
| dm^2  | 平方分米  | `5\quantity{dm^2}` | `$5\quantity{dm^2}$` | 五平方分米  |
| m^2   | 平方米   | `5\quantity{m^2}`  | `$5\quantity{m^2}$`  | 五平方米   |
| km^2  | 平方千米  | `5\quantity{km^2}` | `$5\quantity{km^2}$` | 五平方千米  |
| mm^3  | 立方毫米  | `5\quantity{mm^3}` | `$5\quantity{mm^3}$` | 五立方毫米  |
| cm^3  | 立方厘米  | `5\quantity{cm^3}` | `$5\quantity{cm^3}$` | 五立方厘米  |
| dm^3  | 立方分米  | `5\quantity{dm^3}` | `$5\quantity{dm^3}$` | 五立方分米  |
| m^3   | 立方米   | `5\quantity{m^3}`  | `$5\quantity{m^3}$`  | 五立方米   |
| km^3  | 立方千米  | `5\quantity{km^3}` | `$5\quantity{km^3}$` | 五立方千米  |
| ml    | 毫升    | `5\quantity{ml}`   | `$5\quantity{ml}$`   | 五毫升    |
| s     | 秒     | `5\quantity{s}`    | `$5\quantity{s}$`    | 五秒     |
| min   | 分钟    | `5\quantity{min}`  | `$5\quantity{min}$`  | 五分钟    |
| h     | 小时    | `5\quantity{h}`    | `$5\quantity{h}$`    | 五小时    |
| km/h  | 千米每小时 | `5\quantity{km/h}` | `$5\quantity{km/h}$` | 五千米每小时 |
| g/l   | 克每升   | `5\quantity{g/l}`  | `$5\quantity{g/l}$`  | 五克每升   |

### 常见问题

#### 输入的公式没有被朗读？

1. **分隔符**：确认公式已用 `$...$`、`$$...$$`、`\(...\)` 或 `\[...\]` 包裹
2. **公式复杂度**：确认公式仅使用了[支持的标签和符号](#支持的标签和符号)中的内容
3. **转义字符**：确认在 API 请求中，反斜杠（`\`）已转义为 `\\`

#### 代码中如何处理反斜杠（`\`）？

反斜杠（`\`）在字符串和 JSON 中是转义字符，需要写成 `\\`。例如：在 Python、Java、JavaScript 等语言中，`\frac` 应写为 `\\frac`。
