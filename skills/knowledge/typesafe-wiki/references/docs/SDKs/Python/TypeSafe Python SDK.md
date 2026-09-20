# TypeSafe Python SDK

> Install the TypeSafe Python SDK and get started with asynchronous or synchronous API calls.

<a id="typesafe-python-sdk" />

Browse the [Python SDK source on GitHub](https://github.com/typesafe-ai/typesafe-sdk-python).

Asynchronous and synchronous Python clients for the [TypeSafe](https://typesafe.ai) API. Learn how to use TypeSafe [here](https://docs.typesafe.ai/).

### Quickstart

1. Install the SDK:



**uv**

       ```sh
       uv add typesafe-sdk
       ```



**pip**

       ```sh
       pip install typesafe-sdk
       ```


2. Set `TYPESAFE_API_KEY` in your environment (create it [here](https://console.typesafe.ai/))
3. Call the System One API:



**Async**

       With [AsyncTypeSafeClient](API/Clients/Async client.md):

       ```python
       from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score

       async def main() -> None:
           async with AsyncTypeSafeClient() as client:
               response = await client.system_one(
                   state={"document": "I was charged twice. Please fix this ASAP."},
                   questions={
                       "billing": Noul(instructions="Is this ticket about billing?"),
                       "tone": Choice(
                           instructions="What is the customer's tone?",
                           criteria={"calm": None, "frustrated": None, "angry": None},
                       ),
                       "urgency": Score(
                           instructions="How urgent is this ticket?",
                           criteria=["can wait", "this week", "today"],
                       ),
                   },
               )

           print(response.nouls["billing"].noul)
           print(response.choices["tone"].choice)
           print(response.scores["urgency"].score)
       ```



**Sync**

       With [TypeSafeClient](API/Clients/Sync client.md):

       ```python
       from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

       with TypeSafeClient() as client:
           response = client.system_one(
               state={"document": "I was charged twice. Please fix this ASAP."},
               questions={
                   "billing": Noul(instructions="Is this ticket about billing?"),
                   "tone": Choice(
                       instructions="What is the customer's tone?",
                       criteria={"calm": None, "frustrated": None, "angry": None},
                   ),
                   "urgency": Score(
                       instructions="How urgent is this ticket?",
                       criteria=["can wait", "this week", "today"],
                   ),
               },
           )

       print(response.nouls["billing"].noul)
       print(response.choices["tone"].choice)
       print(response.scores["urgency"].score)
       ```



### Usage

Learn more in the [Usage guide](Usage.md).
