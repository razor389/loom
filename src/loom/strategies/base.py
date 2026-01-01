# src/loom/strategies/base.py
"""
Strategy interface.

Defines a stable strategy contract (e.g., fetch_data) returning:
- List[FinancialRecord],
- List[NarrativeResult],
- summary metadata used by export/validation.

Concrete strategies must be deterministic and testable (clients are injected or accessed via fetchers).
"""
