# developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/query_engine/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/querying/structured_outputs/query_engine/index.md

[Column 1]
--- title: (Deprecated) Query Engines + Pydantic Outputs | Developer Documentation ---
Tip

Every query engine has support for integrated structured responses using the following `response_mode`s in `RetrieverQueryEngine`:
- `refine` - `compact` - `tree_summarize` - `accumulate` (beta, requires extra parsing to convert to objects) - `compact_accumulate` (beta, requires extra parsing to convert to objects)

Under the hood, this uses `OpenAIPydanitcProgam` or `LLMTextCompletionProgram` depending on which LLM you’ve setup. If there are intermediate LLM responses (i.e. during `refine` or `tree_summarize` with multiple LLM calls), the pydantic object is injected into the next LLM prompt as a JSON object.
## Usage Pattern
First, you need to define the object you want to extract.
``` from typing import List from pydantic import BaseModel

[Column 2]
This guide references a deprecated method of extracting structured outputs in a RAG workflow. Check out our structured output starter guide for more details.
Using `index.as_query_engine()` and it’s underlying `RetrieverQueryEngine`, we can support structured pydantic outputs without an additional LLM calls (in contrast to a typical output parser.)


class Biography(BaseModel): """Data model for a biography."""
name: str best_known_for: List[str] extra_info: str ```

Then, you create your query engine.
``` query_engine = index.as_query_engine( response_mode="tree_summarize", output_cls=Biography ) ```

Lastly, you can get a response and inspect the output.
``` response = query_engine.query("Who is Paul Graham?")
print(response.name) # > 'Paul Graham' print(response.best_known_for) # > ['working on Bel', 'co-founding Viaweb', 'creating the programming language Arc'] print(response.extra_info) # > "Paul Graham is a computer scientist, entrepreneur, and writer. He is best known for ..." ```

## Modules
Detailed usage is available in the notebooks below:
- Structured Outputs with a Query Engine - Structured Outputs with a Tree Summarize