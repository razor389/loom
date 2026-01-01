# src/loom/domain/__init__.py
"""
Domain layer (pure definitions).

Contains IO-free models and validation rules:
- canonical intermediate representations (FinancialRecord, NarrativeResult),
- schema validation for metrics catalog and mappings.

This package should not import clients, filesystem code, or network code.
"""
