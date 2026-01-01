# src/loom/core/resolution/tickers.py
"""
Ticker resolution utilities.

This module implements the “entity resolution registry” described in SPEC.md. It loads
`config/ticker_map.yaml` and provides a single coherent interface for all ticker-related
mapping needs:

1) Canonicalization
   Users may enter tickers in multiple legacy forms (e.g., BRK-B, BRK.B, BRK/B). Loom must
   convert these inputs into a canonical ticker for:
   - deterministic output naming
   - stable domain IR tickers
   - consistent validation and debug artifact paths

2) Vendor symbol routing
   Different data sources often require different symbols for the same economic entity.
   For example:
   - Yahoo: BRK-B
   - FMP:   BRK.B (or vendor-specific conventions)
   - SEC:   BRK-B (optional; depending on query mechanism)
   The resolver exposes `vendor_ticker(canonical, vendor)` to retrieve the correct symbol
   for each client without hardcoding source logic elsewhere.

3) Context-specific aliases
   Some features search text or taxonomies where additional aliases are useful:
   - Outlook email subject search terms (ticker + synonyms / old ticker / company name)
   - Forum category tickers (a specific taxonomy key that may not match canonical)
   These are represented under `contexts.*` in the YAML and accessed via helper methods.

4) ADR -> ordinary mapping
   In some cases, the canonical ticker may be an ADR (e.g., ADYEY) while market data queries
   should use the ordinary shares ticker on the local exchange (e.g., ADYEN.AS).
   The YAML may specify `adr.ordinary`; the resolver exposes `adr_ordinary()` and vendor
   symbols may independently set Yahoo/FMP/SEC symbols as needed.

Key types:
- `TickerResolution`: Rich resolution output used for logging and pipeline routing.
- `TickerResolver`: Immutable resolver that loads YAML once and serves queries.

Expected YAML shape (high level):
    version: 1
    tickers:
      BRK.B:
        canonical: BRK.B
        input_aliases: ["BRK-B", "BRK", "BRK/B"]
        vendor_symbols:
          yahoo: BRK-B
          fmp: BRK.B
        contexts:
          email_subject_terms: ["BRK", "BRK.B"]
          forum_category_ticker: BRK
        adr:
          ordinary: null

Error handling:
- Mis-shaped YAML raises `TickerConfigError` at load time.
- Unknown tickers/aliases raise `TickerConfigError` at resolution time.
- Missing vendor mappings return canonical by default (configurable via
  `default_to_canonical`).

Observability integration:
- Call `resolver.resolve(input)` at the CLI boundary.
- If `resolution.was_mapped` is True, emit `event="entity.ticker_mapped"` with resolution
  fields, and propagate `resolution.canonical` downstream.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Set

import yaml


class TickerConfigError(RuntimeError):
    pass


@dataclass(frozen=True)
class TickerResolution:
    """
    Rich resolution result for observability + downstream routing.

    - input_ticker: raw user input
    - normalized_input: stripped/uppercased input used for matching
    - canonical: resolved canonical ticker (output naming + IR ticker)
    - matched_alias: the exact normalized token that matched (may equal canonical)
    - was_mapped: True when input did not already equal canonical (after normalization)
    """
    input_ticker: str
    normalized_input: str
    canonical: str
    matched_alias: str
    was_mapped: bool


@dataclass(frozen=True)
class TickerResolver:
    """
    Loads ticker_map.yaml and provides resolution helpers.
    """

    raw: Dict[str, Any]
    _by_canonical: Dict[str, Dict[str, Any]]
    _alias_to_canonical: Dict[str, str]

    @staticmethod
    def from_file(path: str | Path) -> "TickerResolver":
        p = Path(path)
        if not p.exists():
            raise TickerConfigError(f"Ticker config not found: {p}")

        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception as e:
            raise TickerConfigError(f"Failed to parse YAML {p}: {e}") from e

        tickers = (data.get("tickers") or {})
        if not isinstance(tickers, dict) or not tickers:
            raise TickerConfigError("ticker_map.yaml must contain top-level 'tickers:' map")

        by_canonical: Dict[str, Dict[str, Any]] = {}
        alias_to_canonical: Dict[str, str] = {}

        for key, cfg in tickers.items():
            if not isinstance(cfg, dict):
                raise TickerConfigError(f"Ticker entry '{key}' must be a mapping")

            canonical = str(cfg.get("canonical") or key).upper()

            # Reject duplicate canonicals (easy to accidentally create).
            if canonical in by_canonical:
                raise TickerConfigError(f"Duplicate canonical ticker entry: {canonical}")

            by_canonical[canonical] = cfg

            # Canonical itself is always resolvable.
            alias_to_canonical[canonical] = canonical

            # Also map the YAML key (in case it differs by punctuation/case).
            alias_to_canonical[str(key).upper()] = canonical

            # input_aliases (optional)
            aliases = cfg.get("input_aliases") or []
            if not isinstance(aliases, list):
                raise TickerConfigError(f"{canonical}.input_aliases must be a list")

            for a in aliases:
                if not a:
                    continue
                alias_to_canonical[str(a).upper()] = canonical

        return TickerResolver(raw=data, _by_canonical=by_canonical, _alias_to_canonical=alias_to_canonical)

    # ---------- New primary API ----------

    def resolve(self, input_ticker: str) -> TickerResolution:
        """
        Resolve user input to a rich resolution result (for logging + routing).
        Raises if unknown.
        """
        if not input_ticker:
            raise TickerConfigError("Empty ticker provided")

        normalized = input_ticker.strip().upper()
        canonical = self._alias_to_canonical.get(normalized)
        if not canonical:
            raise TickerConfigError(f"Unknown ticker/alias: {input_ticker}")

        was_mapped = normalized != canonical
        return TickerResolution(
            input_ticker=input_ticker,
            normalized_input=normalized,
            canonical=canonical,
            matched_alias=normalized,
            was_mapped=was_mapped,
        )

    # ---------- Back-compat / convenience ----------

    def canonicalize(self, input_ticker: str) -> str:
        return self.resolve(input_ticker).canonical

    def get(self, canonical_or_alias: str) -> Dict[str, Any]:
        c = self.canonicalize(canonical_or_alias)
        cfg = self._by_canonical.get(c)
        if not cfg:
            raise TickerConfigError(f"No config found for canonical ticker: {c}")
        return cfg

    def vendor_ticker(self, canonical_or_alias: str, vendor: str, *, default_to_canonical: bool = True) -> Optional[str]:
        cfg = self.get(canonical_or_alias)
        vendor = vendor.strip().lower()

        vendor_symbols = cfg.get("vendor_symbols") or {}
        if not isinstance(vendor_symbols, dict):
            raise TickerConfigError(f"{self.canonicalize(canonical_or_alias)}.vendor_symbols must be a mapping")

        sym = vendor_symbols.get(vendor)
        if sym:
            return str(sym)

        return self.canonicalize(canonical_or_alias) if default_to_canonical else None

    def adr_ordinary(self, canonical_or_alias: str) -> Optional[str]:
        cfg = self.get(canonical_or_alias)
        adr = cfg.get("adr") or {}
        if adr and not isinstance(adr, dict):
            raise TickerConfigError(f"{self.canonicalize(canonical_or_alias)}.adr must be a mapping")
        ord_sym = (adr or {}).get("ordinary")
        return str(ord_sym) if ord_sym else None

    def email_terms(self, canonical_or_alias: str) -> Set[str]:
        c = self.canonicalize(canonical_or_alias)
        cfg = self.get(c)

        contexts = cfg.get("contexts") or {}
        if contexts and not isinstance(contexts, dict):
            raise TickerConfigError(f"{c}.contexts must be a mapping")

        terms = {c}
        extra = (contexts or {}).get("email_subject_terms") or []
        if extra and not isinstance(extra, list):
            raise TickerConfigError(f"{c}.contexts.email_subject_terms must be a list")

        for t in extra:
            if t:
                terms.add(str(t))

        return terms

    def forum_category(self, canonical_or_alias: str) -> str:
        c = self.canonicalize(canonical_or_alias)
        cfg = self.get(c)

        contexts = cfg.get("contexts") or {}
        if contexts and not isinstance(contexts, dict):
            raise TickerConfigError(f"{c}.contexts must be a mapping")

        override = (contexts or {}).get("forum_category_ticker")
        return str(override).upper() if override else c


def load_default_resolver() -> TickerResolver:
    # NOTE: adjust if you move/rename the config file
    return TickerResolver.from_file(Path("src/loom/config/ticker_map.yaml"))
