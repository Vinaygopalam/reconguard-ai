from __future__ import annotations

def classify_exception(result: dict) -> str:
    if result["status"] == "AUTO_MATCH": return "EXACT_MATCH"
    records = result["source_records"]; sims = result["similarities"]
    if result["candidate_count"] == 0: return "MISSING_IN_GATEWAY"
    if result["candidate_count"] > 2: return "DUPLICATE_RECORD"
    amounts = [float(record["amount"]) for record in records.values()]
    if len(amounts) >= 2 and max(amounts) - min(amounts) > 0.01:
        if len(amounts) == 3 and abs(amounts[0] - amounts[1]) < 0.01 and abs(amounts[2] - amounts[0]) / max(amounts[0], 1) < .05: return "POSSIBLE_PROCESSING_FEE"
        return "AMOUNT_MISMATCH"
    if any(scores["date"] < 100 for scores in sims.values()): return "DATE_MISMATCH"
    if result["status"] == "HUMAN_REVIEW": return "AMBIGUOUS_MATCH" if result["candidate_count"] > 1 else "FUZZY_MATCH"
    return "UNKNOWN_EXCEPTION"
