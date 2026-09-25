> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 连接复用与连接池

> 面向高并发场景的 HTTP 连接复用和 WebSocket 连接池配置指南。

复用连接可以减少资源消耗、提升吞吐量。具体策略取决于协议类型：

- **HTTP API**（文本生成、多模态、Embeddings）：通过连接池配置（Java）或 Session 对象（Python）复用 TCP 连接。
- **WebSocket API**（TTS、实时语音）：池化持有长连接的合成器对象。

## 前提条件

- 已获取 API Key 并配置为 `DASHSCOPE_API_KEY` 环境变量。
- 已安装最新版 DashScope SDK：
  - **Python SDK**：>= 1.25.2
  - **Java SDK**：>= 2.16.6

## HTTP 连接复用

<Note>
  DashScope 端点因模型类型而异：

  - **文本模型**（`qwen-plus`、`qwen3-max` 等）：使用 `Generation` 类，路由到 `/services/aigc/text-generation/generation`。
  - **多模态模型**（`qwen3.7-plus`、`qwen3-vl-plus` 等）：使用 `MultiModalConversation` 类，路由到 `/services/aigc/multimodal-generation/generation`。
</Note>

### Java SDK

连接池默认启用，可根据需要调整以下参数。

| 参数                            | 说明                                      | 默认值 | 单位 | 备注                  |
| ----------------------------- | --------------------------------------- | --- | -- | ------------------- |
| `connectTimeout`              | 建立连接的超时时间                               | 120 | 秒  | 低延迟场景可缩短此值以减少等待时间。  |
| `readTimeout`                 | 读取数据的超时时间                               | 300 | 秒  |                     |
| `writeTimeout`                | 写入数据的超时时间                               | 60  | 秒  |                     |
| `connectionIdleTimeout`       | 空闲连接的超时时间                               | 300 | 秒  | 适当延长可避免高并发时频繁重连。    |
| `connectionPoolSize`          | 连接池最大连接数                                | 32  | 个  | 过少会导致阻塞，过多会增加服务器压力。 |
| `maximumAsyncRequests`        | 所有主机的最大并发请求数，需 ≤ `connectionPoolSize`   | 32  | 个  |                     |
| `maximumAsyncRequestsPerHost` | 单个主机的最大并发请求数，需 ≤ `maximumAsyncRequests` | 32  | 个  |                     |

配置连接池参数并调用模型服务：

```java
// 建议 DashScope SDK 版本 >= 2.12.0
import java.time.Duration;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.ConnectionConfigurations;
import com.alibaba.dashscope.protocol.Protocol;
import com.alibaba.dashscope.utils.Constants;

public class Main {
  public static MultiModalConversationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
    MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
    Map<String, Object> textContent = new HashMap<>();
    textContent.put("text", "Who are you?");
    MultiModalMessage userMsg = MultiModalMessage.builder()
        .role(Role.USER.getValue())
        .content(Collections.singletonList(textContent))
        .build();
    MultiModalConversationParam param = MultiModalConversationParam.builder()
        // 如果未配置环境变量，请替换为您的 API Key：.apiKey("sk-xxx")
        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
        .model("qwen3.7-plus")
        .messages(Collections.singletonList(userMsg))
        .build();

    return conv.call(param);
  }
  public static void main(String[] args) {
    // 连接池配置
    Constants.connectionConfigurations = ConnectionConfigurations.builder()
        .connectTimeout(Duration.ofSeconds(10))  // 建立连接超时时间，默认 120s
        .readTimeout(Duration.ofSeconds(300)) // 读取数据超时时间，默认 300s
        .writeTimeout(Duration.ofSeconds(60)) // 写入数据超时时间，默认 60s
        .connectionIdleTimeout(Duration.ofSeconds(300)) // 空闲连接超时时间，默认 300s
        .connectionPoolSize(256) // 连接池最大连接数，默认 32
        .maximumAsyncRequests(256)  // 最大并发请求数，默认 32
        .maximumAsyncRequestsPerHost(256) // 单主机最大并发请求数，默认 32
        .build();

    try {
      MultiModalConversationResult result = callWithMessage();
      System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    } catch (ApiException | NoApiKeyException | InputRequiredException e) {
      System.err.println("调用服务时发生错误：" + e.getMessage());
    }
    System.exit(0);
  }
}
```

### Python SDK

Python SDK 通过自定义 Session 实现连接复用，支持[异步 (aiohttp)](#异步-aiohttp)和[同步 (requests.Session)](#同步-requests-session)两种方式。

#### 异步 (aiohttp)

使用 `aiohttp.ClientSession` 和 `aiohttp.TCPConnector` 实现异步连接复用。

| 参数               | 说明        | 默认值   | 备注                     |
| ---------------- | --------- | ----- | ---------------------- |
| `limit`          | 总连接数上限    | 100   | 增大此值可提升并发能力。           |
| `limit_per_host` | 单主机连接数上限  | 0（不限） | 防止对单个主机施加过大压力。         |
| `ssl`            | SSL 上下文配置 | None  | 用于 HTTPS 连接的 SSL 证书验证。 |

```python
import asyncio
import aiohttp
import ssl
import certifi
from dashscope import AioMultiModalConversation
import dashscope
import os

async def main():
  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 如果未配置环境变量，请替换为您的 API Key：dashscope.api_key = "sk-xxx"
  dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

  # 配置连接参数
  connector = aiohttp.TCPConnector(
    limit=100,           # 总连接数上限
    limit_per_host=30,   # 单主机连接数上限
    ssl=ssl.create_default_context(cafile=certifi.where()),
  )

  # 创建自定义 Session 并传入调用方法
  async with aiohttp.ClientSession(connector=connector) as session:
    response = await AioMultiModalConversation.call(
      model='qwen3.7-plus',
      messages=[{'role': 'user', 'content': [{'text': 'Hello, please introduce yourself'}]}],
      session=session,  # 传入自定义 Session
    )
    print(response)

asyncio.run(main())
```

#### 同步 (requests.Session)

使用 `requests.Session` 实现同步连接复用。同一 Session 内的请求会复用 TCP 连接。

```python
import requests
from dashscope import MultiModalConversation
import dashscope
import os

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 如果未配置环境变量，请替换为您的 API Key：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 使用 with 语句确保 Session 正确关闭
with requests.Session() as session:
  response = MultiModalConversation.call(
    model='qwen3.7-plus',
    messages=[{'role': 'user', 'content': [{'text': 'Hello'}]}],
    session=session  # 传入自定义 Session
  )
  print(response)
```

在多次调用间复用同一个 Session：

```python
import requests
from dashscope import MultiModalConversation
import dashscope
import os

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 如果未配置环境变量，请替换为您的 API Key：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 创建 Session 对象
session = requests.Session()

try:
  # 在多次调用间复用同一个 Session
  response1 = MultiModalConversation.call(
    model='qwen3.7-plus',
    messages=[{'role': 'user', 'content': [{'text': 'Hello'}]}],
    session=session
  )
  print(response1)

  response2 = MultiModalConversation.call(
    model='qwen3.7-plus',
    messages=[{'role': 'user', 'content': [{'text': 'Introduce yourself'}]}],
    session=session
  )
  print(response2)
finally:
  # 确保 Session 正确关闭
  session.close()
```

## WebSocket 连接池

TTS 服务使用 WebSocket 连接进行实时流式传输。在生产环境中，每次请求都新建连接会浪费资源并增加延迟。本节介绍面向高吞吐 TTS 场景的连接池、对象池和并发请求管理方案。

### Python：对象池

Python SDK 提供 `SpeechSynthesizerObjectPool` 来管理和复用 `SpeechSynthesizer` 实例。对象池在初始化时预创建对象并建立 WebSocket 连接，消除了逐请求建连的开销。

**池大小建议**：将 `max_size` 设置为峰值并发的 1.5～2 倍，但不要超过账户的 QPS 上限。

```python
import os
import threading
import dashscope
from dashscope.audio.tts_v2 import *

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'

# 创建全局对象池（仅在启动时初始化一次）
pool = SpeechSynthesizerObjectPool(max_size=20)

def synthesize(text, task_id):
  complete_event = threading.Event()

  class Callback(ResultCallback):
    def on_open(self):
      self.file = open(f'result_{task_id}.mp3', 'wb')

    def on_complete(self):
      complete_event.set()

    def on_error(self, message):
      print(f'[task_{task_id}] 错误：{message}')

    def on_data(self, data):
      self.file.write(data)

    def on_close(self):
      if hasattr(self, 'file'):
        self.file.close()

  callback = Callback()

  # 从池中借用一个已建连的合成器
  synth = pool.borrow_synthesizer(
    model='cosyvoice-v3-flash',
    voice='longanyang',
    callback=callback
  )

  try:
    synth.call(text)
    complete_event.wait()
    print(f'[task_{task_id}] 首包延迟：'
       f'{synth.get_first_package_delay()} ms')
    # 将合成器归还到池中以供复用
    pool.return_synthesizer(synth)
  except Exception as e:
    print(f'[task_{task_id}] 失败：{e}')
    synth.close()  # 失败的对象不要归还到池中

# 运行并发任务
texts = ["第一句话。", "第二句话。", "第三句话。"]
threads = [threading.Thread(target=synthesize, args=(t, i))
     for i, t in enumerate(texts)]
for t in threads:
  t.start()
for t in threads:
  t.join()

pool.shutdown()
```

<Warning>
  如果任务失败或仍在运行，不要将合成器归还到池中，应手动调用 close 关闭。
</Warning>

### Java：连接池 + 对象池

Java SDK 使用 OkHttp3 连接池（默认启用），并可选配 Apache Commons Pool2 对象池来管理 `SpeechSynthesizer` 实例。

**第 1 步：通过环境变量配置连接池**

| 变量                                          | 默认值 | 建议        |
| ------------------------------------------- | --- | --------- |
| `DASHSCOPE_CONNECTION_POOL_SIZE`            | 32  | 峰值并发的 2 倍 |
| `DASHSCOPE_MAXIMUM_ASYNC_REQUESTS`          | 32  | 与连接池大小一致  |
| `DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST` | 32  | 与连接池大小一致  |

```bash
export DASHSCOPE_CONNECTION_POOL_SIZE=2000
export DASHSCOPE_MAXIMUM_ASYNC_REQUESTS=2000
export DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST=2000
```

**第 2 步：添加 commons-pool2 依赖**

<Tabs>
  <Tab title="Maven">
    ```xml
    <dependency>
      <groupId>org.apache.commons</groupId>
      <artifactId>commons-pool2</artifactId>
      <version>the-latest-version</version>
    </dependency>
    ```
  </Tab>

  <Tab title="Gradle">
    ```gradle
    implementation group: 'org.apache.commons',
        name: 'commons-pool2', version: 'the-latest-version'
    ```
  </Tab>
</Tabs>

**第 3 步：创建并使用对象池**

| 变量                                 | 默认值 | 建议                     |
| ---------------------------------- | --- | ---------------------- |
| `SAMBERT_OBJECTPOOL_SIZE`（Sambert） | 500 | 峰值并发的 1.5～2 倍，不超过连接池大小 |

```java
import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

// 工厂
class SynthesizerFactory extends BasePooledObjectFactory<SpeechSynthesizer> {
  public SpeechSynthesizer create() { return new SpeechSynthesizer(); }
  public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
    return new DefaultPooledObject<>(obj);
  }
}

// 对象池（全局单例）
GenericObjectPoolConfig<SpeechSynthesizer> config = new GenericObjectPoolConfig<>();
config.setMaxTotal(1200);
config.setMaxIdle(1200);
config.setMinIdle(1200);
GenericObjectPool<SpeechSynthesizer> pool =
  new GenericObjectPool<>(new SynthesizerFactory(), config);

// 在每个任务中使用
SpeechSynthesizer synth = pool.borrowObject();
try {
  // ... 配置参数并调用 synth
  pool.returnObject(synth);
} catch (Exception e) {
  synth = null;  // 失败时不要归还
}
```

<Tip>
  服务器配置参考：4 核 8 GiB 机器可支撑约 600 个并发 Sambert TTS 任务，对象池大小 1200，连接池大小 2000。
</Tip>

## 最佳实践

- **Java SDK**：根据实际并发量设置 `connectionPoolSize` 和 `maximumAsyncRequests`。连接数过少会导致阻塞，过多会增加服务器压力。
- **Python SDK**：使用 `with` 语句管理 Session 生命周期，确保资源正确释放。
- **选择合适的调用方式**：异步应用（如 asyncio 或 FastAPI）使用异步调用，传统应用使用同步调用。
- **WebSocket 对象池**：如果任务失败或仍在运行，不要将合成器归还到池中，应手动调用 close 关闭。

## 性能监控

跟踪以下指标以维护生产环境 TTS 服务的健康状态：

| 指标    | 说明                 | 目标值         |
| ----- | ------------------ | ----------- |
| 首包延迟  | 从发送请求到收到第一个音频分片的时间 | \< 500 ms   |
| 端到端延迟 | 完成整个合成的总时间         | 取决于文本长度     |
| 错误率   | 失败请求的百分比           | \< 0.1%     |
| 池使用率  | 已借出对象数 / 池大小       | 峰值时 60%～80% |
| 连接复用率 | 复用连接数 / 总请求数       | > 95%       |

通过 SDK 获取这些指标：

```python
# TTS
print(f"Request ID: {synthesizer.get_last_request_id()}")
print(f"首包延迟：{synthesizer.get_first_package_delay()} ms")
```

```java
// TTS
System.out.println("Request ID: " + synthesizer.getLastRequestId());
System.out.println("首包延迟：" + synthesizer.getFirstPackageDelay() + " ms");
```

## 上线检查清单

上线前请确认以下事项：

- [ ] API Key 存储在环境变量中，未硬编码到代码里。
- [ ] 连接池和对象池大小已按预期峰值负载配置。
- [ ] 池大小未超过账户的 QPS 上限。
- [ ] 错误处理逻辑将失败对象销毁（而非归还到池中）。
- [ ] 优雅停机时调用了 `pool.shutdown()`（Python）或关闭池（Java）。
- [ ] WebSocket 连接使用了正确的区域端点。
- [ ] 监控面板已配置首包延迟、错误率和池使用率等指标。
- [ ] 已完成 2 倍预期峰值并发的压力测试。
- [ ] 已实现指数退避的重试逻辑以应对瞬时故障。

## 相关文档

- [语音合成](/developer-guides/speech/tts) -- TTS 模型、参数和流式模式。
- [实时语音合成](/developer-guides/speech/realtime-streaming) -- 实时 TTS 流式传输指南。
- [提升识别准确率](/developer-guides/accuracy-tuning/speech-recognition) -- ASR 优化，包括高并发 ASR 模式。
