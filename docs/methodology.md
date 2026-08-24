# ReconGuard AI Methodology

ReconGuard AI is a deterministic, evidence-first reconciliation workflow. The system can use AI-style language for investigation summaries, but explanations never override matching or classification evidence.

## Similarity

Text fields use case-insensitive RapidFuzz ratio. Amount similarity is 100 for exact equality and decreases proportionally to relative difference. Date similarity decreases with day distance within the configured tolerance.

## Matching

Candidates are scored with configurable weights: transaction ID 35%, amount 25%, date 15%, merchant 15%, and reference 10%. A material amount mismatch cannot be automatically matched even when an identifier is exact.

## Trust score

The base score is adjusted for three-source agreement, data completeness, multiple candidates, and duplicate candidates. The final score is clamped to 0–100 and exposed with its component breakdown.

## Classification

Rules classify exact matches first, then duplicate candidates, amount differences, date differences, fuzzy matches, missing anchors, and unknown cases. Processing-fee suggestions require three records and a small ledger difference; the wording remains probabilistic.

## Human-in-the-loop

85–100 is eligible for automatic resolution only with amount agreement. 60–84 is human review. 0–59 is an exception. The interface presents the source records, evidence, score, reason, and recommended action before a user decides what to do.

## Exception and priority intelligence

Rules classify exact matches, fuzzy matches, amount and date mismatches, duplicate candidates, missing anchors, and possible processing-fee patterns. Priority combines financial amount, trust deficit, and exception impact so investigators can work the highest-risk cases first. Related cases are grouped by exception type and total financial impact.

## Evaluation

For generated records, predicted automatic matches are compared with the generator's `EXACT_MATCH` label. Accuracy, precision, recall, and F1 are calculated with zero-division protection. Uploaded files have no ground truth and therefore show operational metrics only.
