# developers.llamaindex.ai/python/framework/integrations/llm/cohere/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/cohere/index.md

--- title: Cohere | Developer Documentation ---

## Basic Usage
#### Call `complete` with a prompt
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-openai %pip install llama-index-llms-cohere ```

``` !pip install llama-index ```

api_key = "<API_KEY>" resp = Cohere(api_key=api_key).complete("Paul Graham is ") ```

[Column 1]
#### Call `chat` with a list of messages
``` from llama_index.core.llms import ChatMessage from llama_index.llms.cohere import Cohere

messages = [ ChatMessage(role="user", content="hello there"), ChatMessage( role="assistant", content="Arrrr, matey! How can I help ye today?" ), ChatMessage(role="user", content="What is your name"), ]

resp = Cohere(api_key=api_key).chat( messages, preamble_override="You are a pirate with a colorful personality" ) ```

[Column 2]
``` an English computer scientist, entrepreneur and investor. He is best known for his work as a co-founder of the seed accelerator Y Combinator. He is also the author of the free startup advice blog "Startups.com". Paul Graham is known for his philanthropic efforts. Has given away hundreds of millions of dollars to good causes. ```


``` assistant: Traditionally, ye refers to gender-nonconforming people of any gender, and those who are genderless, whereas matey refers to a friend, commonly used to address a fellow pirate. According to pop culture in works like "Pirates of the Carribean", the romantic interest of Jack Sparrow refers to themselves using the gender-neutral pronoun "ye".

Are you interested in learning more about the pirate culture? ```
## Streaming
Using `stream_complete` endpoint

llm = Cohere(api_key=api_key) resp = llm.stream_complete("Paul Graham is ") ```

``` an English computer scientist, essayist, and venture capitalist. He is best known for his work as a co-founder of the Y Combinator startup incubator, and his essays, which are widely read and influential in the startup community. ```
Using `stream_chat` endpoint
``` from llama_index.llms.openai import OpenAI
llm = Cohere(api_key=api_key) messages = [ ChatMessage(role="user", content="hello there"), ChatMessage( role="assistant", content="Arrrr, matey! How can I help ye today?" ), ChatMessage(role="user", content="What is your name"), ] resp = llm.stream_chat( messages, preamble_override="You are a pirate with a colorful personality" ) ```

``` for r in resp: print(r.delta, end="") ```
``` Arrrr, matey! According to etiquette, we are suppose to exchange names first! Mine remains a mystery for now. ```
## Configure Model

``` resp = llm.complete("Paul Graham is ") ```

``` an English computer scientist, entrepreneur and investor. He is best known for his work as a co-founder of the seed accelerator Y Combinator. He is also the co-founder of the online dating platform Match.com. ```
## Async

llm = Cohere(model="command", api_key=api_key) ```
``` resp = await llm.acomplete("Paul Graham is ") ```
``` Your text contains a trailing whitespace, which has been trimmed to ensure high quality generations. ```
``` print(resp) ```
``` an English computer scientist, entrepreneur and investor. He is best known for his work as a co-founder of the startup incubator and seed fund Y Combinator, and the programming language Lisp. He has also written numerous essays, many of which have become highly influential in the software engineering field. ```
``` resp = await llm.astream_complete("Paul Graham is ") ```
``` async for delta in resp: print(delta.delta, end="") ```
``` an English computer scientist, essayist, and businessman. He is best known for his work as a co-founder of the startup accelerator Y Combinator, and his essay "Beating the Averages." ```
## Set API Key at a per-instance level
If desired, you can have separate LLM instances use separate API keys.
``` from llama_index.llms.cohere import Cohere
llm_good = Cohere(api_key=api_key) llm_bad = Cohere(model="command", api_key="BAD_KEY")
resp = llm_good.complete("Paul Graham is ") print(resp)
resp = llm_bad.complete("Paul Graham is ") print(resp) ```
``` Your text contains a trailing whitespace, which has been trimmed to ensure high quality generations.
an English computer scientist, entrepreneur and investor. He is best known for his work as a co-founder of the acceleration program Y Combinator. He has also written extensively on the topics of computer science and entrepreneurship. Where did you come across his name?

---------------------------------------------------------------------------
CohereAPIError Traceback (most recent call last)
Cell In[17], line 9 6 resp = llm_good.complete("Paul Graham is ") 7 print(resp) ----> 9 resp = llm_bad.complete("Paul Graham is ") 1 0 print(resp)
File /workspaces/llama_index/gllama_index/llms/base.py:277, in llm_completion_callback.<locals>.wrap.<locals>.wrapped_llm_predict(_self, *args, **kwargs) 2 67 with wrapper_logic(_self) as callback_manager: 2 68 event_id = callback_manager.on_event_start( 2 69 CBEventType.LLM, 2 70 payload={ (...) 2 74 }, 2 75 ) --> 277 f_return_val = f(_self, *args, **kwargs) 2 78 if isinstance(f_return_val, Generator): 2 79 # intercept the generator and add a callback to the end 2 80 def wrapped_gen() -> CompletionResponseGen:
File /workspaces/llama_index/gllama_index/llms/cohere.py:139, in Cohere.complete(self, prompt, **kwargs) 1 36 @llm_completion_callback() 1 37 def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse: 1 38 all_kwargs = self._get_all_kwargs(**kwargs) --> 139 response = completion_with_retry( 1 40 client=self._client, 1 41 max_retries=self.max_retries, 1 42 chat=False, 1 43 prompt=prompt, 1 44 **all_kwargs 1 45 ) 1 47 return CompletionResponse( 1 48 text=response.generations[0].text, 1 49 raw=response.__dict__, 1 50 )

File /workspaces/llama_index/gllama_index/llms/cohere_utils.py:74, in completion_with_retry(client, max_retries, chat, **kwargs) 7 1 else: 7 2 return client.generate(**kwargs) ---> 74 return _completion_with_retry(**kwargs)
File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:289, in BaseRetrying.wraps.<locals>.wrapped_f(*args, **kw) 2 87 @functools.wraps(f) 2 88 def wrapped_f(*args: t.Any, **kw: t.Any) -> t.Any: --> 289 return self(f, *args, **kw)
File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:379, in Retrying.__call__(self, fn, *args, **kwargs) 3 77 retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs) 3 78 while True: --> 379 do = self.iter(retry_state=retry_state) 3 80 if isinstance(do, DoAttempt): 3 81 try:
File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:314, in BaseRetrying.iter(self, retry_state) 3 12 is_explicit_retry = fut.failed and isinstance(fut.exception(), TryAgain) 3 13 if not (is_explicit_retry or self.retry(retry_state)): --> 314 return fut.result() 3 16 if self.after is not None: 3 17 self.after(retry_state)
File /usr/lib/python3.10/concurrent/futures/_base.py:449, in Future.result(self, timeout) 4 47 raise CancelledError() 4 48 elif self._state == FINISHED: --> 449 return self.__get_result() 4 51 self._condition.wait(timeout) 4 53 if self._state in [CANCELLED, CANCELLED_AND_NOTIFIED]:
File /usr/lib/python3.10/concurrent/futures/_base.py:401, in Future.__get_result(self) 3 99 if self._exception: 4 00 try: --> 401 raise self._exception 4 02 finally: 4 03 # Break a reference cycle with the exception in self._exception 4 04 self = None
File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/tenacity/__init__.py:382, in Retrying.__call__(self, fn, *args, **kwargs) 3 80 if isinstance(do, DoAttempt): 3 81 try: --> 382 result = fn(*args, **kwargs) 3 83 except BaseException: # noqa: B902 3 84 retry_state.set_exception(sys.exc_info()) # type: ignore[arg-type]
File /workspaces/llama_index/gllama_index/llms/cohere_utils.py:72, in completion_with_retry.<locals>._completion_with_retry(**kwargs) 7 0 return client.chat(**kwargs) 7 1 else: ---> 72 return client.generate(**kwargs)
File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/cohere/client.py:221, in Client.generate(self, prompt, prompt_vars, model, preset, num_generations, max_tokens, temperature, k, p, frequency_penalty, presence_penalty, end_sequences, stop_sequences, return_likelihoods, truncate, logit_bias, stream) 1 64 """Generate endpoint. 1 65 See https://docs.cohere.ai/reference/generate for advanced arguments 1 66 (...) 2 00 >>> print(token) 2 01 """ 2 02 json_body = { 2 03 "model": model, 2 04 "prompt": prompt, (...) 2 19 "stream": stream, 2 20 } --> 221 response = self._request(cohere.GENERATE_URL, json=json_body, stream=stream) 2 22 if stream: 2 23 return StreamingGenerations(response)

File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/cohere/client.py:927, in Client._request(self, endpoint, json, files, method, stream, params) 9 24 except jsonlib.decoder.JSONDecodeError: # CohereAPIError will capture status 9 25 raise CohereAPIError.from_response(response, message=f"Failed to decode json body: {response.text}") --> 927 self._check_response(json_response, response.headers, response.status_code) 9 28 return json_response
File ~/.local/share/projects/oss/llama_index/.venv/lib/python3.10/site-packages/cohere/client.py:869, in Client._check_response(self, json_response, headers, status_code) 8 67 logger.warning(headers["X-API-Warning"]) 8 68 if "message" in json_response: # has errors --> 869 raise CohereAPIError( 8 70 message=json_response["message"], 8 71 http_status=status_code, 8 72 headers=headers, 8 73 ) 8 74 if 400 <= status_code < 500: 8 75 raise CohereAPIError( 8 76 message=f"Unexpected client error (status {status_code}): {json_response}", 8 77 http_status=status_code, 8 78 headers=headers, 8 79 )

CohereAPIError: invalid api token ```