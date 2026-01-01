# src/loom/strategies/insurance.py
"""
Insurance company strategy.

Coordinates:
- SEC filings/tag extraction + normalization,
- FMP (e.g., tax or supplemental series) as needed,
- optional narrative generation,
to produce FinancialRecords and NarrativeResults suitable for insurance templates.
"""
