# developers.llamaindex.ai/python/framework/integrations/llm/deepseek/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/deepseek/index.md

--- title: DeepSeek | Developer Documentation ---
# LlamaIndex Llms Integration: DeepSeek

This is the DeepSeek integration for LlamaIndex. Visit DeepSeek [1] for information on how to get an API key and which models are supported.

At the time of writing, you can use:
- `deepseek-chat` - `deepseek-reasoner`
## Setup
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-deepseek ```
``` from llama_index.llms.deepseek import DeepSeek
# you can also set DEEPSEEK_API_KEY in your environment variables llm = DeepSeek(model="deepseek-reasoner", api_key="you_api_key")
# You might also want to set deepseek as your default llm # from llama_index.core import Settings # Settings.llm = llm ```
``` response = llm.complete("Is 9.9 or 9.11 bigger?") ```
``` print(response) ```
``` To determine whether 9.9 or 9.11 is larger, compare them by aligning their decimal places:
1. **Write both numbers with the same number of decimal places**: - \(9.9\) becomes \(9.90\). - \(9.11\) remains \(9.11\).
2. **Compare digit by digit**: - **Units place**: Both have \(9\) (equal). - **Tenths place**: \(9\) (in \(9.90\)) vs. \(1\) (in \(9.11\)). Since \(9 > 1\), \(9.90 > 9.11\).
**Conclusion**: \(9.9\) (or \(9.90\)) is greater than \(9.11\).
\(\boxed{9.9}\) ```
#### Call `chat` with a list of messages

messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage( role="user", content="How many 'r's are in the word 'strawberry'?" ), ] resp = llm.chat(messages) ```

``` print(resp) ```
``` assistant: Arrr, matey! Let's plunder the word "strawberry" fer them sneaky 'r's! Here be the breakdown:
**S - T - R - A - W - B - E - R - R - Y**

Shiver me timbers! There be **3 'r's** lurkin' in them letters! Aye, one in "straw" and two in "berry"—just like treasure buried in three chests! 🏴☠️🍓 ```

### Streaming
Using `stream_complete` endpoint
``` response = llm.stream_complete("Is 9.9 or 9.11 bigger?") ```
``` for r in response: print(r.delta, end="") ```

``` To determine whether 9.9 or 9.11 is bigger, we can compare them by converting both numbers to have the same number of decimal places.

- 9.9 can be written as 9.90 (adding a zero to make it two decimal places). - 9.11 is already in two decimal places.
Next, we compare the tenths place: - 9.90 has a 9 in the tenths place. - 9.11 has a 1 in the tenths place.
Since 9 is greater than 1, 9.90 is larger than 9.11.
To confirm, we can subtract: \[ 9.90 - 9.11 = 0.79 \] The positive result indicates that 9.90 is greater than 9.11.
Another method is converting to fractions: - 9.9 is \( \frac{99}{10} \) which is equivalent to \( \frac{990}{100} \). - 9.11 is \( \frac{911}{100} \).
Comparing \( \frac{990}{100} \) and \( \frac{911}{100} \), we see 990 is greater than 911.
Thus, the larger number is \boxed{9.9}. ```
Using `stream_chat` endpoint
``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage( role="system", content="You are a pirate with a colorful personality" ), ChatMessage( role="user", content="How many 'r's are in the word 'strawberry'?" ), ] resp = llm.stream_chat(messages) ```

``` for r in resp: print(r.delta, end="") ```
``` Arrr, matey! Let's plunder the letters o' "strawberry" to count them sneaky 'r's! 🏴☠️
**S-T-R-A-W-B-E-R-R-Y** Yarrr, here be the breakdown:
1. **S** 🚫 2. **T** 🚫 3. **R** ✅ (1st 'r') 4. **A** 🚫 5. **W** 🚫 6. **B** 🚫 7. **E** 🚫 8. **R** ✅ (2nd 'r') 9. **R** ✅ (3rd 'r') 10. **Y** 🚫

**Total 'r's: 3**
Shiver me timbers! Three 'r's be lurkin' in "strawberry"! 🍓⚔️ ```

[1] https://api-docs.deepseek.com/