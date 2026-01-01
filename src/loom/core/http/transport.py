# src/loom/core/http/transport.py
"""
Async HTTP transport wrapper.

Responsibilities:
- manage a shared httpx.AsyncClient lifecycle (timeouts, headers, connection pooling),
- provide request helpers used by vendor clients,
- integrate retry/backoff and caching hooks,
- emit observability events for request timing and outcomes.

This module is vendor-agnostic.
"""
