# src/loom/__init__.py
"""
Loom: Academy Capital Management Report Generator (refactor).

This package implements a modular pipeline that:
- fetches and normalizes financial + narrative inputs into canonical intermediate records,
- validates all metrics against a metrics catalog contract, and
- injects typed tabular data into Excel templates using a "data feed" model (no styling in Python).

Primary execution is via `python -m loom` (CLI).
"""
