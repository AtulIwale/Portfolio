# AI / NLP evidence layer

## Implemented now

`aec/evidence.py` provides TF-IDF unigram/bigram retrieval over six original fictional
control-policy passages. It returns source IDs, exact supporting quotations, similarity
scores and abstains when nothing clears a fixed threshold. It is an **extractive NLP baseline**,
not a large language model, agent, contract interpretation service or production RAG system.

```python
from aec.evidence import EvidenceAssistant
print(EvidenceAssistant().ask('What evidence is required for variation approval?'))
```

`outputs/retrieval_evaluation.json` includes the executed seven-question smoke evaluation.
The questions and corpus were authored together, so this does not establish general NLP quality.
The test checks expected source retrieval and an unrelated-question abstention. It is not
a red-team benchmark or proof of prompt-injection immunity.

## Why this sits beside the six projects

The ML projects prioritise investigation; the evidence layer retrieves the fictional controls
that govern human review. The SQL module calculates amounts. These roles stay separate:
retrieval never invents values, the LLM is not used for arithmetic, and models never approve.

## Deliberately not implemented

Hosted LLM generation, embedding/vector-database retrieval, agent orchestration, fine-tuning,
arbitrary natural-language SQL, client document upload or live ERP writes. A future generative
layer must use authorised sources, tenant filtering, citations, answerability evaluation,
redaction, prompt-injection tests and human approval. It needs separately configured credentials
and a cost/privacy decision; no secret is included here.

Do not advertise this repository as a fully implemented enterprise AI copilot. A precise label is
“Predictive ML with a local evidence-retrieval prototype.”
