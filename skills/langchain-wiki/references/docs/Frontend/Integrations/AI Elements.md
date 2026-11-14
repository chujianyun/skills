# AI Elements

> Composable shadcn/ui-based components for AI chat interfaces with useStream

[AI Elements](https://elements.ai-sdk.dev/) is a composable, shadcn/ui-based component library purpose-built for AI chat interfaces. Components like `Conversation`, `Message`, `Tool`, `Reasoning`, and `PromptInput` are designed to drop directly into any React project and wire to `stream.messages` with minimal glue code.

> [!TIP]
>
> Clone and run the [full AI Elements example](https://github.com/langchain-ai/langgraphjs/tree/main/examples/ai-elements) to see tool call rendering, reasoning display, streaming messages, and more in a working project.

## How it works

1. **Install components as source files:** AI Elements ships via a CLI that adds components directly to your project (shadcn/ui registry style)
2. **Map messages to components:** iterate `stream.messages`, render `HumanMessage` instances as user bubbles and `AIMessage` instances as assistant responses
3. **Compose richer UIs:** wrap tool calls in `<Tool>`, reasoning in `<Reasoning>`, and everything in `<Conversation>` for scroll management

## Installation

Install AI Elements components via the CLI. They're added as editable source files into your project:

```bash
npm install @langchain/react
npx ai-elements@latest add conversation message prompt-input tool reasoning suggestion
```

## Wiring useStream

Render AI Elements components directly from `stream.messages`. Each LangChain `BaseMessage` maps to a component:

```tsx
import { useStream } from "@langchain/react";
import { HumanMessage, AIMessage } from "langchain";

import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/components/ai-elements/message";
import {
  Tool,
  ToolHeader,
  ToolContent,
  ToolInput,
  ToolOutput,
} from "@/components/ai-elements/tool";
import {
  Reasoning,
  ReasoningTrigger,
  ReasoningContent,
} from "@/components/ai-elements/reasoning";
import {
  PromptInput,
  PromptInputBody,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputSubmit,
} from "@/components/ai-elements/prompt-input";

function getReasoningText(msg: AIMessage) {
  return msg.contentBlocks.find((block) => block.type === "reasoning")?.reasoning ?? "";
}

function getTextContent(msg: AIMessage) {
  return msg.text;
}

function getToolCalls(msg: AIMessage) {
  return (msg.tool_calls ?? []).map((tc) => ({
    id: tc.id,
    name: tc.name,
    args: tc.args,
    state: "input-available" as const,
  }));
}

export function Chat() {
  const stream = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "ai_elements",
  });

  return (
    <div className="flex flex-col h-dvh">
      <Conversation className="flex-1">
        <ConversationContent>
          {stream.messages.map((msg, i) => {
            if (HumanMessage.isInstance(msg)) {
              return (
                <Message key={i} from="user">
                  <MessageContent>{msg.text}</MessageContent>
                </Message>
              );
            }
            if (AIMessage.isInstance(msg)) {
              return (
                <div key={i}>
                  {/* Reasoning block (shows when model emits thinking tokens) */}
                  <Reasoning>
                    <ReasoningTrigger />
                    <ReasoningContent>{getReasoningText(msg)}</ReasoningContent>
                  </Reasoning>

                  {/* Inline tool calls with input/output display */}
                  {getToolCalls(msg).map((tc) => (
                    <Tool key={tc.id} defaultOpen>
                      <ToolHeader type={`tool-${tc.name}`} state={tc.state} />
                      <ToolContent>
                        <ToolInput input={tc.args} />
                        {tc.output && (
                          <ToolOutput output={tc.output} errorText={undefined} />
                        )}
                      </ToolContent>
                    </Tool>
                  ))}

                  {/* Streamed text response */}
                  <Message from="assistant">
                    <MessageContent>
                      <MessageResponse>{getTextContent(msg)}</MessageResponse>
                    </MessageContent>
                  </Message>
                </div>
              );
            }
          })}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      <PromptInput
        onSubmit={({ text }) =>
          stream.submit({ messages: [{ type: "human", content: text }] })
        }
      >
        <PromptInputBody>
          <PromptInputTextarea placeholder="Ask me something..." />
        </PromptInputBody>
        <PromptInputFooter>
          <PromptInputSubmit
            status={stream.isLoading ? "streaming" : "ready"}
          />
        </PromptInputFooter>
      </PromptInput>
    </div>
  );
}
```

## Best practices

* **Edit source files freely:** components ship in your project, not as an external package dependency, so you can change anything without forking
* **Use `MessageResponse` for streaming:** it handles streamed partial tokens correctly; avoid rendering raw message content directly during streaming
* **Wrap in `Conversation`:** the `Conversation` component manages scroll behaviour so new messages auto-scroll into view
* **Gate on `isInstance`:** use `HumanMessage.isInstance(msg)` and `AIMessage.isInstance(msg)` rather than checking `msg.getType()` for proper TypeScript narrowing

***

[Connect these docs](https://docs.langchain.com/use-these-docs.md) to your agent of choice via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/integrations/ai-elements.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).
