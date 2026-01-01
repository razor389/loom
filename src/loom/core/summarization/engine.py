# src/loom/core/summarization/engine.py
"""
Summarization engine.

Responsibilities:
- chunking and context assembly for long source corpora,
- token counting / context-window accounting,
- provider invocation via a stable interface,
- producing `NarrativeResult` objects with usage metadata.

The engine must remain provider-agnostic; provider-specific code belongs in `providers/`.
"""
