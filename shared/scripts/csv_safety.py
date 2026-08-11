#!/usr/bin/env python3
"""Shared read/write guardrails for hand-maintained evidence CSVs.

Exists because two incidents in one session came from editing these files
as raw text instead of through the csv module:
  1. An unquoted comma inside a hand-written field shifted column
     alignment for that row (silent corruption, not caught until a later
     script read the file and choked on it).
  2. A script crashed mid-writerows() with the file already truncated to
     whatever had been flushed so far, since writes went directly to the
     real path with no atomicity.

Two guardrails, used together:
  - validate_rows(): every row dict must have exactly the given
    fieldnames as keys -- no extra ("None" bucket from ragged CSV rows),
    no missing.
  - atomic_write_csv(): writes to a temp file in the same directory and
    os.replace()s it into place only after the write succeeds and the
    row count clears any registered minimum (if a schemas dict is
    supplied). A mid-write crash leaves the ORIGINAL file untouched,
    never a truncated one.

This module is game/locale-agnostic: it knows nothing about any specific
evidence CSV's schema. Callers that want the schema/row-count guard pass
their own `schemas` dict (path -> (expected fieldnames or None, minimum
row count)) -- see e.g. games/yellow/italian/scripts/csv_schemas.py.

Usage:
  from csv_safety import read_csv_strict, atomic_write_csv
  from csv_schemas import EXPECTED_SCHEMAS
  rows = read_csv_strict("data/map_id_usage_audit.csv", EXPECTED_SCHEMAS)
  ... mutate rows ...
  atomic_write_csv("data/map_id_usage_audit.csv", rows[0].keys(), rows, EXPECTED_SCHEMAS)
"""
import csv
import os
import tempfile
from pathlib import Path

Schemas = dict  # filename (str, no directory) -> (expected fieldnames tuple or None, minimum row count)


class CsvSafetyError(Exception):
    pass


def _norm(path: str | Path) -> str:
    # Keyed by filename only (not the full path) so callers can register a
    # schema once regardless of where the target repo is cloned or which
    # cwd a script runs from -- see e.g. csv_schemas.py.
    return Path(path).name


def validate_rows(rows: list[dict], fieldnames) -> None:
    """Every row must have exactly `fieldnames` as keys -- no ragged rows
    (extra fields collapse into a None key with csv.DictReader) and no
    missing fields (csv.DictReader fills those with None values, which
    this also catches since None is not a valid key OR a valid string
    value for a required column)."""
    fieldnames = list(fieldnames)
    expected = set(fieldnames)
    for i, row in enumerate(rows, 1):
        got = set(row.keys())
        if got != expected:
            extra = got - expected
            missing = expected - got
            raise CsvSafetyError(
                f"row {i}: schema mismatch -- extra keys {extra or None}, "
                f"missing keys {missing or None} (this usually means an "
                f"unquoted comma or newline inside a field upstream)"
            )
        if None in row.values():
            # DictReader also uses None for genuinely absent trailing
            # fields on a short row; same root cause, same refusal.
            raise CsvSafetyError(f"row {i}: contains a None value -- short/ragged row")


def read_csv_strict(path: str | Path, schemas: Schemas | None = None) -> list[dict]:
    """Read a CSV, validating schema + row count against `schemas` if the
    path is registered there. Raises CsvSafetyError rather than returning
    a partially-corrupt result."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise CsvSafetyError(f"{path}: zero data rows")
    validate_rows(rows, rows[0].keys())

    key = _norm(path)
    if schemas and key in schemas:
        expected_fields, min_rows = schemas[key]
        actual_fields = tuple(rows[0].keys())
        if expected_fields is not None and actual_fields != expected_fields:
            raise CsvSafetyError(
                f"{path}: header mismatch\n  expected: {expected_fields}\n  actual:   {actual_fields}"
            )
        if len(rows) < min_rows:
            raise CsvSafetyError(
                f"{path}: only {len(rows)} rows, expected at least {min_rows} "
                f"-- refusing to treat this as a valid read (looks truncated)"
            )
    return rows


def atomic_write_csv(path: str | Path, fieldnames, rows: list[dict], schemas: Schemas | None = None) -> None:
    """Validate rows against `fieldnames` and (if registered in `schemas`)
    the minimum row count, then write atomically: build the full file in a
    temp path first, and only os.replace() it over the real path once the
    write has fully succeeded. A crash mid-write leaves the original file
    completely untouched -- no truncation is possible with this pattern,
    unlike writing directly to `path`."""
    path = Path(path)
    fieldnames = list(fieldnames)
    validate_rows(rows, fieldnames)

    key = _norm(path)
    if schemas and key in schemas:
        expected_fields, min_rows = schemas[key]
        if expected_fields is not None and tuple(fieldnames) != expected_fields:
            raise CsvSafetyError(
                f"{path}: refusing to write -- fieldnames don't match the registered "
                f"schema\n  expected: {expected_fields}\n  got:      {tuple(fieldnames)}"
            )
        if len(rows) < min_rows:
            raise CsvSafetyError(
                f"{path}: refusing to write only {len(rows)} rows (registered minimum "
                f"is {min_rows}) -- this looks like accidental truncation, not a real "
                f"edit. If rows were legitimately removed, update the schemas dict."
            )

    fd, tmp_path = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        os.replace(tmp_path, path)  # atomic on POSIX and Windows
    except BaseException:
        Path(tmp_path).unlink(missing_ok=True)
        raise
