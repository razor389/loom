# src/loom/core/clients/yahoo_client.py
"""
Yahoo Finance client wrapper.

Primarily wraps `yfinance` or equivalent data access to fetch:
- market data (price, shares, market cap),
- point-in-time metrics needed by strategies.

Returns raw values and provenance identifiers for downstream normalization.
"""
