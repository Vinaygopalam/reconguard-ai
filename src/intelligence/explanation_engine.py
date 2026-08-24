def explain(evidence: dict) -> str:
    return f"What happened? {evidence['reason']} Why? The strongest available evidence produced a trust score of {evidence['trust_score']}/100. Next action: {evidence['recommended_action']}"
