# src/loom/core/clients/yahoo_client.py
"""
Yahoo Finance client wrapper.

Primary responsibility is to fetch market/point-in-time values required by strategies.
This client may use yfinance (sync) internally; if so, it must be invoked in a way that does not
block the async pipeline (e.g., `asyncio.to_thread`), preserving an async external interface.

Returns raw values and provenance identifiers for downstream normalization.
"""
