# Example use cases

> Explore TypeSafe use cases by industry and turn promising ideas into software workflows.

Use this map to brainstorm where TypeSafe could fit in your industry. Open the closest industry, scan the example decisions, and adapt them to the documents and actions in your own workflow.

## Example use case categories

  - **AI Automation Software**: Interleave AI with reliable software in a way where you can run it a million times in the background without a human co-pilot. Code owns control flow (not markdown files) while TypeSafe handles the semantic decisions and language understanding.

  - **Real-time applications**: Frontier intelligence at real-time speeds (150ms) means AI can make decisions faster than human perception. Fast and smart enough to be programmed to play games or embedded into a UI.

  - **AI Map Reduce over Big Data**: 100x cheaper means you can process giant datasets. Search for relevant information over giant corpuses, classify giant agent traces, and extract features to make predictions.

  - **Universal Verification**: Verify the input prompt, extractions, reasoning traces, tool calls, or inputs of any other AI. Detect jailbreaks, citation errors, hallucinations, mistakes, or other error-modes that other AIs or LLMs make at a fraction of the cost for the actual LLM call.

  - **Harness Engineering**: Use Jev queries to make your harness smarter - model routing, semantic context retrieval, LLM error detection and guardrails, reasoning trace classification at lightspeed and a fraction of the cost.

## Example automation use cases


#### Search and retrieval

    * Replace or supplement embeddings in RAG pipelines with semantic search, scoring, and ranking.
    * Score query-to-candidate relevance.
    * Rerank results with pairwise comparisons.
    * Cross-encode queries and candidates for higher precision.
    * Select useful context for downstream AI workflows.



#### Scientific discovery

    * Screen papers against inclusion and exclusion criteria for systematic reviews.
    * Label passages in interview transcripts, open-ended survey responses, and field notes using predefined themes or categories.
    * Check whether cited passages support claims in manuscripts and generated summaries.
    * Flag missing methodological details, such as controls, dataset descriptions, and experimental settings.
    * Identify entities and relationships across papers to build research knowledge graphs, linking findings to supporting passages.



#### Model routing

    * Use Jev to build a custom router that chooses which LLM receives each prompt.
    * Set routing rules and thresholds for your specific workflow.
    * Classify intent and domain.
    * Estimate difficulty and risk.
    * Escalate requests that need a more expensive model.



#### LLM guardrails

    * Place semantic checks on every LLM input, output, and tool call at a fraction of the cost of the LLM call.
    * Detect jailbreaks and prompt injection.
    * Identify policy violations and sensitive-data exposure.
    * Detect tool-call errors and response-quality failures in real time.
    * Log structured check results and probabilities to make AI system and harness failures easier to trace.



#### Semantic code linting

    * Use Jev queries to add automated semantic lints to code and writing.
    * Define checks for your team's coding conventions and writing guidelines.
    * Run these checks in CI and flag violations for review.



#### Feature extraction for predictive modeling

    * Use Jev to extract probabilistic features from natural-language data.
    * Combine these features with structured data to train models for tasks with ground-truth outcomes.
    * Use autoresearch workflows to propose feature definitions and evaluate their predictive value against held-out ground truth.



#### Recruiting

    * Evaluate resumes, applications, and interview feedback against explicit, job-related criteria.
    * Identify relevant experience.
    * Score evidence for required competencies.
    * Match candidates to roles.
    * Route candidates to hiring managers or recruiters.
    * Escalate uncertain cases for human review.



#### Lead generation

    * Match company profiles, executive biographies, and inbound messages to an ideal customer profile.
    * Score industry fit and company maturity.
    * Detect buyer relevance, pain points, and purchase intent.
    * Prioritize and route leads.



#### Customer support

    * Classify incoming tickets by issue, product area, and customer intent.
    * Process call transcripts to extract customer issues, commitments, and follow-up actions.
    * Detect urgency, frustration, churn risk, and refund requests.
    * Route cases to the right team, queue, or automated workflow.
    * Verify support responses against policies and the customer's request.



#### Insurance claims

    * Classify first-notice-of-loss reports, adjuster notes, and supporting documents.
    * Detect claim complexity, missing information, and potential fraud indicators.
    * Prioritize claims for straight-through processing or specialist review.
    * Escalate uncertain or high-risk cases to a human adjuster.



#### Financial crime

    * Evaluate transaction narratives, KYC documents, and alert histories for suspicious characteristics.
    * Match entities across inconsistent names, profiles, and records.
    * Prioritize alerts by risk, relevance, and evidence quality.
    * Route ambiguous cases to investigators for review.



#### Legal and compliance

    * Classify contracts, policies, regulatory filings, and marketing claims.
    * Detect missing clauses, prohibited claims, and policy violations.
    * Verify documents against explicit legal or compliance requirements.
    * Escalate high-risk or uncertain findings to counsel or compliance teams.



#### E-commerce marketplaces

    * Classify and normalize product listings across inconsistent seller catalogs.
    * Extract product attributes from titles and descriptions.
    * Detect prohibited listings, counterfeit signals, review abuse, and policy violations.
    * Rank products and route uncertain listings for human review.



#### Moderation and trust and safety

    * Apply company-specific, nuanced criteria to decide which posts meet your moderation standards.
    * Moderate user content and automated conversations across communities, customer support, and SDR workflows.
    * Detect toxicity, harassment, spam, fraud, unsafe advice, personal-data exposure, opt-out requests, and policy-violating claims.
    * Combine severity and confidence to allow, warn, review, or block content.



#### Advertising

    * Evaluate creative assets, campaign copy, landing pages, and placement context.
    * Classify brand safety and audience suitability.
    * Check regulatory compliance and prohibited claims.
    * Evaluate creative quality and ad-to-landing-page alignment.



#### Gaming

    * Evaluate player reports, in-game chat, reviews, and support conversations.
    * Moderate chat and detect abuse, toxicity, or suspicious behavior.
    * Annotate content and score frustration or engagement.
    * Detect churn signals and route player-support requests.



#### Risk assessment

    * Convert incident reports, claims notes, transaction descriptions, and vendor assessments into probabilistic risk indicators.
    * Use these indicators in insurance and underwriting workflows.
    * Classify risk types and detect suspicious characteristics.
    * Score severity and prioritize review.
    * Extract features for broader risk models.



#### Demand forecasting

    * Enrich forecasting models with semantic signals from customer inquiries, sales notes, product reviews, support tickets, and market reports.
    * Extract purchase intent, urgency, and product interest.
    * Detect supply concerns, competitive pressure, and emerging demand themes.
    * Feed those features into a forecasting model alongside historical time-series data.



#### Graphs and knowledge graphs

    * Annotate and verify knowledge graphs with typed semantic decisions.
    * Classify relationships and entity types.
    * Detect contradictions between records or claims.
    * Support probabilistic traversal and hierarchical classification.


## Example task categories

| Decision shape                 | Reach for it when                                          | Examples                                                                |
| ------------------------------ | ---------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Classification**             | One known category should win                              | Intent, topic, department, risk type, entity type                       |
| **Detection**                  | You need a probability that one property is present        | Spam, fraud, urgency, jailbreaks, sensitive data                        |
| **Scoring**                    | The answer belongs on an ordered rubric                    | Severity, relevance, quality, frustration, suitability                  |
| **Routing**                    | A category selects the next code path                      | Tool use, escalation, model routing, support queues                     |
| **Search**                     | You need to find items that match a natural-language query | Semantic search, document discovery, candidate generation               |
| **Retrieval**                  | A workflow needs the most relevant context or records      | RAG context, evidence retrieval, knowledge lookup                       |
| **Ranking**                    | Items need to be ordered by semantic relevance or quality  | Search results, recommendations, candidate prioritization               |
| **Verification**               | An artifact must be checked for specific failure modes     | Citation support, policy violations, tool-call errors, response quality |
| **ML Feature Extraction**      | A downstream classical ML model needs semantic signals     | Purchase intent, product interest, competitive pressure, churn signals  |
| **Structured Data Extraction** | Known fields must be recovered from unstructured input     | Candidate attributes, order fields, document labels                     |
