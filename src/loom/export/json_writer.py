# src/loom/export/json_writer.py
"""
Debug artifact writer.

Writes structured diagnostic files under outputs/debug/{TICKER}/{YYYY}/ when --debug is enabled:
- raw payload snapshots,
- normalized FinancialRecords/NarrativeResults dumps,
- validation reports,
- a copy of the final workbook and consolidated JSON.

Overwrite semantics: the per-run debug directory is cleared at the start of the run.
"""
