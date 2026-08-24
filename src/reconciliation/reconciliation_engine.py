from __future__ import annotations
import pandas as pd
from dataclasses import asdict, dataclass
from .similarity import compare_records, weighted_score
from ..config import ReconConfig

@dataclass
class ReconciliationResult:
    transaction_id: str; status: str; match_score: float; source_records: dict; similarities: dict; matched_sources: list[str]; candidate_count: int

def reconcile(sources: dict[str, pd.DataFrame], config: ReconConfig | None = None) -> list[dict]:
    config = config or ReconConfig(); anchors = sources["GATEWAY"]
    output = []
    for _, anchor in anchors.iterrows():
        records = {"GATEWAY": anchor.to_dict()}; similarities = {"GATEWAY": {k: 100.0 for k in config.weights}}
        candidates = []
        for source, frame in sources.items():
            if source == "GATEWAY": continue
            if frame.empty: continue
            ranked = []
            for _, row in frame.iterrows():
                scores = compare_records(anchor, row, config.date_tolerance_days)
                ranked.append((weighted_score(scores, config.weights), row, scores))
            ranked.sort(key=lambda item: item[0], reverse=True); best = ranked[0]
            if best[0] >= 45: records[source] = best[1].to_dict(); similarities[source] = best[2]; candidates.append((source, best))
        matched = ["GATEWAY"] + [source for source, _ in candidates]
        score = round(sum(item[1][0] for item in candidates) / len(candidates), 2) if candidates else 0.0
        amounts_agree = len(matched) == 3 and all(similarities[s]["amount"] >= 99 for s in matched)
        material_amount_difference = any(similarities[s]["amount"] < 80 for s in similarities)
        if material_amount_difference: status = "EXCEPTION"
        elif amounts_agree: status = "AUTO_MATCH" if score >= config.auto_match_threshold else "HUMAN_REVIEW"
        elif score >= config.auto_match_threshold: status = "HUMAN_REVIEW"
        elif score >= config.human_review_threshold: status = "HUMAN_REVIEW"
        else: status = "EXCEPTION"
        output.append(asdict(ReconciliationResult(str(anchor.transaction_id), status, score, records, similarities, matched, len(candidates))))
    return output
