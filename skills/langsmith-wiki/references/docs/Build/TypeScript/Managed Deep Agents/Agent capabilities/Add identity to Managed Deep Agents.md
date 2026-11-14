# Add identity to Managed Deep Agents

> Authenticate callers to a Managed Deep Agents deployment with a LangSmith API key, Supabase, another JWT provider, or your own backend.

Identity controls who can invoke your managed deep agent, such as apps and SDK clients that start runs or send messages.

> [!NOTE]
>
> Managed Deep Agents is in **public [beta](../../../../LangSmith%20setup/Cloud/Reference/Release%20stages.md)** on [LangSmith Cloud](../../../../LangSmith%20setup/Cloud/Cloud%20%28SaaS%29.md) and [Bring Your Own Cloud (BYOC)](../../../../LangSmith%20setup/BYOC/Bring%20Your%20Own%20Cloud%20%28BYOC%29.md). Use Managed Deep Agents CLI and SDK v0.10 or later for BYOC.

Put the identity declaration at the project root:

```text
my-agent/
  agent.ts
  identity.ts
```

For the full project layout, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

## Choose the identity provider

By default, `mda init` requires callers to present a LangSmith API key. Anyone who has that key can use the same deployment and may see the same threads. To give each signed-in end user private conversations, use Supabase, another JWT provider, or your own backend instead:

| Goal | Use |
| - | - |
| Lock down the deployment for SDK clients, scripts, and services | [LangSmith API key (default)](#configure-identity-with-a-langsmith-api-key) |
| Signed-in end users with private chats, verified by Managed Deep Agents | [Supabase](#configure-identity-with-supabase) |
| Signed-in end users from another identity provider, such as Auth0, Okta, Clerk, or Microsoft Entra ID | [Another JWT provider](#configure-identity-with-another-jwt-provider) |
| Signed-in end users with private chats, already authenticated by your own API | [Your own backend](#configure-identity-with-your-own-backend) |

Supabase, another JWT provider, and backend identity all give each end user private threads. The difference is who verifies the user. With Supabase or another JWT provider, the browser sends its access token and Managed Deep Agents verifies it. With backend identity, your API verifies the user and asserts the resulting user ID.

For more information, see [Project structure](../Get%20started/Managed%20Deep%20Agents%20project%20structure.md).

> [!NOTE]
>
> On hosted deployments, LangSmith Studio reaches the deployment through a separate workspace-authenticated path. A caller with API access to the LangSmith workspace can read and search every thread in the deployment, whichever identity provider you choose. That caller cannot modify threads owned by your end users. Per-user privacy therefore holds against your end users, not against members of your LangSmith workspace.

## Configure identity with a LangSmith API key

`mda init` scaffolds this identity provider as a secure default. Callers must present a valid LangSmith workspace API key. Managed Deep Agents verifies the key with LangSmith Cloud.

```ts identity.ts
import { auth, defineIdentity } from "managed-deepagents";

export const identity = defineIdentity({
  auth: auth.langsmithApiKey(),
});
```

Clients send the key as `x-api-key`. You do not need to add verification endpoint or tenant settings to your project `.env`. LangSmith supplies those.

> [!WARNING]
>
> Anyone with the key can reach the deployment, so treat the key as a secret. This default does not give each end user private threads. If Alice must not see Bob's threads, use [Supabase](#configure-identity-with-supabase), [another JWT provider](#configure-identity-with-another-jwt-provider), or [your own backend](#configure-identity-with-your-own-backend).

## Configure identity with Supabase

Use Supabase when a browser or another client calls the deployment as a signed-in entity. Each user gets private threads. Managed Deep Agents configures that ownership for you. For more information on the underlying LangSmith Agent Server pattern, see [Make conversations private](../../../../Deploy/Agent%20Server/Auth%20%26%20access%20control/Custom%20auth%20tutorial/Make%20conversations%20private.md).

**1. Enable auth in Supabase**

In the Supabase dashboard, enable the auth provider you will use (for example email/password).

**2. Copy the project reference**

Copy the project reference: the subdomain before `.supabase.co` in your project URL.

**3. Declare identity**

Declare identity with that project reference:

```ts identity.ts
import { auth, defineIdentity } from "managed-deepagents";

export const identity = defineIdentity({
  auth: auth.supabase({ projectRef: "your-project-ref" }),
});
```

Pass `url` instead of the project reference for a custom auth domain.

**4. Send the access token from the client**

In the client app, set the Supabase project URL and publishable key (labeled `anon` in the Supabase dashboard). Sign the user in, then send the access token on every deployment request:

```ts
await fetch(`${deploymentUrl}/threads/${threadId}/runs`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${supabaseAccessToken}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(runBody),
});
```

The publishable key (labeled `anon` in the Supabase dashboard) is only for the client to sign in with Supabase. Do not send a LangSmith API key in this mode. The Bearer token is the caller identity.

Managed Deep Agents verifies the JWT against the project's JWKS URL derived from your project reference (`https://<project-ref>.supabase.co/auth/v1/.well-known/jwks.json`).

> [!NOTE]
>
> Adding Supabase identity to an existing deployment does not add owner metadata to existing threads. Plan and test a migration before relying on identity-based access for those threads.

## Configure identity with another JWT provider

Use this option when your users sign in with an identity provider that issues JWT access tokens, such as Auth0, Okta, Clerk, or Microsoft Entra ID. Managed Deep Agents checks the token signature against the provider's public keys, then gives each user private threads.

Declare the provider with its issuer, the audience your tokens use, and the claim that identifies the user:

```ts identity.ts
import { defineIdentity } from "managed-deepagents";

export const identity = defineIdentity({
  auth: {
    issuer: "https://your-tenant.us.auth0.com/",
    audience: "https://api.example.com",
    discover: true,
    claims: { user: "sub" },
  },
});
```

* **`issuer`**: Must match the `iss` claim in the token.
* **`audience`**: Must match the `aud` claim in the token.
* **`discover`**: Finds the public keys from the provider's `/.well-known/openid-configuration`. If your provider does not publish that document, remove `discover` and set `jwks` to the URL of the public keys.
* **`claims.user`**: Names the claim to use as the user ID. Threads and stored credentials are keyed on this value. You can also set `claims.groups` and `claims.email`.

Clients send the access token as `Authorization: Bearer <access_token>`, the same as in the [Supabase example](#send-the-access-token).

Your tools and middleware can read every verified claim in the token from `principal.claims`. For an example, see [Read the runtime in tools](Managed%20Deep%20Agents%20runtime.md#read-the-runtime-in-tools).

## Configure identity with your own backend

Use backend identity when your own API already authenticates users and calls the deployment on their behalf. Your backend proves itself with a shared secret and names the caller. Managed Deep Agents trusts that name only after the secret matches, then gives each named user private threads.

The browser never reaches the deployment in this mode. Requests go from the browser to your API, and from your API to the deployment.

**1. Declare identity**

```ts identity.ts
import { defineIdentity } from "managed-deepagents";

export const identity = defineIdentity({
  auth: "backend",
});
```

**2. Generate the ingress secret**

Generate a random value and add it to the project `.env` as `MDA_INGRESS_SECRET`:

```bash
openssl rand -hex 32
```

```text .env
MDA_INGRESS_SECRET=<MDA_INGRESS_SECRET>
```

`mda deploy` forwards the value as a hosted deployment secret. A project that declares backend identity without this value fails deploy preflight before any build work, because the deployment would reject every request with 401. For how `.env` values reach a deployment, see [Deploy](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md#secrets-and-environment-files).

**3. Send both headers from your backend**

Authenticate the user in your own API, then send the secret and the resolved user ID on every deployment request:

```ts
await fetch(`${deploymentUrl}/threads/${threadId}/runs`, {
  method: "POST",
  headers: {
    "x-mda-ingress-secret": mdaIngressSecret,
    "x-mda-user-id": userId,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(runBody),
});
```

Use the same identifier for `x-mda-user-id` that your own system uses for that user, and keep it stable across sessions. Threads and stored credentials are keyed on this value, so a user who arrives under a new identifier reaches a different set of threads.

> [!WARNING]
>
> `MDA_INGRESS_SECRET` is a server-side secret. Managed Deep Agents accepts whatever `x-mda-user-id` accompanies a valid secret, so any holder of the secret can act as any user. Keep it on your backend, never in browser code, a mobile app, or a client bundle.

## Scope access by organization or tenant

Managed Deep Agents does not accept a [custom LangGraph auth handler](../../../../Deploy/Agent%20Server/Auth%20%26%20access%20control/Add%20custom%20authentication.md). Its own handler keys threads, stored credentials, and user memory on the user ID. A replacement handler would break those features.

To scope access by organization or tenant, choose the user ID based on what users must share:

* If everyone in an organization should share threads and credentials, use the organization ID as the user ID.
* If each person needs private threads, use the person's ID. Then check the organization in your backend before it calls the deployment, or read an organization claim from `principal.claims` in your tools and middleware.

## Test and deploy

Test the project locally with [`mda dev`](../Build%20and%20deploy/Managed%20Deep%20Agents%20CLI%20reference.md#develop-locally), then deploy it with [`mda deploy`](../Build%20and%20deploy/Deploy%20a%20Managed%20Deep%20Agent.md). Open deployment traces in LangSmith to inspect model calls, tool calls, errors, and latency.

Authentication failures return 401. For the LangSmith API-key default, confirm that clients send `x-api-key`. For Supabase, confirm that clients send `Authorization: Bearer <access_token>`, that `project_ref` / `projectRef` matches your Supabase project, and that callers cannot access another user's threads (403). For another JWT provider, confirm that `issuer` and `audience` match the `iss` and `aud` claims in the token, and that callers cannot access another user's threads (403). For backend identity, confirm that your API sends both `x-mda-ingress-secret` and `x-mda-user-id`, that the secret matches `MDA_INGRESS_SECRET` on the deployment, and that one user's identifier cannot reach another user's threads (403).
