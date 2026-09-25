# developers.llamaindex.ai/python/framework/community/integrations/trulens/index.md
> https://developers.llamaindex.ai/python/framework/community/integrations/trulens/index.md

--- title: Evaluating and Tracking with TruLens | Developer Documentation ---
This page covers how to use TruLens [1] to evaluate and track LLM apps built on Llama-Index.
## What is TruLens?
TruLens is an opensource [2] package that provides instrumentation and evaluation tools for large language model (LLM) based applications. This includes feedback function evaluations of relevance, sentiment and more, plus in-depth tracing including cost and latency.
[3]
As you iterate on new versions of your LLM application, you can compare their performance across all of the different quality metrics you’ve set up. You’ll also be able to view evaluations at a record level, and explore the app metadata for each record.
### Installation and Setup
Adding TruLens is simple, just install it from pypi!
Terminal window
``` pip install trulens-eval ```
``` from trulens_eval import TruLlama ```
## Try it out!
llama\_index\_quickstart.ipynb [4]
![Open In Colab][6] [5]
## Read more
- Build and Evaluate LLM Apps with LlamaIndex and TruLens [7] - More examples [8] - trulens.org [9]

[1] https://trulens.org
[2] https://github.com/truera/trulens
[3] https://www.trulens.org/Assets/image/TruLens_Architecture.png
[4] https://github.com/truera/trulens/blob/trulens-eval-0.20.3/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb
[5] https://colab.research.google.com/github/truera/trulens/blob/main/trulens_eval/examples/quickstart/llama_index_quickstart.ipynb
[6] https://colab.research.google.com/assets/colab-badge.svg
[7] https://medium.com/llamaindex-blog/build-and-evaluate-llm-apps-with-llamaindex-and-trulens-6749e030d83c
[8] https://github.com/truera/trulens/tree/main/trulens_eval/examples/expositional/frameworks/llama_index
[9] https://www.trulens.org/