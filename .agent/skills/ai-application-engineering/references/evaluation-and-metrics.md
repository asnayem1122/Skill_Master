# AI Evaluation, Metrics & Regression Testing

This reference guides the creation of quantitative evaluation pipelines, golden benchmark datasets, RAG Triad measurements, and CI/CD quality gates.

---

## 1. The Evaluation Pyramid

Do not rely solely on subjective vibe checks or pure LLM-as-a-judge scoring. Structure evaluation across three layers:

```
          ▲
         / \
        /   \     Layer 3: Sampled LLM-as-a-Judge & Human Spot Checks
       /     \    (Faithfulness, G-Eval Rubrics, Nuance)
      /-------\
     /         \   Layer 2: AI Benchmark Evals on Golden Datasets
    /           \  (Retrieval Recall@K, Context Precision, Answer Relevancy)
   /-------------\
  /               \ Layer 1: Deterministic Unit & Contract Tests
 /                 \(JSON Schema validity, HTTP 200, Latency < 2s, Regex)
/-------------------\
```

---

## 2. Core RAG Metrics (The RAG Triad)

When evaluating RAG systems, measure retrieval and generation independently to pinpoint failure modes:

```
          [User Query]
           /        \
 Context  /          \  Answer
Relevance/            \Relevance
        ▼              ▼
[Retrieved Context] ──► [Generated Answer]
         ▲
         │ Faithfulness / Groundedness
         └─────────────────────────────┘
```

### 1. Context Recall & Context Precision (Retrieval Metrics)
- **Context Recall**: Did the retrieval system fetch all chunks necessary to answer the question?
  $$\text{Context Recall} = \frac{|\text{Retrieved Ground Truth Chunks}|}{|\text{Total Ground Truth Chunks}|}$$
- **Context Precision**: Are the relevant chunks positioned near the top of the retrieved list rather than buried at the bottom?
  $$\text{Context Precision@K} = \frac{\sum_{k=1}^K (\text{Precision@}k \times \text{rel}_k)}{\text{Total Relevant Documents}}$$

### 2. Faithfulness (Hallucination Detection)
Measures whether every factual claim in the generated answer is directly entailed by the retrieved context.
- **Algorithm**:
  1. Use an LLM to decompose the generated answer into atomic statements:
     $$\text{Answer} \to \{s_1, s_2, \dots, s_n\}$$
  2. For each statement $s_i$, verify whether the retrieved context entails $s_i$ using Natural Language Inference (NLI).
  3. Compute score:
     $$\text{Faithfulness} = \frac{\text{Number of Entailed Statements}}{\text{Total Statements}}$$
- **Target**: Minimum 0.90 for enterprise production.

### 3. Answer Relevancy
Measures how directly the generated answer addresses the user's specific query. Penalizes evasiveness, boilerplate disclaimers, or irrelevant tangents.

---

## 3. G-Eval: Rubric-Based LLM-as-a-Judge

For domain-specific criteria (e.g. brand tone, clinical accuracy, code safety), use **G-Eval** with explicit rubric definitions and chain-of-thought evaluation steps.

### Rubric Definition Example
```yaml
metric_name: "Technical Accuracy & Brevity"
evaluation_criteria: >
  Evaluate whether the technical explanation is accurate, free from obsolete patterns,
  and avoids unnecessary conversational preamble.
evaluation_steps:
  1. Identify all technical claims, code snippets, and commands in the output.
  2. Cross-reference claims against current official documentation.
  3. Check if the response includes unrequested pleasantries or conversational filler.
  4. Penalize answers with incorrect flags or deprecated API calls by at least 3 points.
score_range: "1 to 5"
scoring_rubric:
  5: Completely accurate, uses modern APIs, zero filler.
  4: Accurate, but contains minor verbosity or non-critical formatting issues.
  3: Partially accurate, but omits important caveats or uses older syntax.
  2: Contains at least one demonstrably false technical claim.
  1: Completely hallucinated, broken commands, or dangerous advice.
```

---

## 4. LLM-as-a-Judge Safeguards: Controlling Bias

LLMs evaluating other LLMs exhibit well-documented systematic biases:
1. **Self-Preference Bias**: Models score their own outputs higher than outputs from competing models.
   - *Mitigation*: Never evaluate a model using the same model family as the judge (e.g. use Claude 3.5 Sonnet to evaluate GPT-4o, or GPT-4o to evaluate Claude).
2. **Verbosity Bias**: Models systematically favor longer, wordy answers over concise answers.
   - *Mitigation*: Explicitly instruct the judge rubric to penalize unneeded length, or normalize score by token count.
3. **Position Bias**: In pairwise comparisons (Model A vs Model B), judges favor the model presented first.
   - *Mitigation*: Run evaluation twice swapping position (`A vs B` and `B vs A`), averaging the result.

---

## 5. Golden Dataset Construction

A golden evaluation dataset should contain **minimum 20–50 representative cases** formatted as JSON:

```json
[
  {
    "id": "eval_001",
    "query": "How do I rotate database credentials in staging?",
    "expected_answer": "Run `vault lease renew staging-db` or update the secret in AWS Secrets Manager and restart the ECS service.",
    "ground_truth_chunks": ["doc_vault_credentials_p4", "doc_ecs_deployment_p2"],
    "metadata": { "domain": "devops", "criticality": "high" }
  }
]
```

### Pre/Post Regression Testing Gate in CI/CD
Whenever prompts, model versions, chunk sizes, or embedding models are changed:
1. Run the test suite against the golden dataset.
2. Compare before/after scores:
   - If Faithfulness drops by > 2%, **fail the build**.
   - If Context Recall drops by > 3%, **fail the build**.
   - If 95th-percentile latency increases by > 20%, **fail the build**.
