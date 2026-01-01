# src/loom/core/http/cache.py
"""
File-based client response cache.

Supports cache modes:
- off: bypass cache
- readonly: read hits; do not write
- readwrite: read hits; write misses

Cache keys must be stable (vendor + method + URL + sorted params + relevant headers).
Cached payloads should be stored as JSON for inspectability.

Emits events:
- cache.hit, cache.miss, cache.write
"""
