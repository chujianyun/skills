# Smart home assistant demo

> Demo code: a smart home assistant that uses TypeSafe to evaluate user requests.

## Check it out in action

  <iframe src="https://www.loom.com/embed/18c4dbcf8db546dfb2d7f2ef018e78e4" title="Smart home assistant demo video" allow="fullscreen; picture-in-picture" style={{ width: '100%', aspectRatio: '16 / 9', border: 'none' }} />

## How it works

### Speculative fan-out

The chief pattern demonstrated here is [speculative fan-out](../Patterns/Speculative fan-out.md). Each user request is evaluated against a long list of questions, including many that will end up irrelevant for most requests.

Let's consider the following user request:

> "Turn off all of the lights in the house"

This is a very simple request, and our code will only need to consider the answers to the following questions:

* "What category of request is this?" (smarthome command)
* "What domain is this request targeting?" (whole house)
* "What type of device is this request targeting?" (lights)
* "What action should be taken on the lights?" (turn off)

Notice that the last question is written with the assumption that the user is issuing a command to lights, and we ask it before we know what the user is actually requesting. This is what we call a "speculative question" - we ask it before we even know if it's relevant, allowing us to evaluate all questions in parallel and rely on code to filter out the irrelevant results after the fact. This is a key pattern for building systems that can handle a wide variety of user requests with a single set of questions.

#### The wrong way: sequential API calls

The wrong way to do this would be to separate the questions in to multiple API calls, waiting to ask questions only once you are certain you need the answer:

* "What category of request is this?" (smarthome command)

Then, only once you know it's a smarthome command:

* "What domain is this request targeting?" (whole house)
* "What type of device is this request targeting?" (lights)

Then, only once you know it's targeting lights:

* "What action should be taken on the lights?" (turn off)

This approach optimizes for a minimum number of questions, but it ends up being much slower and more expensive than batching all of the questions in to one upfront API call.

### TypeSafe and LLM pairing

This demo also shows how TypeSafe can be paired with LLMs to handle a system that sometimes requires a string-generation step:

**Splitting a compound user request:** One of the questions in this demo is a Noul question identifying if the user request is asking for more than one distinct action. If this is true, the system uses an LLM to split the request into a list of atomic commands. The split requests are then evaluated by TypeSafe individually.

**Falling back to a conversational LLM:** When TypeSafe determines that the user query is a request for general information or conversation, the system calls an LLM to generate a freeform response. This allows an interactive system to handle requests with known deterministic behavior in a fast and cost efficient way, while still allowing for the flexibility provided by a generative LLM when needed. The initial TypeSafe response is so fast compared to the LLM response that it adds negligible latency to the overall system.

## Run it yourself

This demo is a simple Vite/React single-page app that uses the TypeSafe API to evaluate user requests. The full source code will be available on GitHub at release. Its README includes instructions for running the demo locally and an overview of which bits of the source code are responsible for which parts of the demo.
