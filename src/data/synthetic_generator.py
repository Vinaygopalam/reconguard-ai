from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from faker import Faker

SCENARIOS = ["EXACT_MATCH", "FUZZY_MATCH", "AMOUNT_MISMATCH", "DATE_MISMATCH", "DUPLICATE_RECORD", "MISSING_IN_LEDGER", "POSSIBLE_PROCESSING_FEE"]

def generate_demo_data(n: int = 150, seed: int = 42, output_dir: str | Path | None = None) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed); fake = Faker("en_IN"); Faker.seed(seed)
    dates = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 60, n), unit="D")
    base = pd.DataFrame({"transaction_id": [f"TXN-{10000+i}" for i in range(n)], "amount": rng.integers(500, 85000, n).astype(float), "transaction_date": dates, "merchant": [fake.company() for _ in range(n)], "currency": "INR", "reference": [f"REF{rng.integers(100000,999999)}" for _ in range(n)], "status": "SETTLED", "ground_truth": "EXACT_MATCH"})
    scenario_counts = {"FUZZY_MATCH": int(n*.15), "AMOUNT_MISMATCH": int(n*.10), "DATE_MISMATCH": int(n*.07), "DUPLICATE_RECORD": int(n*.05), "MISSING_IN_LEDGER": int(n*.05), "POSSIBLE_PROCESSING_FEE": int(n*.03)}
    cursor = int(n*.55)
    for scenario, count in scenario_counts.items():
        base.loc[cursor:cursor+count-1, "ground_truth"] = scenario; cursor += count
    bank = base.copy(); gateway = base.copy(); ledger = base.copy()
    fuzzy = base[base.ground_truth == "FUZZY_MATCH"].index
    gateway.loc[fuzzy, "reference"] = gateway.loc[fuzzy, "reference"].str.replace("REF", "GW-")
    gateway.loc[fuzzy, "transaction_id"] = gateway.loc[fuzzy, "transaction_id"].str.replace("TXN-", "PAY-")
    amount = base[base.ground_truth.isin(["AMOUNT_MISMATCH", "POSSIBLE_PROCESSING_FEE"])].index
    ledger.loc[amount, "amount"] = (ledger.loc[amount, "amount"] - np.where(base.loc[amount, "ground_truth"] == "POSSIBLE_PROCESSING_FEE", 250, 750)).clip(lower=1)
    date_shift = base[base.ground_truth == "DATE_MISMATCH"].index
    bank.loc[date_shift, "transaction_date"] += pd.Timedelta(days=4)
    duplicate = base[base.ground_truth == "DUPLICATE_RECORD"].iloc[:max(1, int(len(base[base.ground_truth == "DUPLICATE_RECORD"])/2))]
    bank = pd.concat([bank, duplicate], ignore_index=True)
    missing = base[base.ground_truth == "MISSING_IN_LEDGER"].index
    ledger = ledger.drop(index=missing).reset_index(drop=True)
    for frame in [bank, gateway, ledger]: frame.drop(columns=["ground_truth"], inplace=True)
    result = {"BANK": bank, "GATEWAY": gateway, "LEDGER": ledger, "GROUND_TRUTH": base[["transaction_id", "ground_truth"]]}
    if output_dir:
        output = Path(output_dir); output.mkdir(parents=True, exist_ok=True)
        for source, frame in result.items(): frame.to_csv(output / f"{source.lower()}_transactions.csv", index=False)
    return result
