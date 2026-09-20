# TypeSafe AI 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://docs.typesafe.ai>
- 文档数：109

## 顶层目录

- `(root)`：4 篇
- `Concepts`：5 篇
- `Cookbooks`：18 篇
- `Demos`：2 篇
- `Getting Started`：3 篇
- `Model Jaggedness`：1 篇
- `Patterns`：5 篇
- `Primitives`：5 篇
- `SDKs`：66 篇

## 目录树

```text
docs/
├── Concepts
│   ├── Confidence.md
│   ├── Example use cases.md
│   ├── How to build with TypeSafe.md
│   ├── State.md
│   └── System One.md
├── Cookbooks
│   ├── Autoresearch feature discovery.md
│   ├── Classification using confidence.md
│   ├── Classifying RAG passages.md
│   ├── Date extraction.md
│   ├── Double-checking citations.md
│   ├── Function calling.md
│   ├── Guardrails for LLMs.md
│   ├── Hierarchical classification.md
│   ├── Knowledge graph entity alignment.md
│   ├── Line-by-line search.md
│   ├── Parallel questions.md
│   ├── Pre-parsed value extraction.md
│   ├── Re-ranking.md
│   ├── SDE cascade.md
│   ├── Self-consistency choices.md
│   ├── Self-consistency nouls.md
│   ├── Skill suggestion.md
│   └── Structure recovery.md
├── Demos
│   ├── Demos.md
│   └── Smart home assistant demo.md
├── Getting Started
│   ├── AI primer.md
│   ├── Introduction.md
│   └── Quick start.md
├── Model Jaggedness
│   └── Jev 1.13 jaggedness.md
├── Patterns
│   ├── Composite scoring.md
│   ├── Confidence-gated routing.md
│   ├── Intent routing.md
│   ├── Patterns.md
│   └── Speculative fan-out.md
├── Primitives
│   ├── Advanced structure.md
│   ├── Choice.md
│   ├── Noul.md
│   ├── Primitives (Questions).md
│   └── Score.md
├── SDKs
│   ├── JavaScript
│   │   ├── API
│   │   │   ├── Classes
│   │   │   │   ├── Class APIConnectionError.md
│   │   │   │   ├── Class APIError.md
│   │   │   │   ├── Class APIPromise T.md
│   │   │   │   ├── Class APITimeoutError.md
│   │   │   │   ├── Class APIUserAbortError.md
│   │   │   │   ├── Class AuthenticationError.md
│   │   │   │   ├── Class BadRequestError.md
│   │   │   │   ├── Class InternalServerError.md
│   │   │   │   ├── Class NotFoundError.md
│   │   │   │   ├── Class PermissionDeniedError.md
│   │   │   │   ├── Class RateLimitError.md
│   │   │   │   ├── Class TypeSafeClient.md
│   │   │   │   ├── Class TypeSafeError.md
│   │   │   │   └── Class UnprocessableEntityError.md
│   │   │   ├── Functions
│   │   │   │   ├── Function choice().md
│   │   │   │   ├── Function noul().md
│   │   │   │   └── Function score().md
│   │   │   ├── Interfaces
│   │   │   │   ├── Interface ChoiceQuestion T.md
│   │   │   │   ├── Interface ChoiceResponse T.md
│   │   │   │   ├── Interface Logger.md
│   │   │   │   ├── Interface ModelCard.md
│   │   │   │   ├── Interface Models.md
│   │   │   │   ├── Interface NoulQuestion.md
│   │   │   │   ├── Interface NoulResponse.md
│   │   │   │   ├── Interface Questions.md
│   │   │   │   ├── Interface RequestOptions.md
│   │   │   │   ├── Interface RetryPolicy.md
│   │   │   │   ├── Interface ScoreQuestion T.md
│   │   │   │   ├── Interface ScoreResponse T.md
│   │   │   │   ├── Interface SystemOneRequest Q.md
│   │   │   │   ├── Interface SystemOneRequestPayload.md
│   │   │   │   ├── Interface SystemOneResult Q.md
│   │   │   │   ├── Interface TypeSafeClientConfig.md
│   │   │   │   ├── Interface Usage.md
│   │   │   │   └── Interface WithResponse T.md
│   │   │   ├── Type Aliases
│   │   │   │   ├── Type Alias ChoiceCriteria.md
│   │   │   │   ├── Type Alias Description.md
│   │   │   │   ├── Type Alias EntryType.md
│   │   │   │   ├── Type Alias EnvVar.md
│   │   │   │   ├── Type Alias Fetch.md
│   │   │   │   ├── Type Alias JsonValue.md
│   │   │   │   ├── Type Alias LogLevel.md
│   │   │   │   ├── Type Alias Question.md
│   │   │   │   ├── Type Alias ResultFor T.md
│   │   │   │   ├── Type Alias ScoreCriteria.md
│   │   │   │   ├── Type Alias ScoreLegend T.md
│   │   │   │   └── Type Alias ScoreOf T.md
│   │   │   └── Variables
│   │   │       ├── Variable ENV.md
│   │   │       ├── Variable LOG_LEVELS.md
│   │   │       └── Variable VERSION.md
│   │   ├── API reference.md
│   │   ├── Changelog.md
│   │   └── JavaScript SDK.md
│   ├── Python
│   │   ├── API
│   │   │   ├── Clients
│   │   │   │   ├── Async client.md
│   │   │   │   └── Sync client.md
│   │   │   ├── Types
│   │   │   │   ├── Answers and responses.md
│   │   │   │   ├── Common types.md
│   │   │   │   └── Questions.md
│   │   │   ├── Constants.md
│   │   │   ├── Exceptions.md
│   │   │   └── Retries.md
│   │   ├── API reference.md
│   │   ├── Changelog.md
│   │   ├── TypeSafe Python SDK.md
│   │   └── Usage.md
│   └── Client SDKs.md
├── Agent skill.md
├── API reference.md
├── Legal.md
└── Models.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `API reference.md` | API reference | Full HTTP API reference for the TypeSafe evaluation endpoint. | [原文](<https://docs.typesafe.ai/api>) |
| `Agent skill.md` | Agent skill | Drop-in skill for Claude Code, Codex, and other agent environments. | [原文](<https://docs.typesafe.ai/agent-skill>) |
| `Concepts/Confidence.md` | Confidence | How TypeSafe reports certainty, how it differs from probability, and how to use it to control system behavior. | [原文](<https://docs.typesafe.ai/confidence>) |
| `Concepts/Example use cases.md` | Example use cases | Explore TypeSafe use cases by industry and turn promising ideas into software workflows. | [原文](<https://docs.typesafe.ai/concepts/use-case-map>) |
| `Concepts/How to build with TypeSafe.md` | How to build with TypeSafe | Design AI-powered software by keeping code in control and giving System One narrow, structured decisions. | [原文](<https://docs.typesafe.ai/concepts/how-to-build-with-system-one>) |
| `Concepts/State.md` | State | What state is, how to structure it, and how to give a System One model the context it needs. | [原文](<https://docs.typesafe.ai/concepts/state>) |
| `Concepts/System One.md` | System One | System One models make fast, structured decisions for software. Jev is TypeSafe's flagship model and the first System One model. | [原文](<https://docs.typesafe.ai/concepts/system-one>) |
| `Cookbooks/Autoresearch feature discovery.md` | Autoresearch feature discovery | Runs an autoresearch loop that proposes TypeSafe questions, converts free text into numeric features, and uses model errors to improve a supervised CatBoost regressor. | [原文](<https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery>) |
| `Cookbooks/Classification using confidence.md` | Classification using confidence | Classify SEC annual reports into 75 industry groups with one Choice each, then read the answer's own confidence to decide whether to report that group or the broader division above it. | [原文](<https://docs.typesafe.ai/cookbooks/classification_using_confidence>) |
| `Cookbooks/Classifying RAG passages.md` | Classifying RAG passages | Score each retrieved passage with one TypeSafe request, then decide in code which ones reach the answering model. For example, keep and flag ones that contradict the question, and drop ones carrying a hidden instruction or prompt injection. | [原文](<https://docs.typesafe.ai/cookbooks/classifying_rag_passages>) |
| `Cookbooks/Date extraction.md` | Date extraction | Extracts absolute and relative dates by asking TypeSafe for the parts named in a document, then resolving and validating them in code with confidence-based review. | [原文](<https://docs.typesafe.ai/cookbooks/date_extraction_cookbook>) |
| `Cookbooks/Double-checking citations.md` | Double-checking citations | Catch wrong or hallucinated citations by checking against the source document. One TypeSafe Choice question decides whether the quote's context supports the claim, and its confidence can flag the citation for human review. | [原文](<https://docs.typesafe.ai/cookbooks/citation_check>) |
| `Cookbooks/Function calling.md` | Function calling | Turns natural-language trading requests into calls to ordinary typed functions by mapping function names and closed-set arguments to confidence-aware TypeSafe questions. | [原文](<https://docs.typesafe.ai/cookbooks/function_calling>) |
| `Cookbooks/Guardrails for LLMs.md` | Guardrails for LLMs | Screen every message going into and out of an LLM app with one TypeSafe request, describing possible hazards ('is this a jailbreak attempt?') and scoring severity ('how much harm would complying do?'). Threshold the probabilities it hands back and you decide whether to pass, review, block, or route a message to support. | [原文](<https://docs.typesafe.ai/cookbooks/llm_guardrails>) |
| `Cookbooks/Hierarchical classification.md` | Hierarchical classification | Classifies documents through deep patent, retail product, biomedical, and source-code hierarchies using parallel beam search over TypeSafe Choice probabilities. | [原文](<https://docs.typesafe.ai/cookbooks/hierarchical_classification>) |
| `Cookbooks/Knowledge graph entity alignment.md` | Knowledge graph entity alignment | Decides which of 450 candidate pairs from two beer catalogues describe the same product. One TypeSafe Score question carries the whole decision, because its three levels are the three things you can do with a pair: merge it, leave it unlinked, or hand it to a curator. There is no threshold to fit, and three Noul questions ride along in the same request to tell the curator which field the two sources disagree on. | [原文](<https://docs.typesafe.ai/cookbooks/entity_alignment>) |
| `Cookbooks/Line-by-line search.md` | Line-by-line search | Build semantic search for GitHub's Terms of Service. In one request, score 218 line ids against a plain-language query with a Choice question, and use a Noul question to check whether the document contains an answer. | [原文](<https://docs.typesafe.ai/cookbooks/semantic_find>) |
| `Cookbooks/Parallel questions.md` | Parallel questions | Runs a 13-question regulatory briefing over the GDPR Wikipedia article, showing that batching every question into one TypeSafe call is 12.2x cheaper and 10.0x faster with no change in answers. | [原文](<https://docs.typesafe.ai/cookbooks/parallel_questions>) |
| `Cookbooks/Pre-parsed value extraction.md` | Pre-parsed value extraction | Uses regexes to find candidate emails, phone numbers, and amounts, then has TypeSafe select the requested span so code can normalize a verbatim value. | [原文](<https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook>) |
| `Cookbooks/Re-ranking.md` | Re-ranking | Builds 30-passage BM25 shortlists for 40 CLERC legal queries, then uses one TypeSafe question per query-candidate pair to raise top-1 accuracy from 5% to 18% and top-10 accuracy from 38% to 62%. | [原文](<https://docs.typesafe.ai/cookbooks/rerank_typesafe>) |
| `Cookbooks/SDE cascade.md` | SDE cascade | Uses a 2-stage structured-data-extraction cascade (mini → verify → reasoning) to get most of the quality of a big reasoning model at a fraction of the cost. | [原文](<https://docs.typesafe.ai/cookbooks/sde_cascade>) |
| `Cookbooks/Self-consistency choices.md` | Self-consistency: choices | Add an uncertain outcome to moderation decisions and compare label agreement with the share of automatic actions. | [原文](<https://docs.typesafe.ai/cookbooks/consistency_choice_cookbook>) |
| `Cookbooks/Self-consistency nouls.md` | Self-consistency: nouls | Route uncertain probabilities to human review while keeping the underlying noul values visible. | [原文](<https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook>) |
| `Cookbooks/Skill suggestion.md` | Skill suggestion | Picks at most one skill for an agent turn out of the 182 in Nous Research's Hermes catalog: one TypeSafe request ranks every skill and asks whether the turn needs one at all, a second reads the top three properly and can reject all of them. The winner's name goes into a single line of the agent's system prompt, and both the wrong skills it loads and the ones it loads when nothing fits drop by more than half. | [原文](<https://docs.typesafe.ai/cookbooks/skill_suggestion>) |
| `Cookbooks/Structure recovery.md` | Structure recovery | Reconstructs Markdown from plain text that lost its formatting in two requests: one stitches hard-wrapped lines back together, one classifies every block (heading, list, code, callout) with companion questions read only when relevant. | [原文](<https://docs.typesafe.ai/cookbooks/autoformat>) |
| `Demos/Demos.md` | Demos | Interactive examples showing what's possible with TypeSafe. | [原文](<https://docs.typesafe.ai/demos>) |
| `Demos/Smart home assistant demo.md` | Smart home assistant demo | Demo code: a smart home assistant that uses TypeSafe to evaluate user requests. | [原文](<https://docs.typesafe.ai/demos/smart-home>) |
| `Getting Started/AI primer.md` | AI primer | Why TypeSafe trains decision models with calibrated probabilities instead of optimizing for generated text. | [原文](<https://docs.typesafe.ai/introduction/machine-learning-primer>) |
| `Getting Started/Introduction.md` | Introduction | Jev is TypeSafe's flagship model and the first System One model. Send state and typed questions; get structured answers your code can use directly. | [原文](<https://docs.typesafe.ai/introduction>) |
| `Getting Started/Quick start.md` | Quick start | Prefer to just dive in? Here's everything you need to get started immediately. | [原文](<https://docs.typesafe.ai/introduction/quickstart>) |
| `Legal.md` | Legal | Legal documents and policies for TypeSafe. | [原文](<https://docs.typesafe.ai/legal>) |
| `Model Jaggedness/Jev 1.13 jaggedness.md` | Jev 1.13 jaggedness | Jev isn't perfect. Here are some jagged edges we are aware of with jev-1.13. Many of these will be fixed in later versions. | [原文](<https://docs.typesafe.ai/model-jaggedness/jev-1.13>) |
| `Models.md` | Models |  | [原文](<https://docs.typesafe.ai/models>) |
| `Patterns/Composite scoring.md` | Composite scoring | Break a complex judgment into atomic scores, combine with weights you control in code. | [原文](<https://docs.typesafe.ai/patterns/composite-scoring>) |
| `Patterns/Confidence-gated routing.md` | Confidence-gated routing | Use confidence as a second axis. The answer tells you what; confidence tells you whether to act. | [原文](<https://docs.typesafe.ai/patterns/confidence-routing>) |
| `Patterns/Intent routing.md` | Intent routing | Classify incoming requests and route each to the optimal handler: deterministic logic, a specialist LLM, or a human. | [原文](<https://docs.typesafe.ai/patterns/intent-routing>) |
| `Patterns/Patterns.md` | Patterns | Architectural patterns for building systems with TypeSafe. | [原文](<https://docs.typesafe.ai/patterns>) |
| `Patterns/Speculative fan-out.md` | Speculative fan-out | Send many questions in a single call, including speculative ones, and let your code decide what's relevant. | [原文](<https://docs.typesafe.ai/patterns/fan-out>) |
| `Primitives/Advanced structure.md` | Advanced: structure | Instructions, Choice options, Score levels, and Noul criteria all accept JSON structure. | [原文](<https://docs.typesafe.ai/primitives/advanced>) |
| `Primitives/Choice.md` | Choice | A Choice is a System One question type for selecting one option from a defined set. The answer includes the selected option, a probability for each option, and confidence. | [原文](<https://docs.typesafe.ai/primitives/choice>) |
| `Primitives/Noul.md` | Noul | A Noul question asks the TypeSafe model to evaluate a yes/no question and return the probability that the answer is yes. | [原文](<https://docs.typesafe.ai/primitives/noul>) |
| `Primitives/Primitives (Questions).md` | Primitives (Questions) | The three TypeSafe question types (Choice, Score, Noul), the typed answers they return, how to choose between them, and how to ask several at once. | [原文](<https://docs.typesafe.ai/primitives>) |
| `Primitives/Score.md` | Score | A Score is a System One question type for rating content against ordered, descriptive levels. The answer includes a score, a probability for each level, and confidence. | [原文](<https://docs.typesafe.ai/primitives/score>) |
| `SDKs/Client SDKs.md` | Client SDKs | Install a TypeSafe client SDK and use typed questions and answers in your application. | [原文](<https://docs.typesafe.ai/sdk>) |
| `SDKs/JavaScript/API reference.md` | API reference |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api>) |
| `SDKs/JavaScript/API/Classes/Class APIConnectionError.md` | Class: APIConnectionError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/APIConnectionError>) |
| `SDKs/JavaScript/API/Classes/Class APIError.md` | Class: APIError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/APIError>) |
| `SDKs/JavaScript/API/Classes/Class APIPromise T.md` | Class: APIPromise<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/APIPromise>) |
| `SDKs/JavaScript/API/Classes/Class APITimeoutError.md` | Class: APITimeoutError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/APITimeoutError>) |
| `SDKs/JavaScript/API/Classes/Class APIUserAbortError.md` | Class: APIUserAbortError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/APIUserAbortError>) |
| `SDKs/JavaScript/API/Classes/Class AuthenticationError.md` | Class: AuthenticationError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/AuthenticationError>) |
| `SDKs/JavaScript/API/Classes/Class BadRequestError.md` | Class: BadRequestError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/BadRequestError>) |
| `SDKs/JavaScript/API/Classes/Class InternalServerError.md` | Class: InternalServerError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/InternalServerError>) |
| `SDKs/JavaScript/API/Classes/Class NotFoundError.md` | Class: NotFoundError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/NotFoundError>) |
| `SDKs/JavaScript/API/Classes/Class PermissionDeniedError.md` | Class: PermissionDeniedError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/PermissionDeniedError>) |
| `SDKs/JavaScript/API/Classes/Class RateLimitError.md` | Class: RateLimitError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/RateLimitError>) |
| `SDKs/JavaScript/API/Classes/Class TypeSafeClient.md` | Class: TypeSafeClient |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/TypeSafeClient>) |
| `SDKs/JavaScript/API/Classes/Class TypeSafeError.md` | Class: TypeSafeError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/TypeSafeError>) |
| `SDKs/JavaScript/API/Classes/Class UnprocessableEntityError.md` | Class: UnprocessableEntityError |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/classes/UnprocessableEntityError>) |
| `SDKs/JavaScript/API/Functions/Function choice().md` | Function: choice() |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/functions/choice>) |
| `SDKs/JavaScript/API/Functions/Function noul().md` | Function: noul() |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/functions/noul>) |
| `SDKs/JavaScript/API/Functions/Function score().md` | Function: score() |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/functions/score>) |
| `SDKs/JavaScript/API/Interfaces/Interface ChoiceQuestion T.md` | Interface: ChoiceQuestion<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/ChoiceQuestion>) |
| `SDKs/JavaScript/API/Interfaces/Interface ChoiceResponse T.md` | Interface: ChoiceResponse<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/ChoiceResponse>) |
| `SDKs/JavaScript/API/Interfaces/Interface Logger.md` | Interface: Logger |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/Logger>) |
| `SDKs/JavaScript/API/Interfaces/Interface ModelCard.md` | Interface: ModelCard |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/ModelCard>) |
| `SDKs/JavaScript/API/Interfaces/Interface Models.md` | Interface: Models |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/Models>) |
| `SDKs/JavaScript/API/Interfaces/Interface NoulQuestion.md` | Interface: NoulQuestion |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/NoulQuestion>) |
| `SDKs/JavaScript/API/Interfaces/Interface NoulResponse.md` | Interface: NoulResponse |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/NoulResponse>) |
| `SDKs/JavaScript/API/Interfaces/Interface Questions.md` | Interface: Questions |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/Questions>) |
| `SDKs/JavaScript/API/Interfaces/Interface RequestOptions.md` | Interface: RequestOptions |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/RequestOptions>) |
| `SDKs/JavaScript/API/Interfaces/Interface RetryPolicy.md` | Interface: RetryPolicy |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/RetryPolicy>) |
| `SDKs/JavaScript/API/Interfaces/Interface ScoreQuestion T.md` | Interface: ScoreQuestion<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/ScoreQuestion>) |
| `SDKs/JavaScript/API/Interfaces/Interface ScoreResponse T.md` | Interface: ScoreResponse<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/ScoreResponse>) |
| `SDKs/JavaScript/API/Interfaces/Interface SystemOneRequest Q.md` | Interface: SystemOneRequest<Q> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/SystemOneRequest>) |
| `SDKs/JavaScript/API/Interfaces/Interface SystemOneRequestPayload.md` | Interface: SystemOneRequestPayload |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/SystemOneRequestPayload>) |
| `SDKs/JavaScript/API/Interfaces/Interface SystemOneResult Q.md` | Interface: SystemOneResult<Q> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/SystemOneResult>) |
| `SDKs/JavaScript/API/Interfaces/Interface TypeSafeClientConfig.md` | Interface: TypeSafeClientConfig |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/TypeSafeClientConfig>) |
| `SDKs/JavaScript/API/Interfaces/Interface Usage.md` | Interface: Usage |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/Usage>) |
| `SDKs/JavaScript/API/Interfaces/Interface WithResponse T.md` | Interface: WithResponse<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/interfaces/WithResponse>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias ChoiceCriteria.md` | Type Alias: ChoiceCriteria |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ChoiceCriteria>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias Description.md` | Type Alias: Description |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/Description>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias EntryType.md` | Type Alias: EntryType |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/EntryType>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias EnvVar.md` | Type Alias: EnvVar |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/EnvVar>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias Fetch.md` | Type Alias: Fetch |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/Fetch>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias JsonValue.md` | Type Alias: JsonValue |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/JsonValue>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias LogLevel.md` | Type Alias: LogLevel |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/LogLevel>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias Question.md` | Type Alias: Question |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/Question>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias ResultFor T.md` | Type Alias: ResultFor<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ResultFor>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias ScoreCriteria.md` | Type Alias: ScoreCriteria |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ScoreCriteria>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias ScoreLegend T.md` | Type Alias: ScoreLegend<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ScoreLegend>) |
| `SDKs/JavaScript/API/Type Aliases/Type Alias ScoreOf T.md` | Type Alias: ScoreOf<T> |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/type-aliases/ScoreOf>) |
| `SDKs/JavaScript/API/Variables/Variable ENV.md` | Variable: ENV |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/variables/ENV>) |
| `SDKs/JavaScript/API/Variables/Variable LOG_LEVELS.md` | Variable: LOG_LEVELS |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/variables/LOG_LEVELS>) |
| `SDKs/JavaScript/API/Variables/Variable VERSION.md` | Variable: VERSION |  | [原文](<https://docs.typesafe.ai/sdk/javascript/api/variables/VERSION>) |
| `SDKs/JavaScript/Changelog.md` | Changelog |  | [原文](<https://docs.typesafe.ai/sdk/javascript/changelog>) |
| `SDKs/JavaScript/JavaScript SDK.md` | JavaScript SDK |  | [原文](<https://docs.typesafe.ai/sdk/javascript>) |
| `SDKs/Python/API reference.md` | API reference | Python clients for the TypeSafe AI API | [原文](<https://docs.typesafe.ai/sdk/python/api>) |
| `SDKs/Python/API/Clients/Async client.md` | Async client | Use AsyncTypeSafeClient to ask questions, list models, and configure asynchronous TypeSafe API requests. | [原文](<https://docs.typesafe.ai/sdk/python/api/clients/async>) |
| `SDKs/Python/API/Clients/Sync client.md` | Sync client | Use TypeSafeClient to ask questions, list models, and configure synchronous TypeSafe API requests. | [原文](<https://docs.typesafe.ai/sdk/python/api/clients/sync>) |
| `SDKs/Python/API/Constants.md` | Constants | Default settings and environment variable names for the TypeSafe Python SDK. | [原文](<https://docs.typesafe.ai/sdk/python/api/constants>) |
| `SDKs/Python/API/Exceptions.md` | Exceptions | Handle TypeSafe API errors, rate limits, connection failures, and timeouts. | [原文](<https://docs.typesafe.ai/sdk/python/api/exceptions>) |
| `SDKs/Python/API/Retries.md` | Retries | Configure retries with RetryPolicy — attempt count, retryable statuses, backoff, and retry headers handling. | [原文](<https://docs.typesafe.ai/sdk/python/api/retries>) |
| `SDKs/Python/API/Types/Answers and responses.md` | Answers and responses | Read answers, confidence scores, token usage, and available models returned by the TypeSafe API. | [原文](<https://docs.typesafe.ai/sdk/python/api/types/responses>) |
| `SDKs/Python/API/Types/Common types.md` | Common types | Common types for TypeSafe API SDK. | [原文](<https://docs.typesafe.ai/sdk/python/api/types/common>) |
| `SDKs/Python/API/Types/Questions.md` | Questions | Provide state and ask yes/no, choice, and score questions using objects or dictionaries. | [原文](<https://docs.typesafe.ai/sdk/python/api/types/questions>) |
| `SDKs/Python/Changelog.md` | Changelog | Python clients for the TypeSafe AI API | [原文](<https://docs.typesafe.ai/sdk/python/changelog>) |
| `SDKs/Python/TypeSafe Python SDK.md` | TypeSafe Python SDK | Install the TypeSafe Python SDK and get started with asynchronous or synchronous API calls. | [原文](<https://docs.typesafe.ai/sdk/python>) |
| `SDKs/Python/Usage.md` | Usage | Guides and patterns for working with the TypeSafe Python SDK. | [原文](<https://docs.typesafe.ai/sdk/python/usage>) |
