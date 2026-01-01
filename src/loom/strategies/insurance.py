# src/loom/strategies/insurance.py
"""
Insurance company strategy (async-first).

Coordinates:
- SEC filings/tag extraction + normalization (async),
- FMP (tax/supplemental series) as needed (async),
- optional narrative generation,
to produce FinancialRecords and NarrativeResults suitable for insurance templates.
"""
