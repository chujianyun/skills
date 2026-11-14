# Trace with Instructor

LangSmith provides a convenient integration with [Instructor](https://python.useinstructor.com/), a popular open-source library for generating structured output with LLMs.

> [!NOTE]
>
> In an [agent-based workspace](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Agent%20Registry.md), [create an agent](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md) once before sending traces. Use [agent addressing](../../../Configuration%20%26%20troubleshooting/Agent%20%26%20environment%20settings/Log%20traces%20to%20an%20agent.md) to select its identifier and environment. If an integration requires `project_name`, use the selected environment's [`tracer_session_name`](../../../../../LangSmith%20setup/Overview/Agent-based%20workspaces/Create%20an%20agent.md#use-an-environment-project) as a compatibility value.

In order to use, you first need to set your LangSmith API key.

```shell
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_AGENT_ID="<your-agent-id>"
export LANGSMITH_AGENT_ENVIRONMENT="local"
# For LangSmith API keys linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID environment variable to specify which workspace to use.
export LANGSMITH_WORKSPACE_ID=<your-workspace-id>
```

Next, you will need to install the LangSmith SDK:

```bash pip
pip install -U langsmith
```

```bash uv
uv add langsmith
```

Wrap your OpenAI client with `langsmith.wrappers.wrap_openai`

```python
from openai import OpenAI
from langsmith import wrappers

client = wrappers.wrap_openai(OpenAI())
```

After this, you can patch the wrapped OpenAI client using `instructor`:

```python
import instructor

client = instructor.patch(client)
```

Now, you can use `instructor` as you normally would, but now everything is logged to LangSmith!

```python
from pydantic import BaseModel


class UserDetail(BaseModel):
    name: str
    age: int


user = client.chat.completions.create(
    model="gpt-6-luna",
    response_model=UserDetail,
    messages=[
        {"role": "user", "content": "Extract Jason is 25 years old"},
    ]
)
```

Oftentimes, you use `instructor` inside of other functions.
You can get nested traces by using this wrapped client and decorating those functions with `@traceable`.
Please see [Custom instrumentation](../../Manual%20instrumentation/Custom%20instrumentation.md) for more information on how to annotate your code for tracing with the `@traceable` decorator.

```python {highlight={4}}
from langsmith import traceable

# You can customize the run name with the `name` keyword argument
@traceable(name="Extract User Details")
def my_function(text: str) -> UserDetail:
    return client.chat.completions.create(
        model="gpt-6-luna",
        response_model=UserDetail,
        messages=[
            {"role": "user", "content": f"Extract {text}"},
        ]
    )

my_function("Jason is 25 years old")
```
