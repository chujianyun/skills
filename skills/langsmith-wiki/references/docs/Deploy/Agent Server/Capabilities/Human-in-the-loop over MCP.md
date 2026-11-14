# Human-in-the-loop over MCP

> Ask an MCP client for input when an agent exposed through the Agent Server MCP endpoint pauses, then resume the tool call with the answers.

When an agent exposed through the [MCP endpoint](MCP%20endpoint%20in%20Agent%20Server.md) calls [`interrupt`](https://reference.langchain.com/python/langgraph/types/interrupt), [Agent Server](Agent%20Server.md) asks the MCP client for the answer with [elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation). When the client answers, Agent Server resumes the agent. A person can answer a question, review a tool call, or complete a sign-in flow without leaving the MCP client. To answer interrupts through the Agent Server API instead, see [Human-in-the-loop using server API](Human-in-the-loop%20using%20server%20API.md).

> [!NOTE]
>
> Human-in-the-loop over MCP requires `langgraph-api>=0.18.0` and an MCP client that uses protocol revision `2026-07-28` and declares the `elicitation` capability.

## Pause and resume a tool call

Each pause is one round trip between the client and Agent Server:

1. The client calls the tool. Agent Server runs the agent on a new thread.
2. The agent calls `interrupt()`. The tool call returns `"resultType": "input_required"`, with one `elicitation/create` request per question in `inputRequests`, and an opaque `requestState`.
3. The client asks the user. Then it calls the same tool again with the same arguments, the answers in `inputResponses` under the same keys, and the `requestState` it received.
4. Agent Server resumes the agent. The result is either a new round of questions, with a new `requestState`, or the tool result.

For example, the `greeter` agent from [Relay elicitation requests](#relay-elicitation-requests) asks for a name:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "inputRequests": {
      "user_name": {
        "method": "elicitation/create",
        "params": {
          "message": "What is your name?",
          "mode": "form",
          "requestedSchema": {
            "properties": {
              "name": {
                "type": "string"
              }
            },
            "required": [
              "name"
            ],
            "type": "object"
          }
        }
      }
    },
    "requestState": "01a17b0e-645a-7262-9006-0c9a99e8410d.ZpGdPvXznSjaWLC1pzPMkfnCABBCtiZuYMjERmZUaDM",
    "resultType": "input_required",
    "_meta": {
      "io.modelcontextprotocol/serverInfo": {
        "name": "LangGraph",
        "version": "0.18.0"
      }
    }
  }
}
```

The client answers by calling the tool again:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "greeter",
    "arguments": {},
    "inputResponses": {
      "user_name": {
        "action": "accept",
        "content": {
          "name": "Ada"
        }
      }
    },
    "requestState": "01a17b0e-645a-7262-9006-0c9a99e8410d.ZpGdPvXznSjaWLC1pzPMkfnCABBCtiZuYMjERmZUaDM",
    "_meta": {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {
        "elicitation": {
          "form": {}
        }
      }
    }
  }
}
```

The tool result is the agent's final output as JSON text, `{"greeting":"Hello, Ada!"}`.

These examples show the request and response bodies. On `2026-07-28`, MCP clients also send the `MCP-Protocol-Version: 2026-07-28` header, and `Mcp-Method` and `Mcp-Name` headers that match the body. Without the version header, Agent Server treats the request as coming from an older client. A pause then returns the error result described in [Support clients without elicitation](#support-clients-without-elicitation).

Agent Server applies these rules to every round:

* **Several questions**: When several interrupts are pending at once, such as from parallel nodes, Agent Server asks all of them in one round.
* **Missing answers**: When `inputResponses` lacks an answer to a question, Agent Server asks the same questions again, with the same `requestState`. It ignores answers to questions it did not ask.
* **Answers in the first call**: Answers sent in the first call, without a `requestState`, answer the first round of questions.
* **Repeated answers**: Agent Server resumes the agent once, even when the client sends the same answers more than once.
* **Invalid answers**: An answer that does not fit its question fails with JSON-RPC error `-32602` and HTTP status 400. When the answer came with a `requestState`, the round stays open, so the client can answer it again. An invalid answer in a first call, without a `requestState`, deletes that call's thread, so the client calls the tool again from the start.
* **Invalid state**: A modified `requestState`, or one sent with another tool name or other arguments, fails with JSON-RPC error `-32602` (`Invalid or expired requestState`) and HTTP status 400.
* **Runtime context**: A request can carry a `context` object next to `arguments`, which becomes the agent's [runtime context](https://docs.langchain.com/oss/python/langgraph/graph-api.md#runtime-context). When a request answers a round, the resumed run gets that request's `context`.
* **Lifetime**: When a request without a `requestState` finishes the tool call, Agent Server deletes the thread. When a request with a `requestState` finishes it, Agent Server keeps the thread for 10 minutes. A client that resends its last answers in that time gets the same result. A call that stays paused expires 24 hours after its latest round of questions. A shorter `default_ttl` in the [thread TTL configuration](../Develop%20your%20application/Persistence/How%20to%20add%20TTLs%20to%20your%20application.md#configuring-thread-and-checkpoint-ttl) shortens both times.

## Ask a text question

When the interrupt value is a string, Agent Server asks it as a form with one text field:

```python
from langgraph.graph import START, StateGraph
from langgraph.types import interrupt
from typing_extensions import TypedDict


class State(TypedDict, total=False):
    region: str


def choose_region(state: State) -> State:
    region = interrupt("Which region should the service deploy to?")
    return {"region": region}


graph = (
    StateGraph(State)
    .add_node(choose_region)
    .add_edge(START, "choose_region")
    .compile()
)
```

The client receives this question in `inputRequests`:

```json
{
  "answer-9ef115e0cbdb4042": {
    "method": "elicitation/create",
    "params": {
      "message": "Which region should the service deploy to?",
      "mode": "form",
      "requestedSchema": {
        "properties": {
          "response": {
            "type": "string"
          }
        },
        "required": [
          "response"
        ],
        "type": "object"
      }
    }
  }
}
```

The client answers in the `response` field, such as `{"action": "accept", "content": {"response": "eu-west-1"}}`, and the agent resumes with the string `eu-west-1`. A `decline` or `cancel` answer ends the tool call with an error result: `The request for input was declined.` or `The request for input was cancelled.`

Agent Server derives the key from the question, so the key stays the same when a client sends the call again from the start. When two pending interrupts ask the same text question, one answer resumes both.

## Ask for typed input

To ask for structured input, pass a [`response_schema`](https://docs.langchain.com/oss/python/langgraph/interrupts#define-an-interrupt-response-schema) to `interrupt()`. Response schemas require `langgraph>=1.2.12`. Agent Server turns the schema into the form and checks each answer against it. When the schema is a type, such as a Pydantic model, LangGraph also validates the answer before the agent resumes:

```python
from typing import Literal

from langgraph.graph import START, StateGraph
from langgraph.types import interrupt
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Deployment(BaseModel):
    region: Literal["us-east-1", "eu-west-1"]
    replicas: int = Field(ge=1, le=10)


class State(TypedDict, total=False):
    region: str
    replicas: int


def plan_deployment(state: State) -> State:
    deployment = interrupt(
        "Where should the service deploy?", response_schema=Deployment
    )
    return {"region": deployment.region, "replicas": deployment.replicas}


graph = (
    StateGraph(State)
    .add_node(plan_deployment)
    .add_edge(START, "plan_deployment")
    .compile()
)
```

The client receives this question:

```json
{
  "answer-8a201eb4b84bf9bc": {
    "method": "elicitation/create",
    "params": {
      "message": "Where should the service deploy?",
      "mode": "form",
      "requestedSchema": {
        "properties": {
          "region": {
            "enum": [
              "us-east-1",
              "eu-west-1"
            ],
            "title": "Region",
            "type": "string"
          },
          "replicas": {
            "maximum": 10,
            "minimum": 1,
            "title": "Replicas",
            "type": "integer"
          }
        },
        "required": [
          "region",
          "replicas"
        ],
        "type": "object"
      }
    }
  }
}
```

An answer such as `{"region": "eu-west-1", "replicas": 3}` resumes the agent, and the tool result is `{"region":"eu-west-1","replicas":3}`. An answer outside the schema, such as `"replicas": 20`, fails with error `-32602` (`Form content does not match requestedSchema`), and the client can answer again. With a Pydantic model, `interrupt()` returns an instance of the model.

When the schema does not describe an object, such as `int`, the form has one `response` field, and the agent resumes with its value. When the interrupt value is not a string, the question shows it as JSON. Agent Server cannot ask an interrupt whose value is not a string and that has no `response_schema`.

Agent Server accepts form schemas that follow the MCP rules for elicitation:

* **Fields**: The schema is a flat object. Each property is a string, number, integer, boolean, single-choice enum, or multi-select array of string choices.
* **String formats**: Strings can use the `email`, `uri`, `date`, or `date-time` format.
* **Field keywords**: Each field can carry `title`, `description`, and `default`, plus `minLength`, `maxLength`, `minimum`, `maximum`, `minItems`, and `maxItems` where they apply. Agent Server cannot ask a question whose fields use other keywords, such as `pattern`, `multipleOf`, or the `exclusiveMinimum` from a Pydantic `gt`.
* **Size**: A form has 1 to 100 fields, and its schema is at most 1 MiB.
* **Pydantic schemas**: Agent Server resolves local `$defs` references, turns optional fields into plain fields, and drops titles and descriptions at the root.

When Agent Server cannot turn an interrupt into a valid question, the tool call ends with an error result whose text starts with `This tool needs input that can't be asked over MCP`.

Do not ask for passwords, API keys, access tokens, or payment credentials in a form. The MCP specification forbids it. Send the user to a page instead, as described in [Send the user to a URL](#send-the-user-to-a-url).

## Relay elicitation requests

An interrupt value whose `type` is `mcp_elicitation` carries MCP elicitation requests. Agent Server checks each request against the rules for forms and URLs, then passes it to the client. [`MCPAdapter`](https://reference.langchain.com/python/langchain/mcp/adapter/MCPAdapter) and the LangChain JavaScript MCP adapter raise this interrupt when a tool on another MCP server asks for input. An agent that uses such a tool then relays the question to its own MCP client. An agent can also raise the interrupt directly, as this `greeter` agent does:

```python
from langgraph.graph import START, StateGraph
from langgraph.types import interrupt
from typing_extensions import TypedDict


class State(TypedDict, total=False):
    greeting: str


def ask_name(state: State) -> State:
    reply = interrupt(
        {
            "type": "mcp_elicitation",
            "requests": [
                {
                    "key": "user_name",
                    "message": "What is your name?",
                    "mode": "form",
                    "requested_schema": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                        "required": ["name"],
                    },
                }
            ],
        }
    )
    answer = reply["responses"]["user_name"]
    if answer["action"] != "accept":
        return {"greeting": "Hello, stranger!"}
    return {"greeting": f"Hello, {answer['content']['name']}!"}


graph = StateGraph(State).add_node(ask_name).add_edge(START, "ask_name").compile()
```

Each entry in `requests` has these fields:

* **`key`**: Identifies the request. The answer comes back under this key.
* **`message`**: The question to show the user.
* **`mode`**: `form` or `url`.
* **`requested_schema`**: The form schema, when `mode` is `form`.
* **`url`**: The page to send the user to, when `mode` is `url`.

`requests` can also be an object that maps each key to its request, with the field names that MCP uses, such as `requestedSchema`. In that shape, a request without a `mode` is a form. The LangChain JavaScript MCP adapter uses this shape. Agent Server ignores other keys in the interrupt value, such as the `tool_name` that `MCPAdapter` adds.

The agent resumes with `{"responses": {key: answer}}`, one answer per request. Each answer has an `action` of `accept`, `decline`, or `cancel`, and an `accept` answer to a form carries its `content`. Agent Server passes declined and canceled answers to the agent, so the agent decides what happens next. In the example, a declined question returns `Hello, stranger!`.

When only one interrupt is pending, the client sees the agent's own keys. When several are pending, Agent Server prefixes each key with a digest of its interrupt, such as `<digest>.1/user_name`. Agent Server then asks two tool calls that use the same key as separate questions. The agent still receives its answers under its own keys.

### Send the user to a URL

Use `"mode": "url"` to send the user to a page, such as an OAuth consent screen, so that sensitive data never passes through the MCP client:

```python
from langgraph.graph import START, StateGraph
from langgraph.types import interrupt
from typing_extensions import TypedDict


class State(TypedDict, total=False):
    status: str


def connect_calendar(state: State) -> State:
    reply = interrupt(
        {
            "type": "mcp_elicitation",
            "requests": [
                {
                    "key": "calendar_auth",
                    "message": "Connect your calendar to continue.",
                    "mode": "url",
                    "url": "https://example.com/oauth/calendar/start",
                }
            ],
        }
    )
    if reply["responses"]["calendar_auth"]["action"] != "accept":
        return {"status": "not connected"}
    return {"status": "connected"}


graph = (
    StateGraph(State)
    .add_node(connect_calendar)
    .add_edge(START, "connect_calendar")
    .compile()
)
```

The client receives the URL in the question, and Agent Server does not open it:

```json
{
  "calendar_auth": {
    "method": "elicitation/create",
    "params": {
      "message": "Connect your calendar to continue.",
      "mode": "url",
      "url": "https://example.com/oauth/calendar/start"
    }
  }
}
```

An `accept` answer has no `content`. It confirms that the user finished the flow on that page.

Agent Server asks a URL question only when the URL meets these rules:

* **Scheme**: HTTPS, or HTTP on `localhost`, `127.0.0.1`, or `[::1]`.
* **Host**: The URL names a host.
* **Credentials**: The URL contains no user name or password.
* **Length**: The URL is at most 4,096 characters.

The client must declare the `url` mode of the `elicitation` capability. For a client that declares only `form`, the call fails with error `-32021`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32021,
    "message": "This tool asks for human input and needs url elicitation.",
    "data": {
      "requiredCapabilities": {
        "elicitation": {
          "url": {}
        }
      }
    }
  }
}
```

When a later round needs `url` mode, the call fails the same way. Agent Server then keeps the paused call for 10 minutes instead of 24 hours. In that time, the client can declare `url` and resend the same answers and `requestState` to get the URL question.

## Review tool calls

When an agent built with [`HumanInTheLoopMiddleware`](https://reference.langchain.com/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware) pauses for review, Agent Server asks one question per tool call. Both [interrupt modes](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md#set-the-interrupt-mode) work, in Python and in JavaScript: batched mode, the default, and per-call mode. Per-call mode requires `langchain>=1.4.6` with `interrupt_mode="per_call"` in Python. In JavaScript, it requires the `langchain` package 1.5.18 or later, with `interruptMode: "per_call"`.

The question's message is the middleware's description of the call, or `Run <tool>?` when the call has none. Its form has these fields:

* **`decision`**: Required. One of the decisions that the call allows, each with a title.
* **`message`**: The reason for a rejection, or the answer to send in place of the tool. Present when the call allows `reject` or `respond`.
* **`args`**: The arguments to run the tool with, as a JSON object in a string, prefilled with the arguments that the model chose. Present when the call allows `edit`.

For example, when the agent proposes `send_email` with `to` set to `ada@example.com` and `subject` set to `Launch`, the client receives this question:

```json
{
  "review-7c69d526bcc899c4.1": {
    "method": "elicitation/create",
    "params": {
      "message": "Tool execution requires approval\n\nTool: send_email\nArgs: {'to': 'ada@example.com', 'subject': 'Launch'}",
      "mode": "form",
      "requestedSchema": {
        "properties": {
          "decision": {
            "type": "string",
            "title": "Decision",
            "oneOf": [
              {
                "const": "approve",
                "title": "Approve"
              },
              {
                "const": "edit",
                "title": "Edit the arguments"
              },
              {
                "const": "reject",
                "title": "Reject"
              },
              {
                "const": "respond",
                "title": "Answer for the tool"
              }
            ]
          },
          "message": {
            "type": "string",
            "title": "Message",
            "description": "Why you reject the call, or the answer to send in its place"
          },
          "args": {
            "type": "string",
            "title": "Arguments",
            "description": "The arguments to run the tool with, as a JSON object",
            "default": "{\"to\":\"ada@example.com\",\"subject\":\"Launch\"}"
          }
        },
        "required": [
          "decision"
        ],
        "type": "object"
      }
    }
  }
}
```

Agent Server turns each answer into the middleware's decision:

| Answer | Decision |
| - | - |
| `approve` | `{"type": "approve"}` |
| `reject` | `{"type": "reject", "message": ...}`, with the message left out when it is blank |
| `respond` | `{"type": "respond", "message": ...}`. A message is required. |
| `edit` | `{"type": "edit", "edited_action": {"name": ..., "args": ...}}`, with the reviewed tool's name. In batched mode, the JavaScript middleware receives `editedAction`. |
| `decline` action | A rejection, when the call allows `reject` |

An edit can change the arguments, not the tool. A `cancel` answer, or a `decline` answer to a call that does not allow `reject`, ends the tool call with an error result.

These answers fail with error `-32602`, and the client can answer again:

* Arguments that are not a JSON object.
* A `respond` decision without a message.
* A decision that the call does not allow.

In batched mode, Agent Server checks only that edited arguments are a JSON object. The tool checks its arguments when it runs, as it does for the model's own calls.

In per-call mode, the interrupt's `response_schema` lists the decisions that the call allows and, when the tool declares them, its argument types. Agent Server checks each decision against that schema before the agent resumes. An edit that breaks the tool's argument types fails with error `-32602`, such as `The decision does not fit the tool: "subject" is a required property`, and no tool runs. Agent Server never fetches a reference in that schema. When the schema refers to a document outside itself, Agent Server asks the question without the check.

Each tool call gets its own question, even when two calls have the same tool and the same arguments. When a call's arguments are too large to prefill in a form, Agent Server asks the question without the `edit` choice. It then cannot ask about a call that allows only `edit`.

For more information on review decisions, see [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md).

## Support clients without elicitation

Clients that cannot elicit get an explicit error when a tool pauses:

* **Clients on `2026-07-28` without the `elicitation` capability**: The call fails with JSON-RPC error `-32021` (`This tool asks for human input and needs form elicitation.`) and HTTP status 400. `data.requiredCapabilities` lists every mode that the round needs, such as `{"elicitation": {"form": {}}}`. A client that declares `elicitation` with no modes supports `form`.
* **Clients on `2025-11-25` or earlier**: The tool returns an error result. Its first text block is `This tool paused to ask for human input, and this client can't answer it.`, and the second lists the pending interrupts as JSON.
* **Calls that cannot keep a thread**: The tool returns an error result whose first text block is `This tool paused to ask for human input, and this call can't be resumed.` This happens when the deployment disables threads. It also happens when your [custom auth](../Auth%20%26%20access%20control/Add%20custom%20authentication.md) handlers do not let the caller create or update the call's thread.

Agent Server cannot resume a graph that stops at a static breakpoint, set with `interrupt_before` or `interrupt_after`. For a client that can elicit, the tool call ends with an error result. Other clients receive the graph's state at the breakpoint as a normal tool result.

## Answer from a LangChain agent

An agent that calls the tool through `MCPAdapter`, from `langchain[mcp]>=1.4.0`, pauses with an `mcp_elicitation` interrupt and resumes with the user's answers. In JavaScript, `@langchain/mcp-adapters` 2.0.0 or later does the same. For the client code, see [Elicitation](https://docs.langchain.com/oss/python/langchain/mcp/tools.md#elicitation).

After each answer, the adapter calls the tool again from the start, without a `requestState`. When Agent Server asks an earlier question again, the adapter answers it with the stored answer for the same key. It sends the new `requestState` of that round. The agent behind the tool reruns up to each question, and the thread of the earlier attempt stays paused until it expires.

This replay works because Agent Server derives each key from its question. If a rerun asks a different question, the key changes and the adapter raises an error. For example, a review question changes when the model behind the tool proposes other arguments. Place questions before expensive work or side effects.

If a rerun asks no question, the tool call finishes without the stored answer, and the adapter raises no error. For example, the model behind the tool can skip the call that the user approved.

## Secure paused calls

Agent Server protects paused calls as follows:

* **Bound state**: A `requestState` works only for the agent, tool name, and arguments of the call that produced it.
* **Authorization**: Agent Server reads the paused thread as the caller, through your [custom auth](../Auth%20%26%20access%20control/Add%20custom%20authentication.md) handlers. A `requestState` from another user fails with error `-32602`.
* **Stored value**: The thread stores only a keyed hash of the token in `requestState`, so reading the thread metadata does not reveal a usable value.

## See also

* [MCP endpoint in Agent Server](MCP%20endpoint%20in%20Agent%20Server.md)
* [Human-in-the-loop using server API](Human-in-the-loop%20using%20server%20API.md)
* [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts.md)
* [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop.md)
* [Elicitation in LangChain MCP tools](https://docs.langchain.com/oss/python/langchain/mcp/tools.md#elicitation)
