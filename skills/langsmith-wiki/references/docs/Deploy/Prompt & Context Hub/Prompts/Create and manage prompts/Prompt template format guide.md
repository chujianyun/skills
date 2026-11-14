# Prompt template format guide

This page describes the [prompt template](../Prompt%20engineering%20concepts.md#prompts-vs-prompt-templates) formats supported in the [Playground](../Prompt%20engineering%20concepts.md#playground), [prompt hub](Manage%20prompts.md#public-prompt-hub), and [evaluators](../../../../Test/Get%20started/Evaluation%20concepts.md#evaluators). Prompt templates allow you to create reusable prompts with dynamic placeholders that get filled in at runtime.

> [!TIP]
>
> For a general overview of prompt engineering and prompt templates, refer to the [Concepts](../Prompt%20engineering%20concepts.md#prompts-vs-prompt-templates) page.

LangSmith supports two prompt template formats, which work for different levels of complexity:

| Format | Syntax | Best for |
| - | - | - |
| **f-string** | `{variable}` | Simple prompts with basic variable substitution |
| **mustache** | `{{variable}}` | Complex prompts with loops, conditionals, nested data, or evaluators |

[F-string syntax](#f-string-syntax) is ideal for straightforward prompts. [Mustache](#mustache-syntax) provides features for handling complex data structures and logic, which is helpful for evaluators and advanced use cases.

You can switch between formats in the [UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-prompt-template-format). LangSmith will automatically [convert your template](#conversion-between-formats) when possible, though some mustache features (like loops and conditionals) cannot be converted to f-string format.

Use the [Playground](https://smith.langchain.com/playground) to test out the examples on this page. Switch the **Prompt format** under the prompt settings  menu in the Playground.

## F-string syntax

F-string templates use Python-style formatting with single curly braces `{variable}`. LangSmith uses a [simplified subset](#limitations) of Python's [f-string syntax](https://realpython.com/python-f-strings/): it only supports basic variable substitution, not the full range of Python expressions and formatting options. When you have a flat data structure and only need to insert values into your prompt, f-strings are ideal.

### Basic variables

Variables are replaced with their values from the input data. Variable names must match exactly (case-sensitive):

```python
# Template
Hello, {name}! Welcome to {company}.

# Input
{
  "name": "Ashley",
  "company": "LangChain"
}

# Output
Hello, Ashley! Welcome to LangChain.
```

When the template runs, LangSmith looks up each variable name in the input object and replaces `{name}` with the value of the `name` key.

### Variable names

F-string variable names are treated as simple string identifiers. They cannot contain dots, brackets, or special characters—just alphanumeric characters and underscores.

```python
# Template
Hello, {name}!
Your topic is: {topic}

# Input
{
  "name": "Ashley",
  "topic": "LangSmith"
}

# Output
Hello, Ashley!
Your topic is: LangSmith
```

If your input has nested objects like `{"user": {"name": "Ashley"}}`, you **cannot** access the nested value with `{user.name}` in f-string format. The dot would be treated as part of the variable name (literally looking for a key called `"user.name"`), not as a path separator. For nested access, use [mustache format](#mustache-syntax) instead.

### Literal braces

Sometimes you need to include actual curly braces in your output (for example, in JSON examples or code snippets). To do this, **double the braces**:

```python
# Template
Use double braces for literals: {{not_a_variable}}
But single braces for variables: {variable}

# Input
{
  "variable": "value"
}

# Output
Use double braces for literals: {not_a_variable}
But single braces for variables: value
```

The template parser recognizes `{{` as an escaped brace, not a variable placeholder. Only single braces `{...}` are treated as variables.

### Limitations

LangSmith's f-string implementation is limited to keep templates simple and predictable. The following features are **not supported**:

* **Dot notation for nested access:** Cannot use `{user.name}` to access nested objects. The entire string `"user.name"` would be treated as a single variable name.
* **Format specifiers:** Cannot use `{price:.2f}` for number formatting or `{rate:.1%}` for percentages.
* **Expressions:** Cannot use `{x + y}`, `{len(items)}`, or `{value if condition else default}`.
* **Function calls:** Cannot use `{str.upper()}` or other method calls.
* **Loops or conditionals:** No control flow structures.
* **Array indexing:** Cannot use `{items[0]}` to access array elements.

For any of these advanced features, **use mustache format instead**.

## Mustache syntax

[Mustache](https://mustache.github.io/mustache.5.html) is a "logic-less" templating language, meaning it doesn't allow arbitrary code execution but does provide structured control flow through sections. It's called "logic-less" because you can't write complex expressions—instead, you structure your data to control what renders.

Mustache is designed for complex data structures and dynamic rendering. It's essential for:

* **Evaluators:** Processing thread histories and conversation context.
* **Few-shot prompting:** Iterating over example lists.
* **Nested data:** Accessing deeply nested objects and arrays.
* **Conditional content:** Showing different text based on data presence.

The double-brace syntax `{{variable}}` distinguishes it from f-strings.

### Basic variables

Like f-strings, mustache replaces variables with their values:

```mustache
{{!-- Template --}}
Hello, {{name}}! Welcome to {{company}}.

{{!-- Input --}}
{
  "name": "Ashley",
  "company": "LangChain"
}

{{!-- Output --}}
Hello, Ashley! Welcome to LangChain.
```

> [!NOTE]
>
> `{{!-- ... --}}` is a mustache comment and won't appear in the output. Refer to the [Comments](#comments) section.

### Nested object access

You can traverse nested objects using dot notation:

```mustache
{{!-- Template --}}
User: {{user.name}}
Email: {{user.profile.email}}

{{!-- Input --}}
{
  "user": {
    "name": "Billy",
    "profile": {
      "email": "billy@example.com"
    }
  }
}

{{!-- Output --}}
User: Billy
Email: billy@example.com
```

The template engine follows the path `user` → `profile` → `email` through your data structure. Each dot represents one level of nesting.

Real-world data is often nested (for example: API responses, database records, etc.). Mustache lets you work with this data naturally without flattening it first.

### Sections

Sections are mustache's core feature. A section starts with `{{#name}}` and ends with `{{/name}}`. What happens inside depends on the value:

* **Array:** Repeats the content for each element.
* **Object:** Renders once with that object as context.
* **Truthy value:** Renders once.
* **Falsy value (false, null, undefined, empty array):** Doesn't render.

In the following example, the section `{{#items}}` iterates over the `items` array. For each iteration, the variables inside the section (like `{{name}}` and `{{price}}`) are resolved against the current array element:

```mustache
{{!-- Template --}}
Shopping List:
{{#items}}
  - {{name}}: ${{price}}
{{/items}}

{{!-- Input --}}
{
  "items": [
    {"name": "Apple", "price": "1.50"},
    {"name": "Banana", "price": "0.75"},
    {"name": "Orange", "price": "2.00"}
  ]
}

{{!-- Output --}}
Shopping List:
  - Apple: $1.50
  - Banana: $0.75
  - Orange: $2.00
```

Sections eliminate the need to manually construct repetitive text. In evaluators, you'll use sections to iterate over conversation messages or [few-shot examples](#few-shot-examples).

For deeply nested hierarchical data, you can nest multiple sections to handle complex structures with multiple levels of arrays and objects:

```mustache
{{!-- Template --}}
{{#company}}
Company: {{name}}
{{#departments}}
  Department: {{dept_name}}
  {{#employees}}
    - {{employee_name}} ({{role}})
  {{/employees}}
{{/departments}}
{{/company}}

{{!-- Input --}}
{
  "company": {
    "name": "TechCorp",
    "departments": [
      {
        "dept_name": "Engineering",
        "employees": [
          {"employee_name": "Ashley", "role": "Senior Engineer"},
          {"employee_name": "Billy", "role": "Engineer"}
        ]
      },
      {
        "dept_name": "Sales",
        "employees": [
          {"employee_name": "Carol", "role": "Sales Manager"}
        ]
      }
    ]
  }
}

{{!-- Output --}}
Company: TechCorp
  Department: Engineering
    - Ashley (Senior Engineer)
    - Billy (Engineer)
  Department: Sales
    - Carol (Sales Manager)
```

> [!TIP]
>
> You can create a structure as deep as you need, but consider flattening very deep structures before templating for readability. This approach is useful for nested categories, conversation threads with metadata, or any hierarchical data representation.

### Nested loops

You can nest sections to handle multi-level data structures:

```mustache
{{!-- Template --}}
{{#categories}}
Category: {{name}}
{{#products}}
  - {{title}} ({{price}})
{{/products}}
{{/categories}}

{{!-- Input --}}
{
  "categories": [
    {
      "name": "Fruits",
      "products": [
        {"title": "Apple", "price": "$1.50"},
        {"title": "Banana", "price": "$0.75"}
      ]
    },
    {
      "name": "Vegetables",
      "products": [
        {"title": "Carrot", "price": "$0.50"},
        {"title": "Lettuce", "price": "$1.25"}
      ]
    }
  ]
}

{{!-- Output --}}
Category: Fruits
  - Apple ($1.50)
  - Banana ($0.75)
Category: Vegetables
  - Carrot ($0.50)
  - Lettuce ($1.25)
```

The outer section `{{#categories}}` sets the context to each category object. Inside that context, `{{name}}` refers to the category name, and the inner section `{{#products}}` iterates over that category's products.

Use nested loops when your data has hierarchical relationships—categories with products, departments with employees, or conversation threads with multiple exchanges.

### Array elements by index

Sometimes you need a specific element rather than looping. Use dot notation with numeric indices:

```mustache
{{!-- Template --}}
First item: {{items.0}}
Second item: {{items.1}}
Last item: {{items.2}}

{{!-- Input --}}
{
  "items": ["Apple", "Banana", "Orange"]
}

{{!-- Output --}}
First item: Apple
Second item: Banana
Last item: Orange
```

You must know the index when you're writing the template.

Evaluators often need the first user message or last AI response from a conversation thread. Use `{{all_messages.0}}` for the first message or pre-calculate the last message in your data.

### Conditionals

You can use sections as conditionals. They only render if the value exists, is non-empty, and is not `false`:

```mustache
{{!-- Template --}}
{{#user}}
Welcome back, {{name}}!
{{/user}}

{{!-- Input (user exists) --}}
{
  "user": {
    "name": "Ashley"
  }
}

{{!-- Output --}}
Welcome back, Ashley!

{{!-- Input (no user) --}}
{}

{{!-- Output --}}
(empty - section doesn't render)
```

The section `{{#user}}` checks if `user` exists and is truthy. If so, it renders the content inside with `user` as the context (so `{{name}}` looks for `name` inside `user`).

Show optional content like "Welcome back" messages only when user data is available, or display error messages only when errors exist.

### Inverted sections

Inverted sections render only when a value doesn’t exist, is false, null, undefined, or an empty array. Inverted sections are commonly used to handle empty states, such as missing data or empty lists.

In the following example:

* `{{#results}}` iterates over each result and renders one line per item.
* `{{^results}}` renders only when the results array is empty or missing.
* The inverted section provides a clear fallback when there are no results to display.

```mustache
{{!-- Template --}}
Search results for "{{query}}":

{{#results}}
  - {{title}} ({{year}})
{{/results}}

{{^results}}
No results found. Try a different search term.
{{/results}}

{{!-- Input (with results)--}}
{
  "query": "matrix",
  "results": [
    {"title": "The Matrix", "year": 1999},
    {"title": "The Matrix Reloaded", "year": 2003}
  ]
}

{{!-- Output --}}
Search results for "matrix":

  - The Matrix (1999)
  - The Matrix Reloaded (2003)

{{!-- Input (no results) --}}
{
    "query": "asdlkjasd",
    "results": []
}

{{!-- Output --}}
Search results for "asdlkjasd":

No results found. Try a different search term.
```

You can also combine regular and inverted sections to create if/else logic, providing default values when variables are missing.

The regular section `{{#username}}` renders only if `username` exists. The inverted section `{{^username}}` renders only if it doesn't. Together, they create an if/else branch. This is useful for personalizing prompts when user data is optional or showing default instructions when custom ones aren't provided:

```mustache
{{!-- Template --}}
{{#username}}
Hello, {{username}}!
{{/username}}
{{^username}}
Hello, Guest!
{{/username}}

{{!-- Input (with username) --}}
{"username": "Ashley"}
{{!-- Output: Hello, Ashley! --}}

{{!-- Input (no username) --}}
{}
{{!-- Output: Hello, Guest! --}}
```

This pattern extends to boolean flags, allowing you to change output formatting based on data conditions:

```mustache
{{!-- Template --}}
Status: {{status}}
{{#is_urgent}}
⚠️ URGENT - Immediate attention required!
{{/is_urgent}}
{{^is_urgent}}
Standard priority
{{/is_urgent}}

{{!-- Input --}}
{
  "status": "Open",
  "is_urgent": true
}

{{!-- Output --}}
Status: Open
⚠️ URGENT - Immediate attention required!
```

Use boolean flags in your data to control which content blocks render. This keeps formatting logic out of your application code and in the template instead. This approach is useful for highlighting important information, adjusting tone based on context (formal vs. casual), or showing different instructions for different user types.

### Comments

Comments document your templates without affecting output. Use `{{! comment }}` or `{{!-- comment --}}`:

```mustache
{{!-- Template --}}
Hello, {{name}}!
{{! This is a comment and won't appear in output }}
Welcome to our service.

{{!-- Input --}}
{
  "name": "Ashley"
}

{{!-- Output --}}
Hello, Ashley!
Welcome to our service.
```

Use comments to explain complex sections, document expected data structures, or note why certain logic exists. This helps collaborators understand your templates.

## Special variables for evaluators and threads

When building [evaluators](../../../../Test/Get%20started/Evaluation%20concepts.md#evaluators) or working with conversational AI, LangSmith automatically provides special variables that structure conversation data in useful ways. These variables are **only available in evaluator contexts**, not in regular Playground prompts.

Evaluators need to analyze conversations holistically—looking at patterns across multiple messages, comparing the first question to the final answer, or examining how well the AI responds to follow-up questions. These variables make it easy to access conversation structure without manual data manipulation.

### Thread message variables

LangSmith provides four pre-structured views of a conversation: three over a [thread](../../../../Test/Get%20started/Evaluation%20concepts.md#threads) and one over a [trajectory](../../../../Monitor/Trace/Observability%20concepts.md#trajectories).

```mustache
{{!-- Access all messages in the thread --}}
{{#all_messages}}
{{role}}: {{content}}
{{/all_messages}}

{{!-- Access human-AI message pairs --}}
{{#human_ai_pairs}}
Human: {{human}}
AI: {{ai}}
{{/human_ai_pairs}}

{{!-- Access first human and last AI message --}}
{{#first_human_last_ai}}
Original question: {{first_human}}
Final answer: {{last_ai}}
{{/first_human_last_ai}}

{{!-- Access specific message by index --}}
First message: {{all_messages.0}}
Second message: {{all_messages.1}}

{{!-- Access the trajectory of the session --}}
{{trajectory}}
```

* **`all_messages`**: Every message in chronological order with `role` (user/assistant/system) and `content` fields. Use this to show the full conversation flow.
* **`human_ai_pairs`**: Messages grouped into question-answer pairs. Each pair has `human` (user message) and `ai` (assistant response). Use this when evaluating response quality.
* **`first_human_last_ai`**: Just the initial question (`first_human`) and final answer (`last_ai`). Use this to check if the AI ultimately answered the original question, ignoring the middle conversation.
* **`trajectory`**: Every message in the session as a flat, deduplicated list, including tool calls and tool results. Each message has a `role` of `human`, `ai`, `system`, or `tool`, and a `content` field holding either a string or a list of content blocks such as `text`, `reasoning`, and `tool_call`. Use this to evaluate the path an agent took.

> [!NOTE]
>
> `trajectory` is mutually exclusive with the thread variables. A prompt uses either `trajectory` or `all_messages`, `human_ai_pairs`, and `first_human_last_ai`. For how that rule is enforced and how to use `trajectory` in a thread evaluator, see [Evaluate trajectories](../../../../Monitor/Observe/Online%20evaluators/Set%20up%20multi-turn%20online%20evaluators.md#evaluate-trajectories).

### Example with thread context

The following example is a practical evaluator prompt that uses thread context:

```mustache
{{!-- Template --}}
Evaluate this conversation:

{{#all_messages}}
{{role}}: {{content}}
{{/all_messages}}

Was the AI helpful? Rate from 1-5.

{{!-- Input (provided by LangSmith) --}}
{
  "all_messages": [
    {"role": "user", "content": "What's the weather?"},
    {"role": "assistant", "content": "I don't have access to weather data."},
    {"role": "user", "content": "Can you tell me a joke instead?"},
    {"role": "assistant", "content": "Why did the chicken cross the road?"}
  ]
}

{{!-- Output --}}
Evaluate this conversation:

user: What's the weather?
assistant: I don't have access to weather data.
user: Can you tell me a joke instead?
assistant: Why did the chicken cross the road?

Was the AI helpful? Rate from 1-5.
```

The template uses the mustache section `{{#all_messages}}` to loop over the conversation array. For each iteration, the section sets the context to that message object, so `{{role}}` and `{{content}}` access the properties of the current message. The loop automatically iterates through all four messages in order, displaying each as `"role: content"`. This gives the evaluator LLM the full conversation history to assess helpfulness.

When you create an evaluator in LangSmith, select which thread variables you want to include. LangSmith will automatically populate them from the conversation being evaluated.

### Example with trajectory context

The following example is a practical evaluator prompt that uses trajectory context:

```mustache
{{!-- Template --}}
Evaluate the path this agent took:

<trajectory>
{{trajectory}}
</trajectory>

Did the agent call the right tools to answer the question? Rate from 1-5.

{{!-- Input (provided by LangSmith) --}}
{
  "trajectory": [
    {
      "content": [{"type": "text", "text": "Is my GitHub CLI authenticated?"}],
      "role": "human",
      "id": "01a04b29-ab54-763b-89ba-1f3dd2266c54"
    },
    {
      "content": [
        {
          "type": "tool_call",
          "id": "call_wQO8IHBPu6HyXoZ1Q3UqvxIs",
          "name": "execute",
          "args": {"command": "gh auth status", "timeout": 30}
        }
      ],
      "role": "ai"
    },
    {
      "content": "Logged in to github.com account octocat",
      "role": "tool",
      "tool_call_id": "call_wQO8IHBPu6HyXoZ1Q3UqvxIs"
    },
    {
      "content": [{"type": "text", "text": "Yes, you are logged in as octocat."}],
      "role": "ai"
    }
  ]
}
```

Unlike the thread variables, `trajectory` resolves to the trajectory built from the model and tool calls inside each trace, so the evaluator can score the path an agent took in more detail. Reference the variable directly as `{{trajectory}}`, or loop over the messages with the mustache section `{{#trajectory}}{{role}}{{/trajectory}}` to control what the judge receives.

## Few-shot examples

Few-shot prompting teaches the LLM by example. You provide several input-output pairs demonstrating the task, then ask it to perform the same task on new input.

[Few-shot examples](../../../../Test/Evaluators/Improve%20evaluators/How%20to%20improve%20your%20evaluator%20with%20few-shot%20examples.md#how-few-shot-examples-work) help the LLM understand:

* **Format expectations** (e.g., "respond with JSON" or "use this tone")
* **Edge cases** (e.g., how to handle ambiguous input)
* **Task nuances** (e.g., the difference between "positive" and "very positive" sentiment)

It is especially useful for classification, formatting, and stylistic tasks where showing is clearer than telling.

### Few-shot placeholder

In LangSmith, use the `{{few_shot_examples}}` placeholder where you want your examples to appear:

```mustache
{{!-- Template --}}
You are a sentiment classifier.

{{few_shot_examples}}

Now classify this text:
Text: {{text}}
Sentiment:
```

When you enable few-shot examples in the [LangSmith UI](https://smith.langchain.com?utm_source=docs&utm_medium=cta&utm_campaign=langsmith-signup&utm_content=langsmith-prompt-template-format) (in evaluators or Prompt Hub), you configure the example format separately. LangSmith automatically injects those formatted examples wherever you place the `{{few_shot_examples}}` placeholder. This keeps your prompt template clean and lets you manage examples independently.

**Example output with configured examples:**

```
You are a sentiment classifier.

Text: I love this!
Sentiment: positive
Text: This is terrible.
Sentiment: negative
Text: It's okay.
Sentiment: neutral

Now classify this text:
Text: This is amazing!
Sentiment:
```

Configure your few-shot examples in the LangSmith UI to match the format you use for the actual task. This consistency helps the LLM generalize correctly. The placeholder approach separates prompt structure from example data, making both easier to maintain.

## Conversion between formats

**F-string to mustache** always works for basic variables. Format specifiers are converted, but the formatting is removed.

**Mustache to f-string** only works for basic variables. Mustache features like dot notation, sections, conditionals, and comments have no equivalent in f-strings and cannot be converted:

* **Dot notation:** `{{user.name}}` F-strings would treat `"user.name"` as a single variable name rather than nested access.
* **Sections/loops:** `{{#items}}...{{/items}}` No equivalent in f-strings.
* **Conditionals:** `{{#value}}...{{/value}}` No equivalent in f-strings.
* **Inverted sections:** `{{^value}}...{{/value}}` No equivalent in f-strings.
* **Comments:** `{{! comment }}` No equivalent in f-strings.

If you try to convert a mustache template with these features, LangSmith will either refuse the conversion or convert only the simple parts, breaking the template's functionality. Always preview after conversion.

## Additional resources

* **[LangSmith Prompt Engineering Concepts](../Prompt%20engineering%20concepts.md)**: Higher-level guidance on effective prompting strategies.
* **[Mustache Manual](https://mustache.github.io/mustache.5.html)**: Full mustache specification with all features.
* **[Python f-string Documentation](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)**: Official Python f-string syntax (note: LangSmith uses a simplified subset).
