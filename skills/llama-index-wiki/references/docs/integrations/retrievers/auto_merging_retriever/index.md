# developers.llamaindex.ai/python/framework/integrations/retrievers/auto_merging_retriever/index.md
> https://developers.llamaindex.ai/python/framework/integrations/retrievers/auto_merging_retriever/index.md

--- title: Auto Merging Retriever | Developer Documentation ---
In this notebook, we showcase our `AutoMergingRetriever`, which looks at a set of leaf nodes and recursively “merges” subsets of leaf nodes that reference a parent node beyond a given threshold. This allows us to consolidate potentially disparate, smaller contexts into a larger context that might help synthesis.
You can define this hierarchy yourself over a set of documents, or you can make use of our brand-new text parser: a HierarchicalNodeParser that takes in a candidate set of documents and outputs an entire hierarchy of nodes, from “coarse-to-fine”.
``` %pip install llama-index-llms-openai %pip install llama-index-readers-file pymupdf ```
``` %load_ext autoreload %autoreload 2 ```
If you’re opening this Notebook on colab, you will probably need to install LlamaIndex 🦙.
``` !pip install llama-index ```
## Load Data
Let’s first load the Llama 2 paper: <https://arxiv.org/pdf/2307.09288.pdf>. This will be our test data.
``` !mkdir -p 'data/' !wget --user-agent "Mozilla" "https://arxiv.org/pdf/2307.09288.pdf" -O "data/llama2.pdf" ```
``` from pathlib import Path
from llama_index.readers.file import PDFReader from llama_index.readers.file import PyMuPDFReader ```
``` loader = PyMuPDFReader() # docs0 = loader.load_data(file=Path("./data/llama2.pdf")) docs0 = loader.load(file_path=Path("./data/llama2.pdf")) ```
By default, the PDF reader creates a separate doc for each page. For the sake of this notebook, we stitch docs together into one doc. This will help us better highlight auto-merging capabilities that “stitch” chunks together later on.
``` from llama_index.core import Document
doc_text = "\n\n".join([d.get_content() for d in docs0]) docs = [Document(text=doc_text)] ```
## Parse Chunk Hierarchy from Text, Load into Storage
In this section we make use of the `HierarchicalNodeParser`. This will output a hierarchy of nodes, from top-level nodes with bigger chunk sizes to child nodes with smaller chunk sizes, where each child node has a parent node with a bigger chunk size.
By default, the hierarchy is:
- 1st level: chunk size 2048 - 2nd level: chunk size 512 - 3rd level: chunk size 128
We then load these nodes into storage. The leaf nodes are indexed and retrieved via a vector store - these are the nodes that will first be directly retrieved via similarity search. The other nodes will be retrieved from a docstore.
``` from llama_index.core.node_parser import ( HierarchicalNodeParser, SentenceSplitter, ) ```

``` node_parser = HierarchicalNodeParser.from_defaults() ```
``` nodes = node_parser.get_nodes_from_documents(docs) ```

``` 1029 ```
Here we import a simple helper function for fetching “leaf” nodes within a node list. These are nodes that don’t have children of their own.
``` from llama_index.core.node_parser import get_leaf_nodes, get_root_nodes ```
``` leaf_nodes = get_leaf_nodes(nodes) ```
``` len(leaf_nodes) ```
``` 795 ```
``` root_nodes = get_root_nodes(nodes) ```
### Load into Storage
We define a docstore, which we load all nodes into.
We then define a `VectorStoreIndex` containing just the leaf-level nodes.
``` # define storage context from llama_index.core.storage.docstore import SimpleDocumentStore from llama_index.core import StorageContext from llama_index.llms.openai import OpenAI
docstore = SimpleDocumentStore()
# insert nodes into docstore docstore.add_documents(nodes)
# define storage context (will include vector store by default too) storage_context = StorageContext.from_defaults(docstore=docstore)
llm = OpenAI(model="gpt-3.5-turbo") ```
``` ## Load index into vector index from llama_index.core import VectorStoreIndex
base_index = VectorStoreIndex( leaf_nodes, storage_context=storage_context, ) ```
## Define Retriever
``` from llama_index.core.retrievers import AutoMergingRetriever ```
``` base_retriever = base_index.as_retriever(similarity_top_k=6) retriever = AutoMergingRetriever(base_retriever, storage_context, verbose=True) ```
``` # query_str = "What were some lessons learned from red-teaming?" # query_str = "Can you tell me about the key concepts for safety finetuning" query_str = ( "What could be the potential outcomes of adjusting the amount of safety" " data used in the RLHF stage?" )

nodes = retriever.retrieve(query_str) base_nodes = base_retriever.retrieve(query_str) ```
``` > Merging 4 nodes into parent node. > Parent node id: caf5f81c-842f-46a4-b679-6be584bd6aff. > Parent node text: We conduct RLHF by first collecting human preference data for safety similar to Section 3.2.2: an... ```
``` len(nodes) ```
``` 3 ```
``` len(base_nodes) ```
``` 6 ```
``` from llama_index.core.response.notebook_utils import display_source_node
for node in nodes: display_source_node(node, source_length=10000) ```
**Node ID:** d4d67180-71c8-4328-b3f1-1e98fa42ab69\ **Similarity:** 0.8694979150607424\ **Text:** We also list two qualitative examples where safety and helpfulness reward models don’t agree with each other in Table 35. A.4.2 Qualitative Results on Safety Data Scaling In Section 4.2.3, we study the impact of adding more safety data into model RLHF in a quantitative manner. Here we showcase a few samples to qualitatively examine the evolution of model behavior when we scale safety data in Tables 36, 37, and 38. In general, we are observing that Llama 2-Chat becomes safer responding to unsafe prompts with more safety data used.
**Node ID:** caf5f81c-842f-46a4-b679-6be584bd6aff\ **Similarity:** 0.86168727941324\ **Text:** We conduct RLHF by first collecting human preference data for safety similar to Section 3.2.2: annotators write a prompt that they believe can elicit unsafe behavior, and then compare multiple model responses to the prompts, selecting the response that is safest according to a set of guidelines. We then use the human preference data to train a safety reward model (see Section 3.2.2), and also reuse the adversarial prompts to sample from the model during the RLHF stage. Better Long-Tail Safety Robustness without Hurting Helpfulness Safety is inherently a long-tail problem, where the challenge comes from a small number of very specific cases. We investigate the impact of Safety RLHF by taking two intermediate Llama 2-Chat checkpoints—one without adversarial prompts in the RLHF stage and one with them—and score their responses on our test sets using our safety and helpfulness reward models. In Figure 14, we plot the score distribution shift of the safety RM on the safety test set (left) and that of the helpfulness RM on the helpfulness test set (right). In the left hand side of the figure, we observe that the distribution of safety RM scores on the safety set shifts to higher reward scores after safety tuning with RLHF, and that the long tail of the distribution near zero thins out. A clear cluster appears on the top-left corner suggesting the improvements of model safety. On the right side, we do not observe any gathering pattern below the y = x line on the right hand side of Figure 14, which indicates that the helpfulness score distribution is preserved after safety tuning with RLHF. Put another way, given sufficient helpfulness training data, the addition of an additional stage of safety mitigation does not negatively impact model performance on helpfulness to any notable degradation. A qualitative example is shown in Table 12. Impact of Safety Data Scaling. A tension between helpfulness and safety of LLMs has been observed in previous studies (Bai et al., 2022a). To better understand how the addition of safety training data affects general model performance, especially helpfulness, we investigate the trends in safety data scaling by adjusting the amount of safety data used in the RLHF stage.

**Node ID:** d9893bef-a5a7-4248-a0a1-d7c28800ae59\ **Similarity:** 0.8546977459150967\ **Text:** 0 0.2 0.4 0.6 0.8 1.0 Helpfulness RM Score before Safety RLHF 0.0 0.2 0.4 0.6 0.8 1.0 Helpfulness RM Score after Safety RLHF 0 1000 0 1000 Figure 14: Impact of safety RLHF measured by reward model score distributions. Left: safety reward model scores of generations on the Meta Safety test set. The clustering of samples in the top left corner suggests the improvements of model safety.
``` for node in base_nodes: display_source_node(node, source_length=10000) ```
**Node ID:** 16328561-9ff7-4307-8d31-adf6bb74b71b\ **Similarity:** 0.8770715326726375\ **Text:** A qualitative example is shown in Table 12. Impact of Safety Data Scaling. A tension between helpfulness and safety of LLMs has been observed in previous studies (Bai et al., 2022a). To better understand how the addition of safety training data affects general model performance, especially helpfulness, we investigate the trends in safety data scaling by adjusting the amount of safety data used in the RLHF stage.
**Node ID:** e756d327-1a28-4228-ac38-f8a831b1bf77\ **Similarity:** 0.8728111844788112\ **Text:** A clear cluster appears on the top-left corner suggesting the improvements of model safety. On the right side, we do not observe any gathering pattern below the y = x line on the right hand side of Figure 14, which indicates that the helpfulness score distribution is preserved after safety tuning with RLHF. Put another way, given sufficient helpfulness training data, the addition of an additional stage of safety mitigation does not negatively impact model performance on helpfulness to any notable degradation. A qualitative example is shown in Table 12. Impact of Safety Data Scaling.
**Node ID:** d4d67180-71c8-4328-b3f1-1e98fa42ab69\ **Similarity:** 0.8697379697028405\ **Text:** We also list two qualitative examples where safety and helpfulness reward models don’t agree with each other in Table 35. A.4.2 Qualitative Results on Safety Data Scaling In Section 4.2.3, we study the impact of adding more safety data into model RLHF in a quantitative manner. Here we showcase a few samples to qualitatively examine the evolution of model behavior when we scale safety data in Tables 36, 37, and 38. In general, we are observing that Llama 2-Chat becomes safer responding to unsafe prompts with more safety data used.
**Node ID:** d9893bef-a5a7-4248-a0a1-d7c28800ae59\ **Similarity:** 0.855087365309258\ **Text:** 0 0.2 0.4 0.6 0.8 1.0 Helpfulness RM Score before Safety RLHF 0.0 0.2 0.4 0.6 0.8 1.0 Helpfulness RM Score after Safety RLHF 0 1000 0 1000 Figure 14: Impact of safety RLHF measured by reward model score distributions. Left: safety reward model scores of generations on the Meta Safety test set. The clustering of samples in the top left corner suggests the improvements of model safety.
**Node ID:** d62ee107-9841-44b5-8b70-bc6487ad6315\ **Similarity:** 0.8492541852986794\ **Text:** Better Long-Tail Safety Robustness without Hurting Helpfulness Safety is inherently a long-tail problem, where the challenge comes from a small number of very specific cases. We investigate the impact of Safety RLHF by taking two intermediate Llama 2-Chat checkpoints—one without adversarial prompts in the RLHF stage and one with them—and score their responses on our test sets using our safety and helpfulness reward models.
**Node ID:** 312a63b3-5e28-4fbf-a3e1-4e8dc0c026ea\ **Similarity:** 0.8488371951811564\ **Text:** We conduct RLHF by first collecting human preference data for safety similar to Section 3.2.2: annotators write a prompt that they believe can elicit unsafe behavior, and then compare multiple model responses to the prompts, selecting the response that is safest according to a set of guidelines. We then use the human preference data to train a safety reward model (see Section 3.2.2), and also reuse the adversarial prompts to sample from the model during the RLHF stage.
## Plug it into Query Engine
``` from llama_index.core.query_engine import RetrieverQueryEngine ```
``` query_engine = RetrieverQueryEngine.from_args(retriever) base_query_engine = RetrieverQueryEngine.from_args(base_retriever) ```
``` response = query_engine.query(query_str) ```
``` > Merging 4 nodes into parent node. > Parent node id: 3671b20d-ea5e-4afc-983e-02be6ee8302d. > Parent node text: We conduct RLHF by first collecting human preference data for safety similar to Section 3.2.2: an... ```
``` print(str(response)) ```
``` Adjusting the amount of safety data used in the RLHF stage could potentially have the following outcomes: 1. Improved model safety: Increasing the amount of safety data used in RLHF may lead to improvements in model safety. This means that the model becomes better at responding to unsafe prompts and avoids generating unsafe or harmful outputs. 2. Thinning out of the long tail of safety RM scores: Increasing the amount of safety data may result in a shift in the distribution of safety reward model (RM) scores towards higher reward scores. This means that the model becomes more consistent in generating safe responses and reduces the occurrence of low safety scores. 3. Preservation of helpfulness performance: Adjusting the amount of safety data used in RLHF is not expected to negatively impact model performance on helpfulness. This means that the model's ability to generate helpful responses is maintained even after incorporating additional safety training.
4. Gathering pattern in helpfulness RM scores: There is no observed gathering pattern below the y = x line in the distribution of helpfulness RM scores after safety tuning with RLHF. This suggests that the helpfulness score distribution is preserved, indicating that the model's helpfulness performance is not significantly degraded by the addition of safety mitigation measures. Overall, adjusting the amount of safety data used in the RLHF stage aims to strike a balance between improving model safety without compromising its helpfulness performance. ```
``` base_response = base_query_engine.query(query_str) ```
``` print(str(base_response)) ```
``` Adjusting the amount of safety data used in the RLHF stage could potentially lead to improvements in model safety. This can be observed by a clear cluster appearing on the top-left corner, suggesting enhanced model safety. Additionally, it is indicated that the helpfulness score distribution is preserved after safety tuning with RLHF, indicating that the addition of safety data does not negatively impact model performance on helpfulness. ```
## Evaluation
We evaluate how well the hierarchical retriever works compared to the baseline retriever in a more quantitative manner.
**WARNING**: This can be *expensive*, especially with GPT-4. Use caution and tune the sample size to fit your budget.
``` from llama_index.core.evaluation import DatasetGenerator, QueryResponseDataset from llama_index.llms.openai import OpenAI import nest_asyncio

``` # NOTE: run this if the dataset isn't already saved # Note: we only generate from the first 20 nodes, since the rest are references eval_llm = OpenAI(model="gpt-4") dataset_generator = DatasetGenerator( root_nodes[:20], llm=eval_llm, show_progress=True, num_questions_per_chunk=3, ) ```

``` eval_dataset = await dataset_generator.agenerate_dataset_from_nodes(num=60) ```
``` eval_dataset.save_json("data/llama2_eval_qr_dataset.json") ```
``` # optional eval_dataset = QueryResponseDataset.from_json( "data/llama2_eval_qr_dataset.json" ) ```
### Compare Results
We run evaluations on each of the retrievers: correctness, semantic similarity, relevance, and faithfulness.
``` import asyncio import nest_asyncio
nest_asyncio.apply() ```
``` from llama_index.core.evaluation import ( CorrectnessEvaluator, SemanticSimilarityEvaluator, RelevancyEvaluator, FaithfulnessEvaluator, PairwiseComparisonEvaluator, )

from collections import defaultdict import pandas as pd
# NOTE: can uncomment other evaluators evaluator_c = CorrectnessEvaluator(llm=eval_llm) evaluator_s = SemanticSimilarityEvaluator(llm=eval_llm) evaluator_r = RelevancyEvaluator(llm=eval_llm) evaluator_f = FaithfulnessEvaluator(llm=eval_llm) # pairwise_evaluator = PairwiseComparisonEvaluator(llm=eval_llm) ```
``` from llama_index.core.evaluation.eval_utils import ( get_responses, get_results_df, ) from llama_index.core.evaluation import BatchEvalRunner ```
``` eval_qs = eval_dataset.questions qr_pairs = eval_dataset.qr_pairs ref_response_strs = [r for (_, r) in qr_pairs] ```
``` pred_responses = get_responses(eval_qs, query_engine, show_progress=True) ```
``` base_pred_responses = get_responses( eval_qs, base_query_engine, show_progress=True ) ```
``` 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 60/60 [00:07<00:00, 8.17it/s] ```
``` import numpy as np
pred_response_strs = [str(p) for p in pred_responses] base_pred_response_strs = [str(p) for p in base_pred_responses] ```
``` evaluator_dict = { "correctness": evaluator_c, "faithfulness": evaluator_f, "relevancy": evaluator_r, "semantic_similarity": evaluator_s, } batch_runner = BatchEvalRunner(evaluator_dict, workers=2, show_progress=True) ```

``` eval_results = await batch_runner.aevaluate_responses( eval_qs, responses=pred_responses, reference=ref_response_strs ) ```
``` base_eval_results = await batch_runner.aevaluate_responses( eval_qs, responses=base_pred_responses, reference=ref_response_strs ) ```
``` results_df = get_results_df( [eval_results, base_eval_results], ["Auto Merging Retriever", "Base Retriever"], ["correctness", "relevancy", "faithfulness", "semantic_similarity"], ) display(results_df) ```

``` .dataframe tbody tr th { vertical-align: top; }
.dataframe thead th { text-align: right; } ```
| | names | correctness | relevancy | faithfulness | semantic\_similarity | | - | ---------------------- | ----------- | --------- | ------------ | -------------------- | | 0 | Auto Merging Retriever | 4.266667 | 0.916667 | 0.95 | 0.962196 | | 1 | Base Retriever | 4.208333 | 0.916667 | 0.95 | 0.960602 |
**Analysis**: The results are roughly the same.
Let’s also try to see which answer GPT-4 prefers with our pairwise evals.
``` batch_runner = BatchEvalRunner( {"pairwise": pairwise_evaluator}, workers=10, show_progress=True ) ```
``` pairwise_eval_results = await batch_runner.aevaluate_response_strs( eval_qs, response_strs=pred_response_strs, reference=base_pred_response_strs, ) pairwise_score = np.array( [r.score for r in pairwise_eval_results["pairwise"]] ).mean() ```

``` pairwise_score ```
``` 0.525 ```
**Analysis**: The pairwise comparison score is a measure of the percentage of time the candidate answer (using auto-merging retriever) is preferred vs. the base answer (using the base retriever). Here we see that it’s roughly even.