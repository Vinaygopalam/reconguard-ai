from __future__ import annotations

def calculate_priority(evidence: dict) -> dict:
    records = evidence["source_records"]; amount = max([float(r["amount"]) for r in records.values()] or [0]); score = min(100, round(amount / 3000 + (100 - evidence["trust_score"]) * .35 + (15 if evidence["exception_type"] in {"DUPLICATE_RECORD", "AMOUNT_MISMATCH", "POSSIBLE_PROCESSING_FEE"} else 0), 2))
    category = "CRITICAL" if score >= 80 else "HIGH" if score >= 55 else "MEDIUM" if score >= 25 else "LOW"
    return {"score": score, "category": category}
