# Connect a Managed Deep Agent to a custom channel over HTTP

> Start Managed Deep Agents runs from any external service that can send a webhook, and return responses through your own transport.

An HTTP channel turns a managed deep agent into an HTTP endpoint that any external service can call. Use it for a provider that Managed Deep Agents does not support directly, such as an order system, a support tool, or your own application.

You supply two callbacks: one that authenticates the request, and one that converts it into a message, naming the caller and the conversation it belongs to. Managed Deep Agents owns the trusted handoff, the agent run, and the reply. For the provider-managed alternative, see [Slack](Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md).

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

> [!NOTE]
>
> HTTP channels require `managed-deepagents>=0.8.0`.

`verify`, `parse`, and the optional `post` sit between the external service and the agent run:

![Three-row flow diagram. In the external service row, an inbound event arrives as a provider webhook, and a reply is delivered to the user by the provider. In your code row, verify checks the signature, parse extracts content and a thread ID and returns a message, and post sends the reply to the target. In the Managed Deep Agents row, the agent run executes on the thread and hands its response to post.](../../../../../../assets/images/36caabd2a638-http-channel-flow-light.png)

## Project structure

An HTTP channel declaration lives under `channels/`, like any other channel:

```text
my-agent/
  agent.ts
  channels/
    orders.ts
```

The file name becomes the channel name and the endpoint path. A project can declare more than one HTTP channel, and names must be unique. For the full project layout, see [Project structure](../../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

## Add an HTTP channel

**1. Declare the channel**

```ts channels/orders.ts
import { channels } from "managed-deepagents";

import { parse, verify } from "../lib/orders.js";

export const channel = channels.http({
  provider: "orders",
  verify,
  parse,
});
```

`provider` names the external service, and it is separate from the channel name. Managed Deep Agents sends it to Agent Auth with the caller's ID, resolving the [principal](../Add%20identity%20to%20Managed%20Deep%20Agents.md) whose credentials the run may use. The provider therefore namespaces caller IDs.

Share one provider across channels that serve the same service. Two Shopify channels, `channels/orders` and `channels/refunds`, both declaring `provider: "shopify"`, resolve the same Shopify user to one principal. A channel declaring `provider: "slack"` resolves to a different principal, even when the caller ID is identical.

Declaring the channel registers the provider, so any non-empty name works.

**2. Verify the request**

Managed Deep Agents calls `verify` first. Return `true` to continue to `parse`, or `false` to reject the request with `401`. `verify` may return a promise.

`verify` receives an `HttpChannelRequest` with a `request` and the original `rawBody` bytes. Check a signature against the bytes, not against a re-serialized body:

```ts lib/orders.ts
import { createHmac, timingSafeEqual } from "node:crypto";
import type { HttpChannelRequest } from "managed-deepagents";

export function verify({ request, rawBody }: HttpChannelRequest): boolean {
  const secret = process.env.ORDERS_WEBHOOK_SECRET;
  if (!secret) return false;
  const expected = Buffer.from(
    `sha256=${createHmac("sha256", secret).update(rawBody).digest("hex")}`,
  );
  const received = Buffer.from(request.headers.get("x-orders-signature") ?? "");
  return (
    received.length === expected.length && timingSafeEqual(received, expected)
  );
}
```

> [!WARNING]
>
> The endpoint has no platform authentication. Channel event routes authenticate inside the adapter, not through Managed Deep Agents ingress. That makes `verify` the only thing standing between the public internet and an agent run. Always check a signature or a shared secret, and never accept a request unconditionally.

Use a [deployment secret](../../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md) for the signing key. A `verify` callback that raises rejects the request with `500`.

Resolve channel credentials from the environment, not with `connections.get`, which requires a run. For credentials the agent's tools use during a run, see [Manage connections](../Manage%20connections.md).

**3. Parse the request into a message**

`parse` converts a verified request into a message that starts a run, or ignores the event. It receives the same `HttpChannelRequest` as `verify`, so request headers are available here too, and it may be asynchronous. Return one of two shapes:

* `{ type: "message", message: {...} }` starts a run.
* `{ type: "ignore" }` skips the event.

Both accept an optional `response`, a standard `Response`.

The message carries four required fields:

* **`userId`**: The caller's ID in the external service, as a string, resolved from the verified event. Agent Auth maps it to the principal whose credentials the run may use, so derive it from verified data rather than from an unauthenticated field. Convert a numeric provider ID with `String()`.
* **`threadId`**: The conversation to run in, as a UUID. Managed Deep Agents lowercases it and maps it to a durable agent thread, so the same value continues the same conversation.
* **`target`**: A JSON value that identifies the reply destination in the provider. This is separate from the agent thread UUID. Include it even when the channel only starts runs.
* **`content`**: The message text, or an array of LangChain content blocks.

> [!WARNING]
>
> `threadId` must be a UUID. Managed Deep Agents rejects any other value with `400`, so map an external conversation ID to a UUID before returning it.

Add `parse` to the `lib/orders` file that contains `verify`. Combine the imports from both examples at the top of the file, keeping only one import of `HttpChannelRequest`:

```ts lib/orders.ts
import type {
  HttpChannelParseResult,
  HttpChannelRequest,
} from "managed-deepagents";
import { orderThreadId } from "./ids.js";

export async function parse({
  request,
}: HttpChannelRequest): Promise<HttpChannelParseResult> {
  const event = await request.json();
  if (event.type !== "order.comment") {
    return { type: "ignore" };
  }
  return {
    type: "message",
    message: {
      userId: String(event.actor.id),
      threadId: orderThreadId(String(event.order.id)),
      content: event.comment.body,
      target: String(event.order.id),
    },
    rawEvent: event,
  };
}
```

Define the helper in `lib/ids.ts`. Use a fixed namespace so the same order always maps to the same UUID:

```ts lib/ids.ts
import { createHash } from "node:crypto";

const ORDERS_NAMESPACE = Buffer.from("6f0c9a3e8f1a4f5e9c2b7d4e1a2b3c4d", "hex");

export function orderThreadId(orderId: string): string {
  const bytes = createHash("sha1")
    .update(ORDERS_NAMESPACE)
    .update(orderId, "utf8")
    .digest()
    .subarray(0, 16);
  bytes[6] = (bytes[6]! & 0x0f) | 0x50;
  bytes[8] = (bytes[8]! & 0x3f) | 0x80;
  const hex = bytes.toString("hex");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}
```

Return a `response` to control what the provider receives. Managed Deep Agents sends it after the run is accepted for a message, and immediately for an ignored event. Use it to answer a provider's verification challenge without starting a run:

```ts
return {
  type: "ignore",
  response: Response.json({ challenge: event.challenge }),
};
```

**4. Send replies with post**

Add an async `post` callback to deliver the agent's final response to the external service. Omit it for a channel that only starts runs.

`post` receives one input with the verified `target` and a message. Automatic replies use `type: "content"` with a `content` field. Explicit native messages use `type: "native"` with a `native` field. Return the posted message `id` and an optional `url`.

These examples support content messages and reject native messages. The `target` is the order ID returned by `parse`.

```ts channels/orders.ts
import { channels } from "managed-deepagents";

import { parse, verify } from "../lib/orders.js";

export const channel = channels.http({
  provider: "orders",
  verify,
  parse,
  async post(input) {
    if (input.type !== "content") {
      throw new Error("This adapter supports content messages only");
    }
    const response = await fetch("https://orders.example.com/api/comments", {
      method: "POST",
      headers: {
        authorization: `Bearer ${process.env.ORDERS_API_TOKEN}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ orderId: input.target, body: input.content }),
    });
    if (!response.ok) throw new Error("Order reply failed");
    const posted = await response.json();
    return { id: String(posted.id) };
  },
});
```

Managed Deep Agents posts the reply after the run finishes, separately from the response the provider already received. Two cases produce no reply: a run that pauses on an [interrupt](../Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#respond-to-an-interrupt), and a run whose agent already delivered a final message itself. A failed `post` is logged as a delivery failure.

Add an optional async `onError(error, target)` callback to handle run or delivery failures. It replaces the default error reply. It receives the verified reply target.

## Call the endpoint

A deployed HTTP channel accepts requests at the channel name, not the provider name:

```text
POST https://<deployment-url>/channels/<name>/events
```

A declaration in `channels/orders.ts` is reachable at `/channels/orders/events`.

Your `parse` callback decodes the request body. It can read JSON, form data, text, or bytes. The examples above expect JSON.

Managed Deep Agents answers with one of these, unless `parse` returned its own `response`:

| Status | Body | Cause |
| - | - | - |
| `202` | `{"status": "accepted", "deliveryId": "..."}` | The run started. |
| `202` | `{"status": "ignored"}` | `parse` returned an ignore result. |
| `400` | `{"error": "invalid channel payload"}` | `parse` raised, for example because its decoder rejected the body. |
| `400` | `{"error": "invalid channel parse result"}` | `parse` returned an unrecognized shape. |
| `400` | `{"error": "invalid channel message"}` | The message has an invalid caller, thread UUID, content, or JSON `target`. |
| `401` | `{"error": "invalid channel signature"}` | `verify` rejected the request. |
| `500` | `{"error": "channel verification failed"}` | `verify` raised. |
| `500` | `{"error": "channel runtime is not configured"}` | The managed runtime is missing required configuration. |
| `500` | `{"error": "channel run could not be started"}` | The agent run failed to start. |

A `202` means the run was accepted, not that it finished. The agent's answer arrives later through `post`, if configured.

## Read the event in the agent

Tools and middleware read the delivery from [`runtime.thread.origin.channel`](../Managed%20Deep%20Agents%20runtime.md#channel). For the parser examples, its `provider` is `"orders"`.

Return `rawEvent` from `parse` to expose JSON provider data at `runtime.thread.origin.channel.rawEvent`. If omitted, `rawEvent` is `undefined`.

The reply `target` stays private. Code cannot read it from the channel.

Managed Deep Agents builds the channel's `event` from the parsed message. It does not decode the body again or preserve the provider event automatically.

## Deploy the agent

An HTTP channel needs no provider authorization, so deployment is the standard command. Managed Deep Agents mounts the endpoint from the declaration.

```bash npm
npx mda deploy
```

```bash pnpm
pnpm exec mda deploy
```

```bash bun
bunx mda deploy
```

Put the signing key and any reply credentials in the project `.env` so `mda deploy` forwards them as deployment secrets. Then register `https://<deployment-url>/channels/<name>/events` with the external service as its webhook target.

## Share a channel adapter as a package

A reusable channel adapter is a package that creates an HTTP channel. Publish the provider-specific code separately so other projects can install it without copying callbacks or changing the Managed Deep Agents SDK.

The package owns request verification, event parsing, and optional reply delivery. Managed Deep Agents still owns the agent run and trusted handoff.

### Package the adapter

To package the orders adapter from this guide, move `verify`, `parse`, `post`, and their helpers into the package. Keep secrets in environment variables, not in the published source. Export a factory that returns the HTTP channel declaration:

Declare `managed-deepagents` as a `peerDependencies` entry in `package.json` so the application supplies the SDK. Import only from the public `managed-deepagents` entry point. The factory returns `HttpChannel`. Use `HttpChannelAdapter` and the request, parse-result, and post-input types when typing `verify`, `parse`, and `post`.

Put the callbacks in `src/orders.ts` and export the factory from your package entry point:

```ts src/index.ts
import { channels, type HttpChannel } from "managed-deepagents";

import { parse, post, verify } from "./orders.js";

export function ordersChannel(): HttpChannel {
  return channels.http({
    provider: "orders",
    verify,
    parse,
    post,
  });
}
```

Publish compiled JavaScript and TypeScript declarations, and point the package entry points at those files. Do not bundle a separate copy of `managed-deepagents` into the adapter.

Declare the supported `managed-deepagents` versions in your package metadata. Test against those versions before publishing.

### Use the package in a project

`mda-orders` is an example package name, not a published integration. To install it as an application dependency and declare a channel under `channels/`:

```ts channels/orders.ts
import { ordersChannel } from "mda-orders";

export const channel = ordersChannel();
```

The channel file name, `channels/orders.ts`, determines the endpoint: `/channels/orders/events`.

Keep the `provider` value, `"orders"`, stable across releases because it namespaces caller identities.

### Before you publish

Test valid and invalid signatures, ignored events, conversation-to-thread mapping, and reply delivery. Document required environment variables, supported event types, and any provider limitations. Publishing an adapter does not add managed provider provisioning. Document how to create the provider app, configure credentials, and register the webhook.

For deployment secrets and webhook registration, see [Deploy the agent](#deploy-the-agent).

## See also

* [Channels overview](Connect%20Managed%20Deep%20Agents%20to%20channels.md): understand how channels connect messaging services to an agent.
* [Slack](Connect%20a%20Managed%20Deep%20Agent%20to%20Slack.md): use the provider-managed Slack channel instead.
* [Identity](../Add%20identity%20to%20Managed%20Deep%20Agents.md): authenticate callers and scope channel runs to the resolved user.
* [Deploy an agent](../../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md): configure and deploy a managed deep agent.
