# developers.llamaindex.ai/python/framework/module_guides/evaluating/contributing_llamadatasets/index.md
> https://developers.llamaindex.ai/python/framework/module_guides/evaluating/contributing_llamadatasets/index.md

--- title: Contributing A `LabelledRagDataset` | Developer Documentation ---
Building a more robust RAG system requires a diversified evaluation suite. That is why we launched `LlamaDatasets` in llama-hub [1]. In this page, we discuss how you can contribute the first kind of `LlamaDataset` made available in llama-hub, that is, `LabelledRagDataset`.
Contributing a `LabelledRagDataset` involves two high level steps. Generally speaking, you must create the `LabelledRagDataset`, save it as a json and submit both this json file and the source text files to our llama- datasets repository [2]. Additionally, you’ll have to make a pull request, to upload required metadata of the dataset to our llama-hub repository [3].
To help make the submission process a lot smoother, we’ve prepared a template notebook that you can follow to create a `LabelledRagDataset` from scratch (or convert a similarly structured question-answering dataset into one) and perform other required steps to make your submission. Please refer to the “LlamaDataset Submission Template Notebook” linked below.
## Contributing Other llama-datasets
The general process for contributing any of our other llama-datasets such as the `LabelledEvaluatorDataset` is the same as for the `LabelledRagDataset` previously described. Submission templates for these other datasets are coming soon!
## Submission Example
Read the full submission example Notebook.

[1] https://llamahub.ai
[2] https://github.com/run-llama/llama_datasets
[3] https://github.com/run- llama/llama-hub