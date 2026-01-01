# src/loom/export/excel_writer.py
"""
Excel export writer using the "data feed" model.

Responsibilities:
- load the correct binary Excel template from package resources (not CWD-relative paths),
- locate required named tables (e.g., tbl_data, optional tbl_narrative),
- expand the Excel table *ref* to the required number of rows within a preallocated safe zone,
- write typed values into existing cells (no worksheet row insertion),
- enforce safe-zone limits and raise on overflow,
- emit structured events for table resize actions and output paths.

This module must not apply styling; templates own formatting.
"""

