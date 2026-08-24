from __future__ import annotations

def calculate_trust(result: dict) -> dict:
    similarities = result["similarities"]
    values = [sum(scores.values()) / len(scores) for scores in similarities.values()]
    base = result["match_score"]
    agreement = 5 if len(result["matched_sources"]) == 3 else 0
    completeness = 3 if len(result["matched_sources"]) == 3 else 0
    ambiguity = 8 if result["candidate_count"] > 1 else 0
    duplicate = 5 if result["candidate_count"] > 2 else 0
    final = max(0, min(100, round(base + agreement + completeness - ambiguity - duplicate, 2)))
    return {"final": final, "base_confidence": round(base, 2), "cross_source_bonus": agreement, "completeness_bonus": completeness, "ambiguity_penalty": ambiguity, "duplicate_penalty": duplicate, "similarity_average": round(sum(values)/len(values), 2)}
