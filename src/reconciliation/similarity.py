from __future__ import annotations
from rapidfuzz.fuzz import ratio
import pandas as pd

def text_similarity(left, right) -> float:
    if pd.isna(left) or pd.isna(right) or not str(left) or not str(right): return 0.0
    return float(ratio(str(left).lower(), str(right).lower()))

def amount_similarity(left: float, right: float) -> float:
    if left == right: return 100.0
    return max(0.0, 100.0 * (1 - abs(float(left)-float(right)) / max(abs(float(left)), abs(float(right)), 1)))

def date_similarity(left, right, tolerance: int = 3) -> float:
    days = abs((pd.Timestamp(left) - pd.Timestamp(right)).days)
    return max(0.0, 100.0 - days * (100.0 / max(tolerance, 1)))

def compare_records(left: pd.Series, right: pd.Series, date_tolerance: int = 3) -> dict[str, float]:
    return {"transaction_id": text_similarity(left.transaction_id, right.transaction_id), "amount": amount_similarity(left.amount, right.amount), "date": date_similarity(left.transaction_date, right.transaction_date, date_tolerance), "merchant": text_similarity(left.merchant, right.merchant), "reference": text_similarity(left.reference, right.reference)}

def weighted_score(scores: dict[str, float], weights: dict[str, float]) -> float:
    return round(sum(scores[key] * weights[key] for key in weights), 2)
