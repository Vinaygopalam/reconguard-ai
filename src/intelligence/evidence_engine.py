from __future__ import annotations
from .exception_classifier import classify_exception
from .trust_score import calculate_trust

def build_evidence(result: dict) -> dict:
    trust = calculate_trust(result); exception_type = classify_exception(result)
    records = result["source_records"]; amounts = [float(item["amount"]) for item in records.values()]
    difference = max(amounts) - min(amounts) if amounts else 0
    agreement = "FULL" if len(result["matched_sources"]) == 3 and difference < .01 else "PARTIAL"
    if exception_type == "POSSIBLE_PROCESSING_FEE": reason = f"Bank and gateway agree, while the ledger differs by approximately INR {difference:,.0f}."
    elif exception_type == "AMOUNT_MISMATCH": reason = f"Matched records contain an amount difference of approximately INR {difference:,.0f}."
    elif exception_type == "DATE_MISMATCH": reason = "The records identify the same transaction, but settlement timing differs beyond the normal window."
    elif exception_type == "FUZZY_MATCH": reason = "Evidence suggests a likely match based on merchant, amount, and reference similarity; verify before close."
    else: reason = "All available source evidence is consistent with the reconciliation decision."
    action = "Verify fees, refunds, adjustments, or ledger posting." if exception_type not in {"EXACT_MATCH"} else "No action required; retain the evidence trail."
    return {"transaction_id": result["transaction_id"], "status": result["status"], "trust_score": trust["final"], "evidence": result["similarities"], "cross_source_agreement": agreement, "exception_type": exception_type, "reason": reason, "recommended_action": action, "trust_breakdown": trust, "source_records": records}
