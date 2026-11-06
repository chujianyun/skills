# Multimodal inputs and outputs

> Use images, audio, video, and documents with Deep Agents when your model supports multimodal inputs and tool results

Deep Agents supports multimodal workflows when you use a [Large Language Model](https://docs.langchain.com/oss/python/integrations/chat.md) that accepts multimodal inputs and tool results or returns multimodal outputs. You can attach images and other media to user messages, read non-text files with the built-in `read_file` tool, and return multimodal content from custom tools.

Built-in [context compression](../Context%20management/Context%20engineering%20in%20Deep%20Agents.md#context-compression) is primarily text-oriented. Plan multimodal workloads accordingly: store large media in a backend and pass references when possible.

## Multimodal user input

Pass multimodal content in the `messages` you send to the agent, using the same [standard content blocks](https://docs.langchain.com/oss/python/langchain/messages.md#standard-content-blocks) as LangChain chat models:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "What is in this screenshot?"},
            {"type": "image", "url": "https://example.com/screenshot.png"},
        ],
    }],
})
```

For block types, provider-specific requirements, and additional examples (PDF, audio, video), see [Multimodal messages](https://docs.langchain.com/oss/python/langchain/messages.md#multimodal).

## Built-in `read_file` tool

The harness `read_file` tool returns [standard content blocks](https://docs.langchain.com/oss/python/langchain/messages.md#standard-content-blocks) for supported multimodal files instead of plain text. The agent can inspect images, documents, and media stored in its [filesystem](../Deep%20Agents%20overview.md#virtual-filesystem-access) when the selected model supports the corresponding modality. Check the provider's documentation for your model's supported MIME types.

> [accordion] Supported multimodal file extensions
>
> | Type | Extensions |
> | - | - |
> | [Image](https://docs.langchain.com/oss/python/langchain/messages.md#multimodal) | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.heic`, `.heif` |
> | [Video](https://docs.langchain.com/oss/python/langchain/messages.md#multimodal) | `.mp4`, `.mpeg`, `.mov`, `.avi`, `.flv`, `.mpg`, `.webm`, `.wmv`, `.3gpp` |
> | [Audio](https://docs.langchain.com/oss/python/langchain/messages.md#multimodal) | `.wav`, `.mp3`, `.aiff`, `.aac`, `.ogg`, `.flac` |
> | [File](https://docs.langchain.com/oss/python/langchain/messages.md#multimodal) | `.pdf`, `.ppt`, `.pptx` |

## Custom tool outputs

[Custom tools](Tools.md#custom-tools) can contain multimodal files, such as images:

```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool


@tool
def capture_screenshot() -> list[dict]:
    """Capture a screenshot of the current page."""
    return [
        {"type": "text", "text": "Screenshot of the current page:"},
        {"type": "image", "url": "https://example.com/page.png"},
    ]
```

The return value is converted to a `ToolMessage` the model reads on the next turn. Access the normalized representation with `content_blocks` on the resulting message.

For return-type options, serialization behavior, and MCP examples, see [Multimodal content](https://docs.langchain.com/oss/python/langchain/mcp/tools.md#multimodal-content).

> [!TIP]
>
> When a tool produces images or other large binary data, save the artifact to a [backend](Backends.md) and return a concise text description plus a path or URL. This keeps message history smaller and works better with [context compression](../Context%20management/Context%20engineering%20in%20Deep%20Agents.md#context-compression).

## Context compression and multimodal content

Built-in offloading and summarization are optimized for text and message history:

* **Offloading** measures text tokens only. Non-text blocks (including images) are preserved in replacement messages rather than compressed. A message that contains only an image is not offloaded based on image size alone.
* **Summarization** compacts older messages into a text-only summary. Image, audio, video, and file blocks in that range are not carried forward—the model only sees what the summarizer writes about them. Recent messages below the keep threshold stay unchanged.

  When summarization runs, media blocks in older turns drop out of the active context:

  ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
  # Before — model receives image blocks in older turns
  [
      HumanMessage(
          content=[
              {"type": "text", "text": "What trends do you see in this chart?"},
              {"type": "image", "base64": IMG, "mime_type": "image/png"},
          ]
      ),
      ToolMessage(
          content=[
              {"type": "text", "text": "Updated chart:"},
              {"type": "image", "base64": IMG, "mime_type": "image/png"},
          ],
          tool_call_id="call_chart_1",
      ),
      AIMessage(content="Revenue rose in Q3 based on the chart trend."),
      HumanMessage(content="Reply with one sentence summarizing our analysis."),
  ]

  # After — those turns collapse to text; image blocks are gone
  {"content": (
      "User asked about trends in a chart screenshot. "
      "Tool returned an updated chart. Agent identified Q3 revenue growth."
  )}
  ```

  The original conversation is still written to the filesystem as text. See [Summarization](../Context%20management/Context%20engineering%20in%20Deep%20Agents.md#summarization) for triggers, keep thresholds, and the full flow.

For multimodal-heavy workloads:

* Store images, screenshots, and charts in a filesystem backend or external object store, then pass file paths or URLs through messages.
* Prefer references over base64-encoded image blocks in long-running conversations.
* Use [subagents](../Delegation/Subagents.md) for image-heavy inspection so the main agent receives a compact text result.
* Tune summarization thresholds or provide a custom token counter when your provider charges many tokens for images.

See [Context compression](../Context%20management/Context%20engineering%20in%20Deep%20Agents.md#context-compression) for offloading thresholds, summarization triggers, and customization options.

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/deepagents/multimodal.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
