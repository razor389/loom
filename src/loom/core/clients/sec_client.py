# src/loom/core/clients/sec_client.py
"""
SEC/EDGAR client.

Encapsulates retrieval of filings and exhibit data (e.g., Exhibit 13), including:
- URL/accession handling,
- XML/HTML scraping/parsing,
- basic caching or throttling if needed.

Returns raw tags/values + provenance references for normalization in higher-level fetchers.
"""
