# developers.llamaindex.ai/python/framework/integrations/llm/cometapi/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/cometapi/index.md

--- title: CometAPI | Developer Documentation ---
CometAPI provides access to various state-of-the-art LLM models including GPT series, Claude series, Gemini series, and more through a unified OpenAI-compatible interface. You can find out more on their [homepage] [1].
Visit <https://api.cometapi.com/console/token> to sign up and get an API key.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-cometapi ```
``` %pip install llama-index ```
``` from llama_index.llms.cometapi import CometAPI ```
## Call `chat` with ChatMessage List
You need to either set env var `COMETAPI_API_KEY` or set api\_key in the class constructor
``` import os
os.environ["COMETAPI_KEY"] = "<your-cometapi-key>"
api_key = os.getenv("COMETAPI_KEY") llm = CometAPI( api_key=api_key, max_tokens=256, context_window=4096, model="gpt-5-chat-latest", ) ```

``` from llama_index.core.llms import ChatMessage
messages = [ ChatMessage(role="system", content="You are a helpful assistant"), ChatMessage(role="user", content="Say 'Hi' only!"), ] resp = llm.chat(messages) print(resp) ```

``` assistant: Hi ```
``` resp = llm.complete("Who is Kaiming He") ```
``` print(resp) ```
``` Kaiming He is a renowned computer scientist and research scientist known for his influential contributions to the field of computer vision and deep learning. He is particularly famous for being one of the main authors of the **ResNet** (Residual Networks) architecture, introduced in the 2015 paper *"Deep Residual Learning for Image Recognition"*, which won the Best Paper Award at CVPR 2016. ResNet significantly improved the training of very deep neural networks using residual connections, and it became a foundational architecture for many vision tasks.
### Key Facts about Kaiming He:
- **Education**: Kaiming He earned his Ph.D. in computer science from the Chinese University of Hong Kong (CUHK), where he worked with Prof. Jian Sun and in collaboration with the Visual Computing Group.
- **Research Career**: - He has worked at Microsoft Research Asia (MSRA). - Later, he was a research scientist at Facebook AI Research (FAIR). - As of recent years, he works at FAIR (now part of Meta AI) focusing on computer vision, deep learning, and artificial intelligence.
- **Major Contributions**: - **ResNet** (Deep Residual Networks, 2015) — revolutionized deep network ```
### Streaming
Using `stream_complete` endpoint
``` message = ChatMessage(role="user", content="Tell me what ResNet is") resp = llm.stream_chat([message]) for r in resp: print(r.delta, end="") ```

```` ResNet, short for **Residual Network**, is a type of deep neural network architecture introduced by Microsoft Research in 2015 in the paper *"Deep Residual Learning for Image Recognition"* by Kaiming He et al. It became famous after winning the **ImageNet Large Scale Visual Recognition Challenge ( al. It became famous after winning the **ImageNet Large Scale Visual Recognition Challenge (ILSVRC) 2015**.

### **Key idea** The main innovation of ResNet isILSVRC) 2015**.

### **Key idea** The main innovation of ResNet is the concept of **residual learning** using **skip connections** (or shortcut connections). In very the concept of **residual learning** using **skip connections** (or shortcut connections). In very deep neural networks, performance can degrade because of the **vanishing/exploding gradient problem deep neural networks, performance can degrade because of the **vanishing/exploding gradient problem** and difficulty in optimization. ResNet solves this by letting certain layers "skip" forward in** and difficulty in optimization. ResNet solves this by letting certain layers "skip" forward in the network through identity mappings.

A *residual block the network through identity mappings.
A *residual block* looks like this:
``` Input → [Layer(s): Conv, BatchNorm* looks like this:
``` Input → [Layer(s): Conv, BatchNorm, ReLU] → Output \_____________________________________/ (skip, ReLU] → Output \_____________________________________/ (skip connection) ```

Instead of directly learning a mapping connection) ```
Instead of directly learning a mapping \( H(x) \), the residual block learns \( F(x) \( H(x) \), the residual block learns \( F(x) = H(x) - x \), so that: \[ H(x) = F(x) + x \] Here = H(x) - x \), so that: \[ H(x) = F(x) + x \] Here, \( x \) is added directly to the output of the block, enabling easier gradient flow, \( x \) is added directly to the output of the block, enabling easier gradient flow and allowing training of and allowing training of ````

``` resp = llm.stream_complete("Tell me about Large Language Models") ```
``` for r in resp: print(r.delta, end="") ```
``` Sure! **Large Language Models** (LLMs) are a type of **artificial intelligence model** designed to understand, generate, and manipulate human language. They’re trained on massive amounts of text from books, articles, websites, code** designed to understand, generate, and manipulate human language. They’re trained on massive amounts of text from books, articles, websites, code, and more, enabling them to predict and produce coherent text based on a prompt.
Here’s a detailed, and more, enabling them to predict and produce coherent text based on a prompt.
Here’s a detailed overview:

## **1. What They Are** - LLMs are a subset of ** overview:

## **1. What They Are** - LLMs are a subset of **deep learning** models, usually based on the **transformer architecture** (introduced in 2017deep learning** models, usually based on the **transformer architecture** (introduced in 2017 by *Vaswani et al.* in the paper *"Attention Is All You Need"*). - They are called * by *Vaswani et al.* in the paper *"Attention Is All You Need"*). - They are called *“large”* because they have **billions—or even trillions—of parameters** (adjustable weights“large”* because they have **billions—or even trillions—of parameters** (adjustable weights learned during training) and train on vast datasets.

## **2. How They Work** 1. **Training Data learned during training) and train on vast datasets.
---
## **2. How They Work** 1. **Training Data** They learn patterns of language from huge text corpora taken from books, Wikipedia, the internet, etc** They learn patterns of language from huge text corpora taken from books, Wikipedia, the internet, etc. 2. **Tokenization** Text is broken into small pieces called *tokens* (these. 2. **Tokenization** Text is broken into small pieces called *tokens* (these could be whole words, subwords, or even characters). 3. **Neural Architecture** could be whole words, subwords, or even characters). 3. **Neural Architecture** Transformers use *self-attention* mechanisms to relate different Transformers use *self-attention* mechanisms to relate different ```

### Using Different Models
CometAPI supports various AI models including GPT, Claude, and Gemini series.
``` # Using Claude model claude_llm = CometAPI( api_key=api_key, model="claude-3-7-sonnet-latest", max_tokens=200 )

resp = claude_llm.complete("Explain deep learning briefly") print(resp) ```
``` # Deep Learning: A Brief Explanation
Deep learning is a subset of machine learning that uses neural networks with multiple layers (hence "deep") to analyze data and make predictions.
## Key Characteristics:
- **Neural Networks**: Inspired by the human brain, these networks consist of interconnected nodes (neurons) organized in layers - **Automatic Feature Extraction**: Unlike traditional ML, deep learning automatically discovers important features in data without manual engineering - **Hierarchical Learning**: Lower layers learn simple patterns while deeper layers combine these to recognize complex concepts - **Large Data Requirements**: Typically needs substantial amounts of data to perform well
Deep learning powers many modern technologies including image recognition, natural language processing, speech recognition, and recommendation systems. Its effectiveness comes from its ability to model highly complex relationships in data, though this often requires significant computational resources. ```

[1] https://www.cometapi.com/