# Loom — Academy Capital Management Report Generator (Refactor)

Loom is a modular Python pipeline that generates standardized Excel-based financial company reports for **Operating** and **Insurance** company types.

The system refactors legacy procedural scripts into a maintainable, testable architecture built around:
- a **canonical metrics contract** (`src/loom/config/metrics_catalog.yaml`),
- **strategy-based orchestration** (Operating vs Insurance),
- an Excel-template **“data feed”** approach (Python injects data; templates own styling), and
- **pluggable narrative generation** (provider-agnostic summarization engine).

## Core Philosophy

- **Data feed model:** Python writes *values* into template tables; Python never styles cells.
- **Canonical metrics:** All output metrics must exist in `metrics_catalog.yaml`. Unknown metric keys are rejected.
- **Strategy pattern:** A single orchestrator selects a strategy rather than branching logic throughout the codebase.
- **Simple output:** Default behavior overwrites a single final workbook under `outputs/final/`.
- **Debug-on-demand:** With `--debug`, Loom writes diagnostic artifacts under `outputs/debug/{TICKER}/{YYYY}/` and overwrites them each run.

## Project Layout

Key directories (see `SPEC.md` for the full canonical structure):

- `src/loom/` — application package
  - `config/` — metrics catalog, mappings, example settings
  - `core/clients/` — low-level vendor clients (FMP/SEC/Yahoo/Outlook)
  - `fetchers/` — business logic fetching + normalization into canonical models
  - `strategies/` — Operating vs Insurance orchestration
  - `export/` — Excel writer + debug JSON writer
  - `observability/` — structured event schemas + logging
  - `templates/` — packaged Excel templates (`.xlsm`)
- `outputs/` — runtime artifacts (gitignored)
  - `final/` — user-facing reports
  - `debug/` — diagnostic output when `--debug` is enabled
- `tests/` — unit/integration tests

## Installation

### From source (editable)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
````

## Configuration and Secrets

Loom does not commit secrets.

* `src/loom/config/settings.example.toml` documents supported keys.
* Runtime configuration should come from either:

  * environment variables (recommended for CI), and/or
  * a user-local settings file (not committed), e.g.:

    * Linux/macOS: `~/.config/loom/settings.toml`
    * Windows: `%APPDATA%\\loom\\settings.toml` (or equivalent)

Typical configuration includes:

* API keys (FMP, LLM providers),
* provider selection and model names,
* non-secret defaults (e.g., timeouts).

## Templates (Package Data)

Excel templates live in `src/loom/templates/` and must be loaded via package resources (not CWD-relative paths) to support installed execution.

Template contract:

* a named table `tbl_data` (required)
* a named table `tbl_narrative` (optional)
* formulas should reference structured table columns (e.g., `tbl_data[revenue]`)

## Usage

Primary entrypoint:

```bash
python -m loom TICKER [options]
```

Back-compat entrypoint:

```bash
python -m loom.main TICKER [options]
```

Common flags:

* `--strategy operating|insurance|auto`
* `--start-year YYYY`
* `--end-year YYYY` (optional)
* `--debug`
* `--no-narrative`
* `--output-dir outputs/`

Example:

```bash
python -m loom AAPL --strategy operating --start-year 2022 --end-year 2025
```

## Outputs

### Default (no `--debug`)

Writes only the final workbook (overwritten each run):

* `outputs/final/{TICKER}.{YY}.xlsx` (e.g., `outputs/final/AAPL.26.xlsx`)

### Debug (`--debug`)

In addition to the final workbook, writes diagnostics under:

* `outputs/debug/{TICKER}/{YYYY}/` (cleared/recreated each run)

Typical debug contents:

* `logs.jsonl` (structured events)
* `raw/` (raw vendor payload snapshots / SEC URLs)
* `normalized/` (FinancialRecords + NarrativeResults dumps)
* `validation/` (validation report, missing metrics)
* `final/` (copy of final workbook + consolidated JSON)

## Data Contracts

### Metrics catalog (`metrics_catalog.yaml`)

The system contract. Each metric must define:

* `unit`
* `sign_convention`
* `strategies`
* `missingness_policy` (`required` | `optional` | `warn_if_missing`)
* optional constraints (bounds, allow_negative, ratio bounds)

### Mappings (`mappings_operating.yaml`, `mappings_insurance.yaml`)

Mappings support ordered candidates for each Loom metric key:

1. Try candidates sequentially.
2. If a fallback candidate is used, emit `mapping.fallback_used`.
3. If none resolve:

   * fail if `missingness_policy=required`
   * otherwise warn and omit.

### Intermediate representation

Core canonical models:

* `FinancialRecord` — metric value with fiscal period end support + provenance
* `NarrativeResult` — narrative output with token/context usage metadata

## Development

Run tests:

```bash
pytest -q
```

Lint/typecheck (if configured):

```bash
ruff check .
mypy src
```

## Notes / Platform Considerations

* Outlook integration (`outlook_client.py`) is Windows-only and should degrade gracefully when unavailable.
* Excel table resizing is required because `openpyxl` does not auto-expand tables; Loom explicitly updates table refs and writes into the expanded range.

