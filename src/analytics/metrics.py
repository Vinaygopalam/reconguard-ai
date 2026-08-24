from __future__ import annotations
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def summarize(results: list[dict], ground_truth: pd.DataFrame | None = None) -> dict:
    frame = pd.DataFrame(results); total = len(frame)
    metrics = {"total": total, "auto_matches": int((frame.status == "AUTO_MATCH").sum()), "human_review": int((frame.status == "HUMAN_REVIEW").sum()), "exceptions": int((frame.status == "EXCEPTION").sum()), "reconciliation_rate": round(100 * (frame.status == "AUTO_MATCH").sum() / total, 1) if total else 0, "average_trust": round(frame.trust_score.mean(), 1) if total else 0}
    if ground_truth is not None and not ground_truth.empty:
        merged = frame.merge(ground_truth, on="transaction_id", how="inner"); actual = merged.ground_truth == "EXACT_MATCH"; predicted = merged.status == "AUTO_MATCH"
        metrics.update({"accuracy": round(100 * (actual == predicted).mean(), 1), "precision": round(100 * precision_score(actual, predicted, zero_division=0), 1), "recall": round(100 * recall_score(actual, predicted, zero_division=0), 1), "f1": round(100 * f1_score(actual, predicted, zero_division=0), 1)})
    return metrics
