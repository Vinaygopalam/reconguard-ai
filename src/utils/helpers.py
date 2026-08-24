from ..intelligence.evidence_engine import build_evidence
from ..intelligence.priority_engine import calculate_priority
from ..intelligence.explanation_engine import explain

def enrich_results(results):
    enriched = []
    for result in results:
        item = build_evidence(result); item["priority"] = calculate_priority(item); item["explanation"] = explain(item); enriched.append(item)
    return enriched
