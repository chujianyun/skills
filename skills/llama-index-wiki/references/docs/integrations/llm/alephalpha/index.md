# developers.llamaindex.ai/python/framework/integrations/llm/alephalpha/index.md
> https://developers.llamaindex.ai/python/framework/integrations/llm/alephalpha/index.md

--- title: Aleph Alpha | Developer Documentation ---

Aleph Alpha is a powerful language model that can generate human-like text. Aleph Alpha is capable of generating text in multiple languages and styles, and can be fine-tuned to generate text in specific domains.
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` %pip install llama-index-llms-alephalpha ```
``` !pip install llama-index ```
#### Set your Aleph Alpha token
``` import os
os.environ["AA_TOKEN"] = "your_token_here" ```
#### Call `complete` with a prompt

# To customize your token, do this # otherwise it will lookup AA_TOKEN from your env variable # llm = AlephAlpha(token="<aa_token>") llm = AlephAlpha(model="luminous-base-control")
resp = llm.complete("Paul Graham is ") ```

``` a well-known computer scientist and entrepreneur. He is the co-founder of PayPal and a co-founder of the Y Combinator startup accelerator. He has also co-authored the book "Programming the Web". Paul Graham is also a frequent speaker and writer on topics related to computer science, entrepreneurship, and startups. He has written several blog posts on the topic of "Why Startups Fail". In this post, I will summarize some of the key points from Paul Graham's blog post on why startups fail.

1. Lack of a clear vision: Startups often lack a clear vision of what they ```
#### Additional Response Details
To access detailed response information such as log probabilities, ensure your AlephAlpha instance is initialized with the `log_probs` parameter. The `logprobs` attribute of the `CompletionResponse` will contain this data. Other details like the model version and raw completion text can be accessed directly if they’re part of the response or via `additional_kwargs`.

[Column 1]
llm = AlephAlpha(model="luminous-base-control", log_probs=0)
resp = llm.complete("Paul Graham is ")
if resp.logprobs is not None: print("\nLog Probabilities:") for lp_list in resp.logprobs: for lp in lp_list: print(f"Token: {lp.token}, LogProb: {lp.logprob}")
if "model_version" in resp.additional_kwargs: print("\nModel Version:") print(resp.additional_kwargs["model_version"])
if "raw_completion" in resp.additional_kwargs: print("\nRaw Completion:") print(resp.additional_kwargs["raw_completion"]) ```
``` Log Probabilities: Token: a, LogProb: -0.95955 Token: well, LogProb: -1.9219251 Token: -, LogProb: -0.1312752 Token: known, LogProb: -0.022855662 Token: computer, LogProb: -0.9569155 Token: scientist, LogProb: -0.06721641 Token: and, LogProb: -0.56296504 Token: entrepreneur, LogProb: -0.65574974 Token: ., LogProb: -0.5926046 Token: He, LogProb: -0.1885516 Token: is, LogProb: -0.3927348 Token: the, LogProb: -0.46820825 Token: co, LogProb: -0.465878 Token: -, LogProb: -0.024082167 Token: founder, LogProb: -0.009869587 Token: of, LogProb: -0.31641242 Token: PayPal, LogProb: -1.0825713 Token: and, LogProb: -0.39408743 Token: a, LogProb: -1.45493 Token: co, LogProb: -1.0837904 Token: -, LogProb: -0.0011430404 Token: founder, LogProb: -0.074010715 Token: of, LogProb: -0.038962167 Token: the, LogProb: -1.7761776 Token: Y, LogProb: -0.41853565 Token: Combin, LogProb: -0.17868777 Token: ator, LogProb: -2.0265374e-05 Token: startup, LogProb: -0.24595682 Token: acceler, LogProb: -0.5855012 Token: ator, LogProb: -6.675698e-06 Token: ., LogProb: -0.022597663

Token: He, LogProb: -0.8310143 Token: has, LogProb: -1.5842702 Token: also, LogProb: -0.5774656 Token: been, LogProb: -1.3938092 Token: a, LogProb: -0.67207164 Token: professor, LogProb: -1.0511048 Token: at, LogProb: -0.13273911 Token: the, LogProb: -0.7993539 Token: MIT, LogProb: -1.2281163 Token: Media, LogProb: -0.7707413 Token: Lab, LogProb: -0.06716257 Token: ., LogProb: -0.9140582 Token: Paul, LogProb: -0.8244309 Token: Graham, LogProb: -0.15202633 Token: has, LogProb: -1.3735206 Token: written, LogProb: -0.77148163 Token: several, LogProb: -0.7167357 Token: books, LogProb: -0.24542983 Token: on, LogProb: -0.77700675 Token: computer, LogProb: -0.8485363 Token: science, LogProb: -0.026196867 Token: and, LogProb: -0.4796574 Token: entrepreneurs, LogProb: -0.48952234 Token: hip, LogProb: -1.0847986e-05 Token: ,, LogProb: -0.1426171 Token: including, LogProb: -0.10799221 Token: ", LogProb: -0.4733107 Token: Program, LogProb: -0.9295699 Token: ming, LogProb: -0.00090034 Token: the, LogProb: -1.5219054 Token: Universe, LogProb: -1.2475122

Token: ", LogProb: -0.8377396 Token: and, LogProb: -0.014596111 Token: ", LogProb: -0.0034322182 Token: The, LogProb: -0.97810173 Token: Art, LogProb: -1.4708842 Token: of, LogProb: -0.0017665509 Token: Computer, LogProb: -0.027323013 Token: Programming, LogProb: -0.09090222 Token: "., LogProb: -0.2312944 Token: He, LogProb: -0.9431941 Token: is, LogProb: -0.52350885 Token: also, LogProb: -0.8409716 Token: the, LogProb: -1.2813272 Token: founder, LogProb: -0.8080497 Token: of, LogProb: -0.12735468 Token: the, LogProb: -0.26858208 Token: startup, LogProb: -1.7183943 Token: incub, LogProb: -0.71643037 Token: ator, LogProb: -0.00013922676 Token: ,, LogProb: -1.6374074 Token: Y, LogProb: -1.3464186 Token: Combin, LogProb: -0.043204635 Token: ator, LogProb: -1.490105e-05 Token: ., LogProb: -0.48073012 Token: <|endoftext|>, LogProb: -0.30235213

Model Version: 20240215

## Async
``` from llama_index.llms.alephalpha import AlephAlpha
llm = AlephAlpha(model="luminous-base-control") resp = await llm.acomplete("Paul Graham is ") ```
``` print(resp) ```
```

[Column 2]
Raw Completion: a well-known computer scientist and entrepreneur. He is the co-founder of PayPal and a co-founder of the Y Combinator startup accelerator. He has also been a professor at the MIT Media Lab. Paul Graham has written several books on computer science and entrepreneurship, including "Programming the Universe" and "The Art of Computer Programming". He is also the founder of the startup incubator, Y Combinator. ```
``` a computer scientist and entrepreneur who is known for his work in the field of artificial intelligence and computer science. He is the co-founder of the company Y Combinator, which is a startup accelerator that helps startups get funding and resources. Paul Graham has also written several books on computer science and entrepreneurship, including "Programming: Principles and Practice" and "The Art of Computer Programming". He is a well- known figure in the computer science community and has made significant contributions to the field.
