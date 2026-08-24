from __future__ import annotations
import pandas as pd

ALIASES = {
    "transaction_id": ["transaction_id", "txn_id", "transaction_reference", "id", "payment_id"],
    "amount": ["amount", "payment_amount", "value", "gross_amount", "settlement_amount"],
    "transaction_date": ["transaction_date", "date", "settlement_date", "payment_date", "created_at"],
    "merchant": ["merchant", "merchant_name", "description", "customer", "payee"],
    "currency": ["currency", "currency_code"],
    "reference": ["reference", "ref", "bank_reference", "gateway_reference", "utr"],
    "status": ["status", "payment_status", "settlement_status"],
}
REQUIRED = ["transaction_id", "amount", "transaction_date", "merchant"]

def normalize_columns(frame: pd.DataFrame, source: str) -> pd.DataFrame:
    if frame.empty:
        raise ValueError("The uploaded CSV is empty.")
    lookup = {str(column).strip().lower().replace(" ", "_"): column for column in frame.columns}
    mapping = {}
    for standard, aliases in ALIASES.items():
        for alias in aliases:
            if alias in lookup:
                mapping[lookup[alias]] = standard
                break
    missing = [field for field in REQUIRED if field not in mapping.values()]
    if missing:
        raise ValueError(f"Could not identify required columns: {', '.join(missing)}")
    result = frame.rename(columns=mapping).copy()
    result["transaction_id"] = result["transaction_id"].astype(str).str.strip()
    result["amount"] = pd.to_numeric(result["amount"], errors="coerce")
    result["transaction_date"] = pd.to_datetime(result["transaction_date"], errors="coerce")
    if result["amount"].isna().any():
        raise ValueError("Amount contains invalid numeric values.")
    if result["transaction_date"].isna().any():
        raise ValueError("Date contains invalid values.")
    for optional in ["merchant", "currency", "reference", "status"]:
        if optional not in result:
            result[optional] = "" if optional != "currency" else "INR"
    result["source"] = source.upper()
    return result[["transaction_id", "amount", "transaction_date", "merchant", "currency", "reference", "status", "source"]]

def load_csv(path_or_buffer, source: str) -> pd.DataFrame:
    return normalize_columns(pd.read_csv(path_or_buffer), source)
