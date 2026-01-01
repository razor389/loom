# src/loom/core/clients/__init__.py
"""
Low-level client drivers.

Clients are thin wrappers around external systems (HTTP APIs, EDGAR retrieval, yfinance, Outlook COM).
They focus on:
- request/response mechanics,
- retries/rate limiting/circuit breaking,
- parsing into Python primitives,
and do not perform business-level metric mapping or validation.
"""
