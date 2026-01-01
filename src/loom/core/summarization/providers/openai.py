# src/loom/core/summarization/providers/openai.py
"""
OpenAI provider implementation.

Implements the provider interface using OpenAI SDK calls, translating Loom requests into
vendor calls and returning normalized outputs + token usage where available.
"""
