# src/loom/core/clients/fmp_client.py
"""
Financial Modeling Prep (FMP) client.

Provides HTTP request utilities, rate limiting, error handling, and JSON parsing for FMP endpoints.
Returns raw payloads or lightly-typed structures for use by higher-level fetchers.

No metric-key mapping should live here; mapping occurs in `loom.fetchers.financial`.
"""
