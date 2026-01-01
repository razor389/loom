# src/loom/core/http/retry.py

"""
Retry/backoff policy utilities.

Centralizes tenacity-based retry configuration so all clients behave consistently:
- retry on transient network errors and selected HTTP status codes,
- bounded exponential backoff,
- per-request timeout enforcement.

Vendor clients should import retry helpers from here rather than configuring tenacity ad hoc.
"""
