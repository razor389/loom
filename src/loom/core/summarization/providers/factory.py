# src/loom/core/summarization/providers/factory.py
"""
Provider factory for summarization.

Selects and constructs provider implementations based on configuration (env/settings file),
supporting easy swapping between OpenAI/Anthropic/Gemini (and future providers).
"""
