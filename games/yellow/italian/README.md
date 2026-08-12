# Pokémon Yellow (Italian) — RetroAchievements Game 723 Compatibility

**Status: investigation complete, ready for maintainer review.**

The official Italian release of Pokémon Yellow ("Pokémon — Versione Gialla:
Edizione Speciale Pikachu") does not share all of the WRAM addresses used by
[RetroAchievements Game 723](https://retroachievements.org/game/723) (76
achievements, 2 leaderboards, Rich Presence — authored against the English
release). This project shows that the mismatch is **not** a random or
global relocation: a single, bounded WRAM region is 5 bytes longer in the
Italian ROM, and every RA-referenced address either sits entirely before
that region (unchanged) or entirely after it (shifted by exactly `+5`). It
maps all 131 RA-referenced addresses across that boundary, generates a
translated Italian asset set deterministically from the official set, and
backs the result with both static auditing and real-hardware dynamic
testing.

This is the polished result for a Game 723 maintainer or RA QA team, and
the only fully runtime-verified target in the [Gen I/II regional
compatibility project](../../../README.md) this repo is part of — see also
[Pokémon Yellow (French)](../french/README.md), whose address mapping and
generation are complete but not yet runtime-tested. The full research
process — every dead end, every intermediate hypothesis — lives in a
separate private working repository and is not reproduced here.

## Headline results

| | |
|---|---|
| Game | Pokémon Yellow — official Italian retail release |
| RetroAchievements | [Game 723](https://retroachievements.org/game/723) — 76 achievements, 2 leaderboards, Rich Presence |
| RA addresses resolved | **131 / 131 (100%), 0 unresolved** |
| Relocation model | Bounded WRAM region, not a global offset — see [docs/wram-relocation-model.md](docs/wram-relocation-model.md) |
| Address breakdown | 99 addresses relocated `+5`, 30 addresses unchanged, 2 tied to the documented 81978 exception below |
| Localisation-specific exception | Exactly one: achievement 81978 (value rewrite, not an address change — see below) |
| Targeted dynamic (real-hardware) tests | **7 / 7 passed** |
| Byte-for-byte dynamic match | 6 dynamically tested official achievements match the generator's output exactly |
| Offline generation + audit | Full 76-achievement / 2-leaderboard / Rich Presence set generates cleanly; audit reports 0 unresolved addresses, PASSED |
| Full-set RAIntegration load | Manually verified by the project author: complete generated set loaded as **76 achievements / 458 points**, and one achievement (**Not Mad, Just Disappointed**) triggered naturally from a fresh Italian save under that full set. *(Manual runtime observation — not reproduced by the scripts in this repo. See note below.)* |

## Try it locally

Copy these two generated files into your RetroAchievements `RACache/Data/`
folder (with the Italian ROM loaded and RAIntegration in Compatibility Test
mode):

| Generated file | Copy to |
|---|---|
| [`generated/723-Italian-User.txt`](generated/723-Italian-User.txt) | `RACache/Data/723-User.txt` |
| [`generated/rich_presence_italian.txt`](generated/rich_presence_italian.txt) | `RACache/Data/723-Rich.txt` |

Use the **User** file, not
[`generated/723-Italian-canonical.txt`](generated/723-Italian-canonical.txt),
for local testing. The local file uses synthetic IDs starting at
RAIntegration's `FirstLocalId` (`111000001`) because, against an unrecognized
ROM hash, RAIntegration only merges a local line onto an official asset
*already loaded from the server* — and no such official Game 723 objects
exist in memory for a ROM it doesn't recognize, so an official-ID line loads
zero achievements. IDs at or above `FirstLocalId` are always created fresh as
local assets instead. The canonical file keeps the official RA asset IDs
precisely so a maintainer can diff/merge it against the real set — it is the
submission reference, not something to load locally. See [Generated files,
two formats](#generated-files-two-formats--read-this-before-loading-anything)
below for the full explanation.

## What differs in the Italian ROM

Binary diff of the two retail ROMs (hash-verified against their known
English/Italian identities) shows 30.5% of bytes differ across 46 of 64
banks — consistent with a full text/name-table retranslation and repack,
not a minimal patch. That alone says nothing about whether RetroAchievements'
runtime WRAM addresses still line up. They mostly don't: the Italian binary
has one contiguous WRAM region that is 5 bytes longer than the English
layout (pinned to a 4-byte source-level window,
`0xcf07`–`0xcf0a`), and everything after it in WRAM0 is displaced by exactly
`+5`. Everything before it is untouched.

## WRAM relocation model

Rather than assume a single global offset (wrong — it produces garbage
matches on either side of the boundary) or treat every address as
independently unknown (too conservative — the actual pattern is highly
regular), this project falsifies the relocation structurally: filtering ROM
cross-reference evidence to high-confidence banks collapses the address
deltas into a clean bimodal split — `+5` (214 evidenced sites) and `+0` (207
evidenced sites), with every other observed delta a one-off coincidental
opcode match. Full derivation, including the boundary-pinning method and a
root-caused off-by-one correction along the way: [docs/wram-relocation-model.md](docs/wram-relocation-model.md).

## The 131-address mapping

Every RA-referenced address (achievements + leaderboards + Rich Presence)
is individually classified — `IDENTICAL` (30) or `RELOCATED` (101, 99 at
`+5`, 2 tied to the 81978 exception below) — with its own evidence citation
inline, in [`data/ra_address_triage.csv`](data/ra_address_triage.csv). The
per-asset result of applying that classification — source/Italian memory
references, relocation counts, and final status per asset — is in
[`data/italian_provenance_report.csv`](data/italian_provenance_report.csv).
The broader derivation tables (the full pret-symbol WRAM table, the
separate map-ID literal axis, the dynamic test protocol) live in the
private research repo, not in this snapshot — see
[docs/generation-report.md](../docs/generation-report.md) for what was
checked before publication.

## Achievement 81978 — the one non-address exception

"You're Not Getting Away from Me That Easily" hardcodes 17 literal English
dialogue-tile bytes at `0xc4e1–0xc4f1`. Live dialogue capture on the Italian
ROM confirms **the address range itself is unshifted** — this is the one
place in the whole set where the relocation model correctly predicts *no*
change — but the literal bytes must change, because the Italian line is
different (and two bytes shorter). This is a value/literal rewrite, not an
address relocation, and is the only asset in the set that needs one. Full
byte-level derivation: [docs/dynamic-testing.md](docs/dynamic-testing.md).

## Generation architecture

The Italian asset set was produced by a generic address-substitution
engine ([`shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py),
shared across every game/locale in this project, included here for
transparency) driven by a per-locale `LocalizationConfig` — the Italian
pass is a thin config on top of it, so a new locale pass (as
[French](../french/README.md) already demonstrates) only needs its own
address-triage CSV, not a new copy of the engine. The
config itself, and the driver script that turns its output into the two
loadable RA-format files under [`generated/`](generated/) — see
**Generated files, two formats** below — live in the private research
repo, since both need RA's own raw achievement export to run. Details of
what was generated and how: [docs/generation-report.md](../docs/generation-report.md).

## Automated validation

Before this snapshot was published, the private research repo ran a
7-point audit — 1:1 asset mapping, unchanged metadata
(title/description/points/type/author), preserved condition structure
(except the documented 81978 exception), 0 unresolved addresses across all
131 RA-referenced addresses, canonical/local file correctness, and an
independent re-derivation of the substitution diffed against the actual
output — plus a regression check diffing the generator's output against
the 7 achievements actually run on real hardware, so a future regeneration
can't silently drift from what was physically tested. Full results:
[docs/generation-report.md](../docs/generation-report.md). This snapshot
doesn't include the audit scripts themselves — they depend on the same
private RA export the generator does — but does include their result
([`data/italian_provenance_report.csv`](data/italian_provenance_report.csv))
and the evidence it was checked against
([`data/ra_address_triage.csv`](data/ra_address_triage.csv)).

## Dynamic gameplay testing

7 targeted tests were run against a real Italian ROM in BizHawk +
RAIntegration (Compatibility Test mode, local achievements, Pause on
Trigger used for final captures):

| Test | Result |
|---|---|
| 81978 — You're Not Getting Away from Me That Easily (literal rewrite) | **PASS** |
| King of the Dojo | **PASS** |
| Silph Co. Rival / Do We REALLY Have to Do This Now? | **PASS** |
| Pokédex Seen/Owned operand probes (two independent array offsets) | **PASS** |
| Showdown in Pewter City | **PASS** |
| Fish Out Of Water | **PASS** |
| That's Shocking! (full Elite Four/Champion sequence) | **PASS** |

All 7 fired correctly against the translated addresses/values, independently
validating both the `+5` relocation model and the 81978 literal rewrite
under real game logic — not just static byte comparison. Full test-by-test
detail: [docs/dynamic-testing.md](docs/dynamic-testing.md).

## Full-set RAIntegration smoke test

After generating the complete 76-achievement / 2-leaderboard / Rich
Presence Italian set, the project author manually loaded it into
RAIntegration against the Italian ROM and observed:

- all 76 achievements loaded, totalling **458 points**;
- a natural, unprompted trigger of **Not Mad, Just Disappointed** from a
  fresh Italian save under Pause on Trigger.

**This is a manual runtime observation by the project author, not something
reproduced or verified by the scripts in this repository.** It is reported
here as-is, distinct from the automated static validation and the 7
scripted dynamic tests above, which are independently reproducible.

## Reproduction

This is a **published evidence/handoff snapshot**, not a runnable
reproduction of the generation pipeline. All the automated
generation and auditing described above was performed in the private
research repository this snapshot was published from, against
RetroAchievements' own raw achievement/Rich Presence export for Game
723 — content that belongs to RA/its authors, not to this project, so it
isn't published here (no `imports/ra/` export, no source
`ra_asset_definitions.csv`, no generation scripts).

What you *can* verify directly from this repo, without any RA export:

- **Read the evidence.** [`data/ra_address_triage.csv`](data/ra_address_triage.csv)
  classifies all 131 addresses with an inline evidence citation per row;
  [`data/italian_provenance_report.csv`](data/italian_provenance_report.csv)
  shows the resulting per-asset substitution.
- **Load the output.** [`generated/723-Italian-User.txt`](generated/723-Italian-User.txt)
  and [`generated/rich_presence_italian.txt`](generated/rich_presence_italian.txt)
  are the actual generated files — see **Try it locally** above to load
  them against the real Italian ROM.
- **Read the engine.** [`shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py)
  is the actual substitution engine that produced the output above, included
  for transparency (it isn't runnable standalone here — its
  `LocalizationConfig` and source RA definitions are private-repo-only).

If you're a Game 723 maintainer and want the candidate patch regenerated
(e.g. against a fresh official RA export after an upstream change), reach
out to the project author — see
[docs/maintainer-handoff.md](../docs/maintainer-handoff.md).

## Generated files, two formats — read this before loading anything

The generator produced **two different files that must not be confused**:

- **Canonical file** (`generated/723-Italian-canonical.txt`) — keyed by the
  official RA asset IDs. This is the provenance/submission reference: the
  form a maintainer would actually merge.
- **Local smoke-test file** (`generated/723-Italian-User.txt`) — keyed by
  synthetic local IDs starting at RAIntegration's `FirstLocalId`
  (`111000001`). **This is the only form RAIntegration will actually load**
  against an unrecognized ROM hash in Compatibility Test mode — the
  official-ID file alone produces **zero** loadable achievements, because
  RAIntegration only merges sub-`FirstLocalId` lines onto achievements
  already loaded from the server, which don't exist for a ROM it doesn't
  recognize. To test locally, copy the local file to
  `RACache/Data/723-User.txt`.

Don't repeat the zero-achievement loading mistake made during this
investigation — use the local file for local testing, the canonical file
for anything you send to a maintainer.

## Rich Presence

The generator also produced a translated Italian Rich Presence definition
([`generated/rich_presence_italian.txt`](generated/rich_presence_italian.txt)).
For manual RAIntegration testing it is copied to
`RACache/Data/723-Rich.txt` — see **Try it locally** above.

## ROM / legal note

**No ROM is provided in this repository, and none will be.** The ROM hashes
below are provided purely for identification, so a maintainer can confirm
they're looking at the same binaries this investigation used — they are not
copyrighted content.

| ROM | MD5 | SHA-1 |
|---|---|---|
| English ("Yellow Version — Special Pikachu Edition") | `d9290db87b1f0a23b89f99ee4469e34b` | `cc7d03262ebfaf2f06772c1a480c7d9d5f4a38e1` |
| Italian ("Versione Gialla — Speciale Edizione Pikachu") | `3343ceca5dd6586e4774609526167d55` | `05bb8e99f24d498613930949730afa8024e77d08` |

The English SHA-1 matches the hash the `pret/pokeyellow` disassembly builds
from, so its public symbol table is used as the reference for WRAM naming
throughout this project.

## Repository contents

This target lives at `games/yellow/italian/` within the larger
[Gen I/II regional compatibility project](../../../README.md); paths below
are relative to this directory unless noted.

```
README.md  (this file)
../docs/                       shared across every games/yellow/<locale>/ target
    methodology.md            how the investigation approached the problem
    generation-report.md      what was generated and how it was audited
    maintainer-handoff.md     current status + suggested next step
docs/                          Italian-specific
    wram-relocation-model.md  the +5 bounded-region proof, in full
    dynamic-testing.md        all 7 targeted dynamic tests + the 81978 case
data/
    ra_address_triage.csv           the 131 RA-referenced addresses, classified,
                                     with an inline evidence citation per row
    italian_provenance_report.csv   per-asset result of applying that classification
generated/
    723-Italian-canonical.txt   official RA asset IDs — submission/provenance reference
    723-Italian-User.txt        synthetic local IDs — load this one locally, see above
    rich_presence_italian.txt   translated Rich Presence
```

This snapshot deliberately doesn't include the generation/audit scripts
(they depend on RA's own raw achievement export, not this project's to
publish) or the broader derivation tables the private research repo used
to build `ra_address_triage.csv` (the full pret-symbol WRAM table, the
separate map-ID literal axis, the raw dynamic-test protocol) — those stay
in the private repo, which remains the authoritative full research/tooling
repository. What's here is the result and the evidence backing it.

The one piece of tooling included is the generic address-substitution
engine itself, shared by every game/locale in this project:
[`../../../shared/scripts/asset_localizer.py`](../../../shared/scripts/asset_localizer.py)
(plus its `csv_safety.py` dependency) — included for transparency, not as
a runnable pipeline.

## Current next step

This project is ready for RetroAchievements compatibility testing /
maintainer review of Game 723. See
[docs/maintainer-handoff.md](../docs/maintainer-handoff.md) for what's proven,
what's still open, and a suggested path to get an official Italian-compatible
patch reviewed.
