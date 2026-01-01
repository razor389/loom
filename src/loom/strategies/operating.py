# src/loom/strategies/operating.py
"""
Operating company strategy (async-first).

Coordinates:
- FMP fundamentals + normalization (async),
- Yahoo market data (async interface; may internally use threads),
- optional narrative generation,
to produce FinancialRecords and NarrativeResults suitable for operating templates.
"""
