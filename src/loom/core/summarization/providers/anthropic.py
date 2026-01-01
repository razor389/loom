# src/loom/core/summarization/providers/anthropic.py
"""
Anthropic provider implementation.

Implements the provider interface using Anthropic's SDK, translating Loom requests into
vendor calls and returning normalized outputs + token usage where available.
"""
