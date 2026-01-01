# src/loom/core/resolution/__init__.py
"""
Entity-resolution subsystem.

This package centralizes “identity alignment” logic so the rest of the pipeline can be
vendor-agnostic and deterministic.

Primary responsibilities:
- Convert user-entered tickers (and legacy aliases) into a canonical ticker used for:
  - output naming (e.g., outputs/final/{TICKER}.{YY}.xlsx)
  - domain IR records (FinancialRecord.ticker, NarrativeResult.ticker)
  - observability/log payloads
- Provide per-vendor ticker symbols for downstream clients (FMP / Yahoo / SEC / etc.).
- Provide context-specific search aliases (e.g., Outlook email subject terms, forum category
  tickers) without scattering per-context mapping files across the codebase.
- Provide ADR-to-ordinary mappings when configured (e.g., use ordinary shares tickers for
  Yahoo pricing/history while keeping the canonical ticker stable).

Configuration:
- Source of truth is `src/loom/config/ticker_map.yaml`.
- The CLI should load this config once and pass a resolver (or a resolved struct) into
  strategies/fetchers rather than having each component reload it.

Public API:
- `TickerResolver`: loader + query methods (canonicalize, vendor_ticker, email_terms, etc.)
- `TickerResolution`: a rich resolution result suitable for logging (`entity.ticker_mapped`)

Error handling:
- Unknown tickers/aliases should raise `TickerConfigError` early (CLI boundary preferred).
- Missing vendor mappings may fall back to canonical if `default_to_canonical=True`.

Observability:
- When input aliases differ from canonical, emit `event="entity.ticker_mapped"` with at least
  {input, canonical, matched_alias}.
"""
