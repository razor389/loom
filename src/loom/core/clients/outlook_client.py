# src/loom/core/clients/outlook_client.py
"""
Outlook client (Windows-only, optional).

Design requirements:
- Must not hard-fail imports on non-Windows platforms.
- win32com/pywin32 imports must be lazy or guarded by try/except ImportError.
- Exposes an interface that allows narrative generation to be disabled cleanly.

Produces raw textual sources or message metadata for use by `loom.fetchers.intelligence`.
"""
