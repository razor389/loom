# src/loom/export/__init__.py
"""
Export layer.

Contains output generation logic (code) for producing user-facing deliverables and debug artifacts:
- Excel writer for injecting tabular data into templates,
- JSON writer for structured debug dumps (only under --debug).

Note: runtime artifacts are written under the on-disk `outputs/` directory; the package is `export/`.
"""
