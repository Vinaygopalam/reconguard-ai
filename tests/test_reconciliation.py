import pandas as pd
from src.reconciliation.reconciliation_engine import reconcile
from src.config import ReconConfig

def sources(amount=1000, date="2026-01-01", ref="REF-1", merchant="Acme"):
    row = {"transaction_id":"TXN-1", "amount":amount, "transaction_date":pd.Timestamp(date), "merchant":merchant, "currency":"INR", "reference":ref, "status":"SETTLED", "source":"X"}
    return {source: pd.DataFrame([{**row, "source":source}]) for source in ["BANK","GATEWAY","LEDGER"]}

def test_exact_match_is_automatic():
    result = reconcile(sources())[0]
    assert result["status"] == "AUTO_MATCH" and result["match_score"] == 100

def test_amount_mismatch_needs_review():
    data = sources(); data["LEDGER"].loc[0, "amount"] = 2000
    assert reconcile(data)[0]["status"] != "AUTO_MATCH"

def test_date_tolerance():
    data = sources(); data["BANK"].loc[0, "transaction_date"] += pd.Timedelta(days=2)
    assert reconcile(data, ReconConfig(date_tolerance_days=3))[0]["status"] == "AUTO_MATCH"
