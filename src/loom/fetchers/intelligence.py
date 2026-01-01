# src/loom/fetchers/intelligence.py
"""
Narrative/intelligence fetching.

Responsibilities:
- pull source text from Outlook (when enabled/available),
- invoke summarization engine to produce provider-agnostic narratives,
- return NarrativeResult objects with token usage metadata.

All narrative generation must remain isolated behind the summarization engine interface.
"""
