# src/loom/main.py
"""
Back-compat module entrypoint.

Supports legacy invocation:
    python -m loom.main ...

This module should remain a thin shim that forwards to `loom.cli` (argument parsing + dispatch).
"""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())