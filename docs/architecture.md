# ReconGuard AI Architecture

```mermaid
flowchart TD
  Sources[Bank / Gateway / Ledger CSVs] --> Normalize[Schema normalization and validation]
  Normalize --> Engine[Reconciliation engine]
  Engine --> Match[Exact and fuzzy candidate matching]
  Match --> Decision[Weighted score and decision thresholds]
  Decision --> Intelligence[Trust, evidence, classification, priority]
  Intelligence --> Analytics[Metrics, grouping, close summary]
  Analytics --> UI[Streamlit workspaces]
```

The gateway is the anchor source. Each gateway record is compared to the best bank and ledger candidates. The engine returns a stable result object containing source records, per-field similarities, candidate count, status, and match score. Intelligence functions enrich that object without mutating the matching decision. This boundary makes explanations auditable and testable.

The application stores no credentials and uses local CSVs. The synthetic generator provides the demo path and a separate ground-truth table for evaluation. `app.py` owns presentation and session state; `src/` owns the reusable data, reconciliation, intelligence, and analytics modules.
