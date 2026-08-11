#!/usr/bin/env python3
"""Generic English -> target-language RA asset localizer engine.

Data-driven: given a LocalizationConfig (address map CSV, source files,
output paths, and any documented literal-value overrides), substitutes
memory addresses across achievement/leaderboard conditions and Rich
Presence, producing a transformation report. Nothing in this module is
game- or language-specific -- that all lives in a LocalizationConfig
instance (the Yellow/Italian config that drove this repo's
games/yellow/italian/generated/ output lives in the private research repo,
not published here -- see games/yellow/italian/docs/generation-report.md
for what it does). A French/German/Spanish pass, or a different game, only
needs its own address-triage CSV + config, not a new copy of this file.

This file is included for transparency -- to show the actual substitution
engine that produced games/yellow/italian/generated/723-Italian-*.txt --
not as a runnable pipeline: the LocalizationConfig, source RA definitions,
and driver script that call it are private-repo-only (they depend on RA's
own raw achievement export, which this project does not publish).
"""
from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from csv_safety import atomic_write_csv  # noqa: E402

CONDITION_FIELDS = ["trigger_or_start", "cancel", "submit", "value"]

# RA memory-reference token: optional modifier, "0x", one size letter (or a
# literal space for 16-bit), then hex digits. Deliberately does NOT match
# bare hex literals like Rich Presence Lookup table keys ("0x00=...") since
# those have a digit (not a size letter) immediately after "0x".
MEM_TOKEN_RE = re.compile(r"(?P<mod>[dp~b]?)0x(?P<size>[HWXLUMNOPQRSTK ])(?P<addr>[0-9a-fA-F]+)", re.IGNORECASE)


@dataclass(frozen=True)
class LiteralOverride:
    """A documented non-address exception: the entire text of one condition
    field, for one asset, is replaced verbatim instead of being address-
    substituted (e.g. a translated dialogue-tile literal whose byte count
    changed). Must come with an evidence citation -- never invented."""
    asset_id: str
    field: str
    new_text: str
    evidence: str
    change_type: str = "value+address"


@dataclass
class LocalizationConfig:
    language: str
    definitions_in: Path
    triage_in: Path
    rich_in: Path
    definitions_out: Path
    rich_out: Path
    report_out: Path
    target_address_column: str
    rich_presence_asset_id: str = "rich_presence"
    literal_overrides: list[LiteralOverride] = field(default_factory=list)

    def overrides_by_asset_field(self) -> dict[tuple[str, str], LiteralOverride]:
        return {(o.asset_id, o.field): o for o in self.literal_overrides}


def load_address_map(config: LocalizationConfig) -> dict[int, tuple[int, str]]:
    """int(english_address) -> (int(target_address), resolution_method)."""
    out: dict[int, tuple[int, str]] = {}
    with config.triage_in.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[int(row["address"], 16)] = (
                int(row[config.target_address_column], 16),
                row["resolution_method"],
            )
    return out


class Substituter:
    """Applies the address map to raw RA condition text, tracking every
    substitution made (or skipped) for the transformation report."""

    def __init__(self, addr_map: dict[int, tuple[int, str]]):
        self.addr_map = addr_map
        self.changes: list[dict] = []  # old, new, evidence
        self.unmapped: set[int] = set()

    def _sub(self, m: re.Match) -> str:
        old_addr_int = int(m.group("addr"), 16)
        if old_addr_int not in self.addr_map:
            self.unmapped.add(old_addr_int)
            return m.group(0)
        new_addr_int, evidence = self.addr_map[old_addr_int]
        digits = m.group("addr")
        width = len(digits)
        new_hex = f"{new_addr_int:0{width}x}"
        if digits.isupper() or (digits.strip("0") and not any(c.islower() for c in digits)):
            new_hex = new_hex.upper()
        if new_addr_int != old_addr_int:
            self.changes.append({
                "old_address": f"0x{digits}",
                "new_address": f"0x{new_hex}",
                "evidence_basis": evidence,
            })
        return f"{m.group('mod')}0x{m.group('size')}{new_hex}"

    def apply(self, text: str) -> str:
        if not text:
            return text
        return MEM_TOKEN_RE.sub(self._sub, text)


def transform_definitions(config: LocalizationConfig, addr_map: dict[int, tuple[int, str]],
                           report_rows: list[dict]) -> tuple[list[dict], list[str]]:
    with config.definitions_in.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    overrides = config.overrides_by_asset_field()
    out_rows = []
    for row in rows:
        new_row = dict(row)
        for field_name in CONDITION_FIELDS:
            original = row.get(field_name, "") or ""
            if not original:
                continue
            override = overrides.get((row["asset_id"], field_name))
            if override is not None:
                new_row[field_name] = override.new_text
                report_rows.append({
                    "asset_type": row["asset_type"], "asset_id": row["asset_id"],
                    "title": row["title"], "field": field_name, "change_type": override.change_type,
                    "old": original, "new": override.new_text,
                    "evidence_basis": override.evidence,
                })
                continue
            sub = Substituter(addr_map)
            new_text = sub.apply(original)
            new_row[field_name] = new_text
            for c in sub.changes:
                report_rows.append({
                    "asset_type": row["asset_type"], "asset_id": row["asset_id"],
                    "title": row["title"], "field": field_name, "change_type": "address",
                    "old": c["old_address"], "new": c["new_address"],
                    "evidence_basis": c["evidence_basis"],
                })
            if sub.unmapped:
                raise SystemExit(
                    f"asset {row['asset_id']} field {field_name}: unmapped address(es) "
                    f"{[hex(a) for a in sub.unmapped]} -- not in {config.triage_in}"
                )
        out_rows.append(new_row)
    return out_rows, fieldnames


def transform_rich_presence(config: LocalizationConfig, addr_map: dict[int, tuple[int, str]],
                             report_rows: list[dict]) -> str:
    original = config.rich_in.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    out_lines = []
    in_lookup = False
    for line in lines:
        stripped = line.rstrip("\r\n")
        if stripped.startswith("Lookup:"):
            in_lookup = True
            out_lines.append(line)
            continue
        if stripped.startswith("Display:") or stripped.startswith("Format"):
            in_lookup = False
            out_lines.append(line)
            continue
        if in_lookup:
            # Lookup table rows (value->display-string) use the shared
            # in-engine font/letter encoding, not ROM text -- never touched.
            out_lines.append(line)
            continue
        sub = Substituter(addr_map)
        new_line = sub.apply(line)
        out_lines.append(new_line)
        for c in sub.changes:
            report_rows.append({
                "asset_type": "rich_presence", "asset_id": config.rich_presence_asset_id,
                "title": "Rich Presence", "field": "script", "change_type": "address",
                "old": c["old_address"], "new": c["new_address"],
                "evidence_basis": c["evidence_basis"],
            })
        if sub.unmapped:
            raise SystemExit(
                f"rich presence: unmapped address(es) {[hex(a) for a in sub.unmapped]}"
            )
    return "".join(out_lines)


def run(config: LocalizationConfig) -> dict:
    """Runs the full localization pass for one LocalizationConfig, writing
    definitions_out/rich_out/report_out. Returns summary counters."""
    addr_map = load_address_map(config)
    report_rows: list[dict] = []

    def_rows, def_fieldnames = transform_definitions(config, addr_map, report_rows)
    atomic_write_csv(config.definitions_out, def_fieldnames, def_rows)

    rich_text = transform_rich_presence(config, addr_map, report_rows)
    config.rich_out.write_text(rich_text, encoding="utf-8", newline="")

    report_fields = ["asset_type", "asset_id", "title", "field", "change_type", "old", "new", "evidence_basis"]
    with config.report_out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=report_fields)
        w.writeheader()
        w.writerows(report_rows)

    n_assets = len(def_rows) + 1  # +1 for the single Rich Presence script
    n_addr_changes = sum(1 for r in report_rows if r["change_type"] == "address")
    n_value_changes = sum(1 for r in report_rows if r["change_type"] != "address")
    return {
        "n_assets": n_assets,
        "n_achievements_leaderboards": len(def_rows),
        "n_addr_changes": n_addr_changes,
        "n_value_changes": n_value_changes,
    }
