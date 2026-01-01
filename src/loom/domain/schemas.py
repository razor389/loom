# src/loom/domain/schemas.py
"""
Schema and contract validation.

Validates:
- metrics catalog structure and constraints,
- mapping files (ordered candidate keys),
- runtime records against the catalog (unknown keys rejected),
- required/optional/warn-if-missing policies per strategy/year,
- constraint enforcement (bounds, sign conventions, allow_negative, ratio bounds).

Also produces validation reports suitable for debug artifact dumping.
"""
