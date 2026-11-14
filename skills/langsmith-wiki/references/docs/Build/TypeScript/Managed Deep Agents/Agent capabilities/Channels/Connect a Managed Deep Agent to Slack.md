# Connect a Managed Deep Agent to Slack

> Start Managed Deep Agents runs from Slack messages and send responses to Slack conversations.

A Slack channel lets people invoke a managed deep agent through app mentions, direct messages, and replies in an active Slack thread. Managed Deep Agents verifies Slack events, maps each conversation to a thread, runs the agent as the resolved caller, and posts the response back to Slack.

Managed Deep Agents creates and configures the resources that connect Slack to the deployed agent. Add a channel declaration to the agent project, then deploy.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

## Project structure

```text
my-agent/
  agent.ts
  channels/
    slack.ts
```

## Add a Slack channel

A managed deep agent deployment supports one Slack channel.

The channel declaration lives at `channels/slack.ts`.

To include Slack when you create a project, pass `--channel slack`:

```bash npm
npx managed-deepagents init my-agent --channel slack
```

```bash pnpm
pnpm dlx managed-deepagents init my-agent --channel slack
```

```bash bun
bunx managed-deepagents init my-agent --channel slack
```

To add Slack to an existing project, run the channel initialization command from the project root:

```bash npm
npx mda channels init slack
```

```bash pnpm
pnpm exec mda channels init slack
```

```bash bun
bunx mda channels init slack
```

```ts channels/slack.ts
import { channels } from "managed-deepagents";

export const channel = channels.slack();
```

## Configure your agent's appearance in Slack

Edit the channel declaration to control how the agent appears in Slack.

**name** `string`

The agent name in Slack. The name must contain 1–35 characters and can contain letters, numbers, spaces, underscores, dashes, and periods. It cannot start or end with a space or dash.

**description** `string`

A description of what the agent does. The description can contain up to 139 characters.

**icon** `string`

A path to the agent icon shown in Slack, relative to the `channels/` directory. The icon must be a 512 by 512 pixel PNG file no larger than 1 MB. If you omit this parameter, Managed Deep Agents will generate an icon for you.

**backgroundColor** `string`

The background color behind the agent icon as a six-digit hexadecimal color, such as `#1d4ed8`.

For example, put an icon next to the channel declaration:

```text
my-agent/
  agent.ts
  channels/
    slack.ts
    support-agent.png
```

```ts channels/slack.ts
import { channels } from "managed-deepagents";

export const channel = channels.slack({
  name: "Support Agent",
  description: "Answers customer questions about orders and returns",
  icon: "support-agent.png",
  backgroundColor: "#1d4ed8",
});
```

### Configure which messages start runs

**triggerOnAllMessages** `boolean` (default: false)

Whether every new channel message can start an agent run. When `false`, channel messages start runs only when they mention the agent; direct messages still start runs.

**allowBotTriggers** `boolean` (default: false)

Whether messages from other Slack bots can start agent runs.

## React to the message that starts a run

When a run picks up an inbound message, the agent reacts to it with an emoji, so
the sender knows it was seen before the agent has anything to say. The reaction
never blocks or delays the reply.

Every message gets the same emoji by default. Pass a function to choose one per
message:

**reactions** `false | string | function` (default: "eyes")

Pass `false` to turn reactions off, a Slack emoji short name to use that emoji
instead, or a function taking `{ text }` and returning a short name. The
function may return a promise.

```typescript
import { channels } from "managed-deepagents";

export const channel = channels.slack({
  name: "Support Bot",
  reactions: ({ text }) => (text.includes("broken") ? "bug" : "eyes"),
});
```

Return a Slack short name without the surrounding colons. A name Slack does not
recognize is chosen but never appears, so the reaction is simply missing. A
chooser that throws, that takes longer than five seconds, or that returns
anything else falls back to the default emoji, and the run continues either way.

### Choose the emoji with a decision model

A [decision model](../../../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md) scores a fixed set of
options and answers with one of their keys, so the reaction reflects what the
message says and there is no reply to parse. The answer is always one of the
options you supplied. `TypeSafeClassifier`
([Python](https://docs.langchain.com/oss/python/integrations/providers/typesafe),
[JavaScript](https://docs.langchain.com/oss/javascript/integrations/providers/typesafe)) exposes this as a
`Runnable`, and records traces and token usage in LangSmith.

```bash
npm install @langchain/typesafe
```

```typescript
import { TypeSafeClassifier } from "@langchain/typesafe";
import { channels } from "managed-deepagents";

// The description is what the model matches on, so describe the situation
// rather than the picture. Keep an option for anything unremarkable.
const VOCABULARY = {
  bug: "A defect or incorrect behaviour.",
  rotating_light: "A declared incident or outage.",
  mag: "A code review, pull request, or diff to look at.",
  hourglass: "Waiting on someone or something else; blocked.",
  speech_balloon: "A question, or a request to explain something.",
  wave: "A greeting or hello.",
  eyes: "Anything that does not clearly fit another option.",
};

let cached: TypeSafeClassifier | undefined;
const classifier = () =>
  (cached ??= new TypeSafeClassifier({
    model: "typesafe/jev-latest",
    timeout: 5_000,
  }));

export const channel = channels.slack({
  name: "Support Bot",
  reactions: async ({ text }) => {
    const response = await classifier().invoke({
      state: text.slice(0, 2000),
      questions: {
        emoji: {
          type: "choice",
          instructions: "Which emoji best acknowledges this message?",
          criteria: VOCABULARY,
        },
      },
    });
    const emoji = response.choices.emoji;
    // Below this the model has no real view, so prefer a generic reaction.
    return emoji.confidence >= 0.25 ? emoji.choice : "eyes";
  },
});
```

Both build the classifier on first use rather than at import, because
deployment imports this module to read the channel declaration and the
classifier needs a key to construct.

Set `TYPESAFE_API_KEY` on the deployment. To route through the LLM Gateway
instead, set `TYPESAFE_BASE_URL=https://gateway.smith.langchain.com` and use a
workspace-scoped LangSmith API key, with `TYPESAFE_API_KEY` in your workspace
[provider secrets](../../../../../LLM%20Gateway/Authentication/Provider%20authentication.md#add-a-provider-key).

## Deploy the agent

During deployment, Managed Deep Agents provisions your agent in Slack from the channel declaration.

**1. Deploy your agent**

Run the deployment command from the project root:

```bash npm
npx mda deploy
```

```bash pnpm
pnpm exec mda deploy
```

```bash bun
bunx mda deploy
```

Managed Deep Agents deploys the agent and sets up the resources it needs to appear in Slack.

**2. Authorize Slack if prompted**

If you haven't authorized LangSmith before, the CLI displays an HTTPS authorization link. Open the link, select the Slack workspace, and approve the requested access.

Return to the terminal and press Enter. The CLI checks the authorization again and continues provisioning. If the Slack workspace requires admin approval, complete that approval before continuing.

**3. Use the agent in Slack**

After the first deployment, your agent sends you a direct message in Slack. Reply to the message to start an agent run. The final response appears in the Slack conversation.

> [!NOTE]
>
> Human-in-the-loop requests in Slack support only the `approve` and `reject` [decision types](../Add%20custom%20tools%20to%20Managed%20Deep%20Agents.md#human-in-the-loop).

If Slack is already authorized, deployment completes without an authorization prompt.

After you change the agent's name, description, icon, or background color in the Slack channel declaration, redeploy the agent to apply the changes in Slack.

## Exchange files with Slack

A Slack channel moves files in both directions. Uploads land in the agent's sandbox under `/workspace/attachments/`, and the agent sends a file back by calling `attach_file` with a path under `/workspace`. Declaring a Slack channel and a [sandbox](../Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md) is the whole setup.

> [!NOTE]
>
> Slack file transfer requires `managed-deepagents>=0.8.0` and a sandbox. Without a sandbox, incoming files are not saved and `attach_file` is not offered to the model.

Managed Deep Agents stages the files on the incoming message before the run, along with files shared earlier in the same Slack thread. The agent reads an attachment status message for the paths, then opens the files with its sandbox tools. That status and the file contents are labeled as data, not instructions.

Attachment is never automatic, so state in the agent's [instructions](../Add%20instructions%20to%20Managed%20Deep%20Agents.md) when a file belongs in the reply:

```markdown instructions.md
When someone asks for a report, write the report to a file under `/workspace`,
then call `attach_file` with that path so the file arrives in Slack.
```

Files stay scoped to the Slack thread they arrived in, because every thread gets its own sandbox. A direct message and a channel thread never share attachments. Within one thread, anyone reaches the files anyone else uploaded, since transfers use the bot's Slack access rather than the caller's.

### Review transfer limits

* **File size**: 200 MiB in each direction.
* **Paths**: `attach_file` accepts paths under `/workspace` only.
* **Thread history**: the scan covers recent messages in the thread. When it falls short, the attachment status reports that earlier files may be missing.
* **Skipped files**: files stored outside Slack, and files deleted from Slack.
* **Slack scopes**: a transfer blocked by a missing `files:read`, `files:write`, or history scope reports that you need to reconnect Slack.

## See also

* [Channels overview](Connect%20Managed%20Deep%20Agents%20to%20channels.md): understand how channels connect messaging services to an agent.
* [Design agent template](../../Templates/Deploy%20the%20open-source%20design%20agent.md): deploy a full Slack design agent project.
* [Paid media agent template](../../Templates/Deploy%20the%20open-source%20paid%20media%20agent.md): deploy a full Slack paid media agent project.
* [Decision models](../../../../../LLM%20Gateway/Call%20the%20gateway/Decision%20models.md): configure the model that scores reaction emoji.
* [Set up the LLM Gateway](../../../../../LLM%20Gateway/Get%20started/Set%20up%20the%20LLM%20Gateway.md): add the provider key that reactions need.
* [Agent-owned interrupts](Prompt%20Slack%20users%20with%20agent-owned%20interrupts.md): post a Slack form from a tool and resume the run on submit.
* [Sandboxes](../Add%20a%20sandbox%20to%20Managed%20Deep%20Agents.md): give the agent the filesystem that file transfers read and write.
* [Deploy an agent](../../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md): configure and deploy a managed deep agent.
* [CLI reference](../../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md): review Managed Deep Agents commands and flags.
