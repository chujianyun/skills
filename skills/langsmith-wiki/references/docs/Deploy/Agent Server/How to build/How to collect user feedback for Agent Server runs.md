# How to collect user feedback for Agent Server runs

This tutorial shows you how to collect user feedback for [Agent Server](../Capabilities/Agent%20Server.md) runs and automatically link them to [traces](../../../Monitor/Trace/Observability%20concepts.md#traces) in LangSmith. When creating a run, include the keys in the `feedback_keys` field of the request body. The response will return a pre-signed URL for each key, which your client can use to collect user feedback for the Agent Server run.

LangSmith uses feedback to continuously improve the implementation of your agent. To learn more about how feedback works in LangSmith, refer to [LangSmith feedback](../../../Monitor/Trace/Observability%20concepts.md#feedback).

## How it works

1. Create a run and include `feedback_keys` in the request body. For example, when calling `POST /threads/{thread_id}/runs/stream`, set `feedback_keys` in the request body to:
   ```
   ["user_liked", "user_disliked"]
   ```
2. The `feedback` object from the response contains a pre-signed URL for each key. For example, the `feedback` object is:
   ```
   {
       "user_liked": "https://api.smith.langchain.com/api/v1/feedback/tokens/ef19fedf-dcac-4cbb-a59c-00661efd6425",
       "user_disliked": "https://api.smith.langchain.com/api/v1/feedback/tokens/e952734e-c0a0-417b-a04d-fc2209691ed5"
   }
   ```
3. Request the returned URL (e.g. `POST /api/v1/feedback/tokens/{token_id}`) to associate the feedback key with the trace generated from the Agent Server run. For more details, refer to the [LangSmith API reference](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md).
4. LangSmith associates the submitted feedback with the run using the selected feedback key (e.g. `user_liked` or `user_disliked`).

## Call the streaming run API with `feedback_keys`

Create a run and parse the `feedback` object from the response.

> [tab] Python SDK
>
> ```python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> from langgraph_sdk import get_client
>
> client = get_client(url="<DEPLOYMENT_URL>", api_key="<API_KEY>")
>
> thread = await client.threads.create()
> thread_id = thread["thread_id"]
>
> feedback_urls = {}
>
> async for event in client.runs.stream(
>     thread_id,
>     "agent",
>     input={
>         "messages": [
>             {"role": "user", "content": "Tell me a joke about databases."}
>         ]
>     },
>     stream_mode="updates",
>     feedback_keys=["user_liked", "user_disliked"],
> ):
>     if event.event == "feedback":
>         # Example: {"user_liked": ".../feedback/tokens/<id>", "user_disliked": "..."}
>         feedback_urls = event.data
>         print("Feedback URLs:", feedback_urls)
>     elif event.event == "updates":
>         print(event.data)
> ```

> [tab] JavaScript SDK
>
> ```javascript theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> import { Client } from "@langchain/langgraph-sdk";
>
> const client = new Client({ apiUrl: "<DEPLOYMENT_URL>", apiKey: "<API_KEY>" });
>
> const thread = await client.threads.create();
> const threadId = thread.thread_id;
>
> let feedbackUrls = {};
>
> const streamResponse = client.runs.stream(threadId, "agent", {
>   input: {
>     messages: [{ role: "user", content: "Tell me a joke about databases." }],
>   },
>   streamMode: "updates",
>   feedbackKeys: ["user_liked", "user_disliked"],
> });
>
> for await (const event of streamResponse) {
>   if (event.event === "feedback") {
>     // Example: { user_liked: ".../feedback/tokens/<id>", user_disliked: "..." }
>     feedbackUrls = event.data;
>     console.log("Feedback URLs:", feedbackUrls);
>   } else if (event.event === "updates") {
>     console.log(event.data);
>   }
> }
> ```

> [tab] cURL
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>   --url "<DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/stream" \
>   --header "Content-Type: application/json" \
>   --header "x-api-key: <API_KEY>" \
>   --data '{
>     "assistant_id": "agent",
>     "input": {
>       "messages": [
>         {
>           "role": "user",
>           "content": "Tell me a joke about databases."
>         }
>       ]
>     },
>     "stream_mode": "updates",
>     "feedback_keys": ["user_liked", "user_disliked"]
>   }'
> ```

## Handle the streamed `feedback` event

The stream emits a `feedback` event like the following:

```text
event: feedback
data: {"user_liked":"https://api.smith.langchain.com/api/v1/feedback/tokens/ef19fedf-dcac-4cbb-a59c-00661efd6425", "user_disliked": "https://api.smith.langchain.com/api/v1/feedback/tokens/e952734e-c0a0-417b-a04d-fc2209691ed5"}
```

Each key in `data` matches one of the values you passed in `feedback_keys`. Each value is a generated URL your client can call to submit feedback for that run.

## Submit feedback with the generated URL

When the user chooses a feedback option, `POST` to the corresponding URL. `GET` is also supported. See the [LangSmith API reference](../../../Monitor/Reference/LangSmith%20REST%20API/LangSmith%20API%20reference.md) for more details.

For example, if the user clicks a thumbs down button, call the `user_disliked` URL:

> [tab] POST
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request POST \
>   --url "https://api.smith.langchain.com/api/v1/feedback/tokens/e952734e-c0a0-417b-a04d-fc2209691ed5" \
>   --header "Content-Type: application/json" \
>   --data '{
>     "score": 1,
>     "value": 0,
>     "comment": "I didn't like this joke because it didn't make me laugh.",
>     "correction": {},
>     "metadata": {}
>   }'
> ```

> [tab] GET
>
> `metadata` is not supported with `GET`.
>
> ```bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
> curl --request GET \
>   --url "https://api.smith.langchain.com/api/v1/feedback/tokens/e952734e-c0a0-417b-a04d-fc2209691ed5?score=1&value=0&comment=I%20didn%27t%20like%20this%20joke%20because%20it%20didn%27t%20make%20me%20laugh.&correction=%7B%7D"
> ```

After this request succeeds, LangSmith records feedback on the trace using the key `user_disliked`.

## Optimize feedback data model

The `user_liked` and `user_disliked` keys can also be modeled under a single key such as `user_score`.

For example:

* Use `key="user_score"` with `score=1` for `user_liked`
* Use `key="user_score"` with `score=-1` for `user_disliked`

This can simplify analysis because all user preference signals are grouped under one feedback key.

The feedback data model is flexible and should be designed for your use case. For example, some applications may prefer separate boolean-style keys (`user_liked`, `user_disliked`), while others may prefer a single numeric score (`user_score`) or a richer rubric with multiple feedback keys.

## Productionize in a client UI

A productionized solution will expose the generated feedback URLs through your frontend instead of calling them manually.

Example high-level implementation:

1. Create the run from your backend or frontend.
2. Capture the `feedback` object and store the returned URLs.
3. Render feedback controls such as thumbs up/down buttons and feedback forms.
4. On feedback submission, `POST` or `GET` a feedback URL based on the user's feedback intent.
5. Optionally disable the feedback controls after submission and show confirmation to the user.
