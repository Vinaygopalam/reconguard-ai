from __future__ import annotations
import pandas as pd

def group_exceptions(evidence: list[dict]) -> list[dict]:
    rows = [item for item in evidence if item["exception_type"] != "EXACT_MATCH"]
    if not rows: return []
    frame = pd.DataFrame(rows)
    groups = []
    for exception_type, group in frame.groupby("exception_type"):
        groups.append({"group": exception_type.replace("_", " ").title(), "exception_type": exception_type, "related_exceptions": len(group), "total_amount": round(sum(max(float(r["amount"]) for r in item["source_records"].values()) for item in group.to_dict("records")), 2), "common_pattern": group.iloc[0]["reason"]})
    return groups
