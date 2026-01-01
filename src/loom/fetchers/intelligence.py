# src/loom/fetchers/intelligence.py
"""
Narrative/intelligence fetching (optional, async-first).

Responsibilities:
- optionally pull source text from Outlook (when enabled/available),
- invoke the summarization engine to produce provider-agnostic narratives,
- return NarrativeResult objects with token usage metadata.

Must degrade gracefully when Outlook/LLM providers are unavailable or when --no-narrative is set.
"""
