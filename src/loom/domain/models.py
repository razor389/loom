# src/loom/domain/models.py
"""
Domain models for Loom (IO-free).

Defines canonical intermediate representations (IR), including:
- FinancialRecord: typed metric value with fiscal period end support and provenance.
  Uses Decimal for deterministic arithmetic and clean regression diffs.
- NarrativeResult: narrative output with token/context usage metadata.

Conversion to float is permitted only at the Excel write boundary.
"""
