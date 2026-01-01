# src/loom/observability/events.py
"""
Canonical event definitions and payload helpers.

Defines stable event names such as:
- mapping.fallback_used
- entity.ticker_mapped
- time.fy_end_mismatch
- excel.table_resized
- excel.safe_zone_violation
- cache.hit
- cache.miss
- cache.write

Includes small helpers to create consistent structured payloads for logging and debug reporting.
"""
