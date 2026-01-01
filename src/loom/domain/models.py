# src/loom/domain/models.py
"""
Domain models for Loom.

Defines canonical intermediate representations (IR), including:
- FinancialRecord: typed metric value with fiscal period end support and provenance,
- NarrativeResult: narrative output with token/context usage metadata.

Models are used throughout the pipeline to enforce consistent structure and validation.
"""
