# src/loom/fetchers/__init__.py
"""
Business-level fetchers.

Fetchers orchestrate clients to produce normalized domain objects:
- financial fetchers assemble FinancialRecords from FMP/SEC/Yahoo with mapping + provenance,
- intelligence fetchers assemble NarrativeResults from Outlook and LLM summarization.

Fetchers should not decide overall workflow; strategies do that.
"""
