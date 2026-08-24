from dataclasses import dataclass

@dataclass(frozen=True)
class ReconConfig:
    auto_match_threshold: float = 85.0
    human_review_threshold: float = 60.0
    date_tolerance_days: int = 3
    fee_tolerance: float = 0.03
    weights: dict[str, float] = None

    def __post_init__(self):
        if self.weights is None:
            object.__setattr__(self, "weights", {"transaction_id": .35, "amount": .25, "date": .15, "merchant": .15, "reference": .10})
