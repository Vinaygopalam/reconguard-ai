from .reconciliation_engine import reconcile

def exact_match(sources, config=None):
    return [result for result in reconcile(sources, config) if result["match_score"] >= 99]
