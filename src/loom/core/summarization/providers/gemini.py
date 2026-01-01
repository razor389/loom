# src/loom/core/summarization/providers/gemini.py
"""
Google Gemini provider implementation.

Implements the provider interface using Google Generative AI SDKs, translating Loom requests into
vendor calls and returning normalized outputs + token usage where available.
"""
