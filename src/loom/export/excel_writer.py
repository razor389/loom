# src/loom/export/excel_writer.py
"""
Excel export writer using the "data feed" model.

Responsibilities:
- load the correct binary Excel template from package resources (not CWD-relative paths),
- locate required named tables (e.g., tbl_data, optional tbl_narrative),
- resize openpyxl table references to fit injected rows (openpyxl does not auto-expand tables),
- write typed values into the expanded cell region,
- emit structured events for table resize actions and output paths.

This module must not apply styling; templates own formatting.
"""
