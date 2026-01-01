# src/loom/core/clients/fmp_client.py
"""
Financial Modeling Prep (FMP) client (async-first).

Uses the shared async HTTP transport and cache layer in `loom.core.http`.
Responsibilities:
- construct FMP endpoint URLs + params,
- perform async HTTP requests with retries/timeouts,
- apply client-boundary caching (for faster iteration and rate-limit safety),
- return raw JSON payloads plus provenance identifiers.

No metric-key mapping occurs here; mapping is performed in `loom.fetchers.financial`.
"""
