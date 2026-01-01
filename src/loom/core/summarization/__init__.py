# src/loom/core/summarization/__init__.py
"""
Summarization subsystem public API.

Exports a provider-agnostic `generate_summary(...)` entrypoint used by fetchers/strategies.
Implementation details (chunking, token accounting, provider selection) live in `engine.py` and `providers/`.
"""
