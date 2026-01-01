"""
Shared async HTTP utilities for Loom.

Provides:
- a configured async transport wrapper (httpx AsyncClient),
- file-based caching primitives (readwrite/readonly/off),
- retry/backoff policies (tenacity integration),
- consistent request metadata (timeouts, headers, user-agent).

Vendor clients compose these primitives rather than re-implementing HTTP concerns.
"""
