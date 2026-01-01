# SPEC.md — Project Loom

**Target:** Academy Capital Management Report Generator Refactor

## 1. Executive Summary

Loom is a modular Python pipeline designed to generate standardized financial company reports for Operating and Insurance company types. Loom refactors legacy procedural scripts into a maintainable, testable system built around a canonical metrics contract, strategy-based orchestration, and an Excel-template “data feed” approach.

### Core Philosophy

* **The “Data Feed” Model:** Python fetches, normalizes, and injects typed tabular data into an Excel template. Python never styles cells.
* **Canonical Metrics:** All data must map to `config/metrics_catalog.yaml`. Unknown metric keys are rejected.
* **Pluggable Intelligence:** Narrative generation is isolated and provider-agnostic.
* **Strategy Pattern:** One orchestrator selects the strategy (Operating vs Insurance) rather than branching.
* **Simple User Output:** Default behavior produces a single overwritten workbook in `outputs/final/`.
* **Debug-on-Demand:** With `--debug`, write diagnostic artifacts under `outputs/debug/{ticker}/{year}/` (overwritten).

---

## 2. Directory Structure (Canonical)

> **Note on naming:** The on-disk runtime artifact directory is `outputs/`. The Python package folder for writers/export logic is named `export/` to avoid confusion with runtime outputs.

```text
loom/
├── docs/                             # Documentation
│   ├── architecture.md
│   └── setup.md
│
├── outputs/                          # Runtime Data Artifacts (gitignored)
│   ├── final/                        # User-facing .xlsx reports
│   └── debug/                        # Diagnostic dumps ({TICKER}/{YYYY}/...)
│
├── .cache/                           # OPTIONAL: client response cache (gitignored)
│
├── src/
│   └── loom/                         # Main Package Code
│       ├── __init__.py
│       ├── __main__.py               # Enables: python -m loom (delegates to CLI)
│       ├── main.py                   # Back-compat module entry (python -m loom.main)
│       ├── cli.py                    # CLI implementation (arg parsing + dispatch)
│       │
│       ├── config/
│       │   ├── settings.example.toml     # Example settings (NO secrets)
│       │   ├── metrics_catalog.yaml      # THE CONTRACT: Canonical metric keys, units, signs
│       │   ├── mappings_operating.yaml   # Maps FMP keys to Loom Metric Keys
│       │   ├── mappings_insurance.yaml   # Maps SEC tags to Loom Metric Keys
│       │   └── ticker_map.yaml           # OPTIONAL: Vendor ticker aliases (BRK.B -> BRK-B)
│       │
│       ├── core/
|       ├── core/
|       │   ├── resolution/
|       │   │   ├── __init__.py
|       │   │   └── tickers.py
|       |   |
│       │   ├── http/                     # Shared async HTTP + caching primitives
│       │   │   ├── __init__.py
│       │   │   ├── transport.py          # httpx AsyncClient wrapper, timeouts, headers
│       │   │   ├── cache.py              # file-based cache (read/write/readonly/off)
│       │   │   └── retry.py              # retry/backoff policy (tenacity integration)
│       │   │
│       │   ├── clients/                  # Low-level Drivers (HTTP/MAPI wrappers)
│       │   │   ├── __init__.py
│       │   │   ├── fmp_client.py         # Rate Limits, JSON parsing
│       │   │   ├── sec_client.py         # EDGAR/Exhibit 13 scraping logic
│       │   │   ├── yahoo_client.py       # yfinance wrapper
│       │   │   └── outlook_client.py     # win32com logic (Circuit breaker enabled)
│       │   │
│       │   └── summarization/            # The Intelligence Engine (Vendor Agnostic)
│       │       ├── __init__.py           # Exposes main `generate_summary` function
│       │       ├── engine.py             # Chunking, Token Counting, Context mgmt
│       │       └── providers/
│       │           ├── __init__.py
│       │           ├── base.py
│       │           ├── factory.py
│       │           ├── gemini.py
│       │           ├── anthropic.py
│       │           └── openai.py
│       │
│       ├── domain/                       # Pure Data Definitions (No IO)
│       │   ├── __init__.py
│       │   ├── models.py                 # Pydantic: FinancialRecord, NarrativeResult
│       │   └── schemas.py                # Validation rules for inputs + catalog/mapping checks
│       │
│       ├── fetchers/                     # Business Logic (Orchestrates Clients)
│       │   ├── __init__.py
│       │   ├── financial.py              # FMP/SEC/Yahoo fetching + normalization helpers
│       │   └── intelligence.py           # Outlook + Summarization -> NarrativeResult
│       │
│       ├── strategies/                   # Application Strategy (Orchestrates Fetchers)
│       │   ├── __init__.py
│       │   ├── base.py                   # Interface for fetch_data()
│       │   ├── operating.py              # Logic: FMP + Yahoo -> FinancialRecords
│       │   └── insurance.py              # Logic: SEC + FMP (Tax) -> FinancialRecords
│       │
│       ├── export/                       # Output Generation Logic (code)
│       │   ├── __init__.py
│       │   ├── excel_writer.py           # Data-feed injector + table resize utility
│       │   └── json_writer.py            # Debug artifact dumping (only under --debug)
│       │
│       ├── observability/                # Logging/event schema + sinks
│       │   ├── __init__.py
│       │   ├── events.py                 # Canonical event names + payload shape helpers
│       │   └── logging.py                # Logger config; JSONL sink wiring (debug-aware)
│       │
│       └── templates/                    # Binary Excel Models (package data)
│           ├── operating_v2.xlsm
│           └── insurance_v2.xlsm
│
├── tests/                               # Unit/integration tests
│   ├── domain/
│   ├── fetchers/
│   ├── strategies/
│   └── export/
│
├── .gitignore
├── README.md
├── requirements.txt
└── SPEC.md
```

**Template packaging requirement:** `src/loom/templates/` must be included as package data, and templates must be loaded via package resources (not relative CWD paths) to support installed execution.

---

## 3. Outputs and Persistence Policy

### 3.1 Default (no `--debug`)

Write only the final report workbook:
`outputs/final/{TICKER}.{YY}.xlsx` (example `outputs/final/AAPL.26.xlsx`)

* Overwrite existing file.
* Do not write logs/raw/normalized/validation to disk.

### 3.2 Debug (`--debug`)

In addition to the normal final output, write diagnostics to:
`outputs/debug/{TICKER}/{YYYY}/` (overwritten each run)

```text
outputs/debug/{TICKER}/{YYYY}/
├── logs.jsonl
├── raw/                # raw API payloads / SEC XML urls / etc.
├── normalized/         # FinancialRecords + NarrativeResults dumps
├── validation/         # validation_report.json, missing_metrics.json
└── final/              # copy of final excel + consolidated json
```

**Overwrite rule:** The `{TICKER}/{YYYY}` directory is cleared/recreated at the start of a debug run.

---

## 4. Data Contracts

### 4.1 Metrics Catalog (`config/metrics_catalog.yaml`)

The “law” of the system. Every metric must be defined here.
Minimum required fields:

* `unit`
* `sign_convention`
* `strategies`
* `missingness_policy` (`required` | `optional` | `warn_if_missing`)
* optional constraints: `min/max`, `allow_negative`, `ratio bounds`

### 4.2 Intermediate Representation (IR)

**FinancialRecord** (Decimal-based for deterministic tests/diffs)

```python
class FinancialRecord(BaseModel):
    ticker: str
    fiscal_year: int
    fiscal_period_end_date: date | None

    metric_key: str
    value: Decimal
    period_type: str  # historical | forecast | ttm | point_in_time

    source_type: str
    source_locator: str
    raw_key: str | None
    fetched_at: datetime

    currency: str | None = None
    fx_rate: Decimal | None = None
```

**Rounding rule:** Any derived calculations must be performed in `Decimal`. Conversion to `float` is permitted only at the Excel write boundary.

---

**NarrativeResult**
Add token/context tracking:

```python
class NarrativeResult(BaseModel):
    ticker: str
    category: str
    summary_text: str
    model_used: str
    source_count: int
    context_window_usage: dict  # {"prompt_tokens":..., "completion_tokens":..., "total_tokens":...}
    raw_sources: List[str] = Field(exclude=True)
```

---

## 5. Mapping Contract (Sequential Fallback + Warning)

Mappings (`mappings_operating.yaml`, `mappings_insurance.yaml`) must support ordered candidates.

**Rule:**

1. Try candidates sequentially.
2. If a fallback candidate is used (not the first), emit a WARNING log:

   * `event="mapping.fallback_used"`
   * `metric_key`, `primary_candidate`, `used_candidate`, `ticker`, `year`
3. If no candidates resolve:

   * If `missingness_policy=required` → fail validation.
   * Else warn and omit.

---

## 6. Entity Resolution (Ticker Alignment)

**Problem:** Yahoo/FMP/SEC may require different tickers (BRK.B vs BRK-B).
**Solution:** * `config/ticker_map.yaml` is the **canonical entity-resolution registry**

* It supports:

  * `canonical`
  * `input_aliases` (BRK.B → BRK-B, BF/B → BF-B, etc.)
  * `vendor_symbols`: `yahoo`, `fmp`, `sec` (and optionally `forum`)
  * `contexts.email_subject_terms`
  * `contexts.forum_category_ticker`
  * `adr.ordinary` (ADR → ord mapping)

And update flow wording so **CLI** loads it once and passes a `TickerResolver` (or resolved struct) into strategies/fetchers rather than having each fetcher re-load it.

**Log:**
`event="entity.ticker_mapped"` when aliasing occurs.

---

## 7. Fiscal Year ↔ Period End Handling (Excel Safety)

**Requirement:** The normalizer must assign a concrete `fiscal_period_end_date` per fiscal year.

* **Operating:** Use FMP company fiscal-year-end month/day + statement dates as confirmation.
* **Insurance:** Prefer SEC filing period end; fallback to FMP FY-end.

If statement/filing dates materially disagree with computed fiscal-year mapping:
Emit `event="time.fy_end_mismatch"` warning.

---

## 8. Excel Writer (Data-Feed + Safe Zone; No Row Insertion)

### 8.1 Template Contract (Revised)

Templates must include:

* Named table `tbl_data` (required)
* Named table `tbl_narrative` (optional)
* Formulas should reference structured table columns (e.g., `tbl_data[revenue]`)

#### New requirement: preallocated data-feed zone

* The worksheet must include **a preallocated set of blank rows beneath `tbl_data`** reserved for Loom to write into.
* Content such as footers/notes/signatures must be placed **below the maximum reserved zone** or on a separate sheet.

#### New requirement: Safe Zone sentinel named range (required)

* The template must define a **named range** `Loom_SafeZone_End` that refers to **a single cell** on the same worksheet as `tbl_data`.
* `Loom_SafeZone_End` marks the **last permissible row** that `tbl_data` may expand into.
* Template authors must ensure the area between the bottom of the initial `tbl_data` table and `Loom_SafeZone_End` is part of the reserved data-feed zone (blank / safe to overwrite).

### 8.2 Table Expansion Policy (Revised)

**The writer MUST NOT insert worksheet rows** (e.g., no `worksheet.insert_rows`). Instead:

1. Locate `tbl_data` via `worksheet.tables`
2. Determine the maximum allowed expansion using the `Loom_SafeZone_End` named range:

   * compute the last usable row from the named range cell
   * compute the required last row for the injected dataset
3. Verify the injected dataset fits within the safe zone; otherwise raise a hard error
4. Update the table definition `ref` to the new range
5. Write values into existing cells within the reserved zone

#### Events

* `excel.table_resized` with old/new refs and row counts
* `excel.safe_zone_violation` when requested rows exceed reserved capacity (hard error)

#### Serialization rule

* `FinancialRecord.value` is `Decimal` in the IR.
* Immediately before writing to Excel cells, numeric values must be explicitly cast (e.g., `float(decimal_value)`), rather than relying on implicit `openpyxl` conversion.

---

## 9. Execution Flow (High Level)

**Concurrency model (new):** Client I/O is **async-first**.

* All vendor clients expose `async` methods.
* Fetchers and strategies may parallelize independent requests with `asyncio.gather`.
* CLI remains a synchronous entrypoint but executes the pipeline via `asyncio.run(...)`.

**CLI entrypoints (`__main__.py` / `cli.py` / `main.py`):**

1. Parse CLI args (ticker, strategy, start/end years, `--debug`, narrative flags).
2. Resolve tickers (canonical + vendor tickers).
3. Select strategy.
4. **Strategy returns:**

   * `List[FinancialRecord]`
   * `List[NarrativeResult]`
   * summary metadata (end year, currency, etc.)
5. **Validate:**

   * metric keys exist in catalog
   * required metrics present per strategy/year
   * constraints enforced
6. **Write Excel:**

   * inject records into template tables (with resizing)
7. **If --debug:**

   * dump raw/normalized/validation/logs/final copy via `export/json_writer.py` and log sink.

---

## 10. CLI

```bash
python -m loom TICKER [options]
```

Back-compat (supported):

```bash
python -m loom.main TICKER [options]
```

**Key flags:**

* `--strategy operating|insurance|auto`
* `--start-year YYYY`
* `--end-year YYYY` (optional)
* `--debug` (write to `outputs/debug/{ticker}/{year}/`, overwrite)
* `--no-narrative`
* `--output-dir outputs/` (base dir)

Default overwrite semantics are intentional (no file pile-up).

---

## 11. Settings and Secrets Policy (Operational) — additions

Settings must support:

* HTTP defaults: timeouts, user-agent, retries/backoff
* Cache configuration:

  * `cache_dir` (default `.cache/loom/`)
  * `cache_mode` (`off` | `readonly` | `readwrite`)
  * optional TTL (if enabled)
* Provider configuration (LLM providers optional; narrative can be disabled)
* Outlook integration is optional and must be able to be disabled cleanly on non-Windows platforms.

---

## 12. Migration Plan (Implementation Order)

* [ ] Excel table resize spike in `export/excel_writer.py`
* [ ] Metrics catalog + schema validation (`domain/schemas.py`)
* [ ] Entity resolution + fallback mapping warnings (`fetchers/financial.py`)
* [ ] Fiscal period end assignment (normalize to `fiscal_period_end_date`)
* [ ] Implement `OperatingStrategy` + `InsuranceStrategy`
* [ ] Debug artifact writer (only under `--debug`) via `export/json_writer.py`
* [ ] Observability wiring: canonical event helpers + JSONL sink (`observability/`)
* [ ] Parity checks vs legacy (anchor metric set)
