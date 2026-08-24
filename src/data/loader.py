from __future__ import annotations
import pandas as pd
from .schema_normalizer import normalize_columns

def load_sources(bank, gateway, ledger) -> dict[str, pd.DataFrame]:
    return {"BANK": normalize_columns(bank, "BANK"), "GATEWAY": normalize_columns(gateway, "GATEWAY"), "LEDGER": normalize_columns(ledger, "LEDGER")}

def combine_sources(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.concat(sources.values(), ignore_index=True)
