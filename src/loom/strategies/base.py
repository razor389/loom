# src/loom/strategies/base.py
"""
Strategy interface (async-first).

Defines a stable strategy contract returning:
- List[FinancialRecord] (Decimal-valued),
- List[NarrativeResult],
- summary metadata used by export/validation.

Concrete strategies should parallelize independent vendor calls via asyncio.gather where appropriate.
"""
