# src/loom/observability/logging.py
"""
Logging configuration for Loom.

Sets up:
- standard console logging,
- debug-aware JSONL sink to outputs/debug/.../logs.jsonl when --debug is enabled,
- consistent formatting for structured events.

This module should be the single place where handlers/formatters/sinks are wired.
"""
