# src/loom/core/clients/outlook_client.py
"""
Outlook client (Windows-only) for retrieving local research inputs.

Wraps win32com interactions with circuit-breaker protection to avoid hanging the pipeline.
Produces raw textual sources or message metadata for use by `loom.fetchers.intelligence`.

This module should degrade gracefully when Outlook/COM is unavailable.
"""
