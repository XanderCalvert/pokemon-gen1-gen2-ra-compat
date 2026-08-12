# Generation architecture and audit

**This is a report of work performed in the private research repository,
not a pipeline included here.** The generation and audit scripts
themselves depend on RetroAchievements' own raw achievement/Rich Presence
export for Game 723, which this project does not publish (see the main
[README](../../../README.md#repository-layout)). What's included in this
repo is the one game/locale-agnostic engine those scripts drove
([`shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py))
plus the evidence and results it produced.

## Engine

[`shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py)
is a generic address-substitution engine, parameterised by a
`LocalizationConfig` (source/output paths + the target locale's address
triage CSV). It walks every achievement/leaderboard/Rich Presence condition
in the official RA asset definitions, substitutes any English address that
has a confirmed counterpart in that locale's address-triage CSV
([Italian's](../italian/data/ra_address_triage.csv), [French's](../french/data/ra_address_triage.csv),
[German's](../german/data/ra_address_triage.csv), [Spanish's](../spanish/data/ra_address_triage.csv)),
and leaves everything else (literal values, hit counts, flags, structure)
untouched. Each locale's config — a thin file pointing this engine at its
triage CSV plus its own documented literal override for achievement 81978
— and the driver script that converts its output into the two loadable
RA-format text files under `generated/` both live in the private research
repo, since they need the private RA export to run at all. See **Two
output formats** in the
[Italian README](../italian/README.md#generated-files-two-formats--read-this-before-loading-anything)
for why there are two output files, and why only one of them is actually
loadable locally in RAIntegration — the same applies to French's
[`generated/`](../french/generated/), German's
[`generated/`](../german/generated/), and Spanish's
[`generated/`](../spanish/generated/) output.

## Audit

The same seven checks are run against each locale's generated output in
the private research repo before its snapshot is published:

1. **1:1 asset mapping** — every source asset has exactly one counterpart
   in the target locale, and vice versa.
2. **Metadata unchanged** — title, description, points, flags, type, and
   author are byte-identical between source and generated asset.
3. **Condition structure preserved** — condition counts, types, and hit
   counts match source-to-generated for every asset, except the one
   documented 81978 literal exception (see each locale's own
   `docs/dynamic-testing.md`).
4. **0 unresolved addresses** — every address referenced anywhere in the
   131-row triage table has a resolved classification.
5. **Canonical file correctness** — the canonical output file contains
   exactly the official RA asset IDs, nothing else.
6. **Local-ID bijection** — the local-smoke-test ID↔official-ID map is a
   true one-to-one mapping, and every synthetic local ID is at or above
   RAIntegration's `FirstLocalId` (`111000001`).
7. **Canonical/local parity** — every local-smoke-test line is
   byte-identical to its canonical counterpart everywhere except the ID
   token, so the two output formats can never silently diverge in logic.

An independent re-derivation of the substitution from source files (diffed
against the actual generated output) and a schema validation of the
registered evidence CSVs were folded into the same pass/fail result.

### Italian — as last run against the full official asset set

```
OK   1:1 asset mapping: 78 source assets, 78 Italian counterparts
OK   metadata unchanged for all 78 assets (title/description/points/flags/type/author)
OK   condition counts/types/hit-counts preserved for all 78 assets (except the documented 81978 literal exception)
OK   0 unresolved addresses in data/ra_address_triage.csv (131 rows total)
OK   generated/723-Italian-canonical.txt contains exactly the 78 official RA asset IDs
OK   local_id <-> official_asset_id mapping is a bijection over all 78 assets, every local_id >= FirstLocalId (111000001)
OK   all 78 local smoke-test lines are byte-identical to their canonical counterpart except the ID token

AUDIT PASSED: all checks green, 0 unresolved addresses
```

### French — as last run against the full official asset set

`verify_phase8_remap.py --target-version french` passes in full, including
the 81978 override. Generation totals from that run: 78 assets (76
achievements + 2 leaderboards), 693 conditions processed, 279 memory
references processed (28 unchanged, 701 relocated, 1 explicit exception),
**0 unresolved addresses**. Same 7-check audit, same pass criteria as
Italian above — this is the static/generation half of validation only; see
[French's dynamic-testing.md](../french/docs/dynamic-testing.md) for what
runtime testing has and hasn't been done.

### German — as last run against the full official asset set

Generation totals: 78 assets (76 achievements + 2 leaderboards), 693
conditions processed, 279 memory references processed (32 unchanged, 701
relocated, 1 explicit exception), **0 unresolved addresses**. Same 7-check
audit, same pass criteria as Italian and French above — this is the
static/generation half of validation only; see
[German's dynamic-testing.md](../german/docs/dynamic-testing.md) for what
runtime testing has and hasn't been done.

### Spanish — as last run against the full official asset set

Generation totals: 78 assets (76 achievements + 2 leaderboards), 693
conditions processed, 279 memory references processed (33 unchanged, 701
relocated, 1 explicit exception), **0 unresolved addresses**. Same 7-check
audit, same pass criteria as Italian, French, and German above — this is
the static/generation half of validation only; see
[Spanish's dynamic-testing.md](../spanish/docs/dynamic-testing.md) for
what runtime testing has and hasn't been done.

(78 = 76 achievements + 2 leaderboards, for every locale; Rich Presence is
generated and verified alongside but isn't a numbered RA "asset" in this
count.)

## Provenance

[`data/italian_provenance_report.csv`](../italian/data/italian_provenance_report.csv),
[`data/french_provenance_report.csv`](../french/data/french_provenance_report.csv),
[`data/german_provenance_report.csv`](../german/data/german_provenance_report.csv),
and [`data/spanish_provenance_report.csv`](../spanish/data/spanish_provenance_report.csv)
are the per-asset result of each locale's audit: for each of the 78
generated assets, its source/target memory references, how many addresses
were relocated, and its final status (`RELOCATED` or the one documented
`EXCEPTION`). They're the direct evidence backing the audit summaries
above.

## Regression protection

Before the Italian snapshot was published, the generator's output was
diffed against the 7 achievements that were actually run on real hardware
(see [dynamic-testing.md](../italian/docs/dynamic-testing.md)), so a future
change to the triage data or the substitution engine in the private repo
can't silently drift away from what was physically confirmed to work
in-game. **None of French, German, or Spanish has an equivalent regression
check yet** — since no achievement in any of those locales has been run as
a local achievement in RAIntegration, there's nothing physically confirmed
to diff against (see [French's](../french/docs/dynamic-testing.md),
[German's](../german/docs/dynamic-testing.md), and
[Spanish's](../spanish/docs/dynamic-testing.md) dynamic-testing docs).
