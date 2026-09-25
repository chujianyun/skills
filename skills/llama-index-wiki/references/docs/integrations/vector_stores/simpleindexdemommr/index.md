# developers.llamaindex.ai/python/framework/integrations/vector_stores/simpleindexdemommr/index.md
> https://developers.llamaindex.ai/python/framework/integrations/vector_stores/simpleindexdemommr/index.md

[Column 1]
--- title: Simple Vector Stores - Maximum Marginal Relevance Retrieval | Developer Documentation ---

Download Data
``` %pip install llama-index-embeddings-openai %pip install llama-index-llms-openai ```

``` import os
os.environ["OPENAI_API_KEY"] = "sk-..." ```
``` from llama_index.embeddings.openai import OpenAIEmbedding from llama_index.llms.openai import OpenAI from llama_index.core import Settings
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2) Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small") ```

[Column 2]
This notebook explores the use of MMR retrieval \[1 [1]]. By using maximum marginal relevance, one can iteratively find documents that are dissimilar to previous results. It has been shown to improve performance for LLM retrievals \[2 [2]].
The maximum marginal relevance algorithm is as follows: $$ \text{{MMR}} = \arg\max\_{d\_i \in D \setminus R} \[ \lambda \cdot Sim\_1(d\_i, q) - (1 - \lambda) \cdot \max\_{d\_j \in R} Sim\_2(d\_i, d\_j) ] $$
Here, D is the set of all candidate documents, R is the set of already selected documents, q is the query, $Sim\_1$ is the similarity function between a document and the query, and $Sim\_2$ is the similarity function between two documents. $d\_i$ and $d\_j$ are documents in D and R respectively.
The parameter λ (mmr\_threshold) controls the trade-off between relevance (the first term) and diversity (the second term). If mmr\_threshold is close to 1, more emphasis is put on relevance, while a mmr\_threshold close to 0 puts more emphasis on diversity.

``` !mkdir -p 'data/paul_graham/' !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt' ```


# To use mmr, set it as a vector_store_query_mode query_engine = index.as_query_engine(vector_store_query_mode="mmr") response = query_engine.query("What did the author do growing up?") print(response) ```
``` The author wrote short stories and also worked on programming, specifically on an IBM 1401 computer in 9th grade. ```
``` from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
documents = SimpleDirectoryReader("./data/paul_graham/").load_data() index = VectorStoreIndex.from_documents(documents)
# To set the threshold, set it in vector_store_kwargs query_engine_with_threshold = index.as_query_engine( vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.2} )
response = query_engine_with_threshold.query( "What did the author do growing up?" ) print(response) ```
``` The author wrote short stories and also worked on programming, specifically on an IBM 1401 computer in 9th grade. They later got a microcomputer, a TRS-80, and started programming more extensively, including writing simple games and a word processor. ```
Note that the node score will be scaled with the threshold and will additionally be penalized for the similarity to previous nodes. As the threshold goes to 1, the scores will become equal and similarity to previous nodes will be ignored, turning off the impact of MMR. By lowering the threshold, the algorithm will prefer more diverse documents.
``` index1 = VectorStoreIndex.from_documents(documents) query_engine_no_mrr = index1.as_query_engine() response_no_mmr = query_engine_no_mrr.query( "What did the author do growing up?" )
index2 = VectorStoreIndex.from_documents(documents) query_engine_with_high_threshold = index2.as_query_engine( vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.8} ) response_low_threshold = query_engine_with_high_threshold.query( "What did the author do growing up?" )

index3 = VectorStoreIndex.from_documents(documents) query_engine_with_low_threshold = index3.as_query_engine( vector_store_query_mode="mmr", vector_store_kwargs={"mmr_threshold": 0.2} ) response_high_threshold = query_engine_with_low_threshold.query( "What did the author do growing up?" )

print( "Scores without MMR ", [node.score for node in response_no_mmr.source_nodes], ) print( "Scores with MMR and a threshold of 0.8 ", [node.score for node in response_high_threshold.source_nodes], ) print( "Scores with MMR and a threshold of 0.2 ", [node.score for node in response_low_threshold.source_nodes], ) ```

``` Scores without MMR [0.38770109812709, 0.38159007522004046] Scores with MMR and a threshold of 0.8 [0.07754021962541802, -0.31606868760500917] Scores with MMR and a threshold of 0.2 [0.31016236260600616, 0.1845257045929435] ```
## Retrieval-Only Demonstration
By setting a small chunk size and adjusting the “mmr\_threshold” parameter, we can see how the retrieved results change from very diverse (and less relevant) to less diverse (and more relevant/redundant).
We try the following values: 0.1, 0.5, 0.8, 1.0
llama\_index/docs/examples/data/paul\_graham
``` documents = SimpleDirectoryReader("../data/paul_graham/").load_data() index = VectorStoreIndex.from_documents( documents, ) ```
``` retriever = index.as_retriever( vector_store_query_mode="mmr", similarity_top_k=3, vector_store_kwargs={"mmr_threshold": 0.1}, ) nodes = retriever.retrieve( "What did the author do during his time in Y Combinator?" ) ```

``` from llama_index.core.response.notebook_utils import display_source_node
for n in nodes: display_source_node(n, source_length=1000) ```
**Node ID:** 72313b35-f0dc-4abb-919c-a440aebf0398\ **Similarity:** 0.05985031885642464\ **Text:** As Jessica and I were walking home from dinner on March 11, at the corner of Garden and Walker streets, these three threads converged. Screw the VCs who were taking so long to make up their minds. We’d start our own investment firm and actually implement the ideas we’d been talking about. I’d fund it, and Jessica could quit her job and work for it, and we’d get Robert and Trevor as partners too. \[13]

**Node ID:** d18deb5b-7d2a-4d3d-a30f-a180a1cb7015\ **Similarity:** -0.38235343418846846\ **Text:** I didn’t want to drop out of grad school, but how else was I going to get out? I remember when my friend Robert Morris got kicked out of Cornell for writing the internet worm of 1988, I was envious that he’d found such a spectacular way to get out of grad school.

Then one day in April 1990 a crack appeared in the wall. I ran into professor Cheatham and he asked if I was far enough along to graduate that June. I didn’t have a word of my dissertation written, but in what must have been the quickest bit of thinking in my life, I decided to take a shot at writing one in the 5 weeks or so that remained before the deadline, reusing parts of On Lisp where I could, and I was able to respond, with no perceptible delay “Yes, I think so. I’ll give you something to read in a few days.”
I picked applications of continuations as the topic. In retrospect I should have written about macros and embedded languages. There’s a whole world there that’s barely been explored. But all I wanted was to get…
**Node ID:** 13c6f611-ac9f-47af-b76d-7e40ea16f7ed\ **Similarity:** -0.3384054315291212\ **Text:** \[18] The worst thing about leaving YC was not working with Jessica anymore. We’d been working on YC almost the whole time we’d known each other, and we’d neither tried nor wanted to separate it from our personal lives, so leaving was like pulling up a deeply rooted tree.

``` retriever = index.as_retriever( vector_store_query_mode="mmr", similarity_top_k=3, vector_store_kwargs={"mmr_threshold": 0.5}, ) nodes = retriever.retrieve( "What did the author do during his time in Y Combinator?" ) ```

**Node ID:** 72313b35-f0dc-4abb-919c-a440aebf0398\ **Similarity:** 0.29925159428212317\ **Text:** As Jessica and I were walking home from dinner on March 11, at the corner of Garden and Walker streets, these three threads converged. Screw the VCs who were taking so long to make up their minds. We’d start our own investment firm and actually implement the ideas we’d been talking about. I’d fund it, and Jessica could quit her job and work for it, and we’d get Robert and Trevor as partners too. \[13]

**Node ID:** 13c6f611-ac9f-47af-b76d-7e40ea16f7ed\ **Similarity:** -0.06720844682537574\ **Text:** \[18] The worst thing about leaving YC was not working with Jessica anymore. We’d been working on YC almost the whole time we’d known each other, and we’d neither tried nor wanted to separate it from our personal lives, so leaving was like pulling up a deeply rooted tree.
\[19] One way to get more precise about the concept of invented vs discovered is to talk about space aliens. Any sufficiently advanced alien civilization would certainly know about the Pythagorean theorem, for example. I believe, though with less certainty, that they would also know about the Lisp in McCarthy’s 1960 paper.
But if so there’s no reason to suppose that this is the limit of the language that might be known to them. Presumably aliens need numbers and errors and I/O too. So it seems likely there exists at least one path out of McCarthy’s Lisp along which discoveredness is preserved.
Thanks to Trevor Blackwell, John Collison, Patrick Collison, Daniel Gackle, Ralph Hazell, Jessica Livingston, Robert Mor…
**Node ID:** 6a638da9-f42f-4be6-a415-9698fd9636f9\ **Similarity:** 0.036928354116716855\ **Text:** Meanwhile I’d been hearing more and more about this new thing called the World Wide Web. Robert Morris showed it to me when I visited him in Cambridge, where he was now in grad school at Harvard. It seemed to me that the web would be a big deal. I’d seen what graphical user interfaces had done for the popularity of microcomputers. It seemed like the web would do the same for the internet.
If I wanted to get rich, here was the next train leaving the station. I was right about that part. What I got wrong was the idea. I decided we should start a company to put art galleries online. I can’t honestly say, after reading so many Y Combinator applications, that this was the worst startup idea ever, but it was up there. Art galleries didn’t want to be online, and still don’t, not the fancy ones. That’s not how they sell. I wrote some software to generate web sites for galleries, and Robert wrote some to resize images and set up an http server to serve the pages. Then we tried to sign up ga…
``` retriever = index.as_retriever( vector_store_query_mode="mmr", similarity_top_k=3, vector_store_kwargs={"mmr_threshold": 0.8}, ) nodes = retriever.retrieve( "What did the author do during his time in Y Combinator?" ) ```

**Node ID:** 72313b35-f0dc-4abb-919c-a440aebf0398\ **Similarity:** 0.4788025508513971\ **Text:** As Jessica and I were walking home from dinner on March 11, at the corner of Garden and Walker streets, these three threads converged. Screw the VCs who were taking so long to make up their minds. We’d start our own investment firm and actually implement the ideas we’d been talking about. I’d fund it, and Jessica could quit her job and work for it, and we’d get Robert and Trevor as partners too. \[13]

**Node ID:** 555f8603-79f5-424c-bfef-b7a8d9523d4c\ **Similarity:** 0.30086405397508975\ **Text:** \[15] We got 225 applications for the Summer Founders Program, and we were surprised to find that a lot of them were from people who’d already graduated, or were about to that spring. Already this SFP thing was starting to feel more serious than we’d intended.

**Node ID:** d1a19a77-93e2-4f5b-8eb2-b7f265f15ec2\ **Similarity:** 0.29257547208236784\ **Text:** It’s not that unprestigious types of work are good per se. But when you find yourself drawn to some kind of work despite its current lack of prestige, it’s a sign both that there’s something real to be discovered there, and that you have the right kind of motives. Impure motives are a big danger for the ambitious. If anything is going to lead you astray, it will be the desire to impress people. So while working on things that aren’t prestigious doesn’t guarantee you’re on the right track, it at least guarantees you’re not on the most common type of wrong one.
Over the next several years I wrote lots of essays about all kinds of different topics. O’Reilly reprinted a collection of them as a book, called Hackers & Painters after one of the essays in it. I also worked on spam filters, and did some more painting. I used to have dinners for a group of friends every thursday night, which taught me how to cook for groups. And I bought another building in Cambridge, a former candy factory …
``` retriever = index.as_retriever( vector_store_query_mode="mmr", similarity_top_k=3, vector_store_kwargs={"mmr_threshold": 1.0}, ) nodes = retriever.retrieve( "What did the author do during his time in Y Combinator?" ) ```

``` for n in nodes: display_source_node(n, source_length=1000) ```
**Node ID:** 72313b35-f0dc-4abb-919c-a440aebf0398\ **Similarity:** 0.5985031885642463\ **Text:** As Jessica and I were walking home from dinner on March 11, at the corner of Garden and Walker streets, these three threads converged. Screw the VCs who were taking so long to make up their minds. We’d start our own investment firm and actually implement the ideas we’d been talking about. I’d fund it, and Jessica could quit her job and work for it, and we’d get Robert and Trevor as partners too. \[13]
Once again, ignorance worked in our favor. We had no idea how to be angel investors, and in Boston in 2005 there were no Ron Conways to learn from. So we just made what seemed like the obvious choices, and some of the things we did turned out to be novel.
There are multiple components to Y Combinator, and we didn’t figure them all out at once. The part we got first was to be an angel firm. In those days, those two words didn’t go together. There were VC firms, which were organized companies with people whose job it was to make investments, but they only did big, million dollar investm…
**Node ID:** 555f8603-79f5-424c-bfef-b7a8d9523d4c\ **Similarity:** 0.5814802966348447\ **Text:** \[15] We got 225 applications for the Summer Founders Program, and we were surprised to find that a lot of them were from people who’d already graduated, or were about to that spring. Already this SFP thing was starting to feel more serious than we’d intended.
We invited about 20 of the 225 groups to interview in person, and from those we picked 8 to fund. They were an impressive group. That first batch included reddit, Justin Kan and Emmett Shear, who went on to found Twitch, Aaron Swartz, who had already helped write the RSS spec and would a few years later become a martyr for open access, and Sam Altman, who would later become the second president of YC. I don’t think it was entirely luck that the first batch was so good. You had to be pretty bold to sign up for a weird thing like the Summer Founders Program instead of a summer job at a legit place like Microsoft or Goldman Sachs.
The deal for startups was based on a combination of the deal we did with Julian ($10k for 10%) and …
**Node ID:** 23010353-0f2b-4c4f-9ff0-7c1f1201edac\ **Similarity:** 0.562748668285032\ **Text:** When I was dealing with some urgent problem during YC, there was about a 60% chance it had to do with HN, and a 40% chance it had do with everything else combined. \[17]
As well as HN, I wrote all of YC’s internal software in Arc. But while I continued to work a good deal in Arc, I gradually stopped working on Arc, partly because I didn’t have time to, and partly because it was a lot less attractive to mess around with the language now that we had all this infrastructure depending on it. So now my three projects were reduced to two: writing essays and working on YC.
YC was different from other kinds of work I’ve done. Instead of deciding for myself what to work on, the problems came to me. Every 6 months there was a new batch of startups, and their problems, whatever they were, became our problems. It was very engaging work, because their problems were quite varied, and the good founders were very effective. If you were trying to learn the most you could about startups in the short…

[1] https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
[2] https://arxiv.org/pdf/2211.13892.pdf