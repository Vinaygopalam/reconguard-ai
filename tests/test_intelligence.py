from src.intelligence.evidence_engine import build_evidence
from src.intelligence.priority_engine import calculate_priority
from tests.test_reconciliation import sources
from src.reconciliation.reconciliation_engine import reconcile

def test_exact_match_evidence_is_trusted():
    evidence = build_evidence(reconcile(sources())[0])
    assert evidence["exception_type"] == "EXACT_MATCH" and evidence["trust_score"] == 100

def test_fee_pattern_is_classified():
    data = sources(); data["LEDGER"].loc[0, "amount"] = 750
    evidence = build_evidence(reconcile(data)[0])
    assert evidence["exception_type"] in {"POSSIBLE_PROCESSING_FEE", "AMOUNT_MISMATCH"}

def test_priority_has_numeric_score():
    evidence = build_evidence(reconcile(sources())[0]); priority = calculate_priority(evidence)
    assert 0 <= priority["score"] <= 100
