# src/loom/__main__.py
"""
Module entrypoint for installed execution.

Enables:
    python -m loom ...

Delegates to the CLI implementation in `loom.cli` to keep entrypoint logic minimal.
"""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
