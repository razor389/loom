# src/loom/cli.py
"""
Command-line interface for Loom.

Responsibilities:
- parse user arguments (ticker, strategy, years, debug, narrative flags),
- resolve ticker aliases (canonical vs vendor tickers),
- select and run the appropriate strategy (operating/insurance/auto),
- validate outputs against the metrics catalog + mapping/constraint rules,
- write the final Excel workbook, and
- optionally emit debug artifacts under outputs/debug/{TICKER}/{YYYY}/ (overwrite semantics).

This module owns orchestration boundaries but should not contain vendor-specific IO logic.
"""
from __future__ import annotations
import argparse

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="loom", description="Loom report generator")
    p.add_argument("ticker")
    p.add_argument("--strategy", choices=["operating", "insurance", "auto"], default="auto")
    p.add_argument("--start-year", type=int)
    p.add_argument("--end-year", type=int)
    p.add_argument("--debug", action="store_true")
    p.add_argument("--no-narrative", action="store_true")
    p.add_argument("--output-dir", default="outputs/")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    # TODO: dispatch into orchestrator once implemented
    print(f"[stub] ticker={args.ticker} strategy={args.strategy} start={args.start_year} end={args.end_year} debug={args.debug}")
    return 0