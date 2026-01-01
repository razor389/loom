# src/loom/core/clients/sec_client.py
"""
SEC/EDGAR client (async-first).

Encapsulates retrieval of filings and exhibit data, including:
- URL/accession handling,
- async fetch of HTML/XML resources with retries/timeouts,
- client-boundary caching of responses,
- parsing into lightly-typed primitives suitable for downstream normalization.

Returns raw tags/values + provenance references for normalization in higher-level fetchers.
"""
