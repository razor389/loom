# src/loom/core/clients/__init__.py
"""
Low-level vendor client drivers (async-first).

Clients are thin wrappers around external systems (HTTP APIs, EDGAR retrieval, yfinance, Outlook COM).
They focus on:
- async request/response mechanics via shared `loom.core.http` transport,
- retries/backoff and timeouts,
- caching at the client boundary (readwrite/readonly/off),
- parsing into Python primitives.

Business-level metric mapping/validation belongs in fetchers/domain, not clients.
"""
