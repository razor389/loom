# src/loom/fetchers/financial.py
"""
Financial data fetching + normalization (async-first).

Responsibilities:
- resolve vendor tickers using optional ticker_map.yaml,
- perform async calls to FMP/SEC/Yahoo clients as required,
- apply mapping files (ordered candidates) to translate vendor keys/tags into Loom metric keys,
- emit mapping fallback warnings when non-primary candidates are used,
- normalize fiscal year to a concrete fiscal_period_end_date (Excel safety),
- return FinancialRecord objects (Decimal values) with provenance.

Unknown metric keys must be rejected (catalog is the contract).
"""
