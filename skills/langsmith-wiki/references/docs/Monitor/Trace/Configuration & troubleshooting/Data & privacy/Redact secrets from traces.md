# Redact secrets from traces

> Prevent API keys, tokens, and other secrets from appearing in LangSmith traces using marked secrets and the SDK anonymizer.

When your application handles API keys, tokens, or other credentials, those values can appear in LangSmith traces if they are passed as part of inputs or outputs. Use `LangSmithSecret` (Python only) to mark individual credentials, or the SDK's built-in anonymizer to detect common secret formats before upload.

> [!NOTE]
>
> This page covers redacting secrets (API keys, tokens, credentials) from trace data via the SDK. For redacting personally identifiable information (PII) such as emails, names, or SSNs, see [Prevent logging of sensitive data in traces](Prevent%20logging%20of%20sensitive%20data%20in%20traces.md). To redact secrets at the LLM Gateway layer, see [Data policies](../../../../LLM%20Gateway/Governance/Data%20policies.md).
>
> The coding agent tracing plugins for [Claude Code](../../Tracing%20setup/Integrations/Developer%20tools/Trace%20Claude%20Code%20sessions.md#secret-redaction), [OpenAI Codex](../../Tracing%20setup/Integrations/Developer%20tools/Trace%20OpenAI%20Codex%20sessions.md#secret-redaction), and [Cursor](../../Tracing%20setup/Integrations/Developer%20tools/Trace%20Cursor%20sessions.md#secret-redaction) apply the preset below by default. No SDK code is required for those.

## Mark individual secrets (Python only)

`LangSmithSecret` marks a string for redaction without changing its value in your application. Use it for credentials you can identify when loading them, including formats the built-in secret preset does not recognize. No anonymizer configuration is required.

> [!NOTE]
>
> `LangSmithSecret` requires `langsmith>=0.12.3`.

```python
import os

from langsmith import LangSmithSecret, traceable

api_key = LangSmithSecret(os.environ["VENDOR_API_KEY"])

@traceable
def call_vendor(api_key: str, prompt: str) -> str:
    return f"Response to: {prompt}"

call_vendor(api_key=api_key, prompt="hi")
```

The function receives the real credential. The LangSmith SDK replaces the marked value with `[LANGSMITH SECRET]` before uploading it:

```json
{"api_key": "[LANGSMITH SECRET]", "prompt": "hi"}
```

Masking applies to marked values in inputs, outputs, metadata, and errors, including nested containers. Operations such as `.strip()`, slicing, and concatenation preserve the marker. Unmarked copies of the same credential are not automatically redacted.

### Limitations of marked secrets

* **Masking applies only to LangSmith uploads**: Logging, `json.dumps()`, and third-party clients can read the real value. `repr()` is masked, but `.encode()` returns the real bytes.
* **String construction can remove the marker**: Expressions such as `f"Bearer {api_key}"`, `"Bearer {}".format(api_key)`, and `"".join([api_key])` produce ordinary strings. Wrap the finished value instead: `LangSmithSecret(f"Bearer {api_key}")`.
* **Pydantic models bypass masking**: LangSmith does not mask anything inside a traced Pydantic model. Pydantic serializes its own fields, and validating into a `str` field drops the marker.
* **Custom string representations can expose secrets**: A custom object's `__str__` method that interpolates a secret can expose the plaintext when LangSmith stringifies the object.
* **Secrets as dictionary keys can lose entries**: A single marked key is masked, but multiple marked keys in one dictionary collapse into one `[LANGSMITH SECRET]` key. Marked keys inside dataclasses are not masked.

Use the built-in secret preset alongside `LangSmithSecret` to detect supported credential formats in unmarked strings.

## Use the built-in secret preset

The SDK ships a curated rule set for common credential formats. Pass `create_secret_anonymizer` to the [Client](https://reference.langchain.com/python/langsmith/client/Client) constructor and it redacts detected secrets from run inputs, outputs, errors, and metadata before they are uploaded. Use it when you want coverage of well-known key formats without writing patterns yourself.

> [!NOTE]
>
> The `create_secret_anonymizer` / `createSecretAnonymizer` function requires:
>
> * Python SDK: 0.9.0 or later
> * TypeScript SDK: 0.7.11 or later

```python Python
from langsmith import Client
from langsmith.anonymizer import create_secret_anonymizer

client = Client(anonymizer=create_secret_anonymizer())
```

```typescript TypeScript
import { Client } from "langsmith";
import { createSecretAnonymizer } from "langsmith/anonymizer";

const client = new Client({ anonymizer: createSecretAnonymizer() });
```

Each match is replaced with `[SECRET_DETECTED]`. The preset traverses up to 24 nesting levels, rather than the 10 that `create_anonymizer` uses, because traced payloads nest deeply. Override it with `max_depth`.

The Python and TypeScript presets hold the same rules, so a trace redacted by one matches a trace redacted by the other.

### Rules in the preset

Provider rules are anchored to a known key prefix. Contextual rules fire only when a sensitive name is paired with an assignment, which leaves ordinary code, UUIDs, and content hashes intact.

| Category | Detected formats |
| - | - |
| Anthropic | `sk-ant-` |
| OpenAI | `sk-proj-`, `sk-svcacct-`, `sk-admin-`, and legacy `sk-` keys |
| LangSmith | `lsv2_pt_`, `lsv2_sk_`, `ls__` |
| GitHub | `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, and `github_pat_` |
| GitLab | `glpat-` |
| AWS | Access key IDs prefixed `AKIA`, `ASIA`, `ABIA`, `ACCA`, or `A3T` |
| Google | `AIza` API keys and `ya29.` OAuth access tokens |
| Slack | `xoxb-`, `xoxa-`, `xoxp-`, `xoxr-`, `xoxs-`, `xapp-`, and `hooks.slack.com` webhook URLs |
| Stripe | `sk_live_`, `sk_test_`, `rk_live_`, `rk_test_` |
| npm | `npm_` |
| PyPI | `pypi-AgEIcHlwaS` upload tokens |
| SendGrid | `SG.` |
| JSON Web Tokens | A `header.payload.signature` triple beginning `eyJ` |
| Private keys | PEM blocks for RSA, EC, OpenSSH, DSA, and PGP keys |
| Named assignments | `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD`, `PASSWD`, `PRIVATE_KEY`, `ACCESS_KEY`, `AUTH_TOKEN`, or `CLIENT_SECRET` followed by `=` or `:` and a value of six characters or more |
| Credential headers | `Authorization`, `X-Api-Key`, and `X-Auth-Token`, and a bare `Bearer <token>` |
| URL credentials | The password in `scheme://user:password@host` |

A name rule requires a component boundary, so `TOKEN` matches `api_token` and `mytoken` but not `tokenizer` or `tokens`. Header and `Bearer` rules keep the header name and the scheme word, and redact only the credential that follows.

### Add your own rules to the preset

Pass `extra_rules` to append patterns for credentials the preset does not know about, such as an internal key format. Extra rules run after the built-in ones.

```python Python
import re

from langsmith import Client
from langsmith.anonymizer import create_secret_anonymizer

anonymizer = create_secret_anonymizer(
    extra_rules=[
        {"pattern": re.compile(r"ACME-[A-Z0-9]{16}"), "replace": "[REDACTED_ACME_KEY]"},
    ]
)

client = Client(anonymizer=anonymizer)
```

```typescript TypeScript
import { Client } from "langsmith";
import { createSecretAnonymizer } from "langsmith/anonymizer";

const anonymizer = createSecretAnonymizer({
  extraRules: [
    { pattern: /ACME-[A-Z0-9]{16}/g, replace: "[REDACTED_ACME_KEY]" },
  ],
});

const client = new Client({ anonymizer });
```

A rule without a `replace` value falls back to `[redacted]`, not `[SECRET_DETECTED]`. Set `replace` when you want the two to be distinguishable in a trace.

### Limits of the preset

The preset favors precision over exhaustive coverage, which has consequences worth planning around:

* **Unrecognized formats reach LangSmith**: a credential that matches no rule, including a random high-entropy string with no surrounding context, is uploaded as is.
* **Only four fields are redacted**: the anonymizer covers `inputs`, `outputs`, `error`, and `extra.metadata`. Run names, tags, and attachments are uploaded unmodified.
* **Redaction is not access control**: a redacted trace still holds the prompts, file contents, and tool results it was built from. Restrict who can read the tracing project. To omit content rather than scrub it, see [Prevent logging of sensitive data in traces](Prevent%20logging%20of%20sensitive%20data%20in%20traces.md).

## Write custom patterns

> [!NOTE]
>
> The `create_anonymizer` / `createAnonymizer` function requires:
>
> * Python SDK: 0.1.81 or later
> * TypeScript SDK: 0.1.33 or later

When the preset does not fit, `create_anonymizer` takes a list of regex patterns and replacement strings and applies only those. Pass the resulting anonymizer to the [Client](https://reference.langchain.com/python/langsmith/client/Client) constructor, and it will automatically apply to all run inputs and outputs before they reach LangSmith.

The following example redacts common secret formats, including OpenAI API keys, generic bearer tokens, and `sk-` prefixed keys:

```python Python
from langsmith.anonymizer import create_anonymizer
from langsmith import Client, traceable

# Redact common secret patterns
anonymizer = create_anonymizer([
    # OpenAI-style keys: sk-... or sk-proj-...
    {"pattern": r"sk-[A-Za-z0-9\-_]{20,}", "replace": "<REDACTED_API_KEY>"},
    # Generic bearer tokens
    {"pattern": r"Bearer\s+[A-Za-z0-9\-_\.]{20,}", "replace": "Bearer <REDACTED_TOKEN>"},
    # Anthropic keys
    {"pattern": r"sk-ant-[A-Za-z0-9\-_]{20,}", "replace": "<REDACTED_API_KEY>"},
    # Generic high-entropy strings that look like secrets (40+ hex chars)
    {"pattern": r"\b[0-9a-fA-F]{40,}\b", "replace": "<REDACTED_TOKEN>"},
])

client = Client(anonymizer=anonymizer)

@traceable(client=client)
def call_external_api(api_key: str, prompt: str) -> str:
    # The api_key value will be redacted in the trace
    return f"Response to: {prompt}"

call_external_api(
    api_key="<SECRET>",
    prompt="What is LangSmith?",
)
```

```typescript TypeScript
import { createAnonymizer } from "langsmith/anonymizer";
import { traceable } from "langsmith/traceable";
import { Client } from "langsmith";

// Redact common secret patterns
const anonymizer = createAnonymizer([
    // OpenAI-style keys: sk-... or sk-proj-...
    { pattern: /sk-[A-Za-z0-9\-_]{20,}/g, replace: "<REDACTED_API_KEY>" },
    // Generic bearer tokens
    { pattern: /Bearer\s+[A-Za-z0-9\-_.]{20,}/g, replace: "Bearer <REDACTED_TOKEN>" },
    // Anthropic keys
    { pattern: /sk-ant-[A-Za-z0-9\-_]{20,}/g, replace: "<REDACTED_API_KEY>" },
    // Generic high-entropy strings that look like secrets (40+ hex chars)
    { pattern: /\b[0-9a-fA-F]{40,}\b/g, replace: "<REDACTED_TOKEN>" },
]);

const client = new Client({ anonymizer });

const callExternalApi = traceable(
    async (apiKey: string, prompt: string): Promise<string> => {
        // The apiKey value will be redacted in the trace
        return `Response to: ${prompt}`;
    },
    { client }
);

await callExternalApi(
    "<API_KEY>",
    "What is LangSmith?"
);
```

The anonymizer serializes inputs and outputs to JSON, applies each regex pattern, then deserializes the result before sending to LangSmith. By default, it traverses up to 10 nesting levels deep. To change this, pass the `max_depth` parameter:

```python
anonymizer = create_anonymizer(
    [{"pattern": r"sk-[A-Za-z0-9\-_]{20,}", "replace": "<REDACTED_API_KEY>"}],
    max_depth=5,
)
```

## Use a custom function

If your redaction logic is more complex, pass a function instead of a list of patterns. The function receives a string and returns the redacted string:

```python Python
import re
from langsmith.anonymizer import create_anonymizer
from langsmith import Client

# Example: redact any value that follows a known key name in JSON-like payloads
SECRET_KEYS = {"api_key", "apiKey", "token", "secret", "password", "credential"}

def redact_secret_values(text: str) -> str:
    for key in SECRET_KEYS:
        # Match patterns like: "api_key": "some-value"
        pattern = rf'("{key}"\s*:\s*)"[^"]*"'
        text = re.sub(pattern, r'\1"<REDACTED>"', text)
    return text

anonymizer = create_anonymizer(redact_secret_values)
client = Client(anonymizer=anonymizer)
```

```typescript TypeScript
import { createAnonymizer } from "langsmith/anonymizer";
import { Client } from "langsmith";

const SECRET_KEYS = new Set(["api_key", "apiKey", "token", "secret", "password", "credential"]);

function redactSecretValues(text: string): string {
    for (const key of SECRET_KEYS) {
        // Match patterns like: "api_key": "some-value"
        const pattern = new RegExp(`("${key}"\\s*:\\s*)"[^"]*"`, "g");
        text = text.replace(pattern, '$1"<REDACTED>"');
    }
    return text;
}

const anonymizer = createAnonymizer(redactSecretValues);
const client = new Client({ anonymizer });
```

## Combine with LANGSMITH\_HIDE\_INPUTS

If your use case requires completely suppressing all inputs (for example, for zero-retention compliance), use `LANGSMITH_HIDE_INPUTS=true` instead. The anonymizer is skipped when `LANGSMITH_HIDE_INPUTS` or `LANGSMITH_HIDE_OUTPUTS` is set to `true`.

For more options, including hiding all inputs and outputs, hiding metadata, function-level processors, and third-party PII libraries, see [Prevent logging of sensitive data in traces](Prevent%20logging%20of%20sensitive%20data%20in%20traces.md).
