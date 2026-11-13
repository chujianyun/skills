# 豆包语音合成 WebSocket

<!-- model-detail-quickstart:start -->

双向接口的调用顺序是 `StartConnection` → `StartSession` → `TaskRequest` → `FinishSession`。
文本可以拆成多条 `TaskRequest` 发送；收到的二进制音频按顺序拼接即可。一次连接只执行一次合成。

::: warning
这个接口使用火山语音 v3 **二进制帧协议**，不是 JSON WebSocket。连接建立后发送的每条消息都必须是
二进制帧；不能用 `wscat` 直接粘贴 JSON。
:::

### 开始调用

:::group

```python title="Python"
# pip install "websockets>=14"
import asyncio
import json
import struct
import uuid
from pathlib import Path

import websockets

URL = "wss://tokendance.space/gateway/ark/v3/tts/bidirection"
MODEL = "MODEL_ID"

FULL_CLIENT_REQUEST = 0b0001
AUDIO_ONLY_SERVER = 0b1011
ERROR = 0b1111
WITH_EVENT = 0b0100
POSITIVE_SEQUENCE = 0b0001
NEGATIVE_SEQUENCE = 0b0011

START_CONNECTION = 1
CONNECTION_STARTED = 50
START_SESSION = 100
FINISH_SESSION = 102
SESSION_STARTED = 150
SESSION_FINISHED = 152
TASK_REQUEST = 200
CONNECTION_EVENTS = {1, 2, 50, 51, 52}


def encode_frame(event, payload, session_id=""):
    body = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    frame = bytearray((0x11, (FULL_CLIENT_REQUEST << 4) | WITH_EVENT, 0x10, 0x00))
    frame += struct.pack(">I", event)
    if event not in CONNECTION_EVENTS:
        sid = session_id.encode("utf-8")
        frame += struct.pack(">I", len(sid)) + sid
    frame += struct.pack(">I", len(body)) + body
    return bytes(frame)


def decode_frame(raw):
    if not isinstance(raw, bytes) or len(raw) < 4:
        raise RuntimeError("服务端返回了非法 WebSocket 帧")

    message_type = raw[1] >> 4
    flag = raw[1] & 0x0F
    offset = (raw[0] & 0x0F) * 4

    def read_u32():
        nonlocal offset
        if offset + 4 > len(raw):
            raise RuntimeError("二进制帧长度不足")
        value = struct.unpack_from(">I", raw, offset)[0]
        offset += 4
        return value

    def read_blob():
        nonlocal offset
        size = read_u32()
        end = offset + size
        if end > len(raw):
            raise RuntimeError("二进制帧字段越界")
        value = raw[offset:end]
        offset = end
        return value

    error_code = None
    if message_type == ERROR:
        error_code = read_u32()
    elif flag in (POSITIVE_SEQUENCE, NEGATIVE_SEQUENCE):
        read_u32()  # sequence

    event = None
    if flag == WITH_EVENT:
        event = read_u32()
        if event not in CONNECTION_EVENTS:
            read_blob()  # session_id
        if event in (50, 51, 52):
            read_blob()  # connect_id

    return {
        "type": message_type,
        "event": event,
        "error_code": error_code,
        "payload": read_blob(),
    }


def check_error(frame):
    if frame["type"] != ERROR:
        return
    try:
        message = json.loads(frame["payload"]).get("error", "")
    except json.JSONDecodeError:
        message = frame["payload"].decode("utf-8", errors="replace")
    raise RuntimeError(f'{frame["error_code"]}: {message}')


async def receive_until(ws, expected_event, audio):
    while True:
        frame = decode_frame(await ws.recv())
        check_error(frame)
        if frame["type"] == AUDIO_ONLY_SERVER:
            audio += frame["payload"]
        if frame["event"] == expected_event:
            return frame


async def main():
    headers = {
        "Authorization": "Bearer YOUR_KEY",
        "X-Api-Resource-Id": MODEL,
    }
    audio = bytearray()

    async with websockets.connect(
        URL, additional_headers=headers, max_size=None
    ) as ws:
        await ws.send(encode_frame(START_CONNECTION, {}))
        await receive_until(ws, CONNECTION_STARTED, audio)

        session_id = uuid.uuid4().hex
        await ws.send(encode_frame(START_SESSION, {
            "req_params": {
                "speaker": "zh_female_vv_uranus_bigtts",
                "audio_params": {"format": "mp3", "sample_rate": 24000},
            }
        }, session_id))
        await receive_until(ws, SESSION_STARTED, audio)

        for text in ("你好，", "这是双向流式语音合成。"):
            await ws.send(encode_frame(TASK_REQUEST, {
                "event": TASK_REQUEST,
                "req_params": {"text": text},
            }, session_id))
        await ws.send(encode_frame(FINISH_SESSION, {}, session_id))

        finished = await receive_until(ws, SESSION_FINISHED, audio)
        usage = json.loads(finished["payload"]).get("usage", {})

    Path("out.mp3").write_bytes(audio)
    print(f'wrote out.mp3, text_words={usage.get("text_words", 0)}')


asyncio.run(main())
```

```javascript title="Node.js"
// npm install ws
import { randomUUID } from "node:crypto";
import { writeFileSync } from "node:fs";
import { once } from "node:events";
import WebSocket from "ws";

const URL = "wss://tokendance.space/gateway/ark/v3/tts/bidirection";
const MODEL = "MODEL_ID";

const FULL_CLIENT_REQUEST = 0b0001;
const AUDIO_ONLY_SERVER = 0b1011;
const ERROR = 0b1111;
const WITH_EVENT = 0b0100;
const POSITIVE_SEQUENCE = 0b0001;
const NEGATIVE_SEQUENCE = 0b0011;

const START_CONNECTION = 1;
const CONNECTION_STARTED = 50;
const START_SESSION = 100;
const FINISH_SESSION = 102;
const SESSION_STARTED = 150;
const SESSION_FINISHED = 152;
const TASK_REQUEST = 200;
const CONNECTION_EVENTS = new Set([1, 2, 50, 51, 52]);

function uint32(value) {
  const out = Buffer.allocUnsafe(4);
  out.writeUInt32BE(value);
  return out;
}

function encodeFrame(event, payload, sessionId = "") {
  const body = Buffer.from(JSON.stringify(payload));
  const parts = [
    Buffer.from([0x11, (FULL_CLIENT_REQUEST << 4) | WITH_EVENT, 0x10, 0x00]),
    uint32(event),
  ];
  if (!CONNECTION_EVENTS.has(event)) {
    const sid = Buffer.from(sessionId);
    parts.push(uint32(sid.length), sid);
  }
  parts.push(uint32(body.length), body);
  return Buffer.concat(parts);
}

function decodeFrame(raw) {
  const data = Buffer.from(raw);
  const type = data[1] >> 4;
  const flag = data[1] & 0x0f;
  let offset = (data[0] & 0x0f) * 4;

  const readUint32 = () => {
    const value = data.readUInt32BE(offset);
    offset += 4;
    return value;
  };
  const readBlob = () => {
    const size = readUint32();
    const value = data.subarray(offset, offset + size);
    offset += size;
    return value;
  };

  let errorCode = null;
  if (type === ERROR) errorCode = readUint32();
  else if (flag === POSITIVE_SEQUENCE || flag === NEGATIVE_SEQUENCE) readUint32();

  let event = null;
  if (flag === WITH_EVENT) {
    event = readUint32();
    if (!CONNECTION_EVENTS.has(event)) readBlob(); // session_id
    if ([50, 51, 52].includes(event)) readBlob();  // connect_id
  }
  return { type, event, errorCode, payload: readBlob() };
}

async function receiveUntil(ws, expectedEvent, audio) {
  for await (const raw of ws) {
    const frame = decodeFrame(raw);
    if (frame.type === ERROR) {
      throw new Error(`${frame.errorCode}: ${frame.payload.toString()}`);
    }
    if (frame.type === AUDIO_ONLY_SERVER) audio.push(frame.payload);
    if (frame.event === expectedEvent) return frame;
  }
  throw new Error("WebSocket closed before the expected event");
}

async function main() {
  const ws = new WebSocket(URL, {
    headers: {
      Authorization: "Bearer YOUR_KEY",
      "X-Api-Resource-Id": MODEL,
    },
  });
  await once(ws, "open");
  const audio = [];

  ws.send(encodeFrame(START_CONNECTION, {}));
  await receiveUntil(ws, CONNECTION_STARTED, audio);

  const sessionId = randomUUID().replaceAll("-", "");
  ws.send(encodeFrame(START_SESSION, {
    req_params: {
      speaker: "zh_female_vv_uranus_bigtts",
      audio_params: { format: "mp3", sample_rate: 24000 },
    },
  }, sessionId));
  await receiveUntil(ws, SESSION_STARTED, audio);

  for (const text of ["你好，", "这是双向流式语音合成。"]) {
    ws.send(encodeFrame(TASK_REQUEST, {
      event: TASK_REQUEST,
      req_params: { text },
    }, sessionId));
  }
  ws.send(encodeFrame(FINISH_SESSION, {}, sessionId));

  const finished = await receiveUntil(ws, SESSION_FINISHED, audio);
  const usage = JSON.parse(finished.payload).usage ?? {};
  writeFileSync("out.mp3", Buffer.concat(audio));
  console.log(`wrote out.mp3, text_words=${usage.text_words ?? 0}`);
  ws.close();
}

await main();
```

:::

### 会话顺序

| 客户端发送 | 等待服务端事件 | 说明 |
| --- | --- | --- |
| `StartConnection(1)` | `ConnectionStarted(50)` | 建立协议级连接 |
| `StartSession(100)` | `SessionStarted(150)` | `req_params` 中设置音色和音频格式 |
| 一个或多个 `TaskRequest(200)` | 音频帧 | 每个请求携带一段 `text` |
| `FinishSession(102)` | `SessionFinished(152)` | 终态 payload 包含 `usage.text_words` |

`AudioOnlyServer` 帧的 payload 已经是裸音频，不需要 Base64 解码，按收到顺序拼接即可。
`TaskRequest` 的 payload 必须使用 `{"event":200,"req_params":{"text":"..."}}` 信封；帧头里的
event 不能替代 payload 内的同名字段，否则上游会直接结束会话而不生成音频。
网关在会话终态后关闭连接；当前不支持在同一条连接中复用多个会话。

### 请求参数

`StartSession` 的 `req_params` 与[单向语音合成协议](%E8%B1%86%E5%8C%85%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.md)基本一致：
`speaker` 和 `audio_params` 必填，正文改由后续 `TaskRequest` 分段发送。当前支持
`seed-tts-2.0` 公版音色，不支持自定义音色。

完整帧协议、事件定义和参数说明见[上游官方文档](https://www.volcengine.com/docs/6561/1329505)。

<!-- model-detail-quickstart:end -->
