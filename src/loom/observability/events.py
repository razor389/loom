# src/loom/observability/events.py
"""
Canonical event definitions and payload helpers.

Defines stable event names such as:
- mapping.fallback_used
- entity.ticker_mapped
- time.fy_end_mismatch
- excel.table_resized

Includes small helpers to create consistent structured payloads for logging and debug reporting.
"""
